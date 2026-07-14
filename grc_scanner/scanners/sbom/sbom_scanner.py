import os
import tempfile

from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine

from grc_scanner.integrations.syft_wrapper import SyftWrapper
from grc_scanner.integrations.grype_wrapper import GrypeWrapper


class SBOMScanner:

    name = "sbom_scanner"

    def scan(self, target="."):

        if (
            SyftWrapper.is_available()
            and
            GrypeWrapper.is_available()
        ):
            return self._scan_real(target)

        print("SBOM: Falling back to demo mode")

        return self._scan_demo()

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

            target_type="sbom"
        )

        return RiskEngine.enrich_finding(
            finding
        )