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

# TOP DASHBOARD CONTROLS (Main Page, Column-based Layout)
st.markdown("### ⚙️ Document Controls & Layout Settings")

col_file, col_style, col_layout = st.columns([1.2, 1, 1])

with col_file:
    st.markdown("##### 📂 File Operations")
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
    st.markdown("##### 🎨 Typography & Theme")
    theme_options = list(styles.THEME_BASES.keys())
    selected_theme = st.selectbox("Style Theme", theme_options, index=0, key="selected_theme_key")
    font_size = st.selectbox("Font Size", ["11px", "12px", "13px", "14px", "15px", "16px"], index=3, key="font_size_key")

with col_layout:
    st.markdown("##### 📐 Page Layout")
    page_size = st.selectbox("Page Size", ["A4", "Letter", "Legal", "A3", "A5"], index=0, key="page_size_key")
    orientation = st.radio("Orientation", ["Portrait", "Landscape"], index=0, horizontal=True, key="orientation_key").lower()
    margins = st.select_slider("Margins", options=["narrow", "normal", "wide"], value="normal", key="margins_key")

st.markdown("---")

# Compile Preview HTML
try:
    if not md_text.strip():
        html_body_prev = "<p style='color: #94a3b8; font-style: italic;'>Your rendered PDF preview will appear here...</p>"
    else:
        html_body_prev = markdown.markdown(
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
except Exception as e:
    html_body_prev = f"<p>Error compiling markdown: {e}</p>"

theme_css = styles.get_theme_css(selected_theme, pdf_mode=False)
meta = THEME_METADATA.get(selected_theme, THEME_METADATA["GitHub Light"])
page_bg = meta["page_bg"]
outer_bg = meta["outer_bg"]
text_color = meta["text_color"]

margin_vals = {"narrow": "0.6cm", "normal": "1.2cm", "wide": "2.0cm"}
margin_str = margin_vals.get(margins, "1.2cm")

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
            padding: 10px !important;
            display: flex;
            justify-content: center;
            box-sizing: border-box;
        }}
        
        .page-container {{
            background-color: {page_bg} !important;
            color: {text_color} !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(0, 0, 0, 0.08);
            padding: {margin_str};
            width: 100%;
            max-width: 800px;
            min-height: 1050px;
            box-sizing: border-box;
            border-radius: 4px;
            text-align: left;
        }}
        
        body {{
            padding: 0 !important;
            background: transparent !important;
            font-size: {font_size} !important;
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
            margin-bottom: 1rem !important;
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
    <div class="page-container">
        {html_body_prev}
    </div>
</body>
</html>
"""

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
