import argparse
import json
from pathlib import Path
from .rules import scan_path


def main():
    parser = argparse.ArgumentParser(description="SAYANOX CyberResearch Engine — defensive local source scanner")
    parser.add_argument("target", help="Local file or directory you are authorized to analyze")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        parser.error("target does not exist")
    findings = scan_path(target)
    if args.format == "json":
        print(json.dumps([f.to_dict() for f in findings], indent=2))
        return
    print(f"CyberResearch Engine 0.1.0 | findings: {len(findings)}")
    for f in findings:
        location = f"{f.path}:{f.line}" if f.line else f.path
        print(f"[{f.severity.upper()}] {f.rule_id} {f.title} — {location}")
        print(f"  Evidence: {f.evidence}")
        print(f"  Fix: {f.remediation}")


if __name__ == "__main__":
    main()
