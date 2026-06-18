import re
from pathlib import Path

from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine

from grc_scanner.integrations.gitleaks_wrapper import (
    GitleaksWrapper
)


class SecretsScanner:

    name = "secrets_scanner"

    REGEX_PATTERNS = {

        "AWS Access Key":
        r"AKIA[0-9A-Z]{16}",

        "GitHub Token":
        r"ghp_[A-Za-z0-9]{36}",

        "Private Key":
        r"-----BEGIN.*PRIVATE KEY-----",

        "JWT Token":
        r"eyJ[A-Za-z0-9_-]+\.",

        "Password":
        r"password\s*=\s*[\"'].*?[\"']",

        "API Key":
        r"api[_-]?key\s*=\s*[\"'].*?[\"']"
    }

    def scan(self, path="."):

        if GitleaksWrapper.is_available():

            return self._scan_with_gitleaks(
                path
            )

        return self._scan_with_regex(
            path
        )

    def _scan_with_gitleaks(
        self,
        path
    ):

        findings = []

        results = GitleaksWrapper.scan(
            path
        )

        for item in results:

            findings.append(
                self._create_finding(
                    "secret_detected",
                    item.get(
                        "RuleID",
                        "Secret Detected"
                    ),
                    "fail",
                    "Critical",
                    "Secret discovered",
                    item.get(
                        "File",
                        ""
                    ),
                    (
                        "Credential exposure "
                        "may lead to compromise."
                    ),
                    (
                        "Remove secret and "
                        "rotate immediately."
                    ),
                    (
                        "Move secrets to vault."
                    ),
                    "Secrets"
                )
            )

        return findings

    def _scan_with_regex(
        self,
        path
    ):

        findings = []

        root = Path(path)

        if not root.exists():
            return findings

        for file in root.rglob("*"):

            if not file.is_file():
                continue

            try:

                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                for (
                    secret_type,
                    pattern
                ) in self.REGEX_PATTERNS.items():

                    matches = re.findall(
                        pattern,
                        content,
                        re.IGNORECASE
                    )

                    if matches:

                        findings.append(
                            self._create_finding(
                                "secret_detected",
                                secret_type,
                                "fail",
                                "Critical",
                                f"{secret_type} found",
                                str(file),
                                (
                                    "Sensitive credential "
                                    "exposure."
                                ),
                                (
                                    "Remove secret."
                                ),
                                (
                                    "Use secure vault."
                                ),
                                "Secrets"
                            )
                        )

            except Exception:
                pass

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
            target_type="code"
        )

        return RiskEngine.enrich_finding(
            finding
        )