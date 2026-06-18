from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine


class APIScanner:

    name = "api_scanner"

    def scan(self, target="https://example.com"):

        findings = []

        findings.extend(
            self._check_authentication()
        )

        findings.extend(
            self._check_authorization()
        )

        findings.extend(
            self._check_data_exposure()
        )

        findings.extend(
            self._check_rate_limiting()
        )

        findings.extend(
            self._check_headers()
        )

        findings.extend(
            self._check_injection()
        )

        findings.extend(
            self._check_transport_security()
        )

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