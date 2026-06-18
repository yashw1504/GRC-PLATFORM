from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Finding:
    """
    Standard finding object used by all scanners
    """

    # Basic Information
    check_id: str
    name: str

    # Result
    status: str
    severity: str

    # Risk Management
    risk_score: int = 0
    priority: str = "P5 - Informational"

    # Finding Details
    description: str = ""
    evidence: str = ""

    # Compliance
    mapped_controls: List[str] = field(default_factory=list)

    # Business Context
    business_impact: str = ""
    remediation: str = ""
    recommendation: str = ""

    # Categorization
    category: str = ""

    # Asset Metadata
    target_type: str = ""
    target_asset: str = ""

    # Scanner Metadata
    scanner_name: str = ""

    # Change Management
    owner: str = ""
    estimated_effort: str = ""
    change_request: str = ""

    # Raw Scanner Data
    raw_data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "check_id": self.check_id,
            "name": self.name,
            "status": self.status,
            "severity": self.severity,
            "risk_score": self.risk_score,
            "priority": self.priority,
            "description": self.description,
            "evidence": self.evidence,
            "mapped_controls": self.mapped_controls,
            "business_impact": self.business_impact,
            "remediation": self.remediation,
            "recommendation": self.recommendation,
            "category": self.category,
            "target_type": self.target_type,
            "target_asset": self.target_asset,
            "scanner_name": self.scanner_name,
            "owner": self.owner,
            "estimated_effort": self.estimated_effort,
            "change_request": self.change_request,
            "raw_data": self.raw_data
        }