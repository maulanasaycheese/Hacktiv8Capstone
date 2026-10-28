"""Gabungkan semua layer prompt menjadi satu system prompt."""
from pathlib import Path

root = Path(__file__).parent / "prompts"
layers = sorted(root.glob("0[1-6]-*.md"))
combined = "\n\n---\n\n".join(p.read_text(encoding="utf-8").strip() for p in layers)
out = root / "system-prompt.generated.md"
out.write_text(combined + "\n", encoding="utf-8")
print(f"{len(layers)} layer digabung -> {out} ({len(combined)} karakter)")
