"""Source code scanner - Semgrep SAST + Gitleaks"""
from grc_scanner.scanners.base_scanner import BaseScanner
from grc_scanner.integrations.semgrep_wrapper import SemgrepWrapper
from grc_scanner.integrations.gitleaks_wrapper import GitleaksWrapper
from grc_scanner.converters.semgrep_converter import SemgrepConverter
from grc_scanner.converters.gitleaks_converter import GitleaksConverter

class SourceScanner(BaseScanner):
    def __init__(self):
        self.name = "SourceScanner"

    def scan(self, path=".", **kwargs):
        all_findings = []

        # SAST with Semgrep
        if SemgrepWrapper.is_available():
            print(f"[SourceScanner] Running Semgrep on {path}")
            raw = SemgrepWrapper.scan(path)
            all_findings.extend(SemgrepConverter.convert(raw))

        # Secrets with Gitleaks
        if GitleaksWrapper.is_available():
            print(f"[SourceScanner] Running Gitleaks on {path}")
            raw = GitleaksWrapper.scan(path)
            all_findings.extend(GitleaksConverter.convert(raw))

        return all_findings