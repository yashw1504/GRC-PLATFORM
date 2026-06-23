import json
import shutil
import subprocess


class SemgrepWrapper:

    @staticmethod
    def is_available():
        return shutil.which("semgrep") is not None

    @staticmethod
    def scan(path="."):
        if not SemgrepWrapper.is_available():
            return []

        result = subprocess.run(
            [
                "semgrep",
                "scan",
                "--json",
                path
            ],
            capture_output=True,
            text=True
        )

        if not result.stdout:
            return []

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            return []

        findings = []

        for item in data.get("results", []):
            findings.append(
                {
                    "check_id": item.get("check_id"),
                    "name": item.get("check_id"),
                    "message": item.get("extra", {}).get("message", ""),
                    "path": item.get("path"),
                    "severity": item.get("extra", {}).get("severity", "Medium")
                }
            )

        return findings