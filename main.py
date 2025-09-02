from my_project import logger
from my_project.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from my_project.pipeline.stage_02_datavalidation import DataValidationTrainingPipeline
from my_project.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline
from my_project.pipeline.stage_04_model_trainer import ModelTrainerPipeline
from my_project.pipeline.stage_05_model_evaluation import ModelEvaluation





logger.info("Starting the data ingestion pipeline...")

# ingestion stage
STAGE_NAME = "Data Ingestion Stage"

try:
    pipeline = DataIngestionTrainingPipeline()
    pipeline.main()
    logger.info(f"===== Stage {STAGE_NAME} completed =====")
except Exception as e:
    logger.exception(e)
    raise e

# validation stage
STAGE_NAME = "Data Validation Stage"
logger.info(f"===== Stage {STAGE_NAME} started =====")

try:
    pipeline = DataValidationTrainingPipeline()
    pipeline.main()
    logger.info(f"===== Stage {STAGE_NAME} completed =====")
except Exception as e:
    logger.exception(e)
    raise e

# transformation stage
STAGE_NAME = "Data Transformation Stage"
logger.info(f"===== Stage {STAGE_NAME} started =====")

try:
    pipeline = DataTransformationTrainingPipeline()
    pipeline.main()
    logger.info(f"===== Stage {STAGE_NAME} completed =====")
except Exception as e:
        logger.exception(e)
        raise e  

# model trainer stage
STAGE_NAME = "Model Trainer Stage"
try:
    logger.info(f"===== Stage {STAGE_NAME} started =====")
    pipeline = ModelTrainerPipeline()
    pipeline.main()
    logger.info(f"===== Stage {STAGE_NAME} completed =====\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e


import dagshub
# --- Initialize DagsHub and MLflow ---
dagshub.init(
    repo_owner='Francisroyce',
    repo_name='End-to-End-ML-project-MLflow',
    mlflow=True
)

# model evaluation stage
STAGE_NAME = "Model Evaluation Stage"
logger.info(f"===== Stage {STAGE_NAME} started =====")
try:
    pipeline = ModelEvaluation()
    pipeline.main()
    logger.info(f"===== Stage {STAGE_NAME} completed =====\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e


