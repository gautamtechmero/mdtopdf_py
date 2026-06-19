from pygments.formatters import HtmlFormatter

def get_syntax_highlighting_css(theme_name):
    """Generate Pygments CSS for code blocks based on the theme."""
    style_name = 'default'
    if 'dark' in theme_name.lower():
        style_name = 'monokai'
    elif 'github' in theme_name.lower():
        style_name = 'friendly'
    elif 'academic' in theme_name.lower():
        style_name = 'autumn'
    elif 'modern' in theme_name.lower():
        style_name = 'colorful'
    
    formatter = HtmlFormatter(style=style_name)
    # The markdown library wraps code blocks inside a div with class 'codehilite'
    return formatter.get_style_defs('.codehilite')

# Base typography and structure styles for various themes
THEME_BASES = {
    "GitHub Light": """
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
            font-size: 16px;
            line-height: 1.6;
            color: #24292f;
            background-color: #ffffff;
            margin: 0;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
            color: #1f2328;
        }
        h1 { font-size: 2em; padding-bottom: 0.3em; border-bottom: 1px solid #d0d7de; }
        h2 { font-size: 1.5em; padding-bottom: 0.3em; border-bottom: 1px solid #d0d7de; }
        h3 { font-size: 1.25em; }
        h4 { font-size: 1em; }
        a { color: #0969da; text-decoration: none; }
        a:hover { text-decoration: underline; }
        p { margin-top: 0; margin-bottom: 16px; }
        blockquote {
            padding: 0 1em;
            color: #656d76;
            border-left: 0.25em solid #d0d7de;
            margin: 0 0 16px 0;
        }
        code {
            padding: .2em .4em;
            margin: 0;
            font-size: 85%;
            white-space: break-spaces;
            background-color: rgba(175, 184, 193, 0.2);
            border-radius: 6px;
            font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
        }
        pre {
            padding: 16px;
            overflow: auto;
            font-size: 85%;
            line-height: 1.45;
            background-color: #f6f8fa;
            border-radius: 6px;
            margin-bottom: 16px;
        }
        pre code {
            padding: 0;
            background-color: transparent;
            font-size: 100%;
            border-radius: 0;
        }
        table {
            border-spacing: 0;
            border-collapse: collapse;
            margin-top: 0;
            margin-bottom: 16px;
            width: 100%;
        }
        table th {
            font-weight: 600;
            background-color: #f6f8fa;
        }
        table th, table td {
            padding: 6px 13px;
            border: 1px solid #d0d7de;
        }
        table tr:nth-child(even) {
            background-color: #f6f8fa;
        }
        hr {
            height: .25em;
            padding: 0;
            margin: 24px 0;
            background-color: #d0d7de;
            border: 0;
        }
        ul, ol {
            margin-top: 0;
            margin-bottom: 16px;
            padding-left: 2em;
        }
        img {
            max-width: 100%;
            box-sizing: content-box;
            background-color: #ffffff;
        }
    """,
    "GitHub Dark": """
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
            font-size: 16px;
            line-height: 1.6;
            color: #c9d1d9;
            background-color: #0d1117;
            margin: 0;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
            color: #f0f6fc;
        }
        h1 { font-size: 2em; padding-bottom: 0.3em; border-bottom: 1px solid #21262d; }
        h2 { font-size: 1.5em; padding-bottom: 0.3em; border-bottom: 1px solid #21262d; }
        h3 { font-size: 1.25em; }
        h4 { font-size: 1em; }
        a { color: #58a6ff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        p { margin-top: 0; margin-bottom: 16px; }
        blockquote {
            padding: 0 1em;
            color: #8b949e;
            border-left: 0.25em solid #30363d;
            margin: 0 0 16px 0;
        }
        code {
            padding: .2em .4em;
            margin: 0;
            font-size: 85%;
            white-space: break-spaces;
            background-color: rgba(110, 118, 129, 0.4);
            border-radius: 6px;
            font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
        }
        pre {
            padding: 16px;
            overflow: auto;
            font-size: 85%;
            line-height: 1.45;
            background-color: #161b22;
            border-radius: 6px;
            margin-bottom: 16px;
            border: 1px solid #21262d;
        }
        pre code {
            padding: 0;
            background-color: transparent;
            font-size: 100%;
            border-radius: 0;
        }
        table {
            border-spacing: 0;
            border-collapse: collapse;
            margin-top: 0;
            margin-bottom: 16px;
            width: 100%;
        }
        table th {
            font-weight: 600;
            background-color: #161b22;
        }
        table th, table td {
            padding: 6px 13px;
            border: 1px solid #30363d;
        }
        table tr:nth-child(even) {
            background-color: #161b22;
        }
        hr {
            height: .25em;
            padding: 0;
            margin: 24px 0;
            background-color: #30363d;
            border: 0;
        }
        ul, ol {
            margin-top: 0;
            margin-bottom: 16px;
            padding-left: 2em;
        }
        img {
            max-width: 100%;
            box-sizing: content-box;
            background-color: #0d1117;
        }
    """,
    "Academic / Formal": """
        body {
            font-family: "Georgia", "Times New Roman", Times, serif;
            font-size: 15px;
            line-height: 1.8;
            color: #111111;
            background-color: #fdfdfd;
            margin: 0;
            padding: 40px;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: "Garamond", "Georgia", serif;
            margin-top: 30px;
            margin-bottom: 15px;
            font-weight: normal;
            color: #000000;
            text-align: left;
        }
        h1 { font-size: 2.2em; border-bottom: 1px double #555555; padding-bottom: 5px; }
        h2 { font-size: 1.6em; border-bottom: 1px solid #cccccc; padding-bottom: 3px; }
        h3 { font-size: 1.3em; font-style: italic; }
        h4 { font-size: 1.1em; }
        p { margin-top: 0; margin-bottom: 20px; text-align: justify; }
        blockquote {
            padding: 5px 20px;
            color: #555555;
            border-left: 3px solid #666666;
            margin: 0 0 20px 20px;
            font-style: italic;
        }
        code {
            padding: 1px 3px;
            font-size: 90%;
            background-color: #f4f4f4;
            border: 1px solid #e0e0e0;
            font-family: "Courier New", Courier, monospace;
        }
        pre {
            padding: 15px;
            background-color: #fcfcfc;
            border: 1px solid #e0e0e0;
            margin-bottom: 20px;
            overflow: auto;
        }
        pre code {
            border: none;
            padding: 0;
            background-color: transparent;
        }
        table {
            border-collapse: collapse;
            margin-top: 20px;
            margin-bottom: 20px;
            width: 100%;
        }
        table th {
            font-weight: bold;
            border-bottom: 2px solid #111111;
            border-top: 2px solid #111111;
            padding: 8px;
            background-color: transparent;
        }
        table td {
            padding: 8px;
            border-bottom: 1px solid #dddddd;
        }
        hr {
            height: 1px;
            margin: 30px 0;
            background-color: #666666;
            border: 0;
        }
        ul, ol {
            margin-top: 0;
            margin-bottom: 20px;
            padding-left: 2.5em;
        }
    """,
    "Sleek Modern": """
        body {
            font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-size: 15px;
            line-height: 1.625;
            color: #334155;
            background-color: #f8fafc;
            margin: 0;
            padding: 30px;
        }
        h1, h2, h3, h4, h5, h6 {
            margin-top: 28px;
            margin-bottom: 14px;
            font-weight: 700;
            color: #0f172a;
            letter-spacing: -0.025em;
        }
        h1 { font-size: 2.25em; color: #0e7490; margin-bottom: 20px; }
        h2 { font-size: 1.5em; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; }
        h3 { font-size: 1.25em; }
        a { color: #06b6d4; text-decoration: none; font-weight: 500; }
        a:hover { color: #0891b2; text-decoration: underline; }
        p { margin-top: 0; margin-bottom: 18px; }
        blockquote {
            padding: 8px 16px;
            color: #475569;
            background-color: #ecfeff;
            border-left: 4px solid #06b6d4;
            border-radius: 4px;
            margin: 0 0 18px 0;
        }
        code {
            padding: 2px 6px;
            font-size: 85%;
            background-color: #f1f5f9;
            color: #0f172a;
            border-radius: 4px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        }
        pre {
            padding: 16px;
            background-color: #0f172a;
            color: #f8fafc;
            border-radius: 8px;
            margin-bottom: 18px;
            overflow: auto;
        }
        pre code {
            background-color: transparent;
            color: inherit;
            padding: 0;
            border-radius: 0;
        }
        table {
            border-collapse: separate;
            border-spacing: 0;
            margin-top: 18px;
            margin-bottom: 18px;
            width: 100%;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
        }
        table th {
            font-weight: 600;
            background-color: #f1f5f9;
            color: #0f172a;
            padding: 10px 12px;
            text-align: left;
        }
        table td {
            padding: 10px 12px;
            border-top: 1px solid #e2e8f0;
            background-color: #ffffff;
        }
        table tr:nth-child(even) td {
            background-color: #f8fafc;
        }
        hr {
            height: 2px;
            margin: 28px 0;
            background-color: #e2e8f0;
            border: 0;
        }
        ul, ol {
            margin-top: 0;
            margin-bottom: 18px;
            padding-left: 2em;
        }
    """,
    "Minimalist": """
        body {
            font-family: -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
            font-size: 15px;
            line-height: 1.5;
            color: #111111;
            background-color: #ffffff;
            margin: 0;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            margin-top: 24px;
            margin-bottom: 12px;
            font-weight: 500;
            color: #111111;
        }
        h1 { font-size: 1.8em; margin-bottom: 16px; }
        h2 { font-size: 1.4em; }
        h3 { font-size: 1.2em; }
        a { color: #111111; text-decoration: underline; }
        p { margin-top: 0; margin-bottom: 12px; }
        blockquote {
            padding-left: 15px;
            color: #555555;
            border-left: 1px solid #111111;
            margin: 0 0 12px 0;
        }
        code {
            padding: 1px 3px;
            font-size: 90%;
            background-color: #f7f7f7;
            font-family: monospace;
        }
        pre {
            padding: 12px;
            background-color: #f7f7f7;
            margin-bottom: 12px;
            overflow: auto;
            border: 1px solid #eeeeee;
        }
        pre code {
            padding: 0;
            background-color: transparent;
        }
        table {
            border-collapse: collapse;
            margin-top: 12px;
            margin-bottom: 12px;
            width: 100%;
        }
        table th, table td {
            padding: 6px;
            border-bottom: 1px solid #111111;
            text-align: left;
        }
        hr {
            height: 1px;
            margin: 24px 0;
            background-color: #111111;
            border: 0;
        }
        ul, ol {
            margin-top: 0;
            margin-bottom: 12px;
            padding-left: 2em;
        }
    """
}

def get_theme_css(theme_name, pdf_mode=False, page_size='A4', orientation='portrait', margins='normal'):
    """Generate final CSS styling for the document, including layout parameters for PDF or Web preview."""
    base_css = THEME_BASES.get(theme_name, THEME_BASES["GitHub Light"])
    syntax_css = get_syntax_highlighting_css(theme_name)
    
    # PDF Layout parameters
    pdf_layout_css = ""
    if pdf_mode:
        # Margin definitions (using numbers for clean calculations)
        margin_vals = {
            "narrow": 1.0,
            "normal": 2.0,
            "wide": 3.0
        }
        margin_num = margin_vals.get(margins, 2.0)
        margin_val = f"{margin_num}cm"
        margin_bottom_val = f"{margin_num + 0.5}cm"
        footer_bottom_val = f"{margin_num / 2.0}cm"
        
        # Orientation modifier
        size_str = page_size
        if orientation == 'landscape':
            size_str = f"{page_size} landscape"
            
        pdf_layout_css = f"""
        @page {{
            size: {size_str};
            margin: {margin_val};
            margin-bottom: {margin_bottom_val};
            @frame footer {{
                -pdf-frame-content: footer_content;
                bottom: {footer_bottom_val};
                margin-left: {margin_val};
                margin-right: {margin_val};
                height: 1.0cm;
            }}
        }}
        
        /* Ensure page-breaks are respected */
        .page-break {{
            page-break-before: always;
        }}
        
        /* Prevent headings from being orphaned at bottom of page */
        h1, h2, h3, h4, h5, h6 {{
            keep-with-next: true;
        }}
        
        /* Avoid breaks inside critical elements */
        pre, blockquote, table, tr {{
            page-break-inside: avoid;
        }}
        
        #footer_content {{
            text-align: right;
            font-size: 8pt;
            color: #555555;
            font-family: sans-serif;
        }}
        """
        
    return f"{base_css}\n\n/* Syntax Highlighting Styles */\n{syntax_css}\n\n/* PDF Specific Page Settings */\n{pdf_layout_css}"
