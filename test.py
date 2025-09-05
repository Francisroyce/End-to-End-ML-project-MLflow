from my_project import logger
from my_project.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from my_project.pipeline.stage_02_datavalidation import DataValidationTrainingPipeline
from my_project.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline
from my_project.pipeline.stage_04_model_trainer import ModelTrainerPipeline
from my_project.pipeline.stage_05_model_evaluation import ModelEvaluation

import dagshub

# --- Initialize DagsHub and MLflow ---
dagshub.init(
    repo_owner='Francisroyce',
    repo_name='End-to-End-ML-project-MLflow',
    mlflow=True
)

logger.info("Starting the full data pipeline...")


def run_stage(stage_name, pipeline_class):
    """Helper to run a pipeline stage with logging and error handling."""
    logger.info(f"===== Stage {stage_name} started =====")
    try:
        pipeline = pipeline_class()
        pipeline.main()
        logger.info(f"===== Stage {stage_name} completed =====\n\nx==========x")
    except Exception as e:
        logger.exception(f"Error in {stage_name}: {e}")
        raise e


# List of pipeline stages
stages = [
    ("Data Ingestion Stage", DataIngestionTrainingPipeline),
    ("Data Validation Stage", DataValidationTrainingPipeline),
    ("Data Transformation Stage", DataTransformationTrainingPipeline),
    ("Model Trainer Stage", ModelTrainerPipeline),
    ("Model Evaluation Stage", ModelEvaluation),
]

# Run all stages
for stage_name, pipeline_class in stages:
    run_stage(stage_name, pipeline_class)

logger.info("All pipeline stages completed successfully!")
