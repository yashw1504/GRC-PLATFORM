from pathlib import Path

from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine


class CICDScanner:

    name = "cicd_scanner"

    def scan(self, path="."):

        findings = []

        root = Path(path)

        pipeline_files = []

        pipeline_files.extend(
            root.rglob("*.yml")
        )

        pipeline_files.extend(
            root.rglob("*.yaml")
        )

        features = {
            "sast": False,
            "gitleaks": False,
            "dependency_scan": False,
            "container_scan": False,
            "iac_scan": False,
            "k8s_scan": False,
            "sbom": False,
            "security_gate": False,
            "notifications": False,
            "artifact_signing": False
        }

        for file in pipeline_files:

            try:

                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                findings.extend(
                    self._check_unpinned_actions(
                        file,
                        content
                    )
                )

                findings.extend(
                    self._check_secret_logging(
                        file,
                        content
                    )
                )

                findings.extend(
                    self._check_permissions(
                        file,
                        content
                    )
                )

                findings.extend(
                    self._check_latest_tag(
                        file,
                        content
                    )
                )

                if self._has_sast(content):
                    features["sast"] = True

                if self._has_gitleaks(content):
                    features["gitleaks"] = True

                if self._has_dependency_scan(content):
                    features["dependency_scan"] = True

                if self._has_trivy(content):
                    features["container_scan"] = True

                if self._has_checkov(content):
                    features["iac_scan"] = True

                if self._has_kubescape(content):
                    features["k8s_scan"] = True

                if self._has_sbom(content):
                    features["sbom"] = True

                if self._has_security_gate(content):
                    features["security_gate"] = True

                if self._has_notifications(content):
                    features["notifications"] = True

                if self._has_artifact_signing(content):
                    features["artifact_signing"] = True

            except Exception:
                pass

        findings.extend(
            self._generate_missing_control_findings(
                features,
                path
            )
        )

        maturity = self._calculate_maturity(
            features
        )

        findings.append(
            self._create_finding(
                "cicd_maturity",
                "CI/CD Security Maturity",
                "pass",
                "Info",
                f"CI/CD Security Score = {maturity}/100",
                str(features),
                "",
                "",
                "",
                "CI/CD"
            )
        )

        return findings

    def _has_sast(self, content):

        tools = [
            "semgrep",
            "codeql",
            "sonarqube",
            "checkmarx",
            "fortify",
            "veracode"
        ]

        return any(
            tool in content.lower()
            for tool in tools
        )

    def _has_gitleaks(self, content):

        return (
            "gitleaks"
            in
            content.lower()
        )

    def _has_dependency_scan(self, content):

        tools = [
            "trivy",
            "snyk",
            "dependency-check",
            "dependabot"
        ]

        return any(
            tool in content.lower()
            for tool in tools
        )

    def _has_trivy(self, content):

        return (
            "trivy"
            in
            content.lower()
        )

    def _has_checkov(self, content):

        return (
            "checkov"
            in
            content.lower()
        )

    def _has_kubescape(self, content):

        return (
            "kubescape"
            in
            content.lower()
        )

    def _has_sbom(self, content):

        tools = [
            "syft",
            "cyclonedx",
            "spdx"
        ]

        return any(
            tool in content.lower()
            for tool in tools
        )

    def _has_security_gate(self, content):

        gates = [
            "exit 1",
            "severity-threshold",
            "fail-on-severity",
            "critical"
        ]

        return any(
            gate in content.lower()
            for gate in gates
        )

    def _has_notifications(self, content):

        channels = [
            "slack",
            "teams",
            "pagerduty",
            "webhook"
        ]

        return any(
            c in content.lower()
            for c in channels
        )

    def _has_artifact_signing(self, content):

        tools = [
            "cosign",
            "sigstore",
            "notation"
        ]

        return any(
            tool in content.lower()
            for tool in tools
        )

    def _check_unpinned_actions(
        self,
        file,
        content
    ):

        findings = []

        for line in content.splitlines():

            if "uses:" in line and "@" in line:

                version = (
                    line.split("@")[-1]
                    .strip()
                )

                if len(version) < 20:

                    findings.append(
                        self._create_finding(
                            "cicd_unpinned_actions",
                            "Unpinned GitHub Action",
                            "fail",
                            "High",
                            "Action not pinned to SHA",
                            str(file),
                            "Supply chain attack risk.",
                            "Pin actions to commit SHA.",
                            "Use immutable references.",
                            "CI/CD"
                        )
                    )

        return findings

    def _check_secret_logging(
        self,
        file,
        content
    ):

        findings = []

        patterns = [
            "echo ${{ secrets.",
            "printenv",
            "env"
        ]

        for p in patterns:

            if p.lower() in content.lower():

                findings.append(
                    self._create_finding(
                        "cicd_secrets_in_logs",
                        "Secrets Printed In Logs",
                        "fail",
                        "Critical",
                        "Secrets may be exposed",
                        str(file),
                        "Credential disclosure risk.",
                        "Remove secret output.",
                        "Mask sensitive values.",
                        "CI/CD"
                    )
                )

                break

        return findings

    def _check_permissions(
        self,
        file,
        content
    ):

        findings = []

        if "permissions:" not in content:

            findings.append(
                self._create_finding(
                    "cicd_workflow_permissions_excessive",
                    "Workflow Permissions Undefined",
                    "fail",
                    "High",
                    "Workflow permissions missing",
                    str(file),
                    "GitHub defaults may be excessive.",
                    "Define permissions block.",
                    "Apply least privilege.",
                    "CI/CD"
                )
            )

        return findings

    def _check_latest_tag(
        self,
        file,
        content
    ):

        findings = []

        if ":latest" in content:

            findings.append(
                self._create_finding(
                    "cicd_latest_tag_usage",
                    "Latest Docker Tag Usage",
                    "fail",
                    "Medium",
                    "Latest tag detected",
                    str(file),
                    "Supply chain risk.",
                    "Pin versions.",
                    "Use immutable tags.",
                    "CI/CD"
                )
            )

        return findings

    def _generate_missing_control_findings(
        self,
        features,
        path
    ):

        findings = []

        mapping = {
            "sast": "cicd_no_codeql_or_sast",
            "gitleaks": "cicd_no_secret_scanning",
            "dependency_scan": "cicd_vulnerable_dependency",
            "container_scan": "cicd_no_container_scanning",
            "iac_scan": "cicd_no_iac_scanning",
            "k8s_scan": "cicd_no_k8s_scanning",
            "sbom": "cicd_no_sbom_generation",
            "security_gate": "cicd_no_security_gate",
            "notifications": "cicd_no_notifications",
            "artifact_signing": "cicd_unsigned_artifacts"
        }

        for feature, check_id in mapping.items():

            if not features[feature]:

                findings.append(
                    self._create_finding(
                        check_id,
                        check_id.replace(
                            "_",
                            " "
                        ).title(),
                        "fail",
                        "Medium",
                        f"{feature} not detected",
                        path,
                        "Security control missing.",
                        "Implement control.",
                        "Follow DevSecOps best practices.",
                        "CI/CD"
                    )
                )

        return findings

    def _calculate_maturity(
        self,
        features
    ):

        weights = {
            "sast": 10,
            "gitleaks": 10,
            "dependency_scan": 10,
            "container_scan": 10,
            "iac_scan": 10,
            "k8s_scan": 10,
            "sbom": 10,
            "security_gate": 10,
            "notifications": 10,
            "artifact_signing": 10
        }

        score = 0

        for key, value in weights.items():

            if features[key]:
                score += value

        return score

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
            target_type="cicd"
        )

        return RiskEngine.enrich_finding(
            finding
        )