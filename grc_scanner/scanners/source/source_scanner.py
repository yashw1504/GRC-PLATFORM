from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine
from grc_scanner.integrations.semgrep_wrapper import SemgrepWrapper


class SourceScanner:
    name = "source_scanner"

    def scan(self, path="."):
        findings = []

        if not SemgrepWrapper.is_available():
            return findings

        results = SemgrepWrapper.scan(path)

        for item in results:
            findings.append(
                self._create_finding(
                    item.get("check_id", "source_issue"),
                    item.get("name", "Source Code Issue"),
                    "fail",
                    "Medium",
                    item.get("message", "Potential source code issue"),
                    item.get("path", path),
                    "Source code risk",
                    "Review code",
                    "Fix the issue",
                    "Source Code"
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

        return RiskEngine.enrich_finding(finding)