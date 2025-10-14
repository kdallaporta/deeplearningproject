# main.py
from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import os

app = Flask(__name__)
clf = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

@app.get("/")
def index():
    return render_template("query_page.html")

@app.post("/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify(error="empty text"), 400
    try:
        res = clf(text)
        return jsonify(label=res[0]["label"], score=float(res[0]["score"]))
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host=os.getenv("FLASK_HOST", "0.0.0.0"), port=int(os.getenv("FLASK_PORT", 6667)), debug=debug)
