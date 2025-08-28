# entity

from dataclasses import dataclass
from pathlib import Path

# data ingestion related configuration
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path
    

# data validation related configuration
@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    status_file: Path
    unzip_data_dir: Path
    report_file: Path
    all_schema: Path 


# data transformation related configuration
@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path