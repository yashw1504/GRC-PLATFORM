import json
import shutil
import subprocess


class KubeBenchWrapper:

    @staticmethod
    def is_available():
        return shutil.which("kube-bench") is not None

    @staticmethod
    def scan():

        if not KubeBenchWrapper.is_available():
            return {}

        try:

            result = subprocess.run(
                [
                    "kube-bench",
                    "--json"
                ],
                capture_output=True,
                text=True,
                timeout=600
            )

            if not result.stdout:
                return {}

            return json.loads(
                result.stdout
            )

        except subprocess.TimeoutExpired:
            return []
        except Exception:
            return {}
