# components of data transformation
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from my_project import logger

from my_project.entity.config_entity import DataTransformationConfig

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def initiate_data_transformation(self):
        logger.info("Data Transformation started")
        
        # Load data
        df = pd.read_csv(self.config.data_path)

        # Split into train and test
        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
        
        # Print or log shapes
        print("Train shape:", train_df.shape)
        print("Test shape:", test_df.shape)
        logger.info(f"Train shape: {train_df.shape}, Test shape: {test_df.shape}")
        
        # Define file paths
        train_path = os.path.join(self.config.root_dir, "train.csv")
        test_path = os.path.join(self.config.root_dir, "test.csv")

        # Save transformed data
        train_df.to_csv(train_path, index=False)
        test_df.to_csv(test_path, index=False)
        
        logger.info(f"Transformed data saved at {self.config.root_dir}")
        return train_path, test_path
