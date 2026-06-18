import json
import shutil
import subprocess


class GitleaksWrapper:

    @staticmethod
    def is_available():

        return shutil.which(
            "gitleaks"
        ) is not None

    @staticmethod
    def scan(path):

        if not GitleaksWrapper.is_available():
            return []

        try:

            result = subprocess.run(
                [
                    "gitleaks",
                    "detect",
                    "--source",
                    path,
                    "--report-format",
                    "json",
                    "--report-path",
                    "-"
                ],
                capture_output=True,
                text=True
            )

            if not result.stdout:
                return []

            return json.loads(
                result.stdout
            )

        except Exception:

            return []