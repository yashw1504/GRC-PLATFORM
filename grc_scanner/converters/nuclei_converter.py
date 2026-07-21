"""Convert Nuclei JSON output to Finding objects"""
from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine

class NucleiConverter:
    SEVERITY_MAP = {
        "critical": "Critical",
        "high": "High",
        "medium": "Medium",
        "low": "Low",
        "info": "Info",
        "unknown": "Info"
    }

    @staticmethod
    def convert(raw_results: list) -> list:
        findings = []
        if not raw_results:
            return findings

        for item in raw_results:
            if isinstance(item, dict):
                info = item.get("info", {})
                severity_raw = info.get("severity", "info").lower()
                severity = NucleiConverter.SEVERITY_MAP.get(severity_raw, "Info")

                finding = Finding(
                    check_id=item.get("template-id", "nuclei_unknown"),
                    name=info.get("name", "Unknown Nuclei Finding"),
                    status="fail" if severity in ("Critical", "High", "Medium") else "info",
                    severity=severity,
                    description=info.get("description", ""),
                    evidence=item.get("matched-at", item.get("host", "")),
                    category="Vulnerability",
                    target_asset=item.get("host", ""),
                    scanner_name="nuclei",
                    remediation=info.get("remediation", ""),
                    recommendation=info.get("recommendation", ""),
                    raw_data=item
                )
                finding = RiskEngine.enrich_finding(finding)
                findings.append(finding)

        return findings