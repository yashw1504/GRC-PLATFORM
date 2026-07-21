"""Website/webapp scanner - orchestrates multiple tools"""
from grc_scanner.scanners.base_scanner import BaseScanner
from grc_scanner.integrations.nuclei_wrapper import NucleiWrapper
from grc_scanner.integrations.sslscan_wrapper import SSLScanWrapper
from grc_scanner.converters.nuclei_converter import NucleiConverter
from grc_scanner.converters.sslscan_converter import SSLScanConverter
from grc_scanner.converters.nmap_converter import NmapConverter
import subprocess

class WebsiteScanner(BaseScanner):
    def __init__(self):
        self.name = "WebsiteScanner"

    def scan(self, target, **kwargs):
        all_findings = []

        # 1. Nuclei scan
        if NucleiWrapper.is_available():
            print(f"[WebsiteScanner] Running Nuclei on {target}")
            raw = NucleiWrapper.scan(target)
            all_findings.extend(NucleiConverter.convert(raw))

        # 2. SSL scan
        if SSLScanWrapper.is_available():
            print(f"[WebsiteScanner] Running SSLScan on {target}")
            raw = SSLScanWrapper.scan(target)
            all_findings.extend(SSLScanConverter.convert(raw, target))

        # 3. Quick nmap
        host = target.replace("https://", "").replace("http://", "").split("/")[0]
        try:
            result = subprocess.run(
                ["nmap", "-F", host],
                capture_output=True, text=True, timeout=120
            )
            all_findings.extend(NmapConverter.convert(result.stdout, host))
        except Exception as e:
            print(f"[WebsiteScanner] Nmap error: {e}")

        return all_findings