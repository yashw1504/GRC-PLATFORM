from datetime import datetime
from typing import Optional
from typing import Dict
from typing import Any

from pydantic import BaseModel


# -------------------------
# Create Credential
# -------------------------

class CredentialCreate(BaseModel):

    name: str

    provider: str

    credential_type: str

    description: Optional[str] = None

    credential_data: Dict[str, Any]


# -------------------------
# Update Credential
# -------------------------

class CredentialUpdate(BaseModel):

    name: Optional[str] = None

    description: Optional[str] = None

    credential_data: Optional[Dict[str, Any]] = None


# -------------------------
# Verify Credential
# -------------------------

class CredentialVerifyRequest(BaseModel):

    credential_data: Dict[str, Any]


# -------------------------
# API Response
# -------------------------

class CredentialResponse(BaseModel):

    id: int

    name: str

    provider: str

    credential_type: str

    description: Optional[str]

    status: str

    verified: bool

    created_at: datetime

    updated_at: datetime

    last_verified: Optional[datetime]

    class Config:

        from_attributes = True