import streamlit as st
from src.config import UV_SYSTEM_CHECKLIST
from src.utils.session_manager import get_form_data, update_form_data

def render_uv_checklist():
    """Render the UV System Checklist component."""
    st.header("🔆 UV System Checks")
    
    st.markdown("""
    **Final Halton System Checks - UV System**
    
    Complete the following checklist for UV system verification:
    """)
    
    # Initialize UV checklist data if not exists
    uv_checklist_data = get_form_data('uv_checklist', {})
    
    # Create a table-like layout for the checklist
    st.markdown("### System Checks")
    
    # Create columns for the checklist table
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("**System Checks**")
    with col2:
        st.markdown("**Result**")
    
    st.markdown("---")
    
    # Render each checklist item
    for i, item in enumerate(UV_SYSTEM_CHECKLIST):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{item}**")
        
        with col2:
            # Handle different types of inputs based on the item
            if item == 'Quantity of Slaves per System':
                value = st.number_input(
                    "",
                    min_value=0,
                    value=uv_checklist_data.get(item, 12),  # Default to 12 as shown in image
                    key=f"uv_check_{i}",
                    label_visibility="collapsed"
                )
            elif item == 'UV Pressure Setpoint (Pa)':
                value = st.number_input(
                    "",
                    min_value=0,
                    value=uv_checklist_data.get(item, 50),  # Default to 50 as shown in image
                    key=f"uv_check_{i}",
                    label_visibility="collapsed"
                )
            elif item == 'Capture Jet average pressure reading (Pa)':
                value = st.text_input(
                    "",
                    value=str(uv_checklist_data.get(item, '')),
                    key=f"uv_check_{i}",
                    label_visibility="collapsed",
                    placeholder="Enter pressure reading"
                )
            else:
                # Boolean checkbox for other items
                value = st.checkbox(
                    "",
                    value=uv_checklist_data.get(item, False),
                    key=f"uv_check_{i}",
                    label_visibility="collapsed"
                )
        
        # Update the checklist data
        uv_checklist_data[item] = value
        
        if i < len(UV_SYSTEM_CHECKLIST) - 1:
            st.markdown("---")
    
    # Save the updated checklist data
    update_form_data({'uv_checklist': uv_checklist_data})
    
    # Show completion status
    st.markdown("---")
    
    # Calculate completion percentage
    completed_items = 0
    total_items = len(UV_SYSTEM_CHECKLIST)
    
    for item, value in uv_checklist_data.items():
        if item in UV_SYSTEM_CHECKLIST:
            if isinstance(value, bool) and value:
                completed_items += 1
            elif isinstance(value, (int, float)) and value > 0:
                completed_items += 1
            elif isinstance(value, str) and value.strip():
                completed_items += 1
    
    completion_percentage = (completed_items / total_items) * 100 if total_items > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Completed Items", f"{completed_items}/{total_items}")
    with col2:
        st.metric("Completion", f"{completion_percentage:.1f}%")
    with col3:
        if completion_percentage == 100:
            st.success("✅ UV System Checks Complete")
        elif completion_percentage > 50:
            st.warning("⚠️ UV System Checks In Progress")
        else:
            st.error("❌ UV System Checks Incomplete")

def get_uv_checklist_summary():
    """Get a summary of UV checklist completion for templates."""
    uv_checklist_data = get_form_data('uv_checklist', {})
    
    summary = {
        'total_items': len(UV_SYSTEM_CHECKLIST),
        'completed_items': 0,
        'completion_percentage': 0.0,
        'checklist_items': []
    }
    
    for item in UV_SYSTEM_CHECKLIST:
        value = uv_checklist_data.get(item, '')
        is_completed = False
        
        if isinstance(value, bool):
            is_completed = value
            display_value = "✓" if value else ""
        elif isinstance(value, (int, float)):
            is_completed = value > 0
            display_value = str(value) if value > 0 else ""
        elif isinstance(value, str):
            is_completed = bool(value.strip())
            display_value = value.strip()
        else:
            display_value = ""
        
        if is_completed:
            summary['completed_items'] += 1
        
        summary['checklist_items'].append({
            'item': item,
            'value': display_value,
            'completed': is_completed
        })
    
    summary['completion_percentage'] = (summary['completed_items'] / summary['total_items']) * 100 if summary['total_items'] > 0 else 0
    
    return summary 