import streamlit as st
import pandas as pd
from src.utils.session_manager import get_form_data

def render_testing_panel(report_type: str):
    """Render the testing panel for viewing collected data."""
    st.subheader("🔍 Current Form Data (for testing)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("View collected data (JSON)", expanded=False):
            st.json(get_form_data(), expanded=False)
    
    with col2:
        if report_type == "Canopy Commissioning" and get_form_data('canopies'):
            with st.expander("Canopy Summary", expanded=False):
                canopies_df = pd.DataFrame(get_form_data('canopies'))
                if not canopies_df.empty:
                    st.dataframe(canopies_df, use_container_width=True) 