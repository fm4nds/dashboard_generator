"""
Data validation utilities for enterprise analytics dashboard.
Ensures data quality, integrity, and consistency across the application.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import logging
import os

from ..config.constants import DataTypes, ErrorMessages
from ..config.settings import config

logger = logging.getLogger(__name__)


class DataValidator:
    """
    Data validation class for ensuring data quality and integrity.
    Provides comprehensive validation for files, DataFrames, and configurations.
    """
    
    def __init__(self):
        """Initialize validator with empty error and warning lists."""
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []
    
    def validate_csv_file(self, file_path: str) -> bool:
        """
        Validate CSV file before processing.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Check file size
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            if file_size > config.MAX_FILE_SIZE_MB:
                self.validation_errors.append(
                    ErrorMessages.FILE_TOO_LARGE.value.format(max_size=config.MAX_FILE_SIZE_MB)
                )
                return False
            
            # Try to read CSV
            df = pd.read_csv(file_path, nrows=5)  # Read first 5 rows for validation
            if df.empty:
                self.validation_errors.append(ErrorMessages.EMPTY_FILE.value)
                return False
            
            return True
            
        except Exception as e:
            self.validation_errors.append(f"File validation error: {str(e)}")
            return False
    
    def validate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate DataFrame for quality issues.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dictionary with validation results and quality score
        """
        validation_results = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "quality_score": 100.0
        }
        
        # Check for empty DataFrame
        if df.empty:
            validation_results["is_valid"] = False
            validation_results["errors"].append("DataFrame is empty")
            validation_results["quality_score"] = 0.0
            return validation_results
        
        # Check for missing values
        missing_data = df.isnull().sum()
        total_cells = len(df) * len(df.columns)
        missing_percentage = (missing_data.sum() / total_cells) * 100
        
        if missing_percentage > 50:
            validation_results["is_valid"] = False
            validation_results["errors"].append(f"Too many missing values: {missing_percentage:.1f}%")
            validation_results["quality_score"] -= 30
        elif missing_percentage > 20:
            validation_results["warnings"].append(f"High missing values: {missing_percentage:.1f}%")
            validation_results["quality_score"] -= 10
        
        # Check for duplicate rows
        duplicate_count = df.duplicated().sum()
        duplicate_percentage = (duplicate_count / len(df)) * 100
        
        if duplicate_percentage > 50:
            validation_results["is_valid"] = False
            validation_results["errors"].append(f"Too many duplicates: {duplicate_percentage:.1f}%")
            validation_results["quality_score"] -= 20
        elif duplicate_percentage > 10:
            validation_results["warnings"].append(f"High duplicate rate: {duplicate_percentage:.1f}%")
            validation_results["quality_score"] -= 5
        
        # Check for constant columns
        constant_columns = []
        for col in df.columns:
            if df[col].nunique() == 1:
                constant_columns.append(col)
        
        if constant_columns:
            validation_results["warnings"].append(f"Constant columns detected: {', '.join(constant_columns)}")
            validation_results["quality_score"] -= 5
        
        # Check for data type consistency
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check for mixed data types in object columns
                try:
                    pd.to_numeric(df[col], errors='raise')
                except (ValueError, TypeError):
                    # This is expected for categorical data
                    pass
        
        # Ensure quality score is not negative
        validation_results["quality_score"] = max(0, validation_results["quality_score"])
        
        return validation_results
    
    def validate_chart_config(self, config: Dict[str, Any], available_columns: List[str]) -> bool:
        """
        Validate chart configuration parameters.
        
        Args:
            config: Chart configuration dictionary
            available_columns: List of available columns
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_fields = ['column', 'chart_type', 'title']
        
        for field in required_fields:
            if field not in config:
                self.validation_errors.append(f"Missing required field: {field}")
                return False
        
        if config['column'] not in available_columns:
            self.validation_errors.append(
                ErrorMessages.INVALID_COLUMN.value.format(column=config['column'])
            )
            return False
        
        if config['chart_type'] not in ['pie', 'bar', 'line', 'histogram', 'scatter', 'treemap', 'funnel']:
            self.validation_errors.append(f"Invalid chart type: {config['chart_type']}")
            return False
        
        return True
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get summary of validation results."""
        return {
            "total_errors": len(self.validation_errors),
            "total_warnings": len(self.validation_warnings),
            "errors": self.validation_errors,
            "warnings": self.validation_warnings
        }
    
    def clear_validation_results(self) -> None:
        """Clear validation results."""
        self.validation_errors.clear()
        self.validation_warnings.clear()
