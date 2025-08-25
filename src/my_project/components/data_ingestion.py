import os
import urllib.request as request
import zipfile
from pathlib import Path
from urllib import request

from my_project import logger
from my_project.utils.common import get_size
from my_project.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self) -> None:
        """Downloads the dataset from the source URL if not already present."""
        local_path = Path(self.config.local_data_file)

        if not local_path.exists():
            logger.info(f"Downloading file from: [{self.config.source_URL}] to: [{local_path}]")
            try:
                request.urlretrieve(self.config.source_URL, local_path)
                logger.info(f"File downloaded successfully. Size: {get_size(local_path)} bytes")
            except Exception as e:
                logger.error(f"Failed to download file from {self.config.source_URL}: {e}")
                raise
        else:
            logger.info(f"File already exists at: [{local_path}] (size: {get_size(local_path)} bytes)")

    def unzip_and_clean(self) -> None:
        """Unzips the dataset and removes the original zip file."""
        local_path = Path(self.config.local_data_file)
        unzip_dir = Path(self.config.unzip_dir)

        logger.info(f"Unzipping file: [{local_path}] to dir: [{unzip_dir}]")
        try:
            with zipfile.ZipFile(local_path, "r") as zip_ref:
                zip_ref.extractall(unzip_dir)
            logger.info("Unzipping completed successfully.")
        except zipfile.BadZipFile as e:
            logger.error(f"Invalid zip file: {local_path} ({e})")
            raise
        except Exception as e:
            logger.error(f"Error while unzipping {local_path}: {e}")
            raise

        # Clean up zip file only after successful extraction
        try:
            local_path.unlink()
            logger.info(f"Deleted zip file: [{local_path}]")
        except Exception as e:
            logger.warning(f"Could not delete zip file {local_path}: {e}")
        logger.info(f"Data ingestion completed. Unzipped data available at: [{unzip_dir}]")
