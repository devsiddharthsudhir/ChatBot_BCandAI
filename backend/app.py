from pathlib import Path
import json
from datetime import datetime
import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS

from ml.model import get_response, MODEL_VERSION
from backend import provenance

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "backend" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
CORS(app)

def append_log(session_id: str, entry: dict) -> Path:
    log_path = LOG_DIR / f"{session_id}.jsonl"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return log_path

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()
    session_id = data.get("session_id") or str(uuid.uuid4())

    if not user_message:
        return jsonify({"error": "Empty message", "session_id": session_id}), 400

    reply, meta = get_response(user_message)

    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "session_id": session_id,
        "user_message": user_message,
        "bot_reply": reply,
        "intent_tag": meta["intent_tag"],
        "model_version": meta["model_version"],
        "dataset_id": meta["dataset_id"],
    }

    log_path = append_log(session_id, log_entry)

    try:
        tx_hash = provenance.commit_log(session_id, log_path, MODEL_VERSION)
    except Exception as e:
        print("Blockchain commit failed:", e)
        tx_hash = None

    return jsonify(
        {
            "reply": reply,
            "session_id": session_id,
            "meta": {**meta, "log_tx_hash": tx_hash},
        }
    )

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model_version": MODEL_VERSION})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
