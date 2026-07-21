"""Parse sslscan text output to Finding objects"""
import re
from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine

class SSLScanConverter:
    @staticmethod
    def convert(raw_output: str, host: str = "") -> list:
        findings = []

        # Check for TLS 1.0/1.1 (deprecated)
        if re.search(r"TLSv1\.0.*enabled", raw_output, re.IGNORECASE):
            findings.append(RiskEngine.enrich_finding(Finding(
                check_id="tls_v1_0_enabled",
                name="TLS 1.0 Enabled",
                status="fail",
                severity="Medium",
                description="TLS 1.0 is deprecated and insecure",
                evidence=host,
                category="SSL/TLS",
                target_asset=host,
                scanner_name="sslscan",
                remediation="Disable TLS 1.0, enable TLS 1.2/1.3"
            )))

        if re.search(r"TLSv1\.1.*enabled", raw_output, re.IGNORECASE):
            findings.append(RiskEngine.enrich_finding(Finding(
                check_id="tls_v1_1_enabled",
                name="TLS 1.1 Enabled",
                status="fail",
                severity="Medium",
                description="TLS 1.1 is deprecated and insecure",
                evidence=host,
                category="SSL/TLS",
                target_asset=host,
                scanner_name="sslscan",
                remediation="Disable TLS 1.1, enable TLS 1.2/1.3"
            )))

        # Check for weak cipher suites
        weak_ciphers = re.findall(r"(RC4|DES|MD5|3DES|CBC-SHA|EXP)PT", raw_output)
        if weak_ciphers:
            findings.append(RiskEngine.enrich_finding(Finding(
                check_id="weak_ciphers_detected",
                name="Weak Cipher Suites Detected",
                status="fail",
                severity="High",
                description=f"Weak ciphers found: {', '.join(set(weak_ciphers))}",
                evidence=host,
                category="SSL/TLS",
                target_asset=host,
                scanner_name="sslscan",
                remediation="Remove weak ciphers, use only modern AEAD ciphers"
            )))

        return findings