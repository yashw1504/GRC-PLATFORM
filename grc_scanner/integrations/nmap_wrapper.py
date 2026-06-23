import shutil
import subprocess


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

        try:

            result = subprocess.run(
                [
                    "nmap",
                    "-sV",
                    target
                ],
                capture_output=True,
                text=True
            )

            return result.stdout

        except Exception:
            return ""