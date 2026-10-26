from typing import List

from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine


class FindingNormalizer:

    @staticmethod
    def normalize(findings: List[Finding]):

        normalized = []

        for finding in findings:

            if not isinstance(finding, Finding):
                continue

            if not finding.category:
                finding.category = "General"

            if not finding.target_type:
                finding.target_type = "unknown"

            if not finding.scanner_name:
                finding.scanner_name = "unknown"

            if not finding.status:
                finding.status = "info"
            finding.status = str(finding.status).lower()

            if not finding.severity:
                finding.severity = "Info"
            else:
                severity = str(finding.severity).strip().lower()
                finding.severity = {
                    "critical": "Critical",
                    "high": "High",
                    "medium": "Medium",
                    "moderate": "Medium",
                    "low": "Low",
                    "info": "Info",
                    "informational": "Info",
                }.get(severity, "Info")

            raw_data = finding.raw_data or {}
            finding.cve_id = finding.cve_id or str(
                raw_data.get("cve") or raw_data.get("cve_id") or ""
            )
            finding.cve_id = finding.cve_id.strip().upper()
            if finding.cvss_score is None:
                raw_cvss = raw_data.get("cvss_score", raw_data.get("cvss"))
                try:
                    finding.cvss_score = float(raw_cvss) if raw_cvss is not None else None
                except (TypeError, ValueError):
                    finding.cvss_score = None

            RiskEngine.enrich_finding(finding)

            normalized.append(finding)

        return normalized
