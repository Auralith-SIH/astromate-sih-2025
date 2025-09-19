from flask import Flask
from routes.fatigue import fatigue_bp
from routes.radiation import radiation_bp
from routes.actions import actions_bp  # ← Add this line
from services.simulator import Simulator
from services.cogtwin import CogTwin
from services.shieldmate import ShieldMate
from utils.simple_logger import get_logger

def create_app():
    """Create and configure the Flask app (API-first design)."""
    app = Flask(__name__)

    # Setup logging
    logger = get_logger("astromate-backend")
    app.logger = logger
    app.logger.info("AstroMate backend created")

    # Initialize singletons
    app.simulator = Simulator(seed=42)
    app.cogtwin = CogTwin()
    app.shieldmate = ShieldMate()

    # In-memory histories (no DB yet)
    app.fatigue_history = []
    app.radiation_history = []
    app.actions_history = []

    # Register routes
    app.register_blueprint(fatigue_bp, url_prefix="/api/fatigue")
    app.register_blueprint(radiation_bp, url_prefix="/api/radiation")
    app.register_blueprint(actions_bp, url_prefix="/api/actions")  # ← Add this line

    # Health check endpoint
    @app.route("/", methods=["GET"])
    def health():
        return {"status": "ok", "service": "AstroMate backend (prototype)"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
