from flask import Blueprint, current_app, request, jsonify
import time

fatigue_bp = Blueprint("fatigue", __name__)

# 1️⃣ Generate a simulated fatigue measurement
@fatigue_bp.route("/simulate", methods=["GET"])
def simulate():
    sample = current_app.simulator.generate_fatigue_measurement()
    return jsonify(sample)

# 2️⃣ Evaluate a given fatigue score with thresholds + cognitive prediction
@fatigue_bp.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json(force=True)
    try:
        fatigue_score = float(data.get("fatigue_score"))
    except Exception:
        return jsonify({"error": "Invalid payload"}), 400

    # Fatigue evaluation thresholds
    if fatigue_score > 80:
        status = "ALARM"
        action = "Astronaut requires rest immediately"
    elif fatigue_score > 50:
        status = "WARNING"
        action = "Astronaut should monitor fatigue levels"
    else:
        status = "OK"
        action = "Fatigue level normal"

    # Cognitive prediction using CogTwin
    cognitive_prediction = current_app.cogtwin.predict_cognitive_state(fatigue_score)

    entry = {
        "timestamp": time.time(),
        "input": {"fatigue_score": fatigue_score},
        "result": {"status": status, "action": action, "cognitive_prediction": cognitive_prediction}
    }
    current_app.fatigue_history.append(entry)

    if status == "ALARM":
        current_app.actions_history.append({
            "timestamp": entry["timestamp"],
            "action_type": "FATIGUE_ALARM",
            "description": action
        })

    return jsonify({
        "status": status,
        "action": action,
        "input": {"fatigue_score": fatigue_score},
        "cognitive_prediction": cognitive_prediction
    })

# 3️⃣ Get the last 100 fatigue evaluations
@fatigue_bp.route("/history", methods=["GET"])
def history():
    return jsonify({
        "count": len(current_app.fatigue_history),
        "items": current_app.fatigue_history[-100:]
    })
