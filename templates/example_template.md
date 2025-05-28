# Example Word Template Structure

This is an example of how to structure your Word template with Jinja2 variables.

## Basic Report Information

**Report Type:** {{ report_type }}
**Client:** {{ client_name }}
**Project:** {{ project_name }} ({{ project_number }})
**Date of Visit:** {{ date_of_visit }}
**Engineer:** {{ engineer_name }}
**Generated:** {{ generation_date }} at {{ generation_time }}

---

## Canopy Summary

**Total Number of Canopies:** {{ num_canopies }}

{% for canopy in canopies %}

### Canopy {{ canopy.index }}

- **Drawing Number:** {{ canopy.drawing_number }}
- **Location:** {{ canopy.canopy_location }}
- **Model:** {{ canopy.canopy_model }}
- **Design Airflow:** {{ canopy.design_airflow }} m³/s
- **Supply Airflow:** {{ canopy.supply_airflow }} m³/s
- **Number of Sections:** {{ canopy.number_of_sections }}
  {% if canopy.canopy_length %}
- **Length:** {{ canopy.canopy_length }}mm
  {% endif %}
- **Marvel Technology:** {% if canopy.with_marvel %}Yes{% else %}No{% endif %}

{% if canopy.sections %}

#### Section Data

| Section | KSAs | K-Factor | T.A.B Reading | {% if canopy.with_marvel %}Marvel Settings{% endif %} |
|---------|------|----------|---------------|{% if canopy.with_marvel %}---------------{% endif %}|
{% for section in canopy.sections %}
| {{ section.index }} | {{ section.selected_ksa }} | {{ section.k_factor }} | {{ section.tab_reading }} | {% if canopy.with_marvel %}{{ section.min_percent }}% / {{ section.idle_percent }}% / {{ section.design_percent }}%{% endif %} |
{% endfor %}
{% endif %}

---

{% endfor %}

## Instructions for Creating Word Template

1. Create a new Word document
2. Copy the structure above (without the markdown formatting)
3. Replace the Jinja2 variables ({{ variable_name }}) with the actual template syntax
4. Format the document with your company branding, fonts, colors, etc.
5. Save as .docx file
6. Upload to the templates folder

## Template Variables Available

- Basic info: report_type, client_name, project_name, project_number, date_of_visit, engineer_name
- Generated info: generation_date, generation_time
- Canopy info: num_canopies, canopies (array)
- Each canopy has: index, drawing_number, canopy_location, canopy_model, with_marvel, design_airflow, supply_airflow, number_of_sections, canopy_length, sections (array)
- Each section has: index, selected_ksa, tab_reading, k_factor, min_percent, idle_percent, design_percent
