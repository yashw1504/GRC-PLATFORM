from pathlib import Path
import re

from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine

from grc_scanner.integrations.trivy_wrapper import (
    TrivyWrapper
)


class ContainerScanner:

    name = "container_scanner"

    def scan(self, path="."):

        if TrivyWrapper.is_available():
            return self._scan_with_trivy(path)

        return self._scan_with_dockerfile(path)

    def _scan_with_trivy(self, path):

        findings = []

        results = TrivyWrapper.scan(path)

        for result in results.get("Results", []):

            for vuln in result.get("Vulnerabilities", []):

                severity = vuln.get(
                    "Severity",
                    "Medium"
                )

                findings.append(
                    self._create_finding(
                        check_id="container_cve_found",
                        name=vuln.get(
                            "VulnerabilityID",
                            "Container CVE"
                        ),
                        status="fail",
                        severity=severity,
                        description=vuln.get(
                            "Title",
                            "Container vulnerability detected"
                        ),
                        evidence=result.get(
                            "Target",
                            ""
                        ),
                        business_impact=(
                            "Container vulnerability may be exploited."
                        ),
                        remediation=(
                            "Update vulnerable package."
                        ),
                        recommendation=(
                            "Apply vendor patch."
                        ),
                        category="Container Security"
                    )
                )

        return findings

    def _scan_with_dockerfile(self, path):

        findings = []

        root = Path(path)

        dockerfiles = list(
            root.rglob("Dockerfile")
        )

        for dockerfile in dockerfiles:

            try:

                content = dockerfile.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                findings.extend(
                    self._check_run_as_root(
                        dockerfile,
                        content
                    )
                )

                findings.extend(
                    self._check_latest_tag(
                        dockerfile,
                        content
                    )
                )

                findings.extend(
                    self._check_healthcheck(
                        dockerfile,
                        content
                    )
                )

                findings.extend(
                    self._check_secrets(
                        dockerfile,
                        content
                    )
                )

                findings.extend(
                    self._check_exposed_ports(
                        dockerfile,
                        content
                    )
                )

            except Exception:
                pass

        return findings

    def _check_run_as_root(
        self,
        dockerfile,
        content
    ):

        findings = []

        if "USER root" in content:

            findings.append(
                self._create_finding(
                    "container_runs_as_root",
                    "Container Runs As Root",
                    "fail",
                    "Critical",
                    "Container configured to run as root",
                    str(dockerfile),
                    "Privilege escalation risk.",
                    "Use non-root user.",
                    "Create dedicated application user.",
                    "Container Security"
                )
            )

        return findings

    def _check_latest_tag(
        self,
        dockerfile,
        content
    ):

        findings = []

        if re.search(
            r"FROM\s+.*:latest",
            content,
            re.IGNORECASE
        ):

            findings.append(
                self._create_finding(
                    "container_latest_tag",
                    "Latest Tag Usage",
                    "fail",
                    "Medium",
                    "Container uses latest tag",
                    str(dockerfile),
                    "Unpredictable image updates.",
                    "Pin image version.",
                    "Use immutable versions.",
                    "Container Security"
                )
            )

        return findings

    def _check_healthcheck(
        self,
        dockerfile,
        content
    ):

        findings = []

        if "HEALTHCHECK" not in content.upper():

            findings.append(
                self._create_finding(
                    "container_no_healthcheck",
                    "Healthcheck Missing",
                    "fail",
                    "Medium",
                    "Container missing HEALTHCHECK",
                    str(dockerfile),
                    "Container health cannot be monitored.",
                    "Add HEALTHCHECK instruction.",
                    "Implement health endpoint.",
                    "Container Security"
                )
            )

        return findings

    def _check_secrets(
        self,
        dockerfile,
        content
    ):

        findings = []

        patterns = [
            r"PASSWORD\s*=",
            r"SECRET\s*=",
            r"API_KEY\s*=",
            r"TOKEN\s*="
        ]

        for pattern in patterns:

            if re.search(
                pattern,
                content,
                re.IGNORECASE
            ):

                findings.append(
                    self._create_finding(
                        "container_secrets_in_env",
                        "Secrets In Container",
                        "fail",
                        "Critical",
                        "Secret found in Dockerfile",
                        str(dockerfile),
                        "Credential exposure risk.",
                        "Remove secret from image.",
                        "Use vault or runtime secret injection.",
                        "Container Security"
                    )
                )

                break

        return findings

    def _check_exposed_ports(
        self,
        dockerfile,
        content
    ):

        findings = []

        risky_ports = [
            "21",
            "22",
            "23",
            "3389",
            "445"
        ]

        for port in risky_ports:

            if f"EXPOSE {port}" in content:

                findings.append(
                    self._create_finding(
                        "container_exposed_ports",
                        "Risky Exposed Port",
                        "fail",
                        "High",
                        f"Port {port} exposed",
                        str(dockerfile),
                        "Service may be externally accessible.",
                        "Restrict exposed ports.",
                        "Use internal networking.",
                        "Container Security"
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
            target_type="container"
        )

        return RiskEngine.enrich_finding(
            finding
        )