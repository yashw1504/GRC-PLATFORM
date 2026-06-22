from grc_scanner.engine.scan_engine import (
    ScanEngine
)
TARGET = "https://www.coinhako.com/"

engine = ScanEngine()

result = engine.run(
    TARGET
)

print()

print("=" * 60)
print("SCAN COMPLETE")
print("=" * 60)

print()

print(
    f"Overall Risk Score: "
    f"{result['overall_score']}/100"
)

print()

print("Compliance Scores")

for framework, score in (
    result["compliance_scores"]
    .items()
):
    print(
        f"{framework:<10} {score}%"
    )

print()

print(
    f"Total Findings: "
    f"{result['total_findings']}"
)