"""
Constants and enums for dashboard generator.
Defines chart types, theme colors, messages, and configuration constants.
"""

from enum import Enum
from typing import List, Dict


class ChartTypes(Enum):
    """Available chart types for data visualization."""
    
    PIE = "pie"
    BAR = "bar"
    LINE = "line"
    HISTOGRAM = "histogram"
    SCATTER = "scatter"
    TREEMAP = "treemap"
    FUNNEL = "funnel"
    
    @classmethod
    def get_all_types(cls) -> List[str]:
        """Get all chart type values as a list."""
        return [chart_type.value for chart_type in cls]
    
    @classmethod
    def get_display_names(cls) -> Dict[str, str]:
        """Get chart type display names for UI."""
        return {
            cls.PIE.value: "Pie Chart",
            cls.BAR.value: "Bar Chart", 
            cls.LINE.value: "Line Chart",
            cls.HISTOGRAM.value: "Histogram",
            cls.SCATTER.value: "Scatter Plot",
            cls.TREEMAP.value: "Treemap",
            cls.FUNNEL.value: "Funnel Chart"
        }


class ThemeColors(Enum):
    """Theme color constants for consistent UI styling."""
    
    PRIMARY = "#0078D4"
    SECONDARY = "#106EBE"
    SUCCESS = "#107C10"
    WARNING = "#FF8C00"
    DANGER = "#D13438"
    DARK = "#323130"
    LIGHT = "#F3F2F1"
    WHITE = "#FFFFFF"
    BORDER = "rgba(0, 0, 0, 0.1)"
    SHADOW = "0 2px 8px rgba(0, 0, 0, 0.1)"
    SHADOW_HOVER = "0 4px 16px rgba(0, 0, 0, 0.15)"


class ErrorMessages(Enum):
    """Error message constants for user feedback."""
    
    EMPTY_FILE = "❌ Empty CSV file detected"
    LOAD_ERROR = "❌ Data loading error: {error}"
    NO_CHARTS = "⚠️ Configure at least one chart"
    CHART_ERROR = "Chart generation error: {error}"
    INVALID_COLUMN = "Invalid column selected: {column}"
    FILE_TOO_LARGE = "File size exceeds maximum limit of {max_size}MB"
    UNSUPPORTED_FORMAT = "Unsupported file format. Please use: {formats}"


class SuccessMessages(Enum):
    """Success message constants for user feedback."""
    
    DATA_LOADED = "✅ {count} records loaded successfully"
    CHART_ADDED = "✅ Chart added: {title}"
    CONFIG_SAVED = "✅ Configuration saved successfully!"
    EXPORT_SUCCESS = "✅ Data exported successfully"


class DataTypes(Enum):
    """Data type constants for automatic type detection."""
    
    DATETIME = "datetime"
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    TEXT = "text"
    BOOLEAN = "boolean"


# CSS Style constants for consistent styling
CSS_VARIABLES = """
:root {
    --primary: #0078D4;
    --secondary: #106EBE;
    --success: #107C10;
    --warning: #FF8C00;
    --danger: #D13438;
    --dark: #323130;
    --light: #F3F2F1;
    --white: #FFFFFF;
    --border: rgba(0, 0, 0, 0.1);
    --shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    --shadow-hover: 0 4px 16px rgba(0, 0, 0, 0.15);
}
"""

# Chart configuration constants for consistent chart styling
CHART_CONFIGS = {
    "pie": {
        "color_sequence": "px.colors.qualitative.Set3",
        "requires_y": False
    },
    "bar": {
        "color_sequence": "single_color",
        "requires_y": False
    },
    "line": {
        "color_sequence": "single_color", 
        "requires_y": False
    },
    "histogram": {
        "color_sequence": "single_color",
        "requires_y": False
    },
    "scatter": {
        "color_sequence": "single_color",
        "requires_y": True
    },
    "treemap": {
        "color_sequence": "px.colors.qualitative.Set3",
        "requires_y": False
    },
    "funnel": {
        "color_sequence": "single_color",
        "requires_y": False
    }
}
