import json

from sqlalchemy.orm import Session

from grc_scanner.database import crud
from grc_scanner.database.models import Credential
from grc_scanner.database.schemas import CredentialCreate
from grc_scanner.database.schemas import CredentialUpdate

from grc_scanner.security.encryption import encrypt
from grc_scanner.security.encryption import decrypt


class CredentialService:

    @staticmethod
    def create(
        db: Session,
        credential: CredentialCreate
    ):

        encrypted_data = encrypt(
            credential.credential_data
        )

        return crud.create_credential(
            db=db,
            encrypted_data=encrypted_data,
            credential=credential
        )

    @staticmethod
    def list(
        db: Session
    ):

        return crud.get_credentials(db)

    @staticmethod
    def get(
        db: Session,
        credential_id: int
    ):

        return crud.get_credential(
            db,
            credential_id
        )

    @staticmethod
    def update(
        db: Session,
        db_credential: Credential,
        credential: CredentialUpdate
    ):

        encrypted = None

        if credential.credential_data:

            encrypted = encrypt(
                credential.credential_data
            )

        return crud.update_credential(
            db=db,
            db_credential=db_credential,
            credential=credential,
            encrypted_data=encrypted
        )

    @staticmethod
    def delete(
        db: Session,
        db_credential: Credential
    ):

        crud.delete_credential(
            db,
            db_credential
        )

    @staticmethod
    def decrypt_credential(
        db_credential: Credential
    ):

        return decrypt(
            db_credential.encrypted_data
        )