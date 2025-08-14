"""
Professional visualization generator for enterprise analytics dashboard.
Creates interactive charts and graphs using Plotly with enterprise styling.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import logging

from ..config.constants import ChartTypes, ThemeColors, CHART_CONFIGS
from ..config.settings import config
from ..utils.data_processor import DataProcessor

logger = logging.getLogger(__name__)


class ChartGenerator:
    """
    Professional chart generator for enterprise dashboards.
    Creates interactive visualizations with consistent enterprise styling.
    """
    
    def __init__(self, data_processor: DataProcessor):
        """Initialize chart generator with data processor and theme colors."""
        self.data_processor = data_processor
        self.theme_colors = {
            "primary": ThemeColors.PRIMARY.value,
            "secondary": ThemeColors.SECONDARY.value,
            "success": ThemeColors.SUCCESS.value,
            "warning": ThemeColors.WARNING.value,
            "danger": ThemeColors.DANGER.value
        }
    
    def create_chart(self, config: Dict[str, Any]) -> Optional[go.Figure]:
        """
        Create chart based on configuration.
        
        Args:
            config: Chart configuration dictionary
            
        Returns:
            Plotly figure object or None if error
        """
        try:
            chart_type = config.get('chart_type', 'bar')
            column = config.get('column')
            title = config.get('title', f'Analysis of {column}')
            
            if column not in self.data_processor.df.columns:
                logger.error(f"Column {column} not found in dataset")
                return None
            
            # Apply filters
            filtered_df = self.data_processor.get_filtered_data(config.get('filters', {}))
            
            if filtered_df.empty:
                logger.warning("No data available after filtering")
                return None
            
            # Create chart based on type
            if chart_type == ChartTypes.PIE.value:
                fig = self._create_pie_chart(filtered_df, column, title)
            elif chart_type == ChartTypes.BAR.value:
                fig = self._create_bar_chart(filtered_df, column, title)
            elif chart_type == ChartTypes.LINE.value:
                fig = self._create_line_chart(filtered_df, column, title)
            elif chart_type == ChartTypes.HISTOGRAM.value:
                fig = self._create_histogram(filtered_df, column, title)
            elif chart_type == ChartTypes.SCATTER.value:
                fig = self._create_scatter_plot(filtered_df, column, title, config)
            elif chart_type == ChartTypes.TREEMAP.value:
                fig = self._create_treemap(filtered_df, column, title)
            elif chart_type == ChartTypes.FUNNEL.value:
                fig = self._create_funnel_chart(filtered_df, column, title)
            else:
                logger.error(f"Unsupported chart type: {chart_type}")
                return None
            
            # Apply professional styling
            self._apply_enterprise_styling(fig, title)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating chart: {str(e)}")
            return None
    
    def _create_pie_chart(self, df: pd.DataFrame, column: str, title: str) -> go.Figure:
        """Create pie chart for categorical data distribution."""
        value_counts = df[column].value_counts()
        
        fig = px.pie(
            values=value_counts.values,
            names=value_counts.index,
            title=title,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        return fig
    
    def _create_bar_chart(self, df: pd.DataFrame, column: str, title: str) -> go.Figure:
        """Create bar chart for categorical data frequency."""
        value_counts = df[column].value_counts().head(20)  # Limit to top 20
        
        fig = px.bar(
            x=value_counts.index,
            y=value_counts.values,
            title=title,
            color_discrete_sequence=[self.theme_colors["primary"]]
        )
        
        fig.update_xaxes(title_text=column)
        fig.update_yaxes(title_text="Count")
        
        return fig
    
    def _create_line_chart(self, df: pd.DataFrame, column: str, title: str) -> go.Figure:
        """Create line chart for time series or sequential data."""
        # For time series data
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            time_series = df[column].value_counts().sort_index()
            fig = px.line(
                x=time_series.index,
                y=time_series.values,
                title=title,
                color_discrete_sequence=[self.theme_colors["primary"]]
            )
        else:
            # For categorical data with counts
            value_counts = df[column].value_counts().head(20)
            fig = px.line(
                x=value_counts.index,
                y=value_counts.values,
                title=title,
                color_discrete_sequence=[self.theme_colors["primary"]]
            )
        
        fig.update_xaxes(title_text=column)
        fig.update_yaxes(title_text="Count")
        
        return fig
    
    def _create_histogram(self, df: pd.DataFrame, column: str, title: str) -> go.Figure:
        """Create histogram for numerical data distribution."""
        fig = px.histogram(
            df,
            x=column,
            title=title,
            color_discrete_sequence=[self.theme_colors["primary"]],
            nbins=30
        )
        
        fig.update_xaxes(title_text=column)
        fig.update_yaxes(title_text="Frequency")
        
        return fig
    
    def _create_scatter_plot(self, df: pd.DataFrame, column: str, title: str, config: Dict) -> go.Figure:
        """Create scatter plot for correlation analysis."""
        y_column = config.get('y_column')
        
        if not y_column or y_column not in df.columns:
            # Create scatter with index if no y column specified
            fig = px.scatter(
                x=df.index,
                y=df[column],
                title=title,
                color_discrete_sequence=[self.theme_colors["primary"]]
            )
        else:
            fig = px.scatter(
                df,
                x=column,
                y=y_column,
                title=title,
                color_discrete_sequence=[self.theme_colors["primary"]]
            )
        
        fig.update_xaxes(title_text=column)
        if y_column:
            fig.update_yaxes(title_text=y_column)
        
        return fig
    
    def _create_treemap(self, df: pd.DataFrame, column: str, title: str) -> go.Figure:
        """Create treemap for hierarchical data visualization."""
        value_counts = df[column].value_counts().head(50)  # Limit for performance
        
        fig = px.treemap(
            names=value_counts.index,
            parents=[''] * len(value_counts),
            values=value_counts.values,
            title=title,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        return fig
    
    def _create_funnel_chart(self, df: pd.DataFrame, column: str, title: str) -> go.Figure:
        """Create funnel chart for process flow visualization."""
        value_counts = df[column].value_counts().head(10)  # Top 10 for funnel
        
        fig = px.funnel(
            x=value_counts.values,
            y=value_counts.index,
            title=title,
            color_discrete_sequence=[self.theme_colors["primary"]]
        )
        
        fig.update_xaxes(title_text="Count")
        fig.update_yaxes(title_text=column)
        
        return fig
    
    def _apply_enterprise_styling(self, fig: go.Figure, title: str) -> None:
        """Apply professional enterprise styling to charts."""
        fig.update_layout(
            title={
                'text': title,
                'font': {
                    'size': 18,
                    'color': ThemeColors.DARK.value,
                    'family': 'Inter'
                },
                'x': 0.5,
                'xanchor': 'center'
            },
            font_family='Inter',
            height=config.DEFAULT_CHART_HEIGHT,
            margin=config.CHART_MARGIN,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor=ThemeColors.BORDER.value,
                borderwidth=1
            )
        )
        
        # Professional axis styling
        fig.update_xaxes(
            gridcolor='#E1DFDD',
            gridwidth=1,
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor=ThemeColors.BORDER.value
        )
        
        fig.update_yaxes(
            gridcolor='#E1DFDD',
            gridwidth=1,
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor=ThemeColors.BORDER.value
        )
    
    def create_dashboard_summary(self, kpis: Dict[str, Any]) -> go.Figure:
        """Create dashboard summary with key metrics indicators."""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Data Overview', 'Quality Metrics', 'Performance', 'Trends'),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Data Overview
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=kpis.get('total_records', 0),
                title={"text": "Total Records"},
                delta={'reference': 0},
                domain={'row': 0, 'column': 0}
            ),
            row=1, col=1
        )
        
        # Quality Score
        quality_score = kpis.get('data_consistency_score', 0)
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=quality_score,
                title={'text': "Data Quality Score"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': self.theme_colors["primary"]},
                    'steps': [
                        {'range': [0, 50], 'color': self.theme_colors["danger"]},
                        {'range': [50, 80], 'color': self.theme_colors["warning"]},
                        {'range': [80, 100], 'color': self.theme_colors["success"]}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                },
                domain={'row': 0, 'column': 1}
            ),
            row=1, col=2
        )
        
        # Memory Usage
        memory_usage = kpis.get('memory_usage_mb', 0)
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=memory_usage,
                title={"text": "Memory Usage (MB)"},
                domain={'row': 1, 'column': 0}
            ),
            row=2, col=1
        )
        
        # Processing Time
        processing_time = kpis.get('processing_time_seconds', 0)
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=processing_time,
                title={"text": "Processing Time (s)"},
                domain={'row': 1, 'column': 1}
            ),
            row=2, col=2
        )
        
        # Apply styling
        fig.update_layout(
            title="Dashboard Summary",
            height=600,
            showlegend=False,
            font_family='Inter'
        )
        
        return fig
    
    def create_correlation_matrix(self, numerical_columns: List[str]) -> go.Figure:
        """Create correlation matrix heatmap for numerical columns."""
        if len(numerical_columns) < 2:
            return None
        
        correlation_matrix = self.data_processor.df[numerical_columns].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=np.round(correlation_matrix.values, 2),
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="Correlation Matrix",
            height=500,
            font_family='Inter'
        )
        
        return fig
    
    def create_distribution_comparison(self, column: str, group_by: str = None) -> go.Figure:
        """
        Create distribution comparison chart.
        
        Args:
            column: Column to analyze
            group_by: Optional grouping column
            
        Returns:
            Plotly figure with distribution comparison
        """
        if group_by and group_by in self.data_processor.df.columns:
            # Grouped distribution
            fig = px.histogram(
                self.data_processor.df,
                x=column,
                color=group_by,
                title=f"Distribution of {column} by {group_by}",
                barmode='overlay',
                opacity=0.7
            )
        else:
            # Simple distribution
            fig = px.histogram(
                self.data_processor.df,
                x=column,
                title=f"Distribution of {column}",
                color_discrete_sequence=[self.theme_colors["primary"]]
            )
        
        self._apply_enterprise_styling(fig, f"Distribution Analysis: {column}")
        
        return fig
