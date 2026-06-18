try:
    import boto3

    AWS_AVAILABLE = True
except Exception:
    AWS_AVAILABLE = False

from datetime import datetime
from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine


class AWSScanner:
    name = "aws_scanner"

    def scan(self):
        if not AWS_AVAILABLE:
            return self._fallback_scan()

        try:
            sts = boto3.client("sts")
            sts.get_caller_identity()
            return self._real_scan()
        except Exception:
            return self._fallback_scan()

    def _real_scan(self):
        findings = []

        findings.extend(self._check_root_mfa())
        findings.extend(self._check_admin_policies())
        findings.extend(self._check_old_access_keys())
        findings.extend(self._check_cloudtrail())
        findings.extend(self._check_cloudtrail_multiregion())
        findings.extend(self._check_s3())
        findings.extend(self._check_s3_encryption())
        findings.extend(self._check_s3_versioning())
        findings.extend(self._check_s3_public_access())
        findings.extend(self._check_security_groups())
        findings.extend(self._check_rds())
        findings.extend(self._check_ebs())
        findings.extend(self._check_guardduty())
        findings.extend(self._check_config())
        findings.extend(self._check_kms_rotation())
        findings.extend(self._check_secret_rotation())
        findings.extend(self._check_inspector())
        findings.extend(self._check_waf())

        return findings

    def _check_admin_policies(self):
        findings = []
        try:
            iam = boto3.client("iam")
            users = iam.list_users()["Users"]

            for user in users:
                username = user["UserName"]
                attached = iam.list_attached_user_policies(UserName=username)

                for policy in attached["AttachedPolicies"]:
                    if "AdministratorAccess" in policy["PolicyName"]:
                        findings.append(
                            self._create_finding(
                                "iam_admin_policy_attached",
                                "Administrator Policy Attached",
                                "fail",
                                "High",
                                "Administrator policy detected",
                                username,
                                "Excessive permissions.",
                                "Apply least privilege.",
                                "Remove admin rights.",
                                "AWS IAM",
                            )
                        )
        except Exception as ex:
            findings.append(
                self._create_finding(
                    "aws_scan_error",
                    "AWS Scan Error",
                    "fail",
                    "Low",
                    "Unable to execute check",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS",
                )
            )

        return findings

    def _check_old_access_keys(self):
        findings = []
        try:
            iam = boto3.client("iam")
            users = iam.list_users()["Users"]

            for user in users:
                keys = iam.list_access_keys(UserName=user["UserName"])

                for key in keys["AccessKeyMetadata"]:
                    age = (datetime.utcnow() - key["CreateDate"].replace(tzinfo=None)).days
                    if age > 90:
                        findings.append(
                            self._create_finding(
                                "iam_old_access_keys",
                                "Old Access Key",
                                "fail",
                                "Medium",
                                "Access key older than 90 days",
                                user["UserName"],
                                "Credential compromise risk.",
                                "Rotate keys.",
                                "Use temporary credentials.",
                                "AWS IAM",
                            )
                        )
        except Exception as ex:
            findings.append(
                self._create_finding(
                    "aws_scan_error",
                    "AWS Scan Error",
                    "fail",
                    "Low",
                    "Unable to execute check",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS",
                )
            )

        return findings

    def _check_cloudtrail_multiregion(self):
        findings = []
        try:
            client = boto3.client("cloudtrail")
            trails = client.describe_trails()

            for trail in trails["trailList"]:
                if not trail.get("IsMultiRegionTrail", False):
                    findings.append(
                        self._create_finding(
                            "cloudtrail_not_multi_region",
                            "CloudTrail Not Multi Region",
                            "fail",
                            "Medium",
                            "Trail is not multi-region",
                            trail["Name"],
                            "Incomplete audit coverage.",
                            "Enable multi-region trail.",
                            "Monitor all regions.",
                            "AWS CloudTrail",
                        )
                    )
        except Exception as ex:
            findings.append(
                self._create_finding(
                    "aws_scan_error",
                    "AWS Scan Error",
                    "fail",
                    "Low",
                    "Unable to execute check",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS",
                )
            )

        return findings

    def _check_s3_encryption(self):
        findings = []
        try:
            s3 = boto3.client("s3")
            buckets = s3.list_buckets()

            for bucket in buckets["Buckets"]:
                try:
                    s3.get_bucket_encryption(Bucket=bucket["Name"])
                except Exception:
                    findings.append(
                        self._create_finding(
                            "s3_encryption_disabled",
                            "S3 Encryption Disabled",
                            "fail",
                            "High",
                            "Bucket encryption missing",
                            bucket["Name"],
                            "Sensitive data exposure.",
                            "Enable SSE-KMS.",
                            "Encrypt bucket.",
                            "AWS S3",
                        )
                    )
        except Exception as ex:
            findings.append(
                self._create_finding(
                    "aws_scan_error",
                    "AWS Scan Error",
                    "fail",
                    "Low",
                    "Unable to execute check",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS",
                )
            )

        return findings

    def _check_s3_versioning(self):
        findings = []
        try:
            s3 = boto3.client("s3")
            buckets = s3.list_buckets()

            for bucket in buckets["Buckets"]:
                versioning = s3.get_bucket_versioning(Bucket=bucket["Name"])
                if versioning.get("Status") != "Enabled":
                    findings.append(
                        self._create_finding(
                            "s3_versioning_disabled",
                            "S3 Versioning Disabled",
                            "fail",
                            "Medium",
                            "Versioning not enabled",
                            bucket["Name"],
                            "Ransomware recovery risk.",
                            "Enable versioning.",
                            "Protect object history.",
                            "AWS S3",
                        )
                    )
        except Exception as ex:
            findings.append(
                self._create_finding(
                    "aws_scan_error",
                    "AWS Scan Error",
                    "fail",
                    "Low",
                    "Unable to execute check",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS",
                )
            )

        return findings

    def _check_s3_public_access(self):
        findings = []
        try:
            s3 = boto3.client("s3")
            buckets = s3.list_buckets()

            for bucket in buckets["Buckets"]:
                try:
                    s3.get_public_access_block(Bucket=bucket["Name"])
                except Exception:
                    findings.append(
                        self._create_finding(
                            "s3_bucket_public",
                            "Public S3 Bucket",
                            "fail",
                            "Critical",
                            "Public access block missing",
                            bucket["Name"],
                            "Data leakage risk.",
                            "Block public access.",
                            "Review bucket policies.",
                            "AWS S3",
                        )
                    )
        except Exception as ex:
            findings.append(
                self._create_finding(
                    "aws_scan_error",
                    "AWS Scan Error",
                    "fail",
                    "Low",
                    "Unable to execute check",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS",
                )
            )

        return findings

    def _fallback_scan(self):
        findings = []
        findings.append(
            self._create_finding(
                "aws_demo_mode",
                "AWS Demo Mode",
                "pass",
                "Info",
                "AWS credentials not configured",
                "Running fallback mode",
                "",
                "",
                "",
                "AWS",
            )
        )
        return findings

    def _check_root_mfa(self):
        findings = []
        try:
            iam = boto3.client("iam")
            summary = iam.get_account_summary()
            mfa_enabled = summary["SummaryMap"].get("AccountMFAEnabled", 0)

            if mfa_enabled == 0:
                findings.append(
                    self._create_finding(
                        "iam_root_mfa_disabled",
                        "Root MFA Disabled",
                        "fail",
                        "Critical",
                        "Root account MFA disabled",
                        "AccountMFAEnabled=0",
                        "Account takeover risk.",
                        "Enable root MFA.",
                        "Use hardware MFA.",
                        "AWS IAM",
                    )
                )
            else:
                findings.append(
                    self._create_finding(
                        "iam_root_mfa_disabled",
                        "Root MFA Enabled",
                        "pass",
                        "Info",
                        "Root MFA enabled",
                        "AccountMFAEnabled=1",
                        "",
                        "",
                        "",
                        "AWS IAM",
                    )
                )
        except Exception as ex:
            findings.append(
                self._create_finding(
                    "aws_iam_error",
                    "IAM Scan Error",
                    "fail",
                    "Low",
                    "Unable to query IAM",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS IAM",
                )
            )

        return findings

    def _check_cloudtrail(self):
        findings = []
        try:
            client = boto3.client("cloudtrail")
            trails = client.describe_trails()

            if not trails["trailList"]:
                findings.append(
                    self._create_finding(
                        "cloudtrail_disabled",
                        "CloudTrail Disabled",
                        "fail",
                        "Critical",
                        "No CloudTrail found",
                        "",
                        "No audit trail available.",
                        "Enable CloudTrail.",
                        "Enable multi-region trail.",
                        "AWS CloudTrail",
                    )
                )
        except Exception as ex:
            findings.append(
                self._create_finding(
                    "aws_scan_error",
                    "AWS Scan Error",
                    "fail",
                    "Low",
                    "Unable to execute check",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS",
                )
            )

        return findings

    def _check_s3(self):
        findings = []
        try:
            s3 = boto3.client("s3")
            buckets = s3.list_buckets()

            for bucket in buckets["Buckets"]:
                findings.append(
                    self._create_finding(
                        "s3_bucket_discovered",
                        f"S3 Bucket: {bucket['Name']}",
                        "pass",
                        "Info",
                        "Bucket discovered",
                        bucket["Name"],
                        "",
                        "",
                        "",
                        "AWS S3",
                    )
                )
        except Exception as ex:
            findings.append(
                self._create_finding(
                    "aws_scan_error",
                    "AWS Scan Error",
                    "fail",
                    "Low",
                    "Unable to execute check",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS",
                )
            )

        return findings

    def _check_security_groups(self):
        findings = []
        try:
            ec2 = boto3.client("ec2")
            groups = ec2.describe_security_groups()

            for group in groups["SecurityGroups"]:
                for perm in group["IpPermissions"]:
                    for ip_range in perm.get("IpRanges", []):

                        cidr = ip_range.get("CidrIp")

                        if cidr == "0.0.0.0/0":

                            port = perm.get("FromPort")

                            evidence = (
                                f"{group['GroupName']} "
                                f"Port:{port}"
                            )

                            findings.append(
                                self._create_finding(
                                    "security_group_wide_open",
                                    "Security Group Wide Open",
                                    "fail",
                                    "High",
                                    "Open to internet",
                                    evidence,
                                    "Unauthorized access risk.",
                                    "Restrict CIDR.",
                                    "Use least privilege.",
                                    "AWS EC2",
                                )
                            )
                        cidr = ip_range.get("CidrIp")
                        port = perm.get("FromPort")
                        
                        evidence = (
                            f"{group['GroupName']} "
                            f"Port:{port}"
                        )
                        findings.append(
                                self._create_finding(
                                    "security_group_wide_open",
                                    "Security Group Wide Open",
                                    "fail",
                                    "High",
                                    "Open to internet",
                                    group["GroupName"],
                                    "Unauthorized access risk.",
                                    "Restrict CIDR.",
                                    "Use least privilege.",
                                    "AWS EC2",
                                )
                            )
        except Exception as ex:
            findings.append(
                self._create_finding(
                    "aws_scan_error",
                    "AWS Scan Error",
                    "fail",
                    "Low",
                    "Unable to execute check",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS",
                )
            )

        return findings

    def _check_rds(self):
        findings = []
        try:
            rds = boto3.client("rds")
            instances = rds.describe_db_instances()

            for db in instances["DBInstances"]:
                if db.get("PubliclyAccessible"):
                    findings.append(
                        self._create_finding(
                            "rds_public_access",
                            "Public RDS Instance",
                            "fail",
                            "High",
                            "Database publicly accessible",
                            db["DBInstanceIdentifier"],
                            "Database exposure risk.",
                            "Disable public access.",
                            "Use private subnets.",
                            "AWS RDS",
                        )
                    )
        except Exception as ex:
            findings.append(
                self._create_finding(
                    "aws_scan_error",
                    "AWS Scan Error",
                    "fail",
                    "Low",
                    "Unable to execute check",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS",
                )
            )

        return findings

    def _check_ebs(self):
        findings = []
        try:
            ec2 = boto3.client("ec2")
            volumes = ec2.describe_volumes()

            for volume in volumes["Volumes"]:
                if not volume.get("Encrypted", False):
                    findings.append(
                        self._create_finding(
                            "ebs_encryption_disabled",
                            "Unencrypted EBS Volume",
                            "fail",
                            "High",
                            "Volume encryption disabled",
                            volume["VolumeId"],
                            "Data exposure risk.",
                            "Enable EBS encryption.",
                            "Use KMS encryption.",
                            "AWS EBS",
                        )
                    )
        except Exception as ex:
            findings.append(
                self._create_finding(
                    "aws_scan_error",
                    "AWS Scan Error",
                    "fail",
                    "Low",
                    "Unable to execute check",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS",
                )
            )

        return findings
    
    def _check_guardduty(self):

        findings = []

        try:

            client = boto3.client(
                "guardduty"
            )

            detectors = client.list_detectors()

            if not detectors["DetectorIds"]:

                findings.append(
                    self._create_finding(
                        "guardduty_disabled",
                        "GuardDuty Disabled",
                        "fail",
                        "High",
                        "GuardDuty not enabled",
                        "",
                        "Threat detection unavailable.",
                        "Enable GuardDuty.",
                        "Enable continuous monitoring.",
                        "AWS Security"
                    )
                )

        except Exception as ex:

            findings.append(
                self._create_finding(
                    "guardduty_error",
                    "GuardDuty Scan Error",
                    "fail",
                    "Low",
                    "Unable to query GuardDuty",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS Security"
                )
            )

        return findings
    
    def _check_config(self):

        findings = []

        try:

            client = boto3.client(
                "config"
            )

            recorders = (
                client.describe_configuration_recorders()
            )

            if not recorders[
                "ConfigurationRecorders"
            ]:

                findings.append(
                    self._create_finding(
                        "config_disabled",
                        "AWS Config Disabled",
                        "fail",
                        "High",
                        "AWS Config not enabled",
                        "",
                        "No compliance recording.",
                        "Enable AWS Config.",
                        "Enable configuration tracking.",
                        "AWS Config"
                    )
                )

        except Exception as ex:

            findings.append(
                self._create_finding(
                    "config_error",
                    "AWS Config Scan Error",
                    "fail",
                    "Low",
                    "Unable to query AWS Config",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS Config"
                )
            )

        return findings
    
    def _check_kms_rotation(self):

        findings = []

        try:

            kms = boto3.client("kms")

            keys = kms.list_keys()

            for key in keys["Keys"]:

                rotation = kms.get_key_rotation_status(
                    KeyId=key["KeyId"]
                )

                if not rotation[
                    "KeyRotationEnabled"
                ]:

                    findings.append(
                        self._create_finding(
                            "kms_rotation_disabled",
                            "KMS Rotation Disabled",
                            "fail",
                            "Medium",
                            "KMS rotation disabled",
                            key["KeyId"],
                            "Long-term key exposure risk.",
                            "Enable rotation.",
                            "Rotate keys annually.",
                            "AWS KMS"
                        )
                    )

        except Exception as ex:

            findings.append(
                self._create_finding(
                    "kms_error",
                    "KMS Scan Error",
                    "fail",
                    "Low",
                    "Unable to query KMS",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS KMS"
                )
            )

        return findings
    
    def _check_secret_rotation(self):

        findings = []

        try:

            client = boto3.client(
                "secretsmanager"
            )

            secrets = client.list_secrets()

            for secret in secrets[
                "SecretList"
            ]:

                if not secret.get(
                    "RotationEnabled",
                    False
                ):

                    findings.append(
                        self._create_finding(
                            "secret_rotation_disabled",
                            "Secret Rotation Disabled",
                            "fail",
                            "Medium",
                            "Secret rotation disabled",
                            secret["Name"],
                            "Credential compromise risk.",
                            "Enable rotation.",
                            "Rotate secrets automatically.",
                            "AWS Secrets Manager"
                        )
                    )

        except Exception as ex:

            findings.append(
                self._create_finding(
                    "secret_error",
                    "Secrets Scan Error",
                    "fail",
                    "Low",
                    "Unable to query Secrets Manager",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS Secrets"
                )
            )

        return findings
    
    def _check_inspector(self):

        findings = []

        try:

            client = boto3.client(
                "inspector2"
            )

            client.list_findings(
                maxResults=1
            )

        except Exception:

            findings.append(
                self._create_finding(
                    "inspector_error",
                    "Inspector Scan Error",
                    "fail",
                    "Low",
                    "Unable to query Inspector",
                    "",
                    "Vulnerability visibility reduced.",
                    "Enable Inspector.",
                    "Enable continuous scanning.",
                    "AWS Inspector"
                )
            )

        return findings
    
    def _check_waf(self):

        findings = []

        try:

            waf = boto3.client(
                "wafv2"
            )

            acls = waf.list_web_acls(
                Scope="REGIONAL"
            )

            if not acls["WebACLs"]:

                findings.append(
                    self._create_finding(
                        "waf_missing",
                        "AWS WAF Missing",
                        "fail",
                        "Medium",
                        "No WAF deployed",
                        "",
                        "Web applications exposed.",
                        "Deploy AWS WAF.",
                        "Protect internet-facing workloads.",
                        "AWS WAF"
                    )
                )

        except Exception as ex:

            findings.append(
                self._create_finding(
                    "waf_error",
                    "WAF Scan Error",
                    "fail",
                    "Low",
                    "Unable to query WAF",
                    str(ex),
                    "",
                    "",
                    "",
                    "AWS WAF"
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
        category,
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
            target_type="cloud",
        )
        return RiskEngine.enrich_finding(finding)