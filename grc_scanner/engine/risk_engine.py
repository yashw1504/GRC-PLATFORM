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
    def _score(cls, finding):
        cvss = getattr(finding, "cvss_score", None)
        if cvss is None:
            return cls.calculate_finding_score(finding.severity)
        try:
            return round(max(0.0, min(float(cvss), 10.0)))
        except (TypeError, ValueError):
            return cls.calculate_finding_score(finding.severity)

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

        finding.risk_score = cls._score(finding)
        score = finding.risk_score
        try:
            cvss = float(finding.cvss_score) if finding.cvss_score is not None else score
        except (TypeError, ValueError):
            cvss = score
        finding.priority = (
            "P1 - Immediate" if cvss >= 9 else
            "P2 - High" if cvss >= 7 else
            "P3 - Medium" if cvss >= 4 else
            "P4 - Low" if cvss > 0 else
            "P5 - Informational"
        )

        return finding

    @classmethod
    def overall_score(cls, findings):
        """
        Calculate overall risk score
        """

        scored_findings = [
            finding for finding in findings
            if str(getattr(finding, "status", "")).lower() != "error"
        ]

        if not scored_findings:
            return 0

        total = sum(
            f.risk_score
            for f in scored_findings
        )

        avg = total / len(scored_findings)

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
