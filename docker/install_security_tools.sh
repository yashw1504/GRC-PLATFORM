#!/bin/bash

set -e

echo "=================================="
echo "Installing Security Tools"
echo "=================================="

####################################
# Nuclei
####################################

wget https://github.com/projectdiscovery/nuclei/releases/download/v3.4.7/nuclei_3.4.7_linux_amd64.zip

unzip nuclei_3.4.7_linux_amd64.zip

mv nuclei /usr/local/bin/

chmod +x /usr/local/bin/nuclei

rm nuclei_3.4.7_linux_amd64.zip


####################################
# Semgrep
####################################

pip install semgrep


####################################
# Checkov
####################################

pip install checkov


####################################
# Syft
####################################

curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh \
| sh -s -- -b /usr/local/bin


####################################
# Grype
####################################

curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh \
| sh -s -- -b /usr/local/bin


####################################
# Trivy
####################################

wget https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.67.2_Linux-64bit.deb

dpkg -i trivy_0.67.2_Linux-64bit.deb

rm trivy_0.67.2_Linux-64bit.deb


####################################
# Gitleaks
####################################

wget https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_8.28.0_linux_x64.tar.gz

tar -xzf gitleaks_8.28.0_linux_x64.tar.gz

mv gitleaks /usr/local/bin/

chmod +x /usr/local/bin/gitleaks

rm gitleaks_8.28.0_linux_x64.tar.gz


####################################
# Update Nuclei Templates
####################################

nuclei -update-templates

echo "=================================="
echo "Installation Completed"
echo "=================================="