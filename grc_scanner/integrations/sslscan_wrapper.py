import shutil
import subprocess


class SSLScanWrapper:

    @staticmethod
    def is_available():
        return shutil.which("sslscan") is not None

    @staticmethod
    def scan(host):

        if not SSLScanWrapper.is_available():
            return ""

        host = (
            host.replace("https://", "")
                .replace("http://", "")
                .split("/")[0]
        )

        try:

            result = subprocess.run(
                [
                    "sslscan",
                    host
                ],
                capture_output=True,
                text=True,
                timeout=180
            )

            return result.stdout

        except Exception as e:

            print("SSLScan Error:", e)
            return ""