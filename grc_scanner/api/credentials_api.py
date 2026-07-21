"""API endpoints for cloud credential management"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from grc_scanner.storage.credential_vault import CredentialVault

router = APIRouter(prefix="/credentials", tags=["credentials"])

class CredentialRequest(BaseModel):
    name: str
    provider: str  # aws, azure, gcp, dockerhub
    credentials: dict  # The actual keys/secrets

class CredentialResponse(BaseModel):
    id: int
    name: str
    provider: str

@router.post("/")
def store_credential(req: CredentialRequest):
    if req.provider not in ("aws", "azure", "gcp", "dockerhub"):
        raise HTTPException(status_code=400, detail="Invalid provider")
    cred_id = CredentialVault.store_credential(req.name, req.provider, req.credentials)
    return {"id": cred_id, "message": "Credential stored securely"}

@router.get("/")
def list_credentials():
    return CredentialVault.list_credentials()

@router.get("/{cred_id}")
def get_credential(cred_id: int):
    cred = CredentialVault.get_credential(cred_id)
    if not cred:
        raise HTTPException(status_code=404, detail="Credential not found")
    return cred

@router.delete("/{cred_id}")
def delete_credential(cred_id: int):
    CredentialVault.delete_credential(cred_id)
    return {"message": "Credential deleted"}

@router.post("/scan/{cred_id}")
def scan_with_credential(cred_id: int, scan_type: str = "aws"):
    """Run cloud scan using stored credential"""
    cred = CredentialVault.get_credential(cred_id)
    if not cred:
        raise HTTPException(status_code=404, detail="Credential not found")

    from grc_scanner.scanners.cloud_scanner import AWSCloudScanner, AzureCloudScanner, GCPCloudScanner
    scanners = {
        "aws": AWSCloudScanner(),
        "azure": AzureCloudScanner(),
        "gcp": GCPCloudScanner(),
    }

    scanner = scanners.get(cred["provider"])
    if not scanner:
        raise HTTPException(status_code=400, detail=f"No scanner for provider {cred['provider']}")

    findings = scanner.scan(cred_id=cred_id)
    return {
        "provider": cred["provider"],
        "credential_name": cred["name"],
        "findings_count": len(findings),
        "findings": [f.to_dict() for f in findings]
    }