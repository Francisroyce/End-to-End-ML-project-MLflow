from my_project.config.configuration import ConfigurationManager
from my_project.components.model_trainer import ModelTrainer
from my_project import logger

STAGE_NAME = "Model Trainer Stage"
logger.info(f"===== Stage {STAGE_NAME} started =====")

class ModelTrainerPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            # Load all model trainer configurations
            config = ConfigurationManager()
            model_trainer_configs = config.get_model_trainer_configs()

            results = []

            for model_name, trainer_config in model_trainer_configs.items():
                try:
                    # Pass the ModelTrainerConfig object directly
                    model_trainer = ModelTrainer(config=trainer_config)
                    score = model_trainer.initiate_model_trainer()
                    results.append((model_name, score))
                except Exception as e:
                    logger.warning(f"⚠️ Skipping {model_name} due to error: {e}")
                    continue

            if results:
                # Print summary
                print("\n📊 Model Results:")
                for name, score in results:
                    print(f"{name:15} -> {score:.4f}")

                # Pick best model
                best_model, best_score = max(results, key=lambda x: x[1])
                print(f"\n✅ Best model: {best_model} with score {best_score:.4f}")
            else:
                print("\n❌ No models were successfully trained. Check configuration and errors above.")

            logger.info(f"===== Stage {STAGE_NAME} completed =====")

        except Exception as e:
            logger.exception(f"Error in {STAGE_NAME}: {e}")
            raise e


if __name__ == "__main__":
    pipeline = ModelTrainerPipeline()
    pipeline.main()
