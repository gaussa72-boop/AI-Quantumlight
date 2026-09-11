import os
import sqlite3
import base64
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise RuntimeError("SECRET_KEY must be configured")
app.secret_key = secret_key

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


def ultra_transform(text: str) -> str:
    """Reversible encoding used only as a display/storage transform; not encryption."""
    data = text.encode("utf-8")
    for _ in range(3):
        data = base64.b64encode(data[::-1])
    return data.decode("ascii")


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


with get_db() as conn:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS chats ("
        "id INTEGER PRIMARY KEY, assistant TEXT, role TEXT, message TEXT, encrypted TEXT)"
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok", "openai_configured": client is not None})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_msg = (data.get("message") or "").strip()
    assistant_name = (data.get("assistant") or "Quantumlight").strip()

    if not user_msg:
        return jsonify({"error": "message is required"}), 400

    encrypted_preview = ultra_transform(user_msg)

    if client is None:
        reply = "OpenAI ist noch nicht konfiguriert. Setze OPENAI_API_KEY in der Umgebung."
    else:
        try:
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": f"Du bist {assistant_name}, eine hochentwickelte KI in einem Dark-Sci-Fi-Universum."},
                    {"role": "user", "content": user_msg},
                ],
            )
            reply = response.choices[0].message.content or "Keine Antwort erhalten."
        except Exception:
            reply = "Die KI-Schnittstelle ist momentan nicht erreichbar."

    with get_db() as conn:
        conn.execute(
            "INSERT INTO chats (assistant, role, message, encrypted) VALUES (?, ?, ?, ?)",
            (assistant_name, "user", user_msg, encrypted_preview),
        )

    return jsonify({"reply": reply, "encryption": encrypted_preview})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
