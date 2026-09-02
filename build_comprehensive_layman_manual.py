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
            margin: 18mm;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #1E293B;
            line-height: 1.6;
            font-size: 10pt;
        }
        
        /* Cover Page */
        .cover {
            text-align: center;
            padding-top: 140px;
            page-break-after: always;
        }
        .cover-logo {
            font-size: 42pt;
            font-weight: 900;
            color: #0284C7;
            letter-spacing: 3px;
            margin-bottom: 0px;
        }
        .cover-subtitle {
            font-size: 20pt;
            font-weight: 300;
            color: #475569;
            margin-top: 5px;
            margin-bottom: 30px;
        }
        .cover-badge {
            display: inline-block;
            background-color: #E0F2FE;
            color: #0369A1;
            padding: 8px 24px;
            border-radius: 25px;
            font-weight: 700;
            font-size: 12pt;
        }
        .cover-desc {
            margin-top: 50px;
            font-size: 11pt;
            color: #64748B;
            max-width: 80%;
            margin-left: auto;
            margin-right: auto;
        }
        .cover-meta {
            margin-top: 160px;
            color: #94A3B8;
            font-size: 9.5pt;
            border-top: 1px solid #E2E8F0;
            padding-top: 20px;
        }
        
        /* Typography */
        h1.section-header {
            font-size: 16pt;
            color: #0F172A;
            border-bottom: 2.5px solid #0284C7;
            padding-bottom: 4px;
            margin-top: 28px;
            margin-bottom: 12px;
            page-break-after: avoid;
        }
        h2 {
            font-size: 12pt;
            color: #0369A1;
            margin-top: 18px;
            margin-bottom: 6px;
            page-break-after: avoid;
        }
        h3 {
            font-size: 10.5pt;
            color: #334155;
            margin-top: 12px;
            margin-bottom: 4px;
            page-break-after: avoid;
        }
        p {
            margin-bottom: 10px;
            text-align: justify;
        }
        
        /* Boxes & Callouts */
        .layman-box {
            background-color: #F0F9FF;
            border-left: 4px solid #0284C7;
            padding: 10px 14px;
            margin: 12px 0;
            border-radius: 0 6px 6px 0;
        }
        .layman-title {
            font-weight: 700;
            color: #0369A1;
            margin-bottom: 3px;
            font-size: 10.5pt;
        }
        
        .tip-box {
            background-color: #F0FDF4;
            border-left: 4px solid #16A34A;
            padding: 10px 14px;
            margin: 12px 0;
            border-radius: 0 6px 6px 0;
        }
        .tip-title {
            font-weight: 700;
            color: #15803D;
            margin-bottom: 3px;
        }

        .warn-box {
            background-color: #FEF2F2;
            border-left: 4px solid #EF4444;
            padding: 10px 14px;
            margin: 12px 0;
            border-radius: 0 6px 6px 0;
        }
        .warn-title {
            font-weight: 700;
            color: #B91C1C;
            margin-bottom: 3px;
        }
        
        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0;
            font-size: 9.5pt;
        }
        th {
            background-color: #0F172A;
            color: #FFFFFF;
            font-weight: 600;
            padding: 7px 10px;
            text-align: left;
        }
        td {
            border-bottom: 1px solid #E2E8F0;
            padding: 7px 10px;
            vertical-align: top;
        }
        tr:nth-child(even) {
            background-color: #F8FAFC;
        }
        
        /* Badges & Keycaps */
        .kbd {
            background-color: #F1F5F9;
            border: 1px solid #CBD5E1;
            border-radius: 4px;
            padding: 2px 5px;
            font-family: Consolas, monospace;
            font-size: 9pt;
            color: #0F172A;
            font-weight: 600;
        }

        .menu-path {
            color: #0284C7;
            font-weight: 700;
            font-family: Consolas, monospace;
        }

        .page-break {
            page-break-before: always;
        }
        .footer {
            text-align: center;
            font-size: 8.5pt;
            color: #94A3B8;
            margin-top: 35px;
            border-top: 1px solid #E2E8F0;
            padding-top: 8px;
        }
    </style>
    </head>
    <body>

        <!-- COVER PAGE -->
        <div class="cover">
            <div class="cover-logo">ALLME</div>
            <div class="cover-subtitle">Complete Layman's User Manual</div>
            <div class="cover-badge">Comprehensive Product Guide — Version 36</div>
            <div class="cover-desc">
                An easy-to-understand, step-by-step guide explaining every single feature, menu item, mouse gesture, shortcut, and visual customizer in Allme.
            </div>
            <div class="cover-meta">
                <strong>Target Platform:</strong> Microsoft Windows<br>
                <strong>Language:</strong> Plain English / Layman's Terms<br>
                <strong>Document ID:</strong> ALLME-FULL-MANUAL-V36
            </div>
        </div>

        <!-- TABLE OF CONTENTS -->
        <h1 class="section-header">Table of Contents</h1>
        <ol style="line-height: 1.8;">
            <li><strong>Introduction: What is Allme and What Does It Do?</strong></li>
            <li><strong>Understanding the Allme Desktop Orb (Visual Layout)</strong></li>
            <li><strong>How to Operate Allme (Mouse Clicks & Keyboard Tricks)</strong></li>
            <li><strong>Complete Layman's Guide to Menu Options & Settings</strong>
                <ul>
                    <li>General Controls & Display Modes</li>
                    <li>Visual Animations & Breathing Effects</li>
                    <li>Colors, Themes & System Color Linking</li>
                    <li>Music & Audio Spectrum Visualizers</li>
                    <li>System Health Binding (Link Source & Link Sink)</li>
                    <li>Sizing & Transparency Sliders</li>
                </ul>
            </li>
            <li><strong>The Futuristic System Health Dashboard</strong></li>
            <li><strong>Taking Screenshots & Recording Videos</strong></li>
            <li><strong>Saved File Locations & Troubleshooting Common Issues</strong></li>
        </ol>

        <div class="page-break"></div>

        <!-- SECTION 1 -->
        <h1 class="section-header">1. Introduction: What is Allme and What Does It Do?</h1>
        <p>
            Welcome to <strong>Allme</strong>! Allme is a smart, friendly assistant widget that floats on your computer desktop. 
            It is shaped like a smooth circular orb and sits gently on top of your windows so you can always see and use it.
        </p>
        <p>
            Instead of searching through taskbars or remembering complicated computer commands, Allme gives you instant access to your daily desktop tools with simple mouse clicks.
        </p>
        
        <div class="layman-box">
            <div class="layman-title">What can Allme do for you in plain language?</div>
            <ul>
                <li><strong>Switch Open Apps Instantly:</strong> Click the orb to hop between open programs without searching the taskbar.</li>
                <li><strong>Switch Web Browser Tabs:</strong> Step through your web browser tabs forward and backward directly from the orb.</li>
                <li><strong>Take Screenshots & Record Screen Video:</strong> Capture snapshots or record video clips of your monitor with a single click.</li>
                <li><strong>Glow & Dance to Your Music:</strong> Watch the orb light up with colorful waves and pulsing rings whenever you play songs or videos.</li>
                <li><strong>Monitor Your PC's Health:</strong> See your processor (CPU), graphics card (GPU), memory (RAM), internet speed, and typing speed in real time.</li>
            </ul>
        </div>

        <!-- SECTION 2 -->
        <h1 class="section-header">2. Understanding the Allme Desktop Orb (Visual Layout)</h1>
        <p>
            The Allme widget is designed as a circular orb divided into 3 distinct clickable areas, surrounded by an outer glowing ring:
        </p>
        
        <table>
            <thead>
                <tr>
                    <th>Orb Area</th>
                    <th>Where It Is</th>
                    <th>What You See Inside It</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Center Core</strong></td>
                    <td>The small circle in the very middle of the orb.</td>
                    <td>Shows the logo of your currently active web browser or program icon. Turns into a solid red square while recording video.</td>
                </tr>
                <tr>
                    <td><strong>Left Sector</strong></td>
                    <td>The outer left half-ring surrounding the center.</td>
                    <td>Separated by subtle dashed lines. Highlights when your mouse hovers over the left side.</td>
                </tr>
                <tr>
                    <td><strong>Right Sector</strong></td>
                    <td>The outer right half-ring surrounding the center.</td>
                    <td>Separated by subtle dashed lines. Highlights when your mouse hovers over the right side.</td>
                </tr>
                <tr>
                    <td><strong>Ambient Glow Halo</strong></td>
                    <td>The soft radial light shining around the orb.</td>
                    <td>Pulses with breathing effects, moves with sound volume, or changes color according to your PC health metrics.</td>
                </tr>
            </tbody>
        </table>

        <!-- SECTION 3 -->
        <h1 class="section-header">3. How to Operate Allme (Mouse Clicks & Keyboard Tricks)</h1>
        
        <h2>Basic Mouse Controls</h2>
        <p>Operating Allme is as simple as clicking different parts of the orb with your mouse buttons:</p>
        
        <table>
            <thead>
                <tr>
                    <th>Mouse Button</th>
                    <th>Where You Click</th>
                    <th>What Happens (Action)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Left Click</strong></td>
                    <td>Center Core</td>
                    <td><strong>Quick Switch:</strong> Instantly jumps back to the last program you were working in.</td>
                </tr>
                <tr>
                    <td><strong>Left Click</strong></td>
                    <td>Left Sector</td>
                    <td><strong>Previous App:</strong> Cycles backward to the previous open window on your desktop.</td>
                </tr>
                <tr>
                    <td><strong>Left Click</strong></td>
                    <td>Right Sector</td>
                    <td><strong>Next App:</strong> Cycles forward to the next open window on your desktop.</td>
                </tr>
                <tr>
                    <td><strong>Right Click</strong></td>
                    <td>Center Core</td>
                    <td><strong>Switch Browser Tab:</strong> Brings your web browser to the front and switches tabs.</td>
                </tr>
                <tr>
                    <td><strong>Right Click</strong></td>
                    <td>Left Sector</td>
                    <td><strong>Previous Tab:</strong> Moves to the browser tab on the left.</td>
                </tr>
                <tr>
                    <td><strong>Right Click</strong></td>
                    <td>Right Sector</td>
                    <td><strong>Next Tab:</strong> Moves to the browser tab on the right.</td>
                </tr>
                <tr>
                    <td><strong>Middle Click</strong></td>
                    <td>Center Core</td>
                    <td><strong>Record Video:</strong> Starts or stops recording your screen. The orb border turns red while recording.</td>
                </tr>
                <tr>
                    <td><strong>Middle Click</strong></td>
                    <td>Left or Right Sector</td>
                    <td><strong>Take Screenshot:</strong> Takes a snapshot picture of your screen. The orb flashes white to confirm.</td>
                </tr>
            </tbody>
        </table>

        <div class="page-break"></div>

        <h2>Keyboard & Mouse Combination Tricks</h2>
        <p>You can hold down a key on your keyboard while left-clicking the orb to perform special actions:</p>
        <ul>
            <li><span class="kbd">Shift</span> + <strong>Left Click</strong>: Locks or unlocks the orb's position so you don't accidentally move it.</li>
            <li><span class="kbd">Ctrl</span> + <strong>Left Click</strong>: Turns on <strong>Fly Mode</strong>, making the orb follow your mouse pointer across the desktop.</li>
            <li><span class="kbd">Alt</span> + <strong>Left Click</strong>: Safely closes and exits Allme completely.</li>
        </ul>

        <h2>Moving & Positioning Allme</h2>
        <p>
            To move Allme anywhere on your screen, simply click and hold the left mouse button on the orb and drag it to your desired spot. 
            Allme will automatically remember where you left it, even when you restart your computer!
        </p>

        <!-- SECTION 4 -->
        <h1 class="section-header">4. Complete Layman's Guide to Menu Options & Settings</h1>
        <p>
            Right-clicking the Allme System Tray icon (located near your Windows clock) or right-clicking the menu area opens the <strong>Settings Menu</strong>. 
            Here is a plain-English breakdown of every single menu item and setting:
        </p>

        <h2>Part A: General Controls & Display Modes</h2>
        <table>
            <thead>
                <tr>
                    <th>Menu Setting Name</th>
                    <th>What It Means in Layman's Language</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="menu-path">Always on Top</span></td>
                    <td>When checked, Allme stays visible above all other open programs so it never gets hidden under heavy windows.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">Lock Position</span></td>
                    <td>Freezes Allme in its current spot on your desktop so you cannot accidentally drag or nudge it while clicking.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">Clickthrough (Pass Mouse)</span></td>
                    <td>Makes Allme "transparent" to your mouse. Clicks will pass right through Allme to whatever window or desktop item is behind it.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">🖱️ Clickthrough Mode</span></td>
                    <td>
                        Submenu offering 4 mouse pass-through choices:<br>
                        • <strong>1. Pass All:</strong> Passes all clicks through Allme to background apps.<br>
                        • <strong>2. Pass Left Click Only:</strong> Only left clicks pass through.<br>
                        • <strong>3. Pass Right Click Only:</strong> Only right clicks pass through.<br>
                        • <strong>4. Pass Middle Click Only:</strong> Only middle clicks pass through.
                    </td>
                </tr>
                <tr>
                    <td><span class="menu-path">Fly Mode (Follow Cursor)</span></td>
                    <td>Makes Allme follow your mouse pointer around the screen like a floating helper orb. (Middle-clicking while in Fly Mode instantly switches active windows).</td>
                </tr>
                <tr>
                    <td><span class="menu-path">🎛️ Futuristic Dashboard</span></td>
                    <td>Opens a large, high-tech window displaying detailed graphs of your computer's speed, graphics card, RAM memory, and internet traffic.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">Start with Windows</span></td>
                    <td>When turned on, Allme starts up automatically every time you turn on or log into your Windows computer.</td>
                </tr>
            </tbody>
        </table>

        <h2>Part B: Visual Animations & Breathing Effects</h2>
        <table>
            <thead>
                <tr>
                    <th>Menu Setting Name</th>
                    <th>What It Means in Layman's Language</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="menu-path">Enable Ambient Glow</span></td>
                    <td>Turns the soft glowing light halo around the outside of Allme on or off.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">Enable Breathing Animation</span></td>
                    <td>Adds a slow, gentle pulsing rhythm to Allme, making it feel like it is gently breathing.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">🫁 Breathing Target</span></td>
                    <td>
                        Submenu choosing where the breathing pulse appears:<br>
                        • <strong>1. Both (App & Glow):</strong> Both the orb and the outer glow pulse together.<br>
                        • <strong>2. App Only:</strong> Only the inner orb pulses in size.<br>
                        • <strong>3. Glow Only:</strong> Only the outer glowing light pulses.
                    </td>
                </tr>
                <tr>
                    <td><span class="menu-path">Enable Mouse Movement Activity</span></td>
                    <td>Makes Allme react when you move your mouse cursor quickly. The glow gets brighter and larger as mouse speed increases.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">🖱️ Mouse Movement Target</span></td>
                    <td>Choose whether fast mouse movement brightens <strong>1. Both</strong>, <strong>2. App Only</strong>, or <strong>3. Glow Only</strong>.</td>
                </tr>
            </tbody>
        </table>

        <div class="page-break"></div>

        <h2>Part C: Colors, Themes & System Color Linking</h2>
        <table>
            <thead>
                <tr>
                    <th>Menu Setting Name</th>
                    <th>What It Means in Layman's Language</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="menu-path">🎨 Color Hue Target</span></td>
                    <td>
                        Selects where your custom color choice is applied:<br>
                        • <strong>Both (App & Glow):</strong> Colors both the inner orb and outer glow.<br>
                        • <strong>App Only:</strong> Colors only the inner orb.<br>
                        • <strong>Glow Only:</strong> Colors only the outer glowing halo.
                    </td>
                </tr>
                <tr>
                    <td><span class="menu-path">Link System Accent</span></td>
                    <td>Automatically matches Allme's color theme to your Windows system accent color (your personal Windows color theme).</td>
                </tr>
            </tbody>
        </table>

        <h2>Part D: Music & Audio Spectrum Visualizers</h2>
        <table>
            <thead>
                <tr>
                    <th>Menu Setting Name</th>
                    <th>What It Means in Layman's Language</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="menu-path">Enable Audio Overlay Visualizations</span></td>
                    <td>Turns on live music visualizer effects so Allme dances whenever audio or music plays from your speakers.</td>
                </tr>
                <tr>
                    <td><span class="menu-path">🎛️ Audio Driver Mode</span></td>
                    <td>
                        Submenu choosing how Allme listens to sound:<br>
                        • <strong>1. Both (Volume & Frequency):</strong> Reacts to both sound loudness and musical pitches.<br>
                        • <strong>2. Volume Only:</strong> Reacts only to how loud the sound is.<br>
                        • <strong>3. Frequency Only:</strong> Reacts only to high/low musical notes and beats.
                    </td>
                </tr>
                <tr>
                    <td><span class="menu-path">🎵 Audio Visualizations (Profiles)</span></td>
                    <td>
                        Select your favorite visual style when music plays:<br>
                        • <strong>Pulsing Aura:</strong> A classic glowing halo that pulses smoothly with the beat.<br>
                        • <strong>Chroma Pulse:</strong> A rainbow color show that shifts through colors as music plays.<br>
                        • <strong>Equalizer Ring:</strong> 24 equalizer frequency bars bouncing around the orb like a stereo system.<br>
                        • <strong>Waveform Orbit:</strong> A wavy sound wave spinning around the outside edge of Allme.<br>
                        • <strong>Frequency Ripple:</strong> Shockwave light rings expanding outward whenever heavy bass or drum beats hit.<br>
                        • <strong>Particle Spark:</strong> 12 glowing beat dots orbiting and jumping to the rhythm.
                    </td>
                </tr>
            </tbody>
        </table>

        <h2>Part E: System Health Data Linking (Link Source & Link Sink)</h2>
        <p>
            Allme allows you to link your computer's health metrics (Link Source) to visual changes in the widget (Link Sink).
        </p>

        <h3>Link Source Options (What computer stat do you want to track?)</h3>
        <ul>
            <li><strong>0. None:</strong> Turns off system stat tracking.</li>
            <li><strong>1. Normal Human Breathing Sine:</strong> Uses a smooth, relaxed human breathing rhythm.</li>
            <li><strong>2. CPU Frequency:</strong> Tracks your processor's speed (clock rate).</li>
            <li><strong>3. CPU Usage:</strong> Tracks how hard your processor is working (0% to 100%).</li>
            <li><strong>4. HDD Activity:</strong> Tracks hard drive reading/writing activity. Includes <em>HDD Settings</em> to choose specific drives or Read/Write modes.</li>
            <li><strong>5. Memory Usage:</strong> Tracks how much RAM memory your PC is currently using.</li>
            <li><strong>6. Ethernet & Ping:</strong> Tracks your internet download/upload speeds or ping latency (delay).</li>
            <li><strong>7. GPU Usage:</strong> Tracks how hard your graphics card is working (great for gaming).</li>
            <li><strong>8. System Power Usage:</strong> Tracks your power supply status and laptop battery discharge rate.</li>
            <li><strong>9. Keyboard Typing Speed (WPM):</strong> Tracks how fast you are typing in Words Per Minute.</li>
        </ul>

        <h3>Link Sink Options (How should Allme visually change to show that stat?)</h3>
        <ul>
            <li><strong>0. None:</strong> No visual change.</li>
            <li><strong>1. App Size:</strong> Makes the orb get larger when the stat goes up.</li>
            <li><strong>2. App Color (Red -> Blue Shift):</strong> Shifts orb color from Red to Blue based on the stat level.</li>
            <li><strong>3. Glow Size:</strong> Makes the outer glow halo grow bigger when the stat goes up.</li>
            <li><strong>4. Glow Color (Blue -> Red Shift):</strong> Shifts glow halo color from Blue to Red based on workload.</li>
            <li><strong>5. App Opacity:</strong> Makes the orb more solid or see-through based on the stat.</li>
            <li><strong>6. Glow Opacity:</strong> Brightens or dims the glow halo based on workload.</li>
            <li><strong>7–9. Combined Targets:</strong> Simultaneously modulates both App and Glow size, color, or opacity.</li>
        </ul>

        <div class="page-break"></div>

        <h2>Part F: Sizing & Transparency Sliders</h2>
        <p>At the bottom of the menu, you will find 6 easy-to-use slider bars:</p>
        
        <table>
            <thead>
                <tr>
                    <th>Slider Name</th>
                    <th>What Moving the Slider Does</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>App Opacity</strong></td>
                    <td>Adjusts how solid or see-through the inner orb appears (10% transparent to 100% solid).</td>
                </tr>
                <tr>
                    <td><strong>Glow Opacity</strong></td>
                    <td>Adjusts how bright or faint the outer glowing light halo shines.</td>
                </tr>
                <tr>
                    <td><strong>Glow Size</strong></td>
                    <td>Makes the glowing light ring around Allme larger or smaller.</td>
                </tr>
                <tr>
                    <td><strong>Color Hue</strong></td>
                    <td>A smooth color wheel slider (0° to 360°) allowing you to pick any exact color tint.</td>
                </tr>
                <tr>
                    <td><strong>Breathing Speed</strong></td>
                    <td>Adjusts how fast or slow the breathing animation pulses.</td>
                </tr>
                <tr>
                    <td><strong>App Size</strong></td>
                    <td>Resizes the overall Allme orb from a compact small dot to a large desktop widget.</td>
                </tr>
            </tbody>
        </table>

        <!-- SECTION 5 -->
        <h1 class="section-header">5. The Futuristic System Health Dashboard</h1>
        <p>
            When you select <strong>🎛️ Futuristic Dashboard</strong> from the menu, a full diagnostic window opens. 
            This window is designed like a high-tech control panel that shows live graphs and numbers for your PC:
        </p>
        <ul>
            <li><strong>CPU Processor Graphs:</strong> Shows real-time percentage load across every core of your processor.</li>
            <li><strong>Graphics Card (GPU) Monitor:</strong> Displays graphics workload percentage, video RAM (VRAM) usage, and card temperature.</li>
            <li><strong>Memory (RAM) Gauge:</strong> Shows how many gigabytes of memory are being used by open programs.</li>
            <li><strong>Hard Drive & Network Activity:</strong> Displays live disk read/write speeds, internet upload/download speeds, and ping latency in milliseconds (ms).</li>
            <li><strong>Typing Speed (WPM) Meter:</strong> Shows your real-time typing speed in Words Per Minute as you type on your keyboard.</li>
        </ul>

        <!-- SECTION 6 -->
        <h1 class="section-header">6. Taking Screenshots & Recording Videos</h1>
        
        <h2>Taking Screenshots</h2>
        <p>
            Middle-clicking the outer sectors of Allme takes a full-screen snapshot picture. 
            The orb will briefly flash bright white to let you know the picture was taken. 
            Screenshots are automatically saved with timestamped filenames in your <strong>Pictures/Allme/Screenshots</strong> folder.
        </p>

        <h2>Recording Screen Videos</h2>
        <p>
            Middle-clicking the center core of Allme starts a high-definition video recording of your desktop monitor. 
            While recording, the outer border of Allme turns a bright red color and the center core displays a red square indicator. 
            Middle-click the center core again to stop recording. Videos are saved in your <strong>Pictures/Allme/Recordings</strong> folder.
        </p>

        <!-- SECTION 7 -->
        <h1 class="section-header">7. Saved File Locations & Troubleshooting Common Issues</h1>
        
        <h2>Where Files Are Saved on Your PC</h2>
        <table>
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Folder Location on Your PC</th>
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
                    <td><strong>Saved Settings</strong></td>
                    <td><code>C:/Users/[YourName]/AppData/Roaming/Allme/config.json</code></td>
                </tr>
                <tr>
                    <td><strong>Error & Crash Logs</strong></td>
                    <td><code>C:/Users/[YourName]/AppData/Local/Allme/Logs/allme_crash_report.txt</code></td>
                </tr>
            </tbody>
        </table>

        <h2>Troubleshooting & Frequently Asked Questions</h2>
        
        <div class="tip-box">
            <div class="tip-title">Question: What if Allme disappears or goes off the edge of my screen?</div>
            <strong>Answer:</strong> Simply restart Allme. Upon launching, Allme automatically checks your monitor boundaries. If it sees that it was saved off-screen, it instantly snaps back to the center of your screen.
        </div>

        <div class="tip-box">
            <div class="tip-title">Question: Why can't I drag Allme with my mouse?</div>
            <strong>Answer:</strong> Check if <em>Lock Position</em> or <em>Fly Mode</em> or <em>Clickthrough</em> is turned on. Press <span class="kbd">Shift</span> + <strong>Left Click</strong> on Allme to toggle position lock off.
        </div>

        <div class="warn-box">
            <div class="warn-title">Question: Why does a second instance of Allme close automatically?</div>
            <strong>Answer:</strong> Allme includes a Built-in Single Instance Guarantee. Only one Allme orb can run at a time to prevent duplicate system tray icons and audio driver conflicts. Launching Allme again cleanly closes the old instance.
        </div>

        <div class="footer">
            Allme Complete Layman's User Manual — Version 36<br>
            Designed for Simplicity & Maximum Desktop Productivity &copy; 2026
        </div>

    </body>
    </html>
    """

    app = QApplication(sys.argv)
    doc = QTextDocument()
    doc.setHtml(html)
    
    printer = QPrinter()
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName('AllmeD_v36_Comprehensive_User_Manual.pdf')
    printer.setResolution(300)
    
    doc.print_(printer)
    print("Ultra-Comprehensive Layman PDF User Manual created successfully at AllmeD_v36_Comprehensive_User_Manual.pdf")

if __name__ == '__main__':
    generate_manual()
