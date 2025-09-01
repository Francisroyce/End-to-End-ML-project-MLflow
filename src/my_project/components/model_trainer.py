# components
import pandas as pd
import os
from my_project import logging
from sklearn.linear_model import ElasticNet
import joblib
from my_project.entity.config_entity import ModelTrainerConfig



class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train_model(self, x_train, y_train):
        model = ElasticNet(
            alpha=self.config.alpha,
            l1_ratio=self.config.l1_ratio,
            random_state=self.config.random_state,
        )
        model.fit(x_train, y_train)
        return model

    def initiate_model_trainer(self):
        logging.info("Loading training and test data")
        train_df = pd.read_csv(self.config.trained_data_path)
        test_df = pd.read_csv(self.config.test_data_path)

        target_column = self.config.target_column

        logging.info("Splitting training and test data into features and target")
        x_train = train_df.drop(columns=[target_column], axis=1)
        y_train = train_df[target_column]

        x_test = test_df.drop(columns=[target_column], axis=1)
        y_test = test_df[target_column]

        logging.info("Training the model")
        model = self.train_model(x_train, y_train)

        logging.info("Saving the trained model")
        joblib.dump(model, os.path.join(self.config.root_dir, self.config.model_name))

        logging.info("Model training completed")

        return model
