import os
from grc_scanner.scanners.web.web_scanner import WebScanner

from grc_scanner.engine.compliance_engine import (
    ComplianceEngine
)

from grc_scanner.engine.risk_engine import (
    RiskEngine
)

from grc_scanner.reporters.json_report import (
    JsonReport
)

from grc_scanner.reporters.html_report import (
    HtmlReport
)

from grc_scanner.reporters.executive_report import (
    ExecutiveReport
)

from grc_scanner.scanners.network.network_scanner import (
    NetworkScanner
)

from grc_scanner.scanners.secrets.secrets_scanner import (
    SecretsScanner
)

from grc_scanner.scanners.vulnerability.vulnerability_scanner import (
    VulnerabilityScanner
)

from grc_scanner.scanners.container.container_scanner import (
    ContainerScanner
)

from grc_scanner.scanners.kubernetes.kubernetes_scanner import (
    KubernetesScanner
)

from grc_scanner.scanners.iac.iac_scanner import (
    IaCScanner
)

from grc_scanner.scanners.cicd.cicd_scanner import (
    CICDScanner
)

from grc_scanner.scanners.cloud.aws_scanner import (
    AWSScanner
)

from grc_scanner.scanners.cloud.azure_scanner import (
    AzureScanner
)

from grc_scanner.scanners.cloud.gcp_scanner import (
    GCPScanner
)

from grc_scanner.scanners.database.database_scanner import (
    DatabaseScanner
)

from grc_scanner.scanners.ssl.ssl_scanner import (
    SSLScanner
)

from grc_scanner.scanners.sbom.sbom_scanner import (
    SBOMScanner
)

from grc_scanner.scanners.api.api_scanner import (
    APIScanner
)

from grc_scanner.storage.scan_repository import (
    ScanRepository
)

from grc_scanner.storage.findings_repository import (
    FindingsRepository
)

from grc_scanner.storage.compliance_repository import (
    ComplianceRepository
)

from grc_scanner.storage.report_repository import (
    ReportRepository
)

from grc_scanner.storage.report_repository import (
    ReportRepository
)

class ScanEngine:

    def __init__(self):

        self.web_scanner = WebScanner()
        self.network_scanner = NetworkScanner()
        self.secrets_scanner = SecretsScanner()
        self.compliance_engine = ComplianceEngine()
        self.vulnerability_scanner = VulnerabilityScanner()
        self.container_scanner = ContainerScanner()
        self.kubernetes_scanner = KubernetesScanner()
        self.iac_scanner = IaCScanner()
        self.cicd_scanner = CICDScanner()
        self.aws_scanner = AWSScanner()
        self.azure_scanner = AzureScanner()
        self.gcp_scanner = GCPScanner()
        self.database_scanner = DatabaseScanner()
        self.ssl_scanner = SSLScanner()
        self.sbom_scanner = SBOMScanner()
        self.api_scanner = APIScanner()

    def run(self, target, scan_type="website"):

        print("SCAN_ENGINE_RUN_CALLED")
        print()
        print("=" * 60)
        print("Starting Scan")
        print("=" * 60)

        findings = []

        findings.extend(self.web_scanner.scan(target))

        parsed_host = (
            target
            .replace("https://", "")
            .replace("http://", "")
            .split("/")[0]
        )

        findings.extend(self.network_scanner.scan(parsed_host))
        findings.extend(self.secrets_scanner.scan("."))
        findings.extend(self.vulnerability_scanner.scan(target))
        findings.extend(self.container_scanner.scan("."))
        findings.extend(self.kubernetes_scanner.scan("."))
        findings.extend(self.iac_scanner.scan("."))
        findings.extend(self.cicd_scanner.scan("."))

        findings.extend(self.aws_scanner.scan())
        findings.extend(self.azure_scanner.scan())
        findings.extend(self.gcp_scanner.scan())

        findings.extend(self.database_scanner.scan())
        findings.extend(self.ssl_scanner.scan(target))
        findings.extend(self.sbom_scanner.scan("."))
        findings.extend(self.api_scanner.scan(target))

        findings = self.compliance_engine.map_controls(findings)

        compliance_scores = self.compliance_engine.calculate_scores(findings)

        overall_score = (
            RiskEngine.overall_score(
                findings
            )
        )

        scan_id = (
            ScanRepository.create_scan(
                target,
                overall_score,
                scan_type
            )
        )

        os.makedirs(
            "output",
            exist_ok=True
        )
        
        json_path = (
            f"output/scan_{scan_id}_report.json"
        )

        html_path = (
            f"output/scan_{scan_id}_report.html"
        )

        exec_path = (
            f"output/scan_{scan_id}_executive.txt"
        )

        print(
            "Scan Saved:",
            scan_id
        )

        FindingsRepository.save_findings(
            scan_id,
            findings
        )

        print(
            "Findings Saved"
        )

        ComplianceRepository.save_scores(
            scan_id,
            compliance_scores
        )

        print(
            "Compliance Scores Saved"
        )

        print("Generating JSON Report...")

        json_file = JsonReport.generate(
                        findings,
                        compliance_scores,
                        overall_risk_score=overall_score,
                        output_file=json_path
                    )

        print("Generated:", json_file)

        print("Generating HTML Report...")

        html_file = HtmlReport.generate(
            findings,
            compliance_scores,
            overall_score,
            output_file=html_path
        )

        print("Generated:", html_file)

        print("Generating Executive Report...")

        exec_file = ExecutiveReport.generate(
            findings,
            compliance_scores,
            overall_score,
            output_file=exec_path
        )

        print("Saving JSON Report...")

        print(
            "JSON Exists:",
            os.path.exists(json_path)
        )

        print(
            "HTML Exists:",
            os.path.exists(html_path)
        )

        print(
            "EXEC Exists:",
            os.path.exists(exec_path)
        )

        ReportRepository.save_report(
            scan_id,
            "json",
            json_path
        )

        print("JSON Report Saved")


        print("Saving HTML Report...")
        ReportRepository.save_report(
            scan_id,
            "html",
            html_path
        )
        print("HTML Report Saved")

        print("Saving Executive Report...")
        ReportRepository.save_report(
            scan_id,
            "executive",
            exec_path
        )
        print("Executive Report Saved")

        print("Generated:", exec_file)

        print()
        print("=" * 60)
        print("SCAN SUMMARY")
        print("=" * 60)

        print("Total Findings:", len(findings))
        print("Overall Risk Score:", overall_score)

        result = {
            "target": target,
            "findings": findings,
            "overall_score": overall_score,
            "compliance_scores": compliance_scores,
            "total_findings": len(findings)
        }

        return result