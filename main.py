import streamlit as st
import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.session_manager import initialize_session_state, get_form_data, load_data_from_url_params
from src.components.report_type_selector import render_report_type_selector
from src.components.general_info import render_general_info
from src.components.canopy_config import render_canopy_configuration
from src.components.sidebar import render_sidebar
from src.components.signature_notes import render_signature_and_notes
from src.components.action_buttons import render_action_buttons
from src.components.edge_box_check import render_edge_box_check
from src.components.uv_checklist import render_uv_checklist
from src.components.save_share import render_save_share_section, render_load_shared_data_notification
from src.utils.session_manager import has_uv_technology

# Configure the page
st.set_page_config(
    page_title="Canopy Commissioning Report Generator",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function."""
    st.title("🏭 Canopy Commissioning Report Generator")
    st.markdown("---")
    
    # Initialize session state
    initialize_session_state()
    
    # Check for shared data in URL parameters
    if load_data_from_url_params():
        st.session_state.data_loaded_from_url = True
    
    # Show notification if data was loaded from shared link
    render_load_shared_data_notification()
    
    # Render sidebar
    render_sidebar()
    
    # Report Type Selection
    report_type = render_report_type_selector()
    st.markdown("---")
    
    # General Information Section
    render_general_info()
    
    # Canopy Configuration Section (only for Canopy Commissioning reports)
    if report_type == "Canopy Commissioning":
        st.markdown("---")
        render_canopy_configuration()
        
    # Edge Box Check Section (optional)
    st.markdown("---")
    render_edge_box_check()
    
    # Save & Share Section
    st.markdown("---")
    render_save_share_section()
    
    # Signature and Notes Section
    st.markdown("---")
    render_signature_and_notes()
    
    # Action Buttons
    st.markdown("---")
    render_action_buttons()

if __name__ == "__main__":
    main() 