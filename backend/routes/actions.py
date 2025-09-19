from flask import Blueprint, current_app, jsonify

actions_bp = Blueprint("actions", __name__)

@actions_bp.route("/history", methods=["GET"])
def actions_history():
    # Return last 100 actions for simplicity
    return jsonify({
        "count": len(current_app.actions_history),
        "items": current_app.actions_history[-100:]
    })
