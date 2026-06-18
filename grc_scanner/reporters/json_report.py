import json
from pathlib import Path


class JsonReport:

    @staticmethod
    def generate(
        findings,
        compliance_scores,
        overall_risk_score,
        output_file="output/report.json"
    ):

        report = {
            "summary": {
                "total_findings": len(findings),
                "overall_risk_score": overall_risk_score
            },
            "compliance_scores": compliance_scores,
            "findings": []
        }

        for finding in findings:

            report["findings"].append(
                finding.to_dict()
            )

        Path("output").mkdir(
            exist_ok=True
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                report,
                f,
                indent=4
            )

        return output_file