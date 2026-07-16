from dataclasses import dataclass
from typing import Optional
from typing import Dict


@dataclass
class VerificationResult:

    success: bool

    provider: str

    message: str

    details: Optional[Dict] = None