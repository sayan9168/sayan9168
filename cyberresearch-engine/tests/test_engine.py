import tempfile
from pathlib import Path
from cyberresearch_engine.rules import scan_path


def test_secret_detection():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "sample.py"
        p.write_text("API_KEY = 'not-a-real-secret-value-1234'\n", encoding="utf-8")
        findings = scan_path(p)
        assert any(f.rule_id == "CR-001" for f in findings)


def test_clean_file():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "clean.py"
        p.write_text("print('hello')\n", encoding="utf-8")
        assert scan_path(p) == []
