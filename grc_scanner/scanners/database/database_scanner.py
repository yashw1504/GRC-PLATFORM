from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine


class DatabaseScanner:

    name = "database_scanner"

    def scan(self, target="."):

        findings = []

        findings.extend(
            self._check_public_access()
        )

        findings.extend(
            self._check_default_credentials()
        )

        findings.extend(
            self._check_encryption()
        )

        findings.extend(
            self._check_backup()
        )

        findings.extend(
            self._check_audit_logging()
        )

        findings.extend(
            self._check_tls()
        )

        findings.extend(
            self._check_cassandra()
        )

        findings.extend(
            self._check_hbase()
        )

        findings.extend(
            self._check_hive()
        )

        findings.extend(
            self._check_postgresql()
        )

        findings.extend(
            self._check_mysql()
        )

        findings.extend(
            self._check_mongodb()
        )

        findings.extend(
            self._check_mssql()
        )

        return findings

    def _check_public_access(self):

        findings = []

        findings.append(
            self._create_finding(
                "db_public_access",
                "Database Public Access",
                "fail",
                "Critical",
                "Database accessible from internet",
                "Demo Mode",
                "Unauthorized access risk",
                "Restrict network access",
                "Use private networking",
                "Database"
            )
        )

        return findings

    def _check_default_credentials(self):

        findings = []

        findings.append(
            self._create_finding(
                "db_default_credentials",
                "Default Credentials Detected",
                "fail",
                "Critical",
                "Default credentials detected",
                "Demo Mode",
                "Account compromise risk",
                "Change passwords",
                "Use strong credentials",
                "Database"
            )
        )

        return findings

    def _check_encryption(self):

        findings = []

        findings.append(
            self._create_finding(
                "db_encryption_disabled",
                "Database Encryption Disabled",
                "fail",
                "High",
                "Encryption not verified",
                "Demo Mode",
                "Data exposure risk",
                "Enable encryption",
                "Encrypt at rest",
                "Database"
            )
        )

        return findings

    def _check_backup(self):

        findings = []

        findings.append(
            self._create_finding(
                "db_backup_disabled",
                "Database Backup Disabled",
                "fail",
                "Medium",
                "Backups not verified",
                "Demo Mode",
                "Recovery risk",
                "Enable backups",
                "Implement DR plan",
                "Database"
            )
        )

        return findings

    def _check_audit_logging(self):

        findings = []

        findings.append(
            self._create_finding(
                "db_audit_logging_disabled",
                "Audit Logging Disabled",
                "fail",
                "Medium",
                "Audit logging not enabled",
                "Demo Mode",
                "Visibility gap",
                "Enable audit logging",
                "Monitor activity",
                "Database"
            )
        )

        return findings

    def _check_tls(self):

        findings = []

        findings.append(
            self._create_finding(
                "db_old_tls",
                "Old TLS Version",
                "fail",
                "Medium",
                "Weak TLS configuration",
                "Demo Mode",
                "Encryption weakness",
                "Upgrade TLS",
                "Use TLS 1.2+",
                "Database"
            )
        )

        return findings

    def _check_cassandra(self):

        findings = []

        findings.append(
            self._create_finding(
                "cassandra_auth_disabled",
                "Cassandra Authentication Disabled",
                "fail",
                "Critical",
                "Authentication not enabled",
                "Demo Mode",
                "Unauthorized access risk",
                "Enable PasswordAuthenticator",
                "Use strong authentication",
                "Apache Cassandra"
            )
        )

        findings.append(
            self._create_finding(
                "cassandra_encryption_disabled",
                "Cassandra Encryption Disabled",
                "fail",
                "High",
                "Encryption not enabled",
                "Demo Mode",
                "Data exposure risk",
                "Enable encryption",
                "Encrypt node communication",
                "Apache Cassandra"
            )
        )

        findings.append(
            self._create_finding(
                "cassandra_audit_disabled",
                "Cassandra Audit Logging Disabled",
                "fail",
                "Medium",
                "Audit logging not enabled",
                "Demo Mode",
                "Reduced visibility",
                "Enable audit logging",
                "Track database activity",
                "Apache Cassandra"
            )
        )

        return findings

    def _check_hbase(self):

        findings = []

        findings.append(
            self._create_finding(
                "hbase_auth_disabled",
                "HBase Authentication Disabled",
                "fail",
                "Critical",
                "Authentication not verified",
                "Demo Mode",
                "Unauthorized access risk",
                "Enable Kerberos",
                "Secure cluster access",
                "Apache HBase"
            )
        )

        findings.append(
            self._create_finding(
                "hbase_encryption_disabled",
                "HBase Encryption Disabled",
                "fail",
                "High",
                "Encryption not verified",
                "Demo Mode",
                "Data exposure risk",
                "Enable encryption",
                "Protect stored data",
                "Apache HBase"
            )
        )

        return findings

    def _check_hive(self):

        findings = []

        findings.append(
            self._create_finding(
                "hive_auth_disabled",
                "Hive Authentication Disabled",
                "fail",
                "Critical",
                "Authentication not enabled",
                "Demo Mode",
                "Unauthorized query execution",
                "Enable authentication",
                "Integrate with Kerberos",
                "Apache Hive"
            )
        )

        findings.append(
            self._create_finding(
                "hive_authorization_disabled",
                "Hive Authorization Disabled",
                "fail",
                "High",
                "Authorization not configured",
                "Demo Mode",
                "Privilege escalation risk",
                "Enable Ranger/Sentry",
                "Apply least privilege",
                "Apache Hive"
            )
        )

        findings.append(
            self._create_finding(
                "hive_audit_disabled",
                "Hive Audit Logging Disabled",
                "fail",
                "Medium",
                "Audit logging not enabled",
                "Demo Mode",
                "Reduced forensic visibility",
                "Enable audit logging",
                "Track data access",
                "Apache Hive"
            )
        )

        return findings

    def _check_postgresql(self):

        findings = []

        findings.append(
            self._create_finding(
                "postgres_superuser_enabled",
                "PostgreSQL Superuser Enabled",
                "fail",
                "High",
                "Superuser account detected",
                "Demo Mode",
                "Privilege escalation risk",
                "Limit superuser access",
                "Apply least privilege",
                "PostgreSQL"
            )
        )

        findings.append(
            self._create_finding(
                "postgres_ssl_disabled",
                "PostgreSQL SSL Disabled",
                "fail",
                "High",
                "SSL not enforced",
                "Demo Mode",
                "Data interception risk",
                "Enable SSL",
                "Encrypt database traffic",
                "PostgreSQL"
            )
        )

        findings.append(
            self._create_finding(
                "postgres_public_access",
                "PostgreSQL Public Access",
                "fail",
                "Critical",
                "Public access detected",
                "Demo Mode",
                "Unauthorized access risk",
                "Restrict network access",
                "Use private networking",
                "PostgreSQL"
            )
        )

        findings.append(
            self._create_finding(
                "postgres_audit_disabled",
                "PostgreSQL Audit Logging Disabled",
                "fail",
                "Medium",
                "Audit logging disabled",
                "Demo Mode",
                "Reduced visibility",
                "Enable pgAudit",
                "Monitor database activity",
                "PostgreSQL"
            )
        )

        return findings

    def _check_mysql(self):

        findings = []

        findings.append(
            self._create_finding(
                "mysql_root_remote_login",
                "MySQL Root Remote Login Enabled",
                "fail",
                "Critical",
                "Root remote login allowed",
                "Demo Mode",
                "Unauthorized access risk",
                "Disable remote root login",
                "Restrict administrative access",
                "MySQL"
            )
        )

        findings.append(
            self._create_finding(
                "mysql_ssl_disabled",
                "MySQL SSL Disabled",
                "fail",
                "High",
                "SSL not enforced",
                "Demo Mode",
                "Data interception risk",
                "Enable SSL",
                "Encrypt connections",
                "MySQL"
            )
        )

        findings.append(
            self._create_finding(
                "mysql_public_access",
                "MySQL Public Access",
                "fail",
                "Critical",
                "Public database access",
                "Demo Mode",
                "Exposure risk",
                "Restrict network access",
                "Use private networking",
                "MySQL"
            )
        )

        findings.append(
            self._create_finding(
                "mysql_audit_disabled",
                "MySQL Audit Logging Disabled",
                "fail",
                "Medium",
                "Audit logging disabled",
                "Demo Mode",
                "Reduced visibility",
                "Enable audit logging",
                "Monitor access",
                "MySQL"
            )
        )

        return findings

    def _check_mongodb(self):

        findings = []

        findings.append(
            self._create_finding(
                "mongodb_auth_disabled",
                "MongoDB Authentication Disabled",
                "fail",
                "Critical",
                "Authentication disabled",
                "Demo Mode",
                "Unauthorized access risk",
                "Enable authentication",
                "Protect database access",
                "MongoDB"
            )
        )

        findings.append(
            self._create_finding(
                "mongodb_tls_disabled",
                "MongoDB TLS Disabled",
                "fail",
                "High",
                "TLS not enabled",
                "Demo Mode",
                "Data interception risk",
                "Enable TLS",
                "Encrypt communications",
                "MongoDB"
            )
        )

        findings.append(
            self._create_finding(
                "mongodb_public_access",
                "MongoDB Public Access",
                "fail",
                "Critical",
                "Public exposure detected",
                "Demo Mode",
                "Unauthorized access risk",
                "Restrict access",
                "Use private networking",
                "MongoDB"
            )
        )

        findings.append(
            self._create_finding(
                "mongodb_audit_disabled",
                "MongoDB Audit Logging Disabled",
                "fail",
                "Medium",
                "Audit logging disabled",
                "Demo Mode",
                "Reduced visibility",
                "Enable auditing",
                "Track user activity",
                "MongoDB"
            )
        )

        return findings

    def _check_mssql(self):

        findings = []

        findings.append(
            self._create_finding(
                "mssql_sa_enabled",
                "MSSQL SA Account Enabled",
                "fail",
                "Critical",
                "SA account enabled",
                "Demo Mode",
                "Privilege abuse risk",
                "Disable SA account",
                "Use named admin accounts",
                "MSSQL"
            )
        )

        findings.append(
            self._create_finding(
                "mssql_public_access",
                "MSSQL Public Access",
                "fail",
                "Critical",
                "Public access detected",
                "Demo Mode",
                "Unauthorized access risk",
                "Restrict access",
                "Use private endpoints",
                "MSSQL"
            )
        )

        findings.append(
            self._create_finding(
                "mssql_tls_disabled",
                "MSSQL TLS Disabled",
                "fail",
                "High",
                "TLS not enforced",
                "Demo Mode",
                "Encryption weakness",
                "Enable TLS",
                "Encrypt communications",
                "MSSQL"
            )
        )

        findings.append(
            self._create_finding(
                "mssql_audit_disabled",
                "MSSQL Audit Logging Disabled",
                "fail",
                "Medium",
                "Audit logging disabled",
                "Demo Mode",
                "Reduced visibility",
                "Enable auditing",
                "Monitor activity",
                "MSSQL"
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
            target_type="database"
        )

        return RiskEngine.enrich_finding(finding)