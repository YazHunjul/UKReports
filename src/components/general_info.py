import streamlit as st
from datetime import datetime
from src.utils.session_manager import get_form_data, update_form_data

def render_general_info():
    """Render the general information collection component."""
    try:
        st.header("📋 General Information")
        
        # Initialize session state values if they don't exist
        if 'client_name' not in st.session_state:
            st.session_state.client_name = get_form_data('client_name', '')
        if 'project_name' not in st.session_state:
            st.session_state.project_name = get_form_data('project_name', '')
        if 'project_number' not in st.session_state:
            st.session_state.project_number = get_form_data('project_number', '')
        if 'date_of_visit' not in st.session_state:
            saved_date = get_form_data('date_of_visit', datetime.now().date())
            # Ensure we have a proper date object
            if isinstance(saved_date, str):
                try:
                    if '/' in saved_date:
                        saved_date = datetime.strptime(saved_date, '%Y/%m/%d').date()
                    elif '-' in saved_date:
                        saved_date = datetime.strptime(saved_date, '%Y-%m-%d').date()
                    else:
                        saved_date = datetime.now().date()
                except:
                    saved_date = datetime.now().date()
            st.session_state.date_of_visit = saved_date
        if 'engineer_name' not in st.session_state:
            st.session_state.engineer_name = get_form_data('engineer_name', '')
        
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                client = st.text_input(
                    "Client",
                    value=st.session_state.client_name,
                    key="client_name",
                    help="Enter the client name"
                )
                
                project_number = st.text_input(
                    "Project Number",
                    value=st.session_state.project_number,
                    key="project_number",
                    help="Enter the project number"
                )
                
                engineer = st.text_input(
                    "Engineer(s)",
                    value=st.session_state.engineer_name,
                    key="engineer_name",
                    help="Enter the engineer name(s)"
                )
            
            with col2:
                project_name = st.text_input(
                    "Project Name",
                    value=st.session_state.project_name,
                    key="project_name",
                    help="Enter the project name"
                )
                
                date_of_visit = st.date_input(
                    "Date of Visit",
                    value=st.session_state.date_of_visit,
                    key="date_of_visit",
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
        
    except Exception as e:
        st.error(f"Error loading General Information: {str(e)}")
        st.info("Please refresh the page if this error persists.")
        return {
            'client_name': '',
            'project_name': '',
            'project_number': '',
            'date_of_visit': datetime.now().date(),
            'engineer_name': ''
        } 