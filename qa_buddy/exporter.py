"""Ekspor test case ke CSV (dapat dibuka di Excel / Google Sheets)."""
import csv
import io
import re

COLUMNS = [
    ("id", "ID"),
    ("req", "Requirement"),
    ("judul", "Judul"),
    ("kategori", "Kategori"),
    ("prioritas", "Prioritas"),
    ("precondition", "Precondition"),
    ("langkah", "Langkah"),
    ("data_uji", "Data Uji"),
    ("expected", "Expected Result"),
]


def _clean(value: str) -> str:
    return re.sub(r"\s*<br\s*/?>\s*", "\n", value or "")


def to_csv(cases: list[dict]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([label for _, label in COLUMNS])
    for case in cases:
        writer.writerow([_clean(case.get(key, "")) for key, _ in COLUMNS])
    return buf.getvalue()
