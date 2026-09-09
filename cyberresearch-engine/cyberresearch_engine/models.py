from dataclasses import dataclass, asdict
from typing import Optional
import json

SEVERITIES = ("info", "low", "medium", "high", "critical")

@dataclass(frozen=True)
class Finding:
    rule_id: str
    title: str
    severity: str
    confidence: str
    category: str
    path: str
    line: Optional[int]
    evidence: str
    description: str
    remediation: str
    cwe: Optional[str] = None

    def __post_init__(self):
        if self.severity not in SEVERITIES:
            raise ValueError(f"invalid severity: {self.severity}")

    def to_dict(self):
        return asdict(self)


def findings_to_json(findings):
    return json.dumps([f.to_dict() for f in findings], indent=2)
