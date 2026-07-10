import logging

from grc_scanner.engine.finding_normalizer import FindingNormalizer
from grc_scanner.engine.deduplicator import FindingDeduplicator


class ScannerOrchestrator:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def run(self, scanners, *args):

        findings = []

        for scanner in scanners:

            try:

                scanner_name = getattr(
                    scanner,
                    "name",
                    scanner.__class__.__name__
                )

                self.logger.info(
                    f"Running {scanner_name}"
                )

                result = scanner.scan(*args)

                if result:
                    findings.extend(result)

            except Exception as e:

                self.logger.exception(
                    f"{scanner_name} failed: {e}"
                )

        findings = FindingNormalizer.normalize(
            findings
        )

        findings = FindingDeduplicator.deduplicate(
            findings
        )

        return findings