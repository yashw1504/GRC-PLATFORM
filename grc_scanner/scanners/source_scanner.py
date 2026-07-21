"""Source code scanner using Semgrep"""
from grc_scanner.scanners.base_scanner import BaseScanner
from grc_scanner.integrations.semgrep_wrapper import SemgrepWrapper

class SourceScanner(BaseScanner):
    def __init__(self):
        self.name = "SourceScanner"

    def scan(self, path=".", **kwargs):
        findings = []
        if SemgrepWrapper.is_available():
            print(f"[SourceScanner] Running Semgrep on {path}")
            raw = SemgrepWrapper.scan(path)
            if isinstance(raw, dict):
                for item in raw.get("results", []):
                    findings.append({
                        "check_id": item.get("check_id", "semgrep_unknown"),
                        "name": item.get("extra", {}).get("message", "Unknown")[:200],
                        "status": "fail",
                        "severity": item.get("extra", {}).get("severity", "WARNING"),
                        "evidence": f"{item.get('path', '')}:{item.get('start', {}).get('line', '')}"[:200],
                        "category": "SAST",
                        "scanner_name": "semgrep"
                    })
        return findings