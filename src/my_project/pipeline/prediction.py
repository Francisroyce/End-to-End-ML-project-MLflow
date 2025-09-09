import joblib
import pandas as pd
import numpy as np

class PredictionPipeline:
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)

    def predict(self, input_data: pd.DataFrame) -> np.ndarray:
        predictions = self.model.predict(input_data)
        return predictions
