"""
Data processing utilities for enterprise analytics dashboard.
Handles data loading, cleaning, validation, and transformation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import logging

from ..config.constants import DataTypes, ErrorMessages, SuccessMessages
from ..config.settings import config

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Enterprise-grade data processor for analytics applications.
    Handles data loading, cleaning, type detection, and validation.
    """
    
    def __init__(self):
        """Initialize data processor with empty state."""
        self.df: Optional[pd.DataFrame] = None
        self.data_types: Dict[str, str] = {}
        self.cleaning_log: List[str] = []
        
    def load_data(self, file_path: str, file_type: str = "csv") -> bool:
        """
        Load data from file with comprehensive error handling.
        
        Args:
            file_path: Path to the data file
            file_type: Type of file (csv, xlsx, json)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if file_type.lower() == "csv":
                self.df = pd.read_csv(file_path, encoding=config.DEFAULT_ENCODING)
            elif file_type.lower() == "xlsx":
                self.df = pd.read_excel(file_path)
            elif file_type.lower() == "json":
                self.df = pd.read_json(file_path)
            else:
                logger.error(f"Unsupported file type: {file_type}")
                return False
            
            if self.df.empty:
                logger.error(ErrorMessages.EMPTY_FILE.value)
                return False
            
            # Process and validate data
            self._clean_data()
            self._detect_data_types()
            self._validate_data()
            
            logger.info(SuccessMessages.DATA_LOADED.value.format(count=len(self.df)))
            return True
            
        except Exception as e:
            logger.error(ErrorMessages.LOAD_ERROR.value.format(error=str(e)))
            return False
    
    def _clean_data(self) -> None:
        """Clean and prepare data for analysis."""
        if self.df is None:
            return
        
        initial_rows = len(self.df)
        
        # Remove completely empty rows
        self.df = self.df.dropna(how='all')
        
        # Replace empty strings with NaN
        self.df = self.df.replace('', np.nan)
        
        # Remove duplicate rows
        self.df = self.df.drop_duplicates()
        
        # Clean column names
        self.df.columns = self.df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        final_rows = len(self.df)
        removed_rows = initial_rows - final_rows
        
        if removed_rows > 0:
            self.cleaning_log.append(f"Removed {removed_rows} empty/duplicate rows")
    
    def _detect_data_types(self) -> None:
        """Automatically detect and categorize data types."""
        if self.df is None:
            return
        
        for col in self.df.columns:
            # Try datetime detection with better validation
            if self._is_likely_datetime(col):
                try:
                    # Try to convert with more specific format detection
                    pd.to_datetime(self.df[col], errors='coerce')
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                    self.data_types[col] = DataTypes.DATETIME.value
                    continue
                except (ValueError, TypeError):
                    pass
            
            # Try numeric conversion
            try:
                if self.df[col].dtype == 'object':
                    numeric_series = pd.to_numeric(self.df[col], errors='coerce')
                    if not numeric_series.isna().all():
                        self.df[col] = numeric_series
                        self.data_types[col] = DataTypes.NUMERICAL.value
                        continue
            except (ValueError, TypeError):
                pass
            
            # Check for boolean
            if self.df[col].dtype == 'bool':
                self.data_types[col] = DataTypes.BOOLEAN.value
            else:
                # Default to categorical for object types
                self.data_types[col] = DataTypes.CATEGORICAL.value
    
    def _is_likely_datetime(self, column: str) -> bool:
        """
        Check if a column is likely to contain datetime data.
        
        Args:
            column: Column name to check
            
        Returns:
            bool: True if likely datetime, False otherwise
        """
        if self.df is None:
            return False
        
        # Check column name for date-related keywords
        date_keywords = ['date', 'time', 'created', 'updated', 'modified', 'timestamp']
        if any(keyword in column.lower() for keyword in date_keywords):
            return True
        
        # Check first few non-null values for date-like patterns
        sample_values = self.df[column].dropna().head(10)
        if len(sample_values) == 0:
            return False
        
        # Common date patterns
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
            r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
        ]
        
        import re
        for value in sample_values:
            value_str = str(value).strip()
            if any(re.match(pattern, value_str) for pattern in date_patterns):
                return True
        
        return False
    
    def _validate_data(self) -> None:
        """Validate data quality and log issues."""
        if self.df is None:
            return
        
        # Check for missing values
        missing_data = self.df.isnull().sum()
        for col, missing_count in missing_data.items():
            if missing_count > 0:
                percentage = (missing_count / len(self.df)) * 100
                self.cleaning_log.append(
                    f"Column '{col}': {missing_count} missing values ({percentage:.1f}%)"
                )
        
        # Check for outliers in numerical columns
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.df[(self.df[col] < Q1 - 1.5 * IQR) | 
                              (self.df[col] > Q3 + 1.5 * IQR)]
            
            if len(outliers) > 0:
                self.cleaning_log.append(
                    f"Column '{col}': {len(outliers)} potential outliers detected"
                )
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Generate comprehensive data summary.
        
        Returns:
            Dict containing data summary information
        """
        if self.df is None:
            return {}
        
        summary = {
            "total_records": len(self.df),
            "total_columns": len(self.df.columns),
            "data_types": self.data_types,
            "missing_data": self.df.isnull().sum().to_dict(),
            "cleaning_log": self.cleaning_log,
            "memory_usage": self.df.memory_usage(deep=True).sum() / 1024 / 1024,  # MB
            "column_info": {}
        }
        
        # Detailed column information
        for col in self.df.columns:
            col_info = {
                "data_type": self.data_types.get(col, "unknown"),
                "unique_values": self.df[col].nunique(),
                "missing_count": self.df[col].isnull().sum()
            }
            
            if self.data_types.get(col) == DataTypes.NUMERICAL.value:
                col_info.update({
                    "min": self.df[col].min(),
                    "max": self.df[col].max(),
                    "mean": self.df[col].mean(),
                    "median": self.df[col].median(),
                    "std": self.df[col].std()
                })
            elif self.data_types.get(col) == DataTypes.CATEGORICAL.value:
                col_info["top_values"] = self.df[col].value_counts().head(5).to_dict()
            
            summary["column_info"][col] = col_info
        
        return summary
    
    def get_filtered_data(self, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply filters to the dataset.
        
        Args:
            filters: Dictionary of column filters
            
        Returns:
            Filtered DataFrame
        """
        if self.df is None:
            return pd.DataFrame()
        
        filtered_df = self.df.copy()
        
        for col, filter_value in filters.items():
            if col in filtered_df.columns and filter_value:
                if isinstance(filter_value, list):
                    filtered_df = filtered_df[filtered_df[col].isin(filter_value)]
                elif isinstance(filter_value, dict):
                    # Range filter for numerical data
                    if 'min' in filter_value:
                        filtered_df = filtered_df[filtered_df[col] >= filter_value['min']]
                    if 'max' in filter_value:
                        filtered_df = filtered_df[filtered_df[col] <= filter_value['max']]
                else:
                    filtered_df = filtered_df[filtered_df[col] == filter_value]
        
        return filtered_df
    
    def get_sample_data(self, n: int = 1000) -> pd.DataFrame:
        """
        Get a sample of the data for performance optimization.
        
        Args:
            n: Number of records to sample
            
        Returns:
            Sampled DataFrame
        """
        if self.df is None:
            return pd.DataFrame()
        
        if len(self.df) <= n:
            return self.df
        
        return self.df.sample(n=n, random_state=42)
    
    def export_data(self, format: str = "csv") -> str:
        """
        Export data to specified format.
        
        Args:
            format: Export format (csv, xlsx, json)
            
        Returns:
            Exported data as string
        """
        if self.df is None:
            return ""
        
        if format.lower() == "csv":
            return self.df.to_csv(index=False)
        elif format.lower() == "json":
            return self.df.to_json(orient='records', indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")
