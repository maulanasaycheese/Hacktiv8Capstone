# QA Buddy - AI Agent Test Case Generator

AI Agent yang mengubah requirement / user story menjadi test case terstruktur
(Positive, Negative, Boundary, Edge, Security) lengkap dengan coverage summary.
Perilaku agent dibentuk oleh **6 layer prompt** (`prompts/`), yang dapat dipakai langsung
di IBM Bob maupun lewat aplikasi web/CLI di repo ini.

## Struktur
```
qa-buddy/
  prompts/            6 layer prompt: role, context, task, format, guardrails, few-shot
  qa_buddy/           agent.py (panggil model), prompts.py, parser.py, exporter.py
  templates/ static/  antarmuka web
  app.py              server web + API (/api/generate, /api/export)
  cli.py              versi baris perintah
  build_prompt.py     gabungkan 6 layer menjadi satu system prompt
  examples/           contoh input & output (login toko online, 13 test case)
  tests/              8 pengujian otomatis (pytest)
```

CLI:
```powershell
python cli.py examples/input-login.md --out hasil.csv
```

Pengujian: `python -m pytest -q`

## Keamanan
API key hanya dibaca dari environment variable dan tidak pernah disimpan di repo
(`.env` sudah ada di `.gitignore`). Keluaran model ditampilkan lewat `textContent`, bukan `innerHTML`.

## Teknologi
Python 3, Flask, Anthropic SDK, HTML/CSS/JavaScript, pytest, IBM Bob (prompt layering).
