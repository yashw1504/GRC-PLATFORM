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
            return {}

        try:

            result = subprocess.run(
                [
                    "semgrep",
                    "--config",
                    "auto",
                    path,
                    "--json"
                ],
                capture_output=True,
                text=True
            )

            if not result.stdout:
                return {}

            return json.loads(result.stdout)

        except Exception:
            return {}