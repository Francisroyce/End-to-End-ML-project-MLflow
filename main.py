from my_project import logger
from my_project.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from my_project.pipeline.stage_02_datavalidation import DataValidationTrainingPipeline

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