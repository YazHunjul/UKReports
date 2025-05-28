import os
import io
from datetime import datetime
from typing import Dict, Any
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
from src.utils.session_manager import get_form_data
import streamlit as st
import base64
from PIL import Image

def generate_document(template_path: str) -> bytes:
    """
    Generate a Word document from a template using form data.
    
    Args:
        template_path: Path to the Word template file
        
    Returns:
        bytes: Generated document as bytes
    """
    # Get all form data
    form_data = get_form_data()
    
    # Load template
    doc = DocxTemplate(template_path)
    
    # Prepare context data for template
    context = prepare_template_context(form_data, doc)
    
    # Render template with context
    doc.render(context)
    
    # Save to bytes
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    
    return doc_io.getvalue()

def prepare_template_context(form_data: Dict[str, Any], doc: DocxTemplate) -> Dict[str, Any]:
    """
    Prepare context data for Jinja2 template rendering.
    
    Args:
        form_data: Raw form data from session state
        doc: The DocxTemplate document for creating InlineImage objects
        
    Returns:
        Dict containing organized data for template
    """
    context = {
        # Basic information
        'report_type': form_data.get('report_type', ''),
        'client_name': form_data.get('client_name', ''),
        'project_name': form_data.get('project_name', ''),
        'project_number': form_data.get('project_number', ''),
        'date_of_visit': form_data.get('date_of_visit', ''),
        'engineer_name': form_data.get('engineer_name', ''),
        
        # Generated metadata
        'generation_date': datetime.now().strftime('%Y-%m-%d'),
        'generation_time': datetime.now().strftime('%H:%M:%S'),
        
        # Canopy data
        'num_canopies': form_data.get('num_canopies', 0),
        'canopies': [],
        'marvel_canopies': [],  # Canopies with Marvel Technology
        'standard_canopies': [],  # Canopies without Marvel Technology
        
        # Global Marvel flag
        'has_marvel_technology': False,  # Will be set after processing canopies
        
        # Global UV flag
        'has_uv_technology': False,  # Will be set after processing canopies
    }
    
    # Process canopy data
    canopies_data = form_data.get('canopies', [])
    for i, canopy in enumerate(canopies_data):
        canopy_context = {
            'index': i + 1,
            'drawing_number': canopy.get('drawing_number', ''),
            'canopy_location': canopy.get('canopy_location', ''),
            'canopy_model': canopy.get('canopy_model', ''),
            'with_marvel': canopy.get('with_marvel', False),
            'with_uv_checks': canopy.get('with_uv_checks', False),
            'design_airflow': canopy.get('design_airflow', 0.0),
            'supply_airflow': canopy.get('supply_airflow', 0.0),
            'number_of_sections': canopy.get('number_of_sections', 0),
            'canopy_length': canopy.get('canopy_length'),  # For length-based models
            'grill_size': canopy.get('grill_size', ''),  # For CXW models
            'slot_length': canopy.get('slot_length', 0.0),  # For CMWF models
            'slot_width': canopy.get('slot_width', 85.0),  # For CMWF models
            'is_cxw': canopy.get('canopy_model') == 'CXW',
            'is_cmwf': canopy.get('canopy_model') == 'CMWF',
            'is_cmwi': canopy.get('canopy_model') == 'CMWI',
            'is_uv': False,  # Will be set below
            'has_uv_in_name': False,  # Will be set below
            'sections': []
        }
        
        # Set UV flags for this canopy
        canopy_model = canopy.get('canopy_model', '')
        try:
            from src.config import is_uv_model, has_uv_in_name, is_cmw_model, is_cmwi_model
            canopy_context['is_uv'] = is_uv_model(canopy_model)
            canopy_context['has_uv_in_name'] = has_uv_in_name(canopy_model)
            canopy_context['is_cmw'] = is_cmw_model(canopy_model)
            canopy_context['is_cmwi'] = is_cmwi_model(canopy_model)
            canopy_context['with_water_wash_checks'] = canopy.get('with_water_wash_checks', False)
        except:
            canopy_context['is_cmw'] = False
            canopy_context['is_cmwi'] = False
            canopy_context['with_water_wash_checks'] = False
        
        # Add UV checklist data for this canopy if it's a UV model and UV checks are enabled
        if canopy_context['is_uv'] and canopy_context['with_uv_checks']:
            canopy_uv_key = f'canopy_{i}_uv_checklist'
            canopy_uv_data = form_data.get(canopy_uv_key, {})
            canopy_context['uv_checklist'] = get_canopy_uv_checklist_summary(canopy_uv_data)
        else:
            canopy_context['uv_checklist'] = None
        
        # Add Water Wash checklist data for this canopy if it's a CMW model and Water Wash checks are enabled
        if canopy_context['is_cmw'] and canopy_context['with_water_wash_checks']:
            canopy_wash_key = f'canopy_{i}_water_wash_checklist'
            canopy_wash_data = form_data.get(canopy_wash_key, {})
            canopy_context['water_wash_checklist'] = get_canopy_water_wash_checklist_summary(canopy_wash_data)
        else:
            canopy_context['water_wash_checklist'] = None
        
        # Process section data
        sections_data = canopy.get('sections', [])
        extract_total_flowrate = 0.0
        supply_total_flowrate = 0.0
        
        for j, section in enumerate(sections_data):
            # Handle CXW models differently
            if canopy.get('canopy_model') == 'CXW':
                # CXW models use anemometer reading and calculated free area from grill size
                anemometer_reading = section.get('anemometer_reading', 0.0)
                
                # Calculate free area from grill size
                grill_size = canopy.get('grill_size', '')
                try:
                    from src.config import calculate_free_area_from_grill_size, calculate_cxw_flowrate
                    free_area = calculate_free_area_from_grill_size(grill_size)
                except:
                    free_area = 0.0
                
                # Calculate flowrates using CXW formula: Qv = A x m/s
                extract_flowrate_m3h = 0.0
                extract_flowrate_m3s = 0.0
                if anemometer_reading and free_area:
                    try:
                        extract_flowrate_m3h, extract_flowrate_m3s = calculate_cxw_flowrate(free_area, anemometer_reading)
                        extract_total_flowrate += extract_flowrate_m3s
                    except:
                        pass
                
                section_context = {
                    'index': j + 1,
                    'anemometer_reading': anemometer_reading,
                    'free_area': round(free_area, 4),
                    'extract_flowrate_m3h': round(extract_flowrate_m3h, 2),
                    'extract_flowrate_m3s': round(extract_flowrate_m3s, 3),
                }
            elif canopy.get('canopy_model') == 'CMWF':
                # CMWF models use anemometer reading and calculated free area from slot dimensions
                anemometer_reading = section.get('anemometer_reading', 0.0)
                supply_anemometer_reading = section.get('supply_anemometer_reading', 0.0)
                
                # Calculate free area from slot dimensions
                slot_length = canopy.get('slot_length', 0.0)
                slot_width = canopy.get('slot_width', 85.0)
                try:
                    from src.config import calculate_free_area_from_slot_dimensions, calculate_cmwf_flowrate
                    free_area = calculate_free_area_from_slot_dimensions(slot_length, slot_width)
                except:
                    free_area = 0.0
                
                # Calculate extract flowrates using CMWF formula: Qv = A x m/s
                extract_flowrate_m3h = 0.0
                extract_flowrate_m3s = 0.0
                if anemometer_reading and free_area:
                    try:
                        extract_flowrate_m3h, extract_flowrate_m3s = calculate_cmwf_flowrate(free_area, anemometer_reading)
                        extract_total_flowrate += extract_flowrate_m3s
                    except:
                        pass
                
                # Calculate supply flowrates using CMWF formula: Qv = A x m/s
                supply_flowrate_m3h = 0.0
                supply_flowrate_m3s = 0.0
                if supply_anemometer_reading and free_area:
                    try:
                        supply_flowrate_m3h, supply_flowrate_m3s = calculate_cmwf_flowrate(free_area, supply_anemometer_reading)
                        supply_total_flowrate += supply_flowrate_m3s
                    except:
                        pass
                
                section_context = {
                    'index': j + 1,
                    'anemometer_reading': anemometer_reading,
                    'supply_anemometer_reading': supply_anemometer_reading,
                    'free_area': round(free_area, 4),
                    'extract_flowrate_m3h': round(extract_flowrate_m3h, 2),
                    'extract_flowrate_m3s': round(extract_flowrate_m3s, 3),
                    'supply_flowrate_m3h': round(supply_flowrate_m3h, 2),
                    'supply_flowrate_m3s': round(supply_flowrate_m3s, 3),
                }
            elif canopy.get('canopy_model') == 'CMWI':
                # CMWI models use anemometer reading and calculated free area from slot dimensions (extract only)
                anemometer_reading = section.get('anemometer_reading', 0.0)
                
                # Calculate free area from slot dimensions
                slot_length = canopy.get('slot_length', 0.0)
                slot_width = canopy.get('slot_width', 85.0)
                try:
                    from src.config import calculate_free_area_from_slot_dimensions, calculate_cmwi_flowrate
                    free_area = calculate_free_area_from_slot_dimensions(slot_length, slot_width)
                except:
                    free_area = 0.0
                
                # Calculate extract flowrates using CMWI formula: Qv = A x m/s
                extract_flowrate_m3h = 0.0
                extract_flowrate_m3s = 0.0
                if anemometer_reading and free_area:
                    try:
                        extract_flowrate_m3h, extract_flowrate_m3s = calculate_cmwi_flowrate(free_area, anemometer_reading)
                        extract_total_flowrate += extract_flowrate_m3s
                    except:
                        pass
                
                section_context = {
                    'index': j + 1,
                    'anemometer_reading': anemometer_reading,
                    'free_area': round(free_area, 4),
                    'extract_flowrate_m3h': round(extract_flowrate_m3h, 2),
                    'extract_flowrate_m3s': round(extract_flowrate_m3s, 3),
                }
            else:
                # Standard models use K-factor calculation
                extract_k_factor = get_k_factor_for_section(canopy.get('canopy_model'), section.get('extract_ksa'))
                
                # Calculate extract flowrates
                extract_flowrate_m3h = 0.0
                extract_flowrate_m3s = 0.0
                if section.get('extract_tab_reading') and extract_k_factor:
                    try:
                        tab_value = float(section.get('extract_tab_reading'))
                        extract_flowrate_m3h = extract_k_factor * (tab_value ** 0.5)
                        extract_flowrate_m3s = extract_flowrate_m3h / 3600
                        extract_total_flowrate += extract_flowrate_m3s
                    except:
                        pass
                
                section_context = {
                    'index': j + 1,
                    'extract_ksa': section.get('extract_ksa'),
                    'extract_tab_reading': section.get('extract_tab_reading', ''),
                    'extract_k_factor': extract_k_factor,
                    'extract_flowrate_m3h': round(extract_flowrate_m3h, 2),
                    'extract_flowrate_m3s': round(extract_flowrate_m3s, 3),
                }
            
            # Add supply fields if present (for models with 'F' in name, but not CXW, CMWF, or CMWI)
            if 'supply_plenum_length' in section and canopy.get('canopy_model') not in ['CXW', 'CMWF', 'CMWI']:
                # For supply air K-factor calculation:
                # - Length-based models (CMW-F, CMW-I, KVD, KVV): use plenum length
                # - Section-based models (KVF, UVF, etc.): use same K-factor as extract (based on KSAs)
                canopy_model = canopy.get('canopy_model', '')
                if is_length_based_model_for_supply(canopy_model):
                    supply_k_factor = get_k_factor_for_section(canopy_model, section.get('supply_plenum_length'))
                else:
                    # For section-based models, use the same K-factor as extract air
                    supply_k_factor = extract_k_factor
                
                # Calculate supply flowrates
                supply_flowrate_m3h = 0.0
                supply_flowrate_m3s = 0.0
                if section.get('supply_tab_reading') and supply_k_factor:
                    try:
                        tab_value = float(section.get('supply_tab_reading'))
                        supply_flowrate_m3h = supply_k_factor * (tab_value ** 0.5)
                        supply_flowrate_m3s = supply_flowrate_m3h / 3600
                        supply_total_flowrate += supply_flowrate_m3s
                    except:
                        pass
                
                section_context.update({
                    'supply_plenum_length': section.get('supply_plenum_length'),
                    'supply_tab_reading': section.get('supply_tab_reading', ''),
                    'supply_k_factor': supply_k_factor,
                    'supply_flowrate_m3h': round(supply_flowrate_m3h, 2),
                    'supply_flowrate_m3s': round(supply_flowrate_m3s, 3),
                })
            
            # Add Marvel fields if applicable
            if canopy.get('with_marvel', False):
                section_context.update({
                    'min_percent': section.get('min_percent', 0.0),
                    'idle_percent': section.get('idle_percent', 0.0),
                    'design_m3s': section.get('design_m3s', 0.0),
                })
            
            canopy_context['sections'].append(section_context)
        
        # Add total flowrates to canopy context
        canopy_context.update({
            'extract_total_flowrate_m3s': round(extract_total_flowrate, 3),
            'supply_total_flowrate_m3s': round(supply_total_flowrate, 3),
            'has_f_in_name': 'F' in canopy.get('canopy_model', '')
        })
        
        context['canopies'].append(canopy_context)
        
        # Also add to Marvel or Standard canopy lists
        if canopy.get('with_marvel', False):
            context['marvel_canopies'].append(canopy_context)
        else:
            context['standard_canopies'].append(canopy_context)
    
    # Set global Marvel flag based on whether any canopies have Marvel technology
    context['has_marvel_technology'] = len(context['marvel_canopies']) > 0
    
    # Set global UV flag based on whether any canopies have UV technology
    context['has_uv_technology'] = any(canopy.get('is_uv', False) for canopy in context['canopies'])
    
    # Add UV checklist data if UV technology is present
    if context['has_uv_technology']:
        try:
            from src.components.uv_checklist import get_uv_checklist_summary
            context['uv_checklist'] = get_uv_checklist_summary()
        except:
            context['uv_checklist'] = None
    else:
        context['uv_checklist'] = None
    
    # Set global CMW flag based on whether any canopies have CMW technology
    context['has_cmw_technology'] = any(canopy.get('is_cmw', False) for canopy in context['canopies'])
    
    # Add Water Wash System checklist data if CMW technology is present
    if context['has_cmw_technology']:
        try:
            from src.components.water_wash_checklist import get_water_wash_checklist_summary
            context['water_wash_checklist'] = get_water_wash_checklist_summary()
        except:
            context['water_wash_checklist'] = None
    else:
        context['water_wash_checklist'] = None
    
    # Generate results summary data
    extract_results, supply_results, totals = generate_results_summary_data(context['canopies'])
    context['extract_results'] = extract_results
    context['supply_results'] = supply_results
    context['extract_total_design'] = totals['extract_total_design']
    context['extract_total_actual'] = totals['extract_total_actual']
    context['extract_total_percentage'] = totals['extract_total_percentage']
    context['supply_total_design'] = totals['supply_total_design']
    context['supply_total_actual'] = totals['supply_total_actual']
    context['supply_total_percentage'] = totals['supply_total_percentage']
    
    # Add Edge box data
    edge_box_data = form_data.get('edge_box', {})
    context['edge_box'] = {
        'edge_installed': edge_box_data.get('edge_installed', False),
        'edge_id': edge_box_data.get('edge_id', ''),
        'edge_4g_status': edge_box_data.get('edge_4g_status', ''),
        'lan_connection': edge_box_data.get('lan_connection', False),
        'modbus_operation': edge_box_data.get('modbus_operation', False),
        'modbus_value': edge_box_data.get('modbus_value', None),
        'has_edge_data': any([
            edge_box_data.get('edge_installed', False),
            edge_box_data.get('edge_id', ''),
            edge_box_data.get('edge_4g_status', ''),
            edge_box_data.get('lan_connection', False),
            edge_box_data.get('modbus_operation', False)
        ])
    }
    
    # Add signature and notes data
    context['additional_notes'] = form_data.get('additional_notes', '')
    context['notes_list'] = form_data.get('notes_list', [])
    context['has_notes'] = len(form_data.get('notes_list', [])) > 0
    context['signature_data'] = form_data.get('signature_data', '')
    context['signature_date'] = form_data.get('signature_date', '')
    context['print_name'] = form_data.get('print_name', '')
    context['has_signature'] = form_data.get('has_signature', False)
    
    # Process signature for template if available
    if context['has_signature']:
        try:
            signature_image = create_signature_inline_image_with_doc(context['signature_data'], doc)
            if signature_image:
                context['signature_image'] = signature_image
                context['signature_image_base64'] = context['signature_data']  # Keep original base64 as backup
            else:
                context['signature_image'] = None
                context['signature_image_base64'] = ''
        except Exception as e:
            st.error(f"Error processing signature for template: {e}")
            context['signature_image'] = None
            context['signature_image_base64'] = ''
    else:
        context['signature_image'] = None
        context['signature_image_base64'] = ''
    
    return context

def generate_results_summary_data(canopies: list) -> tuple:
    """
    Generate results summary data for Extract and Supply Air tables.
    
    Args:
        canopies: List of processed canopy data
        
    Returns:
        Tuple of (extract_results, supply_results, totals) where totals is a dict
    """
    extract_results = []
    supply_results = []
    
    total_extract_design = 0.0
    total_extract_actual = 0.0
    total_supply_design = 0.0
    total_supply_actual = 0.0
    
    for canopy in canopies:
        drawing_number = canopy.get('drawing_number', '')
        design_airflow = canopy.get('design_airflow', 0.0)
        supply_airflow = canopy.get('supply_airflow', 0.0)
        extract_total_flowrate = canopy.get('extract_total_flowrate_m3s', 0.0)
        supply_total_flowrate = canopy.get('supply_total_flowrate_m3s', 0.0)
        
        # Calculate percentages
        extract_percentage = (extract_total_flowrate / design_airflow * 100) if design_airflow > 0 else 0
        supply_percentage = (supply_total_flowrate / supply_airflow * 100) if supply_airflow > 0 else 0
        
        # Add to extract results (without TOTAL row)
        extract_results.append({
            'drawing_number': drawing_number,
            'design_flow_rate': f"{design_airflow:.2f}",
            'actual_flowrate': f"{extract_total_flowrate:.3f}",
            'percentage': f"{extract_percentage:.1f}%"
        })
        
        # Add to supply results (only for models with supply air, without TOTAL row)
        if canopy.get('has_f_in_name', False) and supply_airflow > 0:
            supply_results.append({
                'drawing_number': drawing_number,
                'design_flow_rate': f"{supply_airflow:.2f}",
                'actual_flowrate': f"{supply_total_flowrate:.3f}",
                'percentage': f"{supply_percentage:.1f}%"
            })
        
        # Add to totals
        total_extract_design += design_airflow
        total_extract_actual += extract_total_flowrate
        if canopy.get('has_f_in_name', False):
            total_supply_design += supply_airflow
            total_supply_actual += supply_total_flowrate
    
    # Calculate total percentages
    total_extract_percentage = (total_extract_actual / total_extract_design * 100) if total_extract_design > 0 else 0
    total_supply_percentage = (total_supply_actual / total_supply_design * 100) if total_supply_design > 0 else 0
    
    # Create totals dictionary
    totals = {
        'extract_total_design': f"{total_extract_design:.2f}",
        'extract_total_actual': f"{total_extract_actual:.3f}",
        'extract_total_percentage': f"{total_extract_percentage:.1f}%",
        'supply_total_design': f"{total_supply_design:.2f}",
        'supply_total_actual': f"{total_supply_actual:.3f}",
        'supply_total_percentage': f"{total_supply_percentage:.1f}%"
    }
    
    return extract_results, supply_results, totals

def get_k_factor_for_section(canopy_model: str, selected_ksa: int) -> float:
    """
    Get K-factor for a section (helper function for template context).
    
    Args:
        canopy_model: The canopy model
        selected_ksa: Selected KSA count
        
    Returns:
        K-factor value
    """
    try:
        from src.config import get_k_factor
        return get_k_factor(canopy_model, selected_ksa) if canopy_model and selected_ksa else 0.0
    except:
        return 0.0

def is_length_based_model_for_supply(canopy_model: str) -> bool:
    """
    Check if a canopy model uses length-based K-factors for supply air.
    
    Args:
        canopy_model: The canopy model
        
    Returns:
        True if model uses length-based K-factors for supply
    """
    try:
        from src.config import is_length_based_model
        return is_length_based_model(canopy_model)
    except:
        return False

def generate_filename(form_data: Dict[str, Any]) -> str:
    """
    Generate a filename for the document based on form data.
    
    Args:
        form_data: Form data from session state
        
    Returns:
        Generated filename
    """
    client = form_data.get('client_name', 'Client').replace(' ', '_')
    project = form_data.get('project_number', 'Project').replace(' ', '_')
    report_type = form_data.get('report_type', 'Report').replace(' ', '_')
    date = datetime.now().strftime('%Y%m%d')
    
    return f"{client}_{project}_{report_type}_{date}.docx"

def get_canopy_uv_checklist_summary(canopy_uv_data: dict) -> dict:
    """
    Get a summary of UV checklist completion for a specific canopy.
    
    Args:
        canopy_uv_data: UV checklist data for a specific canopy
        
    Returns:
        Dict containing organized UV checklist summary for template
    """
    from src.config import UV_SYSTEM_CHECKLIST
    
    summary = {
        'total_items': len(UV_SYSTEM_CHECKLIST),
        'completed_items': 0,
        'completion_percentage': 0.0,
        'checklist_items': []
    }
    
    for item in UV_SYSTEM_CHECKLIST:
        value = canopy_uv_data.get(item, '')
        is_completed = False
        
        if isinstance(value, bool):
            is_completed = value
            display_value = "✓" if value else ""
        elif isinstance(value, (int, float)) and value is not None:
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

def get_canopy_water_wash_checklist_summary(canopy_wash_data: dict) -> dict:
    """
    Get a summary of Water Wash checklist completion for a specific canopy.
    
    Args:
        canopy_wash_data: Water Wash checklist data for a specific canopy
        
    Returns:
        Dict containing organized Water Wash checklist summary for template
    """
    from src.config import WATER_WASH_SYSTEM_CHECKLIST
    
    summary = {
        'total_items': len(WATER_WASH_SYSTEM_CHECKLIST),
        'completed_items': 0,
        'completion_percentage': 0.0,
        'checklist_items': []
    }
    
    for item in WATER_WASH_SYSTEM_CHECKLIST:
        value = canopy_wash_data.get(item, '')
        is_completed = False
        
        if isinstance(value, bool):
            is_completed = value
            display_value = "✓" if value else ""
        elif isinstance(value, (int, float)) and value is not None:
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

def create_signature_inline_image_with_doc(signature_base64: str, doc: DocxTemplate) -> InlineImage:
    """
    Create an InlineImage object from base64 signature data for Word template.
    
    Args:
        signature_base64: Base64 encoded signature image
        doc: The DocxTemplate document for creating InlineImage objects
        
    Returns:
        InlineImage object for Word template
    """
    if not signature_base64:
        return None
    
    try:
        # Decode base64 to image
        image_data = base64.b64decode(signature_base64)
        img = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if needed (remove alpha channel)
        if img.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize signature to appropriate size for document
        max_width = 300  # pixels
        max_height = 100  # pixels
        
        # Calculate new size maintaining aspect ratio
        ratio = min(max_width / img.width, max_height / img.height)
        new_width = int(img.width * ratio)
        new_height = int(img.height * ratio)
        
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save to BytesIO
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        # Create InlineImage object
        # Convert pixels to inches (assuming 96 DPI)
        width_inches = new_width / 96
        height_inches = new_height / 96
        
        # Create InlineImage
        inline_image = InlineImage(doc, img_io, width=Inches(width_inches), height=Inches(height_inches))
        
        return inline_image
        
    except Exception as e:
        st.error(f"Error creating signature image: {e}")
        return None 