"""
Flask entry point — AI microservice for Tool-27 Audit Committee Reporting.
Runs on port 5000. All routes are registered here as blueprints.
"""

import logging
import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Logging — structured format for easier debugging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------
app = Flask(__name__)


# ---------------------------------------------------------------------------
# Register blueprints
# Add each new route file here as you build it day by day.
# ---------------------------------------------------------------------------

# Day 3 — /categorise
from routes.categorise import categorise_bp
app.register_blueprint(categorise_bp)

# Day 5 — /query (RAG)
from routes.query import query_bp          # remove the #
app.register_blueprint(query_bp)           # remove the #

# Day 6 — /generate-report (async)
# from routes.generate_report import generate_report_bp
# app.register_blueprint(generate_report_bp)

# Day 7 — /health
from routes.health import health_bp
app.register_blueprint(health_bp)



# ---------------------------------------------------------------------------
# Global error handlers
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_ENV", "production") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)