from my_project.config.configuration import ConfigurationManager
from my_project.components.data_validation import DataValidation
from my_project import logger

STAGE_NAME = "Data Validation Stage"
logger.info(f"===== Stage {STAGE_NAME} started =====")

class DataValidationTrainingPipeline:
    def __init__(self):
          pass
    def main(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_data()

if __name__ == "__main__":
    try:
        pipeline = DataValidationTrainingPipeline()
        pipeline.main()
        logger.info(f"===== Stage {STAGE_NAME} completed =====")
    except Exception as e:
        logger.exception(e)
        raise e