# GRC Platform

## Docker deployment

The default Compose file is an EC2-ready deployment file and needs only
`docker-compose.yml` plus a `.env` file on the server. It pulls the images
published by the GitHub Actions workflow:

```bash
cp .env.ec2.example .env
# Edit DB_PASSWORD and VAULT_KEY in .env
docker compose pull
docker compose up -d
```

For a source build on a development machine:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```

## Features

- Web Security Scanning
- Network Security Scanning
- Cloud Security Scanning
- Container Scanning
- Compliance Mapping
- Risk Scoring
- Executive Reports
- Dashboard
- APK Scanning

## Tech Stack

Backend:
- FastAPI
- PostgreSQL (Neon)

Frontend:
- React
- Vite

Cloud:
- AWS
- Azure
- GCP

## Run Backend

uvicorn grc_scanner.api.app:app --reload

## Run Frontend

cd frontend
npm install
npm run dev
