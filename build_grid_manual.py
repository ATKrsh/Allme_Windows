import sys
import os
import base64
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter

def get_base64_image(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
            return f"data:image/png;base64,{encoded}"
    return ""

def generate_manual():
    img_widget = get_base64_image("widget_preview.png")
    img_menu = get_base64_image("menu_preview.png")
    img_dash = get_base64_image("dashboard_preview.png")

    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        @page {
            size: A4;
            margin: 8mm 8mm 8mm 8mm;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #1E293B;
            line-height: 1.3;
            font-size: 8pt;
        }
        
        /* Two-column layout grid */
        .row {
            width: 100%;
            margin-bottom: 6px;
        }
        .col-6 {
            width: 49%;
            float: left;
        }
        .col-6-right {
            width: 49%;
            float: right;
        }
        .col-12 {
            width: 100%;
            clear: both;
        }
        .clearfix::after {
            content: "";
            clear: both;
            display: table;
        }
        
        /* Header Banner */
        .header-banner {
            background: #0F172A;
            color: #FFFFFF;
            padding: 8px 12px;
            border-radius: 4px;
            margin-bottom: 8px;
        }
        .header-title {
            font-size: 18pt;
            font-weight: 900;
            color: #38BDF8;
            letter-spacing: 1px;
            display: inline-block;
        }
        .header-subtitle {
            font-size: 10pt;
            color: #94A3B8;
            float: right;
            margin-top: 6px;
        }
        
        /* Section Headers */
        h1.section-header {
            font-size: 10pt;
            color: #0F172A;
            background-color: #E2E8F0;
            border-left: 3.5px solid #0284C7;
            padding: 2px 6px;
            margin-top: 6px;
            margin-bottom: 4px;
            page-break-after: avoid;
        }
        h2 {
            font-size: 9pt;
            color: #0369A1;
            margin-top: 5px;
            margin-bottom: 2px;
            page-break-after: avoid;
        }
        p {
            margin-bottom: 3px;
            text-align: justify;
        }
        
        /* Image Preview Boxes */
        .img-card {
            text-align: center;
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-radius: 4px;
            padding: 4px;
            margin-bottom: 4px;
        }
        .img-card img {
            max-width: 98%;
            max-height: 165px;
            border-radius: 3px;
        }
        .img-caption {
            font-size: 7.5pt;
            color: #475569;
            font-weight: 600;
            margin-top: 2px;
        }
        
        /* Callouts */
        .info-box {
            background-color: #F0F9FF;
            border-left: 3px solid #0284C7;
            padding: 4px 6px;
            margin: 4px 0;
            border-radius: 0 3px 3px 0;
        }
        .info-title {
            font-weight: 700;
            color: #0369A1;
            margin-bottom: 1px;
            font-size: 8pt;
        }

        /* Compact Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 3px 0;
            font-size: 7.5pt;
        }
        th {
            background-color: #0F172A;
            color: #FFFFFF;
            font-weight: 600;
            padding: 2px 4px;
            text-align: left;
        }
        td {
            border-bottom: 1px solid #E2E8F0;
            padding: 2px 4px;
            vertical-align: top;
        }
        tr:nth-child(even) {
            background-color: #F8FAFC;
        }
        
        .kbd {
            background-color: #F1F5F9;
            border: 1px solid #CBD5E1;
            border-radius: 2px;
            padding: 0px 2px;
            font-family: Consolas, monospace;
            font-size: 7pt;
            color: #0F172A;
            font-weight: 600;
        }
        .menu-path {
            color: #0284C7;
            font-weight: 700;
            font-family: Consolas, monospace;
        }
        
        ul, ol {
            margin-top: 1px;
            margin-bottom: 2px;
            padding-left: 12px;
        }
        li {
            margin-bottom: 1px;
        }

        .footer {
            text-align: center;
            font-size: 7.5pt;
            color: #64748B;
            margin-top: 8px;
            border-top: 1px solid #CBD5E1;
            padding-top: 3px;
            clear: both;
        }
    </style>
    </head>
    <body>

        <!-- COMPACT HEADER BANNER -->
        <div class="header-banner clearfix">
            <span class="header-title">ALLME</span>
            <span class="header-subtitle">Product User Manual &nbsp;|&nbsp; Version 36 (Windows x64)</span>
        </div>

        <!-- ROW 1: INTRODUCTION & WIDGET INTERFACE -->
        <div class="row clearfix">
            <div class="col-6">
                <h1 class="section-header">1. Introduction & Overview</h1>
                <p>
                    <strong>Allme</strong> is a smart desktop assistant widget that floats as a smooth circular orb on your Windows screen. 
                    Positioned on top of your applications, it provides instant 1-click access to window switching, browser tab navigation, screenshot capture, MP4 screen video recording, audio spectrum music visualizers, and live computer hardware telemetry.
                </p>
                <div class="info-box">
                    <div class="info-title">Core Features Summary:</div>
                    <ul>
                        <li><strong>Instant Window Switcher:</strong> Hop between open apps with 1 click.</li>
                        <li><strong>Browser Tab Controls:</strong> Step browser tabs forward and backward.</li>
                        <li><strong>Media Capture:</strong> Take screenshots and record screen video.</li>
                        <li><strong>Audio Spectrum Visualizers:</strong> Orb dances to speaker sound.</li>
                    </ul>
                </div>
            </div>
            <div class="col-6-right">
                <div class="img-card">
                    <img src="__IMG_WIDGET__" alt="Allme Desktop Widget">
                    <div class="img-caption">Figure 1: Allme Circular Desktop Widget & Interaction Ring</div>
                </div>
            </div>
        </div>

        <!-- ROW 2: CONTROLS & SHORTCUTS -->
        <div class="row clearfix">
            <div class="col-6">
                <h1 class="section-header">2. Direct Mouse Button Controls</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Button</th>
                            <th>Target Zone</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Left Click</strong></td>
                            <td>Center Core</td>
                            <td><strong>Quick Switch:</strong> Focus previous active window.</td>
                        </tr>
                        <tr>
                            <td><strong>Left Click</strong></td>
                            <td>Left Sector</td>
                            <td><strong>Previous Window:</strong> Cycle backward open apps.</td>
                        </tr>
                        <tr>
                            <td><strong>Left Click</strong></td>
                            <td>Right Sector</td>
                            <td><strong>Next Window:</strong> Cycle forward open apps.</td>
                        </tr>
                        <tr>
                            <td><strong>Right Click</strong></td>
                            <td>Center Core</td>
                            <td><strong>Switch Browser Tab:</strong> Focus browser & switch tab.</td>
                        </tr>
                        <tr>
                            <td><strong>Right Click</strong></td>
                            <td>Left Sector</td>
                            <td><strong>Previous Tab:</strong> Step browser tab left (Ctrl+PgUp).</td>
                        </tr>
                        <tr>
                            <td><strong>Right Click</strong></td>
                            <td>Right Sector</td>
                            <td><strong>Next Tab:</strong> Step browser tab right (Ctrl+PgDn).</td>
                        </tr>
                        <tr>
                            <td><strong>Middle Click</strong></td>
                            <td>Center Core</td>
                            <td><strong>Record Screen Video:</strong> Start/Stop MP4 (red border).</td>
                        </tr>
                        <tr>
                            <td><strong>Middle Click</strong></td>
                            <td>Outer Ring</td>
                            <td><strong>Take Screenshot:</strong> Capture screen image (white flash).</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="col-6-right">
                <h1 class="section-header">3. Keyboard Modifiers & Positioning</h1>
                <ul>
                    <li><span class="kbd">Shift</span> + <strong>Left Click</strong>: Toggle <strong>Lock Position</strong> (locks widget dragging).</li>
                    <li><span class="kbd">Ctrl</span> + <strong>Left Click</strong>: Toggle <strong>Fly Mode</strong> (widget follows cursor).</li>
                    <li><span class="kbd">Alt</span> + <strong>Left Click</strong>: Safely terminate and <strong>Exit Allme</strong>.</li>
                </ul>
                <div class="info-box">
                    <div class="info-title">Positioning & Dragging:</div>
                    Left-click and hold anywhere on the orb body to drag it across your screen. Coordinates are saved automatically and restored upon PC reboot.
                </div>
            </div>
        </div>

        <!-- ROW 3: SETTINGS MENU & GENERAL TOGGLES -->
        <div class="row clearfix">
            <div class="col-6">
                <div class="img-card">
                    <img src="__IMG_MENU__" alt="Allme Context Menu">
                    <div class="img-caption">Figure 2: Allme Persistent Settings Menu</div>
                </div>
            </div>
            <div class="col-6-right">
                <h1 class="section-header">4. Settings Menu Breakdown</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Setting Name</th>
                            <th>Description & Function</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><span class="menu-path">Always on Top</span></td>
                            <td>Keeps widget visible above all application windows.</td>
                        </tr>
                        <tr>
                            <td><span class="menu-path">Lock Position</span></td>
                            <td>Freezes widget position to prevent accidental dragging.</td>
                        </tr>
                        <tr>
                            <td><span class="menu-path">Clickthrough</span></td>
                            <td>Makes mouse clicks pass through widget to background apps.</td>
                        </tr>
                        <tr>
                            <td><span class="menu-path">Clickthrough Mode</span></td>
                            <td>Submenu: Pass All, Pass Left, Pass Right, Pass Middle.</td>
                        </tr>
                        <tr>
                            <td><span class="menu-path">Fly Mode</span></td>
                            <td>Makes widget track mouse cursor coordinates smoothly.</td>
                        </tr>
                        <tr>
                            <td><span class="menu-path">Start with Windows</span></td>
                            <td>Launches Allme automatically on Windows user login.</td>
                        </tr>
                        <tr>
                            <td><span class="menu-path">Enable Ambient Glow</span></td>
                            <td>Toggles outer glowing halo around the orb on/off.</td>
                        </tr>
                        <tr>
                            <td><span class="menu-path">Breathing Animation</span></td>
                            <td>Adds calm breathing pulse (Target: Both, App, Glow).</td>
                        </tr>
                        <tr>
                            <td><span class="menu-path">Mouse Activity</span></td>
                            <td>Expands glow/orb dynamically on fast mouse movement.</td>
                        </tr>
                        <tr>
                            <td><span class="menu-path">Link System Accent</span></td>
                            <td>Syncs widget color with Windows DWM system accent color.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- ROW 4: AUDIO VISUALIZERS & DATA LINKING -->
        <div class="row clearfix">
            <div class="col-6">
                <h1 class="section-header">5. Audio Spectrum Music Visualizers</h1>
                <p><strong>Audio Driver Modes:</strong> Both (Volume & Frequency), Volume Only, Frequency Only.</p>
                <table>
                    <thead>
                        <tr>
                            <th>Profile Name</th>
                            <th>Visual Render Behavior</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Pulsing Aura</strong></td>
                            <td>Classic radial glow pulsing to audio volume beat.</td>
                        </tr>
                        <tr>
                            <td><strong>Chroma Pulse</strong></td>
                            <td>Rainbow spectrum color rotation on sound peaks.</td>
                        </tr>
                        <tr>
                            <td><strong>Equalizer Ring</strong></td>
                            <td>24 spectrum equalizer bars orbiting widget ring.</td>
                        </tr>
                        <tr>
                            <td><strong>Waveform Orbit</strong></td>
                            <td>Oscillating circular sound wave around border.</td>
                        </tr>
                        <tr>
                            <td><strong>Frequency Ripple</strong></td>
                            <td>Concentric shockwave rings expanding on bass beats.</td>
                        </tr>
                        <tr>
                            <td><strong>Particle Spark</strong></td>
                            <td>12 glowing beat dots orbiting and jumping to rhythm.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="col-6-right">
                <h1 class="section-header">6. System Telemetry Links & Sliders</h1>
                <p><strong>Link Source (0-9):</strong> None, Breathing Sine, CPU Freq, CPU Usage, HDD Activity, Memory Usage, Ethernet & Ping Latency, GPU Usage, Power Usage, Typing WPM.</p>
                <p><strong>Link Sink (0-9):</strong> Modulates App Size, App Color, Glow Size, Glow Color, App Opacity, Glow Opacity, or Combined Attributes.</p>
                <div class="info-box">
                    <div class="info-title">Customization Sliders:</div>
                    App Opacity (0-100%), Glow Opacity (0-100%), Glow Size (0-100%), Color Hue (0°-360° wheel), Breathing Speed (1-100%), App Size (0-100%).
                </div>
            </div>
        </div>

        <!-- ROW 5: DASHBOARD & FILE PATHS -->
        <div class="row clearfix">
            <div class="col-6">
                <div class="img-card">
                    <img src="__IMG_DASH__" alt="Futuristic Dashboard">
                    <div class="img-caption">Figure 3: Allme Futuristic Control Dashboard</div>
                </div>
            </div>
            <div class="col-6-right">
                <h1 class="section-header">7. Diagnostic Dashboard & Storage Paths</h1>
                <p>Launches via <strong>🎛️ Futuristic Dashboard</strong> menu item. Contains Core Modules, Telemetry Links, Visual Targets, and Adjustment sliders.</p>
                <table>
                    <thead>
                        <tr>
                            <th>Item Type</th>
                            <th>Default Storage Location on Windows</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Screenshots</strong></td>
                            <td><code>C:/Users/[User]/Pictures/Allme/Screenshots/</code></td>
                        </tr>
                        <tr>
                            <td><strong>Recordings</strong></td>
                            <td><code>C:/Users/[User]/Pictures/Allme/Recordings/</code></td>
                        </tr>
                        <tr>
                            <td><strong>Settings JSON</strong></td>
                            <td><code>C:/Users/[User]/AppData/Roaming/Allme/config.json</code></td>
                        </tr>
                        <tr>
                            <td><strong>Crash Logs</strong></td>
                            <td><code>C:/Users/[User]/AppData/Local/Allme/Logs/allme_crash_report.txt</code></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- REQUIRED FOOTER -->
        <div class="footer">
            Allme Product User Manual — Version 36 | Created & Developed by ATK ( Amit Kumar Singh ) © 2026
        </div>

    </body>
    </html>
    """

    html = html.replace("__IMG_WIDGET__", img_widget)
    html = html.replace("__IMG_MENU__", img_menu)
    html = html.replace("__IMG_DASH__", img_dash)

    app = QApplication(sys.argv)
    doc = QTextDocument()
    doc.setHtml(html)
    
    printer = QPrinter()
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName('AllmeD_v36_Product_User_Manual.pdf')
    printer.setResolution(300)
    
    doc.print_(printer)
    print("Grid-Aligned Balanced Product User Manual created successfully at AllmeD_v36_Product_User_Manual.pdf")

if __name__ == '__main__':
    generate_manual()
