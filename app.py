import streamlit as st
import markdown
import io
import os
import sys

# Import local stylesheet generator
import styles

# Page setup
st.set_page_config(
    page_title="Markdown to PDF Converter Pro",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Header and element styling
st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2.0rem !important;
    }
    .main-title {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }
    .control-box {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    /* Hide Streamlit sidebar button since we don't use the sidebar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state for editor content directly
if 'markdown_editor_area' not in st.session_state:
    st.session_state.markdown_editor_area = ""

# Callback for file upload to update editor state directly
def handle_file_upload():
    if st.session_state.uploaded_file is not None:
        try:
            uploaded_bytes = st.session_state.uploaded_file.read()
            # Decode file contents to string and store directly in the text area's state key
            st.session_state.markdown_editor_area = uploaded_bytes.decode("utf-8")
        except Exception as e:
            st.error(f"Error reading file: {e}")

# PDF Generation Function
def generate_pdf_bytes(html_content):
    pdf_buffer = io.BytesIO()
    from xhtml2pdf import pisa
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)
    if pisa_status.err:
        raise Exception(f"xhtml2pdf generation failed with error code: {pisa_status.err}")
    return pdf_buffer.getvalue()

# Application title
st.markdown("<h1 class='main-title'>📝 Markdown to PDF Converter Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Write Markdown in the editor, customize settings, and instantly download a styled PDF document.</p>", unsafe_allow_html=True)

# TOP DASHBOARD CONTROLS (Main Page, Column-based Layout)
st.markdown("### ⚙️ Document Controls & Layout Settings")

col_upload, col_settings = st.columns([1, 1])

with col_upload:
    st.markdown("##### 📂 File Operations")
    uploaded_file = st.file_uploader(
        "Upload Markdown (.md) File",
        type=["md", "txt", "markdown"],
        key="uploaded_file",
        on_change=handle_file_upload,
        label_visibility="collapsed"
    )
    
    if st.button("🗑️ Clear Editor", use_container_width=True):
        st.session_state.markdown_editor_area = ""
        st.rerun()

with col_settings:
    st.markdown("##### 🎨 Styling & Margins")
    
    col_theme, col_params = st.columns(2)
    
    with col_theme:
        theme_options = list(styles.THEME_BASES.keys())
        selected_theme = st.selectbox("Style Theme", theme_options, index=0)
        page_size = st.selectbox("Page Size", ["A4", "Letter", "Legal", "A3", "A5"], index=0)
        
    with col_params:
        orientation = st.radio("Orientation", ["Portrait", "Landscape"], index=0).lower()
        margins = st.select_slider("Margins", options=["narrow", "normal", "wide"], value="normal")

st.markdown("---")

# Retrieve the current markdown text directly from the editor's state key
md_text = st.session_state.markdown_editor_area

# Generate HTML body from markdown
try:
    # If the text is empty, display a placeholder to keep preview clean
    if not md_text.strip():
        html_body = "<p style='color: #94a3b8; font-style: italic;'>Your rendered PDF preview will appear here...</p>"
    else:
        html_body = markdown.markdown(
            md_text,
            extensions=['extra', 'codehilite', 'toc', 'sane_lists', 'nl2br']
        )
except Exception as e:
    st.error(f"Markdown compilation error: {e}")
    html_body = f"<p>Error compiling markdown: {e}</p>"

# Retrieve appropriate CSS stylesheets
theme_css = styles.get_theme_css(
    selected_theme,
    pdf_mode=False
)

preview_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Markdown Preview</title>
    <style>
        {theme_css}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""

pdf_css = styles.get_theme_css(
    selected_theme,
    pdf_mode=True,
    page_size=page_size,
    orientation=orientation,
    margins=margins
)

pdf_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Exported PDF</title>
    <style>
        {pdf_css}
    </style>
</head>
<body>
    {html_body}
    <div id="footer_content">
        Page <pdf:pagenumber/> of <pdf:pagecount/>
    </div>
</body>
</html>
"""

# PDF Compilation & Download Button Row
pdf_bytes = b""
pdf_error = None

# Only compile PDF if there is content in the editor
if md_text.strip():
    try:
        pdf_bytes = generate_pdf_bytes(pdf_html)
    except Exception as e:
        pdf_error = str(e)

# Render a prominent PDF download button at the top
st.markdown("### 💾 Export Document")
if not md_text.strip():
    st.info("Write or upload markdown below to enable PDF export.")
elif pdf_error is None:
    st.download_button(
        label="⬇️ Download PDF Document",
        data=pdf_bytes,
        file_name="document.pdf",
        mime="application/pdf",
        use_container_width=True
    )
else:
    st.error("PDF Generator encountered a configuration issue...")
    st.caption(f"Error: {pdf_error}")

st.markdown("---")

# MAIN EDITOR & PREVIEW WORKSPACE
col_editor, col_preview = st.columns([1, 1])

with col_editor:
    st.markdown("### ✍️ Markdown Editor")
    # Text area binds directly to markdown_editor_area in session state
    st.text_area(
        "Write your markdown here:",
        key="markdown_editor_area",
        height=650,
        label_visibility="collapsed",
        placeholder="Type or paste your Markdown here..."
    )
        
with col_preview:
    st.markdown("### 👁️ Live Styled Preview")
    st.components.v1.html(preview_html, height=650, scrolling=True)

# FOOTER REFERENCE GUIDE
with st.expander("📖 PDF Layout & Page Breaks Guide", expanded=False):
    st.markdown("""
    #### Page Breaks in PDF
    To split your PDF document into multiple pages, use this exact HTML snippet:
    ```html
    <div class="page-break"></div>
    ```
    The PDF engine will automatically start a new page after this tag.
    
    #### Table Styling
    Markdown tables are automatically styled with matching headers and subtle alternating row backgrounds depending on the theme selected.
    
    #### Custom CSS Overrides
    If you wish to customize margins or colors directly, you can modify the `styles.py` file or wrap elements inside HTML tags like `<div style="...">`.
    """)
