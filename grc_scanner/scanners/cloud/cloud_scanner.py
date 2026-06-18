from grc_scanner.scanners.cloud.aws_scanner import AWSScanner
from grc_scanner.scanners.cloud.azure_scanner import AzureScanner

class CloudScanner:

    def scan(self):

        findings = []

        findings.extend(
            AWSScanner().scan()
        )

        findings.extend(
            AzureScanner().scan()
        )

        return findings