import streamlit as st

def render_template_help():
    """Render comprehensive template help documentation."""
    st.markdown("## 📖 Template Help & Documentation")
    
    with st.expander("📋 Available Template Variables", expanded=False):
        st.markdown("""
        ### Basic Information Variables
        - `{{client_name}}` - Client name
        - `{{project_name}}` - Project name  
        - `{{project_number}}` - Project number
        - `{{date_of_visit}}` - Date of visit
        - `{{engineer_name}}` - Engineer name
        - `{{report_type}}` - Type of report
        
        ### Generated Metadata
        - `{{generation_date}}` - Document generation date (YYYY-MM-DD)
        - `{{generation_time}}` - Document generation time (HH:MM:SS)
        
        ### Canopy Data
        - `{{num_canopies}}` - Total number of canopies
        
        ### Canopy Organization Variables
        - `{{canopies}}` - All canopies (mixed)
        - `{{standard_canopies}}` - Only canopies WITHOUT Marvel Technology
        - `{{marvel_canopies}}` - Only canopies WITH Marvel Technology
        - `{{has_marvel_technology}}` - Boolean: true if ANY canopy has Marvel Technology
        - `{{has_uv_technology}}` - Boolean: true if ANY canopy has UV system
        
        ### Looping Through All Canopies
        ```
        {% for canopy in canopies %}
            Canopy {{canopy.index}}: {{canopy.canopy_model}}
            Drawing: {{canopy.drawing_number}}
            Location: {{canopy.canopy_location}}
            Design Airflow: {{canopy.design_airflow}} m³/s
            Supply Airflow: {{canopy.supply_airflow}} m³/s
            Number of Sections: {{canopy.number_of_sections}}
            With Marvel: {{canopy.with_marvel}}
            Has F in Name: {{canopy.has_f_in_name}}
            Is CXW: {{canopy.is_cxw}}
            Is UV: {{canopy.is_uv}}
            Has UV in Name: {{canopy.has_uv_in_name}}
            
            {% if canopy.is_cxw %}
            Grill Size: {{canopy.grill_size}}
            {% endif %}
            
            Extract Total Flowrate: {{canopy.extract_total_flowrate_m3s}} m³/s
            {% if canopy.has_f_in_name and not canopy.is_cxw %}
            Supply Total Flowrate: {{canopy.supply_total_flowrate_m3s}} m³/s
            {% endif %}
            
            {% for section in canopy.sections %}
                {% if canopy.is_cxw %}
                Grill {{section.index}}:
                - Anemometer Reading: {{section.anemometer_reading}} m/s
                - Free Area: {{section.free_area}} m²
                - Flowrate: {{section.extract_flowrate_m3h}} m³/h ({{section.extract_flowrate_m3s}} m³/s)
                {% else %}
                Section {{section.index}}:
                - Extract KSA: {{section.extract_ksa}}
                - Extract T.A.B Reading: {{section.extract_tab_reading}}
                - Extract K-Factor: {{section.extract_k_factor}}
                - Extract Flowrate: {{section.extract_flowrate_m3h}} m³/h ({{section.extract_flowrate_m3s}} m³/s)
                
                {% if section.supply_plenum_length %}
                - Supply Plenum Length: {{section.supply_plenum_length}}
                - Supply T.A.B Reading: {{section.supply_tab_reading}}
                - Supply K-Factor: {{section.supply_k_factor}}
                - Supply Flowrate: {{section.supply_flowrate_m3h}} m³/h ({{section.supply_flowrate_m3s}} m³/s)
                {% endif %}
                {% endif %}
                
                {% if section.min_percent %}
                Marvel Settings:
                - Min: {{section.min_percent}}%
                - Idle: {{section.idle_percent}}%
                - Design: {{section.design_percent}}%
                {% endif %}
            {% endfor %}
        {% endfor %}
        ```
        
        ### Global Marvel Technology Check
        Use the global flag to conditionally show content based on whether ANY canopy has Marvel:
        ```
        {% if has_marvel_technology %}
        ⚠️ MARVEL TECHNOLOGY PRESENT
        This project includes canopies with Marvel Technology. Special procedures apply.
        
        Marvel Canopies: {{marvel_canopies|length}}
        Standard Canopies: {{standard_canopies|length}}
        {% else %}
        ✅ STANDARD PROJECT
        This project uses standard canopy configurations only.
        
        Total Canopies: {{num_canopies}}
        {% endif %}
        ```
        
        ### Separate Tables for Marvel vs Standard Canopies
        ```
        ## Standard Canopies
        {% for canopy in standard_canopies %}
        Canopy {{canopy.index}}: {{canopy.canopy_model}} at {{canopy.canopy_location}}
        {% endfor %}
        
        ## Marvel Technology Canopies
        {% for canopy in marvel_canopies %}
        Canopy {{canopy.index}}: {{canopy.canopy_model}} at {{canopy.canopy_location}}
        Marvel Settings Available: Yes
        {% for section in canopy.sections %}
            Section {{section.index}} Marvel: {{section.min_percent}}% / {{section.idle_percent}}% / {{section.design_percent}}%
        {% endfor %}
        {% endfor %}
        ```
        
        ### UV System Variables
        Use these variables when UV technology is present in the project:
        
        **Global UV System Variables:**
        - `{{has_uv_technology}}` - Boolean: true if ANY canopy has UV system
        - `{{uv_checklist}}` - Global UV checklist data (if present)
        - `{{uv_checklist.completion_percentage}}` - Global completion percentage
        - `{{uv_checklist.completed_items}}` - Global completed items count
        - `{{uv_checklist.total_items}}` - Global total items count
        
        **Individual Canopy UV Variables:**
        - `{{canopy.is_uv}}` - Boolean: true if this canopy has UV system
        - `{{canopy.has_uv_in_name}}` - Boolean: true if model name contains 'UV'
        - `{{canopy.with_uv_checks}}` - Boolean: true if UV checks are enabled for this canopy
        - `{{canopy.uv_checklist}}` - Individual canopy UV checklist data (if enabled)
        - `{{canopy.uv_checklist.completion_percentage}}` - Canopy UV completion percentage
        - `{{canopy.uv_checklist.completed_items}}` - Canopy UV completed items
        - `{{canopy.uv_checklist.total_items}}` - Canopy UV total items
        - `{{canopy.uv_checklist.checklist_items}}` - Array of UV checklist items for this canopy
        
        **UV Template Examples:**
        ```
        {% if has_uv_technology %}
        🔆 UV SYSTEM PRESENT
        This project includes canopies with UV technology. UV system checks required.
        
        GLOBAL UV SYSTEM CHECKLIST:
        {% if uv_checklist %}
        UV System Completion: {{uv_checklist.completion_percentage}}%
        Completed Items: {{uv_checklist.completed_items}}/{{uv_checklist.total_items}}
        
        {% for item in uv_checklist.checklist_items %}
        - {{item.item}}: {{item.value}} {% if item.completed %}✓{% endif %}
        {% endfor %}
        {% endif %}
        
        UV CANOPIES IN PROJECT:
        {% for canopy in canopies %}
        {% if canopy.is_uv %}
        - {{canopy.canopy_model}} at {{canopy.canopy_location}}
        
        {% if canopy.with_uv_checks and canopy.uv_checklist %}
        UV Checklist for this canopy: {{canopy.uv_checklist.completion_percentage}}% complete
        {% for item in canopy.uv_checklist.checklist_items %}
        - {{item.item}}: {{item.value}} {% if item.completed %}✓{% endif %}
        {% endfor %}
        {% endif %}
        
        {% endif %}
        {% endfor %}
        {% else %}
        ✅ NO UV SYSTEM
        This project does not include UV technology canopies.
        {% endif %}
        ```
        
        ### CXW Model Variables (Special Handling)
        CXW models have different data structure and use anemometer readings:
        
        **CXW Canopy Variables:**
        - `{{canopy.is_cxw}}` - Boolean, true if canopy is CXW model
        - `{{canopy.grill_size}}` - Grill size (e.g., "600x600")
        - `{{canopy.number_of_sections}}` - Number of grills (not sections)
        
        **CXW Section (Grill) Variables:**
        - `{{section.anemometer_reading}}` - Anemometer reading in m/s
        - `{{section.free_area}}` - Free area in m²
        - `{{section.extract_flowrate_m3h}}` - Calculated flowrate in m³/h
        - `{{section.extract_flowrate_m3s}}` - Calculated flowrate in m³/s
        
        **CXW Template Example:**
        ```
        {% if canopy.is_cxw %}
        CXW Canopy {{canopy.index}}
        Grill Size: {{canopy.grill_size}}
        Number of Grills: {{canopy.number_of_sections}}
        
        {% for section in canopy.sections %}
        Grill {{section.index}}: {{section.anemometer_reading}} m/s, {{section.free_area}} m², {{section.extract_flowrate_m3s}} m³/s
        {% endfor %}
        {% endif %}
        ```
        
        ### Table Data Variables
        For creating tables similar to the Kitchen Canopy Air Readings format:
        
        **Extract Air Data (Always Available):**
        - `{{canopy.drawing_number}}`
        - `{{canopy.canopy_location}}`
        - `{{canopy.canopy_model}}`
        - `{{canopy.design_airflow}}`
        - `{{canopy.number_of_sections}}`
        - `{{canopy.extract_total_flowrate_m3s}}`
        
        **Supply Air Data (Only for models with 'F' in name, excluding CXW):**
        - Use `{% if canopy.has_f_in_name and not canopy.is_cxw %}` to conditionally show supply data
        - `{{canopy.supply_total_flowrate_m3s}}`
        
        **Section-Level Calculations:**
        Each section now includes calculated flowrates:
        - `{{section.extract_flowrate_m3h}}` - Extract flowrate in m³/h
        - `{{section.extract_flowrate_m3s}}` - Extract flowrate in m³/s
        - `{{section.supply_flowrate_m3h}}` - Supply flowrate in m³/h (if applicable)
        - `{{section.supply_flowrate_m3s}}` - Supply flowrate in m³/s (if applicable)
        """)
    
    with st.expander("🔧 Template Creation Tips", expanded=False):
        st.markdown("""
        ### Creating Effective Templates
        
        1. **Use Tables for Data Display**
           - Create Word tables and use template variables in cells
           - Use conditional blocks for models with/without 'F'
           
        2. **Conditional Content**
           ```
           {% if canopy.has_f_in_name %}
           This content only shows for models with 'F' in the name
           {% endif %}
           ```
           
        3. **Loops for Multiple Items**
           ```
           {% for canopy in canopies %}
           Canopy {{canopy.index}}: {{canopy.canopy_model}}
           {% endfor %}
           ```
           
        4. **Number Formatting**
           - Flowrates are pre-rounded: m³/h to 2 decimals, m³/s to 3 decimals
           - K-factors are displayed as provided by the system
           
        5. **Marvel Technology**
           ```
           <!-- Global Marvel check -->
           {% if has_marvel_technology %}
           This project includes Marvel Technology canopies.
           {% endif %}
           
           <!-- Section-level Marvel settings -->
           {% if section.min_percent %}
           Marvel Settings: {{section.min_percent}}% / {{section.idle_percent}}% / {{section.design_percent}}%
           {% endif %}
           
           <!-- Canopy-level Marvel check -->
           {% if canopy.with_marvel %}
           This canopy has Marvel Technology enabled.
           {% endif %}
           ```
           
        6. **UV Technology**
           ```
           <!-- Global UV check -->
           {% if has_uv_technology %}
           This project includes UV technology canopies. UV system checks required.
           {% endif %}
           
           <!-- UV checklist completion -->
           {% if uv_checklist %}
           UV System Completion: {{uv_checklist.completion_percentage}}%
           {% endif %}
           
           <!-- Canopy-level UV check -->
           {% if canopy.is_uv %}
           This canopy includes UV technology.
           {% endif %}
           
           <!-- Check for UV in model name -->
           {% if canopy.has_uv_in_name %}
           This canopy model has UV in its name.
           {% endif %}
           
           <!-- Individual canopy UV checklist -->
           {% if canopy.uv_checklist %}
           UV Checklist for this canopy: {{canopy.uv_checklist.completion_percentage}}% complete
           {% for item in canopy.uv_checklist.checklist_items %}
           - {{item.item}}: {{item.value}} {% if item.completed %}✓{% endif %}
           {% endfor %}
           {% endif %}
           ```
        """)
    
    with st.expander("⚠️ Common Issues & Solutions", expanded=False):
        st.markdown("""
        ### Troubleshooting Template Issues
        
        **Problem: Variables not populating**
        - Check spelling exactly matches variable names above
        - Ensure no extra spaces inside `{{ }}`
        - Use straight quotes, not smart quotes
        
        **Problem: Word splits variables across runs**
        - Type the entire variable in one go
        - Don't use autocorrect or formatting while typing variables
        - Copy-paste variables from this help if needed
        
        **Problem: Conditional blocks not working**
        - Ensure `{% %}` blocks are properly closed
        - Check for typos in condition names
        - Use `{% endif %}` to close `{% if %}` blocks
        
        **Problem: Loops not displaying data**
        - Verify loop variable names match exactly
        - Ensure proper indentation in nested loops
        - Use `{% endfor %}` to close `{% for %}` blocks
        
        **Problem: Table formatting issues**
        - Create the table structure in Word first
        - Add variables to existing cells
        - Test with simple variables before complex loops
        """)
    
    with st.expander("📝 Example Template Structure", expanded=False):
        st.markdown("""
        ### Sample Template Layout
        
        ```
        CANOPY COMMISSIONING REPORT
        
        Client: {{client_name}}
        Project: {{project_name}} ({{project_number}})
        Date: {{date_of_visit}}
        Engineer: {{engineer_name}}
        
        ## STANDARD CANOPIES
        {% for canopy in standard_canopies %}
        
        CANOPY {{canopy.index}} - {{canopy.canopy_model}}
        Location: {{canopy.canopy_location}}
        Drawing: {{canopy.drawing_number}}
        
        EXTRACT AIR DATA
        Design Flowrate: {{canopy.design_airflow}} m³/s
        Sections: {{canopy.number_of_sections}}
        Total Extract Flowrate: {{canopy.extract_total_flowrate_m3s}} m³/s
        
        {% for section in canopy.sections %}
        Section {{section.index}}: {{section.extract_ksa}} KSAs, {{section.extract_tab_reading}} Pa, {{section.extract_flowrate_m3s}} m³/s
        {% endfor %}
        
        {% if canopy.has_f_in_name %}
        SUPPLY AIR DATA
        Total Supply Flowrate: {{canopy.supply_total_flowrate_m3s}} m³/s
        
        {% for section in canopy.sections %}
        Section {{section.index}}: {{section.supply_plenum_length}}mm, {{section.supply_tab_reading}} Pa, {{section.supply_flowrate_m3s}} m³/s
        {% endfor %}
        {% endif %}
        
        {% endfor %}
        
        ## MARVEL TECHNOLOGY CANOPIES
        {% for canopy in marvel_canopies %}
        
        CANOPY {{canopy.index}} - {{canopy.canopy_model}} (WITH MARVEL)
        Location: {{canopy.canopy_location}}
        Drawing: {{canopy.drawing_number}}
        
        EXTRACT AIR DATA
        Design Flowrate: {{canopy.design_airflow}} m³/s
        Sections: {{canopy.number_of_sections}}
        Total Extract Flowrate: {{canopy.extract_total_flowrate_m3s}} m³/s
        
        {% for section in canopy.sections %}
        Section {{section.index}}: {{section.extract_ksa}} KSAs, {{section.extract_tab_reading}} Pa, {{section.extract_flowrate_m3s}} m³/s
        Marvel Settings: {{section.min_percent}}% / {{section.idle_percent}}% / {{section.design_percent}}%
        {% endfor %}
        
        {% if canopy.has_f_in_name %}
        SUPPLY AIR DATA
        Total Supply Flowrate: {{canopy.supply_total_flowrate_m3s}} m³/s
        
        {% for section in canopy.sections %}
        Section {{section.index}}: {{section.supply_plenum_length}}mm, {{section.supply_tab_reading}} Pa, {{section.supply_flowrate_m3s}} m³/s
        {% endfor %}
        {% endif %}
        
        {% endfor %}
        
        Generated: {{generation_date}} {{generation_time}}
        ```
        """)

def render_template_examples():
    """Render template examples and best practices."""
    with st.expander("📝 Template Examples & Best Practices", expanded=False):
        st.markdown("""
        ### 🎯 **Template Best Practices**
        
        1. **Use Tables**: Create tables in Word and use Jinja2 loops to populate rows
        2. **Conditional Sections**: Use `{% if %}` to show/hide entire sections
        3. **Formatting**: Apply Word formatting (bold, colors, etc.) to template text
        4. **Page Breaks**: Insert page breaks in template where needed
        5. **Headers/Footers**: Include company logos and page numbers in headers/footers
        """)
        
        st.markdown("### 📋 **Sample Table Structure**")
        st.markdown("""
        Create a table in Word with headers, then use this structure:
        """)
        
        st.code("""
| Canopy | Model | Location | Design Flow | Supply Flow | K-Factor |
|--------|-------|----------|-------------|-------------|----------|
{% for canopy in canopies %}
| {{ canopy.index }} | {{ canopy.canopy_model }} | {{ canopy.canopy_location }} | {{ canopy.design_airflow }} | {{ canopy.supply_airflow }} | {% for section in canopy.sections %}{{ section.k_factor }}{% if not loop.last %}, {% endif %}{% endfor %} |
{% endfor %}
        """, language="jinja2")
        
        st.markdown("### 🔧 **Advanced Features**")
        st.code("""
# Calculate totals:
Total Canopies: {{ canopies|length }}
Total Sections: {% set total_sections = 0 %}{% for canopy in canopies %}{% set total_sections = total_sections + canopy.sections|length %}{% endfor %}{{ total_sections }}

# Format dates:
Generated on: {{ generation_date|strftime('%B %d, %Y') }}

# Round numbers:
Airflow: {{ canopy.design_airflow|round(2) }} m³/s

# Check for empty values:
{% if canopy.drawing_number %}
Drawing: {{ canopy.drawing_number }}
{% else %}
Drawing: Not specified
{% endif %}
        """, language="jinja2") 