from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine


class SSLScanner:

    name = "ssl_scanner"

    def scan(self, target="https://example.com"):

        findings = []

        findings.extend(
            self._check_certificate()
        )

        findings.extend(
            self._check_tls()
        )

        findings.extend(
            self._check_hsts()
        )

        findings.extend(
            self._check_cipher_suites()
        )

        findings.extend(
            self._check_ocsp()
        )

        return findings

    def _check_certificate(self):

        findings = []

        findings.append(
            self._create_finding(
                "ssl_certificate_expired",
                "SSL Certificate Expired",
                "fail",
                "Critical",
                "Certificate has expired",
                "Demo Mode",
                "Service trust failure",
                "Renew certificate",
                "Maintain valid certificates",
                "SSL/TLS"
            )
        )

        findings.append(
            self._create_finding(
                "ssl_certificate_expiring_soon",
                "SSL Certificate Expiring Soon",
                "warning",
                "Medium",
                "Certificate nearing expiration",
                "Demo Mode",
                "Potential outage risk",
                "Renew certificate",
                "Monitor certificate lifecycle",
                "SSL/TLS"
            )
        )

        findings.append(
            self._create_finding(
                "ssl_self_signed",
                "Self-Signed Certificate",
                "fail",
                "High",
                "Self-signed certificate detected",
                "Demo Mode",
                "Trust risk",
                "Use trusted CA",
                "Replace self-signed cert",
                "SSL/TLS"
            )
        )

        return findings

    def _check_tls(self):

        findings = []

        findings.append(
            self._create_finding(
                "ssl_old_tls_version",
                "Old TLS Version",
                "fail",
                "High",
                "TLS 1.0/1.1 detected",
                "Demo Mode",
                "Weak encryption",
                "Use TLS 1.2+",
                "Disable legacy protocols",
                "SSL/TLS"
            )
        )

        findings.append(
            self._create_finding(
                "ssl_weak_key_length",
                "Weak Key Length",
                "fail",
                "High",
                "Weak RSA key length detected",
                "Demo Mode",
                "Cryptographic weakness",
                "Use 2048+ bit keys",
                "Rotate certificates",
                "SSL/TLS"
            )
        )

        return findings

    def _check_hsts(self):

        findings = []

        findings.append(
            self._create_finding(
                "ssl_hsts_missing",
                "HSTS Missing",
                "fail",
                "Medium",
                "Strict-Transport-Security not configured",
                "Demo Mode",
                "Downgrade attack risk",
                "Enable HSTS",
                "Force HTTPS",
                "SSL/TLS"
            )
        )

        return findings

    def _check_cipher_suites(self):

        findings = []

        findings.append(
            self._create_finding(
                "ssl_weak_cipher",
                "Weak Cipher Suite",
                "fail",
                "High",
                "Weak cipher detected",
                "Demo Mode",
                "Encryption weakness",
                "Disable weak ciphers",
                "Use modern cipher suites",
                "SSL/TLS"
            )
        )

        findings.append(
            self._create_finding(
                "ssl_insecure_renegotiation",
                "Insecure Renegotiation",
                "fail",
                "Medium",
                "Insecure renegotiation supported",
                "Demo Mode",
                "Man-in-the-middle risk",
                "Disable insecure renegotiation",
                "Harden TLS configuration",
                "SSL/TLS"
            )
        )

        return findings

    def _check_ocsp(self):

        findings = []

        findings.append(
            self._create_finding(
                "ssl_ocsp_disabled",
                "OCSP Stapling Disabled",
                "warning",
                "Low",
                "OCSP stapling not enabled",
                "Demo Mode",
                "Reduced revocation checking",
                "Enable OCSP stapling",
                "Improve certificate validation",
                "SSL/TLS"
            )
        )

        findings.append(
            self._create_finding(
                "ssl_certificate_chain_invalid",
                "Invalid Certificate Chain",
                "fail",
                "High",
                "Certificate chain validation failed",
                "Demo Mode",
                "Trust failure",
                "Fix certificate chain",
                "Install intermediate certificates",
                "SSL/TLS"
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
            target_type="ssl"
        )

        return RiskEngine.enrich_finding(finding)