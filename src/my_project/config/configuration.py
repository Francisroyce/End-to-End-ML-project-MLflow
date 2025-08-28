from my_project.constants import *
from my_project.utils.common import read_yaml, create_directories
from pathlib import Path
from my_project.entity.config_entity import (DataIngestionConfig, DataValidationConfig,
                                              DataTransformationConfig)
                                         


# configuration manager
class ConfigurationManager:
    def __init__(
        self,
        config_filepath: Path = CONFIG_FILE_PATH,
        params_filepath: Path = PARAMS_FILE_PATH,
        schema_filepath: Path = SCHEMA_FILE_PATH,
    ):
        # Load configs
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        # Ensure artifacts root exists
        create_directories(Path(self.config.artifacts_root))
        
# data ingestion config
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        cfg = self.config.data_ingestion

        root_dir = Path(cfg.root_dir)
        create_directories([root_dir])

        return DataIngestionConfig(
            root_dir=root_dir,
            source_URL=cfg.source_URL,
            local_data_file=Path(cfg.local_data_file),
            unzip_dir=Path(cfg.unzip_dir),
        )

        
    # data validation dir
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation

        data_validation_config = DataValidationConfig(
            root_dir=Path(config.root_dir),
            status_file=Path(config.root_dir) / config.status_file,
            unzip_data_dir=Path(config.unzip_data_dir),
            report_file=Path(config.root_dir) / config.report_file,
            all_schema=Path(SCHEMA_FILE_PATH),  # 🔥 pass the path, not the Box/dict
        )
        return data_validation_config


    # data transformation config
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        create_directories([Path(config.root_dir)])
        data_transformation_config = DataTransformationConfig(
            root_dir=Path(config.root_dir),
            data_path=Path(config.data_path)
        )
        return data_transformation_config