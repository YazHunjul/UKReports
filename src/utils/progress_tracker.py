from src.config import BASIC_FIELDS, BASIC_CANOPY_FIELDS, BASIC_SECTION_FIELDS, SUPPLY_SECTION_FIELDS, MARVEL_SECTION_FIELDS, is_length_based_model
from src.utils.session_manager import get_form_data

def calculate_progress() -> float:
    """Calculate the overall progress of form completion."""
    progress, _, _ = calculate_detailed_progress()
    return progress

def calculate_detailed_progress() -> tuple[float, int, int]:
    """Calculate detailed progress information including completed and total fields."""
    form_data = get_form_data()
    
    # Count basic fields - use the actual field names instead of BASIC_FIELDS constant
    basic_field_keys = ['report_type', 'client_name', 'project_name', 'project_number', 'date_of_visit', 'engineer_name']
    completed_basic = sum(1 for key in basic_field_keys 
                         if form_data.get(key) and str(form_data.get(key)).strip())
    
    # Count canopy fields if applicable
    canopy_fields_completed = 0
    total_canopy_fields = 0
    
    if form_data.get('report_type') == "Canopy Commissioning":
        num_canopies = form_data.get('num_canopies', 0)
        if num_canopies > 0:
            canopies_data = form_data.get('canopies', [])
            
            for canopy in canopies_data:
                # Count basic canopy fields
                total_canopy_fields += BASIC_CANOPY_FIELDS
                
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
                has_f_in_name = 'F' in canopy_model if canopy_model else False
                
                # Count section fields for all models except length-based ones
                if (canopy_model and 
                    not is_length_based_model(canopy_model) and 
                    num_sections > 0):
                    
                    # Calculate fields per section
                    fields_per_section = BASIC_SECTION_FIELDS  # extract_info
                    if has_f_in_name:
                        fields_per_section += SUPPLY_SECTION_FIELDS  # supply_info
                    if with_marvel:
                        fields_per_section += MARVEL_SECTION_FIELDS
                    
                    total_section_fields = num_sections * fields_per_section
                    total_canopy_fields += total_section_fields
                    
                    # Count completed section fields
                    sections_data = canopy.get('sections', [])
                    for section in sections_data:
                        for section_key, section_value in section.items():
                            if section_value and str(section_value).strip():
                                canopy_fields_completed += 1
    
    # Count Edge box fields (optional)
    edge_box_fields_completed = 0
    total_edge_box_fields = 0
    edge_box_data = form_data.get('edge_box', {})
    
    # Only count Edge box fields if any Edge box data is present
    if any([
        edge_box_data.get('edge_installed', False),
        edge_box_data.get('edge_id', ''),
        edge_box_data.get('edge_4g_status', ''),
        edge_box_data.get('lan_connection', False),
        edge_box_data.get('modbus_operation', False)
    ]):
        # Edge box has 5 main fields: edge_installed, edge_id, edge_4g_status, lan_connection, modbus_operation
        # modbus_value is conditional on modbus_operation being true
        total_edge_box_fields = 5
        if edge_box_data.get('modbus_operation', False):
            total_edge_box_fields += 1  # Add modbus_value field
        
        # Count completed Edge box fields
        if edge_box_data.get('edge_installed', False):
            edge_box_fields_completed += 1
        if edge_box_data.get('edge_id', ''):
            edge_box_fields_completed += 1
        if edge_box_data.get('edge_4g_status', ''):
            edge_box_fields_completed += 1
        if edge_box_data.get('lan_connection', False):
            edge_box_fields_completed += 1
        if edge_box_data.get('modbus_operation', False):
            edge_box_fields_completed += 1
            # If modbus operation is enabled, check modbus_value
            if edge_box_data.get('modbus_value') is not None:
                edge_box_fields_completed += 1
    
    total_fields = len(basic_field_keys) + total_canopy_fields + total_edge_box_fields
    completed_fields = completed_basic + canopy_fields_completed + edge_box_fields_completed
    progress = min(completed_fields / total_fields if total_fields > 0 else 0, 1.0)
    
    return progress, completed_fields, total_fields 