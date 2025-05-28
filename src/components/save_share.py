import streamlit as st
from src.utils.session_manager import get_form_data, get_shareable_url, serialize_form_data_to_url
from src.utils.progress_tracker import calculate_progress

def render_save_share_section():
    """Render the save and share functionality section."""
    st.header("💾 Save & Share Progress")
    
    # Get current form data and progress
    form_data = get_form_data()
    progress = calculate_progress()
    
    # Show current progress
    st.markdown("### 📊 Current Progress")
    progress_bar = st.progress(progress)
    st.markdown(f"**{progress:.1%} Complete**")
    
    # Check if there's any data to save
    has_data = bool(form_data and any(form_data.values()))
    
    if not has_data:
        st.info("ℹ️ No data to save yet. Please fill out some information first.")
        return
    
    # Save and Share section
    st.markdown("### 🔗 Share with Technician")
    st.markdown("""
    **Workflow:**
    1. **Office Staff**: Fill out basic information (client, project details, canopy configurations)
    2. **Generate Link**: Create a shareable link with pre-filled data
    3. **Share**: Send the link to the onsite technician
    4. **Technician**: Opens the link and completes technical measurements
    """)
    
    if st.button("🔗 Generate Shareable Link", type="primary", help="Create a link to share with the technician"):
        with st.spinner("Generating shareable link..."):
            try:
                # Get the current URL info from browser
                current_url = "localhost:8535"  # Default fallback
                
                # Try to get actual URL from headers or context
                try:
                    if hasattr(st, 'context') and hasattr(st.context, 'headers'):
                        host = st.context.headers.get("host", "localhost:8535")
                        current_url = host
                except:
                    pass
                
                # Serialize form data
                serialized_data = serialize_form_data_to_url()
                
                if serialized_data:
                    # Create shareable URL
                    shareable_url = f"http://{current_url}/?data={serialized_data}"
                    
                    # Store in session state for display
                    st.session_state.shareable_url = shareable_url
                    st.success("✅ Shareable link generated!")
                else:
                    st.error("❌ Failed to generate shareable link")
                    
            except Exception as e:
                st.error(f"❌ Error generating link: {e}")
    
    # Display the shareable URL if generated
    if hasattr(st.session_state, 'shareable_url'):
        st.markdown("### 🔗 Shareable Link")
        st.text_input(
            "Copy this link to share:",
            value=st.session_state.shareable_url,
            help="Select all text and copy (Ctrl+C or Cmd+C)"
        )
        
        st.markdown("### 📧 Email Template")
        
        # Get project info for email template
        client_name = form_data.get('client_name', '[Client Name]')
        project_name = form_data.get('project_name', '[Project Name]')
        project_number = form_data.get('project_number', '[Project Number]')
        
        email_template = f"""Subject: Canopy Commissioning - {project_name} ({project_number})

Hi [Technician Name],

Please complete the canopy commissioning for the following project:

Client: {client_name}
Project: {project_name}
Project Number: {project_number}
Progress: {progress:.1%} complete (basic info filled)

Instructions:
1. Click the link below to open the pre-filled commissioning form
2. Complete the technical measurements and readings
3. Add any additional notes
4. Generate and download the final report

Link: {st.session_state.shareable_url}

Please complete the commissioning and send the final report when done.

Thanks!"""
        
        st.text_area(
            "Email Template (copy and customize as needed):",
            value=email_template.strip(),
            height=300,
            help="Copy this template and customize it for your email"
        )

def render_load_shared_data_notification():
    """Show notification if data was loaded from a shared link."""
    if hasattr(st.session_state, 'data_loaded_from_url') and st.session_state.data_loaded_from_url:
        st.success("✅ Pre-filled data loaded from shared link!")
        st.info("👨‍🔧 You can now complete the technical measurements and generate the final report.")
        
        # Clear the flag so it doesn't show again
        del st.session_state.data_loaded_from_url 