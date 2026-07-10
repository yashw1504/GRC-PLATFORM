from grc_scanner.engine.finding import Finding


class FindingDeduplicator:

    @staticmethod
    def deduplicate(findings):

        unique = {}
        merged = []

        for finding in findings:

            key = (
                finding.check_id,
                finding.evidence,
                finding.target_type
            )

            if key not in unique:
                unique[key] = finding
                merged.append(finding)

        return merged