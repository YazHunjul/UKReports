import streamlit as st
from datetime import datetime
import os

# Configure the page
st.set_page_config(
    page_title="Canopy Commissioning Report Generator",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🏭 Canopy Commissioning Report Generator")
    st.markdown("---")
    
    # Initialize session state for form data
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    # Report Type Selection
    st.header("📄 Report Type")
    report_types = ["Canopy Commissioning", "Supply Air Analysis", "Full System Report"]
    
    report_type = st.selectbox(
        "Select Report Type",
        options=report_types,
        index=report_types.index(st.session_state.form_data.get('report_type', 'Canopy Commissioning')),
        help="Choose the type of report to generate"
    )
    
    st.session_state.form_data['report_type'] = report_type
    st.markdown("---")
    
    # General Information Section
    st.header("📋 General Information")
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            client = st.text_input(
                "Client",
                value=st.session_state.form_data.get('client', ''),
                help="Enter the client name"
            )
            
            project_number = st.text_input(
                "Project Number",
                value=st.session_state.form_data.get('project_number', ''),
                help="Enter the project number"
            )
            
            engineer = st.text_input(
                "Engineer(s)",
                value=st.session_state.form_data.get('engineer', ''),
                help="Enter the engineer name(s)"
            )
        
        with col2:
            project_name = st.text_input(
                "Project Name",
                value=st.session_state.form_data.get('project_name', ''),
                help="Enter the project name"
            )
            
            date_of_visit = st.date_input(
                "Date of Visit",
                value=st.session_state.form_data.get('date_of_visit', datetime.now().date()),
                help="Select the date of visit"
            )
    
    # Update session state with current values
    st.session_state.form_data.update({
        'client': client,
        'project_name': project_name,
        'project_number': project_number,
        'date_of_visit': date_of_visit,
        'engineer': engineer
    })
    
    # Canopy Configuration Section (only show for Canopy Commissioning reports)
    if report_type == "Canopy Commissioning":
        st.markdown("---")
        st.header("🏭 Canopy Configuration")
        
        # Number of canopies
        num_canopies = st.number_input(
            "Number of Canopies",
            min_value=1,
            max_value=20,
            value=st.session_state.form_data.get('num_canopies', 1),
            help="Specify how many canopies need to be commissioned"
        )
        
        st.session_state.form_data['num_canopies'] = num_canopies
        
        # Initialize canopies data if not exists
        if 'canopies' not in st.session_state.form_data:
            st.session_state.form_data['canopies'] = []
        
        # Ensure we have the right number of canopy entries
        while len(st.session_state.form_data['canopies']) < num_canopies:
            st.session_state.form_data['canopies'].append({
                'drawing_number': '',
                'canopy_location': '',
                'canopy_model': '',
                'with_marvel': False,
                'design_airflow': 0.0,
                'supply_airflow': 0.0,
                'number_of_sections': 1
            })
        
        # Remove excess canopy entries if number decreased
        if len(st.session_state.form_data['canopies']) > num_canopies:
            st.session_state.form_data['canopies'] = st.session_state.form_data['canopies'][:num_canopies]
        
        # Display canopy input forms
        st.subheader("📝 Canopy Details")
        
        # Canopy model options
        canopy_models = ['KVF', 'KCH-F', 'UVF', 'USR-F', 'KSR-F', 'KWF', 'UWF', 'CMW-FMOD']
        
        for i in range(num_canopies):
            with st.expander(f"Canopy {i+1}", expanded=i == 0):  # First canopy expanded by default
                # First row: Basic info
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    drawing_number = st.text_input(
                        "Drawing Number",
                        value=st.session_state.form_data['canopies'][i].get('drawing_number', ''),
                        key=f"drawing_number_{i}",
                        help="Enter the drawing number for this canopy"
                    )
                
                with col2:
                    canopy_location = st.text_input(
                        "Canopy Location",
                        value=st.session_state.form_data['canopies'][i].get('canopy_location', ''),
                        key=f"canopy_location_{i}",
                        help="Enter the location/description of this canopy"
                    )
                
                with col3:
                    canopy_model = st.selectbox(
                        "Canopy Model",
                        options=[''] + canopy_models,
                        index=canopy_models.index(st.session_state.form_data['canopies'][i].get('canopy_model', '')) + 1 
                              if st.session_state.form_data['canopies'][i].get('canopy_model', '') in canopy_models else 0,
                        key=f"canopy_model_{i}",
                        help="Select the canopy model"
                    )
                
                # Marvel toggle section
                st.markdown("---")
                with_marvel = st.toggle(
                    "🔧 With Marvel Technology",
                    value=st.session_state.form_data['canopies'][i].get('with_marvel', False),
                    key=f"with_marvel_{i}",
                    help="Toggle if this canopy includes Marvel technology"
                )
                
                # Second row: Technical specifications
                st.markdown("**Technical Specifications**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    number_of_sections = st.number_input(
                        "Number of Sections",
                        min_value=1,
                        max_value=20,
                        value=st.session_state.form_data['canopies'][i].get('number_of_sections', 1),
                        key=f"number_of_sections_{i}",
                        help="Enter the number of sections for this canopy"
                    )
                
                with col2:
                    design_airflow = st.number_input(
                        "Design Airflow (m³/s)",
                        min_value=0.0,
                        value=st.session_state.form_data['canopies'][i].get('design_airflow', 0.0),
                        step=0.1,
                        key=f"design_airflow_{i}",
                        help="Enter the design airflow in cubic meters per second"
                    )
                
                with col3:
                    supply_airflow = st.number_input(
                        "Supply Airflow (m³/s)",
                        min_value=0.0,
                        value=st.session_state.form_data['canopies'][i].get('supply_airflow', 0.0),
                        step=0.1,
                        key=f"supply_airflow_{i}",
                        help="Enter the actual supply airflow in cubic meters per second"
                    )
                
                # Section-specific data collection (only if model doesn't have 'F' in name)
                needs_section_data = canopy_model and 'F' not in canopy_model
                
                if needs_section_data and number_of_sections > 0:
                    st.markdown("---")
                    st.markdown("**📊 Section Data Collection**")
                    
                    # Initialize sections data if not exists
                    if 'sections' not in st.session_state.form_data['canopies'][i]:
                        st.session_state.form_data['canopies'][i]['sections'] = []
                    
                    # Ensure we have the right number of section entries
                    while len(st.session_state.form_data['canopies'][i]['sections']) < number_of_sections:
                        section_data = {
                            'extract_info': '',
                            'ksas': '',
                            'tab_reading': ''
                        }
                        # Add Marvel fields if Marvel is enabled
                        if with_marvel:
                            section_data.update({
                                'min_percent': 0.0,
                                'idle_percent': 0.0,
                                'design_percent': 0.0
                            })
                        st.session_state.form_data['canopies'][i]['sections'].append(section_data)
                    
                    # Remove excess section entries if number decreased
                    if len(st.session_state.form_data['canopies'][i]['sections']) > number_of_sections:
                        st.session_state.form_data['canopies'][i]['sections'] = st.session_state.form_data['canopies'][i]['sections'][:number_of_sections]
                    
                    # Update existing sections with Marvel fields if Marvel was just enabled
                    for section in st.session_state.form_data['canopies'][i]['sections']:
                        if with_marvel and 'min_percent' not in section:
                            section.update({
                                'min_percent': 0.0,
                                'idle_percent': 0.0,
                                'design_percent': 0.0
                            })
                        elif not with_marvel and 'min_percent' in section:
                            # Remove Marvel fields if Marvel was disabled
                            for key in ['min_percent', 'idle_percent', 'design_percent']:
                                section.pop(key, None)
                    
                    # Display section input forms
                    for section_idx in range(number_of_sections):
                        with st.container():
                            st.markdown(f"**Section {section_idx + 1}**")
                            
                            if with_marvel:
                                # With Marvel: 6 columns (3 basic + 3 Marvel)
                                col1, col2, col3, col4, col5, col6 = st.columns(6)
                            else:
                                # Without Marvel: 3 columns
                                col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                extract_info = st.text_input(
                                    "Extract Info",
                                    value=st.session_state.form_data['canopies'][i]['sections'][section_idx].get('extract_info', ''),
                                    key=f"extract_info_{i}_{section_idx}",
                                    help=f"Enter extract information for section {section_idx + 1}"
                                )
                            
                            with col2:
                                ksas = st.text_input(
                                    "KSA's",
                                    value=st.session_state.form_data['canopies'][i]['sections'][section_idx].get('ksas', ''),
                                    key=f"ksas_{i}_{section_idx}",
                                    help=f"Enter KSA's for section {section_idx + 1}"
                                )
                            
                            with col3:
                                tab_reading = st.text_input(
                                    "T.A.B Reading",
                                    value=st.session_state.form_data['canopies'][i]['sections'][section_idx].get('tab_reading', ''),
                                    key=f"tab_reading_{i}_{section_idx}",
                                    help=f"Enter T.A.B reading for section {section_idx + 1}"
                                )
                            
                            # Marvel-specific fields
                            if with_marvel:
                                with col4:
                                    min_percent = st.number_input(
                                        "Min (%)",
                                        min_value=0.0,
                                        max_value=100.0,
                                        value=st.session_state.form_data['canopies'][i]['sections'][section_idx].get('min_percent', 0.0),
                                        step=0.1,
                                        key=f"min_percent_{i}_{section_idx}",
                                        help=f"Enter minimum percentage for section {section_idx + 1}"
                                    )
                                
                                with col5:
                                    idle_percent = st.number_input(
                                        "Idle (%)",
                                        min_value=0.0,
                                        max_value=100.0,
                                        value=st.session_state.form_data['canopies'][i]['sections'][section_idx].get('idle_percent', 0.0),
                                        step=0.1,
                                        key=f"idle_percent_{i}_{section_idx}",
                                        help=f"Enter idle percentage for section {section_idx + 1}"
                                    )
                                
                                with col6:
                                    design_percent = st.number_input(
                                        "Design (%)",
                                        min_value=0.0,
                                        max_value=100.0,
                                        value=st.session_state.form_data['canopies'][i]['sections'][section_idx].get('design_percent', 0.0),
                                        step=0.1,
                                        key=f"design_percent_{i}_{section_idx}",
                                        help=f"Enter design percentage for section {section_idx + 1}"
                                    )
                            
                            # Update section data
                            section_data = {
                                'extract_info': extract_info,
                                'ksas': ksas,
                                'tab_reading': tab_reading
                            }
                            
                            if with_marvel:
                                section_data.update({
                                    'min_percent': min_percent,
                                    'idle_percent': idle_percent,
                                    'design_percent': design_percent
                                })
                            
                            st.session_state.form_data['canopies'][i]['sections'][section_idx] = section_data
                            
                            if section_idx < number_of_sections - 1:  # Add separator except for last section
                                st.markdown("---")
                
                # Update the canopy data
                st.session_state.form_data['canopies'][i].update({
                    'drawing_number': drawing_number,
                    'canopy_location': canopy_location,
                    'canopy_model': canopy_model,
                    'with_marvel': with_marvel,
                    'design_airflow': design_airflow,
                    'supply_airflow': supply_airflow,
                    'number_of_sections': number_of_sections
                })
    
    # Display current form data for testing
    st.markdown("---")
    st.subheader("🔍 Current Form Data (for testing)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("View collected data (JSON)", expanded=False):
            st.json(st.session_state.form_data, expanded=False)
    
    with col2:
        if report_type == "Canopy Commissioning" and st.session_state.form_data.get('canopies'):
            with st.expander("Canopy Summary", expanded=False):
                import pandas as pd
                
                canopies_df = pd.DataFrame(st.session_state.form_data['canopies'])
                if not canopies_df.empty:
                    st.dataframe(canopies_df, use_container_width=True)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🗑️ Clear Form", type="secondary"):
            st.session_state.form_data = {}
            st.rerun()
    
    with col2:
        if st.button("💾 Save Progress", type="secondary"):
            st.success("Progress saved!")
    
    with col3:
        # Placeholder for future functionality
        st.info("📝 More sections will be added as we progress")
    
    # Sidebar with project info
    with st.sidebar:
        st.header("📊 Project Status")
        
        # Progress indicator
        basic_fields = ['client', 'project_name', 'project_number', 'date_of_visit', 'engineer', 'report_type']
        completed_basic = sum(1 for key in basic_fields 
                            if st.session_state.form_data.get(key) and str(st.session_state.form_data.get(key)).strip())
        
        # Count canopy fields if applicable
        canopy_fields_completed = 0
        total_canopy_fields = 0
        
        if st.session_state.form_data.get('report_type') == "Canopy Commissioning":
            num_canopies = st.session_state.form_data.get('num_canopies', 0)
            if num_canopies > 0:
                canopies_data = st.session_state.form_data.get('canopies', [])
                
                for canopy in canopies_data:
                    # Count basic canopy fields (7 fields per canopy)
                    basic_canopy_fields = 7
                    total_canopy_fields += basic_canopy_fields
                    
                    for key, value in canopy.items():
                        if key == 'sections':
                            continue  # Handle sections separately
                        elif key == 'with_marvel':
                            # For toggle, we count it as completed regardless of True/False
                            canopy_fields_completed += 1
                        elif value and str(value).strip():
                            canopy_fields_completed += 1
                    
                    # Count section fields if applicable
                    canopy_model = canopy.get('canopy_model', '')
                    with_marvel = canopy.get('with_marvel', False)
                    num_sections = canopy.get('number_of_sections', 0)
                    
                    # Only count section fields if model doesn't have 'F' in name
                    if canopy_model and 'F' not in canopy_model and num_sections > 0:
                        fields_per_section = 3  # extract_info, ksas, tab_reading
                        if with_marvel:
                            fields_per_section += 3  # min_percent, idle_percent, design_percent
                        
                        total_section_fields = num_sections * fields_per_section
                        total_canopy_fields += total_section_fields
                        
                        # Count completed section fields
                        sections_data = canopy.get('sections', [])
                        for section in sections_data:
                            for section_key, section_value in section.items():
                                if section_value and str(section_value).strip():
                                    canopy_fields_completed += 1
        
        total_fields = len(basic_fields) + total_canopy_fields
        completed_fields = completed_basic + canopy_fields_completed
        progress = min(completed_fields / total_fields if total_fields > 0 else 0, 1.0)
        
        st.progress(progress)
        st.write(f"Completed: {completed_fields}/{total_fields} fields")
        
        st.markdown("---")
        st.subheader("🚀 Next Steps")
        st.write("1. ✅ Report Type Selection")
        st.write("2. ✅ General Information")
        
        if st.session_state.form_data.get('report_type') == "Canopy Commissioning":
            st.write("3. ✅ Canopy Configuration")
            st.write("4. ⏳ Kitchen Canopy Air Readings")
            st.write("5. ⏳ Supply Air Data")
            st.write("6. ⏳ Report Generation")
        else:
            st.write("3. ⏳ Additional Sections")
            st.write("4. ⏳ Report Generation")

if __name__ == "__main__":
    main() 