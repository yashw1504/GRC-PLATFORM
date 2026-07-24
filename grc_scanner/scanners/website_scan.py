"""Website/webapp scanner - orchestrates multiple tools"""
from grc_scanner.scanners.base_scanner import BaseScanner
from grc_scanner.integrations.nuclei_wrapper import NucleiWrapper
from grc_scanner.integrations.sslscan_wrapper import SSLScanWrapper
from grc_scanner.converters.nmap_converter import NmapConverter
import subprocess
import os

class WebsiteScanner(BaseScanner):
    def __init__(self):
        self.name = "WebsiteScanner"

    def scan(self, target, **kwargs):
        all_findings = []

        # 1. Nuclei scan
        if NucleiWrapper.is_available():
            print(f"[WebsiteScanner] Running Nuclei on {target}")
            raw = NucleiWrapper.scan(target)
            # Convert raw dicts to Finding objects
            all_findings.extend(self._convert_nuclei(raw))
        else:
            print("[WebsiteScanner] Nuclei is not installed; skipping template scan")

        # 2. SSL scan
        if SSLScanWrapper.is_available():
            print(f"[WebsiteScanner] Running SSLScan on {target}")
            raw = SSLScanWrapper.scan(target)
            if raw:
                all_findings.append({
                    "check_id": "ssl_scan_complete",
                    "name": "SSL Scan Completed",
                    "status": "info",
                    "severity": "Info",
                    "evidence": target[:200],
                    "raw_output": raw[:1000],
                    "scanner_name": "sslscan"
                })
        else:
            print("[WebsiteScanner] SSLScan is not installed; skipping TLS scan")

        # 3. Quick nmap
        host = target.replace("https://", "").replace("http://", "").split("/")[0]
        try:
            result = subprocess.run(
                ["nmap", "-sV", "-F", host],
                capture_output=True, text=True, timeout=120
            )
            if result.stdout:
                all_findings.extend(NmapConverter.convert(result.stdout, host))
            if result.returncode not in (0, 1):
                print(f"[WebsiteScanner] Nmap exited with {result.returncode}: {result.stderr.strip()}")
        except Exception as e:
            print(f"[WebsiteScanner] Nmap error: {e}")

        return all_findings

    def _convert_nuclei(self, raw_results):
        """Simple converter inline since we don't have converter module yet"""
        findings = []
        if not raw_results:
            return findings

        for item in raw_results:
            if isinstance(item, dict):
                info = item.get("info", {})
                severity = info.get("severity", "info").capitalize()
                findings.append({
                    "check_id": item.get("template-id", "nuclei_unknown"),
                    "name": info.get("name", "Unknown Nuclei Finding"),
                    "status": "fail" if severity in ("Critical", "High", "Medium") else "info",
                    "severity": severity if severity in ("Critical", "High", "Medium", "Low", "Info") else "Info",
                    "description": info.get("description", "")[:500],
                    "evidence": item.get("matched-at", item.get("host", ""))[:200],
                    "category": "Vulnerability",
                    "target_asset": item.get("host", ""),
                    "scanner_name": "nuclei",
                    "raw_data": item
                })

        return findings
