class RiskEngine:
    """
    Risk scoring engine
    """

    SCORE_MAP = {
        "Critical": 10,
        "High": 8,
        "Medium": 5,
        "Low": 2,
        "Info": 0
    }

    @classmethod
    def calculate_finding_score(cls, severity):
        return cls.SCORE_MAP.get(severity, 0)

    @classmethod
    def calculate_priority(cls, severity):
        score = cls.calculate_finding_score(severity)

        if score >= 10:
            return "P1 - Immediate"

        if score >= 8:
            return "P2 - High"

        if score >= 5:
            return "P3 - Medium"

        if score >= 2:
            return "P4 - Low"

        return "P5 - Informational"

    @classmethod
    def enrich_finding(cls, finding):
        """
        Add risk score and priority
        """

        finding.risk_score = cls.calculate_finding_score(
            finding.severity
        )

        finding.priority = cls.calculate_priority(
            finding.severity
        )

        return finding

    @classmethod
    def overall_score(cls, findings):
        """
        Calculate overall risk score
        """

        if not findings:
            return 0

        total = sum(
            f.risk_score
            for f in findings
        )

        avg = total / len(findings)

        return min(
            round(avg * 10),
            100
        )

    @classmethod
    def risk_rating(cls, score):

        if score >= 80:
            return "Critical"

        if score >= 60:
            return "High"

        if score >= 40:
            return "Medium"

        if score >= 20:
            return "Low"

        return "Informational"