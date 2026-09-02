import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter

def generate_manual():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        @page {
            size: A4;
            margin: 20mm;
        }
        body {
            font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
            color: #1F2937;
            line-height: 1.6;
            font-size: 10.5pt;
        }
        
        /* Cover Page */
        .cover {
            text-align: center;
            padding-top: 120px;
            page-break-after: always;
        }
        .cover-logo {
            font-size: 38pt;
            font-weight: 800;
            color: #0284C7;
            letter-spacing: 2px;
            margin-bottom: 0px;
        }
        .cover-subtitle {
            font-size: 18pt;
            font-weight: 400;
            color: #475569;
            margin-top: 5px;
            margin-bottom: 40px;
        }
        .cover-badge {
            display: inline-block;
            background-color: #E0F2FE;
            color: #0369A1;
            padding: 6px 18px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 11pt;
        }
        .cover-meta {
            margin-top: 220px;
            color: #64748B;
            font-size: 10pt;
            border-top: 1px solid #E2E8F0;
            padding-top: 20px;
        }
        
        /* Typography */
        h1.section-header {
            font-size: 18pt;
            color: #0F172A;
            border-bottom: 2px solid #0284C7;
            padding-bottom: 6px;
            margin-top: 30px;
            margin-bottom: 15px;
            page-break-after: avoid;
        }
        h2 {
            font-size: 13pt;
            color: #0369A1;
            margin-top: 20px;
            margin-bottom: 8px;
            page-break-after: avoid;
        }
        h3 {
            font-size: 11pt;
            color: #334155;
            margin-top: 14px;
            margin-bottom: 4px;
            page-break-after: avoid;
        }
        p {
            margin-bottom: 10px;
            text-align: justify;
        }
        
        /* Components & Callouts */
        .callout {
            background-color: #F8FAFC;
            border-left: 4px solid #0284C7;
            padding: 12px 16px;
            margin: 15px 0;
            border-radius: 0 6px 6px 0;
        }
        .callout-title {
            font-weight: 700;
            color: #0369A1;
            margin-bottom: 4px;
        }
        
        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 10pt;
        }
        th {
            background-color: #0F172A;
            color: #FFFFFF;
            font-weight: 600;
            padding: 8px 12px;
            text-align: left;
        }
        td {
            border-bottom: 1px solid #E2E8F0;
            padding: 8px 12px;
            vertical-align: top;
        }
        tr:nth-child(even) {
            background-color: #F8FAFC;
        }
        
        /* Lists & Badges */
        ul, ol {
            margin-top: 5px;
            margin-bottom: 15px;
            padding-left: 20px;
        }
        li {
            margin-bottom: 4px;
        }
        .kbd {
            background-color: #F1F5F9;
            border: 1px solid #CBD5E1;
            border-radius: 4px;
            padding: 2px 6px;
            font-family: Consolas, monospace;
            font-size: 9pt;
            color: #0F172A;
        }
        
        .page-break {
            page-break-before: always;
        }
        .footer {
            text-align: center;
            font-size: 8.5pt;
            color: #94A3B8;
            margin-top: 40px;
            border-top: 1px solid #E2E8F0;
            padding-top: 10px;
        }
    </style>
    </head>
    <body>

        <!-- COVER PAGE -->
        <div class="cover">
            <div class="cover-logo">ALLME</div>
            <div class="cover-subtitle">Master Desktop Widget & Telemetry Controller</div>
            <div class="cover-badge">Official Product User Manual — Version 36</div>
            <div class="cover-meta">
                <strong>Platform:</strong> Microsoft Windows (x64)<br>
                <strong>Document Ref:</strong> ALLME-UM-V36-WIN<br>
                <strong>Publication Date:</strong> 2026
            </div>
        </div>

        <!-- TABLE OF CONTENTS -->
        <h1 class="section-header">Table of Contents</h1>
        <ol>
            <li><strong>Product Overview & Concept</strong></li>
            <li><strong>Widget Geometry & Interactive Control Ring</strong></li>
            <li><strong>Operating Modes & Mouse / Keyboard Shortcuts</strong></li>
            <li><strong>Comprehensive Menu Reference</strong></li>
            <li><strong>Audio Spectrum Visualizations & Audio Modes</strong></li>
            <li><strong>Telemetry Link Source & Modulation Sink Engine</strong></li>
            <li><strong>Futuristic Diagnostic Dashboard</strong></li>
            <li><strong>System Paths, Configuration & Troubleshooting</strong></li>
        </ol>

        <div class="page-break"></div>

        <!-- SECTION 1 -->
        <h1 class="section-header">1. Product Overview & Concept</h1>
        <p>
            <strong>Allme</strong> is an omnipresent, frameless, translucent desktop widget designed for Microsoft Windows. 
            Functioning as a central command hub, Allme overlays your workspace to provide high-speed window and web tab navigation, instantaneous full-screen/regional screen capture, real-time video recording, dynamic audio spectrum visualizations, and granular system telemetry telemetry monitoring.
        </p>
        <div class="callout">
            <div class="callout-title">Core Operating Philosophy</div>
            Allme resides unobtrusively on your desktop as a customizable circular orb. It eliminates the need for complex multi-key combinations or switching away from your active work environment by mapping essential productivity and telemetry controls directly to radial mouse gestures and interactive rings.
        </div>

        <!-- SECTION 2 -->
        <h1 class="section-header">2. Widget Geometry & Interactive Control Ring</h1>
        <p>
            The main visual interface consists of a 3-zone interactive circular widget surrounded by an ambient background glow. 
            Understanding the 3 distinct interaction zones is key to operating Allme efficiently:
        </p>
        
        <table>
            <thead>
                <tr>
                    <th>Zone Name</th>
                    <th>Visual Region</th>
                    <th>Primary Functionality</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Center Core</strong></td>
                    <td>Inner central circle with active application icon/favicon</td>
                    <td>Triggers primary quick-switches, browser tab actions, or initiates screen video recording.</td>
                </tr>
                <tr>
                    <td><strong>Left Ring Sector</strong></td>
                    <td>Outer left semicircular arc sector</td>
                    <td>Executes backward window cycling, tab stepping left, or screen capture.</td>
                </tr>
                <tr>
                    <td><strong>Right Ring Sector</strong></td>
                    <td>Outer right semicircular arc sector</td>
                    <td>Executes forward window cycling, tab stepping right, or screen capture.</td>
                </tr>
            </tbody>
        </table>

        <!-- SECTION 3 -->
        <h1 class="section-header">3. Operating Modes & Mouse / Keyboard Shortcuts</h1>
        
        <h2>Direct Mouse Button Mapping</h2>
        <p>Actions vary depending on which mouse button is clicked and which ring sector is targeted:</p>
        
        <table>
            <thead>
                <tr>
                    <th>Mouse Action</th>
                    <th>Target Zone</th>
                    <th>Executed Operation</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Left Click</strong></td>
                    <td>Center Core</td>
                    <td><strong>Quick Switch:</strong> Toggles focus instantly to the previous active window.</td>
                </tr>
                <tr>
                    <td><strong>Left Click</strong></td>
                    <td>Left Ring Sector</td>
                    <td><strong>Window Cycle Left:</strong> Cycles focus backward through open application windows.</td>
                </tr>
                <tr>
                    <td><strong>Left Click</strong></td>
                    <td>Right Ring Sector</td>
                    <td><strong>Window Cycle Right:</strong> Cycles focus forward through open application windows.</td>
                </tr>
                <tr>
                    <td><strong>Right Click</strong></td>
                    <td>Center Core</td>
                    <td><strong>Tab Switch:</strong> Focuses the primary active browser and switches active tab.</td>
                </tr>
                <tr>
                    <td><strong>Right Click</strong></td>
                    <td>Left Ring Sector</td>
                    <td><strong>Tab Cycle Left:</strong> Sends Ctrl+PageUp to step to the previous browser tab.</td>
                </tr>
                <tr>
                    <td><strong>Right Click</strong></td>
                    <td>Right Ring Sector</td>
                    <td><strong>Tab Cycle Right:</strong> Sends Ctrl+PageDown to step to the next browser tab.</td>
                </tr>
                <tr>
                    <td><strong>Middle Click</strong></td>
                    <td>Center Core</td>
                    <td><strong>Record Video On/Off:</strong> Toggles full screen MP4 video recording. Widget border turns red during active recording.</td>
                </tr>
                <tr>
                    <td><strong>Middle Click</strong></td>
                    <td>Outer Sectors</td>
                    <td><strong>Take Screenshot:</strong> Captures screen snapshot with a quick white visual flash feedback.</td>
                </tr>
            </tbody>
        </table>

        <h2>Keyboard Modifier Shortcuts</h2>
        <p>Combining keyboard modifier keys while left-clicking the widget triggers specialized operational modes:</p>
        <ul>
            <li><span class="kbd">Shift</span> + <strong>Left Click</strong>: Toggle <strong>Lock Position</strong> (prevents moving widget).</li>
            <li><span class="kbd">Ctrl</span> + <strong>Left Click</strong>: Toggle <strong>Fly Mode</strong> (widget follows cursor coordinates).</li>
            <li><span class="kbd">Alt</span> + <strong>Left Click</strong>: Instantly terminate and <strong>Quit Allme</strong>.</li>
        </ul>

        <h2>Widget Positioning & Special Modes</h2>
        <ul>
            <li><strong>Dragging:</strong> Left-click and hold anywhere on the widget to reposition it on screen.</li>
            <li><strong>Fly Mode:</strong> When enabled, the widget tracks mouse movements with intelligent screen border collision limits. Pressing <span class="kbd">Middle Click</span> anywhere on screen during Fly Mode triggers Quick Switch.</li>
            <li><strong>Clickthrough Mode:</strong> Allows mouse events to pass directly through the widget to background windows.</li>
        </ul>

        <div class="page-break"></div>

        <!-- SECTION 4 -->
        <h1 class="section-header">4. Comprehensive Menu Reference</h1>
        <p>
            Right-clicking the System Tray icon or invoking the context menu provides access to all configuration items:
        </p>

        <table>
            <thead>
                <tr>
                    <th>Menu Item</th>
                    <th>Type</th>
                    <th>Description & Function</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Always on Top</strong></td>
                    <td>Toggle</td>
                    <td>Forces the widget window to remain on top of all desktop windows.</td>
                </tr>
                <tr>
                    <td><strong>Lock Position</strong></td>
                    <td>Toggle</td>
                    <td>Locks widget coordinates to prevent accidental dragging.</td>
                </tr>
                <tr>
                    <td><strong>Clickthrough (Pass Mouse)</strong></td>
                    <td>Toggle</td>
                    <td>Enables mouse click-through behavior based on selected mode.</td>
                </tr>
                <tr>
                    <td><strong>Clickthrough Mode</strong></td>
                    <td>Submenu</td>
                    <td>Options: <em>1. Pass All (Hardware Pass-Through)</em>, <em>2. Pass Left Click Only</em>, <em>3. Pass Right Click Only</em>, <em>4. Pass Middle Click Only</em>.</td>
                </tr>
                <tr>
                    <td><strong>Fly Mode (Follow Cursor)</strong></td>
                    <td>Toggle</td>
                    <td>Enables cursor-tracking flight behavior.</td>
                </tr>
                <tr>
                    <td><strong>Futuristic Dashboard</strong></td>
                    <td>Action</td>
                    <td>Launches the full performance diagnostic and monitoring dashboard window.</td>
                </tr>
                <tr>
                    <td><strong>Enable Ambient Glow</strong></td>
                    <td>Toggle</td>
                    <td>Toggles outer radial gradient glow around the widget body.</td>
                </tr>
                <tr>
                    <td><strong>Enable Audio Overlay Visualizations</strong></td>
                    <td>Toggle</td>
                    <td>Enables or disables live audio spectrum visual overlays.</td>
                </tr>
                <tr>
                    <td><strong>Enable Breathing Animation</strong></td>
                    <td>Toggle</td>
                    <td>Activates dynamic sine-wave pulsing breathing animations.</td>
                </tr>
                <tr>
                    <td><strong>Breathing Target</strong></td>
                    <td>Submenu</td>
                    <td>Directs breathing pulse target: <em>1. Both (App & Glow)</em>, <em>2. App Only</em>, <em>3. Glow Only</em>.</td>
                </tr>
                <tr>
                    <td><strong>Enable Mouse Movement Activity</strong></td>
                    <td>Toggle</td>
                    <td>Modulates glow and widget scale dynamically based on cursor speed.</td>
                </tr>
                <tr>
                    <td><strong>Mouse Movement Target</strong></td>
                    <td>Submenu</td>
                    <td>Directs mouse activity modulation target: <em>1. Both</em>, <em>2. App Only</em>, <em>3. Glow Only</em>.</td>
                </tr>
                <tr>
                    <td><strong>Start with Windows</strong></td>
                    <td>Toggle</td>
                    <td>Registers executable in Windows Registry for auto-start upon user login.</td>
                </tr>
                <tr>
                    <td><strong>Color Hue Target</strong></td>
                    <td>Submenu</td>
                    <td>Selects color hue application scope (Both, App, Glow) & includes <strong>Link System Accent</strong> toggle to sync with Windows DWM theme color.</td>
                </tr>
                <tr>
                    <td><strong>Audio Visualizations</strong></td>
                    <td>Submenu</td>
                    <td>Configures real-time audio driver mode and audio visualizer profile.</td>
                </tr>
                <tr>
                    <td><strong>Link Source</strong></td>
                    <td>Submenu</td>
                    <td>Selects system telemetry telemetry data channel (0 to 9).</td>
                </tr>
                <tr>
                    <td><strong>Link Sink</strong></td>
                    <td>Submenu</td>
                    <td>Selects widget visual property to modulate based on telemetry (0 to 9).</td>
                </tr>
                <tr>
                    <td><strong>App / Glow Sliders</strong></td>
                    <td>Sliders</td>
                    <td>Adjustable sliders for App Opacity, Glow Opacity, Glow Size, Color Hue (0-360°), Breathing Speed, and App Size.</td>
                </tr>
                <tr>
                    <td><strong>Quit Allme</strong></td>
                    <td>Action</td>
                    <td>Closes all threads, releases hardware hooks, and exits the application.</td>
                </tr>
            </tbody>
        </table>

        <!-- SECTION 5 -->
        <h1 class="section-header">5. Audio Spectrum Visualizations & Audio Modes</h1>
        <h2>Audio Driver Modes</h2>
        <ul>
            <li><strong>Both (Volume & Frequency):</strong> Modulates both amplitude size and frequency waveform animations.</li>
            <li><strong>Volume Only:</strong> Responds exclusively to master audio amplitude.</li>
            <li><strong>Frequency Only:</strong> Responds exclusively to frequency spectrum shifts.</li>
        </ul>

        <h2>Audio Effect Profiles</h2>
        <table>
            <thead>
                <tr>
                    <th>Effect Name</th>
                    <th>Visual Render Behavior</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Pulsing Aura (Classic)</strong></td>
                    <td>Smooth radial glow expanding and contracting with audio intensity.</td>
                </tr>
                <tr>
                    <td><strong>Chroma Pulse (Rainbow Shift)</strong></td>
                    <td>Dynamic HSL rainbow spectrum rotation synchronized with sound peaks.</td>
                </tr>
                <tr>
                    <td><strong>Equalizer Ring</strong></td>
                    <td>24 radial spectrum equalizer bars radiating around the widget perimeter.</td>
                </tr>
                <tr>
                    <td><strong>Waveform Orbit</strong></td>
                    <td>Continuous oscillating circular audio waveform surrounding the widget outer border.</td>
                </tr>
                <tr>
                    <td><strong>Frequency Ripple</strong></td>
                    <td>Concentric shockwave rings emitting outward from the center core on audio transients.</td>
                </tr>
                <tr>
                    <td><strong>Particle Spark</strong></td>
                    <td>12 orbiting beat orbs expanding and dancing to musical rhythm and bass hits.</td>
                </tr>
            </tbody>
        </table>

        <div class="page-break"></div>

        <!-- SECTION 6 -->
        <h1 class="section-header">6. Telemetry Link Source & Modulation Sink Engine</h1>
        <p>
            Allme features an advanced real-time binding engine that allows you to link live system hardware metrics (Link Source) to visual attributes of the widget (Link Sink).
        </p>

        <h2>Available Telemetry Channels (Link Sources)</h2>
        <ol start="0">
            <li><strong>None:</strong> Disable telemetry data binding.</li>
            <li><strong>Normal Human Breathing Sine:</strong> Simulated calm human respiration cycle.</li>
            <li><strong>CPU Frequency:</strong> Real-time processor clock frequency.</li>
            <li><strong>CPU Usage:</strong> Total CPU utilization percentage across all cores.</li>
            <li><strong>HDD Activity:</strong> Disk throughput (Configurable by drive: All, Drive 0, 1, 2; and IO mode: Read/Write/Both).</li>
            <li><strong>Memory Usage:</strong> Real-time system RAM utilization percentage.</li>
            <li><strong>Ethernet & Ping:</strong> Network interface throughput & ICMP latency (Modes: Upload, Download, Both, Ping ms).</li>
            <li><strong>GPU Usage:</strong> NVIDIA/System graphics card workload percentage (GPU 0, GPU 1, or Max).</li>
            <li><strong>System Power Usage:</strong> AC/Battery power status and discharge rate.</li>
            <li><strong>Keyboard Typing Speed:</strong> Live Words Per Minute (WPM) calculations via low-level hook.</li>
        </ol>

        <h2>Modulation Targets (Link Sinks)</h2>
        <ol start="0">
            <li><strong>None</strong></li>
            <li><strong>App Size:</strong> Modulates widget diameter.</li>
            <li><strong>App Color:</strong> Shifts widget color hue from Red to Blue based on telemetry level.</li>
            <li><strong>Glow Size:</strong> Modulates radial glow extent.</li>
            <li><strong>Glow Color:</strong> Shifts glow color hue from Blue to Red based on telemetry level.</li>
            <li><strong>App Opacity:</strong> Adjusts widget transparency dynamically.</li>
            <li><strong>Glow Opacity:</strong> Adjusts glow intensity dynamically.</li>
            <li><strong>App + Glow Size:</strong> Combined scale modulation.</li>
            <li><strong>App + Glow Color Shift:</strong> Combined color shift modulation.</li>
            <li><strong>App + Glow Opacity:</strong> Combined transparency modulation.</li>
        </ol>

        <!-- SECTION 7 -->
        <h1 class="section-header">7. Futuristic Diagnostic Dashboard</h1>
        <p>
            Selecting <strong>Futuristic Dashboard</strong> from the menu opens a dedicated telemetry monitoring window. 
            The dashboard presents detailed visual counters, high-frequency graph plots, and system diagnostics:
        </p>
        <ul>
            <li><strong>CPU Performance Graph:</strong> Per-core load meters, overall utilization percentages, and clock frequencies.</li>
            <li><strong>GPU Telemetry Card:</strong> Live GPU load, VRAM allocation, and NVML temperature readout.</li>
            <li><strong>Memory Allocation Meter:</strong> Active RAM consumption vs total physical memory.</li>
            <li><strong>Disk & Network Telemetry:</strong> Real-time read/write disk I/O rates, net upload/download bandwidth, and live ping latency counters.</li>
            <li><strong>Input Velocity Meters:</strong> Live typing WPM calculator and mouse cursor velocity telemetry.</li>
        </ul>

        <!-- SECTION 8 -->
        <h1 class="section-header">8. System Paths, Configuration & Troubleshooting</h1>
        
        <h2>File System Locations</h2>
        <table>
            <thead>
                <tr>
                    <th>Data Type</th>
                    <th>System Path</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Screenshots Directory</strong></td>
                    <td><code>%USERPROFILE%\Pictures\Allme\Screenshots\</code></td>
                </tr>
                <tr>
                    <td><strong>Recordings Directory</strong></td>
                    <td><code>%USERPROFILE%\Pictures\Allme\Recordings\</code></td>
                </tr>
                <tr>
                    <td><strong>Configuration File</strong></td>
                    <td><code>%APPDATA%\Allme\config.json</code></td>
                </tr>
                <tr>
                    <td><strong>Crash & Diagnostic Log</strong></td>
                    <td><code>%LOCALAPPDATA%\Allme\Logs\allme_crash_report.txt</code></td>
                </tr>
            </tbody>
        </table>

        <h2>Troubleshooting & Diagnostics</h2>
        <div class="callout">
            <div class="callout-title">Widget Off-Screen or Hidden</div>
            If the widget is moved off-screen, restarting the application automatically detects screen boundary violations and resets the position to the desktop safe zone. Alternatively, edit <code>config.json</code> to reset <code>pos_x</code> and <code>pos_y</code>.
        </div>

        <div class="callout">
            <div class="callout-title">Single Instance Protection</div>
            Allme enforces a strict single-instance process lock. Launching a new instance automatically terminates any existing background process to prevent audio hook conflicts and duplicate desktop widgets.
        </div>

        <div class="footer">
            Allme Product User Manual — Version 36 | Designed for Microsoft Windows<br>
            All Rights Reserved &copy; 2026
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
    print("Comprehensive Product User Manual created successfully at AllmeD_v36_Product_User_Manual.pdf")

if __name__ == '__main__':
    generate_manual()
