"""Secure storage for cloud credentials using encryption"""
import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from grc_scanner.storage.postgres_client import PostgresClient

class CredentialVault:
    """Encrypted credential storage for cloud providers"""

    @staticmethod
    def _get_encryption_key():
        """Derive encryption key from app secret"""
        password = os.getenv("VAULT_KEY", "change-this-to-a-secure-random-string").encode()
        salt = b"grc_platform_salt_32bytes"  # In production, use a random salt stored separately
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
        return base64.urlsafe_b64encode(kdf.derive(password))

    @staticmethod
    def _encrypt(data: dict) -> str:
        key = CredentialVault._get_encryption_key()
        f = Fernet(key)
        return f.encrypt(json.dumps(data).encode()).decode()

    @staticmethod
    def _decrypt(encrypted_data: str) -> dict:
        key = CredentialVault._get_encryption_key()
        f = Fernet(key)
        return json.loads(f.decrypt(encrypted_data.encode()).decode())

    @staticmethod
    def store_credential(name: str, provider: str, credentials: dict):
        """Store encrypted credentials"""
        encrypted = CredentialVault._encrypt(credentials)
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cloud_credentials (name, provider, encrypted_data) VALUES (%s, %s, %s) RETURNING id",
            (name, provider, encrypted)
        )
        cred_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return cred_id

    @staticmethod
    def get_credential(cred_id: int) -> dict:
        """Retrieve and decrypt credentials"""
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, provider, encrypted_data FROM cloud_credentials WHERE id = %s", (cred_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            return None
        return {
            "id": cred_id,
            "name": row[0],
            "provider": row[1],
            "credentials": CredentialVault._decrypt(row[2])
        }

    @staticmethod
    def list_credentials():
        """List credential names (without exposing secrets)"""
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, provider, created_at FROM cloud_credentials ORDER BY created_at DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [{"id": r[0], "name": r[1], "provider": r[2], "created_at": str(r[3])} for r in rows]

    @staticmethod
    def delete_credential(cred_id: int):
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cloud_credentials WHERE id = %s", (cred_id,))
        conn.commit()
        cursor.close()
        conn.close()