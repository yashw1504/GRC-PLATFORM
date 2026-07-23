import os
from enum import Enum
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from grc_scanner.engine.scan_engine import ScanEngine
from grc_scanner.storage.dashboard_repository import DashboardRepository
from grc_scanner.storage.scan_repository import ScanRepository
from grc_scanner.storage.findings_repository import FindingsRepository
from grc_scanner.storage.compliance_repository import ComplianceRepository
from grc_scanner.storage.report_repository import ReportRepository
from grc_scanner.utils.file_utils import FileUtils
from dotenv import load_dotenv
from grc_scanner.api.credentials_api import router as credentials_router

load_dotenv()

app = FastAPI(title="GRC Platform API")

# Allow all origins in dev (lock down in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(credentials_router)

class ScanType(str, Enum):
    website = "website"
    source = "source"
    container = "container"
    iac = "iac"
    secrets = "secrets"
    vulnerability = "vulnerability"
    full = "full"

class ScanRequest(BaseModel):
    target_type: str = "website"
    target: str

@app.get("/")
def home():
    return {"message": "GRC Platform API Running", "version": "1.0.0"}

@app.get("/dashboard")
def dashboard():
    return DashboardRepository.get_summary()

@app.get("/scans")
def scans():
    return ScanRepository.get_scans()

@app.get("/findings")
def findings():
    return FindingsRepository.get_findings()

@app.get("/compliance")
def compliance():
    return ComplianceRepository.get_compliance_scores()

@app.post("/scan")
def run_scan(request: ScanRequest):
    engine = ScanEngine()
    try:
        result = engine.run(request.target, request.target_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    # Convert findings to dicts for JSON response
    result["findings"] = [f.to_dict() for f in result["findings"]]
    return result

@app.post("/scan-upload")
async def scan_upload(scan_type: ScanType = Form(...), file: UploadFile = File(...)):
    saved_file = FileUtils.save_upload(file)
    project_path = FileUtils.extract_archive(saved_file)
    engine = ScanEngine()
    result = engine.run(target=project_path, scan_type=scan_type.value, source_path=project_path)
    result["findings"] = [f.to_dict() for f in result["findings"]]
    return result

@app.get("/scans/{scan_id}")
def scan_details(scan_id: int):
    return {
        "scan": ScanRepository.get_scan(scan_id),
        "findings": FindingsRepository.get_findings_by_scan(scan_id),
        "compliance": ComplianceRepository.get_scores_by_scan(scan_id)
    }

@app.get("/reports/{scan_id}")
def get_reports(scan_id: int):
    return ReportRepository.get_reports_by_scan(scan_id)

@app.get("/download/{scan_id}/{report_type}")
def download_report(scan_id: int, report_type: str):
    reports = ReportRepository.get_reports_by_scan(scan_id)
    for report in reports:
        if report["type"] == report_type:
            if not os.path.exists(report["path"]):
                raise HTTPException(status_code=404, detail="Report file not found")
            return FileResponse(report["path"], filename=os.path.basename(report["path"]))
    raise HTTPException(status_code=404, detail="Report not found")

@app.get("/compliance/{scan_id}")
def compliance_by_scan(scan_id: int):
    return ComplianceRepository.get_scores_by_scan(scan_id)

@app.get("/download-report/{report_id}")
def download_report_by_id(report_id: int):
    report = ReportRepository.get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if not os.path.exists(report["path"]):
        raise HTTPException(status_code=404, detail="Report file not found")
    return FileResponse(report["path"], filename=os.path.basename(report["path"]))