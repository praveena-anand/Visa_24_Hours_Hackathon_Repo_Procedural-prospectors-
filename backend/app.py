from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

from agents.report_understanding import understand_report
from agents.anomaly_detection import detect_anomalies
from agents.root_cause_reasoning import explain_root_cause
from agents.action_recommendation import recommend_actions

from rag.embed import embed_documents
from rag.retrieve import retrieve_context

app = Flask(__name__, template_folder="../frontend/templates")
CORS(app)

# Cache structure:
# {
#   "authorization": [summary1, summary2],
#   "settlement": [summary1, summary2]
# }
CACHE = {
    "authorization": [],
    "settlement": []
}

# -------------------- ROUTES --------------------

@app.route("/")
def home():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    report_type = request.form["type"]  # authorization | settlement
    file = request.files["file"]

    save_path = f"data/{report_type}/{file.filename}"
    file.save(save_path)

    # Agent 1: Understand report
    summary = understand_report(save_path)

    # Agent 2: Detect anomalies
    anomalies = detect_anomalies(summary)

    # Store summary by report type
    CACHE[report_type].append(summary)

    # RAG: embed with report-type context
    embed_documents({
        "report_type": report_type,
        "summary": summary
    })

    return jsonify({
        "message": f"{report_type.capitalize()} report processed",
        "anomalies": anomalies
    })


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/chat", methods=["POST"])
def chat():
    query = request.json["query"]

    # Retrieve cross-report context
    context = retrieve_context(query)

    # Agent 3: Root-cause reasoning (cross-report)
    explanation = explain_root_cause(query, context)

    # Agent 4: Action recommendations
    actions = recommend_actions(explanation)

    return jsonify({
        "answer": explanation,
        "actions": actions
    })


# -------------------- CHART DATA API --------------------

@app.route("/chart-data", methods=["GET"])
def chart_data():
    """
    Provides simple aggregated metrics for charts.
    Keeps frontend dumb and backend intelligent.
    """

    auth_declines = []
    settlement_delays = []

    for s in CACHE["authorization"]:
        stats = s.get("stats", {})
        if "declined_txns" in stats:
            auth_declines.append(stats["declined_txns"].get("mean", 0))

    for s in CACHE["settlement"]:
        stats = s.get("stats", {})
        if "delay_hours" in stats:
            settlement_delays.append(stats["delay_hours"].get("mean", 0))

    return jsonify({
        "authorization": {
            "avg_declines": round(sum(auth_declines) / len(auth_declines), 2)
            if auth_declines else 0
        },
        "settlement": {
            "avg_delay_hours": round(sum(settlement_delays) / len(settlement_delays), 2)
            if settlement_delays else 0
        }
    })


# -------------------- MAIN --------------------

if __name__ == "__main__":
    app.run(debug=True)
