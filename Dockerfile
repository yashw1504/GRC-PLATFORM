FROM python:3.11-slim

WORKDIR /app

# Copy version file and installer first (better layer caching)
COPY docker/tool_versions.env /tmp/tool_versions.env
COPY docker/install_security_tools.sh /tmp/install_security_tools.sh
COPY docker/verify_security_tools.sh /tmp/verify_security_tools.sh

# Install all security tools
RUN chmod +x /tmp/install_security_tools.sh && \
    chmod +x /tmp/verify_security_tools.sh && \
    /tmp/install_security_tools.sh && \
    /tmp/verify_security_tools.sh

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

EXPOSE 8000

CMD ["uvicorn", "grc_scanner.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
