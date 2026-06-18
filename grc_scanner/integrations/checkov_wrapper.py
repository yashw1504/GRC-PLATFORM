import json
import shutil
import subprocess


class CheckovWrapper:

    @staticmethod
    def is_available():
        return shutil.which("checkov") is not None

    @staticmethod
    def scan(path="."):

        if not CheckovWrapper.is_available():
            return {}

        try:

            result = subprocess.run(
                [
                    "checkov",
                    "-d",
                    path,
                    "-o",
                    "json"
                ],
                capture_output=True,
                text=True
            )

            if not result.stdout:
                return {}

            return json.loads(
                result.stdout
            )

        except Exception:
            return {}