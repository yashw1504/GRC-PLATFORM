from grc_scanner.storage.postgres_client import PostgresClient

class DashboardRepository:
    @staticmethod
    def get_summary():
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM scans")
        total_scans = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM findings")
        total_findings = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM findings WHERE severity='Critical'")
        critical = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM findings WHERE severity='High'")
        high = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(AVG(overall_score), 0) FROM scans")
        avg_score = round(cursor.fetchone()[0], 1)

        cursor.close()
        conn.close()

        return {
            "total_scans": total_scans,
            "total_findings": total_findings,
            "critical": critical,
            "high": high,
            "average_risk_score": avg_score
        }