import json
import shutil
import subprocess


class SyftWrapper:

    @staticmethod
    def is_available():
        return shutil.which("syft") is not None

    @staticmethod
    def scan(path="."):

        if not SyftWrapper.is_available():
            return {}

        cmd = [
            "syft",
            path,
            "-o",
            "cyclonedx-json"
        ]

        try:

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )

            if result.returncode != 0:
                print(result.stderr)
                return {}

            return json.loads(result.stdout)

        except Exception as e:
            print("Syft Error:", e)
            return {}