import json
import shutil
import subprocess


class NucleiWrapper:

    @staticmethod
    def is_available():
        return shutil.which("nuclei") is not None

    @staticmethod
    def scan(target):

        if not NucleiWrapper.is_available():
            return []

        try:

            result = subprocess.run(
                [
                    "nuclei",
                    "-u",
                    target,
                    "-json"
                ],
                capture_output=True,
                text=True
            )

            findings = []

            for line in result.stdout.splitlines():

                try:
                    findings.append(
                        json.loads(line)
                    )
                except Exception:
                    pass

            return findings

        except Exception:
            return []