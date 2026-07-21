"""Convert Checkov JSON output to Finding objects"""
from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine

class CheckovConverter:
    @staticmethod
    def convert(raw_results: list) -> list:
        findings = []

        for item in raw_results:
            if isinstance(item, dict):
                # Checkov output structure
                for check_type in item.get("results", {}).get("passed_checks", []):
                    pass  # We skip passed checks

                for failed_check in item.get("results", {}).get("failed_checks", []):
                    severity = failed_check.get("severity", "Medium")
                    finding = Finding(
                        check_id=failed_check.get("check_id", "checkov_unknown"),
                        name=failed_check.get("check_name", "Unknown Checkov Finding"),
                        status="fail",
                        severity=severity,
                        description=failed_check.get("check_name", ""),
                        evidence=f"{failed_check.get('resource', '')}:{failed_check.get('file_line_range', '')}",
                        category="IaC Misconfiguration",
                        target_asset=failed_check.get("repo_file_path", ""),
                        scanner_name="checkov",
                        remediation=failed_check.get("guideline", ""),
                        raw_data=failed_check
                    )
                    finding = RiskEngine.enrich_finding(finding)
                    findings.append(finding)

        return findings