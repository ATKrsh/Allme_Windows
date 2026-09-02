# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['e:\\workspace\\Allme\\allme.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['soundcard', 'sounddevice', 'cffi', '_cffi_backend', 'pyaudio', 'numpy', 'mss', 'cv2', 'psutil', 'pynvml'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'unittest', 'pydoc'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Allme_v36',
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
    name='Allme_v36',
)
