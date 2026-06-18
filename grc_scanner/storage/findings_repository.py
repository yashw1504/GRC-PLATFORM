from grc_scanner.storage.postgres_client import (
    PostgresClient
)


class FindingsRepository:

    @staticmethod
    def save_findings(
        scan_id,
        findings
    ):

        conn = (
            PostgresClient.get_connection()
        )

        cursor = conn.cursor()

        for finding in findings:

            cursor.execute(
                """
                INSERT INTO findings
                (
                    scan_id,
                    check_id,
                    name,
                    status,
                    severity,
                    risk_score,
                    priority,
                    category,
                    scanner_name,
                    evidence
                )
                VALUES
                (
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                )
                """,
                (
                    scan_id,
                    finding.check_id,
                    finding.name,
                    finding.status,
                    finding.severity,
                    finding.risk_score,
                    finding.priority,
                    finding.category,
                    finding.scanner_name,
                    finding.evidence
                )
            )

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def get_findings():

        conn = (
            PostgresClient.get_connection()
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                scan_id,
                name,
                severity,
                category,
                scanner_name,
                status,
                risk_score
            FROM findings
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        findings = []

        for row in rows:

            findings.append(
                {
                    "id": row[0],
                    "scan_id": row[1],
                    "name": row[2],
                    "severity": row[3],
                    "category": row[4],
                    "scanner": row[5],
                    "status": row[6],
                    "risk_score": row[7]
                }
            )

        return findings
    
    @staticmethod
    def get_findings_by_scan(
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
                name,
                severity,
                category,
                risk_score
            FROM findings
            WHERE scan_id=%s
            """,
            (scan_id,)
        )

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        results = []

        for row in rows:

            results.append(
                {
                    "id": row[0],
                    "name": row[1],
                    "severity": row[2],
                    "category": row[3],
                    "risk_score": row[4]
                }
            )

        return results