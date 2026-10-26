import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()


class PostgresClient:

    @staticmethod
    def get_connection():

        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            sslmode="require"
        )

    @staticmethod
    def initialize():
        """Create the application schema and apply additive column migrations."""
        statements = (
            """CREATE TABLE IF NOT EXISTS scans (
                id SERIAL PRIMARY KEY, target TEXT, overall_score INTEGER,
                scan_type VARCHAR(100), scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS findings (
                id SERIAL PRIMARY KEY,
                scan_id INTEGER REFERENCES scans(id) ON DELETE CASCADE,
                check_id TEXT, name TEXT, status TEXT, severity TEXT,
                risk_score INTEGER, priority TEXT, category TEXT,
                scanner_name TEXT, evidence TEXT, cve_id TEXT,
                cvss_score NUMERIC(3,1), target_asset TEXT, description TEXT,
                mapped_controls TEXT, remediation TEXT, target_type TEXT,
                business_impact TEXT, recommendation TEXT, owner TEXT,
                estimated_effort TEXT, change_request TEXT, raw_data TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS compliance_scores (
                id SERIAL PRIMARY KEY,
                scan_id INTEGER REFERENCES scans(id) ON DELETE CASCADE,
                framework TEXT, score INTEGER
            )""",
            """CREATE TABLE IF NOT EXISTS reports (
                id SERIAL PRIMARY KEY,
                scan_id INTEGER REFERENCES scans(id) ON DELETE CASCADE,
                report_type TEXT, report_path TEXT
            )""",
            "ALTER TABLE findings ADD COLUMN IF NOT EXISTS cve_id TEXT",
            "ALTER TABLE findings ADD COLUMN IF NOT EXISTS cvss_score NUMERIC(3,1)",
            "ALTER TABLE findings ADD COLUMN IF NOT EXISTS target_asset TEXT",
            "ALTER TABLE findings ADD COLUMN IF NOT EXISTS description TEXT",
            "ALTER TABLE findings ADD COLUMN IF NOT EXISTS mapped_controls TEXT",
            "ALTER TABLE findings ADD COLUMN IF NOT EXISTS remediation TEXT",
            "ALTER TABLE findings ADD COLUMN IF NOT EXISTS target_type TEXT",
            "ALTER TABLE findings ADD COLUMN IF NOT EXISTS business_impact TEXT",
            "ALTER TABLE findings ADD COLUMN IF NOT EXISTS recommendation TEXT",
            "ALTER TABLE findings ADD COLUMN IF NOT EXISTS owner TEXT",
            "ALTER TABLE findings ADD COLUMN IF NOT EXISTS estimated_effort TEXT",
            "ALTER TABLE findings ADD COLUMN IF NOT EXISTS change_request TEXT",
            "ALTER TABLE findings ADD COLUMN IF NOT EXISTS raw_data TEXT",
        )
        connection = PostgresClient.get_connection()
        try:
            with connection.cursor() as cursor:
                for statement in statements:
                    cursor.execute(statement)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
