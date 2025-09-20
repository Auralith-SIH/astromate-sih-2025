import numpy as np
import tensorflow as tf
from pathlib import Path

class CogTwin:
    """ML wrapper for cognitive performance prediction based on fatigue score."""

    def __init__(self):
        # Path to your TensorFlow Lite model
        model_path = Path(__file__).parent.parent.parent / "ml-core/models/cogtwin_model.tflite"
        if not model_path.exists():
            raise FileNotFoundError(f"TFLite model not found at {model_path}")

        # Load TFLite model
        self.interpreter = tf.lite.Interpreter(model_path=str(model_path))
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def predict_cognitive_performance(self, fatigue_score: float) -> dict:
        """
        Given a fatigue score, predict cognitive performance using the TFLite model.
        Returns a dictionary with a rounded float value for compatibility with API.
        """
        input_data = np.array([[fatigue_score]], dtype=np.float32)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output_details[0]['index'])
        cognitive_performance = float(output[0][0])
        return {"cognitive_performance": round(cognitive_performance, 2)}
