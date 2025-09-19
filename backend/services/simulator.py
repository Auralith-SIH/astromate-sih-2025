import random

class Simulator:
    """Simulates astronaut health metrics like fatigue and radiation exposure."""

    def __init__(self, seed=None):
        self.seed = seed
        if seed is not None:
            random.seed(seed)

    def generate_fatigue_measurement(self):
        """Return a simulated fatigue score (0-100)."""
        return {"fatigue_score": round(random.uniform(0, 100), 2)}

    def generate_radiation_measurement(self):
        """Return a simulated radiation measurement in mSv/h."""
        return {"radiation_level": round(random.uniform(0, 5), 3)}  # Example in mSv/h
