from flask import Blueprint, current_app, request, jsonify
import time

radiation_bp = Blueprint("radiation", __name__)

# 1️⃣ Generate a simulated radiation measurement
@radiation_bp.route("/simulate", methods=["GET"])
def simulate():
    sample = current_app.simulator.generate_radiation_measurement()
    return jsonify(sample)

# 2️⃣ Evaluate a given radiation level with ShieldMate
@radiation_bp.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json(force=True)
    try:
        radiation_level = float(data.get("radiation_level"))
    except Exception:
        return jsonify({"error": "Invalid payload"}), 400

    result = current_app.shieldmate.evaluate(radiation_level)
    entry = {
        "timestamp": time.time(),
        "input": {"radiation_level": radiation_level},
        "result": result
    }
    current_app.radiation_history.append(entry)

    if result["status"] == "ALARM":
        current_app.actions_history.append({
            "timestamp": entry["timestamp"],
            "action_type": "RADIATION_ALARM",
            "description": result["action"]
        })

    return jsonify({
        "status": result["status"],
        "action": result["action"],
        "input": {"radiation_level": radiation_level}
    })

# 3️⃣ Get the last 100 radiation evaluations
@radiation_bp.route("/history", methods=["GET"])
def history():
    return jsonify({
        "count": len(current_app.radiation_history),
        "items": current_app.radiation_history[-100:]
    })

# 4️⃣ Simple exposure calculation (astronaut hours in space)
@radiation_bp.route("/exposure", methods=["GET"])
def get_radiation_exposure():
    hours_in_space = float(request.args.get('hours', 0))
    dose = hours_in_space * 0.05  # Sieverts per hour (placeholder)
    response = {
        "hours_in_space": hours_in_space,
        "radiation_dose_sieverts": dose
    }
    return jsonify(response)
