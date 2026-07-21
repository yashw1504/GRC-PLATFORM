FROM python:3.11-slim

WORKDIR /app

# Install system deps first
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    wget curl unzip tar git ca-certificates \
    python3-pip nmap sslscan netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Copy and install security tools
COPY docker/tool_versions.env /tmp/tool_versions.env
COPY docker/install_security_tools.sh /tmp/install_security_tools.sh
RUN chmod +x /tmp/install_security_tools.sh && /tmp/install_security_tools.sh

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Ensure directories exist
RUN mkdir -p uploads extracted output

EXPOSE 8000

CMD ["uvicorn", "grc_scanner.api.app:app", "--host", "0.0.0.0", "--port", "8000"]