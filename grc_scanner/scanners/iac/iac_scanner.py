from pathlib import Path

from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine

from grc_scanner.integrations.checkov_wrapper import (
    CheckovWrapper
)


class IaCScanner:

    name = "iac_scanner"

    def scan(self, path="."):

        if CheckovWrapper.is_available():
            return self._scan_with_checkov(path)

        return self._scan_with_fallback(path)

    def _scan_with_checkov(self, path):

        findings = []

        results = CheckovWrapper.scan(path)

        if not results:
            return findings

        findings.append(
            self._create_finding(
                "iac_checkov_scan",
                "Checkov Scan Completed",
                "pass",
                "Info",
                "Checkov scan completed",
                path,
                "",
                "",
                "",
                "Infrastructure as Code"
            )
        )

        return findings

    def _scan_with_fallback(self, path):

        findings = []

        root = Path(path)

        tf_files = list(root.rglob("*.tf"))

        for tf_file in tf_files:

            try:

                content = tf_file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                findings.extend(
                    self._check_public_s3(
                        tf_file,
                        content
                    )
                )

                findings.extend(
                    self._check_open_security_group(
                        tf_file,
                        content
                    )
                )

                findings.extend(
                    self._check_admin_policy(
                        tf_file,
                        content
                    )
                )

                findings.extend(
                    self._check_unencrypted_storage(
                        tf_file,
                        content
                    )
                )

            except Exception:
                pass

        return findings

    def _check_public_s3(
        self,
        file,
        content
    ):

        findings = []

        if 'acl = "public-read"' in content.lower():

            findings.append(
                self._create_finding(
                    "iac_terraform_s3_public",
                    "Public S3 Bucket",
                    "fail",
                    "Critical",
                    "Public S3 bucket detected",
                    str(file),
                    "Data exposure risk.",
                    "Make bucket private.",
                    "Use least privilege.",
                    "Infrastructure as Code"
                )
            )

        return findings

    def _check_open_security_group(
        self,
        file,
        content
    ):

        findings = []

        if "0.0.0.0/0" in content:

            findings.append(
                self._create_finding(
                    "iac_terraform_security_group_wide_open",
                    "Wide Open Security Group",
                    "fail",
                    "High",
                    "Security group open to the internet",
                    str(file),
                    "Unauthorized access risk.",
                    "Restrict CIDR ranges.",
                    "Allow only required networks.",
                    "Infrastructure as Code"
                )
            )

        return findings

    def _check_admin_policy(
        self,
        file,
        content
    ):

        findings = []

        if (
            'Action = "*"' in content
            or '"*"' in content
        ):

            findings.append(
                self._create_finding(
                    "iac_terraform_iam_full_admin",
                    "IAM Full Admin Policy",
                    "fail",
                    "Critical",
                    "Overly permissive IAM policy",
                    str(file),
                    "Privilege escalation risk.",
                    "Apply least privilege.",
                    "Limit permissions.",
                    "Infrastructure as Code"
                )
            )

        return findings

    def _check_unencrypted_storage(
        self,
        file,
        content
    ):

        findings = []

        if (
            "encrypted = false"
            in content.lower()
        ):

            findings.append(
                self._create_finding(
                    "iac_unencrypted_storage",
                    "Unencrypted Storage",
                    "fail",
                    "High",
                    "Storage encryption disabled",
                    str(file),
                    "Sensitive data may be exposed.",
                    "Enable encryption.",
                    "Use KMS-managed keys.",
                    "Infrastructure as Code"
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
            target_type="iac"
        )

        return RiskEngine.enrich_finding(
            finding
        )