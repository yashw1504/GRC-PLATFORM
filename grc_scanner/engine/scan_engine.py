import os
from grc_scanner.engine.compliance_engine import ComplianceEngine
from grc_scanner.engine.risk_engine import RiskEngine
from grc_scanner.reporters.json_report import JsonReport
from grc_scanner.reporters.html_report import HtmlReport
from grc_scanner.reporters.executive_report import ExecutiveReport
from grc_scanner.storage.scan_repository import ScanRepository
from grc_scanner.storage.findings_repository import FindingsRepository
from grc_scanner.storage.compliance_repository import ComplianceRepository
from grc_scanner.storage.report_repository import ReportRepository
from grc_scanner.db_init import init_database

# Only import what actually exists
from grc_scanner.scanners.website_scan import WebsiteScanner
from grc_scanner.scanners.source_scanner import SourceScanner
from grc_scanner.scanners.secrets_scanner_impl import SecretsScanner
from grc_scanner.scanners.vulnerability_scanner_impl import VulnerabilityScanner
from grc_scanner.scanners.container_scanner_impl import ContainerScanner
from grc_scanner.scanners.iac_scanner_impl import IaCScanner

class ScanEngine:
    def __init__(self):
        try:
            init_database()
        except:
            pass

        self.compliance_engine = ComplianceEngine()

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
            "source": ["source", "secrets"],
            "container": ["container"],
            "iac": ["iac"],
            "secrets": ["secrets"],
            "vulnerability": ["vulnerability"],
            "full": ["website", "source", "container", "iac", "secrets", "vulnerability"],
        }

    def _finding_to_dict(self, finding):
        """Convert a finding (dict or Finding object) to dict"""
        if hasattr(finding, 'to_dict'):
            return finding.to_dict()
        if isinstance(finding, dict):
            return finding
        return {"name": str(finding)}

    def run(self, target, scan_type="website", source_path=None):
        print("=" * 60)
        print(f"Starting {scan_type.upper()} scan on {target}")
        print("=" * 60)

        scanner_names = self.SCAN_GROUPS.get(scan_type, ["website"])
        all_findings = []

        for name in scanner_names:
            scanner = self.scanners.get(name)
            if not scanner:
                print(f"[{name}] No scanner registered")
                continue
            try:
                if name in ("source", "container", "iac", "secrets"):
                    path = source_path or target
                    findings = scanner.scan(path)
                else:
                    findings = scanner.scan(target)

                if findings:
                    print(f"  [{name}] Found {len(findings)} items")
                    all_findings.extend(findings)

            except Exception as e:
                print(f"[{name}] Error: {e}")

        # Convert to Finding objects if they're dicts
        from grc_scanner.engine.finding import Finding
        converted = []
        for f in all_findings:
            if isinstance(f, Finding):
                converted.append(f)
            elif isinstance(f, dict):
                finding = Finding(
                    check_id=f.get("check_id", "unknown"),
                    name=f.get("name", "Unknown"),
                    status=f.get("status", "info"),
                    severity=f.get("severity", "Info"),
                    description=f.get("description", ""),
                    evidence=f.get("evidence", ""),
                    category=f.get("category", ""),
                    target_asset=f.get("target_asset", ""),
                    scanner_name=f.get("scanner_name", ""),
                    raw_data=f.get("raw_data", {})
                )
                converted.append(finding)

        # Compliance mapping
        converted = self.compliance_engine.map_controls(converted)
        compliance_scores = self.compliance_engine.calculate_scores(converted)
        overall_score = RiskEngine.overall_score(converted)

        # Save to DB
        scan_id = ScanRepository.create_scan(target, overall_score, scan_type)
        os.makedirs("output", exist_ok=True)

        FindingsRepository.save_findings(scan_id, converted)
        ComplianceRepository.save_scores(scan_id, compliance_scores)

        # Generate reports
        json_path = f"output/scan_{scan_id}_report.json"
        html_path = f"output/scan_{scan_id}_report.html"
        exec_path = f"output/scan_{scan_id}_executive.txt"

        JsonReport.generate(converted, compliance_scores,
                           overall_risk_score=overall_score, output_file=json_path)
        HtmlReport.generate(converted, compliance_scores,
                           overall_score, output_file=html_path)
        ExecutiveReport.generate(converted, compliance_scores,
                                overall_score, output_file=exec_path)

        ReportRepository.save_report(scan_id, "json", json_path)
        ReportRepository.save_report(scan_id, "html", html_path)
        ReportRepository.save_report(scan_id, "executive", exec_path)

        print()
        print("=" * 60)
        print(f"SCAN #{scan_id} COMPLETE")
        print(f"Total Findings: {len(converted)}")
        print(f"Risk Score: {overall_score}/100")
        print(f"Risk Rating: {RiskEngine.risk_rating(overall_score)}")
        print("=" * 60)

        return {
            "target": target,
            "scan_id": scan_id,
            "findings": converted,
            "overall_score": overall_score,
            "compliance_scores": compliance_scores,
            "total_findings": len(converted)
        }