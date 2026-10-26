#!/bin/bash
set -e

echo "=================================="
echo "Installing Security Tools"
echo "=================================="

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# -------------------------------
# Load tool versions
# -------------------------------
source /tmp/tool_versions.env

# -------------------------------
# Install OS packages
# -------------------------------
apt-get update

DEBIAN_FRONTEND=noninteractive apt-get install -y \
    wget \
    curl \
    unzip \
    tar \
    git \
    ca-certificates \
    python3-pip

rm -rf /var/lib/apt/lists/*

# -------------------------------
# Nuclei
# -------------------------------
if command_exists nuclei; then
    echo "Nuclei already installed; skipping"
else
echo "Installing Nuclei ${NUCLEI_VERSION}"

wget -q \
https://github.com/projectdiscovery/nuclei/releases/download/v${NUCLEI_VERSION}/nuclei_${NUCLEI_VERSION}_linux_amd64.zip

unzip -q nuclei_${NUCLEI_VERSION}_linux_amd64.zip

mv nuclei /usr/local/bin/

chmod +x /usr/local/bin/nuclei

rm nuclei_${NUCLEI_VERSION}_linux_amd64.zip
fi

# -------------------------------
# Semgrep
# -------------------------------
if command_exists semgrep; then
    echo "Semgrep already installed; skipping"
else
echo "Installing Semgrep"

pip3 install --no-cache-dir \
semgrep==${SEMGREP_VERSION}
fi

# -------------------------------
# Checkov
# -------------------------------
if command_exists checkov; then
    echo "Checkov already installed; skipping"
else
echo "Installing Checkov"

pip3 install --no-cache-dir \
checkov==${CHECKOV_VERSION}
fi

####################################
# Trivy
####################################


####################################
# Trivy
####################################

if command_exists trivy; then
    echo "Trivy already installed; skipping"
else
echo "Installing Trivy ${TRIVY_VERSION}"
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin v${TRIVY_VERSION}
fi
# -------------------------------
# Syft
# -------------------------------
if command_exists syft; then
    echo "Syft already installed; skipping"
else
echo "Installing Syft ${SYFT_VERSION}"

curl -sSfL \
https://raw.githubusercontent.com/anchore/syft/main/install.sh \
| sh -s -- \
-b /usr/local/bin \
v${SYFT_VERSION}
fi

# -------------------------------
# Grype
# -------------------------------
if command_exists grype; then
    echo "Grype already installed; skipping"
else
echo "Installing Grype ${GRYPE_VERSION}"

curl -sSfL \
https://raw.githubusercontent.com/anchore/grype/main/install.sh \
| sh -s -- \
-b /usr/local/bin \
v${GRYPE_VERSION}
fi

####################################
# Trivy
####################################

# -------------------------------
# Gitleaks
# -------------------------------
if command_exists gitleaks; then
    echo "Gitleaks already installed; skipping"
else
echo "Installing Gitleaks ${GITLEAKS_VERSION}"

wget -q \
https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz

tar -xzf \
gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz

mv gitleaks /usr/local/bin/

chmod +x /usr/local/bin/gitleaks

rm \
gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz
fi

# -------------------------------
# OSV Scanner
# -------------------------------
if command_exists osv-scanner; then
    echo "OSV Scanner already installed; skipping"
else
echo "Installing OSV Scanner ${OSV_SCANNER_VERSION}"

wget -q \
https://github.com/google/osv-scanner/releases/download/v${OSV_SCANNER_VERSION}/osv-scanner_linux_amd64

mv osv-scanner_linux_amd64 /usr/local/bin/osv-scanner

chmod +x /usr/local/bin/osv-scanner
fi

# -------------------------------
# Update Nuclei Templates
# -------------------------------
echo "Updating Nuclei Templates"

nuclei -update-templates || true

# -------------------------------
# Verify installations
# -------------------------------
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
