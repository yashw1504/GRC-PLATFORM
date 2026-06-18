GCP_AVAILABLE = False

from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine


class GCPScanner:
    name = "gcp_scanner"

    def scan(self):
        print(
            "GCP_AVAILABLE =",
            GCP_AVAILABLE
        )

        if not GCP_AVAILABLE:
            return self._fallback_scan()

        try:
            return self._real_scan()
        except Exception:
            return self._fallback_scan()

    def _real_scan(self):
        findings = []

        findings.extend(
            self._check_iam()
        )

        findings.extend(
            self._check_storage()
        )

        findings.extend(
            self._check_compute()
        )

        findings.extend(
            self._check_networking()
        )

        findings.extend(
            self._check_sql()
        )

        findings.extend(
            self._check_kms()
        )

        findings.extend(
            self._check_monitoring()
        )

        findings.extend(
            self._check_gke()
        )

        return findings

    def _fallback_scan(self):
        findings = []

        findings.extend(
            self._check_iam()
        )

        findings.extend(
            self._check_storage()
        )

        findings.extend(
            self._check_compute()
        )

        findings.extend(
            self._check_networking()
        )

        findings.extend(
            self._check_sql()
        )

        findings.extend(
            self._check_kms()
        )

        findings.extend(
            self._check_monitoring()
        )

        findings.extend(
            self._check_gke()
        )

        return findings

    def _check_iam(self):
        findings = []

        findings.append(
            self._create_finding(
                "gcp_mfa_disabled",
                "MFA Not Enabled",
                "fail",
                "High",
                "MFA not enabled",
                "Demo Mode",
                "Account takeover risk",
                "Enable MFA",
                "Protect privileged accounts",
                "GCP IAM"
            )
        )

        findings.append(
            self._create_finding(
                "gcp_service_account_admin",
                "Privileged Service Account",
                "fail",
                "High",
                "Service account has excessive permissions",
                "Demo Mode",
                "Privilege escalation risk",
                "Reduce permissions",
                "Apply least privilege",
                "GCP IAM"
            )
        )

        findings.append(
            self._create_finding(
                "gcp_stale_accounts",
                "Inactive Accounts",
                "fail",
                "Medium",
                "Inactive users detected",
                "Demo Mode",
                "Dormant account risk",
                "Disable inactive accounts",
                "Review user activity",
                "GCP IAM"
            )
        )

        findings.append(
            self._create_finding(
                "gcp_audit_logging_disabled",
                "Audit Logging Disabled",
                "fail",
                "High",
                "Audit logs not verified",
                "Demo Mode",
                "Reduced visibility",
                "Enable audit logging",
                "Use Cloud Audit Logs",
                "GCP IAM"
            )
        )

        return findings

    def _check_storage(self):
        findings = []

        findings.append(
            self._create_finding(
                "gcp_storage_public",
                "Public Storage Bucket",
                "fail",
                "Critical",
                "Public bucket detected",
                "Demo Mode",
                "Data exposure risk",
                "Disable public access",
                "Restrict bucket access",
                "GCP Storage"
            )
        )

        findings.append(
            self._create_finding(
                "gcp_storage_encryption_disabled",
                "Storage Encryption Disabled",
                "fail",
                "High",
                "Encryption not verified",
                "Demo Mode",
                "Data exposure risk",
                "Enable encryption",
                "Use CMEK",
                "GCP Storage"
            )
        )

        findings.append(
            self._create_finding(
                "gcp_storage_logging_disabled",
                "Storage Logging Disabled",
                "fail",
                "Medium",
                "Logging not enabled",
                "Demo Mode",
                "Reduced audit visibility",
                "Enable logging",
                "Monitor storage activity",
                "GCP Storage"
            )
        )

        return findings

    def _check_compute(self):
        findings = []

        findings.append(
            self._create_finding(
                "gcp_vm_public_ip",
                "VM Public IP",
                "fail",
                "High",
                "Public IP detected",
                "Demo Mode",
                "Internet exposure risk",
                "Use private networking",
                "Restrict public access",
                "GCP Compute"
            )
        )

        findings.append(
            self._create_finding(
                "gcp_vm_disk_encryption_disabled",
                "VM Disk Encryption Disabled",
                "fail",
                "High",
                "Disk encryption not verified",
                "Demo Mode",
                "Data exposure risk",
                "Enable disk encryption",
                "Use CMEK",
                "GCP Compute"
            )
        )

        findings.append(
            self._create_finding(
                "gcp_vm_backup_disabled",
                "VM Backup Disabled",
                "fail",
                "Medium",
                "Backup not verified",
                "Demo Mode",
                "Recovery risk",
                "Enable backups",
                "Implement recovery plan",
                "GCP Compute"
            )
        )

        return findings
    
    def _check_networking(self):

        findings = []

        findings.append(
            self._create_finding(
                "gcp_firewall_wide_open",
                "Firewall Wide Open",
                "fail",
                "High",
                "Firewall allows 0.0.0.0/0",
                "Demo Mode",
                "Network exposure risk",
                "Restrict firewall rules",
                "Apply least privilege",
                "GCP Network"
            )
        )

        findings.append(
            self._create_finding(
                "gcp_ssh_open",
                "SSH Open To Internet",
                "fail",
                "High",
                "SSH accessible from internet",
                "Demo Mode",
                "Remote attack risk",
                "Restrict SSH access",
                "Use IAP/Bastion",
                "GCP Network"
            )
        )

        findings.append(
            self._create_finding(
                "gcp_rdp_open",
                "RDP Open To Internet",
                "fail",
                "High",
                "RDP accessible from internet",
                "Demo Mode",
                "Remote attack risk",
                "Restrict RDP access",
                "Use VPN",
                "GCP Network"
            )
        )

        return findings
    
    def _check_sql(self):

        findings = []

        findings.append(
            self._create_finding(
                "gcp_sql_public_access",
                "Cloud SQL Public Access",
                "fail",
                "High",
                "Public database endpoint detected",
                "Demo Mode",
                "Database exposure risk",
                "Use private IP",
                "Restrict access",
                "GCP SQL"
            )
        )

        findings.append(
            self._create_finding(
                "gcp_sql_backup_disabled",
                "Cloud SQL Backup Disabled",
                "fail",
                "Medium",
                "Backups not verified",
                "Demo Mode",
                "Recovery risk",
                "Enable backups",
                "Implement DR",
                "GCP SQL"
            )
        )

        findings.append(
            self._create_finding(
                "gcp_sql_old_tls",
                "Old TLS Versions Allowed",
                "fail",
                "Medium",
                "TLS configuration not verified",
                "Demo Mode",
                "Weak encryption risk",
                "Upgrade TLS",
                "Use modern TLS",
                "GCP SQL"
            )
        )

        return findings
    
    def _check_kms(self):

        findings = []

        findings.append(
            self._create_finding(
                "gcp_kms_rotation_disabled",
                "KMS Rotation Disabled",
                "fail",
                "Medium",
                "Key rotation not verified",
                "Demo Mode",
                "Cryptographic risk",
                "Enable rotation",
                "Rotate regularly",
                "GCP KMS"
            )
        )

        findings.append(
            self._create_finding(
                "gcp_kms_old_keys",
                "Old Encryption Keys",
                "fail",
                "Low",
                "Old keys detected",
                "Demo Mode",
                "Crypto hygiene issue",
                "Rotate keys",
                "Review key lifecycle",
                "GCP KMS"
            )
        )

        return findings
    
    def _check_monitoring(self):

        findings = []

        findings.append(
            self._create_finding(
                "gcp_monitoring_disabled",
                "Cloud Monitoring Disabled",
                "fail",
                "Medium",
                "Monitoring not verified",
                "Demo Mode",
                "Visibility gap",
                "Enable monitoring",
                "Collect metrics",
                "GCP Monitoring"
            )
        )

        findings.append(
            self._create_finding(
                "gcp_logging_disabled",
                "Cloud Logging Disabled",
                "fail",
                "Medium",
                "Logging not verified",
                "Demo Mode",
                "Audit visibility gap",
                "Enable logging",
                "Retain audit logs",
                "GCP Logging"
            )
        )

        return findings
    
    def _check_gke(self):

        findings = []

        findings.append(
            self._create_finding(
                "gke_public_api",
                "GKE Public API",
                "fail",
                "High",
                "Public control plane detected",
                "Demo Mode",
                "Cluster exposure risk",
                "Use private cluster",
                "Restrict API access",
                "GKE"
            )
        )

        findings.append(
            self._create_finding(
                "gke_rbac_disabled",
                "GKE RBAC Disabled",
                "fail",
                "High",
                "RBAC not verified",
                "Demo Mode",
                "Privilege escalation risk",
                "Enable RBAC",
                "Apply least privilege",
                "GKE"
            )
        )

        findings.append(
            self._create_finding(
                "gke_network_policy_disabled",
                "GKE Network Policy Disabled",
                "fail",
                "Medium",
                "Network policy not enabled",
                "Demo Mode",
                "Lateral movement risk",
                "Enable network policies",
                "Restrict traffic",
                "GKE"
            )
        )

        findings.append(
            self._create_finding(
                "gke_secret_encryption_disabled",
                "GKE Secret Encryption Disabled",
                "fail",
                "High",
                "Secret encryption not verified",
                "Demo Mode",
                "Secret exposure risk",
                "Enable secret encryption",
                "Use CMEK",
                "GKE"
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
            target_type="cloud"
        )

        return RiskEngine.enrich_finding(finding)