import json
from grc_scanner.storage.postgres_client import PostgresClient
from grc_scanner.engine.finding import Finding

class FindingsRepository:
    @staticmethod
    def save_findings(scan_id, findings):
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        for f in findings:
            cursor.execute("""
                INSERT INTO findings (scan_id, check_id, name, status, severity, risk_score, priority,
                    description, evidence, category, target_type, target_asset, scanner_name,
                    remediation, recommendation, business_impact, mapped_controls, raw_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                scan_id, f.check_id, f.name, f.status, f.severity, f.risk_score, f.priority,
                f.description, f.evidence, f.category, f.target_type, f.target_asset, f.scanner_name,
                f.remediation, f.recommendation, f.business_impact,
                f.mapped_controls, json.dumps(f.raw_data) if f.raw_data else None
            ))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_findings():
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, scan_id, check_id, name, severity, category, scanner_name, risk_score, target_asset FROM findings ORDER BY risk_score DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [{"id": r[0], "scan_id": r[1], "check_id": r[2], "name": r[3], "severity": r[4],
                 "category": r[5], "scanner": r[6], "risk_score": r[7], "target": r[8]} for r in rows]

    @staticmethod
    def get_findings_by_scan(scan_id):
        conn = PostgresClient.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, check_id, name, severity, risk_score, priority, description, evidence, category, scanner_name, remediation FROM findings WHERE scan_id = %s ORDER BY risk_score DESC", (scan_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [{"id": r[0], "check_id": r[1], "name": r[2], "severity": r[3], "risk_score": r[4],
                 "priority": r[5], "description": r[6], "evidence": r[7], "category": r[8],
                 "scanner": r[9], "remediation": r[10]} for r in rows]