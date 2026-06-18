import json
import shutil
import subprocess


class KubescapeWrapper:

    @staticmethod
    def is_available():
        return shutil.which("kubescape") is not None

    @staticmethod
    def scan(path="."):

        if not KubescapeWrapper.is_available():
            return {}

        try:

            result = subprocess.run(
                [
                    "kubescape",
                    "scan",
                    path,
                    "--format",
                    "json"
                ],
                capture_output=True,
                text=True
            )

            if not result.stdout:
                return {}

            return json.loads(result.stdout)

        except Exception:
            return {}