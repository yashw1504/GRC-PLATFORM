import os
import tempfile

from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine

from grc_scanner.integrations.syft_wrapper import SyftWrapper
from grc_scanner.integrations.grype_wrapper import GrypeWrapper
from grc_scanner.engine.scanner_errors import scanner_error_finding


class SBOMScanner:

    name = "sbom_scanner"

    def scan(self, target="."):

        if (
            SyftWrapper.is_available()
            and
            GrypeWrapper.is_available()
        ):
            return self._scan_real(target)

        missing = []
        if not SyftWrapper.is_available():
            missing.append("Syft")
        if not GrypeWrapper.is_available():
            missing.append("Grype")
        return [scanner_error_finding(
            self.name,
            f"Required SBOM tooling is unavailable: {', '.join(missing)}.",
            target,
            category="SBOM",
        )]

    def _scan_real(self, target):

        findings = []

        sbom_file = tempfile.NamedTemporaryFile(
            suffix=".json",
            delete=False
        ).name

        try:

            generated = SyftWrapper.generate(
                target,
                sbom_file
            )

            if not generated:
                return []

            results = GrypeWrapper.scan(
                sbom_file
            )

            if not isinstance(results, dict):
                return []

            matches = results.get(
                "matches",
                []
            )

            for match in matches:

                vulnerability = match.get(
                    "vulnerability",
                    {}
                )

                artifact = match.get(
                    "artifact",
                    {}
                )

                findings.append(
                    self._create_finding(
                        vulnerability,
                        artifact
                    )
                )

        finally:

            if os.path.exists(sbom_file):
                os.remove(sbom_file)

        return findings

    def _scan_demo(self):

        findings = []

        findings.append(
            self._demo_finding(
                "sbom_missing",
                "SBOM Missing",
                "High"
            )
        )

        return findings

    def _demo_finding(
        self,
        check_id,
        name,
        severity
    ):

        finding = Finding(
            check_id=check_id,
            name=name,
            status="fail",
            severity=severity,
            description=name,
            evidence="Demo Mode",
            business_impact="Supply Chain Risk",
            remediation="Generate SBOM",
            recommendation="Install Syft",
            category="SBOM",
            scanner_name=self.name,
            target_type="sbom"
        )

        return RiskEngine.enrich_finding(
            finding
        )

    def _create_finding(
        self,
        vulnerability,
        artifact
    ):

        severity = vulnerability.get(
            "severity",
            "Medium"
        ).capitalize()

        evidence = (
            f'{artifact.get("name","")} '
            f'{artifact.get("version","")}'
        )

        description = vulnerability.get(
            "description",
            ""
        )

        if len(description) > 500:
            description = description[:500]

        cvss_score = None
        cvss_records = vulnerability.get("cvss", []) or []
        if isinstance(cvss_records, dict):
            cvss_records = [cvss_records]
        for score_record in cvss_records:
            metrics = score_record.get("metrics", {})
            raw_score = metrics.get("baseScore") or metrics.get("cvssData", {}).get("baseScore")
            try:
                candidate = float(raw_score)
            except (TypeError, ValueError):
                continue
            cvss_score = max(cvss_score or 0, candidate)

        finding = Finding(

            check_id=vulnerability.get(
                "id",
                "CVE"
            ),

            name=vulnerability.get(
                "id",
                "Unknown CVE"
            ),

            status="fail",

            severity=severity,

            description=description,

            evidence=evidence,

            business_impact="Known vulnerable dependency.",

            remediation="Upgrade to a fixed version.",

            recommendation="Update or replace dependency.",

            category="SBOM",

            scanner_name=self.name,

            target_type="sbom",
            cve_id=str(vulnerability.get("id", "")),
            cvss_score=cvss_score,
            target_asset=evidence,
            raw_data={"vulnerability": vulnerability, "artifact": artifact}
        )

        return RiskEngine.enrich_finding(
            finding
        )
