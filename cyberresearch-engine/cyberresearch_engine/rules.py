import re
from pathlib import Path
from .models import Finding

TEXT_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs", ".php", ".rb", ".yml", ".yaml", ".json", ".env", ".toml", ".ini", ".cfg"}

RULES = [
    ("CR-001", "Potential hardcoded secret", "high", re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*[\"'][^\"']{8,}[\"']"), "secrets", "Move credentials to a secret manager or environment configuration."),
    ("CR-002", "Weak TLS verification disabled", "high", re.compile(r"(?i)(verify\s*=\s*False|CURLOPT_SSL_VERIFYPEER\s*[,:]\s*false|rejectUnauthorized\s*[:=]\s*false)"), "transport", "Enable certificate verification and validate the trust chain."),
    ("CR-003", "Dangerous dynamic code execution", "high", re.compile(r"(?i)\b(eval|exec)\s*\("), "code-execution", "Avoid dynamic evaluation of untrusted input; use a constrained parser instead."),
    ("CR-004", "Potential shell command construction", "medium", re.compile(r"(?i)\b(subprocess\.(run|Popen|call)|os\.system)\s*\("), "command-execution", "Prefer argument arrays and avoid passing untrusted strings to shells."),
    ("CR-005", "Permissive CORS configuration", "medium", re.compile(r"(?i)(Access-Control-Allow-Origin\s*[:=]\s*[\"']\*[\"']|origin\s*[:=]\s*[\"']\*[\"'])"), "web", "Restrict allowed origins to trusted application origins."),
]


def scan_file(path: Path):
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return findings
    for rule_id, title, severity, pattern, category, remediation in RULES:
        for line_no, line in enumerate(text.splitlines(), 1):
            match = pattern.search(line)
            if match:
                evidence = line.strip()[:180]
                findings.append(Finding(rule_id, title, severity, "medium", category, str(path), line_no, evidence, f"The pattern matched rule {rule_id}.", remediation))
    return findings


def scan_path(root: Path):
    paths = [root] if root.is_file() else root.rglob("*")
    findings = []
    for path in paths:
        if path.is_file() and (path.suffix.lower() in TEXT_EXTENSIONS or path.name.startswith(".env")):
            findings.extend(scan_file(path))
    return findings
