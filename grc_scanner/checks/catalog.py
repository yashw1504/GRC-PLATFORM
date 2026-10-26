"""Load the generated inventory without importing scanner implementations."""

import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent


def load_catalog():
    with (DATA_DIR / "observed_check_catalog.json").open(encoding="utf-8") as handle:
        return json.load(handle)


def load_coverage_matrix():
    with (DATA_DIR / "scanner_coverage_matrix.json").open(encoding="utf-8") as handle:
        return json.load(handle)


def coverage_summary():
    catalog = load_catalog()
    matrix = load_coverage_matrix()
    entries = catalog["checks"]
    return {
        "catalog_check_ids": len(entries),
        "code_referenced_check_ids": matrix["code_referenced_check_ids"],
        "mapped_check_ids": sum(bool(entry["mapped_controls"]) for entry in entries),
        "unmapped_check_ids": sum(not entry["mapped_controls"] for entry in entries),
        "mapping_only_check_ids": matrix["mapping_only_check_ids"],
        "code_referenced_unmapped_check_ids": matrix["code_referenced_unmapped_check_ids"],
        "mapped_ids_with_fewer_than_three_frameworks": matrix[
            "mapped_ids_with_fewer_than_three_frameworks"
        ],
        "mapped_ids_missing_pci": matrix["mapped_ids_missing_pci"],
        "mapped_ids_missing_owasp": matrix["mapped_ids_missing_owasp"],
        "scanner_categories": len(matrix["categories"]),
        "categories_with_full_implementation": sum(
            category["implementation_status"] == "complete"
            for category in matrix["categories"]
        ),
        "definitions_complete": catalog["definitions_complete"],
        "prompt_expected_total": matrix["prompt_expected_total"],
        "prompt_category_count_sum": matrix["prompt_category_count_sum"],
        "detailed_file_count_sum": matrix["count_reconciliation"]["detailed_file_count_sum"],
    }
