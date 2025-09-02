# components
import os
import json
import joblib
import pandas as pd
import numpy as np
import mlflow
import uuid
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from my_project import logger

from my_project.entity.config_entity import ModelEvaluationConfig
from my_project.config.configuration import ConfigurationManager

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig = None):
        # If config not passed, create it automatically from ConfigurationManager
        self.config = config or ConfigurationManager().get_model_evaluation_config()

        # --- Create a unique experiment name to avoid deleted experiment errors ---
        experiment_name = f"model_evaluation_{uuid.uuid4().hex[:6]}"
        mlflow.set_experiment(experiment_name)

        # Ensure directories exist
        os.makedirs(self.config.root_dir, exist_ok=True)
        os.makedirs(Path(self.config.metric_file_name).parent, exist_ok=True)

    def evaluate_model(self):
        """
        Evaluate trained model on test data, log metrics to MLflow (DagsHub-compatible),
        save metrics locally, and save the model locally (artifact folder).
        """
        try:
            # Load test data
            test_df = pd.read_csv(self.config.test_data_path)
            if self.config.target_column not in test_df.columns:
                raise KeyError(f"Target column '{self.config.target_column}' not found in test data")

            x_test = test_df.drop(columns=[self.config.target_column])
            y_test = test_df[self.config.target_column]

            # Load trained model
            if not Path(self.config.model_path).exists():
                raise FileNotFoundError(f"Model file not found at {self.config.model_path}")
            model = joblib.load(self.config.model_path)

            # Generate predictions
            y_pred = model.predict(x_test)

            # Calculate metrics
            metrics = {
                "MAE": mean_absolute_error(y_test, y_pred),
                "MSE": mean_squared_error(y_test, y_pred),
                "RMSE": np.sqrt(mean_squared_error(y_test, y_pred)),
                "R2_Score": r2_score(y_test, y_pred)
            }

            # --- LOG METRICS AND PARAMETERS TO MLflow ONLY ---
            with mlflow.start_run(run_name="model_evaluation"):
                if self.config.all_params:
                    for key, value in self.config.all_params.items():
                        mlflow.log_param(key, value)
                for key, value in metrics.items():
                    mlflow.log_metric(key, value)

            # --- SAVE METRICS LOCALLY ---
            with open(self.config.metric_file_name, "w") as f:
                json.dump(metrics, f, indent=4)

            # --- SAVE MODEL LOCALLY AS ARTIFACT ---
            artifact_dir = Path(self.config.root_dir) / "model_artifacts"
            artifact_dir.mkdir(exist_ok=True)
            joblib.dump(model, artifact_dir / "model.joblib")

            logger.info(f"Model evaluation metrics logged and saved: {metrics}")
            logger.info(f"Model saved locally at: {artifact_dir / 'model.joblib'}")
            return metrics

        except Exception as e:
            logger.error(f"Error during model evaluation: {e}")
            raise

    # --- Add main method for consistency ---
    def main(self):
        logger.info("Starting model evaluation...")
        self.evaluate_model()
        logger.info("Model evaluation completed.")
