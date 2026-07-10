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

            severity = str(
                extra.get(
                    "severity",
                    "WARNING"
                )
            ).lower()

            if severity == "error":
                severity = "Critical"
            elif severity == "warning":
                severity = "High"
            elif severity == "info":
                severity = "Low"
            else:
                severity = "Medium"

            check_id = item.get(
                "check_id",
                "semgrep_rule"
            )

            name = (
                extra.get("message")
                or metadata.get("shortDescription")
                or check_id
            )

            path_name = item.get(
                "path",
                "Unknown"
            )

            line = (
                item.get(
                    "start",
                    {}
                ).get(
                    "line",
                    "?"
                )
            )

            code = extra.get(
                "lines",
                ""
            )

            evidence = (
                f"File: {path_name}\n"
                f"Line: {line}\n"
                f"{code}"
            )

            fix = metadata.get(
                "fix"
            )

            references = metadata.get(
                "references",
                []
            )

            if isinstance(
                references,
                str
            ):
                references = [references]

            if fix:
                recommendation = fix

            elif references:
                recommendation = references[0]

            else:
                recommendation = (
                    "Review and remediate the affected code."
                )

            business_impact = (
                "Potential source code vulnerability "
                "identified during static analysis."
            )

            rule = check_id.lower()

            if "sql" in rule:
                category = "Injection"

            elif "xss" in rule:
                category = "Cross-Site Scripting"

            elif "command" in rule:
                category = "Command Injection"

            elif "jwt" in rule:
                category = "Authentication"

            elif "secret" in rule:
                category = "Secrets"

            elif "github-actions" in rule:
                category = "CI/CD"

            elif "docker" in rule:
                category = "Container"

            else:
                category = "SAST"

            findings.append(

                self._create_finding(

                    check_id=check_id,

                    name=name,

                    status="fail",

                    severity=severity,

                    description=extra.get(
                        "message",
                        "Semgrep finding"
                    ),

                    evidence=evidence,

                    business_impact=business_impact,

                    remediation=(
                        "Fix the affected code according "
                        "to secure coding practices."
                    ),

                    recommendation=recommendation,

                    category=category

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