#!/bin/bash

echo "=================================="
echo "Verifying Security Tools"
echo "=================================="

verify() {
    echo
    echo "Checking: $1"
    if eval "$2"; then
        echo "✅ $1 OK"
    else
        echo "❌ $1 FAILED"
    fi
}

verify "Python" "python3 --version"
verify "Nmap" "nmap --version"
verify "SSLScan" "sslscan --version"
verify "Semgrep" "semgrep --version"
verify "Checkov" "checkov --version"
verify "Nuclei" "nuclei -version"
verify "Syft" "syft version"
verify "Grype" "grype version"
verify "Trivy" "trivy --version"
verify "Gitleaks" "gitleaks version"
verify "OSV Scanner" "osv-scanner --version"

echo
echo "=================================="
echo "Verification Complete"
echo "=================================="
