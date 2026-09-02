import ast
import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter

def generate_manual():
    with open('allme.py', 'r', encoding='utf-8') as f:
        code = f.read()

    tree = ast.parse(code)
    
    # Extract imports
    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.append(f"{node.module} ({', '.join([a.name for a in node.names])})")
            
    # Extract functions and classes
    classes = []
    functions = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            doc = ast.get_docstring(node) or "No description available."
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            classes.append({'name': node.name, 'doc': doc, 'methods': methods})
        elif isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node) or "No description available."
            functions.append({'name': node.name, 'doc': doc})

    html = f"""
    <html>
    <head>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; line-height: 1.6; margin: 40px; }}
        h1 {{ color: #2C3E50; text-align: center; border-bottom: 2px solid #3498DB; padding-bottom: 10px; }}
        h2 {{ color: #2980B9; margin-top: 30px; border-bottom: 1px solid #BDC3C7; padding-bottom: 5px; }}
        h3 {{ color: #16A085; }}
        p {{ text-align: justify; }}
        .header {{ text-align: center; margin-bottom: 50px; }}
        .lib-list {{ columns: 2; -webkit-columns: 2; -moz-columns: 2; list-style-type: square; }}
        .method-list {{ margin-left: 20px; font-size: 0.9em; color: #555; }}
        .code {{ font-family: monospace; background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
        .footer {{ text-align: center; font-size: 0.8em; color: #7F8C8D; margin-top: 50px; border-top: 1px solid #E0E0E0; padding-top: 10px; }}
    </style>
    </head>
    <body>
        <div class="header">
            <h1>AllmeD_v36 (Allme_Windows)</h1>
            <h2>Comprehensive Technical Manual</h2>
            <p><strong>Master Desktop Widget combining ASwitch + captureME + Telemetry Suite</strong></p>
            <p>Always-on-top, translucent circular widget with window/tab switching, screen capture, video recording & system telemetry.</p>
        </div>
        
        <h2>1. Introduction & Uses</h2>
        <p>
            Allme is designed to be an omnipresent, always-on-top desktop widget. It consolidates essential system utilities into a minimal, translucent circular interface. 
            The primary uses include rapid window and tab switching, capturing screenshots, recording the screen with audio, and monitoring system telemetry (CPU, GPU, RAM, Network).
            By running in the background and overlaying the desktop, it provides instant access to these tools without disrupting the user's workflow.
        </p>

        <h2>2. Libraries Used</h2>
        <ul class="lib-list">
    """
    for imp in sorted(set(imports)):
        html += f"<li>{imp}</li>"
        
    html += """
        </ul>

        <h2>3. Classes and Components</h2>
    """
    for cls in classes:
        html += f"<h3>Class: <span class='code'>{cls['name']}</span></h3>"
        html += f"<p>{cls['doc'].replace(chr(10), '<br>')}</p>"
        if cls['methods']:
            html += "<p><strong>Key Methods:</strong></p><ul class='method-list'>"
            for m in cls['methods']:
                html += f"<li>{m}</li>"
            html += "</ul>"
            
    html += """
        <h2>4. Core Functions</h2>
    """
    for func in functions:
        html += f"<h3>Function: <span class='code'>{func['name']}</span></h3>"
        html += f"<p>{func['doc'].replace(chr(10), '<br>')}</p>"

    html += """
        <h2>5. Context Menu & Interaction</h2>
        <p>
            The widget interacts primarily via mouse events. A right-click on the main widget typically invokes a comprehensive context menu (QMenu) providing access to:
        </p>
        <ul>
            <li><strong>Dashboard & Telemetry:</strong> View detailed system metrics.</li>
            <li><strong>Capture & Record:</strong> Tools for taking screenshots and starting/stopping screen recordings.</li>
            <li><strong>Settings:</strong> Configuration options such as startup behavior and visual preferences.</li>
            <li><strong>Exit:</strong> Safely terminate the application and its background processes.</li>
        </ul>
        
        <div class="footer">
            Generated Automatically | Allme_Windows Technical Documentation
        </div>
    </body>
    </html>
    """

    app = QApplication(sys.argv)
    doc = QTextDocument()
    doc.setHtml(html)
    
    printer = QPrinter()
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName('AllmeD_v36_Manual.pdf')
    printer.setResolution(300)
    
    doc.print_(printer)
    print("PDF Manual created successfully at AllmeD_v36_Manual.pdf")

if __name__ == '__main__':
    generate_manual()
