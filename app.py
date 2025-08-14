"""
Main entry point for Dashboard Generator.
Streamlit application for creating professional data dashboards and visualizations.
"""

import streamlit as st
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.dashboard.analytics import DashboardGenerator
from src.config.settings import config
from src.config.constants import ChartTypes, CSS_VARIABLES

# Configure page
st.set_page_config(
    page_title="Dashboard Generator",
    page_icon="📊",
    layout=config.LAYOUT,
    initial_sidebar_state="collapsed"  # Collapse sidebar by default
)



# Apply custom CSS
st.markdown(f"""
<style>
{CSS_VARIABLES}



/* CSS Variables for clean light theme */
:root {{
    --primary: {config.PRIMARY_COLOR};
    --secondary: {config.SECONDARY_COLOR};
    --success: {config.SUCCESS_COLOR};
    --warning: {config.WARNING_COLOR};
    --danger: {config.DANGER_COLOR};
    --dark: #2C3E50;
    --light: #ECF0F1;
    --white: #FFFFFF;
    --border: rgba(44, 62, 80, 0.1);
    --shadow: 0 2px 8px rgba(44, 62, 80, 0.1);
    --shadow-hover: 0 4px 16px rgba(44, 62, 80, 0.15);
}}

/* Clean light theme background */
.stApp {{
    background: linear-gradient(135deg, #FAFAFA 0%, #F8F9FA 100%) !important;
}}

/* Main container */
.main .block-container {{ 
    background: transparent !important; 
    padding-top: 1rem; 
    max-width: 1400px !important;
}}

/* Dashboard Cards */
.kpi-card {{
    background: var(--white);
    border-radius: 8px;
    padding: 24px;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}}

.kpi-card:hover {{
    box-shadow: var(--shadow-hover);
    transform: translateY(-2px);
}}

.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--primary);
}}

.kpi-value {{
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--dark);
    margin: 8px 0;
    line-height: 1;
}}

.kpi-label {{
    font-size: 0.9rem;
    color: #5D6D7E;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* Dashboard Header */
.dashboard-header {{
    background: var(--white);
    border-radius: 12px;
    padding: 32px;
    margin-bottom: 24px;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
}}

.dashboard-title {{
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--dark);
    margin: 0 0 8px 0;
}}

.dashboard-subtitle {{
    font-size: 1.1rem;
    color: #5D6D7E;
    margin: 0;
    font-weight: 400;
}}

/* Configuration Cards */
.config-card {{
    background: var(--white);
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
    transition: all 0.3s ease;
}}

.config-card:hover {{
    box-shadow: var(--shadow-hover);
}}

.config-title {{
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--dark);
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--primary);
}}

/* Chart Cards */
.chart-card {{
    background: var(--white);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 24px;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
    transition: all 0.3s ease;
}}

.chart-card:hover {{
    box-shadow: var(--shadow-hover);
}}

.chart-title {{
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--dark);
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}}

/* Buttons */
.stButton > button {{
    background: var(--primary) !important;
    border: none !important;
    border-radius: 6px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    font-size: 14px !important;
    box-shadow: var(--shadow) !important;
    transition: all 0.3s ease !important;
}}

.stButton > button:hover {{
    background: var(--secondary) !important;
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-hover) !important;
}}

/* Text colors with good contrast */
.stApp h1, 
.stApp h2, 
.stApp h3, 
.stApp h4, 
.stApp h5, 
.stApp h6 {{
    color: var(--dark) !important;
}}

.stApp p, 
.stApp div, 
.stApp span {{
    color: #5D6D7E !important;
}}

/* Streamlit specific elements */
.stApp .stTextInput > div > div > input {{
    color: var(--dark) !important;
    background-color: #FFFFFF !important;
    border: 1px solid #D5DBDB !important;
}}

.stApp .stSelectbox > div > div > div {{
    color: var(--dark) !important;
    background-color: #FFFFFF !important;
    border: 1px solid #D5DBDB !important;
}}

/* File Uploader - Clean styling */
.stApp .stFileUploader {{
    color: var(--dark) !important;
}}

.stApp .stFileUploader > div {{
    color: var(--dark) !important;
    background-color: #FFFFFF !important;
    border: 2px dashed #BDC3C7 !important;
}}

.stApp .stFileUploader > div:hover {{
    border-color: var(--primary) !important;
    background-color: #F8F9FA !important;
}}

/* File Uploader text and elements */
.stApp .stFileUploader p {{
    color: var(--dark) !important;
}}

.stApp .stFileUploader span {{
    color: var(--dark) !important;
}}

.stApp .stFileUploader div {{
    color: var(--dark) !important;
}}

/* Override any dark theme styles for file uploader */
.stApp .stFileUploader * {{
    color: var(--dark) !important;
    background-color: transparent !important;
}}

.stApp .stFileUploader > div * {{
    color: var(--dark) !important;
    background-color: transparent !important;
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .dashboard-title {{ font-size: 2rem; }}
    .kpi-value {{ font-size: 2rem; }}
    .chart-card {{ padding: 16px; }}
    .config-card {{ padding: 16px; }}
}}
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function for the dashboard generator."""
    
    # Application header
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style="font-size: 3.5rem; font-weight: 700; color: var(--dark); margin: 0;">
            📊 Dashboard Generator
        </h1>
        <p style="font-size: 1.3rem; color: #605E5C; margin: 15px 0 0 0;">
            Create data dashboards and visualizations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add clean header styling
    st.markdown("""
    <style>
    /* Clean header colors with good contrast */
    .stApp h1 {
        color: #2C3E50 !important;
    }
    .stApp p {
        color: #5D6D7E !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'dashboard_generator' not in st.session_state:
        st.session_state.dashboard_generator = DashboardGenerator()
    
    if 'dashboard_title' not in st.session_state:
        st.session_state.dashboard_title = "My Dashboard"
    
    if 'dashboard_subtitle' not in st.session_state:
        st.session_state.dashboard_subtitle = "Data analysis and insights"
    
    generator = st.session_state.dashboard_generator
    
    # Configuration Section - Main Area
    st.markdown("""
    <div class="config-card">
        <div class="config-title">⚙️ Dashboard Configuration</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Configuration fields in columns
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.text_input("Dashboard Title", value=st.session_state.dashboard_title, key="title_input")
    
    with col2:
        st.text_input("Dashboard Subtitle", value=st.session_state.dashboard_subtitle, key="subtitle_input")
    
    with col3:
        if st.button("💾", use_container_width=True):
            st.session_state.dashboard_title = st.session_state.title_input
            st.session_state.dashboard_subtitle = st.session_state.subtitle_input
            st.success("✅ Configuration saved successfully!")
    
    st.markdown("---")
    
    # Data Upload Section
    st.markdown("""
    <div class="config-card">
        <div class="config-title">📁 Data Upload</div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Select CSV file", type=['csv'])
    
    if uploaded_file:
        if generator.load_data(uploaded_file):
            st.success(f"✅ {len(generator.data_processor.df)} records loaded successfully")
            
            st.markdown("---")
            
            # Visualization Setup Section
            st.markdown("""
            <div class="config-card">
                <div class="config-title">📈 Create Visualizations</div>
            </div>
            """, unsafe_allow_html=True)
            
            available_columns = generator.get_available_columns()
            
            if available_columns:
                # Chart configuration in columns
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    col_name = st.selectbox("Select column", available_columns)
                
                with col2:
                    chart_type = st.selectbox("Chart type", ChartTypes.get_all_types())
                
                with col3:
                    chart_title = st.text_input("Chart title", value=f"Analysis of {col_name}")
                
                # Y-axis selection for scatter plots
                y_column = None
                if chart_type == ChartTypes.SCATTER.value:
                    y_column = st.selectbox("Select Y-axis column", available_columns, key="y_axis")
                
                # Action buttons
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.button("➕ Add Chart", use_container_width=True):
                        if generator.add_chart_config(col_name, chart_type, chart_title, y_column):
                            st.success(f"✅ Chart added: {chart_title}")
                        else:
                            st.error("❌ Failed to add chart")
                
                with col2:
                    if st.button("🚀 Generate Dashboard", use_container_width=True):
                        if generator.charts_config:
                            st.session_state.show_dashboard = True
                            st.rerun()
                        else:
                            st.warning("⚠️ Add at least one chart first")
                
                # Configured charts
                if generator.charts_config:
                    st.markdown("---")
                    st.markdown("**📊 Your Charts:**")
                    
                    for i, config in enumerate(generator.charts_config):
                        col1, col2, col3 = st.columns([3, 2, 1])
                        with col1:
                            st.write(f"📊 {config['title']}")
                        with col2:
                            st.write(f"({config['chart_type']})")
                        with col3:
                            if st.button("🗑️", key=f"del_{i}", use_container_width=True):
                                generator.remove_chart_config(i)
                                st.rerun()
    
    # Main dashboard area
    if st.session_state.get('show_dashboard', False) and generator.data_processor.df is not None:
        st.markdown("---")
        generator.generate_dashboard()
        
        # Additional analysis options
        st.markdown("---")
        st.markdown("### 🔍 Advanced Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Correlation Matrix", use_container_width=True):
                correlation_fig = generator.create_correlation_analysis()
                if correlation_fig:
                    st.plotly_chart(correlation_fig, use_container_width=True)
                else:
                    st.warning("⚠️ Need at least 2 numerical columns for correlation analysis")
        
        with col2:
            st.write("")  # Empty space for layout balance
        
        with col3:
            if st.button("🔄 New Dashboard", use_container_width=True):
                st.session_state.show_dashboard = False
                generator.clear_all_charts()
                generator.filters = {}
                st.rerun()


if __name__ == "__main__":
    main()
