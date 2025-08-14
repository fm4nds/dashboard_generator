"""
Dashboard configuration settings and constants.
Centralized configuration management for the dashboard generator.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import os


@dataclass
class DashboardConfig:
    """
    Configuration class for dashboard settings.
    Manages application, theme, chart, and performance settings.
    """
    
    # Application settings
    APP_TITLE: str = "Dashboard Generator"
    APP_ICON: str = "📊"
    LAYOUT: str = "wide"
    INITIAL_SIDEBAR_STATE: str = "expanded"
    
    # Theme settings
    PRIMARY_COLOR: str = "#0078D4"
    SECONDARY_COLOR: str = "#106EBE"
    SUCCESS_COLOR: str = "#107C10"
    WARNING_COLOR: str = "#FF8C00"
    DANGER_COLOR: str = "#D13438"
    DARK_COLOR: str = "#323130"
    LIGHT_COLOR: str = "#F3F2F1"
    WHITE_COLOR: str = "#FFFFFF"
    
    # Chart settings
    DEFAULT_CHART_HEIGHT: int = 400
    DEFAULT_CHART_WIDTH: int = 800
    CHART_MARGIN: Dict[str, int] = None
    
    # Data settings
    MAX_FILE_SIZE_MB: int = 100
    SUPPORTED_FORMATS: List[str] = None
    DEFAULT_ENCODING: str = "utf-8"
    
    # Performance settings
    CACHE_TTL: int = 3600  # 1 hour
    MAX_RECORDS_DISPLAY: int = 10000
    
    def __post_init__(self):
        """Initialize default values after dataclass creation."""
        if self.CHART_MARGIN is None:
            self.CHART_MARGIN = {"l": 20, "r": 20, "t": 40, "b": 20}
        
        if self.SUPPORTED_FORMATS is None:
            self.SUPPORTED_FORMATS = ["csv", "xlsx", "json"]
    
    @classmethod
    def from_env(cls) -> "DashboardConfig":
        """Load configuration from environment variables."""
        config = cls()
        
        # Override with environment variables if present
        if os.getenv("DASHBOARD_TITLE"):
            config.APP_TITLE = os.getenv("DASHBOARD_TITLE")
        
        if os.getenv("PRIMARY_COLOR"):
            config.PRIMARY_COLOR = os.getenv("PRIMARY_COLOR")
        
        if os.getenv("MAX_FILE_SIZE_MB"):
            config.MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB"))
        
        return config


# Global configuration instance
config = DashboardConfig.from_env()
