import json

from cryptography.fernet import Fernet

from grc_scanner.core.config import settings


if not settings.ENCRYPTION_KEY:
    raise RuntimeError(
        "ENCRYPTION_KEY is missing. Please configure it in your .env file."
    )


cipher = Fernet(
    settings.ENCRYPTION_KEY.encode()
)


def encrypt(data: dict) -> str:
    """
    Encrypt dictionary before storing in database.
    """

    json_data = json.dumps(data)

    encrypted = cipher.encrypt(
        json_data.encode()
    )

    return encrypted.decode()


def decrypt(data: str) -> dict:
    """
    Decrypt credential data from database.
    """

    decrypted = cipher.decrypt(
        data.encode()
    )

    return json.loads(
        decrypted.decode()
    )