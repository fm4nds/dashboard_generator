"""
Dashboard module for data analysis and visualization.
Contains the main dashboard generation and visualization components.
"""

from .analytics import DashboardGenerator
from .visualizations import ChartGenerator
from .kpi_calculator import KPICalculator

__all__ = [
    "DashboardGenerator",
    "ChartGenerator",
    "KPICalculator"
]
