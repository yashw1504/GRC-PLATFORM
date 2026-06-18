from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine


class SBOMScanner:

    name = "sbom_scanner"

    def scan(self, target="."):

        findings = []

        findings.extend(
            self._check_vulnerable_dependencies()
        )

        findings.extend(
            self._check_supply_chain()
        )

        findings.extend(
            self._check_licenses()
        )

        findings.extend(
            self._check_sbom_quality()
        )

        return findings

    def _check_vulnerable_dependencies(self):

        findings = []

        findings.append(
            self._create_finding(
                "sbom_critical_dependency",
                "Critical Vulnerable Dependency",
                "fail",
                "Critical",
                "Critical vulnerable dependency found",
                "Demo Mode",
                "Remote compromise risk",
                "Upgrade dependency",
                "Remove vulnerable package",
                "SBOM"
            )
        )

        findings.append(
            self._create_finding(
                "sbom_high_dependency",
                "High Vulnerable Dependency",
                "fail",
                "High",
                "High severity dependency found",
                "Demo Mode",
                "Security risk",
                "Upgrade dependency",
                "Patch vulnerable package",
                "SBOM"
            )
        )

        findings.append(
            self._create_finding(
                "sbom_eol_dependency",
                "End Of Life Dependency",
                "fail",
                "Medium",
                "EOL package detected",
                "Demo Mode",
                "Unsupported software risk",
                "Upgrade package",
                "Use supported versions",
                "SBOM"
            )
        )

        findings.append(
            self._create_finding(
                "sbom_unmaintained_package",
                "Unmaintained Package",
                "fail",
                "Medium",
                "Package no longer maintained",
                "Demo Mode",
                "Supply chain risk",
                "Replace package",
                "Use maintained libraries",
                "SBOM"
            )
        )

        return findings

    def _check_supply_chain(self):

        findings = []

        findings.append(
            self._create_finding(
                "sbom_unsigned_package",
                "Unsigned Package",
                "fail",
                "High",
                "Package signature missing",
                "Demo Mode",
                "Tampering risk",
                "Verify signatures",
                "Use signed artifacts",
                "SBOM"
            )
        )

        findings.append(
            self._create_finding(
                "sbom_unknown_supplier",
                "Unknown Package Supplier",
                "fail",
                "Medium",
                "Supplier not trusted",
                "Demo Mode",
                "Supply chain risk",
                "Review supplier",
                "Use trusted sources",
                "SBOM"
            )
        )

        findings.append(
            self._create_finding(
                "sbom_tampered_package",
                "Tampered Package",
                "fail",
                "Critical",
                "Package integrity validation failed",
                "Demo Mode",
                "Malware risk",
                "Replace package",
                "Verify integrity",
                "SBOM"
            )
        )

        return findings

    def _check_licenses(self):

        findings = []

        findings.append(
            self._create_finding(
                "sbom_gpl_license",
                "GPL License Detected",
                "warning",
                "Medium",
                "GPL licensed package detected",
                "Demo Mode",
                "Legal compliance risk",
                "Review licensing",
                "Consult legal team",
                "SBOM"
            )
        )

        findings.append(
            self._create_finding(
                "sbom_unknown_license",
                "Unknown License",
                "fail",
                "Medium",
                "Unknown package license",
                "Demo Mode",
                "Compliance risk",
                "Review package",
                "Identify license",
                "SBOM"
            )
        )

        findings.append(
            self._create_finding(
                "sbom_restricted_license",
                "Restricted License",
                "fail",
                "Medium",
                "Restricted license detected",
                "Demo Mode",
                "Legal exposure",
                "Review licensing",
                "Use approved licenses",
                "SBOM"
            )
        )

        return findings

    def _check_sbom_quality(self):

        findings = []

        findings.append(
            self._create_finding(
                "sbom_missing",
                "SBOM Missing",
                "fail",
                "High",
                "No SBOM generated",
                "Demo Mode",
                "Supply chain visibility gap",
                "Generate SBOM",
                "Use CycloneDX or SPDX",
                "SBOM"
            )
        )

        findings.append(
            self._create_finding(
                "sbom_incomplete",
                "Incomplete SBOM",
                "fail",
                "Medium",
                "SBOM missing components",
                "Demo Mode",
                "Inventory gap",
                "Regenerate SBOM",
                "Ensure full dependency coverage",
                "SBOM"
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
            target_type="sbom"
        )

        return RiskEngine.enrich_finding(
            finding
        )