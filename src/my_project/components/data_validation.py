# components
import os
import pandas as pd
import yaml
import numpy as np
from pathlib import Path
from typing import Dict, Any
from my_project import logger

from my_project.entity.config_entity import DataValidationConfig


DTYPE_MAPPING = {
    "int": ["int64", "int32"],
    "float": ["float64", "float32"],
    "string": ["object", "string"]
}


class DataValidation:
    """Validates ingested data against schema, generates report, and can remove outliers."""

    def __init__(self, config: DataValidationConfig):
        self.config = config

        # Load schema
        with open(self.config.all_schema, "r") as f:
            self.schema: Dict[str, Any] = yaml.safe_load(f)

    def _detect_outliers(self, df: pd.DataFrame, column: str):
        """Return dict of outliers {index: value} and list of indices using IQR method."""
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outlier_mask = (df[column] < lower_bound) | (df[column] > upper_bound)
        outliers = df.loc[outlier_mask, column]
        return outliers.to_dict(), outliers.index.tolist()

    def validate_data(self, remove_outliers: bool = True) -> bool:
        report = {"status": "success", "errors": [], "warnings": [], "outliers": {}}

        try:
            logger.info("Starting data validation")

            # Check file exists
            if not self.config.unzip_data_dir.exists():
                raise FileNotFoundError(f"Data file not found: {self.config.unzip_data_dir}")

            df = pd.read_csv(self.config.unzip_data_dir)

            # Validate columns
            expected_columns = set(self.schema.get("columns", {}).keys())
            actual_columns = set(df.columns)
            if expected_columns != actual_columns:
                error = f"Column mismatch. Expected: {expected_columns}, Found: {actual_columns}"
                report["errors"].append(error)

            # Validate data types
            for column, expected_type in self.schema.get("columns", {}).items():
                if column in df.columns:
                    actual_type = str(df[column].dtype)
                    if actual_type not in DTYPE_MAPPING.get(expected_type, [expected_type]):
                        error = f"Type mismatch for '{column}': expected {expected_type}, found {actual_type}"
                        report["errors"].append(error)

            # Missing values check
            missing = df.isnull().sum()
            missing = missing[missing > 0]
            if not missing.empty:
                for col, count in missing.items():
                    report["errors"].append(f"Missing values in column '{col}': {count}")

            # Outlier detection (IQR method, per column)
            all_outlier_indices = set()
            for column in df.select_dtypes(include=["float64", "int64"]).columns:
                outlier_dict, outlier_indices = self._detect_outliers(df, column)
                if outlier_dict:
                    report["warnings"].append(
                        f"Column '{column}' has {len(outlier_dict)} potential outliers"
                    )
                    report["outliers"][column] = outlier_dict
                    all_outlier_indices.update(outlier_indices)

            # Remove outliers if requested
            if remove_outliers and all_outlier_indices:
                logger.info(f"Removing {len(all_outlier_indices)} outlier rows")
                df = df.drop(index=all_outlier_indices)

            # Finalize report
            if report["errors"]:
                report["status"] = "failed"
                logger.error(f"Validation failed with errors: {report['errors']}")
            else:
                logger.info("Data validation completed successfully")

            # Save the cleaned dataset inside data_validation artifacts
            self.config.root_dir.mkdir(parents=True, exist_ok=True)
            cleaned_file = self.config.root_dir / "cleaned_data.csv"
            df.to_csv(cleaned_file, index=False)
            logger.info(f"Cleaned data saved to {cleaned_file}")

            # Add cleaned file path to report
            report["cleaned_file"] = str(cleaned_file)

        except Exception as e:
            logger.exception("Unexpected error during validation")
            report["status"] = "failed"
            report["errors"].append(str(e))

        # Save results
        self.config.root_dir.mkdir(parents=True, exist_ok=True)

        # Status text
        self.config.status_file.write_text(report["status"])

        # Detailed YAML report
        with open(self.config.report_file, "w") as f:
            yaml.dump(report, f, sort_keys=False)

        return report["status"] == "success"
