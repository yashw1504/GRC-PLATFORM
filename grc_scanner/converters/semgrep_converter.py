"""Convert Semgrep JSON output to Finding objects"""
from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine

class SemgrepConverter:
    SEVERITY_MAP = {
        "ERROR": "Critical",
        "WARNING": "High",
        "INFO": "Medium"
    }

    @staticmethod
    def convert(raw_results: dict) -> list:
        findings = []
        results = raw_results.get("results", []) if isinstance(raw_results, dict) else []

        for item in results:
            sev_raw = item.get("extra", {}).get("severity", "INFO")
            severity = SemgrepConverter.SEVERITY_MAP.get(sev_raw, "Info")

            finding = Finding(
                check_id=item.get("check_id", "semgrep_unknown"),
                name=item.get("extra", {}).get("message", "Unknown Semgrep Finding"),
                status="fail",
                severity=severity,
                description=item.get("extra", {}).get("message", ""),
                evidence=f"{item.get('path', '')}:{item.get('start', {}).get('line', '')}",
                category="SAST",
                target_asset=item.get("path", ""),
                scanner_name="semgrep",
                remediation=item.get("extra", {}).get("fix", ""),
                raw_data=item
            )
            finding = RiskEngine.enrich_finding(finding)
            findings.append(finding)

        return findings