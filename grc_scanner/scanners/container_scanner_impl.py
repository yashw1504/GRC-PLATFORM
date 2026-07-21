"""Container scanner using Trivy"""
from grc_scanner.scanners.base_scanner import BaseScanner
from grc_scanner.integrations.trivy_wrapper import TrivyWrapper

class ContainerScanner(BaseScanner):
    def __init__(self):
        self.name = "ContainerScanner"

    def scan(self, path=".", **kwargs):
        if not TrivyWrapper.is_available():
            print("[ContainerScanner] Trivy not available")
            return []
        print(f"[ContainerScanner] Running Trivy on {path}")
        raw = TrivyWrapper.scan(path)
        findings = []
        if isinstance(raw, dict):
            for result in raw.get("Results", []):
                target = result.get("Target", "unknown")
                for vuln in result.get("Vulnerabilities", []):
                    findings.append({
                        "check_id": vuln.get("VulnerabilityID", "trivy_unknown"),
                        "name": vuln.get("Title", "Unknown")[:200],
                        "status": "fail",
                        "severity": vuln.get("Severity", "Medium"),
                        "evidence": f"{target}: {vuln.get('PkgName', '')}"[:200],
                        "category": "Vulnerability",
                        "scanner_name": "trivy"
                    })
        return findings