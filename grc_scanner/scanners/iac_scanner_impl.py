"""IaC scanner using Checkov"""
from grc_scanner.scanners.base_scanner import BaseScanner
from grc_scanner.integrations.checkov_wrapper import CheckovWrapper

class IaCScanner(BaseScanner):
    def __init__(self):
        self.name = "IaCScanner"

    def scan(self, path=".", **kwargs):
        if not CheckovWrapper.is_available():
            print("[IaCScanner] Checkov not available")
            return []
        print(f"[IaCScanner] Scanning IaC in {path}")
        raw = CheckovWrapper.scan(path)
        findings = []
        for item in raw if isinstance(raw, list) else []:
            if isinstance(item, dict):
                for failed in item.get("results", {}).get("failed_checks", []):
                    findings.append({
                        "check_id": failed.get("check_id", "checkov_unknown"),
                        "name": failed.get("check_name", "Unknown"),
                        "status": "fail",
                        "severity": failed.get("severity", "Medium"),
                        "evidence": f"{failed.get('file_line_range', '')}"[:200],
                        "category": "IaC",
                        "scanner_name": "checkov"
                    })
        return findings