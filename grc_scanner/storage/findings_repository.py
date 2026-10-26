import json

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
                    evidence,
                    cve_id,
                    cvss_score,
                    target_asset,
                    description,
                    mapped_controls,
                    remediation,
                    target_type,
                    business_impact,
                    recommendation,
                    owner,
                    estimated_effort,
                    change_request,
                    raw_data
                )
                VALUES
                (
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s
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
                    finding.evidence,
                    finding.cve_id,
                    finding.cvss_score,
                    finding.target_asset,
                    finding.description,
                    " | ".join(finding.mapped_controls or []),
                    finding.remediation,
                    finding.target_type,
                    finding.business_impact,
                    finding.recommendation,
                    finding.owner,
                    finding.estimated_effort,
                    finding.change_request,
                    json.dumps(finding.raw_data or {}, default=str)
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
                risk_score,
                check_id,
                priority,
                evidence,
                cve_id,
                cvss_score,
                target_asset
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
                    "risk_score": row[7],
                    "check_id": row[8],
                    "priority": row[9],
                    "evidence": row[10],
                    "cve_id": row[11],
                    "cvss_score": float(row[12]) if row[12] is not None else None,
                    "target_asset": row[13]
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
                risk_score,
                check_id,
                status,
                priority,
                scanner_name,
                evidence,
                cve_id,
                cvss_score,
                target_asset,
                description,
                remediation,
                mapped_controls,
                target_type,
                business_impact,
                recommendation,
                owner,
                estimated_effort,
                change_request,
                raw_data
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
                    "risk_score": row[4],
                    "check_id": row[5],
                    "status": row[6],
                    "priority": row[7],
                    "scanner": row[8],
                    "evidence": row[9],
                    "cve_id": row[10],
                    "cvss_score": float(row[11]) if row[11] is not None else None,
                    "target_asset": row[12],
                    "description": row[13],
                    "remediation": row[14],
                    "mapped_controls": row[15].split(" | ") if row[15] else [],
                    "target_type": row[16],
                    "business_impact": row[17],
                    "recommendation": row[18],
                    "owner": row[19],
                    "estimated_effort": row[20],
                    "change_request": row[21],
                    "raw_data": json.loads(row[22]) if row[22] else {}
                }
            )

        return results
