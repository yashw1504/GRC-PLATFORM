from urllib.parse import urlparse
import requests

from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine
from grc_scanner.engine.scanner_errors import scanner_error_finding


class APIScanner:

    name = "api_scanner"

    def scan(self, target):
        if not target:
            return [scanner_error_finding(
                self.name, "An API URL is required to run API checks.", category="API"
            )]
        if not target.startswith(("http://", "https://")):
            target = f"https://{target}"

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)
        except requests.RequestException:
            return [scanner_error_finding(
                self.name, "The API endpoint could not be reached; API checks were not completed.",
                target, category="API",
            )]

        findings = []
        parsed = urlparse(target)
        if parsed.scheme != "https":
            findings.append(self._create_finding(
                "api_https_enforced", "API Transport Security", "fail", "High",
                "The API endpoint uses unencrypted HTTP.", target,
                "API traffic can be intercepted or modified.",
                "Serve the API over HTTPS and redirect HTTP requests.",
                "Require TLS 1.2 or newer.", "API Transport Security",
            ))

        cors = response.headers.get("Access-Control-Allow-Origin", "").strip()
        if cors == "*":
            findings.append(self._create_finding(
                "api_cors_wildcard", "Wildcard CORS Policy", "fail", "Medium",
                "The API response allows requests from every origin.", cors,
                "Browser clients from untrusted origins can access API responses.",
                "Restrict CORS to trusted application origins.",
                "Review credential and origin policies together.", "API Configuration",
            ))

        server = response.headers.get("Server", "").strip()
        if server and any(character.isdigit() for character in server):
            findings.append(self._create_finding(
                "api_server_header_disclosure", "Server Version Disclosure", "fail", "Low",
                "The API response exposes a server version in its Server header.", server,
                "Version details can help attackers select targeted exploits.",
                "Remove or generalize version information in response headers.",
                "Keep server software patched.", "API Configuration",
            ))

        if "application/json" not in response.headers.get("Content-Type", "").lower():
            findings.append(self._create_finding(
                "api_content_type", "API Content Type", "warning", "Low",
                "The endpoint response does not declare a JSON content type.",
                response.headers.get("Content-Type", "Not present"),
                "Clients may parse responses inconsistently.",
                "Set an explicit content type that matches the response body.",
                "Use application/json for JSON responses.", "API Configuration",
            ))

        return findings

    def _check_authentication(self):

        findings = []

        findings.append(
            self._create_finding(
                "api_no_authentication",
                "No Authentication",
                "fail",
                "Critical",
                "API endpoint accessible without authentication",
                "Demo Mode",
                "Unauthorized access risk",
                "Implement authentication",
                "Use OAuth2 or JWT",
                "API"
            )
        )

        findings.append(
            self._create_finding(
                "api_weak_authentication",
                "Weak Authentication",
                "fail",
                "High",
                "Weak authentication mechanism",
                "Demo Mode",
                "Account compromise risk",
                "Strengthen authentication",
                "Use MFA and OAuth",
                "API"
            )
        )

        findings.append(
            self._create_finding(
                "api_basic_auth_enabled",
                "Basic Authentication Enabled",
                "warning",
                "Medium",
                "Basic authentication detected",
                "Demo Mode",
                "Credential exposure risk",
                "Disable basic auth",
                "Use token-based auth",
                "API"
            )
        )

        return findings

    def _check_authorization(self):

        findings = []

        findings.append(
            self._create_finding(
                "api_bola",
                "Broken Object Level Authorization",
                "fail",
                "Critical",
                "Authorization bypass possible",
                "Demo Mode",
                "Data exposure risk",
                "Implement access controls",
                "Validate object ownership",
                "API"
            )
        )

        findings.append(
            self._create_finding(
                "api_broken_function_auth",
                "Broken Function Level Authorization",
                "fail",
                "Critical",
                "Privilege escalation possible",
                "Demo Mode",
                "Unauthorized functionality access",
                "Implement RBAC",
                "Enforce authorization",
                "API"
            )
        )

        findings.append(
            self._create_finding(
                "api_excessive_permissions",
                "Excessive Permissions",
                "fail",
                "High",
                "API grants excessive permissions",
                "Demo Mode",
                "Privilege abuse risk",
                "Apply least privilege",
                "Reduce access scope",
                "API"
            )
        )

        return findings

    def _check_data_exposure(self):

        findings = []

        findings.append(
            self._create_finding(
                "api_sensitive_data_exposure",
                "Sensitive Data Exposure",
                "fail",
                "Critical",
                "Sensitive data returned in API response",
                "Demo Mode",
                "Data leakage risk",
                "Mask sensitive data",
                "Review responses",
                "API"
            )
        )

        findings.append(
            self._create_finding(
                "api_pii_exposure",
                "PII Exposure",
                "fail",
                "High",
                "Personally identifiable information exposed",
                "Demo Mode",
                "Privacy violation risk",
                "Protect PII",
                "Mask personal data",
                "API"
            )
        )

        findings.append(
            self._create_finding(
                "api_token_exposure",
                "Token Exposure",
                "fail",
                "High",
                "API token disclosed",
                "Demo Mode",
                "Account takeover risk",
                "Rotate token",
                "Protect credentials",
                "API"
            )
        )

        return findings

    def _check_rate_limiting(self):

        findings = []

        findings.append(
            self._create_finding(
                "api_no_rate_limit",
                "No Rate Limiting",
                "fail",
                "Medium",
                "Rate limiting not configured",
                "Demo Mode",
                "DoS risk",
                "Implement throttling",
                "Protect endpoints",
                "API"
            )
        )

        findings.append(
            self._create_finding(
                "api_no_bruteforce_protection",
                "No Brute Force Protection",
                "fail",
                "Medium",
                "Brute force controls missing",
                "Demo Mode",
                "Credential attack risk",
                "Implement account lockout",
                "Add detection controls",
                "API"
            )
        )

        return findings

    def _check_headers(self):

        findings = []

        findings.append(
            self._create_finding(
                "api_missing_security_headers",
                "Missing Security Headers",
                "fail",
                "Medium",
                "Security headers missing",
                "Demo Mode",
                "Browser attack risk",
                "Add headers",
                "Harden responses",
                "API"
            )
        )

        findings.append(
            self._create_finding(
                "api_cors_wildcard",
                "CORS Wildcard Enabled",
                "fail",
                "Medium",
                "Access-Control-Allow-Origin=* detected",
                "Demo Mode",
                "Cross-origin attack risk",
                "Restrict CORS",
                "Allow trusted origins only",
                "API"
            )
        )

        return findings

    def _check_injection(self):

        findings = []

        findings.append(
            self._create_finding(
                "api_sql_injection",
                "SQL Injection Risk",
                "fail",
                "Critical",
                "Potential SQL injection",
                "Demo Mode",
                "Database compromise risk",
                "Use parameterized queries",
                "Validate input",
                "API"
            )
        )

        findings.append(
            self._create_finding(
                "api_xss",
                "Cross-Site Scripting Risk",
                "fail",
                "High",
                "Reflected input detected",
                "Demo Mode",
                "Client compromise risk",
                "Sanitize input",
                "Encode output",
                "API"
            )
        )

        findings.append(
            self._create_finding(
                "api_command_injection",
                "Command Injection Risk",
                "fail",
                "Critical",
                "Potential command execution",
                "Demo Mode",
                "Server compromise risk",
                "Validate input",
                "Avoid shell execution",
                "API"
            )
        )

        return findings

    def _check_transport_security(self):

        findings = []

        findings.append(
            self._create_finding(
                "api_http_allowed",
                "HTTP Allowed",
                "fail",
                "High",
                "HTTP endpoint detected",
                "Demo Mode",
                "Traffic interception risk",
                "Enforce HTTPS",
                "Redirect HTTP to HTTPS",
                "API"
            )
        )

        findings.append(
            self._create_finding(
                "api_old_tls",
                "Old TLS Version",
                "fail",
                "Medium",
                "Legacy TLS version detected",
                "Demo Mode",
                "Weak encryption risk",
                "Upgrade TLS",
                "Use TLS 1.2+",
                "API"
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
            target_type="api"
        )

        return RiskEngine.enrich_finding(
            finding
        )
