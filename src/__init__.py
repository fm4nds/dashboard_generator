"""
Dashboard Generator
A professional-grade dashboard creation platform for data analysis and visualization.

Author: Amanda Galindo
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Amanda Galindo"
__email__ = "amanda.galindo@example.com"

from .dashboard.analytics import DashboardGenerator
from .config.settings import DashboardConfig
from .utils.data_processor import DataProcessor

__all__ = [
    "DashboardGenerator",
    "DashboardConfig",
    "DataProcessor"
]
