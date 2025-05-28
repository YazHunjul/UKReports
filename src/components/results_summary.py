import streamlit as st
import pandas as pd
from src.utils.session_manager import get_form_data
from src.config import is_cxw_model, is_cmwf_model, calculate_cxw_flowrate, calculate_cmwf_flowrate, calculate_free_area_from_grill_size, calculate_free_area_from_slot_dimensions, get_k_factor

def render_results_summary():
    """Render the Results Summary tables for Extract and Supply Air."""
    st.header("📊 Results Summary")
    
    form_data = get_form_data()
    canopies_data = form_data.get('canopies', [])
    
    if not canopies_data:
        st.info("ℹ️ No canopy data available for results summary.")
        return
    
    # Prepare data for Extract Air table
    extract_data = []
    supply_data = []
    
    for canopy in canopies_data:
        canopy_model = canopy.get('canopy_model', '')
        drawing_number = canopy.get('drawing_number', '')
        design_airflow = canopy.get('design_airflow', 0.0)
        supply_airflow = canopy.get('supply_airflow', 0.0)
        sections = canopy.get('sections', [])
        
        if not canopy_model or not sections:
            continue
        
        # Calculate actual flowrates based on model type
        actual_extract_flowrate = 0.0
        actual_supply_flowrate = 0.0
        
        if is_cxw_model(canopy_model):
            # CXW models use anemometer readings and grill size
            grill_size = canopy.get('grill_size', '')
            free_area = calculate_free_area_from_grill_size(grill_size)
            
            for section in sections:
                anemometer_reading = section.get('anemometer_reading', 0.0)
                if anemometer_reading and free_area:
                    _, flowrate_m3s = calculate_cxw_flowrate(free_area, anemometer_reading)
                    actual_extract_flowrate += flowrate_m3s
                    
        elif is_cmwf_model(canopy_model):
            # CMWF models use anemometer readings and slot dimensions
            slot_length = canopy.get('slot_length', 0)
            slot_width = canopy.get('slot_width', 85)
            free_area = calculate_free_area_from_slot_dimensions(slot_length, slot_width)
            
            for section in sections:
                anemometer_reading = section.get('anemometer_reading', 0.0)
                if anemometer_reading and free_area:
                    _, flowrate_m3s = calculate_cmwf_flowrate(free_area, anemometer_reading)
                    actual_extract_flowrate += flowrate_m3s
                    
        else:
            # Standard models use K-factor calculations
            for section in sections:
                # Extract air calculation
                extract_ksa = section.get('extract_ksa')
                extract_tab_reading = section.get('extract_tab_reading', '')
                
                if extract_ksa and extract_tab_reading:
                    try:
                        k_factor = get_k_factor(canopy_model, extract_ksa)
                        tab_value = float(extract_tab_reading)
                        flowrate_m3h = k_factor * (tab_value ** 0.5)
                        actual_extract_flowrate += flowrate_m3h / 3600  # Convert to m³/s
                    except:
                        pass
                
                # Supply air calculation (for models with 'F' in name)
                if 'F' in canopy_model and 'supply_tab_reading' in section:
                    supply_tab_reading = section.get('supply_tab_reading', '')
                    
                    if supply_tab_reading:
                        try:
                            # Use same K-factor logic as in document generator
                            from src.config import is_length_based_model
                            if is_length_based_model(canopy_model):
                                supply_k_factor = get_k_factor(canopy_model, section.get('supply_plenum_length'))
                            else:
                                supply_k_factor = get_k_factor(canopy_model, extract_ksa)
                            
                            tab_value = float(supply_tab_reading)
                            flowrate_m3h = supply_k_factor * (tab_value ** 0.5)
                            actual_supply_flowrate += flowrate_m3h / 3600  # Convert to m³/s
                        except:
                            pass
        
        # Calculate percentages
        extract_percentage = (actual_extract_flowrate / design_airflow * 100) if design_airflow > 0 else 0
        supply_percentage = (actual_supply_flowrate / supply_airflow * 100) if supply_airflow > 0 else 0
        
        # Add to extract data
        extract_data.append({
            'Drawing Number': drawing_number,
            'Design Flow Rate (m³/s)': f"{design_airflow:.2f}",
            'Actual Flowrate (m³/s)': f"{actual_extract_flowrate:.3f}",
            'Percentage of Design %': f"{extract_percentage:.1f}%"
        })
        
        # Add to supply data (only for models with supply air)
        if 'F' in canopy_model and supply_airflow > 0:
            supply_data.append({
                'Drawing Number': drawing_number,
                'Design Flow Rate (m³/s)': f"{supply_airflow:.2f}",
                'Actual Flowrate (m³/s)': f"{actual_supply_flowrate:.3f}",
                'Percentage of Design %': f"{supply_percentage:.1f}%"
            })
    
    # Calculate totals
    total_extract_design = sum(float(row['Design Flow Rate (m³/s)']) for row in extract_data)
    total_extract_actual = sum(float(row['Actual Flowrate (m³/s)']) for row in extract_data)
    total_extract_percentage = (total_extract_actual / total_extract_design * 100) if total_extract_design > 0 else 0
    
    total_supply_design = sum(float(row['Design Flow Rate (m³/s)']) for row in supply_data)
    total_supply_actual = sum(float(row['Actual Flowrate (m³/s)']) for row in supply_data)
    total_supply_percentage = (total_supply_actual / total_supply_design * 100) if total_supply_design > 0 else 0
    
    # Render Extract Air table
    st.subheader("🔵 Extract Air")
    if extract_data:
        extract_df = pd.DataFrame(extract_data)
        st.dataframe(extract_df, use_container_width=True, hide_index=True)
        
        # Show totals separately
        st.markdown("**TOTALS:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Design Flow Rate", f"{total_extract_design:.2f} m³/s")
        with col2:
            st.metric("Total Actual Flowrate", f"{total_extract_actual:.3f} m³/s")
        with col3:
            st.metric("Total Percentage", f"{total_extract_percentage:.1f}%")
    else:
        st.info("ℹ️ No extract air data available.")
    
    # Render Supply Air table
    st.subheader("🔴 Supply Air")
    if supply_data:
        supply_df = pd.DataFrame(supply_data)
        st.dataframe(supply_df, use_container_width=True, hide_index=True)
        
        # Show totals separately
        st.markdown("**TOTALS:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Design Flow Rate", f"{total_supply_design:.2f} m³/s")
        with col2:
            st.metric("Total Actual Flowrate", f"{total_supply_actual:.3f} m³/s")
        with col3:
            st.metric("Total Percentage", f"{total_supply_percentage:.1f}%")
    else:
        st.info("ℹ️ No supply air data available.") 