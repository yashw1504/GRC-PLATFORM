import shutil
import subprocess
from urllib.parse import urlparse


class NmapWrapper:

    @staticmethod
    def is_available():

        return shutil.which(
            "nmap"
        ) is not None

    @staticmethod
    def scan(target):

        if not NmapWrapper.is_available():
            return ""

        parsed = urlparse(target if "://" in target else f"//{target}")
        host = parsed.hostname or target.split("/")[0]

        try:

            result = subprocess.run(
                [
                    "nmap",
                    "-sV",
                    "-F",
                    host
                ],
                capture_output=True,
                text=True
            )

            return result.stdout

        except Exception:
            return ""
