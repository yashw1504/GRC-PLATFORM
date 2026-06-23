FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y wget

RUN apt-get update && apt-get install -y \
    nmap \
    sslscan

RUN apt-get update && \
    apt-get install -y wget unzip && \
    wget https://github.com/projectdiscovery/nuclei/releases/latest/download/nuclei_3.4.10_linux_amd64.zip && \
    unzip nuclei_3.4.10_linux_amd64.zip && \
    mv nuclei /usr/local/bin/ && \
    chmod +x /usr/local/bin/nuclei && \
    rm -f nuclei_3.4.10_linux_amd64.zip


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "grc_scanner.api.app:app", "--host", "0.0.0.0", "--port", "8000"]