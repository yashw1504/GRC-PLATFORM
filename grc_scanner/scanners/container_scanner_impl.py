"""Container scanner using Trivy"""
from grc_scanner.scanners.base_scanner import BaseScanner
from grc_scanner.integrations.trivy_wrapper import TrivyWrapper
from grc_scanner.integrations.syft_wrapper import SyftWrapper
from grc_scanner.converters.trivy_converter import TrivyConverter

class ContainerScanner(BaseScanner):
    def __init__(self):
        self.name = "ContainerScanner"

    def scan(self, path=".", **kwargs):
        all_findings = []

        if TrivyWrapper.is_available():
            print(f"[ContainerScanner] Running Trivy on {path}")
            raw = TrivyWrapper.scan(path)
            all_findings.extend(TrivyConverter.convert(raw))

        return all_findings