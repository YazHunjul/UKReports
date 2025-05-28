import streamlit as st
import os
from src.utils.session_manager import clear_form_data, get_form_data
from src.utils.document_generator import generate_document, generate_filename

def render_action_buttons():
    """Render action buttons for document generation."""
    st.header("📄 Document Generation")
    
    # Get form data to determine report type
    form_data = get_form_data()
    report_type = form_data.get('report_type', '')
    
    if report_type:
        # Automatically select template based on report type
        template_filename = get_template_for_report_type(report_type)
        template_path = os.path.join('templates', template_filename)
        
        # Check if template exists
        if os.path.exists(template_path):
            st.info(f"📋 Using template: **{template_filename}** for {report_type}")
            
            if st.button("📥 Generate & Download Document", type="primary"):
                try:
                    doc_bytes = generate_document(template_path)
                    filename = generate_filename(form_data)
                    
                    st.download_button(
                        label="💾 Download Generated Document",
                        data=doc_bytes,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    
                    st.success("✅ Document generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error generating document: {str(e)}")
                    st.exception(e)
        else:
            st.error(f"❌ Template not found: {template_filename}")
            st.info("Please ensure the correct template file is in the templates/ directory.")
    else:
        st.info("ℹ️ Please select a report type to generate a document.")

def get_template_for_report_type(report_type: str) -> str:
    """Get the template filename based on report type."""
    template_mapping = {
        "Canopy Commissioning": "Canopy Commissioning Report Template 2022.docx",
        "Supply Air Analysis": "supply_air_analysis_template.docx", 
        "Full System Report": "full_system_report_template.docx"
    }
    
    return template_mapping.get(report_type, "canopy_commissioning_template.docx")

 