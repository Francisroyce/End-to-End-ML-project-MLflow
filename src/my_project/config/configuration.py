from my_project.constants import *
from my_project.utils.common import read_yaml, create_directories
from pathlib import Path
from my_project.entity.config_entity import DataIngestionConfig

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
