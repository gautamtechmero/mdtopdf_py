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
    /* Hide Streamlit sidebar button since we don't use the sidebar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Theme metadata for outer background, paper background, and text colors in the preview
THEME_METADATA = {
    "GitHub Light": {
        "page_bg": "#ffffff",
        "outer_bg": "#f1f5f9",
        "text_color": "#24292f"
    },
    "GitHub Dark": {
        "page_bg": "#0d1117",
        "outer_bg": "#030712",
        "text_color": "#c9d1d9"
    },
    "Academic / Formal": {
        "page_bg": "#fdfdfd",
        "outer_bg": "#f1f5f9",
        "text_color": "#111111"
    },
    "Sleek Modern": {
        "page_bg": "#f8fafc",
        "outer_bg": "#e2e8f0",
        "text_color": "#334155"
    },
    "Minimalist": {
        "page_bg": "#ffffff",
        "outer_bg": "#f8fafc",
        "text_color": "#111111"
    }
}

# Initialize session state for editor content directly
if 'markdown_editor_area' not in st.session_state:
    st.session_state.markdown_editor_area = ""

# Callback for file upload to update editor state directly
def handle_file_upload():
    if st.session_state.uploaded_file is not None:
        try:
            uploaded_bytes = st.session_state.uploaded_file.read()
            st.session_state.markdown_editor_area = uploaded_bytes.decode("utf-8")
        except Exception as e:
            st.error(f"Error reading file: {e}")

# PDF Generation Function using Playwright (Chromium)
def generate_pdf_bytes(html_content, page_size, orientation, margins):
    from playwright.sync_api import sync_playwright
    
    # Margin formatting for Playwright
    margin_vals = {
        "narrow": "1.0cm",
        "normal": "2.0cm",
        "wide": "3.0cm"
    }
    margin_str = margin_vals.get(margins, "2.0cm")
    
    # Chromium footer template containing native page numbers
    footer_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 8px; color: #888888; width: 100%; text-align: right; padding-right: {margin_str}; box-sizing: border-box;">
        Page <span class="pageNumber"></span> of <span class="totalPages"></span>
    </div>
    """
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_content)
        
        landscape_bool = (orientation == 'landscape')
        
        # Print page to PDF bytes
        pdf_data = page.pdf(
            format=page_size,
            landscape=landscape_bool,
            print_background=True,
            display_header_footer=True,
            header_template="<span></span>", # Empty header
            footer_template=footer_html,
            margin={
                "top": margin_str,
                "bottom": margin_str,
                "left": margin_str,
                "right": margin_str
            }
        )
        browser.close()
        return pdf_data

# Application title
st.markdown("<h1 class='main-title'>📝 Markdown to PDF Converter Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Write or upload Markdown, customize style theme and PDF layout settings, and download your document.</p>", unsafe_allow_html=True)

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

# Retrieve appropriate CSS theme styles
theme_css = styles.get_theme_css(selected_theme, pdf_mode=False)

# Fetch theme metadata for paper layout
meta = THEME_METADATA.get(selected_theme, THEME_METADATA["GitHub Light"])
page_bg = meta["page_bg"]
outer_bg = meta["outer_bg"]
text_color = meta["text_color"]

# Compile standalone HTML doc for Preview (Paper Sheet style, responsive)
preview_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Markdown Preview</title>
    <style>
        {theme_css}
        
        /* Layout overrides to simulate a physical paper sheet */
        html, body {{
            background-color: {outer_bg} !important;
            margin: 0 !important;
            padding: 15px !important;
            display: flex;
            justify-content: center;
            box-sizing: border-box;
        }}
        
        .page-container {{
            background-color: {page_bg} !important;
            color: {text_color} !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(0, 0, 0, 0.08);
            padding: 1.5cm;
            width: 100%;
            max-width: 800px;
            min-height: 1050px; /* A4 aspect ratio representation */
            box-sizing: border-box;
            border-radius: 4px;
            text-align: left;
        }}
        
        /* Force body rules to apply nicely inside the container instead */
        body {{
            padding: 0 !important;
            background: transparent !important;
        }}
        
        /* Responsive table wrapping */
        table {{
            width: 100% !important;
            table-layout: auto !important;
        }}
        table td, table th {{
            word-break: break-word !important;
            max-width: 250px;
        }}
        img {{
            max-width: 100% !important;
            height: auto !important;
        }}
    </style>
</head>
<body>
    <div class="page-container">
        {html_body}
    </div>
</body>
</html>
"""

# Compile standard HTML doc for PDF compiler (without outer borders, using real print styling)
pdf_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Exported PDF</title>
    <style>
        {theme_css}
        
        /* standard print page-breaks and wrapping */
        .page-break {{
            page-break-before: always;
            break-before: page;
        }}
        pre, blockquote, table, tr {{
            page-break-inside: avoid;
            break-inside: avoid;
        }}
        body {{
            word-wrap: break-word;
        }}
        
        /* Ensure table text wraps correctly in the printed PDF */
        table {{
            width: 100% !important;
            table-layout: auto !important;
            border-collapse: collapse;
        }}
        table td, table th {{
            word-break: break-word !important;
        }}
        img {{
            max-width: 100% !important;
            height: auto !important;
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""

# PDF Compilation & Download Button Row
pdf_bytes = b""
pdf_error = None

# Only compile PDF if there is content in the editor
if md_text.strip():
    try:
        pdf_bytes = generate_pdf_bytes(pdf_html, page_size, orientation, margins)
    except Exception as e:
        pdf_error = str(e)

# Render a prominent PDF download button
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
    st.text_area(
        "Write your markdown here:",
        key="markdown_editor_area",
        height=700,
        label_visibility="collapsed",
        placeholder="Type or paste your Markdown here..."
    )
        
with col_preview:
    st.markdown("### 👁️ Live Styled Preview")
    st.components.v1.html(preview_html, height=700, scrolling=True)

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
