"""IaC scanner using Checkov"""
from grc_scanner.scanners.base_scanner import BaseScanner
from grc_scanner.integrations.checkov_wrapper import CheckovWrapper
from grc_scanner.converters.checkov_converter import CheckovConverter

class IaCScanner(BaseScanner):
    def __init__(self):
        self.name = "IaCScanner"

    def scan(self, path=".", **kwargs):
        if not CheckovWrapper.is_available():
            print("[IaCScanner] Checkov not available")
            return []

        print(f"[IaCScanner] Scanning IaC in {path}")
        raw = CheckovWrapper.scan(path)
        return CheckovConverter.convert(raw)