"""Secrets scanner using Gitleaks"""
from grc_scanner.scanners.base_scanner import BaseScanner
from grc_scanner.integrations.gitleaks_wrapper import GitleaksWrapper

class SecretsScanner(BaseScanner):
    def __init__(self):
        self.name = "SecretsScanner"

    def scan(self, path=".", **kwargs):
        if not GitleaksWrapper.is_available():
            print("[SecretsScanner] Gitleaks not available")
            return []

        print(f"[SecretsScanner] Scanning for secrets in {path}")
        raw = GitleaksWrapper.scan(path)
        if isinstance(raw, list):
            return [{
                "check_id": item.get("rule_id", "gitleaks_unknown"),
                "name": f"Secret: {item.get('rule', 'Unknown')}",
                "status": "fail",
                "severity": "Critical",
                "evidence": f"{item.get('file', '')}:{item.get('start_line', '')}"[:200],
                "scanner_name": "gitleaks"
            } for item in raw if isinstance(item, dict)]
        return []