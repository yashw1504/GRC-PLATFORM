from fastapi import FastAPI
from grc_scanner.storage.dashboard_repository import (
    DashboardRepository
)
from grc_scanner.storage.scan_repository import (
    ScanRepository
)

from grc_scanner.storage.findings_repository import (
    FindingsRepository
)

from grc_scanner.storage.compliance_repository import (
    ComplianceRepository
)

from pydantic import BaseModel

from grc_scanner.engine.scan_engine import (
    ScanEngine
)

from fastapi.responses import FileResponse

from grc_scanner.storage.report_repository import (
    ReportRepository
)

from fastapi.responses import FileResponse
from grc_scanner.storage.report_repository import (
    ReportRepository
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi import UploadFile, File, Form

app = FastAPI(
    title="GRC Platform API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://13.233.237.54:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(
    BaseModel
):
    target_type: str
    target: str


@app.get("/")
def home():

    return {
        "message": "GRC Platform Running"
    }

@app.get("/dashboard")
def dashboard():

    return (
        DashboardRepository.get_summary()
    )

@app.get("/scans")
def scans():

    return (
        ScanRepository.get_scans()
    )

@app.get("/findings")
def findings():

    return (
        FindingsRepository.get_findings()
    )

@app.get("/compliance")
def compliance():

    return (
        ComplianceRepository.get_compliance_scores()
    )

@app.post("/scan")
def run_scan(
    request: ScanRequest
):

    engine = ScanEngine()

    result = engine.run(
        request.target,
        request.target_type
    )

    return {
        "target": request.target,
        "overall_score": result[
            "overall_score"
        ],
        "findings": result[
            "total_findings"
        ],
        "compliance_scores": result[
            "compliance_scores"
        ]
    }

@app.post("/scan-upload")
async def scan_upload(

    scan_type: str = Form(...),

    file: UploadFile = File(...)

):

    return {
        "filename": file.filename,
        "scan_type": scan_type
    }

@app.get("/scans/{scan_id}")
def scan_details(
    scan_id: int
):

    return {
        "scan":
            ScanRepository.get_scan(
                scan_id
            ),

        "findings":
            FindingsRepository
            .get_findings_by_scan(
                scan_id
            ),

        "compliance":
            ComplianceRepository
            .get_scores_by_scan(
                scan_id
            )
    }

@app.get(
    "/reports/{scan_id}"
)
def get_reports(
    scan_id: int
):

    return (
        ReportRepository
        .get_reports_by_scan(
            scan_id
        )
    )

@app.get(
    "/download/{scan_id}/{report_type}"
)
def download_report(
    scan_id: int,
    report_type: str
):

    reports = (
        ReportRepository
        .get_reports_by_scan(
            scan_id
        )
    )

    for report in reports:

        if (
            report["type"]
            ==
            report_type
        ):

            return FileResponse(
                report["path"],
                filename=
                report["path"]
                .split("/")[-1]
            )

    return {
        "error":
        "Report not found"
    }

@app.get(
    "/compliance/{scan_id}"
)
def compliance_by_scan(
    scan_id: int
):

    return (
        ComplianceRepository
        .get_scores_by_scan(
            scan_id
        )
    )

@app.get(
    "/compliance/{scan_id}"
)
def compliance_by_scan(
    scan_id: int
):

    return (
        ComplianceRepository
        .get_scores_by_scan(
            scan_id
        )
    )

@app.get(
    "/download-report/{report_id}"
)
def download_report(
    report_id: int
):

    report = (
        ReportRepository
        .get_report_by_id(
            report_id
        )
    )

    if not report:

        return {
            "error": "Report not found"
        }

    return FileResponse(
        report["path"],
        filename=
        report["path"]
        .split("/")[-1]
    )