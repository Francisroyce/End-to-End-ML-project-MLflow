from my_project.config.configuration import ConfigurationManager
from my_project.components.data_ingestion import DataIngestion
from my_project import logger



# Data ingestion pipline

STAGE_NAME = "Data Ingestion Stage"
logger.info(f"===== Stage {STAGE_NAME} started =====")

class DataIngestionTrainingPipeline:
    def __init__(self):
          pass
    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.unzip_and_clean()

if __name__ == "__main__":
    try:
        pipeline = DataIngestionTrainingPipeline()
        pipeline.main()
        logger.info(f"===== Stage {STAGE_NAME} completed =====")
    except Exception as e:
        logger.exception(e)
        raise e