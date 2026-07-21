"""Convert Nmap XML output to Finding objects"""
import re
from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine

class NmapConverter:
    @staticmethod
    def convert(nmap_output: str, host: str = "") -> list:
        findings = []

        if not nmap_output:
            return findings

        # Find open ports
        open_ports = re.findall(r"(\d+)/tcp.*?open", nmap_output, re.IGNORECASE)
        if open_ports:
            port_str = ", ".join(open_ports)
            # Determine severity based on what's open
            sensitive_ports = {"22", "23", "3389", "5900", "3306", "5432", "6379", "27017"}
            sensitive_open = [p for p in open_ports if p in sensitive_ports]

            if sensitive_open:
                findings.append(RiskEngine.enrich_finding(Finding(
                    check_id="sensitive_ports_open",
                    name="Sensitive Ports Exposed",
                    status="fail",
                    severity="High",
                    description=f"Sensitive ports open: {', '.join(sensitive_open)}",
                    evidence=f"{host}: {', '.join(sensitive_open)}",
                    category="Network Security",
                    target_asset=host,
                    scanner_name="nmap",
                    remediation="Restrict access to sensitive ports using security groups/firewalls"
                )))

            findings.append(RiskEngine.enrich_finding(Finding(
                check_id="open_ports_detected",
                name=f"Open Ports: {len(open_ports)} found",
                status="info",
                severity="Info",
                description=f"Open ports: {port_str}",
                evidence=host,
                category="Network Security",
                target_asset=host,
                scanner_name="nmap",
                raw_data={"open_ports": open_ports}
            )))

        return findings