#!/bin/bash
set -e

echo "=================================="
echo "Installing Security Tools"
echo "=================================="

source /tmp/tool_versions.env

apt-get update

DEBIAN_FRONTEND=noninteractive apt-get install -y \
    wget \
    curl \
    unzip \
    tar \
    git \
    ca-certificates \
    python3-pip \
    nmap \
    sslscan \
    netcat-openbsd

rm -rf /var/lib/apt/lists/*

# Nuclei
echo "Installing Nuclei ${NUCLEI_VERSION}"
wget -q https://github.com/projectdiscovery/nuclei/releases/download/v${NUCLEI_VERSION}/nuclei_${NUCLEI_VERSION}_linux_amd64.zip
unzip -q nuclei_${NUCLEI_VERSION}_linux_amd64.zip
mv nuclei /usr/local/bin/
chmod +x /usr/local/bin/nuclei
rm nuclei_${NUCLEI_VERSION}_linux_amd64.zip

# Semgrep
echo "Installing Semgrep ${SEMGREP_VERSION}"
pip3 install --no-cache-dir semgrep==${SEMGREP_VERSION}

# Checkov
echo "Installing Checkov ${CHECKOV_VERSION}"
pip3 install --no-cache-dir checkov==${CHECKOV_VERSION}

# Trivy (single install - removed duplicate)
echo "Installing Trivy ${TRIVY_VERSION}"
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin v${TRIVY_VERSION}

# Syft
echo "Installing Syft ${SYFT_VERSION}"
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin v${SYFT_VERSION}

# Grype
echo "Installing Grype ${GRYPE_VERSION}"
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin v${GRYPE_VERSION}

# Gitleaks
echo "Installing Gitleaks ${GITLEAKS_VERSION}"
wget -q https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz
tar -xzf gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz
mv gitleaks /usr/local/bin/
chmod +x /usr/local/bin/gitleaks
rm gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz

# OSV Scanner
echo "Installing OSV Scanner ${OSV_SCANNER_VERSION}"
wget -q https://github.com/google/osv-scanner/releases/download/v${OSV_SCANNER_VERSION}/osv-scanner_linux_amd64
mv osv-scanner_linux_amd64 /usr/local/bin/osv-scanner
chmod +x /usr/local/bin/osv-scanner

# Update Nuclei Templates
echo "Updating Nuclei Templates"
nuclei -update-templates || true

# Verify
echo
echo "Installed Versions"
echo "------------------"
nuclei -version || true
semgrep --version || true
checkov --version || true
syft version || true
grype version || true
trivy --version || true
gitleaks version || true
osv-scanner --version || true

echo
echo "=================================="
echo "Security Tools Installed Successfully"
echo "=================================="