import socket

from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine


class NetworkScanner:

    name = "network_scanner"

    COMMON_PORTS = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        135: "RPC",
        139: "NetBIOS",
        143: "IMAP",
        389: "LDAP",
        443: "HTTPS",
        445: "SMB",
        993: "IMAPS",
        995: "POP3S",
        1433: "MSSQL",
        1521: "Oracle",
        2049: "NFS",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        6379: "Redis",
        8080: "HTTP-ALT",
        8443: "HTTPS-ALT",
        9200: "Elasticsearch",
        27017: "MongoDB"
    }

    RISKY_SERVICES = {
        "FTP",
        "Telnet",
        "SMB",
        "RDP",
        "VNC",
        "Redis",
        "MongoDB",
        "Elasticsearch",
        "NetBIOS"
    }

    def scan(self, host):

        findings = []

        open_ports = []

        for port, service in self.COMMON_PORTS.items():

            try:

                with socket.create_connection(
                    (host, port),
                    timeout=1
                ):

                    open_ports.append(
                        {
                            "port": port,
                            "service": service
                        }
                    )

            except Exception:
                pass

        findings.extend(
            self._build_findings(
                open_ports
            )
        )

        return findings

    def _build_findings(self, open_ports):

        findings = []

        if not open_ports:

            findings.append(
                self._create_finding(
                    "open_ports_detected",
                    "Open Ports Scan",
                    "pass",
                    "Info",
                    "No common ports detected",
                    "No open ports",
                    "",
                    "",
                    "",
                    "Network Security"
                )
            )

            return findings

        for port_info in open_ports:

            service = port_info["service"]
            port = port_info["port"]

            severity = (
                "High"
                if service in self.RISKY_SERVICES
                else "Info"
            )

            status = (
                "fail"
                if service in self.RISKY_SERVICES
                else "pass"
            )

            findings.append(
                self._create_finding(
                    "open_ports_detected",
                    f"{service} Port Open",
                    status,
                    severity,
                    f"{service} detected",
                    f"Port {port}",
                    (
                        f"{service} may expose "
                        f"attack surface."
                    ),
                    (
                        "Restrict access using "
                        "firewall rules."
                    ),
                    (
                        "Review exposure."
                    ),
                    "Network Security"
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

        return RiskEngine.enrich_finding(
            finding
        )