# GRC Platform

## Features

- Web Security Scanning
- Network Security Scanning
- Cloud Security Scanning
- Compliance Mapping
- Risk Scoring
- Executive Reports
- Dashboard

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