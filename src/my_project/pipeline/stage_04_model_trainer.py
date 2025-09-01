from my_project.config.configuration import ConfigurationManager
from my_project.components.model_trainer import ModelTrainer
from my_project import logger


STAGE_NAME = "Model Trainer Stage"
logger.info(f"===== Stage {STAGE_NAME} started =====")

class ModelTrainerPipeline:
    def __init__(self):
          pass
    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        print(model_trainer_config)
        
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.initiate_model_trainer()

if __name__ == "__main__":
    try:
        pipeline = ModelTrainerPipeline()
        pipeline.main()
        logger.info(f"===== Stage {STAGE_NAME} completed =====")
    except Exception as e:
        logger.exception(e)
        raise e