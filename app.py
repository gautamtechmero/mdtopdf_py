import streamlit as st
import streamlit.components.v1 as components
import markdown
import io
import os
import sys

# Import local stylesheet generator
import styles

# Declare custom workspace component
parent_dir = os.path.dirname(os.path.abspath(__file__))
component_dir = os.path.join(parent_dir, "editor_component")
markdown_workspace = components.declare_component("markdown_workspace", path=component_dir)

# Page setup
st.set_page_config(
    page_title="Markdown to PDF Converter Pro",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Header and element styling with custom typography and premium themes
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800&display=swap');
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
        max-width: 100% !important;
    }
    
    .main-title {
        font-family: 'Outfit', 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.3rem;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
        letter-spacing: -0.03em;
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 25px;
    }
    
    /* Make background deep and clean dark */
    .stApp {
        background-color: #0b0f19 !important;
        color: #f8fafc !important;
    }
    
    /* Premium Glassmorphic Settings Panel */
    div[data-testid="stBorderedContainer"] {
        background-color: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 12px !important;
        padding: 20px 24px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4) !important;
        margin-bottom: 20px !important;
    }
    
    /* Control headers styling */
    .control-section-header {
        font-family: 'Outfit', sans-serif;
        font-size: 0.9rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
        border-bottom: 1px solid #1f2937;
        padding-bottom: 6px;
    }
    
    /* Sleek Button Styles */
    div.stButton > button {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%) !important;
        color: #f8fafc !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        font-family: 'Inter', sans-serif;
        font-size: 13px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2) !important;
        height: 38px !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    div.stButton > button:hover {
        border-color: #60a5fa !important;
        color: #60a5fa !important;
        box-shadow: 0 4px 12px -1px rgba(96, 165, 250, 0.25) !important;
        transform: translateY(-1px);
    }
    
    /* File uploader styling */
    div[data-testid="stFileUploader"] {
        background-color: #111827 !important;
        border: 1px dashed #374151 !important;
        border-radius: 8px !important;
        padding: 6px !important;
        margin-bottom: 10px !important;
    }
    
    /* Hide Streamlit default components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    h1, h2, h3, h4, h5, h6, p, label {
        font-family: 'Inter', sans-serif !important;
    }
    
    label[data-testid="stWidgetLabel"] {
        color: #94a3b8 !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }
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
    import subprocess
    import sys
    
    # Margin formatting for Playwright (Optimized tighter spacing)
    margin_vals = {
        "narrow": "0.6cm",
        "normal": "1.2cm",
        "wide": "2.0cm"
    }
    margin_str = margin_vals.get(margins, "1.2cm")
    
    # Chromium footer template containing native page numbers
    footer_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 8px; color: #888888; width: 100%; text-align: right; padding-right: {margin_str}; box-sizing: border-box;">
        Page <span class="pageNumber"></span> of <span class="totalPages"></span>
    </div>
    """
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except Exception as e:
            err_msg = str(e)
            if "Executable doesn't exist" in err_msg or "playwright install" in err_msg.lower() or "looks like playwright was just installed" in err_msg.lower():
                # Let user know in Streamlit UI we are downloading
                st.info("Playwright Chromium browser not found. Automatically installing Chromium browser (this may take a minute)...")
                try:
                    # Run install command
                    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
                    st.success("Chromium installed successfully! Continuing PDF compilation...")
                    # Retry launching
                    browser = p.chromium.launch(headless=True)
                except Exception as install_err:
                    raise RuntimeError(f"Failed to auto-install Playwright Chromium: {install_err}") from install_err
            else:
                raise
        
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
st.markdown("<p class='subtitle'>Write or upload Markdown, customize layout settings, and download your styled PDF document.</p>", unsafe_allow_html=True)

# Retrieve the current markdown text directly from the editor's state key
md_text = st.session_state.markdown_editor_area

# Pre-compile PDF so the download button has the data available immediately
pdf_bytes = b""
pdf_error = None
if md_text.strip():
    try:
        # 1. Compile Markdown HTML
        html_body = markdown.markdown(
            md_text,
            extensions=['extra', 'toc', 'sane_lists', 'nl2br', 'markdown.extensions.codehilite'],
            extension_configs={
                'markdown.extensions.codehilite': {
                    'guess_lang': False,
                    'use_pygments': True,
                    'noclasses': False
                }
            }
        )
        # 2. Get layout variables (needed for compiling layout parameters)
        # These are read from session state if they exist, or set to defaults first
        p_theme = st.session_state.get("selected_theme_key", "GitHub Light")
        p_size = st.session_state.get("page_size_key", "A4")
        p_orient = st.session_state.get("orientation_key", "Portrait").lower()
        p_margins = st.session_state.get("margins_key", "normal")
        p_font = st.session_state.get("font_size_key", "14px")
        
        pdf_css = styles.get_theme_css(p_theme, pdf_mode=False)
        
        # Determine CSS page size configuration
        size_css = p_size
        if p_orient == 'landscape':
            size_css = f"{p_size} landscape"
            
        margin_vals = {"narrow": "0.6cm", "normal": "1.2cm", "wide": "2.0cm"}
        margin_str = margin_vals.get(p_margins, "1.2cm")

        pdf_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Exported PDF</title>
    <style>
        @page {{
            size: {size_css};
            margin: {margin_str};
        }}
        {pdf_css}
        .page-break {{
            page-break-before: always;
            break-before: page;
        }}
        h1, h2, h3, h4, h5, h6 {{
            page-break-after: avoid !important;
            break-after: avoid !important;
        }}
        h1 + *, h2 + *, h3 + *, h4 + *, h5 + *, h6 + * {{
            page-break-before: avoid !important;
            break-before: avoid !important;
        }}
        pre, blockquote, table, tr, li {{
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }}
        p {{
            word-wrap: break-word;
            orphans: 3 !important;
            widows: 3 !important;
        }}
        body {{
            word-wrap: break-word;
            font-size: {p_font} !important;
            padding: 0 !important;
            margin: 0 !important;
        }}
        h1:first-child, h2:first-child, p:first-child {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        table {{
            width: 100% !important;
            max-width: 100% !important;
            table-layout: auto !important;
            border-collapse: collapse !important;
        }}
        table td, table th {{
            word-break: normal !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            min-width: 80px !important;
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
        pdf_bytes = generate_pdf_bytes(pdf_html, p_size, p_orient, p_margins)
    except Exception as e:
        pdf_error = str(e)

# TOP DASHBOARD CONTROLS (Main Page, Column-based Layout wrapped in premium card container)
with st.container(border=True):
    col_file, col_style, col_layout = st.columns([1.2, 1, 1])
    
    with col_file:
        st.markdown("<div class='control-section-header'>📂 File Operations</div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload Markdown (.md) File",
            type=["md", "txt", "markdown"],
            key="uploaded_file",
            on_change=handle_file_upload,
            label_visibility="collapsed"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🗑️ Clear Editor", use_container_width=True):
                st.session_state.markdown_editor_area = ""
                st.rerun()
        with col_btn2:
            if not md_text.strip():
                st.button("⬇️ Download PDF", disabled=True, use_container_width=True, help="Write or upload markdown to export")
            elif pdf_error is not None:
                st.button("⚠️ PDF Error", disabled=True, use_container_width=True, help=f"Error compiling PDF: {pdf_error}")
            else:
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_bytes,
                    file_name="document.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

    with col_style:
        st.markdown("<div class='control-section-header'>🎨 Typography & Theme</div>", unsafe_allow_html=True)
        theme_options = list(styles.THEME_BASES.keys())
        selected_theme = st.selectbox("Style Theme", theme_options, index=0, key="selected_theme_key")
        font_size = st.selectbox("Font Size", ["11px", "12px", "13px", "14px", "15px", "16px"], index=3, key="font_size_key")

    with col_layout:
        st.markdown("<div class='control-section-header'>📐 Page Layout</div>", unsafe_allow_html=True)
        page_size = st.selectbox("Page Size", ["A4", "Letter", "Legal", "A3", "A5"], index=0, key="page_size_key")
        orientation = st.radio("Orientation", ["Portrait", "Landscape"], index=0, horizontal=True, key="orientation_key").lower()
        margins = st.select_slider("Margins", options=["narrow", "normal", "wide"], value="normal", key="margins_key")

st.markdown("---")

# RENDER CUSTOM WORKSPACE COMPONENT (Unified Editor & Live Preview with dynamic View Mode controls)
theme_css = styles.get_theme_css(selected_theme, pdf_mode=False)

returned_text = markdown_workspace(
    initial_value=st.session_state.markdown_editor_area,
    theme_css=theme_css,
    page_size=page_size,
    orientation=orientation,
    margins=margins,
    font_size=font_size,
    height=800,
    key="workspace_editor_preview"
)

# If the text was changed inside Javascript and returned to Streamlit, update state and rerun
if returned_text is not None and returned_text != st.session_state.markdown_editor_area:
    st.session_state.markdown_editor_area = returned_text
    st.rerun()

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
