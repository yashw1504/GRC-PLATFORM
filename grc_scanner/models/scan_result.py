from dataclasses import dataclass, field


@dataclass
class ScanResult:

    target: str

    findings: list = field(
        default_factory=list
    )

    compliance_scores: dict = field(
        default_factory=dict
    )

    overall_score: int = 0