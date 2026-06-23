from grc_scanner.storage.postgres_client import (
    PostgresClient
)


class ReportRepository:

    @staticmethod
    def save_report(
        scan_id,
        report_type,
        report_path
    ):

        conn = (
            PostgresClient.get_connection()
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO reports
            (
                scan_id,
                report_type,
                report_path
            )
            VALUES
            (
                %s,%s,%s
            )
            """,
            (
                scan_id,
                report_type,
                report_path
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def get_reports_by_scan(
        scan_id
    ):

        conn = (
            PostgresClient.get_connection()
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                report_type,
                report_path
            FROM reports
            WHERE scan_id=%s
            """,
            (scan_id,)
        )

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        reports = []

        for row in rows:

            reports.append(
                {
                    "id": row[0],
                    "type": row[1],
                    "path": row[2]
                }
            )

        return reports
    
    @staticmethod
    def get_report_by_id(
        report_id
    ):

        conn = (
            PostgresClient.get_connection()
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                report_type,
                report_path
            FROM reports
            WHERE id=%s
            """,
            (report_id,)
        )

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            return None

        return {
            "id": row[0],
            "type": row[1],
            "path": row[2]
        }