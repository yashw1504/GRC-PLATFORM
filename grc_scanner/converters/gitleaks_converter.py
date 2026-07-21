"""Convert Gitleaks JSON output to Finding objects"""
from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine

class GitleaksConverter:
    @staticmethod
    def convert(raw_results: list) -> list:
        findings = []
        if not raw_results:
            return findings

        # Gitleaks can return a list directly
        items = raw_results if isinstance(raw_results, list) else []

        for item in items:
            if isinstance(item, dict):
                finding = Finding(
                    check_id=item.get("rule_id", "gitleaks_unknown"),
                    name=f"Secret Leaked: {item.get('rule', 'Unknown')}",
                    status="fail",
                    severity="Critical",
                    description=f"Secret detected: {item.get('description', '')}",
                    evidence=f"{item.get('file', '')}:{item.get('start_line', '')}",
                    category="Secrets",
                    target_asset=item.get("file", ""),
                    scanner_name="gitleaks",
                    remediation="Rotate the secret immediately. Remove from source control.",
                    raw_data=item
                )
                finding = RiskEngine.enrich_finding(finding)
                findings.append(finding)

        return findings