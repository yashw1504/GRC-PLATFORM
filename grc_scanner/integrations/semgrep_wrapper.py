import json
import shutil
import subprocess


class SemgrepWrapper:

    @staticmethod
    def is_available():
        return shutil.which("semgrep") is not None

    @staticmethod
    def scan(path):

        if not SemgrepWrapper.is_available():
            return []

        cmd = [
            "semgrep",
            "--config=auto",
            "--json",
            path
        ]

        try:

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )

            data = json.loads(result.stdout)

            return data.get("results", [])

        except Exception as e:
            print("Semgrep Error:", e)
            return []