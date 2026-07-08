import json
import shutil
import subprocess


class NucleiWrapper:

    @staticmethod
    def is_available():
        return shutil.which("nuclei") is not None

    @staticmethod
    def scan(target, extra_args=None):

        if not NucleiWrapper.is_available():
            return []

        cmd = [
            "nuclei",
            "-u",
            target,
            "-json",
            "-silent",
            "-duc",
            "-rl", "20"
        ]

        if extra_args:
            cmd.extend(extra_args)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode != 0:
                print("Nuclei stderr:")
                print(result.stderr)

            findings = []

            for line in result.stdout.splitlines():
                try:
                    findings.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

            return findings

        except Exception as e:
            print(f"Nuclei Error: {e}")
            return []