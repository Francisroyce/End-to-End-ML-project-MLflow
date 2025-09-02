from my_project.config.configuration import ConfigurationManager
from my_project.components.model_evaluation import ModelEvaluation
from my_project import logger


# pipeline
import dagshub

# --- Initialize DagsHub and MLflow ---
dagshub.init(
    repo_owner='Francisroyce',
    repo_name='End-to-End-ML-project-MLflow',
    mlflow=True
)
try:
    config_manager = ConfigurationManager()
    model_evaluation_config = config_manager.get_model_evaluation_config()
    model_evaluation = ModelEvaluation(config=model_evaluation_config)
    metrics = model_evaluation.evaluate_model()
    print("Model evaluation metrics:", metrics)
except Exception as e:
    print(f"Error during model evaluation: {e}")