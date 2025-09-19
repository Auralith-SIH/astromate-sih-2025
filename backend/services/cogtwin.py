
import random

class CogTwin:
    """Simulates astronaut cognitive twin predictions."""

    def predict_cognitive_state(self, fatigue_score: float):
        # Example: simple linear relation
        cognitive_performance = max(0, 100 - fatigue_score + random.uniform(-5, 5))
        return {"cognitive_performance": round(cognitive_performance, 2)}
