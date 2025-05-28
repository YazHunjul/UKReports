import streamlit as st
import json
import base64
import urllib.parse
from typing import Dict, Any, List

def initialize_session_state():
    """Initialize session state for form data if not exists."""
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}

def update_form_data(data: Dict[str, Any]):
    """Update form data in session state."""
    st.session_state.form_data.update(data)

def get_form_data(key: str = None, default: Any = None):
    """Get form data from session state."""
    if key is None:
        return st.session_state.form_data
    return st.session_state.form_data.get(key, default)

def clear_form_data():
    """Clear all form data from session state."""
    st.session_state.form_data = {}

def serialize_form_data_to_url() -> str:
    """Serialize current form data to a URL-safe string."""
    try:
        # Get current form data
        form_data = get_form_data()
        
        # Convert to JSON string
        json_str = json.dumps(form_data, default=str)
        
        # Encode to base64 for URL safety
        encoded_data = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        
        # URL encode for safety
        url_safe_data = urllib.parse.quote(encoded_data)
        
        return url_safe_data
    except Exception as e:
        st.error(f"Error serializing form data: {e}")
        return ""

def deserialize_form_data_from_url(url_data: str) -> bool:
    """Deserialize form data from URL parameter and load into session state."""
    try:
        # URL decode
        decoded_url = urllib.parse.unquote(url_data)
        
        # Base64 decode
        json_str = base64.b64decode(decoded_url.encode('utf-8')).decode('utf-8')
        
        # Parse JSON
        form_data = json.loads(json_str)
        
        # Load into session state
        st.session_state.form_data = form_data
        
        return True
    except Exception as e:
        st.error(f"Error loading shared data: {e}")
        return False

def get_shareable_url() -> str:
    """Generate a shareable URL with current form data."""
    try:
        # Get current URL without query parameters
        base_url = st.get_option("browser.serverAddress") or "localhost"
        port = st.get_option("server.port") or 8501
        
        # Serialize form data
        serialized_data = serialize_form_data_to_url()
        
        if serialized_data:
            # Create shareable URL
            shareable_url = f"http://{base_url}:{port}/?data={serialized_data}"
            return shareable_url
        else:
            return ""
    except Exception as e:
        st.error(f"Error generating shareable URL: {e}")
        return ""

def load_data_from_url_params():
    """Load form data from URL parameters if present."""
    try:
        # Get URL parameters
        query_params = st.query_params
        
        if "data" in query_params:
            url_data = query_params["data"]
            if deserialize_form_data_from_url(url_data):
                st.success("✅ Shared data loaded successfully!")
                # Clear the URL parameter to avoid reloading on refresh
                st.query_params.clear()
                return True
    except Exception as e:
        st.error(f"Error loading data from URL: {e}")
    
    return False

def has_marvel_technology() -> bool:
    """Check if any canopy in the project has Marvel technology enabled."""
    canopies = get_form_data('canopies', [])
    return any(canopy.get('with_marvel', False) for canopy in canopies)

def has_uv_technology() -> bool:
    """Check if any canopy in the project has UV technology (UV models)."""
    canopies = get_form_data('canopies', [])
    from src.config import is_uv_model
    return any(is_uv_model(canopy.get('canopy_model', '')) for canopy in canopies)

def initialize_canopy_data(num_canopies: int):
    """Initialize canopy data structure."""
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

def initialize_section_data(canopy_index: int, num_sections: int, with_marvel: bool):
    """Initialize section data for a specific canopy."""
    canopy = st.session_state.form_data['canopies'][canopy_index]
    canopy_model = canopy.get('canopy_model', '')
    has_f_in_name = 'F' in canopy_model if canopy_model else False
    
    if 'sections' not in canopy:
        canopy['sections'] = []
    
    # Ensure we have the right number of section entries
    while len(canopy['sections']) < num_sections:
        section_data = {
            'extract_ksa': None,
            'extract_tab_reading': ''
        }
        
        # Add supply fields for models with 'F' in name
        if has_f_in_name:
            section_data.update({
                'supply_plenum_length': 1000,
                'supply_tab_reading': ''
            })
        
        # Add Marvel fields if Marvel is enabled
        if with_marvel:
            section_data.update({
                'min_percent': 0.0,
                'idle_percent': 0.0,
                'design_percent': 0.0
            })
        canopy['sections'].append(section_data)
    
    # Remove excess section entries if number decreased
    if len(canopy['sections']) > num_sections:
        canopy['sections'] = canopy['sections'][:num_sections]
    
    # Update existing sections with correct fields based on model
    for section in canopy['sections']:
        # Ensure extract fields exist
        if 'extract_ksa' not in section:
            section['extract_ksa'] = None
        if 'extract_tab_reading' not in section:
            section['extract_tab_reading'] = ''
        
        # Add/remove supply fields based on model
        if has_f_in_name:
            if 'supply_plenum_length' not in section:
                section['supply_plenum_length'] = 1000
            if 'supply_tab_reading' not in section:
                section['supply_tab_reading'] = ''
        else:
            # Remove supply fields if model doesn't have 'F'
            section.pop('supply_plenum_length', None)
            section.pop('supply_tab_reading', None)
        
        # Handle Marvel fields
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