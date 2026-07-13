#!/bin/bash

set -e

echo "=================================="
echo "Verifying Security Tools"
echo "=================================="

python --version

nmap --version

sslscan --version

semgrep --version

checkov --version

nuclei -version

syft version

grype version

trivy --version

gitleaks version

echo "=================================="
echo "All Security Tools Installed"
echo "=================================="