# Configuration settings for the Canopy Commissioning Report Generator

# Report types
REPORT_TYPES = ["Canopy Commissioning", "Supply Air Analysis", "Full System Report"]

# Canopy models
CANOPY_MODELS = [
    'KVF', 'KVI', 'KCH-F', 'KCH-I', 'KSR-S', 'KSR-F', 'KSR-M',
    'UVF', 'UVI', 'USR-S', 'USR-F', 'USR-M', 'KWF', 'KWI', 
    'UWF', 'UWI', 'CMW-FMOD', 'CMW-IMOD', 'CMW-F', 'CMW-I',
    'KVD', 'KVV', 'CXW', 'CMWF', 'CMWI'
]

# UV canopy models (models that include UV systems)
UV_CANOPY_MODELS = ['UVF', 'UVI', 'USR-S', 'USR-F', 'USR-M', 'UWF', 'UWI']

# CMW canopy models (Cold Mist and Washing systems)
CMW_CANOPY_MODELS = ['CMWI', 'CMWF', 'CMW-FMOD', 'CMW-IMOD', 'CMW-F', 'CMW-I']

# Water Wash System Checklist Items (for CMW models)
WATER_WASH_SYSTEM_CHECKLIST = [
    'Airflow switch set up and tested',
    'Drain plugs removed to flush hot/cold water',
    'Detergent connected and bled into hot water system',
    'Cold mist nozzles aligned correctly',
    'Cold mist operation tested',
    'Cold water pressure (BAR)',
    'Hot wash operation tested',
    'Hot water pressure (BAR)',
    'Hot water temperature (°C)',
    'Capture Jet operational',
    'Capture Jet average Pressure (Pa)'
]

# UV System Checklist Items
UV_SYSTEM_CHECKLIST = [
    'Quantity of Slaves per System',
    'Airflow Proved on Each Controller',
    'UV Pressure Setpoint (Pa)',
    'All UV Safety Switches Tested',
    'All Filter Safety Switches Tested',
    'Communication To All Canopy Controllers',
    'UV System Tested and Fully Operational',
    'Capture Jet operational',
    'MUS Auxiliary Module Installed and Tested',
    'Capture Jet average pressure reading (Pa)'
]

# CMW canopy models (Cold Mist and Washing systems)
CMW_CANOPY_MODELS = ['CMWI', 'CMWF', 'CMW-FMOD', 'CMW-IMOD', 'CMW-F', 'CMW-I']

# Water Wash System Checklist Items (for CMW models)
WATER_WASH_SYSTEM_CHECKLIST = [
    'Airflow switch set up and tested',
    'Drain plugs removed to flush hot/cold water',
    'Detergent connected and bled into hot water system',
    'Cold mist nozzles aligned correctly',
    'Cold mist operation tested',
    'Cold water pressure (BAR)',
    'Hot wash operation tested',
    'Hot water pressure (BAR)',
    'Hot water temperature (°C)',
    'Capture Jet operational',
    'Capture Jet average Pressure (Pa)'
]

# Basic form fields for progress tracking
BASIC_FIELDS = 6  # report_type, client_name, project_name, project_number, date_of_visit, engineer_name

# Canopy configuration
MAX_CANOPIES = 20
MAX_SECTIONS = 6

# Section field configuration
BASIC_SECTION_FIELDS = 2  # extract_ksa, extract_tab_reading (always present)
SUPPLY_SECTION_FIELDS = 2  # supply_plenum_length, supply_tab_reading (only for models with 'F')
MARVEL_SECTION_FIELDS = 3  # min_percent, idle_percent, design_percent
BASIC_CANOPY_FIELDS = 7   # drawing_number, canopy_location, canopy_model, with_marvel, design_airflow, supply_airflow, number_of_sections 

# K-factor data based on canopy documentation
K_FACTOR_DATA = {
    # 1.1 Capture Jet™ hoods (KVF, KVI, KCH-F, KCH-I)
    'KVF': {
        'type': 'section_based',
        'sections': {
            1: 71.8, 2: 143.6, 3: 215.4, 4: 287.2, 5: 359.0, 6: 430.8
        }
    },
    'KVI': {
        'type': 'section_based',
        'sections': {
            1: 71.8, 2: 143.6, 3: 215.4, 4: 287.2, 5: 359.0, 6: 430.8
        }
    },
    'KCH-F': {
        'type': 'section_based',
        'sections': {
            1: 71.8, 2: 143.6, 3: 215.4, 4: 287.2, 5: 359.0, 6: 430.8
        }
    },
    'KCH-I': {
        'type': 'section_based',
        'sections': {
            1: 71.8, 2: 143.6, 3: 215.4, 4: 287.2, 5: 359.0, 6: 430.8
        }
    },
    
    # 1.2 Capture Jet™ low proximity (KSR-S, KSR-F, KSR-M)
    'KSR-S': {
        'type': 'section_based',
        'sections': {
            1: 67.7, 2: 135.4, 3: 203.1, 4: 270.8, 5: 338.5, 6: 406.2
        }
    },
    'KSR-F': {
        'type': 'section_based',
        'sections': {
            1: 67.7, 2: 135.4, 3: 203.1, 4: 270.8, 5: 338.5, 6: 406.2
        }
    },
    'KSR-M': {
        'type': 'section_based',
        'sections': {
            1: 67.7, 2: 135.4, 3: 203.1, 4: 270.8, 5: 338.5, 6: 406.2
        }
    },
    
    # 1.3 Capture Ray™ hoods (UVF, UVI)
    'UVF': {
        'type': 'section_based',
        'sections': {
            1: 49.7, 2: 99.4, 3: 149.1, 4: 198.8, 5: 248.5, 6: 298.2
        }
    },
    'UVI': {
        'type': 'section_based',
        'sections': {
            1: 49.7, 2: 99.4, 3: 149.1, 4: 198.8, 5: 248.5, 6: 298.2
        }
    },
    
    # 1.4 Capture Ray™ low proximity (USR-S, USR-F, USR-M)
    'USR-S': {
        'type': 'section_based',
        'sections': {
            1: 67.7, 2: 135.4, 3: 203.1, 4: 270.8, 5: 338.5, 6: 406.2
        }
    },
    'USR-F': {
        'type': 'section_based',
        'sections': {
            1: 67.7, 2: 135.4, 3: 203.1, 4: 270.8, 5: 338.5, 6: 406.2
        }
    },
    'USR-M': {
        'type': 'section_based',
        'sections': {
            1: 67.7, 2: 135.4, 3: 203.1, 4: 270.8, 5: 338.5, 6: 406.2
        }
    },
    
    # 1.5 Water Wash hoods (KWF, KWI, UWF, UWI, CMW-FMOD, CMW-IMOD)
    'KWF': {
        'type': 'section_based',
        'sections': {
            1: 65.5, 2: 131.0, 3: 196.5, 4: 262.0, 5: 327.5, 6: 393.0
        }
    },
    'KWI': {
        'type': 'section_based',
        'sections': {
            1: 65.5, 2: 131.0, 3: 196.5, 4: 262.0, 5: 327.5, 6: 393.0
        }
    },
    'UWF': {
        'type': 'section_based',
        'sections': {
            1: 65.5, 2: 131.0, 3: 196.5, 4: 262.0, 5: 327.5, 6: 393.0
        }
    },
    'UWI': {
        'type': 'section_based',
        'sections': {
            1: 65.5, 2: 131.0, 3: 196.5, 4: 262.0, 5: 327.5, 6: 393.0
        }
    },
    'CMW-FMOD': {
        'type': 'section_based',
        'sections': {
            1: 65.5, 2: 131.0, 3: 196.5, 4: 262.0, 5: 327.5, 6: 393.0
        }
    },
    'CMW-IMOD': {
        'type': 'section_based',
        'sections': {
            1: 65.5, 2: 131.0, 3: 196.5, 4: 262.0, 5: 327.5, 6: 393.0
        }
    },
    
    # 1.6 Cold Mist only (CMW-F, CMW-I)
    'CMW-F': {
        'type': 'length_based',
        'length_ranges': {
            1000: 115, 1500: 172.5, 2000: 230, 2500: 287.5, 3000: 345
        }
    },
    'CMW-I': {
        'type': 'length_based',
        'length_ranges': {
            1000: 115, 1500: 172.5, 2000: 230, 2500: 287.5, 3000: 345
        }
    },
    
    # 1.7 Steam hoods (KVD, KVV)
    'KVD': {
        'type': 'length_based',
        'length_ranges': {
            1000: 161, 1500: 241.5, 2000: 322, 2500: 402.5, 3000: 483, 3500: 563.5, 4000: 644
        }
    },
    'KVV': {
        'type': 'length_based',
        'length_ranges': {
            1000: 161, 1500: 241.5, 2000: 322, 2500: 402.5, 3000: 483, 3500: 563.5, 4000: 644
        }
    },
    
    # 1.8 CXW hoods (special handling - uses anemometer readings and free area calculation)
    'CXW': {
        'type': 'cxw_special',
        'calculation': 'Qv = A x m/s'  # Flowrate = Free Area x Anemometer Reading
    },
    
    # 1.9 CMWF hoods (similar to CXW but uses slot dimensions)
    'CMWF': {
        'type': 'cmwf_special',
        'calculation': 'Qv = A x m/s'  # Flowrate = Free Area x Anemometer Reading
    },
    
    # 1.10 CMWI hoods (similar to CMWF but extract only)
    'CMWI': {
        'type': 'cmwi_special',
        'calculation': 'Qv = A x m/s'  # Flowrate = Free Area x Anemometer Reading
    }
}

def get_k_factor(canopy_model: str, ksa_count: int) -> float:
    """
    Get K-factor value for a given canopy model and number of KSAs.
    
    Args:
        canopy_model: The canopy model (e.g., 'KVF', 'UVF', etc.)
        ksa_count: Number of KSAs (1-6) for section-based models or length in mm for length-based
    
    Returns:
        K-factor value or 0.0 if not found
    """
    if canopy_model not in K_FACTOR_DATA:
        return 0.0
    
    model_data = K_FACTOR_DATA[canopy_model]
    
    if model_data['type'] == 'section_based':
        return model_data['sections'].get(ksa_count, 0.0)
    
    elif model_data['type'] == 'length_based':
        # For length-based models, find the closest length
        length_ranges = model_data['length_ranges']
        if ksa_count in length_ranges:
            return length_ranges[ksa_count]
        
        # Find closest length if exact match not found
        available_lengths = sorted(length_ranges.keys())
        closest_length = min(available_lengths, key=lambda x: abs(x - ksa_count))
        return length_ranges[closest_length]
    
    return 0.0

def get_available_ksas(canopy_model: str) -> list:
    """
    Get available KSA options for a given canopy model.
    
    Args:
        canopy_model: The canopy model (e.g., 'KVF', 'UVF', etc.)
    
    Returns:
        List of available KSA counts/lengths
    """
    if canopy_model not in K_FACTOR_DATA:
        return []
    
    model_data = K_FACTOR_DATA[canopy_model]
    
    if model_data['type'] == 'section_based':
        return list(model_data['sections'].keys())
    elif model_data['type'] == 'length_based':
        return list(model_data['length_ranges'].keys())
    
    return []

def is_length_based_model(canopy_model: str) -> bool:
    """Check if a canopy model uses length-based K-factors."""
    return canopy_model in K_FACTOR_DATA and K_FACTOR_DATA[canopy_model]['type'] == 'length_based'

def is_cxw_model(canopy_model: str) -> bool:
    """
    Check if a canopy model is CXW type (special handling).
    
    Args:
        canopy_model: The canopy model
        
    Returns:
        True if model is CXW type
    """
    return canopy_model == 'CXW'

def is_cmwf_model(canopy_model: str) -> bool:
    """
    Check if a canopy model is CMWF type (uses slot dimensions).
    
    Args:
        canopy_model: The canopy model
        
    Returns:
        True if model is CMWF type
    """
    return canopy_model == 'CMWF'

def is_cmwi_model(canopy_model: str) -> bool:
    """
    Check if a canopy model is CMWI type (extract only, uses slot dimensions).
    
    Args:
        canopy_model: The canopy model
        
    Returns:
        True if model is CMWI type
    """
    return canopy_model == 'CMWI'

def is_cmw_anemometer_model(canopy_model: str) -> bool:
    """
    Check if a canopy model is a CMW type that uses anemometer readings (CMWF, CMWI).
    
    Args:
        canopy_model: The canopy model
        
    Returns:
        True if model is CMW anemometer type
    """
    return canopy_model in ['CMWF', 'CMWI']

def is_cmw_model(canopy_model: str) -> bool:
    """
    Check if a canopy model is CMW type (Cold Mist and Washing system).
    
    Args:
        canopy_model: The canopy model
        
    Returns:
        True if model is CMW type
    """
    return canopy_model in CMW_CANOPY_MODELS

def is_uv_model(canopy_model: str) -> bool:
    """
    Check if a canopy model includes UV system.
    
    Args:
        canopy_model: The canopy model
        
    Returns:
        True if model includes UV system
    """
    return canopy_model in UV_CANOPY_MODELS

def has_uv_in_name(canopy_model: str) -> bool:
    """
    Check if a canopy model has 'UV' in its name.
    
    Args:
        canopy_model: The canopy model
        
    Returns:
        True if model name contains 'UV'
    """
    return 'UV' in canopy_model if canopy_model else False

def calculate_free_area_from_grill_size(grill_size: str, free_area_percentage: float = 0.75) -> float:
    """
    Calculate free area from grill size.
    
    Args:
        grill_size: Grill size string (e.g., "600x600", "500x500")
        free_area_percentage: Percentage of total area that is free (default 75%)
        
    Returns:
        Free area in m²
    """
    if not grill_size:
        return 0.0
    
    try:
        # Parse grill size (e.g., "600x600" -> width=600, height=600)
        if 'x' in grill_size.lower():
            dimensions = grill_size.lower().replace('mm', '').replace(' ', '').split('x')
            if len(dimensions) == 2:
                width_mm = float(dimensions[0])
                height_mm = float(dimensions[1])
                
                # Convert to m² and apply free area percentage
                total_area_m2 = (width_mm / 1000) * (height_mm / 1000)
                free_area_m2 = total_area_m2 * free_area_percentage
                
                return free_area_m2
    except:
        pass
    
    return 0.0

def calculate_cxw_flowrate(free_area: float, anemometer_reading: float) -> tuple:
    """
    Calculate flowrate for CXW canopies using Qv = A x m/s formula.
    
    Args:
        free_area: Free area in m²
        anemometer_reading: Anemometer reading in m/s
        
    Returns:
        Tuple of (flowrate_m3h, flowrate_m3s)
    """
    if not free_area or not anemometer_reading:
        return 0.0, 0.0
    
    flowrate_m3s = free_area * anemometer_reading  # m³/s
    flowrate_m3h = flowrate_m3s * 3600  # m³/h
    
    return flowrate_m3h, flowrate_m3s

def calculate_free_area_from_slot_dimensions(slot_length: float, slot_width: float, free_area_percentage: float = 0.75) -> float:
    """
    Calculate free area from slot dimensions for CMWF/CMWI canopies.
    
    Args:
        slot_length: Length of slot in mm
        slot_width: Width of slot in mm  
        free_area_percentage: Percentage of total area that is free (default 75%)
        
    Returns:
        Free area in m²
    """
    if not slot_length or not slot_width:
        return 0.0
    
    try:
        # Convert to m² and apply free area percentage
        total_area_m2 = (slot_length / 1000) * (slot_width / 1000)
        free_area_m2 = total_area_m2 * free_area_percentage
        
        return free_area_m2
    except:
        return 0.0

def calculate_cmwf_flowrate(free_area: float, anemometer_reading: float) -> tuple:
    """
    Calculate flowrate for CMWF canopies using Qv = A x m/s formula.
    Same as CXW but for slot-based calculations.
    
    Args:
        free_area: Free area in m²
        anemometer_reading: Anemometer reading in m/s
        
    Returns:
        Tuple of (flowrate_m3h, flowrate_m3s)
    """
    if not free_area or not anemometer_reading:
        return 0.0, 0.0
    
    flowrate_m3s = free_area * anemometer_reading  # m³/s
    flowrate_m3h = flowrate_m3s * 3600  # m³/h
    
    return flowrate_m3h, flowrate_m3s

def calculate_cmwi_flowrate(free_area: float, anemometer_reading: float) -> tuple:
    """
    Calculate flowrate for CMWI canopies using Qv = A x m/s formula.
    Same as CMWF but for extract only (no supply air).
    
    Args:
        free_area: Free area in m²
        anemometer_reading: Anemometer reading in m/s
        
    Returns:
        Tuple of (flowrate_m3h, flowrate_m3s)
    """
    if not free_area or not anemometer_reading:
        return 0.0, 0.0
    
    flowrate_m3s = free_area * anemometer_reading  # m³/s
    flowrate_m3h = flowrate_m3s * 3600  # m³/h
    
    return flowrate_m3h, flowrate_m3s 