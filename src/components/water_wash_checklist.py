import streamlit as st
from src.config import WATER_WASH_SYSTEM_CHECKLIST
from src.utils.session_manager import get_form_data, update_form_data

def render_water_wash_checklist_for_canopy(canopy_index: int, canopy_model: str):
    """Render Water Wash System Checklist for a specific canopy."""
    st.markdown("💧 **Water Wash System Checklist**")
    
    # Initialize Water Wash checklist data for this specific canopy if not exists
    canopy_wash_key = f'canopy_{canopy_index}_water_wash_checklist'
    canopy_wash_data = get_form_data(canopy_wash_key, {})
    
    # Render each checklist item in a compact format
    for i, item in enumerate(WATER_WASH_SYSTEM_CHECKLIST):
        # Handle different types of inputs based on the item
        if item == 'Cold water pressure (BAR)':
            value = st.number_input(
                f"📊 {item}",
                min_value=0.0,
                step=0.1,
                value=canopy_wash_data.get(item, None),  # Default to None (empty)
                key=f"canopy_{canopy_index}_wash_check_{i}",
                help="Enter cold water pressure in BAR"
            )
        elif item == 'Hot water pressure (BAR)':
            value = st.number_input(
                f"📊 {item}",
                min_value=0.0,
                step=0.1,
                value=canopy_wash_data.get(item, None),  # Default to None (empty)
                key=f"canopy_{canopy_index}_wash_check_{i}",
                help="Enter hot water pressure in BAR"
            )
        elif item == 'Hot water temperature (°C)':
            value = st.number_input(
                f"🌡️ {item}",
                min_value=0.0,
                step=1.0,
                value=canopy_wash_data.get(item, None),  # Default to None (empty)
                key=f"canopy_{canopy_index}_wash_check_{i}",
                help="Enter hot water temperature in Celsius"
            )
        elif item == 'Capture Jet average Pressure (Pa)':
            value = st.text_input(
                f"📊 {item}",
                value=canopy_wash_data.get(item, ''),  # Default to empty
                key=f"canopy_{canopy_index}_wash_check_{i}",
                placeholder="Enter pressure reading",
                help="Enter capture jet average pressure reading"
            )
        else:
            # Boolean checkbox for other items - default to False (unchecked)
            value = st.checkbox(
                f"☐ {item}",
                value=canopy_wash_data.get(item, False),  # Default to False (unchecked)
                key=f"canopy_{canopy_index}_wash_check_{i}",
                help=f"Check if {item.lower()} is completed"
            )
        
        # Update the checklist data for this canopy
        canopy_wash_data[item] = value
    
    # Save the updated checklist data for this canopy
    update_form_data({canopy_wash_key: canopy_wash_data})
    
    # Show compact completion status
    completed_items = 0
    total_items = len(WATER_WASH_SYSTEM_CHECKLIST)
    
    for item, value in canopy_wash_data.items():
        if item in WATER_WASH_SYSTEM_CHECKLIST:
            if isinstance(value, bool) and value:
                completed_items += 1
            elif isinstance(value, (int, float)) and value is not None and value > 0:
                completed_items += 1
            elif isinstance(value, str) and value.strip():
                completed_items += 1
    
    completion_percentage = (completed_items / total_items) * 100 if total_items > 0 else 0
    
    # Compact status display
    if completion_percentage == 100:
        st.success(f"✅ Water Wash Checks Complete ({completed_items}/{total_items})")
    elif completion_percentage > 50:
        st.warning(f"⚠️ Water Wash Checks In Progress ({completed_items}/{total_items} - {completion_percentage:.0f}%)")
    else:
        st.error(f"❌ Water Wash Checks Incomplete ({completed_items}/{total_items} - {completion_percentage:.0f}%)")

def get_water_wash_checklist_summary():
    """Get a summary of Water Wash checklist completion for templates."""
    # This would be used for global water wash checklist if needed
    pass 