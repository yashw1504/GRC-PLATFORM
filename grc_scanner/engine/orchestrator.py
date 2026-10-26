import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from grc_scanner.engine.finding_normalizer import FindingNormalizer
from grc_scanner.engine.deduplicator import FindingDeduplicator
from grc_scanner.engine.scanner_errors import scanner_error_finding


class ScannerOrchestrator:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def run(self, scanners, *args):

        findings = []

        def run_scanner(scanner):
            scanner_name = getattr(scanner, "name", scanner.__class__.__name__)
            try:
                self.logger.info(
                    f"Running {scanner_name}"
                )
            except Exception as e:
                self.logger.exception(
                    f"{scanner_name} failed: {e}"
                )
                return []
            return scanner_name, scanner.scan(*args)

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(run_scanner, scanner): scanner for scanner in scanners}
            for future in as_completed(futures):
                scanner = futures[future]
                scanner_name = getattr(scanner, "name", scanner.__class__.__name__)
                try:
                    result = future.result()
                    if result and result[1]:
                        findings.extend(result[1])
                except Exception as e:
                    self.logger.exception("%s failed: %s", scanner_name, e)
                    findings.append(scanner_error_finding(
                        scanner_name,
                        "The scanner could not complete this check.",
                    ))

        findings = FindingNormalizer.normalize(
            findings
        )

        findings = FindingDeduplicator.deduplicate(
            findings
        )

        return findings
