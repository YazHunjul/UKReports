# Canopy Commissioning Report Generator

A modular Streamlit application that allows technicians to fill out canopy commissioning data and generate professional Word document reports.

## Features

- ✅ **General Information Collection**: Client details, project info, engineer names, and visit dates
- 🏭 **Intelligent Canopy Configuration**:
  - 22 canopy models with automatic K-factor calculation
  - Section-based models (1-6 sections) and length-based models (1000-4000mm)
  - Marvel Technology integration with additional fields
  - Smart section data collection based on model type
- 📊 **Automatic K-Factor Calculation**: Real-time K-factor display based on:
  - Canopy model selection
  - Number of sections (for section-based models)
  - Canopy length (for length-based models like CMW-F, CMW-I, KVD, KVV)
- 🔄 **Session State Management**: Form data persists during the session
- 📊 **Progress Tracking**: Visual progress indicator in sidebar
- 🧪 **Testing Interface**: View collected data in real-time
- 📱 **Responsive Design**: Clean, modern UI with proper spacing
- 📚 **Built-in Documentation**: K-factor reference tables and canopy type explanations
- 🔌 **Edge Box Check (Optional)**: Optional Edge box configuration and status tracking
- 💧 **Water Wash System Checklist**: CMW model checklist for water wash system commissioning

## Document Generation

- 📄 **Jinja2 Template System**: Upload Word templates with Jinja2 variables
- 🔄 **Automatic Population**: Form data automatically fills template variables
- ⬇️ **Download Reports**: Generate and download professional Word documents
- 📚 **Template Documentation**: Built-in reference for available variables
- 🔍 **Debug Panel**: View template data and troubleshoot issues

### Template Variables Available

- **Basic Info**: `{{ client_name }}`, `{{ project_name }}`, `{{ engineer_name }}`
- **Canopy Data**: `{% for canopy in canopies %}...{% endfor %}`
- **Section Data**: `{% for section in canopy.sections %}...{% endfor %}`
- **K-Factors**: `{{ section.k_factor }}`
- **Marvel Settings**: `{{ section.min_percent }}%`, `{{ section.idle_percent }}%`
- **Edge Box Data**: `{{ edge_box.edge_installed }}`, `{{ edge_box.edge_id }}`, `{{ edge_box.edge_4g_status }}`, `{{ edge_box.lan_connection }}`, `{{ edge_box.modbus_operation }}`, `{{ edge_box.modbus_value }}`
- **Water Wash System Data**: `{{ canopy.water_wash_checklist }}`, `{{ has_cmw_technology }}`, `{{ water_wash_checklist }}`

## Planned Features

- 🏭 Kitchen Canopy Air Readings section
- 📊 Supply Air Data section
- 💾 Data persistence and loading
- 📧 Email report functionality

## Setup

1. **Create and activate virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run main.py
   ```

## Project Structure

```
REPORTS-UK/
├── venv/                           # Virtual environment
├── src/                           # Source code package
│   ├── __init__.py               # Package initialization
│   ├── config.py                 # Configuration constants
│   ├── components/               # UI Components
│   │   ├── __init__.py
│   │   ├── report_type_selector.py
│   │   ├── general_info.py
│   │   ├── canopy_config.py
│   │   ├── edge_box_check.py
│   │   ├── sidebar.py
│   │   ├── testing_panel.py
│   │   └── action_buttons.py
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       ├── session_manager.py
│       └── progress_tracker.py
├── main.py                       # Main application entry point
├── app.py                        # Legacy monolithic app (deprecated)
├── requirements.txt              # Python dependencies
└── README.md                    # Project documentation
```

## Usage

1. Open the application in your browser (usually http://localhost:8501)
2. Fill in the General Information section
3. Use the sidebar to track progress
4. View collected data in the testing section
5. Generate and download Word documents using templates
6. Clear form or save progress as needed

## Development Notes

- Built with Streamlit for the web interface
- Uses python-docx for Word document generation
- Session state management for data persistence
- **Modular Architecture**: Clean separation of concerns with dedicated modules

## Architecture Overview

### **Components (`src/components/`)**

- **report_type_selector.py**: Report type selection UI
- **general_info.py**: General information form
- **canopy_config.py**: Canopy configuration with sections
- **edge_box_check.py**: Optional Edge box configuration and status
- **water_wash_checklist.py**: Water Wash System checklist for CMW models
- **sidebar.py**: Progress tracking and navigation
- **testing_panel.py**: Data visualization for testing
- **action_buttons.py**: Form control buttons

### **Utilities (`src/utils/`)**

- **session_manager.py**: Session state management
- **progress_tracker.py**: Progress calculation logic

### **Configuration (`src/config.py`)**

- Constants and settings
- Canopy models and field definitions
- Progress tracking configuration

### **Benefits of Modular Design**

- **Maintainability**: Easy to update individual components
- **Reusability**: Components can be reused across different views
- **Testing**: Individual modules can be tested in isolation
- **Scalability**: Easy to add new features without affecting existing code
- **Collaboration**: Multiple developers can work on different modules
