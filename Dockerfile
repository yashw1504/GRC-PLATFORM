FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# The project's version-pinned installer provides every CLI used by the
# scanner wrappers (Nmap, Nuclei, SSLScan, Trivy, Syft, Grype, Gitleaks,
# OSV Scanner, Semgrep, and Checkov).
COPY docker/tool_versions.env /tmp/tool_versions.env
COPY docker/install_security_tools.sh /usr/local/bin/install-security-tools
RUN chmod +x /usr/local/bin/install-security-tools \
    && /usr/local/bin/install-security-tools \
    && rm -f /tmp/tool_versions.env /usr/local/bin/install-security-tools

COPY . .

EXPOSE 8000

CMD ["uvicorn", "grc_scanner.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
