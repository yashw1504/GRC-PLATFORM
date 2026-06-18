from grc_scanner.storage.postgres_client import (
    PostgresClient
)


class ComplianceRepository:

    @staticmethod
    def save_scores(
        scan_id,
        compliance_scores
    ):

        conn = (
            PostgresClient.get_connection()
        )

        cursor = conn.cursor()

        for framework, score in (
            compliance_scores.items()
        ):

            cursor.execute(
                """
                INSERT INTO compliance_scores
                (
                    scan_id,
                    framework,
                    score
                )
                VALUES
                (
                    %s,%s,%s
                )
                """,
                (
                    scan_id,
                    framework,
                    score
                )
            )

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def get_compliance_scores():

        conn = (
            PostgresClient.get_connection()
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                framework,
                score
            FROM compliance_scores
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        scores = []

        for row in rows:

            scores.append(
                {
                    "framework": row[0],
                    "score": row[1]
                }
            )

        return scores
    
    @staticmethod
    def get_scores_by_scan(
        scan_id
    ):

        conn = (
            PostgresClient.get_connection()
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                framework,
                score
            FROM compliance_scores
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
                    "framework": row[0],
                    "score": row[1]
                }
            )

        return results
    
    @staticmethod
    def get_scores_by_scan(
        scan_id
    ):

        conn = (
            PostgresClient.get_connection()
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                framework,
                score
            FROM compliance_scores
            WHERE scan_id=%s
            ORDER BY framework
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
                    "framework": row[0],
                    "score": row[1]
                }
            )

        return results
    
    @staticmethod
    def get_scores_by_scan(
        scan_id
    ):

        conn = (
            PostgresClient.get_connection()
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                framework,
                score
            FROM compliance_scores
            WHERE scan_id=%s
            ORDER BY framework
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
                    "framework": row[0],
                    "score": row[1]
                }
            )

        return results