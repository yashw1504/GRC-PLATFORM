from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from grc_scanner.database.database import get_db
from grc_scanner.database.schemas import CredentialCreate
from grc_scanner.database.schemas import CredentialUpdate
from grc_scanner.database.schemas import CredentialResponse

from grc_scanner.services.credential_service import CredentialService

router = APIRouter(
    prefix="/credentials",
    tags=["Credentials"]
)


# -----------------------------------------
# Create Credential
# -----------------------------------------

@router.post(
    "",
    response_model=CredentialResponse
)
def create_credential(
    credential: CredentialCreate,
    db: Session = Depends(get_db)
):

    return CredentialService.create(
        db,
        credential
    )


# -----------------------------------------
# List Credentials
# -----------------------------------------

@router.get(
    "",
    response_model=list[CredentialResponse]
)
def list_credentials(
    db: Session = Depends(get_db)
):

    return CredentialService.list(db)


# -----------------------------------------
# Get Credential
# -----------------------------------------

@router.get(
    "/{credential_id}",
    response_model=CredentialResponse
)
def get_credential(
    credential_id: int,
    db: Session = Depends(get_db)
):

    credential = CredentialService.get(
        db,
        credential_id
    )

    if credential is None:

        raise HTTPException(
            status_code=404,
            detail="Credential not found"
        )

    return credential


# -----------------------------------------
# Update Credential
# -----------------------------------------

@router.put(
    "/{credential_id}",
    response_model=CredentialResponse
)
def update_credential(
    credential_id: int,
    request: CredentialUpdate,
    db: Session = Depends(get_db)
):

    db_credential = CredentialService.get(
        db,
        credential_id
    )

    if db_credential is None:

        raise HTTPException(
            status_code=404,
            detail="Credential not found"
        )

    return CredentialService.update(
        db,
        db_credential,
        request
    )


# -----------------------------------------
# Delete Credential
# -----------------------------------------

@router.delete(
    "/{credential_id}"
)
def delete_credential(
    credential_id: int,
    db: Session = Depends(get_db)
):

    db_credential = CredentialService.get(
        db,
        credential_id
    )

    if db_credential is None:

        raise HTTPException(
            status_code=404,
            detail="Credential not found"
        )

    CredentialService.delete(
        db,
        db_credential
    )

    return {

        "message": "Credential deleted successfully"

    }