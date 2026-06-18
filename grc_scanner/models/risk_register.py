from dataclasses import dataclass


@dataclass
class RiskRegister:

    risk_id: str

    title: str

    severity: str

    owner: str

    status: str

    remediation: str