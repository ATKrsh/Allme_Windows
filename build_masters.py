import os
import sys
import subprocess

ALLME_FILE = "allme.py"

def build(exe_name, enable_dashboard):
    print(f"--- Building {exe_name} (Dashboard: {enable_dashboard}) ---")
    
    # 1. Modify allme.py to toggle ENABLE_DASHBOARD_BUILD
    with open(ALLME_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if enable_dashboard:
        content = content.replace("ENABLE_DASHBOARD_BUILD = False", "ENABLE_DASHBOARD_BUILD = True")
    else:
        content = content.replace("ENABLE_DASHBOARD_BUILD = True", "ENABLE_DASHBOARD_BUILD = False")
        
    with open(ALLME_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    # 2. Generate Spec File pointing directly to local allme.py
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['allme.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['soundcard', 'sounddevice', 'cffi', '_cffi_backend', 'pyaudio', 'numpy', 'mss', 'cv2', 'psutil'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['tkinter', 'unittest', 'pydoc', 'pynvml'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{exe_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{exe_name}',
)
"""
    temp_spec = f"{exe_name}.spec"
    with open(temp_spec, 'w', encoding='utf-8') as f:
        f.write(spec_content)
        
    # 3. Run PyInstaller
    print(f"Running pyinstaller {temp_spec}...")
    subprocess.run(["pyinstaller", "-y", temp_spec])
    print(f"Finished {exe_name}.\n")

if __name__ == "__main__":
    # Build the non-dashboard master (v37)
    build("Allme_v37", False)
    
    # Build the dashboard master (v37)
    build("AllMeD_v37", True)
    
    print("Done! Check the /dist folder for both executables.")
