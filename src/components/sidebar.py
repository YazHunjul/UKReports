import streamlit as st
from src.utils.progress_tracker import calculate_detailed_progress
from src.utils.session_manager import get_form_data

def render_sidebar():
    """Render the sidebar with progress tracking and navigation."""
    with st.sidebar:
        st.header("📊 Project Status")
        
        # Progress indicator
        progress, completed_fields, total_fields = calculate_detailed_progress()
        
        st.progress(progress)
        st.write(f"Completed: {completed_fields}/{total_fields} fields")
        
        st.markdown("---")
        st.subheader("🚀 Next Steps")
        st.write("1. ✅ Report Type Selection")
        st.write("2. ✅ General Information")
        
        if get_form_data('report_type') == "Canopy Commissioning":
            st.write("3. ✅ Canopy Configuration")
            st.write("4. ⏳ Kitchen Canopy Air Readings")
            st.write("5. ⏳ Supply Air Data")
            st.write("6. ⏳ Report Generation")
        else:
            st.write("3. ⏳ Additional Sections")
            st.write("4. ⏳ Report Generation") 