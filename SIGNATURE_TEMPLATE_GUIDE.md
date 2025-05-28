# Signature Image and Notes in Word Templates Guide

## How to Use Signature Images and Multiple Notes in Your Word Templates

The signature drawing functionality now provides proper image embedding in Word documents, and the notes system supports multiple individual notes.

## Template Variables Available

### Text Variables

- `{{ additional_notes }}` - All notes combined as single text (backward compatibility)
- `{{ notes_list }}` - Array of individual notes for iteration
- `{{ has_notes }}` - Boolean flag if any notes exist
- `{{ signature_date }}` - Date of signature
- `{{ print_name }}` - Printed name
- `{{ has_signature }}` - Boolean flag if signature exists

### Image Variable

- `{{ signature_image }}` - **Use this for the actual signature image**
- `{{ signature_image_base64 }}` - Base64 string (backup, not recommended for display)

## How to Use Multiple Notes in Your Template

### Method 1: Iterate Over Individual Notes (Recommended)

```
ADDITIONAL NOTES
{% for note in notes_list %}
{{ loop.index }}. {{ note }}

{% endfor %}
```

### Method 2: Check if Notes Exist Before Displaying

```
{% if has_notes %}
ADDITIONAL NOTES
{% for note in notes_list %}
• {{ note }}

{% endfor %}
{% endif %}
```

### Method 3: Numbered List with Custom Formatting

```
{% if has_notes %}
ADDITIONAL NOTES AND OBSERVATIONS

{% for note in notes_list %}
Note {{ loop.index }}: {{ note }}

{% endfor %}
{% endif %}
```

### Method 4: Backward Compatibility (Single Text Block)

```
ADDITIONAL NOTES
{{ additional_notes }}
```

## How to Add Signature Image to Your Template

### Method 1: Direct Image Insertion (Recommended)

In your Word template, simply add:

```
{{ signature_image }}
```

This will insert the signature as an actual image in the document.

### Method 2: With Text Context

```
Engineer Signature: {{ signature_image }}
Date: {{ signature_date }}
Print Name: {{ print_name }}
```

### Method 3: In a Table

You can also use it in tables:

```
| Field | Value |
|-------|-------|
| Signature | {{ signature_image }} |
| Date | {{ signature_date }} |
| Print Name | {{ print_name }} |
```

## Complete Example Template Section

```
{% if has_notes %}
ADDITIONAL NOTES AND OBSERVATIONS

{% for note in notes_list %}
{{ loop.index }}. {{ note }}

{% endfor %}
{% endif %}

ENGINEER SIGNATURE
Signature: {{ signature_image }}
Date: {{ signature_date }}
Print Name: {{ print_name }}
```

## Image Properties

The signature image is automatically:

- **Resized** to maximum 300x100 pixels
- **Converted** to RGB format (removes transparency)
- **Optimized** for document embedding
- **Scaled** to appropriate size in inches

## Notes System Features

The new notes system provides:

- **Multiple Notes**: Add as many individual notes as needed
- **Edit Notes**: Modify existing notes after adding them
- **Delete Notes**: Remove individual notes
- **Automatic Numbering**: Templates can use `{{ loop.index }}` for numbering
- **Backward Compatibility**: Old templates using `{{ additional_notes }}` still work

## Troubleshooting

### If you see numbers/letters instead of image:

- Make sure you're using `{{ signature_image }}` not `{{ signature_image_base64 }}`
- Ensure your Word template is saved as .docx format
- Check that the signature was actually drawn (not just a blank canvas)

### If image doesn't appear:

- Verify that a signature was captured (you should see "✅ Signature captured successfully!")
- Check that the template file exists and is accessible
- Make sure you're using the correct template variable name

### If notes don't appear:

- Check that notes were actually added (you should see "✅ X note(s) added to the report")
- Use `{% if has_notes %}` to conditionally display notes section
- Make sure you're using the correct Jinja2 syntax for loops

## Technical Details

- **Format**: PNG images embedded as InlineImage objects
- **Size**: Automatically scaled to fit document layout
- **Quality**: Optimized for document printing and viewing
- **Compatibility**: Works with all modern Word versions (.docx format)
- **Notes Storage**: Individual notes stored as array, combined text for compatibility
