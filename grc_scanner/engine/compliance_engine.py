import json
from pathlib import Path


class ComplianceEngine:

    def __init__(self):
        mapping_file = Path("grc_scanner/frameworks/frameworks.json")

        with open(
            mapping_file,
            "r",
            encoding="utf-8"
        ) as f:
            self.data = json.load(f)

    def map_controls(self, findings):
        mapping = self.data.get("check_to_control_mapping", {})

        for finding in findings:
            finding.mapped_controls = mapping.get(finding.check_id, [])

            if not finding.mapped_controls:
                print(f"WARNING: No compliance mapping for {finding.check_id}")

        return findings

    def calculate_scores(self, findings):
        mapping = self.data.get("check_to_control_mapping", {})

        for finding in findings:
            if not hasattr(finding, "mapped_controls") or finding.mapped_controls is None:
                finding.mapped_controls = mapping.get(finding.check_id, [])

        frameworks = {
            "PCI": [],
            "ISO": [],
            "GDPR": [],
            "HIPAA": [],
            "SOC2": [],
            "DPDPA": [],
            "OWASP": []
        }

        for finding in findings:
            for control in finding.mapped_controls:
                for fw in frameworks:
                    if control.startswith(fw):
                        frameworks[fw].append(finding)
                        break

        scores = {}

        for fw, controls in frameworks.items():
            if not controls:
                scores[fw] = 100
                continue

            failed = len([f for f in controls if f.status == "fail"])
            total = len(controls)

            scores[fw] = max(
                0,
                round(((total - failed) / total) * 100)
            )

        return scores