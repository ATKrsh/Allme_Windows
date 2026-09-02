import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter

def generate_user_manual():
    html = """
    <html>
    <head>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #2b2b2b; line-height: 1.6; margin: 40px; }
        .cover { text-align: center; margin-top: 150px; page-break-after: always; }
        .cover h1 { font-size: 3em; color: #2C3E50; margin-bottom: 10px; }
        .cover h2 { font-size: 1.5em; color: #34495E; font-weight: 300; }
        .cover p { font-size: 1.2em; color: #7F8C8D; margin-top: 50px; }
        
        h1.section-title { color: #2980B9; border-bottom: 2px solid #3498DB; padding-bottom: 5px; margin-top: 40px; }
        h2 { color: #16A085; margin-top: 25px; }
        h3 { color: #27AE60; }
        p { text-align: justify; font-size: 11pt; }
        ul, ol { font-size: 11pt; }
        li { margin-bottom: 8px; }
        .feature-box { background-color: #F8F9F9; border-left: 4px solid #3498DB; padding: 10px 20px; margin: 20px 0; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #BDC3C7; padding: 8px; text-align: left; font-size: 10.5pt; }
        th { background-color: #ECF0F1; color: #2C3E50; }
        
        .footer { text-align: center; font-size: 0.8em; color: #95A5A6; margin-top: 60px; border-top: 1px solid #E0E0E0; padding-top: 10px; }
        .page-break { page-break-before: always; }
    </style>
    </head>
    <body>
        <!-- Cover Page -->
        <div class="cover">
            <h1>AllmeD_v36</h1>
            <h2>Product User Manual</h2>
            <p>Your Master Desktop Widget for Productivity and Monitoring</p>
            <br><br><br>
            <p><em>Version 36 | Windows Edition</em></p>
        </div>
        
        <!-- Table of Contents -->
        <h1 class="section-title">Table of Contents</h1>
        <ol>
            <li>Introduction</li>
            <li>Getting Started</li>
            <li>The Widget Interface</li>
            <li>ASwitch: Window and Tab Management</li>
            <li>captureME: Screen & Video Capture</li>
            <li>Telemetry Suite: System Monitoring</li>
            <li>Settings & Preferences</li>
            <li>Troubleshooting</li>
        </ol>

        <!-- Content -->
        <h1 class="section-title">1. Introduction</h1>
        <p>
            Welcome to <strong>AllmeD_v36</strong>! Allme is a master desktop widget designed to streamline your daily computer interactions. 
            By combining multiple utility applications into one unified, non-intrusive interface, Allme enhances productivity and keeps you informed about your system's health.
        </p>
        <div class="feature-box">
            <strong>Key Features:</strong>
            <ul>
                <li><strong>Always-on-top Widget:</strong> A translucent, circular overlay giving instant access to all tools.</li>
                <li><strong>ASwitch:</strong> Lightning-fast window and tab switching.</li>
                <li><strong>captureME:</strong> Integrated screenshot and video recording capabilities.</li>
                <li><strong>Telemetry Suite:</strong> Real-time monitoring of CPU, GPU, RAM, and Network usage.</li>
            </ul>
        </div>

        <h1 class="section-title">2. Getting Started</h1>
        <h2>Installation & Launch</h2>
        <p>
            Running Allme is as simple as executing the <code>AllmeD_v36.exe</code> application. No complicated setup is required. 
            Once launched, the Allme widget will appear on your desktop. It is designed to be translucent and always-on-top, meaning it won't be easily hidden behind other windows.
        </p>
        <p><em>Note: Only one instance of Allme can run at a time. If you launch it again, it will gracefully close the older instance.</em></p>

        <h1 class="section-title">3. The Widget Interface</h1>
        <p>
            The core interaction with Allme happens through the main Widget.
        </p>
        <ul>
            <li><strong>Left Click:</strong> Depending on your settings, clicking the widget can toggle the full Telemetry Dashboard or bring up the quick action wheel.</li>
            <li><strong>Right Click:</strong> Opens the comprehensive Context Menu, giving you access to all sub-tools, settings, and the exit button.</li>
            <li><strong>Drag and Drop:</strong> Click and hold to drag the widget to any location on your screen. It will remember its position.</li>
        </ul>

        <h1 class="section-title">4. ASwitch: Window and Tab Management</h1>
        <p>
            ASwitch is built into Allme to help you navigate between numerous open windows and tabs effortlessly.
        </p>
        <ul>
            <li>Access ASwitch via the right-click context menu.</li>
            <li>Provides a list or visual grid of your currently active windows.</li>
            <li>Select a window to instantly bring it to the foreground.</li>
        </ul>

        <div class="page-break"></div>

        <h1 class="section-title">5. captureME: Screen & Video Capture</h1>
        <p>
            Need to quickly grab a screenshot or record your desktop? <strong>captureME</strong> is built right in.
        </p>
        <table>
            <tr>
                <th>Feature</th>
                <th>Description</th>
            </tr>
            <tr>
                <td>Screenshot Capture</td>
                <td>Takes a high-quality capture of your entire screen or a selected region. Saved directly to your designated media folder.</td>
            </tr>
            <tr>
                <td>Video Recording</td>
                <td>Start and stop screen recordings with audio. A red indicator on the widget lets you know when recording is active.</td>
            </tr>
            <tr>
                <td>Quick Shortcuts</td>
                <td>Use predefined keyboard shortcuts (configurable in settings) to instantly capture without navigating menus.</td>
            </tr>
        </table>

        <h1 class="section-title">6. Telemetry Suite: System Monitoring</h1>
        <p>
            For power users and gamers, keeping an eye on system resources is crucial. The Telemetry Dashboard provides real-time, aesthetically pleasing graphs and readouts for:
        </p>
        <ul>
            <li><strong>CPU:</strong> Overall usage percentage, per-core loads, and temperatures (if supported).</li>
            <li><strong>GPU:</strong> Graphics processing load, VRAM usage, and temperatures.</li>
            <li><strong>RAM:</strong> Current memory utilization and available free space.</li>
            <li><strong>Network:</strong> Live upload and download speeds.</li>
        </ul>
        <p><em>Tip: You can set the dashboard to appear on a secondary monitor for uninterrupted monitoring.</em></p>

        <h1 class="section-title">7. Settings & Preferences</h1>
        <p>
            Allme is highly customizable. Right-click the widget and select <strong>Settings</strong> to customize:
        </p>
        <ul>
            <li><strong>Appearance:</strong> Adjust the translucency, size, and accent color of the widget to match your Windows theme.</li>
            <li><strong>Startup:</strong> Choose whether Allme should start automatically when you log into Windows.</li>
            <li><strong>Hotkeys:</strong> Rebind shortcuts for captureME and ASwitch.</li>
            <li><strong>Media Directory:</strong> Change where your screenshots and recordings are saved.</li>
        </ul>

        <h1 class="section-title">8. Troubleshooting</h1>
        <div class="feature-box">
            <strong>Widget is missing?</strong><br>
            If the widget is accidentally moved off-screen, simply restart the application. It will reset its position if it detects it is out of bounds.
        </div>
        <div class="feature-box">
            <strong>Crash Logs</strong><br>
            If Allme encounters an unexpected error, it generates a detailed crash report located in <code>%LocalAppData%\Allme\Logs\allme_crash_report.txt</code>. 
            This file contains both layman explanations and technical details for support.
        </div>

        <div class="footer">
            Copyright &copy; 2026 | Allme Productivity Solutions | Document automatically generated.
        </div>
    </body>
    </html>
    """

    app = QApplication(sys.argv)
    doc = QTextDocument()
    doc.setHtml(html)
    
    printer = QPrinter()
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName('AllmeD_v36_Product_User_Manual.pdf')
    printer.setResolution(300)
    
    doc.print_(printer)
    print("PDF User Manual created successfully at AllmeD_v36_Product_User_Manual.pdf")

if __name__ == '__main__':
    generate_user_manual()
