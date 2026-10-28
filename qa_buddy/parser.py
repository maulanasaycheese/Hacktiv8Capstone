"""Mengubah tabel markdown hasil agent menjadi daftar test case terstruktur."""
from collections import Counter

HEADER_MAP = {
    "id": "id",
    "req": "req",
    "judul": "judul",
    "kategori": "kategori",
    "prioritas": "prioritas",
    "precondition": "precondition",
    "langkah": "langkah",
    "data uji": "data_uji",
    "expected result": "expected",
}


def _split_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(c and set(c) <= set("-: ") for c in cells)


def parse_test_cases(markdown: str) -> list[dict]:
    """Ambil baris test case dari tabel markdown pertama yang punya kolom ID."""
    cases: list[dict] = []
    columns: list[str] | None = None
    for raw in markdown.splitlines():
        if not raw.strip().startswith("|"):
            if columns and cases:
                break  # tabel selesai
            continue
        cells = _split_row(raw)
        if _is_separator(cells):
            continue
        if columns is None:
            names = [HEADER_MAP.get(c.lower()) for c in cells]
            if names and names[0] == "id":
                columns = names
            continue
        if len(cells) < len(columns):
            cells += [""] * (len(columns) - len(cells))
        row = {name: cells[i] for i, name in enumerate(columns) if name}
        if row.get("id"):
            cases.append(row)
    return cases


def summarize(cases: list[dict]) -> dict:
    """Ringkasan cakupan per kategori dan per requirement."""
    return {
        "total": len(cases),
        "per_kategori": dict(Counter(c.get("kategori", "") for c in cases)),
        "per_requirement": dict(Counter(c.get("req", "") for c in cases)),
    }
