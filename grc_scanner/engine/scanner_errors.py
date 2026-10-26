from grc_scanner.engine.finding import Finding
from urllib.parse import urlsplit, urlunsplit


def _safe_target(target):
    if not target:
        return ""
    value = str(target)
    parsed = urlsplit(value)
    if parsed.scheme and parsed.hostname:
        hostname = parsed.hostname
        if ":" in hostname:
            hostname = f"[{hostname}]"
        try:
            port = parsed.port
        except ValueError:
            port = None
        if port:
            hostname = f"{hostname}:{port}"
        return urlunsplit((parsed.scheme, hostname, parsed.path, "", ""))
    return value


def scanner_error_finding(scanner_name, detail, target="", category="Scanner Error"):
    safe_target = _safe_target(target)
    check_id = "SCANNER-" + "-".join(
        part for part in scanner_name.upper().replace("_", " ").split() if part
    )
    return Finding(
        check_id=check_id,
        name=f"{scanner_name.replace('_', ' ').title()} unavailable",
        status="error",
        severity="Info",
        description=detail,
        evidence=safe_target,
        category=category,
        target_asset=safe_target,
        scanner_name=scanner_name,
        raw_data={"error": True},
    )
