import hashlib

from grc_scanner.engine.finding import Finding


class FindingDeduplicator:

    @staticmethod
    def deduplicate(findings):

        unique = {}
        merged = []

        for finding in findings:
            raw = finding.raw_data or {}
            cve = finding.cve_id or raw.get("cve") or raw.get("cve_id") or raw.get("vulnerability_id")
            target = (finding.target_asset or "").strip().lower()
            if cve:
                key = ("cve", str(cve).strip().upper(), target)
            else:
                evidence = " ".join((finding.evidence or "").lower().split())
                evidence_hash = hashlib.sha256(evidence.encode("utf-8")).hexdigest()
                key = ("evidence", target, finding.check_id, evidence_hash)

            existing = unique.get(key)
            if existing is None:
                unique[key] = finding
                merged.append(finding)
                continue

            # Keep the most useful record while retaining which scanners found it.
            if finding.risk_score > existing.risk_score:
                existing.severity = finding.severity
                existing.risk_score = finding.risk_score
                existing.priority = finding.priority
            scanners = set(filter(None, (existing.scanner_name, finding.scanner_name)))
            existing.scanner_name = ", ".join(sorted(scanners))
            if not existing.evidence and finding.evidence:
                existing.evidence = finding.evidence

        return merged
