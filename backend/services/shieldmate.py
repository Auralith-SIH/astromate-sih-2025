class ShieldMate:
    """Evaluates radiation exposure and recommends actions."""

    def __init__(self):
        # Define thresholds (example)
        self.threshold_warning = 2.0  # mSv/h
        self.threshold_alarm = 4.0    # mSv/h

    def evaluate(self, radiation_level: float):
        if radiation_level >= self.threshold_alarm:
            return {"status": "ALARM", "action": "Evacuate immediately / Shield required"}
        elif radiation_level >= self.threshold_warning:
            return {"status": "WARNING", "action": "Limit exposure / Monitor closely"}
        else:
            return {"status": "OK", "action": "Radiation level safe"}
