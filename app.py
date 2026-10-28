"""Web UI & API QA Buddy (Flask)."""
import os

from flask import Flask, Response, jsonify, render_template, request

from qa_buddy.agent import generate
from qa_buddy.exporter import to_csv


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 256 * 1024

    @app.get("/")
    def index():
        live = bool(os.getenv("ANTHROPIC_API_KEY", "").strip())
        return render_template("index.html", live=live)

    @app.post("/api/generate")
    def api_generate():
        data = request.get_json(silent=True) or {}
        try:
            result = generate(data.get("requirement", ""), data.get("context", ""))
        except ValueError as exc:
            return jsonify(error=str(exc)), 400
        except Exception as exc:  # kesalahan dari penyedia model / jaringan
            app.logger.exception("Gagal memanggil model")
            return jsonify(error=f"Gagal menghubungi model: {type(exc).__name__}"), 502
        return jsonify(result.to_dict())

    @app.post("/api/export")
    def api_export():
        data = request.get_json(silent=True) or {}
        cases = data.get("cases")
        if not isinstance(cases, list) or not cases:
            return jsonify(error="Tidak ada test case untuk diekspor."), 400
        body = "\ufeff" + to_csv(cases)  # BOM agar Excel membaca UTF-8
        return Response(
            body,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=test-cases.csv"},
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
