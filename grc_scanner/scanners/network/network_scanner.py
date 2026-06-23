from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine
from grc_scanner.integrations.nmap_wrapper import NmapWrapper


class NetworkScanner:
    name = "network_scanner"

    def scan(self, target):
        if NmapWrapper.is_available():
            return self._scan_with_nmap(target)

        return self._scan_with_fallback(target)

    def _scan_with_nmap(self, target):
        findings = []
        output = NmapWrapper.scan(target)

        if not output:
            return findings

        lower_output = output.lower()

        if "open" in lower_output:
            findings.append(
                self._create_finding(
                    "network_open_ports",
                    "Open Ports Detected",
                    "fail",
                    "High",
                    "Nmap found open ports",
                    target,
                    "Attack surface exposed",
                    "Close unused ports",
                    "Restrict access",
                    "Network"
                )
            )

        if "22/tcp" in lower_output:
            findings.append(
                self._create_finding(
                    "network_ssh_open",
                    "SSH Port Open",
                    "fail",
                    "Medium",
                    "SSH port is open",
                    target,
                    "Brute-force exposure",
                    "Restrict SSH access",
                    "Use allowlists",
                    "Network"
                )
            )

        if "80/tcp" in lower_output or "443/tcp" in lower_output:
            findings.append(
                self._create_finding(
                    "network_web_open",
                    "Web Ports Open",
                    "pass",
                    "Low",
                    "Web service detected",
                    target,
                    "Expected exposure",
                    "Review service",
                    "Verify hardening",
                    "Network"
                )
            )

        return findings

    def _scan_with_fallback(self, target):
        findings = []

        findings.append(
            self._create_finding(
                "network_fallback_check",
                "Basic Network Scan",
                "pass",
                "Low",
                "Fallback network scan executed",
                target,
                "No Nmap available",
                "Install Nmap for deeper checks",
                "Use Nmap where possible",
                "Network"
            )
        )

        return findings

    def _create_finding(
        self,
        check_id,
        name,
        status,
        severity,
        description,
        evidence,
        business_impact,
        remediation,
        recommendation,
        category
    ):
        finding = Finding(
            check_id=check_id,
            name=name,
            status=status,
            severity=severity,
            description=description,
            evidence=evidence,
            business_impact=business_impact,
            remediation=remediation,
            recommendation=recommendation,
            category=category,
            scanner_name=self.name,
            target_type="network"
        )

        return RiskEngine.enrich_finding(finding)