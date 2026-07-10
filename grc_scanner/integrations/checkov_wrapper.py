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
            return []

        cmd = [
            "checkov",
            "-d",
            path,
            "-o",
            "json"
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )

            if not result.stdout.strip():
                return []

            data = json.loads(result.stdout)

            # Checkov may return a dict or a list
            if isinstance(data, dict):
                return [data]

            if isinstance(data, list):
                return data

            return []

        except Exception as e:
            print(f"Checkov Error: {e}")
            return []