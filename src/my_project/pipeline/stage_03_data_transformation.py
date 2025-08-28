from my_project.config.configuration import ConfigurationManager
from my_project.components.data_transfromation import DataTransformation
from my_project import logger


STAGE_NAME = "Data Transformation Stage"
logger.info(f"===== Stage {STAGE_NAME} started =====")

class DataTransformationTrainingPipeline:
    def __init__(self):
          pass
    def main(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        print(data_transformation_config)
        
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.initiate_data_transformation()

if __name__ == "__main__":
    try:
        pipeline = DataTransformationTrainingPipeline()
        pipeline.main()
        logger.info(f"===== Stage {STAGE_NAME} completed =====")
    except Exception as e:
        logger.exception(e)
        raise e  