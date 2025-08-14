"""
KPI calculation module for dashboard generator.
Provides comprehensive metrics generation and statistical analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging

from ..config.constants import DataTypes, ThemeColors
from ..utils.data_processor import DataProcessor

logger = logging.getLogger(__name__)


class KPICalculator:
    """
    Comprehensive KPI calculator for data analysis.
    Generates core metrics, statistical analysis, and performance indicators.
    """
    
    def __init__(self, data_processor: DataProcessor):
        """Initialize KPI calculator with data processor."""
        self.data_processor = data_processor
        self.kpis_cache: Dict[str, Any] = {}
        
    def calculate_all_kpis(self) -> Dict[str, Any]:
        """Calculate all KPIs across different data categories."""
        if self.data_processor.df is None:
            return {}
        
        kpis = {}
        
        # Core metrics
        kpis.update(self._calculate_core_metrics())
        
        # Numerical analysis
        kpis.update(self._calculate_numerical_kpis())
        
        # Temporal analysis
        kpis.update(self._calculate_temporal_kpis())
        
        # Categorical analysis
        kpis.update(self._calculate_categorical_kpis())
        
        # Quality metrics
        kpis.update(self._calculate_quality_metrics())
        
        # Performance metrics
        kpis.update(self._calculate_performance_metrics())
        
        # Cache results
        self.kpis_cache = kpis
        
        return kpis
    
    def _calculate_core_metrics(self) -> Dict[str, Any]:
        """Calculate basic dataset metrics."""
        df = self.data_processor.df
        
        return {
            "total_records": len(df),
            "total_columns": len(df.columns),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
            "data_completeness": (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        }
    
    def _calculate_numerical_kpis(self) -> Dict[str, Any]:
        """Calculate statistical KPIs for numerical columns."""
        df = self.data_processor.df
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        kpis = {}
        
        for col in numerical_cols:
            col_data = df[col].dropna()
            if len(col_data) == 0:
                continue
                
            kpis[f"{col}_sum"] = col_data.sum()
            kpis[f"{col}_avg"] = col_data.mean()
            kpis[f"{col}_median"] = col_data.median()
            kpis[f"{col}_max"] = col_data.max()
            kpis[f"{col}_min"] = col_data.min()
            kpis[f"{col}_std"] = col_data.std()
            kpis[f"{col}_variance"] = col_data.var()
            kpis[f"{col}_skewness"] = col_data.skew()
            kpis[f"{col}_kurtosis"] = col_data.kurtosis()
            
            # Percentiles
            kpis[f"{col}_p25"] = col_data.quantile(0.25)
            kpis[f"{col}_p75"] = col_data.quantile(0.75)
            kpis[f"{col}_iqr"] = kpis[f"{col}_p75"] - kpis[f"{col}_p25"]
            
            # Outlier detection
            lower_bound = kpis[f"{col}_p25"] - 1.5 * kpis[f"{col}_iqr"]
            upper_bound = kpis[f"{col}_p75"] + 1.5 * kpis[f"{col}_iqr"]
            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
            kpis[f"{col}_outliers_count"] = len(outliers)
            kpis[f"{col}_outliers_percentage"] = (len(outliers) / len(col_data)) * 100
        
        return kpis
    
    def _calculate_temporal_kpis(self) -> Dict[str, Any]:
        """Calculate time-based KPIs for datetime columns."""
        df = self.data_processor.df
        datetime_cols = df.select_dtypes(include=['datetime64']).columns
        kpis = {}
        
        for col in datetime_cols:
            col_data = df[col].dropna()
            if len(col_data) == 0:
                continue
                
            kpis[f"{col}_earliest"] = col_data.min()
            kpis[f"{col}_latest"] = col_data.max()
            kpis[f"{col}_date_range_days"] = (col_data.max() - col_data.min()).days
            
            # Time-based patterns
            kpis[f"{col}_weekday_distribution"] = col_data.dt.dayofweek.value_counts().to_dict()
            kpis[f"{col}_month_distribution"] = col_data.dt.month.value_counts().to_dict()
            kpis[f"{col}_year_distribution"] = col_data.dt.year.value_counts().to_dict()
            
            # Seasonal analysis
            kpis[f"{col}_quarterly_distribution"] = col_data.dt.quarter.value_counts().to_dict()
            
            # Time gaps analysis
            sorted_dates = col_data.sort_values()
            time_gaps = sorted_dates.diff().dropna()
            if len(time_gaps) > 0:
                kpis[f"{col}_avg_time_gap_hours"] = time_gaps.mean().total_seconds() / 3600
                kpis[f"{col}_max_time_gap_hours"] = time_gaps.max().total_seconds() / 3600
        
        return kpis
    
    def _calculate_categorical_kpis(self) -> Dict[str, Any]:
        """Calculate diversity and distribution KPIs for categorical columns."""
        df = self.data_processor.df
        categorical_cols = df.select_dtypes(include=['object']).columns
        kpis = {}
        
        for col in categorical_cols:
            col_data = df[col].dropna()
            if len(col_data) == 0:
                continue
                
            value_counts = col_data.value_counts()
            
            kpis[f"{col}_unique_count"] = col_data.nunique()
            kpis[f"{col}_mode"] = col_data.mode().iloc[0] if not col_data.mode().empty else None
            kpis[f"{col}_mode_frequency"] = value_counts.iloc[0] if len(value_counts) > 0 else 0
            kpis[f"{col}_mode_percentage"] = (value_counts.iloc[0] / len(col_data)) * 100 if len(value_counts) > 0 else 0
            
            # Diversity metrics
            kpis[f"{col}_entropy"] = self._calculate_entropy(value_counts)
            kpis[f"{col}_gini_coefficient"] = self._calculate_gini_coefficient(value_counts)
            
            # Top values
            kpis[f"{col}_top_5_values"] = value_counts.head(5).to_dict()
            kpis[f"{col}_bottom_5_values"] = value_counts.tail(5).to_dict()
            
            # Cardinality analysis
            kpis[f"{col}_cardinality_ratio"] = col_data.nunique() / len(col_data)
        
        return kpis
    
    def _calculate_quality_metrics(self) -> Dict[str, Any]:
        """Calculate data quality and consistency metrics."""
        df = self.data_processor.df
        kpis = {}
        
        # Missing data analysis
        missing_data = df.isnull().sum()
        kpis["total_missing_values"] = missing_data.sum()
        kpis["missing_values_percentage"] = (missing_data.sum() / (len(df) * len(df.columns))) * 100
        
        # Column-wise missing data
        kpis["columns_with_missing_data"] = (missing_data > 0).sum()
        kpis["columns_complete_data"] = (missing_data == 0).sum()
        
        # Duplicate analysis
        kpis["duplicate_rows"] = df.duplicated().sum()
        kpis["duplicate_percentage"] = (df.duplicated().sum() / len(df)) * 100
        
        # Data consistency
        kpis["data_consistency_score"] = self._calculate_consistency_score()
        
        return kpis
    
    def _calculate_performance_metrics(self) -> Dict[str, Any]:
        """Calculate processing and memory efficiency metrics."""
        df = self.data_processor.df
        kpis = {}
        
        # Processing efficiency
        start_time = datetime.now()
        _ = df.describe()
        processing_time = (datetime.now() - start_time).total_seconds()
        kpis["processing_time_seconds"] = processing_time
        
        # Memory efficiency
        kpis["memory_efficiency_mb_per_record"] = df.memory_usage(deep=True).sum() / (1024 * 1024 * len(df))
        
        # Column efficiency
        kpis["avg_column_cardinality"] = df.nunique().mean()
        kpis["high_cardinality_columns"] = (df.nunique() > len(df) * 0.5).sum()
        
        return kpis
    
    def _calculate_entropy(self, value_counts: pd.Series) -> float:
        """Calculate Shannon entropy for categorical data diversity."""
        probabilities = value_counts / value_counts.sum()
        return -np.sum(probabilities * np.log2(probabilities))
    
    def _calculate_gini_coefficient(self, value_counts: pd.Series) -> float:
        """Calculate Gini coefficient for categorical data concentration."""
        probabilities = value_counts / value_counts.sum()
        return 1 - np.sum(probabilities ** 2)
    
    def _calculate_consistency_score(self) -> float:
        """Calculate overall data consistency score (0-100)."""
        df = self.data_processor.df
        
        # Factors affecting consistency
        missing_penalty = df.isnull().sum().sum() / (len(df) * len(df.columns))
        duplicate_penalty = df.duplicated().sum() / len(df)
        
        # Normalize to 0-100 scale
        consistency_score = (1 - missing_penalty - duplicate_penalty) * 100
        return max(0, min(100, consistency_score))
    
    def get_kpi_summary(self) -> Dict[str, Any]:
        """Get condensed KPI summary for dashboard display."""
        if not self.kpis_cache:
            self.calculate_all_kpis()
        
        summary = {
            "core_metrics": {
                "total_records": self.kpis_cache.get("total_records", 0),
                "total_columns": self.kpis_cache.get("total_columns", 0),
                "data_completeness": self.kpis_cache.get("data_completeness", 0),
                "memory_usage_mb": self.kpis_cache.get("memory_usage_mb", 0)
            },
            "quality_metrics": {
                "missing_percentage": self.kpis_cache.get("missing_values_percentage", 0),
                "duplicate_percentage": self.kpis_cache.get("duplicate_percentage", 0),
                "consistency_score": self.kpis_cache.get("data_consistency_score", 0)
            },
            "performance_metrics": {
                "processing_time": self.kpis_cache.get("processing_time_seconds", 0),
                "memory_efficiency": self.kpis_cache.get("memory_efficiency_mb_per_record", 0)
            }
        }
        
        return summary
    

