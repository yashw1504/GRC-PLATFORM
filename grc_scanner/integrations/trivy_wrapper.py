import json
import shutil
import subprocess


class TrivyWrapper:

    @staticmethod
    def is_available():

        return shutil.which(
            "trivy"
        ) is not None

    @staticmethod
    def scan(path="."):

        if not TrivyWrapper.is_available():
            return {}

        try:

            result = subprocess.run(
                [
                    "trivy",
                    "fs",
                    path,
                    "--format",
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