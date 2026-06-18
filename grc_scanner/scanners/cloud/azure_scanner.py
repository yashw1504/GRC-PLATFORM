AZURE_AVAILABLE = False

from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine


class AzureScanner:
    name = "azure_scanner"

    def _real_scan(self):
        findings = []

        findings.append(
            self._create_finding(
                "azure_real_mode",
                "Azure Real Mode",
                "pass",
                "Info",
                "Azure SDK detected",
                "Real Scan Path",
                "",
                "",
                "",
                "Azure"
            )
        )

        findings.extend(self._check_entra_id())
        findings.extend(self._check_storage())
        findings.extend(self._check_virtual_machines())
        findings.extend(self._check_networking())
        findings.extend(self._check_sql())
        findings.extend(self._check_keyvault())
        findings.extend(self._check_defender())
        findings.extend(self._check_aks())
        findings.extend(self._check_app_services())
        findings.extend(self._check_function_apps())
        findings.extend(self._check_monitoring())
        findings.extend(self._check_policy())
        findings.extend(self._check_recovery_services())

        return findings

    def scan(self):
        print("AZURE_AVAILABLE =", AZURE_AVAILABLE)

        if not AZURE_AVAILABLE:
            return self._fallback_scan()

        try:
            from grc_scanner.cloud.azure_auth import AzureAuth

            credential = AzureAuth.get_credential()

            if credential is None:
                return self._fallback_scan()

            print("USING REAL SCAN")
            return self._real_scan()

        except Exception:
            print("USING FALLBACK")
            return self._fallback_scan()

    def _fallback_scan(self):
        findings = []

        findings.extend(self._check_entra_id())
        findings.extend(self._check_storage())
        findings.extend(self._check_virtual_machines())
        findings.extend(self._check_networking())
        findings.extend(self._check_sql())
        findings.extend(self._check_keyvault())
        findings.extend(self._check_defender())
        findings.extend(self._check_aks())
        findings.extend(self._check_app_services())
        findings.extend(self._check_function_apps())
        findings.extend(self._check_monitoring())
        findings.extend(self._check_policy())
        findings.extend(self._check_recovery_services())

        return findings

    def _check_entra_id(self):
        findings = []

        findings.append(
            self._create_finding(
                "azure_mfa_disabled",
                "MFA Not Enabled",
                "fail",
                "High",
                "MFA enforcement not verified",
                "Demo Mode",
                "Account compromise risk.",
                "Enable MFA.",
                "Enforce MFA for all users.",
                "Azure Entra ID"
            )
        )

        findings.append(
            self._create_finding(
                "azure_guest_users_enabled",
                "Guest Users Enabled",
                "fail",
                "Medium",
                "Guest access not reviewed",
                "Demo Mode",
                "External access risk.",
                "Review guest users.",
                "Restrict guest access.",
                "Azure Entra ID"
            )
        )

        findings.append(
            self._create_finding(
                "azure_legacy_auth_enabled",
                "Legacy Authentication Enabled",
                "fail",
                "High",
                "Legacy authentication protocols detected",
                "Demo Mode",
                "Credential stuffing risk.",
                "Disable legacy authentication.",
                "Use modern authentication.",
                "Azure Entra ID"
            )
        )

        findings.append(
            self._create_finding(
                "azure_conditional_access_missing",
                "Conditional Access Missing",
                "fail",
                "High",
                "Conditional access policies not verified",
                "Demo Mode",
                "Identity protection gap.",
                "Enable Conditional Access.",
                "Require MFA and risk policies.",
                "Azure Entra ID"
            )
        )

        findings.append(
            self._create_finding(
                "azure_global_admin_excessive",
                "Excessive Global Administrators",
                "fail",
                "Medium",
                "Too many global administrators",
                "Demo Mode",
                "Privilege escalation risk.",
                "Reduce administrator count.",
                "Apply least privilege.",
                "Azure Entra ID"
            )
        )

        findings.append(
            self._create_finding(
                "azure_stale_accounts",
                "Inactive User Accounts",
                "fail",
                "Medium",
                "Dormant accounts detected",
                "Demo Mode",
                "Account takeover risk.",
                "Disable inactive users.",
                "Review dormant accounts.",
                "Azure Entra ID"
            )
        )

        findings.append(
            self._create_finding(
                "azure_service_principal_admin",
                "Privileged Service Principal",
                "fail",
                "High",
                "Service principal has elevated privileges",
                "Demo Mode",
                "Automation credential abuse risk.",
                "Review permissions.",
                "Apply least privilege.",
                "Azure Entra ID"
            )
        )

        findings.append(
            self._create_finding(
                "azure_audit_logs_disabled",
                "Audit Logs Disabled",
                "fail",
                "High",
                "Audit logging not verified",
                "Demo Mode",
                "Reduced forensic visibility.",
                "Enable audit logging.",
                "Send logs to Log Analytics.",
                "Azure Entra ID"
            )
        )

        return findings

    def _check_storage(self):
        findings = []

        findings.append(
            self._create_finding(
                "azure_storage_public",
                "Public Storage Account",
                "fail",
                "Critical",
                "Public storage access possible",
                "Demo Mode",
                "Data exposure risk.",
                "Disable public access.",
                "Use private endpoints.",
                "Azure Storage"
            )
        )

        findings.append(
            self._create_finding(
                "azure_storage_https_disabled",
                "HTTPS Not Enforced",
                "fail",
                "High",
                "HTTPS enforcement not verified",
                "Demo Mode",
                "Data transmission risk.",
                "Require HTTPS.",
                "Disable HTTP access.",
                "Azure Storage"
            )
        )

        findings.append(
            self._create_finding(
                "azure_storage_encryption_disabled",
                "Storage Encryption Disabled",
                "fail",
                "High",
                "Storage encryption not verified",
                "Demo Mode",
                "Data exposure risk.",
                "Enable encryption at rest.",
                "Use Microsoft-managed or customer-managed keys.",
                "Azure Storage"
            )
        )

        findings.append(
            self._create_finding(
                "azure_storage_softdelete_disabled",
                "Storage Soft Delete Disabled",
                "fail",
                "Medium",
                "Soft delete not verified",
                "Demo Mode",
                "Recovery risk.",
                "Enable soft delete.",
                "Protect deleted blobs and files.",
                "Azure Storage"
            )
        )

        findings.append(
            self._create_finding(
                "azure_storage_logging_disabled",
                "Storage Logging Disabled",
                "fail",
                "Medium",
                "Diagnostic logging not verified",
                "Demo Mode",
                "Reduced audit visibility.",
                "Enable storage logging.",
                "Send logs to Log Analytics.",
                "Azure Storage"
            )
        )

        findings.append(
            self._create_finding(
                "azure_storage_blob_public",
                "Public Blob Access Enabled",
                "fail",
                "High",
                "Blob public access not verified",
                "Demo Mode",
                "Data leakage risk.",
                "Disable blob public access.",
                "Restrict container permissions.",
                "Azure Storage"
            )
        )

        findings.append(
            self._create_finding(
                "azure_storage_network_rules_missing",
                "Storage Network Rules Missing",
                "fail",
                "High",
                "Network restrictions not verified",
                "Demo Mode",
                "Unrestricted network access risk.",
                "Restrict storage network access.",
                "Use private endpoints or firewall rules.",
                "Azure Storage"
            )
        )

        findings.append(
            self._create_finding(
                "azure_storage_key_rotation_disabled",
                "Storage Key Rotation Disabled",
                "fail",
                "Medium",
                "Key rotation not verified",
                "Demo Mode",
                "Credential exposure risk.",
                "Rotate storage account keys.",
                "Use managed identities where possible.",
                "Azure Storage"
            )
        )

        return findings

    def _check_virtual_machines(self):
        findings = []

        findings.append(
            self._create_finding(
                "azure_vm_public_ip",
                "VM Public IP",
                "fail",
                "High",
                "Public IP detected",
                "Demo Mode",
                "Internet exposure risk.",
                "Use private networking.",
                "Review NSGs.",
                "Azure VM"
            )
        )

        findings.append(
            self._create_finding(
                "azure_vm_disk_encryption_disabled",
                "VM Disk Encryption Disabled",
                "fail",
                "High",
                "Disk encryption not verified",
                "Demo Mode",
                "Data exposure risk.",
                "Enable disk encryption.",
                "Use Azure Disk Encryption.",
                "Azure VM"
            )
        )

        findings.append(
            self._create_finding(
                "azure_vm_backup_disabled",
                "VM Backup Disabled",
                "fail",
                "Medium",
                "Backup configuration not verified",
                "Demo Mode",
                "Recovery risk.",
                "Enable backups.",
                "Use Recovery Services Vault.",
                "Azure VM"
            )
        )

        findings.append(
            self._create_finding(
                "azure_vm_jit_disabled",
                "Just-In-Time Access Disabled",
                "fail",
                "Medium",
                "JIT access not configured",
                "Demo Mode",
                "Administrative exposure risk.",
                "Enable JIT VM access.",
                "Reduce attack surface.",
                "Azure VM"
            )
        )

        return findings

    def _check_networking(self):
        findings = []

        findings.append(
            self._create_finding(
                "azure_nsg_wide_open",
                "NSG Wide Open",
                "fail",
                "High",
                "Network Security Group allows unrestricted access",
                "Demo Mode",
                "Unauthorized access risk.",
                "Restrict inbound rules.",
                "Apply least privilege networking.",
                "Azure Networking"
            )
        )

        findings.append(
            self._create_finding(
                "azure_nsg_ssh_open",
                "SSH Open To Internet",
                "fail",
                "High",
                "Port 22 exposed to internet",
                "Demo Mode",
                "Remote access attack risk.",
                "Restrict SSH access.",
                "Use Bastion or VPN.",
                "Azure Networking"
            )
        )

        findings.append(
            self._create_finding(
                "azure_nsg_rdp_open",
                "RDP Open To Internet",
                "fail",
                "High",
                "Port 3389 exposed to internet",
                "Demo Mode",
                "Remote desktop attack risk.",
                "Restrict RDP access.",
                "Use Just-In-Time access.",
                "Azure Networking"
            )
        )

        findings.append(
            self._create_finding(
                "azure_firewall_disabled",
                "Azure Firewall Disabled",
                "fail",
                "Medium",
                "Firewall status unknown",
                "Demo Mode",
                "Network filtering gap.",
                "Enable Azure Firewall.",
                "Centralize traffic inspection.",
                "Azure Networking"
            )
        )

        findings.append(
            self._create_finding(
                "azure_ddos_disabled",
                "DDoS Protection Disabled",
                "fail",
                "Medium",
                "DDoS protection not verified",
                "Demo Mode",
                "Availability risk.",
                "Enable Azure DDoS Protection.",
                "Protect internet-facing services.",
                "Azure Networking"
            )
        )

        return findings

    def _check_sql(self):
        findings = []

        findings.append(
            self._create_finding(
                "azure_sql_public_access",
                "SQL Public Access",
                "fail",
                "High",
                "Public SQL endpoint",
                "Demo Mode",
                "Database exposure risk.",
                "Restrict access.",
                "Use private endpoints.",
                "Azure SQL"
            )
        )

        findings.append(
            self._create_finding(
                "azure_sql_auditing_disabled",
                "SQL Auditing Disabled",
                "fail",
                "Medium",
                "Database auditing not verified",
                "Demo Mode",
                "Reduced forensic visibility.",
                "Enable SQL auditing.",
                "Send logs to Log Analytics.",
                "Azure SQL"
            )
        )

        findings.append(
            self._create_finding(
                "azure_sql_tde_disabled",
                "SQL Transparent Data Encryption Disabled",
                "fail",
                "High",
                "TDE not verified",
                "Demo Mode",
                "Data exposure risk.",
                "Enable Transparent Data Encryption.",
                "Encrypt database files at rest.",
                "Azure SQL"
            )
        )

        findings.append(
            self._create_finding(
                "azure_sql_threat_detection_disabled",
                "SQL Threat Detection Disabled",
                "fail",
                "High",
                "Threat detection not verified",
                "Demo Mode",
                "Detection gap.",
                "Enable threat detection.",
                "Monitor suspicious activity.",
                "Azure SQL"
            )
        )

        findings.append(
            self._create_finding(
                "azure_sql_backup_disabled",
                "SQL Backup Not Verified",
                "fail",
                "Medium",
                "Backup configuration not verified",
                "Demo Mode",
                "Recovery risk.",
                "Enable automated backups.",
                "Ensure restore capability.",
                "Azure SQL"
            )
        )

        findings.append(
            self._create_finding(
                "azure_sql_old_tls",
                "Old TLS Versions Allowed",
                "fail",
                "Medium",
                "Old TLS not verified",
                "Demo Mode",
                "Weak transport security.",
                "Require TLS 1.2 or higher.",
                "Disable legacy TLS versions.",
                "Azure SQL"
            )
        )

        return findings

    def _check_keyvault(self):
        findings = []

        findings.append(
            self._create_finding(
                "azure_keyvault_softdelete_disabled",
                "Key Vault Soft Delete Disabled",
                "fail",
                "Medium",
                "Soft delete not verified",
                "Demo Mode",
                "Recovery risk.",
                "Enable soft delete.",
                "Protect secrets.",
                "Azure Key Vault"
            )
        )

        findings.append(
            self._create_finding(
                "azure_keyvault_purge_protection_disabled",
                "Key Vault Purge Protection Disabled",
                "fail",
                "High",
                "Purge protection not verified",
                "Demo Mode",
                "Irrecoverable deletion risk.",
                "Enable purge protection.",
                "Prevent permanent deletion.",
                "Azure Key Vault"
            )
        )

        findings.append(
            self._create_finding(
                "azure_keyvault_public_access",
                "Key Vault Public Access Enabled",
                "fail",
                "High",
                "Public access not verified",
                "Demo Mode",
                "Secret exposure risk.",
                "Restrict public access.",
                "Use private endpoints.",
                "Azure Key Vault"
            )
        )

        findings.append(
            self._create_finding(
                "azure_keyvault_old_keys",
                "Old Key Vault Keys",
                "fail",
                "Medium",
                "Key rotation not verified",
                "Demo Mode",
                "Credential exposure risk.",
                "Rotate keys and secrets.",
                "Use automated rotation.",
                "Azure Key Vault"
            )
        )

        findings.append(
            self._create_finding(
                "azure_keyvault_no_rbac",
                "Key Vault RBAC Not Verified",
                "fail",
                "Medium",
                "RBAC configuration not verified",
                "Demo Mode",
                "Access control gap.",
                "Enable RBAC authorization.",
                "Use least privilege access.",
                "Azure Key Vault"
            )
        )

        return findings

    def _check_defender(self):
        findings = []

        findings.append(
            self._create_finding(
                "azure_defender_disabled",
                "Defender for Cloud Disabled",
                "fail",
                "High",
                "Defender status unknown",
                "Demo Mode",
                "Threat detection gap.",
                "Enable Defender.",
                "Enable continuous monitoring.",
                "Azure Security"
            )
        )

        findings.append(
            self._create_finding(
                "azure_security_center_disabled",
                "Security Center Disabled",
                "fail",
                "High",
                "Security Center not verified",
                "Demo Mode",
                "Security posture gap.",
                "Enable Microsoft Defender for Cloud.",
                "Monitor and harden resources.",
                "Azure Security"
            )
        )

        findings.append(
            self._create_finding(
                "azure_recommendations_unresolved",
                "Unresolved Security Recommendations",
                "fail",
                "Medium",
                "Security recommendations not reviewed",
                "Demo Mode",
                "Residual risk remains open.",
                "Review and resolve recommendations.",
                "Track security posture improvements.",
                "Azure Security"
            )
        )

        return findings
    
    def _check_aks(self):

        findings = []

        findings.append(
            self._create_finding(
                "aks_public_api",
                "AKS Public API Server",
                "fail",
                "High",
                "AKS API server exposed publicly",
                "Demo Mode",
                "Cluster administration exposure risk.",
                "Use private AKS cluster.",
                "Restrict API access.",
                "Azure AKS"
            )
        )

        findings.append(
            self._create_finding(
                "aks_rbac_disabled",
                "AKS RBAC Disabled",
                "fail",
                "High",
                "RBAC configuration not verified",
                "Demo Mode",
                "Privilege escalation risk.",
                "Enable RBAC.",
                "Apply least privilege.",
                "Azure AKS"
            )
        )

        findings.append(
            self._create_finding(
                "aks_private_cluster_disabled",
                "AKS Private Cluster Disabled",
                "fail",
                "High",
                "Private cluster configuration not verified",
                "Demo Mode",
                "Public management plane exposure.",
                "Enable private cluster.",
                "Restrict control plane access.",
                "Azure AKS"
            )
        )

        findings.append(
            self._create_finding(
                "aks_secret_encryption_disabled",
                "AKS Secret Encryption Disabled",
                "fail",
                "High",
                "Secret encryption not verified",
                "Demo Mode",
                "Credential exposure risk.",
                "Enable secret encryption.",
                "Use Key Vault integration.",
                "Azure AKS"
            )
        )

        findings.append(
            self._create_finding(
                "aks_network_policy_disabled",
                "AKS Network Policy Disabled",
                "fail",
                "Medium",
                "Network policy configuration not verified",
                "Demo Mode",
                "Pod-to-pod traffic unrestricted.",
                "Enable network policies.",
                "Restrict east-west traffic.",
                "Azure AKS"
            )
        )

        findings.append(
            self._create_finding(
                "aks_audit_logging_disabled",
                "AKS Audit Logging Disabled",
                "fail",
                "Medium",
                "Audit logging not verified",
                "Demo Mode",
                "Reduced forensic visibility.",
                "Enable AKS audit logging.",
                "Send logs to Log Analytics.",
                "Azure AKS"
            )
        )

        return findings
    
    def _check_app_services(self):

        findings = []

        findings.append(
            self._create_finding(
                "azure_appservice_http_enabled",
                "App Service HTTP Enabled",
                "fail",
                "High",
                "HTTPS enforcement not verified",
                "Demo Mode",
                "Traffic interception risk.",
                "Enable HTTPS only.",
                "Disable HTTP access.",
                "Azure App Service"
            )
        )

        findings.append(
            self._create_finding(
                "azure_appservice_ftps_disabled",
                "FTPS Not Enforced",
                "fail",
                "Medium",
                "FTPS configuration not verified",
                "Demo Mode",
                "Credential exposure risk.",
                "Require FTPS.",
                "Disable insecure FTP.",
                "Azure App Service"
            )
        )

        findings.append(
            self._create_finding(
                "azure_appservice_managed_identity_missing",
                "Managed Identity Missing",
                "fail",
                "High",
                "Managed identity not enabled",
                "Demo Mode",
                "Credential management risk.",
                "Enable managed identity.",
                "Avoid embedded secrets.",
                "Azure App Service"
            )
        )

        findings.append(
            self._create_finding(
                "azure_appservice_auth_disabled",
                "Authentication Disabled",
                "fail",
                "High",
                "Authentication configuration not verified",
                "Demo Mode",
                "Unauthorized access risk.",
                "Enable App Service Authentication.",
                "Use Entra ID integration.",
                "Azure App Service"
            )
        )

        return findings

    def _check_function_apps(self):

        findings = []

        findings.append(
            self._create_finding(
                "azure_function_public_access",
                "Function Public Access",
                "fail",
                "High",
                "Public access not verified",
                "Demo Mode",
                "Internet exposure risk.",
                "Restrict access.",
                "Use private endpoints.",
                "Azure Functions"
            )
        )

        findings.append(
            self._create_finding(
                "azure_function_managed_identity_missing",
                "Function Managed Identity Missing",
                "fail",
                "High",
                "Managed identity not enabled",
                "Demo Mode",
                "Credential exposure risk.",
                "Enable managed identity.",
                "Avoid hardcoded secrets.",
                "Azure Functions"
            )
        )

        findings.append(
            self._create_finding(
                "azure_function_http_only",
                "Function HTTPS Enforcement Missing",
                "fail",
                "Medium",
                "HTTPS enforcement not verified",
                "Demo Mode",
                "Transport security risk.",
                "Enable HTTPS only.",
                "Disable HTTP access.",
                "Azure Functions"
            )
        )

        return findings
    
    def _check_monitoring(self):

        findings = []

        findings.append(
            self._create_finding(
                "azure_monitor_disabled",
                "Azure Monitor Disabled",
                "fail",
                "Medium",
                "Monitoring configuration not verified",
                "Demo Mode",
                "Reduced visibility.",
                "Enable Azure Monitor.",
                "Collect operational telemetry.",
                "Azure Monitor"
            )
        )

        findings.append(
            self._create_finding(
                "azure_log_analytics_missing",
                "Log Analytics Missing",
                "fail",
                "Medium",
                "Log Analytics workspace not verified",
                "Demo Mode",
                "Logging gap.",
                "Enable Log Analytics.",
                "Centralize logs.",
                "Azure Monitor"
            )
        )

        findings.append(
            self._create_finding(
                "azure_activity_log_disabled",
                "Activity Logs Disabled",
                "fail",
                "High",
                "Activity logging not verified",
                "Demo Mode",
                "Reduced audit visibility.",
                "Enable activity logging.",
                "Retain audit events.",
                "Azure Monitor"
            )
        )

        return findings
    
    def _check_policy(self):

        findings = []

        findings.append(
            self._create_finding(
                "azure_policy_disabled",
                "Azure Policy Disabled",
                "fail",
                "High",
                "Policy enforcement not verified",
                "Demo Mode",
                "Governance gap.",
                "Enable Azure Policy.",
                "Enforce compliance controls.",
                "Azure Policy"
            )
        )

        findings.append(
            self._create_finding(
                "azure_policy_noncompliant_resources",
                "Non-Compliant Resources",
                "fail",
                "Medium",
                "Policy compliance not verified",
                "Demo Mode",
                "Configuration drift risk.",
                "Review compliance state.",
                "Remediate non-compliant resources.",
                "Azure Policy"
            )
        )

        return findings
    
    def _check_recovery_services(self):

        findings = []

        findings.append(
            self._create_finding(
                "azure_backup_disabled",
                "Azure Backup Disabled",
                "fail",
                "Medium",
                "Backup status not verified",
                "Demo Mode",
                "Recovery risk.",
                "Enable Azure Backup.",
                "Protect critical workloads.",
                "Azure Recovery"
            )
        )

        findings.append(
            self._create_finding(
                "azure_site_recovery_disabled",
                "Site Recovery Disabled",
                "fail",
                "Medium",
                "Disaster recovery not verified",
                "Demo Mode",
                "Business continuity risk.",
                "Enable Azure Site Recovery.",
                "Implement disaster recovery.",
                "Azure Recovery"
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