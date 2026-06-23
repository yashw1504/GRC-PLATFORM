FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y wget

RUN apt-get update && \
    apt-get install -y nmap

RUN wget https://github.com/gitleaks/gitleaks/releases/download/v8.24.2/gitleaks_8.24.2_linux_x64.tar.gz \
    && tar -xzf gitleaks_8.24.2_linux_x64.tar.gz \
    && mv gitleaks /usr/local/bin/

RUN wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor -o /usr/share/keyrings/trivy.gpg

RUN echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" \
    > /etc/apt/sources.list.d/trivy.list

RUN apt-get update && \
    apt-get install -y trivy



COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "grc_scanner.api.app:app", "--host", "0.0.0.0", "--port", "8000"]