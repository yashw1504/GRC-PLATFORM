import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class PostgresClient:
    @staticmethod
    def get_connection():
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "grc_platform"),
            user=os.getenv("DB_USER", "grc_user"),
            password=os.getenv("DB_PASSWORD", "grc_secure_password"),
            sslmode=os.getenv("DB_SSLMODE", "prefer"),
        )
