from pathlib import Path


class ExecutiveReport:

    @staticmethod
    def generate(
        findings,
        compliance_scores,
        overall_risk_score,
        output_file="output/executive_summary.txt"
    ):

        Path("output").mkdir(
            exist_ok=True
        )

        critical = [
            f for f in findings
            if f.severity == "Critical"
        ]

        high = [
            f for f in findings
            if f.severity == "High"
        ]

        report = []

        report.append("=" * 60)
        report.append("EXECUTIVE SECURITY SUMMARY")
        report.append("=" * 60)

        report.append("")
        report.append(
            f"Overall Risk Score: "
            f"{overall_risk_score}/100"
        )

        report.append("")

        report.append("COMPLIANCE SCORES")

        for framework, score in compliance_scores.items():

            report.append(
                f"{framework:<10} {score}%"
            )

        report.append("")

        report.append(
            f"Critical Findings: {len(critical)}"
        )

        report.append(
            f"High Findings: {len(high)}"
        )

        report.append("")

        report.append(
            "TOP RISKS"
        )

        report.append("-" * 60)

        top_findings = sorted(
            findings,
            key=lambda x: x.risk_score,
            reverse=True
        )[:10]

        for finding in top_findings:

            report.append("")
            report.append(
                f"Finding: {finding.name}"
            )

            report.append(
                f"Severity: {finding.severity}"
            )

            report.append(
                f"Priority: {finding.priority}"
            )

            report.append(
                f"Business Impact: "
                f"{finding.business_impact}"
            )

            report.append(
                f"Recommendation: "
                f"{finding.remediation}"
            )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "\n".join(report)
            )

        return output_file