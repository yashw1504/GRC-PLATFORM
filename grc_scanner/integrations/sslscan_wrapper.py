import shutil
import subprocess


class SSLScanWrapper:

    @staticmethod
    def is_available():
        return shutil.which("sslscan") is not None

    @staticmethod
    def scan(target):

        if not SSLScanWrapper.is_available():
            return ""

        target = target.replace("https://", "")
        target = target.replace("http://", "")

        try:

            result = subprocess.run(
                [
                    "sslscan",
                    target
                ],
                capture_output=True,
                text=True
            )

            return result.stdout

        except Exception:
            return ""