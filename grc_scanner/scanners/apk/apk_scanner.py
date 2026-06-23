from pathlib import Path

from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine


class APKScanner:

    name = "apk_scanner"

    def scan(self, apk_path):

        findings = []

        apk_file = Path(apk_path)

        if not apk_file.exists():

            findings.append(
                self._create_finding(
                    "apk_missing",
                    "APK File Missing",
                    "fail",
                    "Critical",
                    "APK file not found",
                    apk_path,
                    "Scan cannot be performed.",
                    "Upload valid APK.",
                    "Verify file path.",
                    "Mobile Security"
                )
            )

            return findings

        findings.extend(
            self._check_debuggable(apk_file)
        )

        findings.extend(
            self._check_backup_enabled(apk_file)
        )

        findings.extend(
            self._check_apk_size(apk_file)
        )

        return findings

    def _check_debuggable(self, apk_file):

        findings = []

        return findings

    def _check_backup_enabled(self, apk_file):

        findings = []

        return findings

    def _check_apk_size(self, apk_file):

        findings = []

        size_mb = apk_file.stat().st_size / 1024 / 1024

        if size_mb > 100:

            findings.append(
                self._create_finding(
                    "apk_large_size",
                    "Large APK Size",
                    "fail",
                    "Low",
                    f"APK size is {size_mb:.2f} MB",
                    str(apk_file),
                    "Large APK may contain unnecessary resources.",
                    "Reduce APK size.",
                    "Remove unused libraries.",
                    "Mobile Security"
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
            target_type="apk"
        )

        return RiskEngine.enrich_finding(
            finding
        )