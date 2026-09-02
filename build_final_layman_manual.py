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
            margin: 10mm 12mm 10mm 12mm;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #1E293B;
            line-height: 1.4;
            font-size: 9.5pt;
        }
        
        /* Compact Header & Cover */
        .cover {
            text-align: center;
            padding-top: 15px;
            padding-bottom: 15px;
            border-bottom: 2px solid #0284C7;
            margin-bottom: 12px;
        }
        .cover-logo {
            font-size: 32pt;
            font-weight: 900;
            color: #0284C7;
            letter-spacing: 2px;
            margin-bottom: 0px;
        }
        .cover-subtitle {
            font-size: 15pt;
            font-weight: 400;
            color: #334155;
            margin-top: 2px;
            margin-bottom: 8px;
        }
        .cover-author {
            font-size: 12pt;
            font-weight: 700;
            color: #0369A1;
            background-color: #E0F2FE;
            display: inline-block;
            padding: 5px 18px;
            border-radius: 18px;
            margin-top: 4px;
        }
        .cover-meta {
            margin-top: 8px;
            color: #64748B;
            font-size: 8.5pt;
        }
        
        /* Section Formatting */
        h1.section-header {
            font-size: 12.5pt;
            color: #0F172A;
            background-color: #F1F5F9;
            border-left: 4px solid #0284C7;
            padding: 3px 8px;
            margin-top: 14px;
            margin-bottom: 6px;
            page-break-after: avoid;
        }
        h2 {
            font-size: 10.5pt;
            color: #0369A1;
            margin-top: 10px;
            margin-bottom: 4px;
            page-break-after: avoid;
        }
        h3 {
            font-size: 9.5pt;
            color: #334155;
            margin-top: 8px;
            margin-bottom: 3px;
            page-break-after: avoid;
        }
        p {
            margin-bottom: 5px;
            text-align: justify;
        }
        
        /* Image Preview Box */
        .img-container {
            text-align: center;
            margin: 8px 0;
            page-break-inside: avoid;
        }
        .img-container img {
            max-width: 90%;
            max-height: 240px;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .img-caption {
            font-size: 8pt;
            color: #64748B;
            font-style: italic;
            margin-top: 3px;
        }
        
        /* Tables & Callouts */
        .layman-box {
            background-color: #F0F9FF;
            border-left: 3.5px solid #0284C7;
            padding: 6px 10px;
            margin: 6px 0;
            border-radius: 0 4px 4px 0;
            page-break-inside: avoid;
        }
        .layman-title {
            font-weight: 700;
            color: #0369A1;
            margin-bottom: 2px;
            font-size: 9.5pt;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 6px 0;
            font-size: 8.5pt;
            page-break-inside: avoid;
        }
        th {
            background-color: #0F172A;
            color: #FFFFFF;
            font-weight: 600;
            padding: 4px 6px;
            text-align: left;
        }
        td {
            border-bottom: 1px solid #E2E8F0;
            padding: 4px 6px;
            vertical-align: top;
        }
        tr:nth-child(even) {
            background-color: #F8FAFC;
        }
        
        .kbd {
            background-color: #F1F5F9;
            border: 1px solid #CBD5E1;
            border-radius: 3px;
            padding: 1px 4px;
            font-family: Consolas, monospace;
            font-size: 8pt;
            color: #0F172A;
            font-weight: 600;
        }
        .menu-path {
            color: #0284C7;
            font-weight: 700;
            font-family: Consolas, monospace;
        }
        
        ul, ol {
            margin-top: 2px;
            margin-bottom: 4px;
            padding-left: 16px;
        }
        li {
            margin-bottom: 2px;
        }

        .footer {
            text-align: center;
            font-size: 8pt;
            color: #94A3B8;
            margin-top: 15px;
            border-top: 1px solid #E2E8F0;
            padding-top: 4px;
        }
    </style>
    </head>
    <body>

        <!-- COMPACT COVER HEADER -->
        <div class="cover">
            <div class="cover-logo">ALLME</div>
            <div class="cover-subtitle">Complete Layman's Product User Manual</div>
            <div class="cover-author">Author & Creator: ATK ( Amit Kumar Singh )</div>
            <div class="cover-meta">
                <strong>Platform:</strong> Microsoft Windows (x64) &nbsp;|&nbsp; 
                <strong>Version:</strong> AllmeD_v36 &nbsp;|&nbsp; 
                <strong>Document Ref:</strong> ALLME-UM-V36-ATK
            </div>
        </div>

        <!-- SECTION 1 -->
        <h1 class="section-header">1. Introduction & Overview</h1>
        <p>
            Welcome to <strong>Allme</strong>, created by <strong>ATK ( Amit Kumar Singh )</strong>! Allme is a smart, friendly desktop widget that floats as a smooth circular orb on your Windows desktop. 
            It is designed to sit gently on top of your open applications, providing instant 1-click access to window switching, browser tab control, screenshot capture, high-definition screen video recording, audio spectrum music visualizers, and live computer hardware telemetry.
        </p>

        <div class="layman-box">
            <div class="layman-title">What Allme Does For You (Summary):</div>
            <ul>
                <li><strong>Instant Window Switcher:</strong> Switch active open application windows with a single click.</li>
                <li><strong>Web Browser Tab Control:</strong> Step through browser tabs forward and backward directly from the orb.</li>
                <li><strong>One-Click Screenshots & Screen Recording:</strong> Capture snapshot images or record MP4 screen video clips.</li>
                <li><strong>Audio Spectrum Visualizations:</strong> Watch the orb dance to music played through your speakers.</li>
                <li><strong>Live PC Hardware Monitoring:</strong> View real-time CPU, GPU, RAM, Disk, and Internet traffic metrics.</li>
            </ul>
        </div>

        <!-- SECTION 2 -->
        <h1 class="section-header">2. The Allme Widget Interface & Visual Components</h1>
        <p>
            The Allme widget consists of a 3-zone interactive circular orb surrounded by a customizable ambient glow halo:
        </p>

        <div class="img-container">
            <img src="__IMG_WIDGET__" alt="Allme Desktop Widget Preview">
            <div class="img-caption">Figure 2.1: The Allme Desktop Widget (showing central core, ring sectors, icon preview, and ambient glow halo).</div>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Orb Area</th>
                    <th>Visual Description</th>
                    <th>Core Functionality</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Center Core</strong></td>
                    <td>Small circle in the middle displaying active app/browser icon.</td>
                    <td>Performs Quick Switch (between windows), Tab Switch (in browser), or toggles Screen Video Recording (turns red).</td>
                </tr>
                <tr>
                    <td><strong>Left Sector</strong></td>
                    <td>Outer left arc sector separated by subtle dashed dividers.</td>
                    <td>Cycles windows left, steps browser tabs left, or takes screen capture.</td>
                </tr>
                <tr>
                    <td><strong>Right Sector</strong></td>
                    <td>Outer right arc sector separated by subtle dashed dividers.</td>
                    <td>Cycles windows right, steps browser tabs right, or takes screen capture.</td>
                </tr>
                <tr>
                    <td><strong>Ambient Glow Halo</strong></td>
                    <td>Soft glowing light ring shining around the orb.</td>
                    <td>Pulses with breathing effects, moves with sound volume, or shifts color based on PC hardware load.</td>
                </tr>
            </tbody>
        </table>

        <!-- SECTION 3 -->
        <h1 class="section-header">3. How to Operate Allme (Mouse Clicks & Keyboard Controls)</h1>
        
        <h2>Direct Mouse Button Controls</h2>
        <table>
            <thead>
                <tr>
                    <th>Mouse Button</th>
                    <th>Where You Click</th>
                    <th>Executed Action</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Left Click</strong></td>
                    <td>Center Core</td>
                    <td><strong>Quick Switch:</strong> Jumps instantly back to your previous active window.</td>
                </tr>
                <tr>
                    <td><strong>Left Click</strong></td>
                    <td>Left Sector</td>
                    <td><strong>Previous Window:</strong> Cycles backward through open desktop application windows.</td>
                </tr>
                <tr>
                    <td><strong>Left Click</strong></td>
                    <td>Right Sector</td>
                    <td><strong>Next Window:</strong> Cycles forward through open desktop application windows.</td>
                </tr>
                <tr>
                    <td><strong>Right Click</strong></td>
                    <td>Center Core</td>
                    <td><strong>Switch Browser Tab:</strong> Focuses web browser and switches active tab.</td>
                </tr>
                <tr>
                    <td><strong>Right Click</strong></td>
                    <td>Left Sector</td>
                    <td><strong>Previous Browser Tab:</strong> Steps to the browser tab on the left (Ctrl+PageUp).</td>
                </tr>
                <tr>
                    <td><strong>Right Click</strong></td>
                    <td>Right Sector</td>
                    <td><strong>Next Browser Tab:</strong> Steps to the browser tab on the right (Ctrl+PageDown).</td>
                </tr>
                <tr>
                    <td><strong>Middle Click</strong></td>
                    <td>Center Core</td>
                    <td><strong>Record Screen Video:</strong> Starts or stops MP4 video recording (orb border turns red).</td>
                </tr>
                <tr>
                    <td><strong>Middle Click</strong></td>
                    <td>Left or Right Sector</td>
                    <td><strong>Take Screenshot:</strong> Captures a full-screen snapshot picture (orb flashes white).</td>
                </tr>
            </tbody>
        </table>

        <h2>Keyboard Modifier Combinations</h2>
        <ul>
            <li><span class="kbd">Shift</span> + <strong>Left Click</strong>: Toggle <strong>Lock Position</strong> (locks widget to prevent accidental movement).</li>
            <li><span class="kbd">Ctrl</span> + <strong>Left Click</strong>: Toggle <strong>Fly Mode</strong> (makes the widget follow mouse cursor).</li>
            <li><span class="kbd">Alt</span> + <strong>Left Click</strong>: Safely terminates and <strong>Exits Allme</strong>.</li>
        </ul>

        <h2>Widget Dragging & Positioning</h2>
        <p>
            Left-click and hold anywhere on the widget body to drag it to any screen location. 
            Allme automatically saves your chosen coordinates and restores them when you reboot your PC.
        </p>

        <!-- SECTION 4 -->
        <h1 class="section-header">4. Complete Layman's Menu & Settings Reference</h1>
        <p>
            Right-clicking the System Tray icon or widget opens the <strong>Persistent Settings Menu</strong> created by <strong>ATK ( Amit Kumar Singh )</strong>:
        </p>

        <div class="img-container">
            <img src="__IMG_MENU__" alt="Allme Context Menu Preview">
            <div class="img-caption">Figure 4.1: The Allme Persistent Context Menu (showing toggles, submenus, audio visualizers, telemetry links, and sliders).</div>
        </div>

        <h2>Part A: General Display & Control Toggles</h2>
        <table>
            <thead>
                <tr>
                    <th>Menu Setting Name</th>
                    <th>Layman's Description & Purpose</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="menu-path">Always on Top</span></td>
                    <td>Keeps Allme visible above all open windows so it never gets hidden under application windows.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">Lock Position</span></td>
                    <td>Freezes Allme in its current spot so you cannot accidentally drag or nudge it while clicking.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">Clickthrough (Pass Mouse)</span></td>
                    <td>Makes Allme transparent to mouse clicks, letting clicks pass through to background apps.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">🖱️ Clickthrough Mode</span></td>
                    <td>
                        Submenu options: <em>1. Pass All (Hardware Pass-Through)</em>, <em>2. Pass Left Click Only</em>, <em>3. Pass Right Click Only</em>, <em>4. Pass Middle Click Only</em>.
                    </td>
                </tr>
                <tr>
                    <td><span class="menu-path">Fly Mode (Follow Cursor)</span></td>
                    <td>Makes Allme float and follow your mouse cursor coordinates across the screen.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">🎛️ Futuristic Dashboard</span></td>
                    <td>Opens the full system diagnostic and hardware performance monitoring window.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">Start with Windows</span></td>
                    <td>Configures Allme to start automatically whenever you log into Windows.</td>
                </tr>
            </tbody>
        </table>

        <h2>Part B: Visual Animations, Breathing & Colors</h2>
        <table>
            <thead>
                <tr>
                    <th>Menu Setting Name</th>
                    <th>Layman's Description & Purpose</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="menu-path">Enable Ambient Glow</span></td>
                    <td>Turns the outer glowing light halo around the orb on or off.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">Enable Breathing Animation</span></td>
                    <td>Adds a slow, calm pulsing rhythm to the widget so it feels alive.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">🫁 Breathing Target</span></td>
                    <td>Submenu choices: <em>1. Both (App & Glow)</em>, <em>2. App Only</em>, <em>3. Glow Only</em>.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">Enable Mouse Movement Activity</span></td>
                    <td>Makes the orb and glow expand and brighten dynamically based on mouse movement speed.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">🖱️ Mouse Movement Target</span></td>
                    <td>Submenu choices: <em>1. Both</em>, <em>2. App Only</em>, <em>3. Glow Only</em>.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">🎨 Color Hue Target</span></td>
                    <td>Submenu choices: <em>Both</em>, <em>App Only</em>, <em>Glow Only</em>.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">Link System Accent</span></td>
                    <td>Automatically matches Allme's color theme to your Windows DWM system accent color.</td>
                </tr>
            </tbody>
        </table>

        <h2>Part C: Audio Spectrum Music Visualizers</h2>
        <table>
            <thead>
                <tr>
                    <th>Menu Setting Name</th>
                    <th>Layman's Description & Purpose</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="menu-path">Enable Audio Overlay Visualizations</span></td>
                    <td>Turns on live music visualizer effects so Allme dances when speaker audio plays.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">🎛️ Audio Driver Mode</span></td>
                    <td>Submenu: <em>1. Both (Volume & Frequency)</em>, <em>2. Volume Only</em>, <em>3. Frequency Only</em>.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">🎵 Audio Visualizations (Profiles)</span></td>
                    <td>
                        Select music visualization style:<br>
                        • <strong>Pulsing Aura:</strong> Classic smooth glowing halo pulsing to volume beat.<br>
                        • <strong>Chroma Pulse:</strong> Rainbow spectrum color rotation synchronized with audio peaks.<br>
                        • <strong>Equalizer Ring:</strong> 24 radial spectrum equalizer bars dancing around the orb.<br>
                        • <strong>Waveform Orbit:</strong> Oscillating circular sound wave spinning around the outer edge.<br>
                        • <strong>Frequency Ripple:</strong> Shockwave light rings expanding outward on heavy drum/bass beats.<br>
                        • <strong>Particle Spark:</strong> 12 glowing beat dots orbiting and bouncing to rhythm.
                    </td>
                </tr>
            </tbody>
        </table>

        <h2>Part D: System Data Binding (Link Source & Link Sink)</h2>
        <p>
            Connect live PC hardware metrics (Link Source) to visual attributes of Allme (Link Sink):
        </p>
        <ul>
            <li><strong>Link Source Options (0-9):</strong> None, Breathing Sine, CPU Frequency, CPU Usage, HDD Activity (with drive & IO mode options), Memory Usage, Ethernet & Ping Latency, GPU Usage (GPU 0/1/Max), System Power Usage, Keyboard Typing WPM.</li>
            <li><strong>Link Sink Options (0-9):</strong> Modulates App Size, App Color, Glow Size, Glow Color, App Opacity, Glow Opacity, or combined Size/Color/Opacity attributes.</li>
        </ul>

        <h2>Part E: Customization Sliders</h2>
        <ul>
            <li><strong>App Opacity (0-100%):</strong> Adjusts widget transparency (solid to transparent).</li>
            <li><strong>Glow Opacity (0-100%):</strong> Adjusts outer glow halo brightness.</li>
            <li><strong>Glow Size (0-100%):</strong> Adjusts diameter of the outer glowing halo.</li>
            <li><strong>Color Hue (0°-360°):</strong> Smooth spectrum slider to pick any custom color.</li>
            <li><strong>Breathing Speed (1-100%):</strong> Adjusts breathing animation frequency.</li>
            <li><strong>App Size (0-100%):</strong> Resizes the Allme orb on screen.</li>
        </ul>

        <!-- SECTION 5 -->
        <h1 class="section-header">5. The Futuristic Diagnostic Dashboard</h1>
        <p>
            Selecting <strong>🎛️ Futuristic Dashboard</strong> launches a dedicated diagnostic panel designed by <strong>ATK ( Amit Kumar Singh )</strong>:
        </p>

        <div class="img-container">
            <img src="__IMG_DASH__" alt="Allme Futuristic Dashboard Preview">
            <div class="img-caption">Figure 5.1: The AllMeD Futuristic Control Dashboard (showing Core Modules, Telemetry Links, Visual Targets, and Adjustments).</div>
        </div>

        <ul>
            <li><strong>Core Modules Box:</strong> Toggle ambient glow, audio visualizations, breathing, mouse activity, and Windows auto-startup.</li>
            <li><strong>Telemetry Links Box:</strong> Select live Link Source and Link Sink hardware data bindings.</li>
            <li><strong>Visual Targets Box:</strong> Configure Audio Driver Modes, Audio Visualizer Effects, Breathing Targets, and Mouse Targets.</li>
            <li><strong>Adjustments Box:</strong> Direct slider adjustments for App Size, App Opacity, Glow Size, Glow Opacity, App Hue, and Breath Speed.</li>
        </ul>

        <!-- SECTION 6 -->
        <h1 class="section-header">6. Media Capture & System Paths</h1>
        <table>
            <thead>
                <tr>
                    <th>Item / File Type</th>
                    <th>Default Storage Location on Windows</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Screenshots</strong></td>
                    <td><code>C:/Users/[YourName]/Pictures/Allme/Screenshots/</code></td>
                </tr>
                <tr>
                    <td><strong>Video Recordings</strong></td>
                    <td><code>C:/Users/[YourName]/Pictures/Allme/Recordings/</code></td>
                </tr>
                <tr>
                    <td><strong>Configuration File</strong></td>
                    <td><code>C:/Users/[YourName]/AppData/Roaming/Allme/config.json</code></td>
                </tr>
                <tr>
                    <td><strong>Crash Diagnostic Logs</strong></td>
                    <td><code>C:/Users/[YourName]/AppData/Local/Allme/Logs/allme_crash_report.txt</code></td>
                </tr>
            </tbody>
        </table>

        <div class="footer">
            Allme Product User Manual — Version 36 &nbsp;|&nbsp; Created & Developed by <strong>ATK ( Amit Kumar Singh )</strong> &copy; 2026
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
    print("Final Layman Product User Manual created successfully at AllmeD_v36_Product_User_Manual.pdf")

if __name__ == '__main__':
    generate_manual()
