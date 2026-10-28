"""Menggabungkan layer prompt (01..06) menjadi satu system prompt."""
from pathlib import Path

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"


def list_layers() -> list[Path]:
    return sorted(PROMPT_DIR.glob("0[1-6]-*.md"))


def build_system_prompt() -> str:
    layers = list_layers()
    if len(layers) != 6:
        raise FileNotFoundError(
            f"Ditemukan {len(layers)} layer prompt di {PROMPT_DIR}, seharusnya 6."
        )
    return "\n\n---\n\n".join(p.read_text(encoding="utf-8").strip() for p in layers) + "\n"
