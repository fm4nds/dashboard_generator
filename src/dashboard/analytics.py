"""
Core analytics orchestrator for dashboard generator.
Manages data processing, KPI calculation, and visualization generation.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from ..config.settings import config
from ..config.constants import ChartTypes, ErrorMessages, SuccessMessages
from ..utils.data_processor import DataProcessor
from .kpi_calculator import KPICalculator
from .visualizations import ChartGenerator

logger = logging.getLogger(__name__)


class DashboardGenerator:
    """
    Main analytics orchestrator that coordinates data processing, KPI calculation,
    and visualization generation for professional dashboards.
    """
    
    def __init__(self):
        """Initialize analytics components and state."""
        self.data_processor = DataProcessor()
        self.kpi_calculator = KPICalculator(self.data_processor)
        self.chart_generator = ChartGenerator(self.data_processor)
        self.charts_config: List[Dict[str, Any]] = []
        self.filters: Dict[str, Any] = {}
        self.theme = 'professional'
        
    def load_data(self, uploaded_file) -> bool:
        """
        Load and validate uploaded data file.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        if uploaded_file is None:
            return False
            
        try:
            self.data_processor.df = pd.read_csv(uploaded_file)
            
            if self.data_processor.df.empty:
                st.error(ErrorMessages.EMPTY_FILE.value)
                return False
                
            # Process and validate data
            self.data_processor._clean_data()
            self.data_processor._detect_data_types()
            self.data_processor._validate_data()
            
            return True
            
        except Exception as e:
            st.error(ErrorMessages.LOAD_ERROR.value.format(error=str(e)))
            return False
    
    def get_available_columns(self) -> List[str]:
        """Get list of available columns for analysis."""
        if self.data_processor.df is None:
            return []
        return self.data_processor.df.columns.tolist()
    
    def get_column_data_types(self) -> Dict[str, str]:
        """Get detected data types for all columns."""
        if self.data_processor.df is None:
            return {}
        return self.data_processor.data_types
    
    def calculate_kpis(self) -> Dict[str, Any]:
        """Calculate all KPIs for the loaded dataset."""
        return self.kpi_calculator.calculate_all_kpis()
    
    def create_chart(self, config: Dict[str, Any]):
        """Create visualization based on chart configuration."""
        return self.chart_generator.create_chart(config)
    
    def _get_theme_color(self) -> str:
        """Get theme color for visualizations."""
        if self.theme == 'professional':
            return '#0078D4'
        return '#0078D4'
    
    def _apply_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply current filters to dataset."""
        return self.data_processor.get_filtered_data(self.filters)
    
    def generate_dashboard(self):
        """Generate and display the complete dashboard interface."""
        if not self.charts_config:
            st.warning(ErrorMessages.NO_CHARTS.value)
            return
        
        # Dashboard Header
        st.markdown(f"""
        <div class="dashboard-header">
            <h1 class="dashboard-title">{st.session_state.get('dashboard_title', 'My Dashboard')}</h1>
            <p class="dashboard-subtitle">{st.session_state.get('dashboard_subtitle', 'Data analysis and insights')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display KPIs
        kpis = self.calculate_kpis()
        if kpis:
            st.markdown("### 📊 Key Performance Indicators")
        
            kpi_summary = self.kpi_calculator.get_kpi_summary()
            
            kpi_cols = st.columns(4)
            
            with kpi_cols[0]:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Total Records</div>
                    <div class="kpi-value">{kpi_summary['core_metrics']['total_records']:,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with kpi_cols[1]:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Data Quality Score</div>
                    <div class="kpi-value">{kpi_summary['quality_metrics']['consistency_score']:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with kpi_cols[2]:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Memory Usage</div>
                    <div class="kpi-value">{kpi_summary['core_metrics']['memory_usage_mb']:.1f} MB</div>
                </div>
                """, unsafe_allow_html=True)
            
            with kpi_cols[3]:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Processing Time</div>
                    <div class="kpi-value">{kpi_summary['performance_metrics']['processing_time']:.3f}s</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Dynamic Filters
        if self.data_processor.df is not None:
            st.markdown("### 🔍 Data Filters")
            
            filter_cols = st.columns(3)
            categorical_cols = self.data_processor.df.select_dtypes(include=['object']).columns
            
            for i, col in enumerate(categorical_cols[:3]):
                if i < len(filter_cols):
                    with filter_cols[i]:
                        unique_values = self.data_processor.df[col].dropna().unique()
                        if len(unique_values) <= 20:  # Limit to reasonable number of options
                            selected_values = st.multiselect(
                                f"Filter by {col}",
                                options=unique_values,
                                default=unique_values[:5] if len(unique_values) > 5 else unique_values
                            )
                            self.filters[col] = selected_values
        
        # Display Visualizations
        st.markdown("### 📈 Charts & Visualizations")
        
        for i, config in enumerate(self.charts_config):
            fig = self.create_chart(config)
            if fig:
                st.markdown(f"""
                <div class="chart-card">
                    <div class="chart-title">{config['title']}</div>
                </div>
                """, unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
        
        # Data Table and Export
        st.markdown("### 📋 Data Table")
        
        filtered_df = self._apply_filters(self.data_processor.df)
        st.dataframe(filtered_df, use_container_width=True)
        
        # Export functionality
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Export Data (CSV)",
            data=csv,
            file_name=f"dashboard_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get comprehensive data summary statistics."""
        return self.data_processor.get_data_summary()
    
    def add_chart_config(self, column: str, chart_type: str, title: str, y_column: str = None) -> bool:
        """
        Add new chart configuration to dashboard.
        
        Args:
            column: Primary data column for visualization
            chart_type: Type of chart to create
            title: Chart title
            y_column: Secondary column for scatter plots
            
        Returns:
            bool: True if configuration added successfully
        """
        if column not in self.get_available_columns():
            return False
        
        config = {
            'column': column,
            'chart_type': chart_type,
            'title': title,
            'filters': self.filters.copy()
        }
        
        if y_column and chart_type == ChartTypes.SCATTER.value:
            config['y_column'] = y_column
        
        self.charts_config.append(config)
        return True
    
    def remove_chart_config(self, index: int) -> bool:
        """Remove chart configuration by index."""
        if 0 <= index < len(self.charts_config):
            self.charts_config.pop(index)
            return True
        return False
    
    def clear_all_charts(self) -> None:
        """Clear all chart configurations."""
        self.charts_config.clear()
    
    def get_recommended_charts(self) -> List[Dict[str, str]]:
        """
        Generate chart recommendations based on data types.
        
        Returns:
            List of recommended chart configurations
        """
        recommendations = []
        data_types = self.get_column_data_types()
        
        for col, dtype in data_types.items():
            if dtype == 'categorical':
                recommendations.extend([
                    {'column': col, 'chart_type': 'pie', 'title': f'Distribution of {col}'},
                    {'column': col, 'chart_type': 'bar', 'title': f'Frequency of {col}'},
                    {'column': col, 'chart_type': 'treemap', 'title': f'Hierarchy of {col}'}
                ])
            elif dtype == 'numerical':
                recommendations.extend([
                    {'column': col, 'chart_type': 'histogram', 'title': f'Distribution of {col}'},
                    {'column': col, 'chart_type': 'bar', 'title': f'Analysis of {col}'}
                ])
            elif dtype == 'datetime':
                recommendations.extend([
                    {'column': col, 'chart_type': 'line', 'title': f'Time Series of {col}'}
                ])
        
        return recommendations
    
    def create_correlation_analysis(self) -> Optional[Any]:
        """Create correlation matrix for numerical columns."""
        numerical_cols = self.data_processor.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numerical_cols) >= 2:
            return self.chart_generator.create_correlation_matrix(numerical_cols)
        return None
    

