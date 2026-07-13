FROM python:3.11-slim

WORKDIR /app

# System packages
RUN apt-get update && \
    apt-get install -y \
    wget \
    unzip \
    curl \
    git \
    jq \
    ca-certificates \
    nmap \
    sslscan && \
    rm -rf /var/lib/apt/lists/*

# Copy installer
COPY docker/install_security_tools.sh /tmp/install_security_tools.sh
RUN chmod +x /tmp/install_security_tools.sh && \
    /tmp/install_security_tools.sh

# Verify installation
COPY docker/verify_security_tools.sh /tmp/verify_security_tools.sh
RUN chmod +x /tmp/verify_security_tools.sh && \
    /tmp/verify_security_tools.sh

# Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Application
COPY . .

EXPOSE 8000

CMD [
    "uvicorn",
    "grc_scanner.api.app:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]