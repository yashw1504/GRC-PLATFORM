from grc_scanner.storage.postgres_client import PostgresClient

class ComplianceRepository:
    @staticmethod
    def save_scores(scan_id, scores):
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        for framework, score in scores.items():
            cursor.execute(
                "INSERT INTO compliance_scores (scan_id, framework, score) VALUES (%s, %s, %s)",
                (scan_id, framework, score)
            )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_compliance_scores():
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cs.framework, cs.score, s.target, s.scan_date
            FROM compliance_scores cs
            JOIN scans s ON cs.scan_id = s.id
            ORDER BY cs.scan_id DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [{"framework": r[0], "score": r[1], "target": r[2], "scan_date": str(r[3])} for r in rows]

    @staticmethod
    def get_scores_by_scan(scan_id):
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT framework, score FROM compliance_scores WHERE scan_id = %s", (scan_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [{"framework": r[0], "score": r[1]} for r in rows]