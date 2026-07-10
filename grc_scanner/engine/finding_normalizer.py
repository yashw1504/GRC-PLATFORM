from typing import List

from grc_scanner.engine.finding import Finding


class FindingNormalizer:

    @staticmethod
    def normalize(findings: List[Finding]):

        normalized = []

        for finding in findings:

            if not isinstance(finding, Finding):
                continue

            if not finding.category:
                finding.category = "General"

            if not finding.target_type:
                finding.target_type = "unknown"

            if not finding.scanner_name:
                finding.scanner_name = "unknown"

            if not finding.status:
                finding.status = "info"

            if not finding.severity:
                finding.severity = "Info"

            normalized.append(finding)

        return normalized