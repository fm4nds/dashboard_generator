"""
Helper utilities for enterprise analytics dashboard.
Provides common utility functions for data formatting, analysis, and validation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class DashboardHelpers:
    """
    Helper class with utility functions for dashboard operations.
    Provides static methods for common data processing tasks.
    """
    
    @staticmethod
    def format_number(value: float, decimals: int = 2) -> str:
        """
        Format number with appropriate suffixes (K, M, B).
        
        Args:
            value: Number to format
            decimals: Number of decimal places
            
        Returns:
            Formatted string with suffix
        """
        if value >= 1e9:
            return f"{value/1e9:.{decimals}f}B"
        elif value >= 1e6:
            return f"{value/1e6:.{decimals}f}M"
        elif value >= 1e3:
            return f"{value/1e3:.{decimals}f}K"
        else:
            return f"{value:.{decimals}f}"
    
    @staticmethod
    def calculate_percentage_change(current: float, previous: float) -> float:
        """
        Calculate percentage change between two values.
        
        Args:
            current: Current value
            previous: Previous value
            
        Returns:
            Percentage change value
        """
        if previous == 0:
            return 0.0
        return ((current - previous) / previous) * 100
    
    @staticmethod
    def get_color_for_percentage_change(change: float) -> str:
        """
        Get color based on percentage change direction.
        
        Args:
            change: Percentage change value
            
        Returns:
            Hex color string
        """
        if change > 0:
            return "#107C10"  # Green for positive
        elif change < 0:
            return "#D13438"  # Red for negative
        else:
            return "#605E5C"  # Gray for no change
    
    @staticmethod
    def generate_sample_data(rows: int = 1000) -> pd.DataFrame:
        """
        Generate sample data for testing and demonstration.
        
        Args:
            rows: Number of rows to generate
            
        Returns:
            DataFrame with sample business data
        """
        np.random.seed(42)
        
        # Generate sample data
        data = {
            'date': pd.date_range(start='2023-01-01', periods=rows, freq='D'),
            'category': np.random.choice(['A', 'B', 'C', 'D'], rows),
            'region': np.random.choice(['North', 'South', 'East', 'West'], rows),
            'sales': np.random.normal(1000, 200, rows),
            'profit': np.random.normal(200, 50, rows),
            'quantity': np.random.poisson(50, rows),
            'customer_satisfaction': np.random.uniform(1, 5, rows)
        }
        
        return pd.DataFrame(data)
    
    @staticmethod
    def detect_outliers(series: pd.Series, method: str = 'iqr') -> pd.Series:
        """
        Detect outliers in a series using different methods.
        
        Args:
            series: Pandas series to analyze
            method: Method to use ('iqr' or 'zscore')
            
        Returns:
            Boolean series indicating outlier positions
        """
        if method == 'iqr':
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return (series < lower_bound) | (series > upper_bound)
        
        elif method == 'zscore':
            z_scores = np.abs((series - series.mean()) / series.std())
            return z_scores > 3
        
        else:
            raise ValueError(f"Unknown method: {method}")
    
    @staticmethod
    def calculate_statistics(series: pd.Series) -> Dict[str, float]:
        """
        Calculate comprehensive statistics for a series.
        
        Args:
            series: Pandas series to analyze
            
        Returns:
            Dictionary with statistical measures
        """
        stats = {
            'count': len(series),
            'mean': series.mean(),
            'median': series.median(),
            'std': series.std(),
            'min': series.min(),
            'max': series.max(),
            'q25': series.quantile(0.25),
            'q75': series.quantile(0.75),
            'skewness': series.skew(),
            'kurtosis': series.kurtosis()
        }
        
        # Add outlier information
        outliers = DashboardHelpers.detect_outliers(series)
        stats['outliers_count'] = outliers.sum()
        stats['outliers_percentage'] = (outliers.sum() / len(series)) * 100
        
        return stats
    
    @staticmethod
    def create_time_series_features(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
        """
        Create time series features from date column.
        
        Args:
            df: DataFrame with date column
            date_column: Name of the date column
            
        Returns:
            DataFrame with additional time-based features
        """
        df_copy = df.copy()
        
        # Ensure date column is datetime
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
        
        # Extract time features
        df_copy[f'{date_column}_year'] = df_copy[date_column].dt.year
        df_copy[f'{date_column}_month'] = df_copy[date_column].dt.month
        df_copy[f'{date_column}_day'] = df_copy[date_column].dt.day
        df_copy[f'{date_column}_weekday'] = df_copy[date_column].dt.dayofweek
        df_copy[f'{date_column}_quarter'] = df_copy[date_column].dt.quarter
        df_copy[f'{date_column}_week'] = df_copy[date_column].dt.isocalendar().week
        
        return df_copy
    
    @staticmethod
    def calculate_rolling_statistics(series: pd.Series, window: int = 7) -> Dict[str, pd.Series]:
        """
        Calculate rolling statistics for time series data.
        
        Args:
            series: Pandas series
            window: Rolling window size
            
        Returns:
            Dictionary with rolling statistical measures
        """
        return {
            'rolling_mean': series.rolling(window=window).mean(),
            'rolling_std': series.rolling(window=window).std(),
            'rolling_min': series.rolling(window=window).min(),
            'rolling_max': series.rolling(window=window).max(),
            'rolling_median': series.rolling(window=window).median()
        }
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """
        Format duration in seconds to human-readable format.
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted duration string
        """
        if seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    
    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """
        Get file size in megabytes.
        
        Args:
            file_path: Path to file
            
        Returns:
            File size in MB
        """
        import os
        return os.path.getsize(file_path) / (1024 * 1024)
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Simple email validation using regex.
        
        Args:
            email: Email string to validate
            
        Returns:
            True if valid email format
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename for safe file operations.
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename safe for file system
        """
        import re
        # Remove or replace invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip('. ')
        return sanitized
