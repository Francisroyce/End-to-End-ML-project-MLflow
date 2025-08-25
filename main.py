from my_project import logger
from my_project.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline

logger.info("Starting the data ingestion pipeline...")

STAGE_NAME = "Data Ingestion Stage"

try:
    pipeline = DataIngestionTrainingPipeline()
    pipeline.main()
    logger.info(f"===== Stage {STAGE_NAME} completed =====")
except Exception as e:
    logger.exception(e)
    raise e