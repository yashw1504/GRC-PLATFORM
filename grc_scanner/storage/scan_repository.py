from grc_scanner.storage.postgres_client import PostgresClient

class ScanRepository:
    @staticmethod
    def create_scan(target, overall_score, scan_type):
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO scans (target, overall_score, scan_type) VALUES (%s, %s, %s) RETURNING id",
            (target, overall_score, scan_type)
        )
        scan_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return scan_id

    @staticmethod
    def get_scans():
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, target, overall_score, scan_type, scan_date FROM scans ORDER BY scan_date DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            {"id": r[0], "target": r[1], "overall_score": r[2], "scan_type": r[3], "scan_date": str(r[4])}
            for r in rows
        ]

    @staticmethod
    def get_scan(scan_id):
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, target, overall_score, scan_type, scan_date FROM scans WHERE id = %s", (scan_id,))
        r = cursor.fetchone()
        cursor.close()
        conn.close()
        if r:
            return {"id": r[0], "target": r[1], "overall_score": r[2], "scan_type": r[3], "scan_date": str(r[4])}
        return None