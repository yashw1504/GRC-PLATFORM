from pathlib import Path
import yaml

from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine

from grc_scanner.integrations.kubescape_wrapper import (
    KubescapeWrapper
)


class KubernetesScanner:

    name = "kubernetes_scanner"

    def scan(self, path="."):

        if KubescapeWrapper.is_available():
            return self._scan_with_kubescape(path)

        return self._scan_yaml(path)

    def _scan_with_kubescape(self, path):

        findings = []

        results = KubescapeWrapper.scan(path)

        if not results:
            return findings

        findings.append(
            self._create_finding(
                "k8s_scan_completed",
                "Kubescape Scan",
                "pass",
                "Info",
                "Kubescape scan completed",
                path,
                "",
                "",
                "",
                "Kubernetes"
            )
        )

        return findings

    def _scan_yaml(self, path):

        findings = []

        root = Path(path)

        yaml_files = []

        yaml_files.extend(
            root.rglob("*.yaml")
        )

        yaml_files.extend(
            root.rglob("*.yml")
        )

        network_policy_found = False

        for file in yaml_files:

            try:

                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                docs = list(
                    yaml.safe_load_all(content)
                )

                for doc in docs:

                    if not isinstance(doc, dict):
                        continue

                    kind = doc.get("kind", "")

                    if kind == "NetworkPolicy":
                        network_policy_found = True

                    findings.extend(
                        self._check_privileged(
                            file,
                            content
                        )
                    )

                    findings.extend(
                        self._check_privilege_escalation(
                            file,
                            content
                        )
                    )

                    findings.extend(
                        self._check_hostpath(
                            file,
                            content
                        )
                    )

                    findings.extend(
                        self._check_resource_limits(
                            file,
                            content
                        )
                    )

            except Exception:
                pass

        if not network_policy_found:

            findings.append(
                self._create_finding(
                    "k8s_network_policy_missing",
                    "Network Policy Missing",
                    "fail",
                    "Medium",
                    "No NetworkPolicy found",
                    path,
                    "Network segmentation absent.",
                    "Create Kubernetes Network Policies.",
                    "Implement Zero Trust networking.",
                    "Kubernetes"
                )
            )

        return findings

    def _check_privileged(
        self,
        file,
        content
    ):

        findings = []

        if "privileged: true" in content:

            findings.append(
                self._create_finding(
                    "k8s_pod_privileged",
                    "Privileged Container",
                    "fail",
                    "Critical",
                    "Privileged container detected",
                    str(file),
                    "Container has host-level privileges.",
                    "Disable privileged mode.",
                    "Use least privilege.",
                    "Kubernetes"
                )
            )

        return findings

    def _check_privilege_escalation(
        self,
        file,
        content
    ):

        findings = []

        if (
            "allowPrivilegeEscalation: true"
            in content
        ):

            findings.append(
                self._create_finding(
                    "k8s_container_privilege_escalation",
                    "Privilege Escalation Enabled",
                    "fail",
                    "High",
                    "Privilege escalation enabled",
                    str(file),
                    "Container may gain elevated access.",
                    "Disable privilege escalation.",
                    "Set allowPrivilegeEscalation=false.",
                    "Kubernetes"
                )
            )

        return findings

    def _check_hostpath(
        self,
        file,
        content
    ):

        findings = []

        if "hostPath:" in content:

            findings.append(
                self._create_finding(
                    "k8s_host_path_mounted",
                    "HostPath Volume Mounted",
                    "fail",
                    "High",
                    "Host filesystem mounted",
                    str(file),
                    "Host compromise risk.",
                    "Avoid hostPath volumes.",
                    "Use Persistent Volumes.",
                    "Kubernetes"
                )
            )

        return findings

    def _check_resource_limits(
        self,
        file,
        content
    ):

        findings = []

        if "resources:" not in content:

            findings.append(
                self._create_finding(
                    "k8s_resource_limits_missing",
                    "Resource Limits Missing",
                    "fail",
                    "Medium",
                    "Container missing limits",
                    str(file),
                    "Resource exhaustion possible.",
                    "Define CPU and memory limits.",
                    "Apply quotas.",
                    "Kubernetes"
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
            target_type="kubernetes"
        )

        return RiskEngine.enrich_finding(
            finding
        )