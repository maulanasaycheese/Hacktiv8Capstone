import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app  # noqa: E402
from qa_buddy import agent  # noqa: E402
from qa_buddy.exporter import to_csv  # noqa: E402
from qa_buddy.parser import parse_test_cases, summarize  # noqa: E402
from qa_buddy.prompts import build_system_prompt, list_layers  # noqa: E402

EXAMPLE = Path(__file__).resolve().parent.parent / "examples" / "output-login.md"


@pytest.fixture(autouse=True)
def no_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)


def test_six_prompt_layers_combined():
    assert len(list_layers()) == 6
    prompt = build_system_prompt()
    for marker in ("Layer 1", "Layer 2", "Layer 3", "Layer 4", "Layer 5", "Layer 6"):
        assert marker in prompt


def test_parser_reads_example_output():
    cases = parse_test_cases(EXAMPLE.read_text(encoding="utf-8"))
    assert len(cases) == 13
    assert cases[0]["id"] == "TC-001"
    assert cases[7]["kategori"] == "Boundary"
    assert "<br>" in cases[0]["langkah"]


def test_summary_matches_documented_coverage():
    s = summarize(parse_test_cases(EXAMPLE.read_text(encoding="utf-8")))
    assert s["total"] == 13
    assert s["per_kategori"]["Negative"] == 4
    assert s["per_requirement"] == {"REQ-1": 6, "REQ-2": 2, "REQ-3": 3, "REQ-4": 2}


def test_csv_export_converts_line_breaks():
    csv_text = to_csv(parse_test_cases(EXAMPLE.read_text(encoding="utf-8")))
    assert csv_text.splitlines()[0].startswith("ID,Requirement")
    assert "<br>" not in csv_text


def test_empty_requirement_rejected():
    with pytest.raises(ValueError):
        agent.generate("   ")


def test_demo_mode_without_api_key():
    result = agent.generate("REQ-1: contoh")
    assert result.demo is True
    assert len(result.cases) == 13


def test_live_path_uses_system_prompt_and_parses():
    captured = {}

    class FakeMessages:
        def create(self, **kwargs):
            captured.update(kwargs)
            text = "| ID | Req | Judul | Kategori | Prioritas | Precondition | Langkah | Data Uji | Expected Result |\n|---|---|---|---|---|---|---|---|---|\n| TC-001 | REQ-1 | x | Positive | High | - | 1. a | d | ok |"
            return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)])

    fake = SimpleNamespace(messages=FakeMessages())
    result = agent.generate("REQ-1: usia 17-60", "aplikasi HR", client=fake)
    assert result.demo is False and len(result.cases) == 1
    assert "Layer 5" in captured["system"]
    assert "aplikasi HR" in captured["messages"][0]["content"]


def test_api_endpoints():
    client = create_app().test_client()
    assert client.get("/").status_code == 200
    bad = client.post("/api/generate", json={"requirement": ""})
    assert bad.status_code == 400
    ok = client.post("/api/generate", json={"requirement": "REQ-1: login"})
    assert ok.status_code == 200 and ok.get_json()["demo"] is True
    csv_resp = client.post("/api/export", json={"cases": ok.get_json()["cases"]})
    assert csv_resp.status_code == 200
    assert csv_resp.mimetype == "text/csv"
    assert client.post("/api/export", json={"cases": []}).status_code == 400
