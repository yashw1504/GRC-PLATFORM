"""Regenerate observed check inventory from scanner code and control mappings."""

import ast
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "grc_scanner"
SCANNERS = PACKAGE / "scanners"
OUTPUT = PACKAGE / "checks"

EXPECTED_COUNTS = {
    "web_security": 90,
    "api_security": 60,
    "ssl_tls": 60,
    "http_headers": 40,
    "network": 60,
    "aws": 55,
    "azure": 50,
    "gcp": 50,
    "kubernetes": 25,
    "database": 20,
    "secrets": 20,
    "iac": 20,
    "mobile": 20,
    "cicd": 15,
    "vulnerability": 20,
    "privacy": 20,
}

CATEGORY_SOURCES = {
    "web_security": ("web/web_scanner.py",),
    "api_security": ("api/api_scanner.py",),
    "ssl_tls": ("ssl/ssl_scanner.py", "web/web_scanner.py"),
    "http_headers": ("web/web_scanner.py", "api/api_scanner.py"),
    "network": ("network/network_scanner.py",),
    "aws": ("cloud/aws_scanner.py",),
    "azure": ("cloud/azure_scanner.py",),
    "gcp": ("cloud/gcp_scanner.py",),
    "kubernetes": ("kubernetes/kubernetes_scanner.py", "cloud/azure_scanner.py", "cloud/gcp_scanner.py"),
    "database": ("database/database_scanner.py",),
    "secrets": ("secrets/secrets_scanner.py",),
    "iac": ("iac/iac_scanner.py",),
    "mobile": ("apk/apk_scanner.py",),
    "cicd": ("cicd/cicd_scanner.py",),
    "vulnerability": ("vulnerability/vulnerability_scanner.py", "container/container_scanner.py", "sbom/sbom_scanner.py", "semgrep/semgrep_scanner.py"),
    "privacy": ("web/web_scanner.py",),
}

IMPLEMENTATION_STATUS = {
    "web_security": ("partial", "Active HTTP checks exist; coverage is far below the requested catalog."),
    "api_security": ("partial", "Passive response checks are active; authentication and authorization probes are not."),
    "ssl_tls": ("partial", "Custom web TLS checks and optional SSLScan are present."),
    "http_headers": ("partial", "A small set of response header checks is active."),
    "network": ("partial", "Nmap is optional; without it, the scan reports an unavailable result."),
    "aws": ("partial", "Boto3 checks run only when account credentials are available."),
    "azure": ("unavailable", "Current scanner reports unavailable; legacy check methods are not invoked."),
    "gcp": ("unavailable", "Current scanner reports unavailable; legacy check methods are not invoked."),
    "kubernetes": ("partial", "Manifest checks run locally; Kubescape is optional."),
    "database": ("unavailable", "No database client checks are active."),
    "secrets": ("partial", "Gitleaks or local pattern checks run on source paths."),
    "iac": ("partial", "Checkov is optional; local Terraform checks provide limited coverage."),
    "mobile": ("partial", "APK checks are limited and external mobile tooling is not wired into the active path."),
    "cicd": ("partial", "Repository workflow checks cover a subset of pipeline risks."),
    "vulnerability": ("partial", "Nuclei and fallback exposure probes cover a subset of web vulnerabilities."),
    "privacy": ("partial", "A small number of website privacy indicators are checked."),
}


def extract_declared_ids(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    check_ids = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id == "Finding":
            value = next((kw.value for kw in node.keywords if kw.arg == "check_id"), None)
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                check_ids.add(value.value)
        if isinstance(node.func, ast.Attribute) and node.func.attr == "_create_finding" and node.args:
            value = node.args[0]
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                check_ids.add(value.value)
    return check_ids


def framework_name(control):
    prefixes = ("PCI", "ISO", "NIST", "GDPR", "HIPAA", "SOC2", "DPDPA", "OWASP")
    return next((prefix for prefix in prefixes if control.startswith(prefix)), "OTHER")


def main():
    mapping_path = PACKAGE / "frameworks" / "frameworks.json"
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))["check_to_control_mapping"]
    source_files = sorted(SCANNERS.rglob("*.py"))
    code_text = {path: path.read_text(encoding="utf-8") for path in source_files}
    declared_by_file = {path: extract_declared_ids(path) for path in source_files}
    check_ids = set(mapping)
    for ids in declared_by_file.values():
        check_ids.update(ids)

    checks = []
    for check_id in sorted(check_ids):
        refs = [
            path.relative_to(ROOT).as_posix()
            for path, text in code_text.items()
            if check_id in declared_by_file[path] or re.search(
                rf"(?<![A-Za-z0-9_]){re.escape(check_id)}(?![A-Za-z0-9_])",
                text,
            )
        ]
        controls = mapping.get(check_id, [])
        checks.append({
            "id": check_id,
            "code_references": refs,
            "mapped_controls": controls,
            "mapped_frameworks": sorted({framework_name(control) for control in controls}),
            "mapping_status": "mapped" if controls else "unmapped",
            "definition_status": "missing",
        })

    catalog = {
        "schema_version": 1,
        "source": "Generated from scanner source references and frameworks/frameworks.json",
        "definitions_complete": False,
        "definition_note": "Code references and mappings are inventory evidence, not authored check definitions.",
        "checks": checks,
    }
    category_count_sum = sum(EXPECTED_COUNTS.values())
    detailed_file_counts = dict(EXPECTED_COUNTS)
    detailed_file_counts.update({"ssl_tls": 55, "http_headers": 35, "network": 50})
    detailed_file_count_sum = sum(detailed_file_counts.values())
    categories = []
    for category, expected in EXPECTED_COUNTS.items():
        sources = CATEGORY_SOURCES[category]
        observed = sorted({
            check_id for check_id in check_ids
            if any(source in ref for source in sources for ref in next(
                (entry["code_references"] for entry in checks if entry["id"] == check_id), []
            ))
        })
        status, note = IMPLEMENTATION_STATUS[category]
        categories.append({
            "id": category,
            "prompt_expected_checks": expected,
            "observed_check_ids": len(observed),
            "implementation_status": status,
            "scanner_sources": [f"grc_scanner/scanners/{source}" for source in sources],
            "note": note,
        })

    matrix = {
        "schema_version": 1,
        "prompt_expected_total": 625,
        "prompt_category_count_sum": category_count_sum,
        "count_reconciliation": {
            "prompt_total_matches_category_sum": category_count_sum == 625,
            "detailed_file_count_sum": detailed_file_count_sum,
            "detailed_file_counts_match_total": detailed_file_count_sum == 625,
            "note": "The category table sums to 625, but the detailed SSL, header, and network file ranges sum to 605.",
        },
        "catalog_check_ids": len(checks),
        "code_referenced_check_ids": sum(bool(entry["code_references"]) for entry in checks),
        "mapped_check_ids": sum(bool(entry["mapped_controls"]) for entry in checks),
        "mapping_only_check_ids": sum(
            bool(entry["mapped_controls"]) and not entry["code_references"]
            for entry in checks
        ),
        "code_referenced_unmapped_check_ids": sum(
            bool(entry["code_references"]) and not entry["mapped_controls"]
            for entry in checks
        ),
        "unmapped_check_ids": sum(not entry["mapped_controls"] for entry in checks),
        "mapped_ids_with_fewer_than_three_frameworks": sum(
            bool(entry["mapped_controls"]) and len(entry["mapped_frameworks"]) < 3
            for entry in checks
        ),
        "mapped_ids_missing_pci": sum(
            bool(entry["mapped_controls"]) and "PCI" not in entry["mapped_frameworks"]
            for entry in checks
        ),
        "mapped_ids_missing_owasp": sum(
            bool(entry["mapped_controls"]) and "OWASP" not in entry["mapped_frameworks"]
            for entry in checks
        ),
        "categories": categories,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "observed_check_catalog.json").write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (OUTPUT / "scanner_coverage_matrix.json").write_text(
        json.dumps(matrix, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "catalog_check_ids": len(checks),
        "code_referenced_check_ids": matrix["code_referenced_check_ids"],
        "mapped_check_ids": matrix["mapped_check_ids"],
        "unmapped_check_ids": matrix["unmapped_check_ids"],
        "prompt_category_count_sum": category_count_sum,
        "output": str(OUTPUT.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
