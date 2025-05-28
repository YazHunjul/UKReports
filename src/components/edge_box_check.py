import streamlit as st
from src.utils.session_manager import update_form_data, get_form_data

def render_edge_box_check():
    """Render the Edge box check section."""
    st.header("🔌 Edge Box Check (Optional)")
    st.markdown("Complete this section if an Edge box is present in the system.")
    
    # Get current edge box data
    edge_data = get_form_data('edge_box', {})
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Edge Installed checkbox
        edge_installed = st.checkbox(
            "Edge Installed",
            value=edge_data.get('edge_installed', False),
            key="edge_installed"
        )
        
        # Edge ID input
        edge_id = st.text_input(
            "Edge ID",
            value=edge_data.get('edge_id', ''),
            placeholder="e.g., GB9999",
            key="edge_id"
        )
        
        # Edge 4G Status
        edge_4g_status = st.selectbox(
            "Edge 4G Status",
            options=["", "Online", "Offline", "Online / Offline"],
            index=0 if edge_data.get('edge_4g_status', '') == '' else 
                  ["", "Online", "Offline", "Online / Offline"].index(edge_data.get('edge_4g_status', '')),
            key="edge_4g_status"
        )
    
    with col2:
        # LAN Connection Available checkbox
        lan_connection = st.checkbox(
            "LAN Connection Available",
            value=edge_data.get('lan_connection', False),
            key="lan_connection"
        )
        
        # Modbus Operation
        modbus_operation = st.checkbox(
            "Modbus Operation",
            value=edge_data.get('modbus_operation', False),
            key="modbus_operation"
        )
        
        # Modbus Operation Value (if Modbus Operation is checked)
        modbus_value = ""
        if modbus_operation:
            modbus_value = st.number_input(
                "Modbus Operation Value",
                min_value=0,
                max_value=100,
                value=edge_data.get('modbus_value', 50),
                key="modbus_value"
            )
    
    # Update session state with edge box data
    edge_box_data = {
        'edge_box': {
            'edge_installed': edge_installed,
            'edge_id': edge_id,
            'edge_4g_status': edge_4g_status,
            'lan_connection': lan_connection,
            'modbus_operation': modbus_operation,
            'modbus_value': modbus_value if modbus_operation else None
        }
    }
    
    update_form_data(edge_box_data)
    
    # Show a summary if any edge box data is filled
    if any([edge_installed, edge_id, edge_4g_status, lan_connection, modbus_operation]):
        st.info("✅ Edge box information has been recorded.")
    
    return edge_box_data['edge_box'] 