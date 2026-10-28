"""Inti agent: menyusun prompt berlapis dan memanggil model."""
import os
from dataclasses import dataclass, field
from pathlib import Path

from .parser import parse_test_cases, summarize
from .prompts import build_system_prompt

ROOT = Path(__file__).resolve().parent.parent
DEMO_OUTPUT = ROOT / "examples" / "output-login.md"
DEFAULT_MODEL = "claude-sonnet-5-5"
MAX_REQUIREMENT_CHARS = 8000
MAX_TOKENS = 4000


@dataclass
class Result:
    markdown: str
    cases: list[dict] = field(default_factory=list)
    summary: dict = field(default_factory=dict)
    demo: bool = False

    def to_dict(self) -> dict:
        return {
            "markdown": self.markdown,
            "cases": self.cases,
            "summary": self.summary,
            "demo": self.demo,
        }


def _make_result(markdown: str, demo: bool) -> Result:
    cases = parse_test_cases(markdown)
    return Result(markdown=markdown, cases=cases, summary=summarize(cases), demo=demo)


def build_user_message(requirement: str, context: str = "") -> str:
    parts = []
    if context.strip():
        parts.append(f"Konteks proyek:\n{context.strip()}")
    parts.append(f"Requirement:\n{requirement.strip()}")
    return "\n\n".join(parts)


def generate(requirement: str, context: str = "", client=None) -> Result:
    """Buat test case dari requirement.

    Tanpa ANTHROPIC_API_KEY, agent berjalan dalam mode DEMO (output contoh tetap),
    sehingga aplikasi dapat diperagakan tanpa koneksi ke model.
    """
    requirement = (requirement or "").strip()
    if not requirement:
        raise ValueError("Requirement tidak boleh kosong.")
    if len(requirement) > MAX_REQUIREMENT_CHARS:
        raise ValueError(f"Requirement terlalu panjang (maksimal {MAX_REQUIREMENT_CHARS} karakter).")

    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if client is None and not api_key:
        return _make_result(DEMO_OUTPUT.read_text(encoding="utf-8"), demo=True)

    if client is None:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model=os.getenv("QA_BUDDY_MODEL", DEFAULT_MODEL),
        max_tokens=MAX_TOKENS,
        system=build_system_prompt(),
        messages=[{"role": "user", "content": build_user_message(requirement, context)}],
    )
    text = "".join(b.text for b in message.content if getattr(b, "type", "") == "text")
    return _make_result(text, demo=False)
