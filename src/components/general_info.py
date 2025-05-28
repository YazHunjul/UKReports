import streamlit as st
from datetime import datetime
from src.utils.session_manager import get_form_data, update_form_data

def render_general_info():
    """Render the general information collection component."""
    st.header("📋 General Information")
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            client = st.text_input(
                "Client",
                key="client_name",
                help="Enter the client name"
            )
            
            project_number = st.text_input(
                "Project Number",
                key="project_number",
                help="Enter the project number"
            )
            
            engineer = st.text_input(
                "Engineer(s)",
                key="engineer_name",
                help="Enter the engineer name(s)"
            )
        
        with col2:
            project_name = st.text_input(
                "Project Name",
                key="project_name",
                help="Enter the project name"
            )
            
            date_of_visit = st.date_input(
                "Date of Visit",
                key="date_of_visit",
                value=datetime.now().date(),
                help="Select the date of visit"
            )
    
    # Get values from session state (automatically managed by Streamlit with keys)
    client_value = st.session_state.get('client_name', '')
    project_name_value = st.session_state.get('project_name', '')
    project_number_value = st.session_state.get('project_number', '')
    date_of_visit_value = st.session_state.get('date_of_visit', datetime.now().date())
    engineer_value = st.session_state.get('engineer_name', '')
    
    # Update form data with current values
    update_form_data({
        'client_name': client_value,
        'project_name': project_name_value,
        'project_number': project_number_value,
        'date_of_visit': date_of_visit_value,
        'engineer_name': engineer_value
    })
    
    return {
        'client_name': client_value,
        'project_name': project_name_value,
        'project_number': project_number_value,
        'date_of_visit': date_of_visit_value,
        'engineer_name': engineer_value
    } 