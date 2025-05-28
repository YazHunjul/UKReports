import streamlit as st
from src.config import CANOPY_MODELS, MAX_CANOPIES, MAX_SECTIONS, get_k_factor, is_length_based_model, get_available_ksas, is_cxw_model, is_cmwf_model, is_cmwi_model, is_cmw_anemometer_model, is_cmw_model, calculate_cxw_flowrate, calculate_cmwf_flowrate, calculate_cmwi_flowrate, calculate_free_area_from_grill_size, calculate_free_area_from_slot_dimensions, is_uv_model, UV_SYSTEM_CHECKLIST, WATER_WASH_SYSTEM_CHECKLIST
from src.utils.session_manager import get_form_data, update_form_data, initialize_canopy_data, initialize_section_data
from src.components.water_wash_checklist import render_water_wash_checklist_for_canopy

import pandas as pd

def render_canopy_configuration():
    """Render the canopy configuration component."""
    st.header("🏭 Canopy Configuration")
    
    # Initialize session state for number of canopies if not exists
    if 'num_canopies' not in st.session_state:
        st.session_state.num_canopies = get_form_data('num_canopies', 1)
    
    # Number of canopies
    num_canopies = st.number_input(
        "Number of Canopies",
        min_value=1,
        max_value=MAX_CANOPIES,
        key="num_canopies",
        help="Specify how many canopies need to be commissioned"
    )
    
    # Get the value from session state
    num_canopies_value = st.session_state.get('num_canopies', 1)
    
    update_form_data({'num_canopies': num_canopies_value})
    initialize_canopy_data(num_canopies_value)
    
    # Display canopy input forms
    st.subheader("📝 Canopy Details")
    
    for i in range(num_canopies_value):
        with st.expander(f"Canopy {i+1}", expanded=i == 0):
            render_single_canopy(i)

def render_single_canopy(canopy_index: int):
    """Render a single canopy configuration form."""
    canopies = get_form_data('canopies', [])
    if canopy_index >= len(canopies):
        return
    
    canopy = canopies[canopy_index]
    
    # Initialize session state values if not exists
    drawing_key = f"drawing_number_{canopy_index}"
    location_key = f"canopy_location_{canopy_index}"
    model_key = f"canopy_model_{canopy_index}"
    
    if drawing_key not in st.session_state:
        st.session_state[drawing_key] = canopy.get('drawing_number', '')
    if location_key not in st.session_state:
        st.session_state[location_key] = canopy.get('canopy_location', '')
    if model_key not in st.session_state:
        st.session_state[model_key] = canopy.get('canopy_model', '')
    
    # First row: Basic info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        drawing_number = st.text_input(
            "Drawing Number",
            key=drawing_key,
            help="Enter the drawing number for this canopy"
        )
    
    with col2:
        canopy_location = st.text_input(
            "Canopy Location",
            key=location_key,
            help="Enter the location/description of this canopy"
        )
    
    with col3:
        canopy_model = st.selectbox(
            "Canopy Model",
            options=[''] + CANOPY_MODELS,
            key=model_key,
            help="Select the canopy model"
        )
    
    # Get values from session state
    drawing_number_value = st.session_state.get(drawing_key, '')
    canopy_location_value = st.session_state.get(location_key, '')
    canopy_model_value = st.session_state.get(model_key, '')
    
    # Initialize default values for all variables that will be used later
    design_airflow_value = 0.0
    supply_airflow_value = 0.0
    number_of_sections_value = 1
    canopy_length_value = None
    grill_size_value = ''
    slot_length = 0
    slot_width = 85
    
    # Marvel and UV toggle section
    st.markdown("---")
    
    # Initialize toggle keys
    marvel_key = f"with_marvel_{canopy_index}"
    uv_key = f"with_uv_checks_{canopy_index}"
    water_wash_key = f"with_water_wash_checks_{canopy_index}"
    
    if marvel_key not in st.session_state:
        st.session_state[marvel_key] = canopy.get('with_marvel', False)
    if uv_key not in st.session_state:
        st.session_state[uv_key] = canopy.get('with_uv_checks', False)
    if water_wash_key not in st.session_state:
        st.session_state[water_wash_key] = canopy.get('with_water_wash_checks', False)
    
    # Create columns for toggles based on canopy model type
    if canopy_model_value and is_uv_model(canopy_model_value):
        # UV models get Marvel + UV toggles
        col1, col2 = st.columns(2)
        
        with col1:
            with_marvel = st.toggle(
                "🔧 With Marvel Technology",
                key=marvel_key,
                help="Toggle if this canopy includes Marvel technology"
            )
        
        with col2:
            with_uv_checks = st.toggle(
                "🔆 UV System Checks",
                key=uv_key,
                help="Toggle to enable UV system checklist for this canopy"
            )
        
        with_water_wash_checks = False
        
        # UV checklist section (only if UV checks are enabled)
        if st.session_state.get(uv_key, False):
            render_uv_checklist_for_canopy(canopy_index, canopy_model_value)
            
    elif canopy_model_value and is_cmw_model(canopy_model_value):
        # CMW models get Marvel + Water Wash toggles
        col1, col2 = st.columns(2)
        
        with col1:
            with_marvel = st.toggle(
                "🔧 With Marvel Technology",
                key=marvel_key,
                help="Toggle if this canopy includes Marvel technology"
            )
        
        with col2:
            with_water_wash_checks = st.toggle(
                "💧 Water Wash System Checks",
                key=water_wash_key,
                help="Toggle to enable Water Wash system checklist for this canopy"
            )
        
        with_uv_checks = False
        
        # Water Wash checklist section (only if Water Wash checks are enabled)
        if st.session_state.get(water_wash_key, False):
            render_water_wash_checklist_for_canopy(canopy_index, canopy_model_value)
            
    else:
        # Other models get only Marvel toggle
        with_marvel = st.toggle(
            "🔧 With Marvel Technology",
            key=marvel_key,
            help="Toggle if this canopy includes Marvel technology"
        )
        with_uv_checks = False
        with_water_wash_checks = False
    
    # Get toggle values from session state
    with_marvel_value = st.session_state.get(marvel_key, False)
    with_uv_checks_value = st.session_state.get(uv_key, False)
    with_water_wash_checks_value = st.session_state.get(water_wash_key, False)
    
    # Technical specifications
    st.markdown("**Technical Specifications**")
    
    # Handle CXW models specially
    if canopy_model_value and is_cxw_model(canopy_model_value):
        # CXW models need grill size and quantity of grills
        col1, col2, col3 = st.columns(3)
        
        # Initialize session state for CXW fields
        grill_key = f"grill_size_{canopy_index}"
        grills_key = f"number_of_grills_{canopy_index}"
        design_key = f"design_airflow_{canopy_index}"
        
        if grill_key not in st.session_state:
            st.session_state[grill_key] = canopy.get('grill_size', '')
        if grills_key not in st.session_state:
            st.session_state[grills_key] = canopy.get('number_of_sections', 1)
        if design_key not in st.session_state:
            st.session_state[design_key] = canopy.get('design_airflow', 0.0)
        
        with col1:
            grill_size = st.text_input(
                "Grill Size (mm)",
                key=grill_key,
                help="Enter the grill size (e.g., '600x600')"
            )
        
        with col2:
            number_of_sections = st.number_input(
                "Quantity of Grills",
                min_value=1,
                max_value=MAX_SECTIONS,
                key=grills_key,
                help="Enter the number of grills for this canopy"
            )
        
        with col3:
            design_airflow = st.number_input(
                "Design Flowrate (m³/s)",
                min_value=0.0,
                step=0.1,
                key=design_key,
                help="Enter the design flowrate in cubic meters per second"
            )
        
        # Get values from session state
        grill_size_value = st.session_state.get(grill_key, '')
        number_of_sections_value = st.session_state.get(grills_key, 1)
        design_airflow_value = st.session_state.get(design_key, 0.0)
        
        # CXW models don't have supply airflow
        supply_airflow_value = 0.0
        canopy_length_value = None
        
    # Handle CMWF models specially
    elif canopy_model_value and is_cmwf_model(canopy_model_value):
        # CMWF models need slot dimensions and quantity of sections
        col1, col2 = st.columns(2)
        
        # Initialize session state for CMWF fields
        slot_length_key = f"slot_length_{canopy_index}"
        slot_width_key = f"slot_width_{canopy_index}"
        
        if slot_length_key not in st.session_state:
            st.session_state[slot_length_key] = canopy.get('slot_length', 0)
        if slot_width_key not in st.session_state:
            st.session_state[slot_width_key] = canopy.get('slot_width', 85)
        
        with col1:
            slot_length = st.number_input(
                "Length of Slot (mm)",
                min_value=0,
                step=50,
                key=slot_length_key,
                help="Enter the length of the slot in millimeters"
            )
        
        with col2:
            slot_width = st.number_input(
                "Width of Slot (mm)",
                min_value=0,
                step=5,
                key=slot_width_key,
                help="Enter the width of the slot in millimeters"
            )
        
        col1, col2, col3 = st.columns(3)
        
        # Initialize session state for other CMWF fields
        sections_key = f"number_of_sections_{canopy_index}"
        design_key = f"design_airflow_{canopy_index}"
        supply_key = f"supply_airflow_{canopy_index}"
        
        if sections_key not in st.session_state:
            st.session_state[sections_key] = canopy.get('number_of_sections', 1)
        if design_key not in st.session_state:
            st.session_state[design_key] = canopy.get('design_airflow', 0.0)
        if supply_key not in st.session_state:
            st.session_state[supply_key] = canopy.get('supply_airflow', 0.0)
        
        with col1:
            number_of_sections = st.number_input(
                "Quantity of Canopy Sections",
                min_value=1,
                max_value=MAX_SECTIONS,
                key=sections_key,
                help="Enter the number of sections for this canopy"
            )
        
        with col2:
            design_airflow = st.number_input(
                "Design Flowrate (m³/s)",
                min_value=0.0,
                step=0.1,
                key=design_key,
                help="Enter the design flowrate in cubic meters per second"
            )
        
        with col3:
            supply_airflow = st.number_input(
                "Supply Airflow (m³/s)",
                min_value=0.0,
                step=0.1,
                key=supply_key,
                help="Enter the actual supply airflow in cubic meters per second"
            )
        
        # Update values from session state
        slot_length = st.session_state.get(slot_length_key, 0)
        slot_width = st.session_state.get(slot_width_key, 85)
        number_of_sections_value = st.session_state.get(sections_key, 1)
        design_airflow_value = st.session_state.get(design_key, 0.0)
        supply_airflow_value = st.session_state.get(supply_key, 0.0)
        canopy_length_value = None
        
    # Handle CMWI models specially (extract only, no supply)
    elif canopy_model_value and is_cmwi_model(canopy_model_value):
        # CMWI models need slot dimensions and quantity of sections (extract only)
        col1, col2 = st.columns(2)
        
        # Initialize session state for CMWI fields
        slot_length_key = f"slot_length_{canopy_index}"
        slot_width_key = f"slot_width_{canopy_index}"
        
        if slot_length_key not in st.session_state:
            st.session_state[slot_length_key] = canopy.get('slot_length', 0)
        if slot_width_key not in st.session_state:
            st.session_state[slot_width_key] = canopy.get('slot_width', 85)
        
        with col1:
            slot_length = st.number_input(
                "Length of Slot (mm)",
                min_value=0,
                step=50,
                key=slot_length_key,
                help="Enter the length of the slot in millimeters"
            )
        
        with col2:
            slot_width = st.number_input(
                "Width of Slot (mm)",
                min_value=0,
                step=5,
                key=slot_width_key,
                help="Enter the width of the slot in millimeters"
            )
        
        col1, col2 = st.columns(2)
        
        # Initialize session state for other CMWI fields
        sections_key = f"number_of_sections_{canopy_index}"
        design_key = f"design_airflow_{canopy_index}"
        
        if sections_key not in st.session_state:
            st.session_state[sections_key] = canopy.get('number_of_sections', 1)
        if design_key not in st.session_state:
            st.session_state[design_key] = canopy.get('design_airflow', 0.0)
        
        with col1:
            number_of_sections = st.number_input(
                "Quantity of Canopy Sections",
                min_value=1,
                max_value=MAX_SECTIONS,
                key=sections_key,
                help="Enter the number of sections for this canopy"
            )
        
        with col2:
            design_airflow = st.number_input(
                "Design Flowrate (m³/s)",
                min_value=0.0,
                step=0.1,
                key=design_key,
                help="Enter the design flowrate in cubic meters per second"
            )
        
        # Update values from session state
        slot_length = st.session_state.get(slot_length_key, 0)
        slot_width = st.session_state.get(slot_width_key, 85)
        number_of_sections_value = st.session_state.get(sections_key, 1)
        design_airflow_value = st.session_state.get(design_key, 0.0)
        supply_airflow_value = 0.0  # CMWI models don't have supply airflow
        canopy_length_value = None
    
    # Handle length-based vs section-based models differently
    elif canopy_model_value and is_length_based_model(canopy_model_value):
        # Length-based models (CMW-F, CMW-I, KVD, KVV)
        col1, col2, col3 = st.columns(3)
        
        # Initialize session state for length-based fields
        length_key = f"canopy_length_{canopy_index}"
        design_key = f"design_airflow_{canopy_index}"
        supply_key = f"supply_airflow_{canopy_index}"
        
        if length_key not in st.session_state:
            st.session_state[length_key] = canopy.get('canopy_length', 1000)
        if design_key not in st.session_state:
            st.session_state[design_key] = canopy.get('design_airflow', 0.0)
        if supply_key not in st.session_state:
            st.session_state[supply_key] = canopy.get('supply_airflow', 0.0)
        
        with col1:
            canopy_length = st.number_input(
                "Canopy Length (mm)",
                min_value=1000,
                max_value=4000,
                step=500,
                key=length_key,
                help="Enter the canopy length in millimeters (1000-4000mm)"
            )
        
        with col2:
            design_airflow = st.number_input(
                "Design Airflow (m³/s)",
                min_value=0.0,
                step=0.1,
                key=design_key,
                help="Enter the design airflow in cubic meters per second"
            )
        
        with col3:
            supply_airflow = st.number_input(
                "Supply Airflow (m³/s)",
                min_value=0.0,
                step=0.1,
                key=supply_key,
                help="Enter the actual supply airflow in cubic meters per second"
            )
        
        # Update values from session state
        canopy_length_value = st.session_state.get(length_key, 1000)
        design_airflow_value = st.session_state.get(design_key, 0.0)
        supply_airflow_value = st.session_state.get(supply_key, 0.0)
        number_of_sections_value = 1  # Length-based models don't use sections
        
    else:
        # Section-based models
        col1, col2, col3 = st.columns(3)
        
        # Initialize session state for section-based fields
        sections_key = f"number_of_sections_{canopy_index}"
        design_key = f"design_airflow_{canopy_index}"
        supply_key = f"supply_airflow_{canopy_index}"
        
        if sections_key not in st.session_state:
            st.session_state[sections_key] = canopy.get('number_of_sections', 1)
        if design_key not in st.session_state:
            st.session_state[design_key] = canopy.get('design_airflow', 0.0)
        if supply_key not in st.session_state:
            st.session_state[supply_key] = canopy.get('supply_airflow', 0.0)
        
        with col1:
            number_of_sections = st.number_input(
                "Number of Sections",
                min_value=1,
                max_value=MAX_SECTIONS,
                key=sections_key,
                help="Enter the number of sections for this canopy"
            )
        
        with col2:
            design_airflow = st.number_input(
                "Design Airflow (m³/s)",
                min_value=0.0,
                step=0.1,
                key=design_key,
                help="Enter the design airflow in cubic meters per second"
            )
        
        with col3:
            supply_airflow = st.number_input(
                "Supply Airflow (m³/s)",
                min_value=0.0,
                step=0.1,
                key=supply_key,
                help="Enter the actual supply airflow in cubic meters per second"
            )
        
        # Update values from session state
        number_of_sections_value = st.session_state.get(sections_key, 1)
        design_airflow_value = st.session_state.get(design_key, 0.0)
        supply_airflow_value = st.session_state.get(supply_key, 0.0)
        canopy_length_value = None  # Section-based models don't use length
    
    # Update the canopy data
    canopy_data = {
        'drawing_number': drawing_number_value,
        'canopy_location': canopy_location_value,
        'canopy_model': canopy_model_value,
        'with_marvel': with_marvel_value,
        'with_uv_checks': with_uv_checks_value,
        'with_water_wash_checks': with_water_wash_checks_value,
        'design_airflow': design_airflow_value,
        'supply_airflow': supply_airflow_value,
        'number_of_sections': number_of_sections_value
    }
    
    # Add length for length-based models
    if canopy_model_value and is_length_based_model(canopy_model_value):
        canopy_data['canopy_length'] = canopy_length_value
    
    # Add grill size for CXW models
    if canopy_model_value and is_cxw_model(canopy_model_value):
        canopy_data['grill_size'] = grill_size_value
    
    # Add slot dimensions for CMWF and CMWI models
    if canopy_model_value and (is_cmwf_model(canopy_model_value) or is_cmwi_model(canopy_model_value)):
        canopy_data['slot_length'] = slot_length
        canopy_data['slot_width'] = slot_width
    
    get_form_data('canopies')[canopy_index].update(canopy_data)
    
    # Section-specific data collection
    render_section_data(canopy_index, canopy_model_value, with_marvel_value, number_of_sections_value)

def render_section_data(canopy_index: int, canopy_model: str, with_marvel: bool, number_of_sections: int):
    """Render section data collection for a canopy."""
    # Show section data for all models except length-based ones
    # CMW anemometer models (CMWF, CMWI) should show section data like CXW
    needs_section_data = (canopy_model and not is_length_based_model(canopy_model))
    
    if needs_section_data and number_of_sections > 0:
        st.markdown("---")
        st.markdown("**📊 Section Data Collection**")
        
        # Initialize section data first
        initialize_section_data(canopy_index, number_of_sections, with_marvel)
        
        # Display section input forms
        for section_idx in range(number_of_sections):
            with st.container():
                render_single_section(canopy_index, section_idx, with_marvel, canopy_model)
                
                if section_idx < number_of_sections - 1:  # Add separator except for last section
                    st.markdown("---")
        

    else:
        if not canopy_model:
            st.info("ℹ️ Please select a canopy model to see section options")
        elif is_length_based_model(canopy_model):
            st.info(f"ℹ️ Model '{canopy_model}' uses length-based configuration (no sections)")
        elif number_of_sections <= 0:
            st.info("ℹ️ Please set number of sections > 0")

def render_single_section(canopy_index: int, section_idx: int, with_marvel: bool, canopy_model: str):
    """Render a single section data form."""
    # For CXW models, use "Grill" instead of "Section"
    # For CMWF/CMWI models, use "Section" but with different fields
    if is_cxw_model(canopy_model):
        st.markdown(f"**Grill {section_idx + 1}**")
    elif is_cmwf_model(canopy_model) or is_cmwi_model(canopy_model):
        st.markdown(f"**Section {section_idx + 1}**")
    else:
        st.markdown(f"**Section {section_idx + 1}**")
    
    canopy = get_form_data('canopies')[canopy_index]
    section = canopy['sections'][section_idx]
    
    # Handle CXW models specially
    if is_cxw_model(canopy_model):
        # CXW models need anemometer reading - free area is calculated from grill size
        st.markdown("**Extract Air Readings**")
        
        # Get grill size from canopy data
        canopy = get_form_data('canopies')[canopy_index]
        grill_size = canopy.get('grill_size', '')
        
        # Calculate free area from grill size
        free_area = calculate_free_area_from_grill_size(grill_size)
        
        col1, col2 = st.columns(2)
        
        # Initialize session state for CXW section fields
        anemometer_key = f"anemometer_reading_{canopy_index}_{section_idx}"
        if anemometer_key not in st.session_state:
            st.session_state[anemometer_key] = section.get('anemometer_reading', 0.0)
        
        with col1:
            anemometer_reading = st.number_input(
                "Anemometer Reading (Average m/s)",
                min_value=0.0,
                step=0.1,
                key=anemometer_key,
                help=f"Enter the average anemometer reading for grill {section_idx + 1}"
            )
        
        with col2:
            # Display calculated free area (read-only)
            if free_area > 0:
                st.write(f"**Free Area: {free_area:.4f} m²**")
            else:
                st.info("ℹ️ Free area will be calculated from grill size")
        
        # Get value from session state
        anemometer_reading = st.session_state.get(anemometer_key, 0.0)
        
        # Calculate and display flowrates
        if anemometer_reading > 0 and free_area > 0:
            flowrate_m3h, flowrate_m3s = calculate_cxw_flowrate(free_area, anemometer_reading)
            st.write(f"**Flowrate: {flowrate_m3h:.2f} m³/h ({flowrate_m3s:.3f} m³/s)**")
        
        # Update section data for CXW
        section_data = {
            'anemometer_reading': anemometer_reading,
            'free_area': free_area  # Store calculated free area
        }
        
        # Marvel fields for CXW models (if enabled)
        if with_marvel:
            st.markdown("**Marvel Technology Settings**")
            col1, col2, col3 = st.columns(3)
            
            # Initialize session state for Marvel fields
            min_key = f"min_percent_{canopy_index}_{section_idx}"
            idle_key = f"idle_percent_{canopy_index}_{section_idx}"
            design_key = f"design_m3s_{canopy_index}_{section_idx}"
            
            if min_key not in st.session_state:
                st.session_state[min_key] = section.get('min_percent', 0.0)
            if idle_key not in st.session_state:
                st.session_state[idle_key] = section.get('idle_percent', 0.0)
            if design_key not in st.session_state:
                st.session_state[design_key] = section.get('design_m3s', 0.0)
            
            with col1:
                min_percent = st.number_input(
                    "Min (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=0.1,
                    key=min_key,
                    help=f"Enter minimum percentage for grill {section_idx + 1}"
                )
            
            with col2:
                idle_percent = st.number_input(
                    "Idle (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=0.1,
                    key=idle_key,
                    help=f"Enter idle percentage for grill {section_idx + 1}"
                )
            
            with col3:
                design_m3s = st.number_input(
                    "Design (m³/s)",
                    min_value=0.0,
                    step=0.01,
                    key=design_key,
                    help=f"Enter design flowrate in m³/s for grill {section_idx + 1}"
                )
            
            # Get values from session state
            min_percent = st.session_state.get(min_key, 0.0)
            idle_percent = st.session_state.get(idle_key, 0.0)
            design_m3s = st.session_state.get(design_key, 0.0)
            
            # Add Marvel fields to CXW section data
            section_data.update({
                'min_percent': min_percent,
                'idle_percent': idle_percent,
                'design_m3s': design_m3s
            })
    
    # Handle CMWF models specially
    elif is_cmwf_model(canopy_model):
        # CMWF models need anemometer reading - free area is calculated from slot dimensions
        st.markdown("**Extract Air Readings**")
        
        # Get slot dimensions from canopy data
        canopy = get_form_data('canopies')[canopy_index]
        slot_length = canopy.get('slot_length', 0.0)
        slot_width = canopy.get('slot_width', 85.0)
        
        # Calculate free area from slot dimensions
        free_area = calculate_free_area_from_slot_dimensions(slot_length, slot_width)
        
        col1, col2 = st.columns(2)
        
        # Initialize session state for CMWF extract fields
        anemometer_key = f"anemometer_reading_{canopy_index}_{section_idx}"
        if anemometer_key not in st.session_state:
            st.session_state[anemometer_key] = section.get('anemometer_reading', 0.0)
        
        with col1:
            anemometer_reading = st.number_input(
                "Anemometer Reading (Average m/s)",
                min_value=0.0,
                step=0.1,
                key=anemometer_key,
                help=f"Enter the average anemometer reading for section {section_idx + 1}"
            )
        
        with col2:
            # Display calculated free area (read-only)
            if free_area > 0:
                st.write(f"**Free Area: {free_area:.4f} m²**")
            else:
                st.info("ℹ️ Free area will be calculated from slot dimensions")
        
        # Get value from session state
        anemometer_reading = st.session_state.get(anemometer_key, 0.0)
        
        # Calculate and display flowrates
        if anemometer_reading > 0 and free_area > 0:
            flowrate_m3h, flowrate_m3s = calculate_cmwf_flowrate(free_area, anemometer_reading)
            st.write(f"**Flowrate: {flowrate_m3h:.2f} m³/h ({flowrate_m3s:.3f} m³/s)**")
        
        # Supply Air Readings for CMWF (F models have supply)
        st.markdown("**Supply Air Readings**")
        
        col1, col2 = st.columns(2)
        
        # Initialize session state for CMWF supply fields
        supply_anemometer_key = f"supply_anemometer_reading_{canopy_index}_{section_idx}"
        if supply_anemometer_key not in st.session_state:
            st.session_state[supply_anemometer_key] = section.get('supply_anemometer_reading', 0.0)
        
        with col1:
            supply_anemometer_reading = st.number_input(
                "Supply Anemometer Reading (Average m/s)",
                min_value=0.0,
                step=0.1,
                key=supply_anemometer_key,
                help=f"Enter the supply anemometer reading for section {section_idx + 1}"
            )
        
        with col2:
            # Display calculated free area for supply (same as extract)
            if free_area > 0:
                st.write(f"**Free Area: {free_area:.4f} m²**")
            else:
                st.info("ℹ️ Free area will be calculated from slot dimensions")
        
        # Get value from session state
        supply_anemometer_reading = st.session_state.get(supply_anemometer_key, 0.0)
        
        # Calculate and display supply flowrates
        supply_flowrate_m3h = 0.0
        supply_flowrate_m3s = 0.0
        if supply_anemometer_reading > 0 and free_area > 0:
            supply_flowrate_m3h, supply_flowrate_m3s = calculate_cmwf_flowrate(free_area, supply_anemometer_reading)
            st.write(f"**Supply Flowrate: {supply_flowrate_m3h:.2f} m³/h ({supply_flowrate_m3s:.3f} m³/s)**")
        
        # Update section data for CMWF
        section_data = {
            'anemometer_reading': anemometer_reading,
            'supply_anemometer_reading': supply_anemometer_reading,
            'free_area': free_area  # Store calculated free area
        }
        
        # Marvel fields for CMWF models (if enabled)
        if with_marvel:
            st.markdown("**Marvel Technology Settings**")
            col1, col2, col3 = st.columns(3)
            
            # Initialize session state for Marvel fields
            min_key = f"min_percent_{canopy_index}_{section_idx}"
            idle_key = f"idle_percent_{canopy_index}_{section_idx}"
            design_key = f"design_m3s_{canopy_index}_{section_idx}"
            
            if min_key not in st.session_state:
                st.session_state[min_key] = section.get('min_percent', 0.0)
            if idle_key not in st.session_state:
                st.session_state[idle_key] = section.get('idle_percent', 0.0)
            if design_key not in st.session_state:
                st.session_state[design_key] = section.get('design_m3s', 0.0)
            
            with col1:
                min_percent = st.number_input(
                    "Min (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=0.1,
                    key=min_key,
                    help=f"Enter minimum percentage for section {section_idx + 1}"
                )
            
            with col2:
                idle_percent = st.number_input(
                    "Idle (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=0.1,
                    key=idle_key,
                    help=f"Enter idle percentage for section {section_idx + 1}"
                )
            
            with col3:
                design_m3s = st.number_input(
                    "Design (m³/s)",
                    min_value=0.0,
                    step=0.01,
                    key=design_key,
                    help=f"Enter design flowrate in m³/s for section {section_idx + 1}"
                )
            
            # Get values from session state
            min_percent = st.session_state.get(min_key, 0.0)
            idle_percent = st.session_state.get(idle_key, 0.0)
            design_m3s = st.session_state.get(design_key, 0.0)
            
            # Add Marvel fields to CMWF section data
            section_data.update({
                'min_percent': min_percent,
                'idle_percent': idle_percent,
                'design_m3s': design_m3s
            })
    
    # Handle CMWI models specially (extract only)
    elif is_cmwi_model(canopy_model):
        # CMWI models need anemometer reading - free area is calculated from slot dimensions
        st.markdown("**Extract Air Readings**")
        
        # Get slot dimensions from canopy data
        canopy = get_form_data('canopies')[canopy_index]
        slot_length = canopy.get('slot_length', 0.0)
        slot_width = canopy.get('slot_width', 85.0)
        
        # Calculate free area from slot dimensions
        free_area = calculate_free_area_from_slot_dimensions(slot_length, slot_width)
        
        col1, col2 = st.columns(2)
        
        # Initialize session state for CMWI extract fields
        anemometer_key = f"anemometer_reading_{canopy_index}_{section_idx}"
        if anemometer_key not in st.session_state:
            st.session_state[anemometer_key] = section.get('anemometer_reading', 0.0)
        
        with col1:
            anemometer_reading = st.number_input(
                "Anemometer Reading (Average m/s)",
                min_value=0.0,
                step=0.1,
                key=anemometer_key,
                help=f"Enter the average anemometer reading for section {section_idx + 1}"
            )
        
        with col2:
            # Display calculated free area (read-only)
            if free_area > 0:
                st.write(f"**Free Area: {free_area:.4f} m²**")
            else:
                st.info("ℹ️ Free area will be calculated from slot dimensions")
        
        # Get value from session state
        anemometer_reading = st.session_state.get(anemometer_key, 0.0)
        
        # Calculate and display flowrates
        if anemometer_reading > 0 and free_area > 0:
            flowrate_m3h, flowrate_m3s = calculate_cmwi_flowrate(free_area, anemometer_reading)
            st.write(f"**Flowrate: {flowrate_m3h:.2f} m³/h ({flowrate_m3s:.3f} m³/s)**")
        
        # Update section data for CMWI (extract only)
        section_data = {
            'anemometer_reading': anemometer_reading,
            'free_area': free_area  # Store calculated free area
        }
        
        # Marvel fields for CMWI models (if enabled)
        if with_marvel:
            st.markdown("**Marvel Technology Settings**")
            col1, col2, col3 = st.columns(3)
            
            # Initialize session state for Marvel fields
            min_key = f"min_percent_{canopy_index}_{section_idx}"
            idle_key = f"idle_percent_{canopy_index}_{section_idx}"
            design_key = f"design_m3s_{canopy_index}_{section_idx}"
            
            if min_key not in st.session_state:
                st.session_state[min_key] = section.get('min_percent', 0.0)
            if idle_key not in st.session_state:
                st.session_state[idle_key] = section.get('idle_percent', 0.0)
            if design_key not in st.session_state:
                st.session_state[design_key] = section.get('design_m3s', 0.0)
            
            with col1:
                min_percent = st.number_input(
                    "Min (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=0.1,
                    key=min_key,
                    help=f"Enter minimum percentage for section {section_idx + 1}"
                )
            
            with col2:
                idle_percent = st.number_input(
                    "Idle (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=0.1,
                    key=idle_key,
                    help=f"Enter idle percentage for section {section_idx + 1}"
                )
            
            with col3:
                design_m3s = st.number_input(
                    "Design (m³/s)",
                    min_value=0.0,
                    step=0.01,
                    key=design_key,
                    help=f"Enter design flowrate in m³/s for section {section_idx + 1}"
                )
            
            # Get values from session state
            min_percent = st.session_state.get(min_key, 0.0)
            idle_percent = st.session_state.get(idle_key, 0.0)
            design_m3s = st.session_state.get(design_key, 0.0)
            
            # Add Marvel fields to CMWI section data
            section_data.update({
                'min_percent': min_percent,
                'idle_percent': idle_percent,
                'design_m3s': design_m3s
            })
    
    else:
        # Standard models (non-CXW, non-CMWF)
        # Determine what fields to show based on model name
        has_f_in_name = 'F' in canopy_model if canopy_model else False
        
        # Extract Info section (always present)
        st.markdown("**Extract Info**")
        col1, col2 = st.columns(2)
        
        # Initialize session state for extract fields
        extract_ksa_key = f"extract_ksa_{canopy_index}_{section_idx}"
        extract_tab_key = f"extract_tab_reading_{canopy_index}_{section_idx}"
        
        if extract_ksa_key not in st.session_state:
            if canopy_model:
                available_ksas = get_available_ksas(canopy_model)
                if available_ksas:
                    default_ksa = section.get('extract_ksa', available_ksas[0])
                    st.session_state[extract_ksa_key] = default_ksa if default_ksa in available_ksas else available_ksas[0]
                else:
                    st.session_state[extract_ksa_key] = None
            else:
                st.session_state[extract_ksa_key] = None
        
        if extract_tab_key not in st.session_state:
            st.session_state[extract_tab_key] = section.get('extract_tab_reading', '')
        
        with col1:
            # KSA selection dropdown for extract
            if canopy_model:
                available_ksas = get_available_ksas(canopy_model)
                if available_ksas:
                    extract_ksa = st.selectbox(
                        "Section KSA's",
                        options=available_ksas,
                        key=extract_ksa_key,
                        help=f"Select the number of KSAs for extract in section {section_idx + 1}"
                    )
                    # Calculate and display K-factor for extract
                    k_factor = get_k_factor(canopy_model, extract_ksa)
                    if k_factor > 0:
                        st.write(f"**K-Factor: {k_factor:.1f}**")
                else:
                    extract_ksa = None
            else:
                extract_ksa = None
        
        with col2:
            extract_tab_reading = st.text_input(
                "T.A.B Reading",
                key=extract_tab_key,
                help=f"Enter T.A.B reading for extract in section {section_idx + 1}"
            )
        
        # Get values from session state
        extract_ksa = st.session_state.get(extract_ksa_key, None)
        extract_tab_reading = st.session_state.get(extract_tab_key, '')
        
        # Supply Info section (only for models with 'F' in name)
        if has_f_in_name:
            st.markdown("**Supply Info**")
            col1, col2 = st.columns(2)
            
            # Initialize session state for supply fields
            supply_plenum_key = f"supply_plenum_length_{canopy_index}_{section_idx}"
            supply_tab_key = f"supply_tab_reading_{canopy_index}_{section_idx}"
            
            if supply_plenum_key not in st.session_state:
                plenum_lengths = [1000, 1500, 2000, 2500, 3000, 3500, 4000]
                default_plenum = section.get('supply_plenum_length', 1000)
                st.session_state[supply_plenum_key] = default_plenum if default_plenum in plenum_lengths else 1000
            
            if supply_tab_key not in st.session_state:
                st.session_state[supply_tab_key] = section.get('supply_tab_reading', '')
            
            with col1:
                # Plenum Length dropdown for supply
                plenum_lengths = [1000, 1500, 2000, 2500, 3000, 3500, 4000]  # Standard plenum lengths
                supply_plenum_length = st.selectbox(
                    "Plenum Length",
                    options=plenum_lengths,
                    key=supply_plenum_key,
                    help=f"Select the plenum length for supply in section {section_idx + 1}"
                )
            
            with col2:
                supply_tab_reading = st.text_input(
                    "T.A.B Point Reading",
                    key=supply_tab_key,
                    help=f"Enter T.A.B point reading for supply in section {section_idx + 1}"
                )
            
            # Get values from session state
            supply_plenum_length = st.session_state.get(supply_plenum_key, 1000)
            supply_tab_reading = st.session_state.get(supply_tab_key, '')
        else:
            supply_plenum_length = None
            supply_tab_reading = None
        
        # Marvel-specific fields (if enabled)
        if with_marvel:
            st.markdown("**Marvel Technology Settings**")
            col1, col2, col3 = st.columns(3)
            
            # Initialize session state for Marvel fields
            min_key = f"min_percent_{canopy_index}_{section_idx}"
            idle_key = f"idle_percent_{canopy_index}_{section_idx}"
            design_key = f"design_m3s_{canopy_index}_{section_idx}"
            
            if min_key not in st.session_state:
                st.session_state[min_key] = section.get('min_percent', 0.0)
            if idle_key not in st.session_state:
                st.session_state[idle_key] = section.get('idle_percent', 0.0)
            if design_key not in st.session_state:
                st.session_state[design_key] = section.get('design_m3s', 0.0)
            
            with col1:
                min_percent = st.number_input(
                    "Min (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=0.1,
                    key=min_key,
                    help=f"Enter minimum percentage for section {section_idx + 1}"
                )
            
            with col2:
                idle_percent = st.number_input(
                    "Idle (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=0.1,
                    key=idle_key,
                    help=f"Enter idle percentage for section {section_idx + 1}"
                )
            
            with col3:
                design_m3s = st.number_input(
                    "Design (m³/s)",
                    min_value=0.0,
                    step=0.01,
                    key=design_key,
                    help=f"Enter design flowrate in m³/s for section {section_idx + 1}"
                )
            
            # Get values from session state
            min_percent = st.session_state.get(min_key, 0.0)
            idle_percent = st.session_state.get(idle_key, 0.0)
            design_m3s = st.session_state.get(design_key, 0.0)
        else:
            min_percent = 0.0
            idle_percent = 0.0
            design_m3s = 0.0
        
        # Update section data for standard models
        section_data = {
            'extract_ksa': extract_ksa,
            'extract_tab_reading': extract_tab_reading
        }
        
        # Add supply fields only for models with 'F' in name
        if has_f_in_name:
            section_data.update({
                'supply_plenum_length': supply_plenum_length,
                'supply_tab_reading': supply_tab_reading
            })
        
        if with_marvel:
            section_data.update({
                'min_percent': min_percent,
                'idle_percent': idle_percent,
                'design_m3s': design_m3s
            })
    
    canopy['sections'][section_idx] = section_data 

def render_canopy_data_tables(canopy_index: int, canopy_model: str):
    """Render canopy data in table format based on model type."""
    canopy = get_form_data('canopies')[canopy_index]
    
    st.markdown("---")
    st.markdown("### 📋 Kitchen Canopy Air Readings")
    st.markdown(f"**Canopy {canopy_index + 1}**")
    
    # Handle CXW models specially
    if is_cxw_model(canopy_model):
        # CXW Extract Air Data Table
        st.markdown("#### Extract Air Data")
        
        extract_data = {
            'Drawing Number': [canopy.get('drawing_number', '')],
            'Canopy Location': [canopy.get('canopy_location', '')],
            'Canopy Model': [canopy.get('canopy_model', '')],
            'Design Flowrate (m³/s)': [canopy.get('design_airflow', 0.0)],
            'Quantity of Grills': [canopy.get('number_of_sections', 0)],
            'Grill Size (mm)': [canopy.get('grill_size', '')],
            'Calculation': ['Qv = A x m/s']
        }
        
        extract_df = pd.DataFrame(extract_data)
        st.table(extract_df)
        
        # CXW Extract Air Readings Table
        st.markdown("#### Extract Air Readings")
        
        sections_data = canopy.get('sections', [])
        if sections_data:
            readings_data = []
            grill_size = canopy.get('grill_size', '')
            
            for i, section in enumerate(sections_data):
                anemometer_reading = section.get('anemometer_reading', 0.0)
                
                # Calculate free area from grill size for each section
                free_area = calculate_free_area_from_grill_size(grill_size)
                
                # Calculate flowrate using CXW formula
                flowrate_m3h, flowrate_m3s = calculate_cxw_flowrate(free_area, anemometer_reading)
                
                readings_data.append({
                    'Anemometer Reading (Average m/s)': f"{anemometer_reading:.1f}" if anemometer_reading else '',
                    'Free Area (m²)': f"{free_area:.4f}" if free_area else '',
                    'Flowrate (m³/h)': f"{flowrate_m3h:.2f}" if flowrate_m3h else '',
                    'Flowrate (m³/s)': f"{flowrate_m3s:.3f}" if flowrate_m3s else ''
                })
            
            # Add total row
            total_flowrate_m3s = sum(float(row['Flowrate (m³/s)']) if row['Flowrate (m³/s)'] else 0 for row in readings_data)
            readings_data.append({
                'Anemometer Reading (Average m/s)': '',
                'Free Area (m²)': '',
                'Flowrate (m³/h)': 'Total Flowrate',
                'Flowrate (m³/s)': f"{total_flowrate_m3s:.3f}m³/s"
            })
            
            readings_df = pd.DataFrame(readings_data)
            st.table(readings_df)
        
        return  # Exit early for CXW models
    
    # Handle CMWF models specially
    elif is_cmwf_model(canopy_model):
        # CMWF Extract Air Data Table
        st.markdown("#### Extract Air Data")
        
        extract_data = {
            'Drawing Number': [canopy.get('drawing_number', '')],
            'Canopy Location': [canopy.get('canopy_location', '')],
            'Canopy Model': [canopy.get('canopy_model', '')],
            'Design Flowrate (m³/s)': [canopy.get('design_airflow', 0.0)],
            'Quantity of Canopy Sections': [canopy.get('number_of_sections', 0)],
            'Length of Slot (mm)': [canopy.get('slot_length', 0.0)],
            'Width of Slot (mm)': [canopy.get('slot_width', 85.0)],
            'Calculation': ['Qv = A x m/s']
        }
        
        extract_df = pd.DataFrame(extract_data)
        st.table(extract_df)
        
        # CMWF Extract Air Readings Table
        st.markdown("#### Extract Air Readings")
        
        sections_data = canopy.get('sections', [])
        if sections_data:
            readings_data = []
            slot_length = canopy.get('slot_length', 0.0)
            slot_width = canopy.get('slot_width', 85.0)
            
            for i, section in enumerate(sections_data):
                anemometer_reading = section.get('anemometer_reading', 0.0)
                
                # Calculate free area from slot dimensions for each section
                free_area = calculate_free_area_from_slot_dimensions(slot_length, slot_width)
                
                # Calculate flowrate using CMWF formula
                flowrate_m3h, flowrate_m3s = calculate_cmwf_flowrate(free_area, anemometer_reading)
                
                readings_data.append({
                    'Anemometer Reading (Average m/s)': f"{anemometer_reading:.1f}" if anemometer_reading else '',
                    'Free Area (m²)': f"{free_area:.4f}" if free_area else '',
                    'Flowrate (m³/h)': f"{flowrate_m3h:.2f}" if flowrate_m3h else '',
                    'Flowrate (m³/s)': f"{flowrate_m3s:.3f}" if flowrate_m3s else ''
                })
            
            # Add total row
            total_flowrate_m3s = sum(float(row['Flowrate (m³/s)']) if row['Flowrate (m³/s)'] else 0 for row in readings_data)
            readings_data.append({
                'Anemometer Reading (Average m/s)': '',
                'Free Area (m²)': '',
                'Flowrate (m³/h)': 'Total Flowrate',
                'Flowrate (m³/s)': f"{total_flowrate_m3s:.3f}m³/s"
            })
            
            readings_df = pd.DataFrame(readings_data)
            st.table(readings_df)
        
        # CMWF Supply Air Data Table
        st.markdown("#### Supply Air Data")
        
        supply_data = {
            'Drawing Number': [canopy.get('drawing_number', '')],
            'Canopy Location': [canopy.get('canopy_location', '')],
            'Canopy Model': [canopy.get('canopy_model', '')],
            'Design Flowrate (m³/s)': [canopy.get('supply_airflow', 0.0)],
            'Quantity of Canopy Sections': [canopy.get('number_of_sections', 0)],
            'Length of Slot (mm)': [canopy.get('slot_length', 0.0)],
            'Width of Slot (mm)': [canopy.get('slot_width', 85.0)],
            'Calculation': ['Qv = A x m/s']
        }
        
        supply_df = pd.DataFrame(supply_data)
        st.table(supply_df)
        
        # CMWF Supply Air Readings Table
        st.markdown("#### Supply Air Readings")
        
        if sections_data:
            supply_readings_data = []
            
            for i, section in enumerate(sections_data):
                supply_anemometer_reading = section.get('supply_anemometer_reading', 0.0)
                
                # Calculate free area from slot dimensions for each section
                free_area = calculate_free_area_from_slot_dimensions(slot_length, slot_width)
                
                # Calculate supply flowrate using CMWF formula
                supply_flowrate_m3h, supply_flowrate_m3s = calculate_cmwf_flowrate(free_area, supply_anemometer_reading)
                
                supply_readings_data.append({
                    'Anemometer Reading (Average m/s)': f"{supply_anemometer_reading:.1f}" if supply_anemometer_reading else '',
                    'Free Area (m²)': f"{free_area:.4f}" if free_area else '',
                    'Flowrate (m³/h)': f"{supply_flowrate_m3h:.2f}" if supply_flowrate_m3h else '',
                    'Flowrate (m³/s)': f"{supply_flowrate_m3s:.3f}" if supply_flowrate_m3s else ''
                })
            
            # Add total row
            total_supply_flowrate_m3s = sum(float(row['Flowrate (m³/s)']) if row['Flowrate (m³/s)'] else 0 for row in supply_readings_data)
            supply_readings_data.append({
                'Anemometer Reading (Average m/s)': '',
                'Free Area (m²)': '',
                'Flowrate (m³/h)': 'Total Flowrate',
                'Flowrate (m³/s)': f"{total_supply_flowrate_m3s:.3f}m³/s"
            })
            
            supply_readings_df = pd.DataFrame(supply_readings_data)
            st.table(supply_readings_df)
        
        return  # Exit early for CMWF models
    
    # Handle CMWI models specially (extract only)
    elif is_cmwi_model(canopy_model):
        # CMWI Extract Air Data Table
        st.markdown("#### Extract Air Data")
        
        extract_data = {
            'Drawing Number': [canopy.get('drawing_number', '')],
            'Canopy Location': [canopy.get('canopy_location', '')],
            'Canopy Model': [canopy.get('canopy_model', '')],
            'Design Flowrate (m³/s)': [canopy.get('design_airflow', 0.0)],
            'Quantity of Canopy Sections': [canopy.get('number_of_sections', 0)],
            'Length of Slot (mm)': [canopy.get('slot_length', 0.0)],
            'Width of Slot (mm)': [canopy.get('slot_width', 85.0)],
            'Calculation': ['Qv = A x m/s']
        }
        
        extract_df = pd.DataFrame(extract_data)
        st.table(extract_df)
        
        # CMWI Extract Air Readings Table
        st.markdown("#### Extract Air Readings")
        
        sections_data = canopy.get('sections', [])
        if sections_data:
            readings_data = []
            slot_length = canopy.get('slot_length', 0.0)
            slot_width = canopy.get('slot_width', 85.0)
            
            for i, section in enumerate(sections_data):
                anemometer_reading = section.get('anemometer_reading', 0.0)
                
                # Calculate free area from slot dimensions for each section
                free_area = calculate_free_area_from_slot_dimensions(slot_length, slot_width)
                
                # Calculate flowrate using CMWI formula
                flowrate_m3h, flowrate_m3s = calculate_cmwi_flowrate(free_area, anemometer_reading)
                
                readings_data.append({
                    'Anemometer Reading (Average m/s)': f"{anemometer_reading:.1f}" if anemometer_reading else '',
                    'Free Area (m²)': f"{free_area:.4f}" if free_area else '',
                    'Flowrate (m³/h)': f"{flowrate_m3h:.2f}" if flowrate_m3h else '',
                    'Flowrate (m³/s)': f"{flowrate_m3s:.3f}" if flowrate_m3s else ''
                })
            
            # Add total row
            total_flowrate_m3s = sum(float(row['Flowrate (m³/s)']) if row['Flowrate (m³/s)'] else 0 for row in readings_data)
            readings_data.append({
                'Anemometer Reading (Average m/s)': '',
                'Free Area (m²)': '',
                'Flowrate (m³/h)': 'Total Flowrate',
                'Flowrate (m³/s)': f"{total_flowrate_m3s:.3f}m³/s"
            })
            
            readings_df = pd.DataFrame(readings_data)
            st.table(readings_df)
        
        return  # Exit early for CMWI models
    
    # Standard models (non-CXW, non-CMWF)
    has_f_in_name = 'F' in canopy_model if canopy_model else False
    
    # Extract Air Data Table (always present)
    st.markdown("#### Extract Air Data")
    
    # Create extract air data summary
    extract_data = {
        'Drawing Number': [canopy.get('drawing_number', '')],
        'Canopy Location': [canopy.get('canopy_location', '')],
        'Canopy Model': [canopy.get('canopy_model', '')],
        'Design Flowrate (m³/s)': [canopy.get('design_airflow', 0.0)],
        'Quantity of Canopy Sections': [canopy.get('number_of_sections', 0)],
        'Quantity of KSA\'s per Section': ['Variable'],
        'Canopy K-Factor (m³/h)': ['Variable'],
        'Calculation': ['Qv = Kf x √Pa']
    }
    
    extract_df = pd.DataFrame(extract_data)
    st.table(extract_df)
    
    # Extract Air Readings Table
    st.markdown("#### Extract Air Readings")
    
    sections_data = canopy.get('sections', [])
    if sections_data:
        readings_data = []
        for i, section in enumerate(sections_data):
            extract_ksa = section.get('extract_ksa', '')
            extract_tab_reading = section.get('extract_tab_reading', '')
            k_factor = get_k_factor(canopy_model, extract_ksa) if extract_ksa else 0.0
            
            # Calculate flowrate if we have tab reading and k-factor
            flowrate_m3h = 0.0
            flowrate_m3s = 0.0
            if extract_tab_reading and k_factor:
                try:
                    tab_value = float(extract_tab_reading)
                    flowrate_m3h = k_factor * (tab_value ** 0.5)  # Qv = Kf x √Pa
                    flowrate_m3s = flowrate_m3h / 3600  # Convert to m³/s
                except:
                    pass
            
            readings_data.append({
                'T.A.B Point Reading (Pa)': extract_tab_reading,
                'K-Factor (m³/h)': f"{k_factor:.1f}" if k_factor else '',
                'Flowrate (m³/h)': f"{flowrate_m3h:.2f}" if flowrate_m3h else '',
                'Flowrate (m³/s)': f"{flowrate_m3s:.3f}" if flowrate_m3s else ''
            })
        
        # Add total row
        total_flowrate_m3s = sum(float(row['Flowrate (m³/s)']) if row['Flowrate (m³/s)'] else 0 for row in readings_data)
        readings_data.append({
            'T.A.B Point Reading (Pa)': '',
            'K-Factor (m³/h)': '',
            'Flowrate (m³/h)': 'Total Flowrate',
            'Flowrate (m³/s)': f"{total_flowrate_m3s:.3f}m³/s"
        })
        
        readings_df = pd.DataFrame(readings_data)
        st.table(readings_df)
    
    # Supply Air Data Table (only for models with 'F' in name)
    if has_f_in_name:
        st.markdown("#### Supply Air Data")
        
        supply_data = {
            'Drawing Number': [canopy.get('drawing_number', '')],
            'Canopy Location': [canopy.get('canopy_location', '')],
            'Canopy Model': [canopy.get('canopy_model', '')],
            'Design Flowrate (m³/s)': [canopy.get('supply_airflow', 0.0)],
            'Quantity of Canopy Sections': [canopy.get('number_of_sections', 0)],
            'Plenum Length per Section (mm)': ['Variable'],
            'Canopy K-Factor (m³/h)': ['Variable'],
            'Calculation': ['Qv = Kf x √Pa']
        }
        
        supply_df = pd.DataFrame(supply_data)
        st.table(supply_df)
        
        # Supply Air Readings Table
        st.markdown("#### Supply Air Readings")
        
        if sections_data:
            supply_readings_data = []
            for i, section in enumerate(sections_data):
                supply_plenum_length = section.get('supply_plenum_length', '')
                supply_tab_reading = section.get('supply_tab_reading', '')
                
                # For supply air K-factor calculation:
                # - Length-based models (CMW-F, CMW-I, KVD, KVV): use plenum length
                # - Section-based models (KVF, UVF, etc.): use same K-factor as extract (based on KSAs)
                if is_length_based_model(canopy_model):
                    k_factor = get_k_factor(canopy_model, supply_plenum_length) if supply_plenum_length else 0.0
                else:
                    # For section-based models, use the same K-factor as extract air (based on KSAs)
                    extract_ksa = section.get('extract_ksa', '')
                    k_factor = get_k_factor(canopy_model, extract_ksa) if extract_ksa else 0.0
                
                # Calculate flowrate if we have tab reading and k-factor
                flowrate_m3h = 0.0
                flowrate_m3s = 0.0
                if supply_tab_reading and k_factor:
                    try:
                        tab_value = float(supply_tab_reading)
                        flowrate_m3h = k_factor * (tab_value ** 0.5)  # Qv = Kf x √Pa
                        flowrate_m3s = flowrate_m3h / 3600  # Convert to m³/s
                    except:
                        pass
                
                supply_readings_data.append({
                    'T.A.B Point Reading (Pa)': supply_tab_reading,
                    'K-Factor (m³/h)': f"{k_factor:.1f}" if k_factor else '',
                    'Flowrate (m³/h)': f"{flowrate_m3h:.2f}" if flowrate_m3h else '',
                    'Flowrate (m³/s)': f"{flowrate_m3s:.3f}" if flowrate_m3s else ''
                })
            
            # Add total row
            total_supply_flowrate_m3s = sum(float(row['Flowrate (m³/s)']) if row['Flowrate (m³/s)'] else 0 for row in supply_readings_data)
            supply_readings_data.append({
                'T.A.B Point Reading (Pa)': '',
                'K-Factor (m³/h)': '',
                'Flowrate (m³/h)': 'Total Flowrate',
                'Flowrate (m³/s)': f"{total_supply_flowrate_m3s:.3f}m³/s"
            })
            
            supply_readings_df = pd.DataFrame(supply_readings_data)
            st.table(supply_readings_df)

def render_uv_checklist_for_canopy(canopy_index: int, canopy_model: str):
    """Render UV System Checklist for a specific canopy."""
    st.markdown("🔆 **UV System Checklist**")
    
    # Initialize UV checklist data for this specific canopy if not exists
    canopy_uv_key = f'canopy_{canopy_index}_uv_checklist'
    canopy_uv_data = get_form_data(canopy_uv_key, {})
    
    # Render each checklist item in a compact format
    for i, item in enumerate(UV_SYSTEM_CHECKLIST):
        # Handle different types of inputs based on the item
        if item == 'Quantity of Slaves per System':
            value = st.number_input(
                f"📊 {item}",
                min_value=0,
                value=canopy_uv_data.get(item, None),  # Default to None (empty)
                key=f"canopy_{canopy_index}_uv_check_{i}",
                help="Enter quantity of slaves per system"
            )
        elif item == 'UV Pressure Setpoint (Pa)':
            value = st.number_input(
                f"📊 {item}",
                min_value=0,
                value=canopy_uv_data.get(item, None),  # Default to None (empty)
                key=f"canopy_{canopy_index}_uv_check_{i}",
                help="Enter UV pressure setpoint in Pa"
            )
        elif item == 'Capture Jet average pressure reading (Pa)':
            value = st.text_input(
                f"📊 {item}",
                value=canopy_uv_data.get(item, ''),  # Default to empty
                key=f"canopy_{canopy_index}_uv_check_{i}",
                placeholder="Enter pressure reading",
                help="Enter capture jet average pressure reading"
            )
        else:
            # Boolean checkbox for other items - default to False (unchecked)
            value = st.checkbox(
                f"☐ {item}",
                value=canopy_uv_data.get(item, False),  # Default to False (unchecked)
                key=f"canopy_{canopy_index}_uv_check_{i}",
                help=f"Check if {item.lower()} is completed"
            )
        
        # Update the checklist data for this canopy
        canopy_uv_data[item] = value
    
    # Save the updated checklist data for this canopy
    update_form_data({canopy_uv_key: canopy_uv_data})
    
    # Show compact completion status
    completed_items = 0
    total_items = len(UV_SYSTEM_CHECKLIST)
    
    for item, value in canopy_uv_data.items():
        if item in UV_SYSTEM_CHECKLIST:
            if isinstance(value, bool) and value:
                completed_items += 1
            elif isinstance(value, (int, float)) and value is not None and value > 0:
                completed_items += 1
            elif isinstance(value, str) and value.strip():
                completed_items += 1
    
    completion_percentage = (completed_items / total_items) * 100 if total_items > 0 else 0
    
    # Compact status display
    if completion_percentage == 100:
        st.success(f"✅ UV Checks Complete ({completed_items}/{total_items})")
    elif completion_percentage > 50:
        st.warning(f"⚠️ UV Checks In Progress ({completed_items}/{total_items} - {completion_percentage:.0f}%)")
    else:
        st.error(f"❌ UV Checks Incomplete ({completed_items}/{total_items} - {completion_percentage:.0f}%)") 