import re
import ssl
import socket
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine


class WebScanner:
    name = "web_scanner"

    def scan(self, target):
        findings = []

        try:
            response = requests.get(
                target,
                timeout=10,
                verify=False,
                allow_redirects=True
            )

            findings.extend(self._check_https(target))
            findings.extend(self._check_security_headers(response))
            findings.extend(self._check_cookie_security(response))
            findings.extend(self._check_server_header(response))
            findings.extend(self._check_privacy_policy(target, response))
            findings.extend(self._check_cookie_banner(response))
            findings.extend(self._check_login_page(target))
            findings.extend(self._technology_fingerprint(response))
            findings.extend(self._check_tls_version(target))

        except Exception as ex:
            finding = Finding(
                check_id="web_scan_failed",
                name="Web Scan Failure",
                status="fail",
                severity="High",
                description="Web scan failed",
                evidence=str(ex),
                business_impact="Unable to assess website security posture.",
                remediation="Verify connectivity and DNS resolution.",
                scanner_name=self.name,
                target_type="web"
            )
            findings.append(RiskEngine.enrich_finding(finding))

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
            target_type="web"
        )
        return RiskEngine.enrich_finding(finding)

    def _check_https(self, target):
        findings = []

        if target.lower().startswith("https://"):
            findings.append(
                self._create_finding(
                    "https_enforced",
                    "HTTPS Enforcement",
                    "pass",
                    "Info",
                    "HTTPS enabled",
                    target,
                    "",
                    "",
                    "",
                    "Transport Security"
                )
            )
        else:
            findings.append(
                self._create_finding(
                    "https_enforced",
                    "HTTPS Enforcement",
                    "fail",
                    "Critical",
                    "HTTPS not enforced",
                    target,
                    "Traffic may be intercepted.",
                    "Enable HTTPS.",
                    "Force HTTPS redirect.",
                    "Transport Security"
                )
            )

        return findings

    def _check_security_headers(self, response):
        findings = []
        headers = response.headers

        checks = {
            "Strict-Transport-Security": "hsts_present",
            "Content-Security-Policy": "csp_present",
            "X-Frame-Options": "x_frame_options",
            "X-Content-Type-Options": "x_content_type_options"
        }

        for header, check_id in checks.items():
            if header in headers:
                findings.append(
                    self._create_finding(
                        check_id,
                        header,
                        "pass",
                        "Info",
                        f"{header} present",
                        headers.get(header),
                        "",
                        "",
                        "",
                        "Security Headers"
                    )
                )
            else:
                findings.append(
                    self._create_finding(
                        check_id,
                        header,
                        "fail",
                        "High",
                        f"{header} missing",
                        "Not Present",
                        "Missing security header.",
                        f"Add {header}",
                        "Review secure headers.",
                        "Security Headers"
                    )
                )

        return findings

    def _check_cookie_security(self, response):
        findings = []

        cookies = response.cookies

        if not cookies:
            return findings

        for cookie in cookies:

            secure = getattr(cookie, "secure", False)

            if secure:
                findings.append(
                    self._create_finding(
                        "cookies_secure",
                        "Secure Cookie",
                        "pass",
                        "Info",
                        "Cookie uses Secure flag",
                        cookie.name,
                        "",
                        "",
                        "",
                        "Cookie Security"
                    )
                )
            else:
                findings.append(
                    self._create_finding(
                        "cookies_secure",
                        "Secure Cookie",
                        "fail",
                        "Medium",
                        "Cookie missing Secure flag",
                        cookie.name,
                        "Cookie may be transmitted over HTTP.",
                        "Set Secure flag on cookie.",
                        "Secure all session cookies.",
                        "Cookie Security"
                    )
                )

        return findings

    def _check_server_header(self, response):

        findings = []

        server = response.headers.get("Server")

        if server:

            findings.append(
                self._create_finding(
                    "server_header_leak",
                    "Server Header Disclosure",
                    "fail",
                    "Low",
                    "Server header exposed",
                    server,
                    "Technology disclosure helps attackers.",
                    "Hide or minimize server banner.",
                    "Use generic server header.",
                    "Information Disclosure"
                )
            )

        else:

            findings.append(
                self._create_finding(
                    "server_header_leak",
                    "Server Header Disclosure",
                    "pass",
                    "Info",
                    "Server header hidden",
                    "",
                    "",
                    "",
                    "",
                    "Information Disclosure"
                )
            )

        return findings

    def _check_privacy_policy(self, target, response):

        findings = []

        html = response.text.lower()

        if "privacy policy" in html:

            findings.append(
                self._create_finding(
                    "privacy_policy_found",
                    "Privacy Policy",
                    "pass",
                    "Info",
                    "Privacy policy detected",
                    target,
                    "",
                    "",
                    "",
                    "Privacy"
                )
            )

        else:

            findings.append(
                self._create_finding(
                    "privacy_policy_found",
                    "Privacy Policy",
                    "fail",
                    "Medium",
                    "Privacy policy not detected",
                    target,
                    "Privacy obligations may not be met.",
                    "Publish a privacy policy.",
                    "Review GDPR and DPDPA requirements.",
                    "Privacy"
                )
            )

        return findings

    def _check_cookie_banner(self, response):

        findings = []

        html = response.text.lower()

        keywords = [
            "cookie consent",
            "accept cookies",
            "cookie settings",
            "cookie banner"
        ]

        found = any(
            keyword in html
            for keyword in keywords
        )

        if found:

            findings.append(
                self._create_finding(
                    "cookie_banner_found",
                    "Cookie Banner",
                    "pass",
                    "Info",
                    "Cookie banner detected",
                    "Banner Found",
                    "",
                    "",
                    "",
                    "Privacy"
                )
            )

        else:

            findings.append(
                self._create_finding(
                    "cookie_banner_found",
                    "Cookie Banner",
                    "fail",
                    "Medium",
                    "Cookie banner not detected",
                    "Not Found",
                    "May violate privacy regulations.",
                    "Implement cookie consent banner.",
                    "Review GDPR consent requirements.",
                    "Privacy"
                )
            )

        return findings

    def _check_login_page(self, target):

        findings = []

        paths = [
            "/login",
            "/signin",
            "/admin",
            "/auth/login"
        ]

        for path in paths:

            try:

                url = urljoin(target, path)

                r = requests.get(
                    url,
                    timeout=5,
                    verify=False
                )

                if r.status_code == 200:

                    findings.append(
                        self._create_finding(
                            "login_page_found",
                            "Login Page Found",
                            "pass",
                            "Info",
                            "Login page detected",
                            url,
                            "",
                            "",
                            "",
                            "Authentication"
                        )
                    )

                    break

            except Exception:
                pass

        return findings

    def _technology_fingerprint(self, response):

        findings = []

        tech = []

        server = response.headers.get("Server")
        powered = response.headers.get("X-Powered-By")

        if server:
            tech.append(server)

        if powered:
            tech.append(powered)

        findings.append(
            self._create_finding(
                "technology_fingerprint",
                "Technology Fingerprint",
                "pass",
                "Info",
                "Technology stack identified",
                ", ".join(tech) if tech else "Unknown",
                "",
                "",
                "",
                "Information Gathering"
            )
        )

        return findings

    def _check_tls_version(self, target):

        findings = []

        try:

            parsed = urlparse(target)

            hostname = parsed.hostname

            if not hostname:
                return findings

            context = ssl.create_default_context()

            with socket.create_connection(
                (hostname, 443),
                timeout=5
            ) as sock:

                with context.wrap_socket(
                    sock,
                    server_hostname=hostname
                ) as ssock:

                    version = ssock.version()

            if version in ["TLSv1.2", "TLSv1.3"]:

                findings.append(
                    self._create_finding(
                        "tls_version_good",
                        "TLS Version",
                        "pass",
                        "Info",
                        "Strong TLS version",
                        version,
                        "",
                        "",
                        "",
                        "Transport Security"
                    )
                )

            else:

                findings.append(
                    self._create_finding(
                        "tls_version_good",
                        "TLS Version",
                        "fail",
                        "High",
                        "Weak TLS version detected",
                        version,
                        "Weak encryption may expose data.",
                        "Upgrade TLS configuration.",
                        "Allow only TLS 1.2+.",
                        "Transport Security"
                    )
                )

        except Exception as ex:

            findings.append(
                self._create_finding(
                    "tls_version_good",
                    "TLS Version",
                    "fail",
                    "Medium",
                    "Unable to determine TLS version",
                    str(ex),
                    "",
                    "Review TLS configuration.",
                    "",
                    "Transport Security"
                )
            )

        return findings