import streamlit as st
from src.config import REPORT_TYPES
from src.utils.session_manager import get_form_data, update_form_data

def render_report_type_selector():
    """Render the report type selection component."""
    st.header("📄 Report Type")
    
    # Initialize the session state value if not exists
    if 'report_type' not in st.session_state:
        st.session_state.report_type = 'Canopy Commissioning'
    
    report_type = st.selectbox(
        "Select Report Type",
        options=REPORT_TYPES,
        key="report_type",
        help="Choose the type of report to generate"
    )
    
    # Get the value from session state
    report_type_value = st.session_state.get('report_type', 'Canopy Commissioning')
    
    update_form_data({'report_type': report_type_value})
    return report_type_value 