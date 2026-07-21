import os
from grc_scanner.engine.compliance_engine import ComplianceEngine
from grc_scanner.engine.orchestrator import ScannerOrchestrator
from grc_scanner.engine.risk_engine import RiskEngine
from grc_scanner.reporters.json_report import JsonReport
from grc_scanner.reporters.html_report import HtmlReport
from grc_scanner.reporters.executive_report import ExecutiveReport
from grc_scanner.scanners.website_scan import WebsiteScanner
from grc_scanner.scanners.secrets_scanner_impl import SecretsScanner
from grc_scanner.scanners.vulnerability_scanner_impl import VulnerabilityScanner
from grc_scanner.scanners.container_scanner_impl import ContainerScanner
from grc_scanner.scanners.iac_scanner_impl import IaCScanner
from grc_scanner.scanners.source_scanner import SourceScanner
from grc_scanner.storage.scan_repository import ScanRepository
from grc_scanner.storage.findings_repository import FindingsRepository
from grc_scanner.storage.compliance_repository import ComplianceRepository
from grc_scanner.storage.report_repository import ReportRepository
from grc_scanner.utils.file_utils import FileUtils
from grc_scanner.db_init import init_database

class ScanEngine:
    def __init__(self):
        # Initialize DB if needed
        try:
            init_database()
        except:
            pass

        self.scanners = {
            "website": WebsiteScanner(),
            "source": SourceScanner(),
            "secrets": SecretsScanner(),
            "vulnerability": VulnerabilityScanner(),
            "container": ContainerScanner(),
            "iac": IaCScanner(),
        }

        self.SCAN_GROUPS = {
            "website": ["website", "vulnerability"],
            "source": ["source"],
            "container": ["container"],
            "iac": ["iac"],
            "secrets": ["secrets"],
            "vulnerability": ["vulnerability"],
            "full": ["website", "source", "container", "iac", "secrets", "vulnerability"],
        }

        self.compliance_engine = ComplianceEngine()

    def run(self, target, scan_type="website", source_path=None):
        print("=" * 60)
        print(f"Starting {scan_type.upper()} scan on {target}")
        print("=" * 60)

        scanner_names = self.SCAN_GROUPS.get(scan_type, self.SCAN_GROUPS.get("website"))
        all_findings = []

        scan_target = target
        for name in scanner_names:
            scanner = self.scanners[name]
            try:
                if name in ("source", "container", "iac", "secrets"):
                    path = source_path or target
                    findings = scanner.scan(path)
                else:
                    findings = scanner.scan(target)
                all_findings.extend(findings)
            except Exception as e:
                print(f"[{name}] Error: {e}")

        # Compliance mapping
        all_findings = self.compliance_engine.map_controls(all_findings)
        compliance_scores = self.compliance_engine.calculate_scores(all_findings)
        overall_score = RiskEngine.overall_score(all_findings)

        # Save to DB
        scan_id = ScanRepository.create_scan(target, overall_score, scan_type)
        os.makedirs("output", exist_ok=True)

        FindingsRepository.save_findings(scan_id, all_findings)
        ComplianceRepository.save_scores(scan_id, compliance_scores)

        # Generate reports
        json_path = f"output/scan_{scan_id}_report.json"
        html_path = f"output/scan_{scan_id}_report.html"
        exec_path = f"output/scan_{scan_id}_executive.txt"

        JsonReport.generate(all_findings, compliance_scores, overall_risk_score=overall_score, output_file=json_path)
        HtmlReport.generate(all_findings, compliance_scores, overall_score, output_file=html_path)
        ExecutiveReport.generate(all_findings, compliance_scores, overall_score, output_file=exec_path)

        ReportRepository.save_report(scan_id, "json", json_path)
        ReportRepository.save_report(scan_id, "html", html_path)
        ReportRepository.save_report(scan_id, "executive", exec_path)

        print()
        print("=" * 60)
        print("SCAN SUMMARY")
        print("=" * 60)
        print(f"Total Findings: {len(all_findings)}")
        print(f"Overall Risk Score: {overall_score}/100")
        for fw, score in compliance_scores.items():
            print(f"  {fw:<10} {score}%")

        return {
            "target": target,
            "findings": all_findings,
            "overall_score": overall_score,
            "compliance_scores": compliance_scores,
            "total_findings": len(all_findings)
        }