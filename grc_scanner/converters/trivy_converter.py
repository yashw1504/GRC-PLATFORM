"""Convert Trivy JSON output to Finding objects"""
from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine

class TrivyConverter:
    @staticmethod
    def convert(raw_results: dict) -> list:
        findings = []
        if not raw_results:
            return findings

        for result in raw_results.get("Results", []):
            target = result.get("Target", "unknown")
            vulns = result.get("Vulnerabilities", [])

            for vuln in vulns:
                severity = vuln.get("Severity", "Unknown")
                finding = Finding(
                    check_id=vuln.get("VulnerabilityID", "trivy_unknown"),
                    name=vuln.get("Title", "Unknown Trivy Finding"),
                    status="fail",
                    severity=severity,
                    description=vuln.get("Description", ""),
                    evidence=f"{target}: {vuln.get('PkgName', '')} {vuln.get('InstalledVersion', '')}",
                    category="Vulnerability",
                    target_asset=target,
                    scanner_name="trivy",
                    remediation=vuln.get("FixedVersion", "No fix available"),
                    raw_data=vuln
                )
                finding = RiskEngine.enrich_finding(finding)
                findings.append(finding)

        return findings