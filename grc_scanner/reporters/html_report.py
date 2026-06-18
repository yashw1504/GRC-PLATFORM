from pathlib import Path


class HtmlReport:

    @staticmethod
    def generate(
        findings,
        compliance_scores,
        overall_risk_score=0,
        output_file="output/report.html"
    ):

        Path("output").mkdir(
            exist_ok=True
        )

        html = f"""
<!DOCTYPE html>
<html>
<head>
<title>GRC Security Assessment Report</title>

<style>

body {{
    font-family: Arial;
    margin: 40px;
    background-color: #f5f5f5;
}}

h1 {{
    color: #1f4e79;
}}

.card {{
    background: white;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 10px;
    box-shadow: 0px 0px 10px #cccccc;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th {{
    background-color: #1f4e79;
    color: white;
    padding: 10px;
}}

td {{
    padding: 10px;
    border: 1px solid #ddd;
}}

.pass {{
    color: green;
    font-weight: bold;
}}

.fail {{
    color: red;
    font-weight: bold;
}}

.high {{
    color: red;
}}

.medium {{
    color: orange;
}}

.low {{
    color: green;
}}

</style>
</head>

<body>

<h1>GRC Security Assessment Report</h1>

<div class="card">

<h2>Overall Risk Score</h2>

<h1>{overall_risk_score}/100</h1>

</div>

<div class="card">

<h2>Compliance Scores</h2>

<table>

<tr>
<th>Framework</th>
<th>Score</th>
</tr>
"""

        for framework, score in compliance_scores.items():

            html += f"""
<tr>
<td>{framework}</td>
<td>{score}%</td>
</tr>
"""

        html += """
</table>
</div>

<div class="card">

<h2>Security Findings</h2>

<table>

<tr>
<th>Check</th>
<th>Status</th>
<th>Severity</th>
<th>Risk Score</th>
<th>Priority</th>
<th>Evidence</th>
</tr>
"""

        for finding in findings:

            html += f"""
<tr>
<td>{finding.name}</td>
<td>{finding.status}</td>
<td>{finding.severity}</td>
<td>{finding.risk_score}</td>
<td>{finding.priority}</td>
<td>{finding.evidence}</td>
</tr>
"""

        html += """
</table>
</div>

</body>
</html>
"""

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(html)

        return output_file