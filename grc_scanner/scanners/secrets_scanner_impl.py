"""Secrets scanner using Gitleaks"""
from grc_scanner.scanners.base_scanner import BaseScanner
from grc_scanner.integrations.gitleaks_wrapper import GitleaksWrapper
from grc_scanner.converters.gitleaks_converter import GitleaksConverter

class SecretsScanner(BaseScanner):
    def __init__(self):
        self.name = "SecretsScanner"

    def scan(self, path=".", **kwargs):
        if not GitleaksWrapper.is_available():
            print("[SecretsScanner] Gitleaks not available")
            return []

        print(f"[SecretsScanner] Scanning for secrets in {path}")
        raw = GitleaksWrapper.scan(path)
        return GitleaksConverter.convert(raw)
    