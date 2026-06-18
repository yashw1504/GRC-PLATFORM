from grc_scanner.storage.postgres_client import (
    PostgresClient
)


class ScanRepository:

    @staticmethod
    def create_scan(
        target,
        overall_score,
        scan_type
    ):

        conn = (
            PostgresClient.get_connection()
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO scans
            (
                target,
                overall_score,
                scan_type
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            RETURNING id
            """,
            (
                target,
                overall_score,
                scan_type
            )
        )

        scan_id = cursor.fetchone()[0]

        conn.commit()

        cursor.close()

        conn.close()

        return scan_id

    @staticmethod
    def get_scans():

        conn = (
            PostgresClient.get_connection()
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                target,
                overall_score,
                scan_date,
                scan_type
            FROM scans
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        scans = []

        for row in rows:

            scans.append(
                {
                    "id": row[0],
                    "target": row[1],
                    "overall_score": row[2],
                    "scan_date": str(row[3]),
                    "scan_type": row[4]
                }
            )

        return scans

    @staticmethod
    def get_scan(scan_id):

        conn = (
            PostgresClient.get_connection()
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                target,
                overall_score,
                scan_date,
                scan_type
            FROM scans
            WHERE id=%s
            """,
            (scan_id,)
        )

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            return None

        return {
            "id": row[0],
            "target": row[1],
            "overall_score": row[2],
            "scan_date": str(row[3]),
            "scan_type": row[4]
        }