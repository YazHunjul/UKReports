import streamlit as st
import base64
from io import BytesIO
from PIL import Image
from datetime import datetime
from src.utils.session_manager import get_form_data, update_form_data

# Import the drawable canvas - we know it's available
from streamlit_drawable_canvas import st_canvas

def render_signature_and_notes():
    """Render signature drawing canvas and additional notes section."""
    st.header("📝 Additional Notes & Signature")
    
    # Additional Notes Section with multiple notes support
    st.subheader("📄 Additional Notes")
    
    # Get existing notes from session state
    notes_list = get_form_data('notes_list', [])
    
    # Display existing notes
    if notes_list:
        st.markdown("**Current Notes:**")
        for i, note in enumerate(notes_list):
            col1, col2 = st.columns([4, 1])
            with col1:
                # Allow editing existing notes
                updated_note = st.text_area(
                    f"Note {i + 1}",
                    value=note,
                    height=80,
                    key=f"note_edit_{i}",
                    help=f"Edit note {i + 1}"
                )
                # Update the note if it changed
                if updated_note != note:
                    notes_list[i] = updated_note
            
            with col2:
                st.write("")  # Add some spacing
                if st.button(f"🗑️ Delete", key=f"delete_note_{i}", help=f"Delete note {i + 1}"):
                    notes_list.pop(i)
                    st.rerun()
    
    # Add new note section
    st.markdown("**Add New Note:**")
    col1, col2 = st.columns([4, 1])
    
    with col1:
        new_note = st.text_area(
            "New Note",
            placeholder="Enter a new note, observation, or comment here...",
            height=100,
            key="new_note_input",
            help="Add a new note to the report"
        )
    
    with col2:
        st.write("")  # Add some spacing
        if st.button("➕ Add Note", type="primary", help="Add this note to the list"):
            if new_note.strip():
                notes_list.append(new_note.strip())
                st.rerun()
            else:
                st.warning("Please enter some text before adding a note.")
    
    # Display summary
    if notes_list:
        st.success(f"✅ {len(notes_list)} note(s) added to the report")
    else:
        st.info("ℹ️ No notes added yet. Use the text area above to add notes.")
    
    # Date and Print Name Section (moved before signature)
    st.subheader("📅 Signature Details")
    
    # Get engineer name from general info for auto-population
    engineer_name = get_form_data('engineer_name', '')
    
    # Initialize session state values if not exists
    if 'signature_date' not in st.session_state:
        st.session_state.signature_date = get_form_data('signature_date', datetime.now().date())
    if 'print_name' not in st.session_state:
        st.session_state.print_name = get_form_data('print_name', engineer_name)
    
    col1, col2 = st.columns(2)
    
    with col1:
        signature_date = st.date_input(
            "Date",
            key="signature_date",
            help="Date of signature"
        )
    
    with col2:
        print_name = st.text_input(
            "Print Name",
            key="print_name",
            placeholder="Enter your full name",
            help="Print your full name clearly"
        )
    
    # Get values from session state
    signature_date_value = st.session_state.get('signature_date', datetime.now().date())
    print_name_value = st.session_state.get('print_name', engineer_name)
    
    # Signature Section
    st.subheader("✍️ Engineer Signature")
    st.markdown("Please draw your signature in the box below:")
    
    # Create signature canvas
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Canvas for signature drawing
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0)",  # Transparent fill
            stroke_width=2,
            stroke_color="#000000",  # Black stroke
            background_color="#FFFFFF",  # White background
            background_image=None,
            update_streamlit=True,
            height=200,
            width=600,
            drawing_mode="freedraw",
            point_display_radius=0,
            key="signature_canvas",
        )
    
    with col2:
        st.markdown("**Instructions:**")
        st.markdown("• Use your mouse or touchscreen to draw")
        st.markdown("• Draw your signature clearly")
        st.markdown("• Click 'Clear Signature' to start over")
        
        if st.button("🗑️ Clear Signature", type="secondary"):
            st.rerun()
    
    # Process signature data
    signature_data = None
    
    if canvas_result.image_data is not None:
        # Convert canvas to image
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        
        # Check if there's actually a signature (not just blank canvas)
        # Convert to grayscale to check for non-white pixels
        grayscale = img.convert('L')
        pixels = list(grayscale.getdata())
        
        # If there are pixels that are not white (255), there's a signature
        has_signature = any(pixel < 250 for pixel in pixels)  # Allow for slight variations
        
        if has_signature:
            # Convert to base64 for storage
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            signature_data = base64.b64encode(buffered.getvalue()).decode()
            
            st.success("✅ Signature captured successfully!")
        else:
            st.info("ℹ️ Please draw your signature in the canvas above")
    
    # Update session state
    update_form_data({
        'notes_list': notes_list,
        'additional_notes': '\n\n'.join(notes_list),  # Keep backward compatibility
        'signature_data': signature_data,
        'signature_date': signature_date_value,
        'print_name': print_name_value,
        'has_signature': signature_data is not None
    })
    
    return {
        'notes_list': notes_list,
        'additional_notes': '\n\n'.join(notes_list),  # Keep backward compatibility
        'signature_data': signature_data,
        'signature_date': signature_date_value,
        'print_name': print_name_value,
        'has_signature': signature_data is not None
    }

def get_signature_image_for_template(signature_base64: str) -> str:
    """
    Convert base64 signature data to a format suitable for Word template.
    
    Args:
        signature_base64: Base64 encoded signature image
        
    Returns:
        Base64 string suitable for Word template
    """
    if not signature_base64:
        return ""
    
    try:
        # Decode base64 to image
        image_data = base64.b64decode(signature_base64)
        img = Image.open(BytesIO(image_data))
        
        # Convert to RGB if needed (remove alpha channel)
        if img.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
            img = background
        
        # Resize if too large (optional)
        max_width = 400
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert back to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
        
    except Exception as e:
        st.error(f"Error processing signature: {e}")
        return "" 