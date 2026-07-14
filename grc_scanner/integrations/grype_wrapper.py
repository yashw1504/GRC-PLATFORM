import json
import shutil
import subprocess


class GrypeWrapper:

    @staticmethod
    def is_available():
        return shutil.which("grype") is not None

    @staticmethod
    def scan(sbom_file):

        if not GrypeWrapper.is_available():
            return {}

        try:

            result = subprocess.run(
                [
                    "grype",
                    f"sbom:{sbom_file}",
                    "-o",
                    "json"
                ],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return {}

            if not result.stdout:
                return {}

            return json.loads(result.stdout)

        except Exception:
            return {}