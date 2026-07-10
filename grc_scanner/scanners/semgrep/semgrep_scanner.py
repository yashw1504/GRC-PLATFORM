from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine

from grc_scanner.integrations.semgrep_wrapper import (
    SemgrepWrapper
)


class SemgrepScanner:

    name = "semgrep_scanner"

    def scan(self, path):

        if not SemgrepWrapper.is_available():
            return []

        findings = []

        results = SemgrepWrapper.scan(path)

        for item in results:

            extra = item.get("extra", {})

            metadata = extra.get("metadata", {})

            severity = extra.get(
                "severity",
                "WARNING"
            ).lower()

            if severity == "error":
                severity = "Critical"
            elif severity == "warning":
                severity = "High"
            elif severity == "info":
                severity = "Low"
            else:
                severity = "Medium"

            findings.append(

                self._create_finding(

                    check_id=item.get(
                        "check_id",
                        "semgrep_rule"
                    ),

                    name=item.get(
                        "check_id",
                        "Semgrep Finding"
                    ),

                    status="fail",

                    severity=severity,

                    description=extra.get(
                        "message",
                        "Semgrep finding"
                    ),

                    evidence=(
                        f"{item.get('path')} : "
                        f"Line {item.get('start', {}).get('line')}"
                    ),

                    business_impact=(
                        "Potential source code vulnerability."
                    ),

                    remediation=(
                        metadata.get(
                            "fix",
                            "Review the affected code."
                        )
                    ),

                    recommendation=(
                        metadata.get(
                            "references",
                            ["Review Semgrep documentation."]
                        )[0]
                        if metadata.get("references")
                        else "Review Semgrep documentation."
                    ),

                    category="SAST"

                )

            )

        return findings

    def _create_finding(
        self,
        check_id,
        name,
        status,
        severity,
        description,
        evidence,
        business_impact,
        remediation,
        recommendation,
        category
    ):

        finding = Finding(
            check_id=check_id,
            name=name,
            status=status,
            severity=severity,
            description=description,
            evidence=evidence,
            business_impact=business_impact,
            remediation=remediation,
            recommendation=recommendation,
            category=category,
            scanner_name=self.name,
            target_type="source"
        )

        return RiskEngine.enrich_finding(
            finding
        )