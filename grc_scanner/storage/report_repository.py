from grc_scanner.storage.postgres_client import PostgresClient

class ReportRepository:
    @staticmethod
    def save_report(scan_id, report_type, path):
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reports (scan_id, type, path) VALUES (%s, %s, %s)",
            (scan_id, report_type, path)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_reports_by_scan(scan_id):
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, type, path FROM reports WHERE scan_id = %s", (scan_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [{"id": r[0], "type": r[1], "path": r[2]} for r in rows]

    @staticmethod
    def get_report_by_id(report_id):
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, scan_id, type, path FROM reports WHERE id = %s", (report_id,))
        r = cursor.fetchone()
        cursor.close()
        conn.close()
        if r:
            return {"id": r[0], "scan_id": r[1], "type": r[2], "path": r[3]}
        return None