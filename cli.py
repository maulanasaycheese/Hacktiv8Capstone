"""Pemakaian: python cli.py examples/input-login.md [--context "..."] [--out hasil.csv]"""
import argparse
import sys
from pathlib import Path

from qa_buddy.agent import generate
from qa_buddy.exporter import to_csv


def main() -> int:
    ap = argparse.ArgumentParser(description="QA Buddy - generator test case")
    ap.add_argument("input", help="file teks berisi requirement")
    ap.add_argument("--context", default="", help="konteks proyek singkat")
    ap.add_argument("--out", help="simpan test case ke file CSV")
    args = ap.parse_args()

    requirement = Path(args.input).read_text(encoding="utf-8")
    try:
        result = generate(requirement, args.context)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if result.demo:
        print("[MODE DEMO] ANTHROPIC_API_KEY belum diset, memakai output contoh.\n")
    print(result.markdown)
    if args.out:
        Path(args.out).write_text("\ufeff" + to_csv(result.cases), encoding="utf-8")
        print(f"\n{len(result.cases)} test case disimpan ke {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
