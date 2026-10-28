"""
Hindustan Unilever Limited (HUL) - Executive Decision Intelligence Engine
Flask Application & REST API Server (Port 5012)
Project - 12: Executive Decision Intelligence

Serves:
- Executive Glassmorphic FMCG Decision Intelligence Dashboard
- Real-Time Counterfactual What-If Scenario Stress Simulator
- Grounded LLM Decision Agent & Natural Language Query Terminal
- Vital Drivers Attribution vs Departmental Vanity Metrics Engine
- 5 Prescriptive Board Strategic Protocols (Alpha to Epsilon)
- High-Resolution Publication-Grade PDF Report Generator & Direct Download
"""

import os
import sys
import json
from flask import Flask, render_template, jsonify, request, send_file

# Add project root to path
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

os.environ["LOKY_MAX_CPU_COUNT"] = "4"

from data.generate_kpi_dataset import generate_hul_executive_dataset
from models.causal_attribution_engine import CausalAttributionEngine
from models.scenario_simulator import ScenarioSimulator
from models.llm_decision_agent import LLMDecisionAgent
from report.generate_pdf_report import build_pdf_report

app = Flask(__name__, static_folder="static", template_folder="templates")

DATA_DIR = os.path.join(base_dir, "data")
CSV_PATH = os.path.join(DATA_DIR, "hul_executive_kpi_dataset.csv")
REPORT_PATH = os.path.join(base_dir, "report", "HUL_Executive_Decision_Intelligence_Report.pdf")

# Step 1: Ensure dataset exists
if not os.path.exists(CSV_PATH):
    print("[Flask-Init] Synthesizing HUL enterprise KPI telemetry records...")
    generate_hul_executive_dataset(CSV_PATH)

# Step 2: Initialize AI diagnostic models & engines
print("[Flask-Init] Loading Causal Attribution Engine and training models...")
attribution_engine = CausalAttributionEngine()
attribution_engine.train_and_analyze(CSV_PATH)

simulator = ScenarioSimulator()
llm_agent = LLMDecisionAgent(attribution_engine)

# Step 3: Ensure PDF Report exists
if not os.path.exists(REPORT_PATH):
    print("[Flask-Init] Compiling initial executive PDF deliverable...")
    build_pdf_report(CSV_PATH, REPORT_PATH)

print("[Flask-Init] Decision Intelligence server initialized successfully!")


# --------------------------------------------------------------------------
# REST API Endpoints & Routes
# --------------------------------------------------------------------------

@app.route("/")
def index():
    """Serves the main executive decision intelligence dashboard."""
    return render_template("index.html")

@app.route("/api/overview", methods=["GET"])
def get_overview():
    """Returns overview of drivers, vanity audit, and model metrics."""
    return jsonify({
        "model_metrics": attribution_engine.model_metrics,
        "driver_rankings": attribution_engine.driver_rankings[:8],
        "elasticities": attribution_engine.elasticities,
        "vanity_audit": attribution_engine.vanity_metrics_audit,
        "transmission_graph": attribution_engine.transmission_graph
    })

@app.route("/api/simulate", methods=["POST"])
def run_simulation():
    """Calculates counterfactual financial outcomes from operational lever adjustments."""
    data = request.get_json() or {}
    results = simulator.simulate(data)
    return jsonify(results)

@app.route("/api/agent_query", methods=["POST"])
def agent_query():
    """Processes natural language inquiries via the LLM Decision Agent."""
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    response = llm_agent.answer_executive_query(query)
    return jsonify(response)

@app.route("/api/protocols", methods=["GET"])
def get_protocols():
    """Returns the 5 prescriptive board strategic protocols."""
    protocols = llm_agent.get_prescriptive_protocols()
    return jsonify(protocols)

@app.route("/api/download_report", methods=["GET"])
def download_report():
    """Serves the publication-grade PDF report directly as an attachment."""
    if not os.path.exists(REPORT_PATH):
        build_pdf_report(CSV_PATH, REPORT_PATH)
    
    return send_file(
        REPORT_PATH,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="HUL_Executive_Decision_Intelligence_Report.pdf"
    )

@app.route("/api/health", methods=["GET"])
def health_check():
    """API health probe."""
    return jsonify({
        "status": "healthy",
        "system": "HUL Executive Decision Intelligence Engine",
        "port": 5012,
        "dataset_records": attribution_engine.model_metrics.get("sample_size", 720)
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5012))
    print(f"\n[HUL Decision Intelligence Engine] Dashboard active on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)

