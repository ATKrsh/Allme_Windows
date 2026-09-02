# allme.py
# Allme — Master Desktop Widget combining ASwitch + captureME + Telemetry Suite
# Always-on-top, translucent circular widget with window/tab switching, screen capture, video recording & system telemetry.

import sys
import os
import io
import time
import math
import json
import socket
import collections
import threading
import subprocess
import base64
import winreg
import ctypes
import ctypes.wintypes

def get_system_accent_color(hex_format=True):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\DWM')
        val, _ = winreg.QueryValueEx(key, 'ColorizationColor')
        r = (val >> 16) & 255
        g = (val >> 8) & 255
        b = val & 255
        if hex_format: return f"#{r:02X}{g:02X}{b:02X}"
        return r, g, b
    except: pass
    return "#00E5FF" if hex_format else (0, 229, 255)
    
from urllib.parse import urlparse
from urllib.request import urlopen

# Flag to enable/disable Dashboard build. Set to True to build AllMeD with dashboard.
ENABLE_DASHBOARD_BUILD = True

# Force stdout/stderr to UTF-8
class _DummyWriter:
    def write(self, *a, **k): pass
    def flush(self, *a, **k): pass

if sys.stdout is None:
    sys.stdout = _DummyWriter()
else:
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

if sys.stderr is None:
    sys.stderr = _DummyWriter()
else:
    try:
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

# Single Instance Guarantee: Terminate previous running instance when a new instance launches
kernel32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32

def kill_previous_instances():
    """
    Terminates any previously running instance of Allme so only the newly launched instance runs.
    """
    import psutil
    current_pid = os.getpid()
    
    if getattr(sys, 'frozen', False):
        exe_name = os.path.basename(sys.executable)
        subprocess.run(f'taskkill /F /FI "PID ne {current_pid}" /IM "{exe_name}"', shell=True, capture_output=True)
        subprocess.run(f'taskkill /F /FI "PID ne {current_pid}" /IM "Allme*"', shell=True, capture_output=True)
    else:
        subprocess.run(f'wmic process where "name like \'%allme%\' and ProcessId != {current_pid}" call terminate', shell=True, capture_output=True)

    # 2. psutil backup iteration
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'exe']):
            try:
                pid = proc.info['pid']
                if pid == current_pid: continue
                pname = (proc.info['name'] or '').lower()
                exe_path = (proc.info['exe'] or '').lower()
                cmd = proc.info['cmdline'] or []
                cmd_str = ' '.join(cmd).lower()
                
                if 'allme' in pname or 'allme' in exe_path or 'allme.py' in cmd_str:
                    try:
                        proc.kill()
                    except Exception:
                        subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True)
            except (psutil.NoSuchProcess, psutil.AccessDenied): pass
    except Exception: pass

# Crash Logging & Reporting Subsystem
LOG_DIR = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Allme", "Logs")
os.makedirs(LOG_DIR, exist_ok=True)
CRASH_LOG_FILE = os.path.join(LOG_DIR, "allme_crash_report.txt")

def log_crash_report(exc_type, exc_value, exc_tb):
    """
    Writes a dual Layman + Technical crash log whenever an unhandled exception occurs.
    """
    import traceback, datetime
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    layman_summary = (
        "================================================================================\n"
        "                     ALLME CRASH REPORT (LAYMAN SUMMARY)                         \n"
        "================================================================================\n"
        f"Time of Crash : {now_str}\n"
        f"Error Summary : {exc_type.__name__ if exc_type else 'Unknown Error'}\n"
        f"Details       : {str(exc_value)}\n\n"
        "What happened:\n"
        "  Allme encountered an unexpected error and had to close to prevent instability.\n"
        "  Your configuration and saved captures are completely safe.\n\n"
        "How to fix:\n"
        "  1. Relaunch Allme.\n"
        "  2. If the issue repeats, share this log file with the developer.\n"
        "--------------------------------------------------------------------------------\n\n"
    )

    tech_details = (
        "================================================================================\n"
        "                   TECHNICAL DIAGNOSTIC LOG (FOR DEVELOPERS)                    \n"
        "================================================================================\n"
        f"Python Version : {sys.version}\n"
        f"OS             : {sys.platform}\n"
        "Full Traceback :\n" +
        "".join(traceback.format_exception(exc_type, exc_value, exc_tb)) +
        "================================================================================\n"
    )

    try:
        with open(CRASH_LOG_FILE, "w", encoding="utf-8") as f:
            f.write(layman_summary + tech_details)
    except Exception:
        pass

def global_exception_handler(exc_type, exc_value, exc_tb):
    log_crash_report(exc_type, exc_value, exc_tb)
    sys.__excepthook__(exc_type, exc_value, exc_tb)

sys.excepthook = global_exception_handler

try:
    _con = ctypes.windll.kernel32.GetConsoleWindow()
    if _con:
        ctypes.windll.user32.ShowWindow(_con, 0)
except Exception:
    pass

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSystemTrayIcon,
    QMenu, QAction, QSlider, QWidgetAction, QLabel, QActionGroup,
    QDialog, QGridLayout, QPushButton, QComboBox, QCheckBox, QGroupBox
)
from PyQt5.QtCore import (
    Qt, QPoint, QPointF, QRectF, QTimer, pyqtSignal, QEvent
)
from PyQt5.QtGui import (
    QPainter, QColor, QPen, QBrush, QIcon, QPixmap, QCursor, QRadialGradient, QLinearGradient
)
from PyQt5.QtWinExtras import QtWin

import mss
import mss.tools
import cv2
import numpy as np
import psutil

try:
    import pynvml
    pynvml.nvmlInit()
    HAS_NVML = True
except Exception:
    HAS_NVML = False

try:
    import pyaudio
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False

# =============================================================================
#  Paths & Configuration Setup (from captureME)
# =============================================================================
PICTURES_DIR = os.path.join(os.path.expanduser("~"), "Pictures")
APP_DATA_DIR = os.path.join(os.getenv('APPDATA', os.path.expanduser('~')), "Allme")
os.makedirs(APP_DATA_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(APP_DATA_DIR, "config.json")

CAPTURES_DIR = os.path.join(PICTURES_DIR, "Allme")
os.makedirs(CAPTURES_DIR, exist_ok=True)
os.makedirs(os.path.join(CAPTURES_DIR, "Screenshots"), exist_ok=True)
os.makedirs(os.path.join(CAPTURES_DIR, "Recordings"), exist_ok=True)

REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "Allme"

DEFAULT_CONFIG = {
    "opacity": 0.9,
    "glow_opacity": 0.9,
    "glow_size_pct": 50,
    "hue": 190,
    "color_hue_target": "both",     # "both", "app", "glow"
    "audio_effect": "pulsing_aura", # "pulsing_aura", "equalizer_ring", "waveform_orbit", "frequency_ripple", "particle_spark", "chroma_pulse"
    "audio_visual_mode": "both",    # "both", "volume", "frequency"
    "base_glow_enabled": True,
    "glow_enabled": True,
    "size_pct": 50,
    "always_on_top": True,
    "lock_position": False,
    "clickthrough": False,
    "clickthrough_mode": "all",      # "all", "left", "right", "middle"
    "start_with_windows": False,
    "breathing": False,
    "breathing_target": "both",     # "both", "app", "glow"
    "breathing_speed": 50,          # 1 to 100
    "mouse_movement_enabled": True,
    "mouse_movement_target": "both",# "both", "app", "glow"
    "pos_x": -1,
    "pos_y": -1
}

def load_config():
    cfg = DEFAULT_CONFIG.copy()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                cfg.update(data)
        except Exception:
            pass
    return cfg

def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        pass

def set_startup(enable):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_ALL_ACCESS)
            if enable:
                exe_path = f'"{sys.executable}"'
                if getattr(sys, 'frozen', False):
                    exe_path = f'"{os.path.abspath(sys.argv[0])}"'
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
            else:
                try: winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError: pass
            winreg.CloseKey(key)
        except Exception as e:
            print("Registry error:", e)

def check_startup():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        winreg.QueryValueEx(key, APP_NAME)
        winreg.CloseKey(key)
        return True
    except Exception: return False

# =============================================================================
#  Persistent QMenu Subclass (Stays open on action clicks until click outside)
# =============================================================================
class PersistentMenu(QMenu):
    def __init__(self, title="", parent=None):
        if title:
            super().__init__(title, parent)
        else:
            super().__init__(parent)

    def mouseReleaseEvent(self, event):
        action = self.actionAt(event.pos())
        if action and action.isCheckable():
            action.trigger()
            self.update()
            event.accept()
        else:
            super().mouseReleaseEvent(event)

# =============================================================================
#  Win32 Declarations & Hooks
# =============================================================================
user32   = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
shell32  = ctypes.windll.shell32

shell32.ExtractIconW.argtypes = [ctypes.wintypes.HINSTANCE, ctypes.c_wchar_p, ctypes.c_int]
shell32.ExtractIconW.restype  = ctypes.wintypes.HICON
if hasattr(user32, 'DestroyIcon'):
    user32.DestroyIcon.argtypes = [ctypes.wintypes.HICON]
    user32.DestroyIcon.restype  = ctypes.wintypes.BOOL

kernel32.OpenProcess.argtypes  = [ctypes.c_ulong, ctypes.c_bool, ctypes.c_ulong]
kernel32.OpenProcess.restype   = ctypes.wintypes.HANDLE
kernel32.CloseHandle.argtypes  = [ctypes.wintypes.HANDLE]
kernel32.CloseHandle.restype   = ctypes.c_bool
kernel32.QueryFullProcessImageNameW.argtypes = [
    ctypes.wintypes.HANDLE, ctypes.c_ulong,
    ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_ulong),
]
kernel32.QueryFullProcessImageNameW.restype = ctypes.c_bool
kernel32.GetModuleHandleW.argtypes = [ctypes.c_wchar_p]
kernel32.GetModuleHandleW.restype  = ctypes.wintypes.HMODULE

user32.GetWindowThreadProcessId.argtypes = [ctypes.wintypes.HWND, ctypes.POINTER(ctypes.c_ulong)]
user32.GetWindowThreadProcessId.restype  = ctypes.c_ulong

IsWindowVisible = user32.IsWindowVisible
IsWindowVisible.argtypes = [ctypes.wintypes.HWND]
IsWindowVisible.restype  = ctypes.wintypes.BOOL

GetWindowTextW = user32.GetWindowTextW
GetWindowTextW.argtypes = [ctypes.wintypes.HWND, ctypes.c_wchar_p, ctypes.c_int]
GetWindowTextW.restype  = ctypes.c_int

GetWindowTextLengthW = user32.GetWindowTextLengthW
GetWindowTextLengthW.argtypes = [ctypes.wintypes.HWND]
GetWindowTextLengthW.restype  = ctypes.c_int

GetParent = user32.GetParent
GetParent.argtypes = [ctypes.wintypes.HWND]
GetParent.restype  = ctypes.wintypes.HWND

user32.GetClassNameW.argtypes = [ctypes.wintypes.HWND, ctypes.c_wchar_p, ctypes.c_int]
user32.GetClassNameW.restype  = ctypes.c_int

GWL_EXSTYLE      = -20
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_LAYERED    = 0x00080000
WS_EX_NOACTIVATE = 0x08000000
WS_EX_TRANSPARENT= 0x00000020
LWA_ALPHA        = 0x00000002
SW_RESTORE       = 9
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

if hasattr(user32, "GetWindowLongPtrW"):
    GetWindowLongW = user32.GetWindowLongPtrW
    GetWindowLongW.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
    GetWindowLongW.restype  = ctypes.c_ssize_t
    SetWindowLongW = user32.SetWindowLongPtrW
    SetWindowLongW.argtypes = [ctypes.wintypes.HWND, ctypes.c_int, ctypes.c_ssize_t]
    SetWindowLongW.restype  = ctypes.c_ssize_t
else:
    GetWindowLongW = user32.GetWindowLongW
    GetWindowLongW.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
    GetWindowLongW.restype  = ctypes.c_long
    SetWindowLongW = user32.SetWindowLongW
    SetWindowLongW.argtypes = [ctypes.wintypes.HWND, ctypes.c_int, ctypes.c_long]
    SetWindowLongW.restype  = ctypes.c_long

SetForegroundWindow = user32.SetForegroundWindow
SetForegroundWindow.argtypes = [ctypes.wintypes.HWND]
SetForegroundWindow.restype  = ctypes.wintypes.BOOL

ShowWindow = user32.ShowWindow
ShowWindow.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
ShowWindow.restype  = ctypes.wintypes.BOOL

GetForegroundWindow = user32.GetForegroundWindow
GetForegroundWindow.argtypes = []
GetForegroundWindow.restype  = ctypes.wintypes.HWND

IsWindow = user32.IsWindow
IsWindow.argtypes = [ctypes.wintypes.HWND]
IsWindow.restype  = ctypes.wintypes.BOOL

IsIconic = user32.IsIconic
IsIconic.argtypes = [ctypes.wintypes.HWND]
IsIconic.restype  = ctypes.wintypes.BOOL

SetLayeredWindowAttributes = user32.SetLayeredWindowAttributes
SetLayeredWindowAttributes.argtypes = [ctypes.wintypes.HWND, ctypes.wintypes.COLORREF,
                                       ctypes.c_byte, ctypes.wintypes.DWORD]
SetLayeredWindowAttributes.restype  = ctypes.wintypes.BOOL

SetWindowPos = user32.SetWindowPos
SetWindowPos.argtypes = [ctypes.wintypes.HWND, ctypes.wintypes.HWND,
                         ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
SetWindowPos.restype  = ctypes.wintypes.BOOL

EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
EnumWindows = user32.EnumWindows
EnumWindows.argtypes = [EnumWindowsProc, ctypes.wintypes.LPARAM]
EnumWindows.restype  = ctypes.wintypes.BOOL

user32.keybd_event.argtypes = [ctypes.c_byte, ctypes.c_byte, ctypes.c_ulong, ctypes.c_void_p]
user32.keybd_event.restype  = None

VK_CONTROL      = 0x11
VK_SHIFT        = 0x10
VK_TAB          = 0x09
VK_PRIOR        = 0x21
VK_NEXT         = 0x22
KEYEVENTF_KEYUP = 0x0002

class SystemPowerStatus(ctypes.Structure):
    _fields_ = [
        ('ACLineStatus', ctypes.c_byte),
        ('BatteryFlag', ctypes.c_byte),
        ('BatteryLifePercent', ctypes.c_byte),
        ('SystemStatusFlag', ctypes.c_byte),
        ('BatteryLifeTime', ctypes.c_ulong),
        ('BatteryFullLifeTime', ctypes.c_ulong)
    ]

HOOKPROC = ctypes.WINFUNCTYPE(
    ctypes.c_ssize_t, ctypes.c_int,
    ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM
)

user32.SetWindowsHookExW.argtypes = [ctypes.c_int, HOOKPROC, ctypes.wintypes.HINSTANCE, ctypes.wintypes.DWORD]
user32.SetWindowsHookExW.restype  = ctypes.c_void_p

user32.UnhookWindowsHookEx.argtypes = [ctypes.c_void_p]
user32.UnhookWindowsHookEx.restype  = ctypes.c_bool

user32.CallNextHookEx.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM]
user32.CallNextHookEx.restype  = ctypes.c_ssize_t

class MouseHook:
    def __init__(self, signal_emitter):
        self.signal_emitter = signal_emitter
        self.hook_id = None
        self._c_callback = HOOKPROC(self._hook_callback)

    def install(self):
        try:
            self.hook_id = user32.SetWindowsHookExW(14, self._c_callback, kernel32.GetModuleHandleW(None), 0)
        except Exception:
            pass

    def uninstall(self):
        if self.hook_id:
            try:
                user32.UnhookWindowsHookEx(self.hook_id)
            except Exception:
                pass
            self.hook_id = None

    def _hook_callback(self, nCode, wParam, lParam):
        if nCode >= 0 and wParam == 0x0207:
            try:
                self.signal_emitter()
            except Exception:
                pass
        return user32.CallNextHookEx(self.hook_id, nCode, wParam, lParam)

class KeyboardHook:
    def __init__(self, callback):
        self.callback = callback
        self.hook_id = None
        self._c_callback = HOOKPROC(self._hook_callback)

    def install(self):
        try:
            self.hook_id = user32.SetWindowsHookExW(13, self._c_callback, kernel32.GetModuleHandleW(None), 0)
        except Exception:
            pass

    def uninstall(self):
        if self.hook_id:
            try:
                user32.UnhookWindowsHookEx(self.hook_id)
            except Exception:
                pass
            self.hook_id = None

    def _hook_callback(self, nCode, wParam, lParam):
        if nCode >= 0 and wParam in (0x0100, 0x0104):
            try:
                self.callback()
            except Exception:
                pass
        return user32.CallNextHookEx(self.hook_id, nCode, wParam, lParam)

# =============================================================================
#  Audio Monitoring Thread (WASAPI Loopback + soundcard + sounddevice)
# =============================================================================
class AudioMonitor(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.current_volume = 0.0      # RMS Volume Amplitude -> BG Glow Intensity
        self.current_frequency = 0.0   # Dominant Frequency (Hz) -> BG Glow Radius / Size
        self.running = True

    def run(self):
        sr = 44100
        blocksize = 128

        def process_signal(signal):
            if len(signal) == 0: return
            # 1. Instantaneous RMS Volume Amplitude calculation
            rms = np.sqrt(np.mean(signal**2))
            target_vol = min(1.0, float(rms * 14.0))
            if target_vol > self.current_volume:
                self.current_volume = target_vol
            else:
                self.current_volume += (target_vol - self.current_volume) * 0.45

            # 2. FFT Spectral Analysis for Dominant Frequency
            fft_data = np.abs(np.fft.rfft(signal * np.hanning(len(signal))))
            freqs = np.fft.rfftfreq(len(signal), 1.0 / sr)
            
            valid_idx = np.where(freqs >= 40.0)[0]
            if len(valid_idx) > 0 and np.max(fft_data[valid_idx]) > 0.0002:
                peak_idx = valid_idx[np.argmax(fft_data[valid_idx])]
                dom_freq = freqs[peak_idx]
                norm_freq = min(1.0, max(0.0, (dom_freq - 50.0) / 3950.0))
            else:
                norm_freq = 0.0

            if norm_freq > self.current_frequency:
                self.current_frequency = norm_freq
            else:
                self.current_frequency += (norm_freq - self.current_frequency) * 0.40

        # Primary Approach: Native WASAPI Desktop Loopback via soundcard
        try:
            import soundcard as sc
            default_spk = sc.default_speaker()
            loopback_mic = sc.get_microphone(id=str(default_spk.name), include_loopback=True)
            with loopback_mic.recorder(samplerate=sr, blocksize=blocksize) as recorder:
                while self.running:
                    data = recorder.record(numframes=blocksize)
                    signal = data[:, 0] if data.ndim > 1 else data
                    process_signal(signal)
            return
        except Exception:
            pass

        # Secondary Approach: sounddevice input stream
        try:
            import sounddevice as sd
            def sd_callback(indata, frames, time_info, status):
                if not self.running: return
                process_signal(indata[:, 0])

            input_device = None
            devices = sd.query_devices()
            for idx, dev in enumerate(devices):
                if dev.get('max_input_channels', 0) > 0:
                    name_lower = dev.get('name', '').lower()
                    if 'stereo mix' in name_lower or 'loopback' in name_lower or 'what u hear' in name_lower:
                        input_device = idx; break
            if input_device is None:
                default_dev = sd.default.device[0]
                if default_dev != -1 and default_dev is not None:
                    input_device = default_dev

            if input_device is not None:
                with sd.InputStream(device=input_device, callback=sd_callback, channels=1, samplerate=sr, blocksize=2048):
                    while self.running:
                        time.sleep(0.02)
                return
        except Exception:
            pass

        # Tertiary Fallback: PyAudio if available
        if HAS_PYAUDIO:
            try:
                p = pyaudio.PyAudio()
                stream = p.open(format=pyaudio.paInt16, channels=1, rate=22050, input=True, frames_per_buffer=1024)
                while self.running:
                    data = stream.read(1024, exception_on_overflow=False)
                    audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
                    process_signal(audio_data)
                stream.stop_stream(); stream.close(); p.terminate()
                return
            except Exception: pass

        while self.running:
            time.sleep(0.1)

# =============================================================================
#  Thread-Safe Telemetry Sampling Thread (10 Channels)
# =============================================================================
class TelemetryMonitor(threading.Thread):
    def __init__(self, widget):
        super().__init__(daemon=True)
        self._w = widget
        self.running = True
        self.lock = threading.Lock()
        self.key_timestamps = collections.deque()
        self.mouse_timestamps = collections.deque()
        self.last_disk_stats = {}
        self.last_net_stats = None
        self.last_sample_time = time.time()
        self.current_ping = 0.0
        self.current_val = 0.0

    def record_key(self):
        with self.lock:
            self.key_timestamps.append(time.time())

    def record_mouse(self):
        with self.lock:
            self.mouse_timestamps.append(time.time())

    def get_sample(self):
        with self.lock:
            return self.current_val

    def run(self):
        while self.running:
            try:
                now = time.time()
                dt = max(0.2, now - self.last_sample_time)
                self.last_sample_time = now

                cutoff = now - 10.0
                with self.lock:
                    while self.key_timestamps and self.key_timestamps[0] < cutoff:
                        self.key_timestamps.popleft()
                    while self.mouse_timestamps and self.mouse_timestamps[0] < cutoff:
                        self.mouse_timestamps.popleft()
                    num_keys = len(self.key_timestamps)
                    num_mouse = len(self.mouse_timestamps)

                # 1. Normal Breathing (slow, calm human sine rhythm ~0.25 Hz)
                sine_val = (math.sin(now * 1.5) + 1.0) / 2.0 if self._w.config.get("breathing", False) else 0.0

                # 2. CPU Freq
                try:
                    freq = psutil.cpu_freq()
                    cpu_freq_val = min(1.0, max(0.0, freq.current / (freq.max or 4000.0))) if freq else 0.5
                except Exception: cpu_freq_val = 0.5

                # 3. CPU Usage
                try: cpu_usage_val = psutil.cpu_percent() / 100.0
                except Exception: cpu_usage_val = 0.0

                # 4. HDD Activity (Enhanced sensitivity: 5MB/s max scale for clear visual response)
                hdd_val = 0.0
                try:
                    drive_choice = self._w.config.get("hdd_drive", "All")
                    io_mode = self._w.config.get("hdd_mode", "both")
                    disks = psutil.disk_io_counters(perdisk=True)

                    read_bytes = 0; write_bytes = 0
                    if drive_choice == "All" or drive_choice not in disks:
                        for d_stat in disks.values():
                            read_bytes += d_stat.read_bytes
                            write_bytes += d_stat.write_bytes
                    else:
                        d_stat = disks[drive_choice]
                        read_bytes = d_stat.read_bytes
                        write_bytes = d_stat.write_bytes

                    prev = self.last_disk_stats.get(drive_choice, (read_bytes, write_bytes))
                    d_read = max(0, read_bytes - prev[0]) / dt
                    d_write = max(0, write_bytes - prev[1]) / dt
                    self.last_disk_stats[drive_choice] = (read_bytes, write_bytes)

                    if io_mode == "read": total_b = d_read
                    elif io_mode == "write": total_b = d_write
                    else: total_b = d_read + d_write

                    hdd_val = min(1.0, total_b / 5000000.0)  # 5 MB/s
                except Exception: pass

                # 5. Memory Usage (Sensitive scaling across 0% to 100%)
                try:
                    mem = psutil.virtual_memory().percent
                    mem_val = min(1.0, max(0.0, mem / 100.0))
                except Exception: mem_val = 0.5

                # 6. Ethernet & Ping (Enhanced sensitivity: 1MB/s max scale)
                net_val = 0.0
                net_mode = self._w.config.get("net_mode", "both")
                try:
                    net_io = psutil.net_io_counters()
                    if self.last_net_stats:
                        d_sent = max(0, net_io.bytes_sent - self.last_net_stats[0]) / dt
                        d_recv = max(0, net_io.bytes_recv - self.last_net_stats[1]) / dt
                        if net_mode == "upload": b_spd = d_sent
                        elif net_mode == "download": b_spd = d_recv
                        elif net_mode == "ping": b_spd = 0
                        else: b_spd = d_sent + d_recv
                        net_val = min(1.0, b_spd / 1000000.0) # 1 MB/s
                    self.last_net_stats = (net_io.bytes_sent, net_io.bytes_recv)
                except Exception: pass

                if net_mode == "ping":
                    try:
                        t0 = time.time()
                        s = socket.create_connection(("8.8.8.8", 53), timeout=0.8)
                        s.close()
                        lat = (time.time() - t0) * 1000.0
                        self.current_ping += (lat - self.current_ping) * 0.3
                    except Exception: pass
                    net_val = min(1.0, max(0.0, self.current_ping / 200.0))

                # 7. GPU Usage
                gpu_val = 0.0
                gpu_choice = self._w.config.get("gpu_choice", "gpu0")
                if HAS_NVML:
                    try:
                        count = pynvml.nvmlDeviceGetCount()
                        if count > 0:
                            if gpu_choice == "gpu1" and count > 1: idx = 1
                            elif gpu_choice == "max":
                                idx = max(range(count), key=lambda i: pynvml.nvmlDeviceGetUtilizationRates(pynvml.nvmlDeviceGetHandleByIndex(i)).gpu)
                            else: idx = 0
                            h = pynvml.nvmlDeviceGetHandleByIndex(idx)
                            gpu_val = pynvml.nvmlDeviceGetUtilizationRates(h).gpu / 100.0
                    except Exception: pass

                # 8. System Power Usage
                power_val = 0.5
                try:
                    sps = SystemPowerStatus()
                    kernel32.GetSystemPowerStatus(ctypes.byref(sps))
                    if sps.BatteryLifePercent != 255 and sps.BatteryLifePercent != -1:
                        power_val = sps.BatteryLifePercent / 100.0
                    else:
                        power_val = 1.0 if sps.ACLineStatus == 1 else 0.5
                except Exception: pass

                # 9. Mouse Activity (Real-time movement velocity + click rate)
                mouse_val = min(1.0, (num_mouse / 20.0) * 0.4 + self._w.smooth_accel * 0.6)

                # 10. Keyboard Typing Speed (WPM)
                kb_val = min(1.0, (num_keys * 6) / 300.0)

                metrics = {
                    "breathing": sine_val,
                    "cpu_freq": cpu_freq_val,
                    "cpu_usage": cpu_usage_val,
                    "hdd": hdd_val,
                    "memory": mem_val,
                    "ethernet": net_val,
                    "gpu": gpu_val,
                    "power": power_val,
                    "mouse": mouse_val,
                    "keyboard": kb_val
                }

                sel_source = self._w.config.get("telemetry_source", "cpu_usage")
                sample_val = metrics.get(sel_source, 0.0)

                with self.lock:
                    self.current_val += (sample_val - self.current_val) * 0.25

            except Exception: pass
            time.sleep(0.15)

# =============================================================================
#  Video Recorder Thread (from captureME)
# =============================================================================
class VideoRecorder:
    def __init__(self):
        self.recording = False
        self.thread = None
        self.output_filepath = ""

    def start_recording(self):
        if self.recording:
            return
        self.recording = True
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.output_filepath = os.path.join(CAPTURES_DIR, "Recordings", f"recording_{timestamp}.mp4")
        self.thread = threading.Thread(target=self._record_loop, daemon=True)
        self.thread.start()

    def stop_recording(self):
        self.recording = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)

    def _record_loop(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = None
        fps = 20.0
        frame_time = 1.0 / fps

        with mss.mss() as sct:
            mon = sct.monitors[0]
            width = mon["width"]
            height = mon["height"]
            out = cv2.VideoWriter(self.output_filepath, fourcc, fps, (width, height))

            while self.recording:
                start = time.time()
                img = sct.grab(mon)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                out.write(frame)
                elapsed = time.time() - start
                sleep_dur = frame_time - elapsed
                if sleep_dur > 0:
                    time.sleep(sleep_dur)

            if out:
                out.release()

# =============================================================================
#  Favicon Manager (from ASwitch)
# =============================================================================
class FaviconManager:
    def __init__(self):
        self._cache = {}
        self._lock  = threading.Lock()
        self._pending = set()
        self._result_domain = None
        self._result_data   = None
        self._result_ready  = False

    def request(self, hwnd):
        t = threading.Thread(target=self._worker, args=(int(hwnd),), daemon=True)
        t.start()

    def poll_result(self):
        with self._lock:
            if self._result_ready:
                self._result_ready = False
                return (self._result_domain, self._result_data)
        return None

    def _worker(self, hwnd):
        try:
            raw = self._get_browser_url(hwnd)
            if not raw: return
            domain = self._parse_domain(raw)
            if not domain: return

            with self._lock:
                if domain in self._cache:
                    self._result_domain = domain
                    self._result_data   = self._cache[domain]
                    self._result_ready  = True
                    return
                if domain in self._pending: return
                self._pending.add(domain)

            try:
                url = f"https://www.google.com/s2/favicons?sz=64&domain={domain}"
                data = urlopen(url, timeout=4).read()
                with self._lock:
                    self._cache[domain] = data
                    self._pending.discard(domain)
                    self._result_domain = domain
                    self._result_data   = data
                    self._result_ready  = True
            except Exception:
                with self._lock:
                    self._pending.discard(domain)
        except Exception:
            pass

    def _parse_domain(self, raw):
        url = raw.strip()
        if not url: return None
        if '://' not in url: url = 'https://' + url
        try:
            p = urlparse(url)
            d = p.netloc or p.path.split('/')[0]
            d = d.split(':')[0]
            if '.' in d: return d
        except Exception: pass
        return None

    def _get_browser_url(self, hwnd):
        try:
            ps = (
                "$ErrorActionPreference='SilentlyContinue';"
                "Add-Type -AssemblyName UIAutomationClient;"
                f"$r=[System.Windows.Automation.AutomationElement]::FromHandle({hwnd});"
                "$c=New-Object System.Windows.Automation.PropertyCondition("
                "[System.Windows.Automation.AutomationElement]::ControlTypeProperty,"
                "[System.Windows.Automation.ControlType]::Edit);"
                "$all=$r.FindAll([System.Windows.Automation.TreeScope]::Descendants,$c);"
                "$best='';"
                "foreach($e in $all){"
                "try{$n=$e.Current.Name;"
                "$vp=$e.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern);"
                "$v=$vp.Current.Value;"
                "if($v){"
                "if($n -match 'address|url|location'){$v;exit}"
                "if(-not $best -and $v -match '[\\w.-]+\\.[a-zA-Z]{2,}'){$best=$v}"
                "}}catch{}};"
                "if($best){$best}"
            )
            r = subprocess.run(
                ['powershell', '-NoProfile', '-NonInteractive', '-Command', ps],
                capture_output=True, text=True, timeout=4,
                creationflags=0x08000000
            )
            return r.stdout.strip() if r.stdout else None
        except Exception:
            return None

# =============================================================================
#  Window & Browser Switching Logic
# =============================================================================
def get_window_title(hwnd):
    length = GetWindowTextLengthW(hwnd)
    if length == 0: return ""
    buf = ctypes.create_unicode_buffer(length + 1)
    GetWindowTextW(hwnd, buf, length + 1)
    return buf.value.strip()

def get_window_icon(hwnd):
    if not hwnd or not IsWindow(hwnd): return None
    try:
        pid = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if pid.value:
            h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value)
            if h:
                try:
                    buf = ctypes.create_unicode_buffer(512)
                    size = ctypes.c_ulong(512)
                    if kernel32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size)):
                        hicon = shell32.ExtractIconW(0, buf.value, 0)
                        if hicon and getattr(hicon, 'value', 0) > 1:
                            px = QtWin.fromHICON(hicon)
                            user32.DestroyIcon(hicon)
                            if not px.isNull(): return px
                finally:
                    kernel32.CloseHandle(h)
    except Exception: pass
    return None

def is_user_application(hwnd):
    if not IsWindow(hwnd) or not IsWindowVisible(hwnd): return False
    title = get_window_title(hwnd)
    if not title or GetParent(hwnd): return False
    ex = GetWindowLongW(hwnd, GWL_EXSTYLE)
    if ex & WS_EX_TOOLWINDOW: return False
    ignored = ["Program Manager", "Start", "Settings", "Cortana",
               "Windows Shell Experience Host", "Microsoft Text Input Application",
               "Allme", "ASwitch", "captureME"]
    return title not in ignored

def get_user_windows():
    wins = []
    def cb(hwnd, _lp):
        if is_user_application(hwnd): wins.append(hwnd)
        return True
    EnumWindows(EnumWindowsProc(cb), 0)
    return wins

def get_active_window_id():
    hwnd = GetForegroundWindow()
    if hwnd and is_user_application(hwnd): return hwnd
    return None

def switch_to_window(wid):
    if IsIconic(wid): ShowWindow(wid, SW_RESTORE)
    SetForegroundWindow(wid)
    return True

def is_valid_window(wid):
    return bool(IsWindow(wid))

BROWSER_CLASSES = {'Chrome_WidgetWin_1', 'MozillaWindowClass', 'IEFrame'}
BROWSER_KEYWORDS = {'chrome', 'firefox', 'edge', 'brave', 'opera', 'vivaldi', 'browser', 'safari', 'arc', 'tor'}
BROWSER_PROCS = frozenset(['chrome.exe', 'firefox.exe', 'msedge.exe', 'brave.exe', 'opera.exe', 'vivaldi.exe', 'arc.exe'])

def _proc_name(hwnd):
    try:
        pid = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if not pid.value: return ''
        h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value)
        if not h: return ''
        buf = ctypes.create_unicode_buffer(260)
        size = ctypes.c_ulong(260)
        kernel32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size))
        kernel32.CloseHandle(h)
        return os.path.basename(buf.value).lower()
    except Exception: return ''

def is_browser(hwnd):
    if not hwnd or not IsWindow(hwnd): return False
    proc = _proc_name(hwnd)
    if not proc: return False
    if proc in BROWSER_PROCS: return True
    buf = ctypes.create_unicode_buffer(260)
    user32.GetClassNameW(hwnd, buf, 260)
    cls = buf.value.strip()
    return cls in BROWSER_CLASSES and any(kw in proc for kw in BROWSER_KEYWORDS)

def send_ctrl_pageup():
    user32.keybd_event(VK_CONTROL, 0, 0, 0); time.sleep(0.02)
    user32.keybd_event(VK_PRIOR, 0, 0, 0);   time.sleep(0.02)
    user32.keybd_event(VK_PRIOR, 0, KEYEVENTF_KEYUP, 0); time.sleep(0.02)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)

def send_ctrl_pagedown():
    user32.keybd_event(VK_CONTROL, 0, 0, 0); time.sleep(0.02)
    user32.keybd_event(VK_NEXT, 0, 0, 0);    time.sleep(0.02)
    user32.keybd_event(VK_NEXT, 0, KEYEVENTF_KEYUP, 0); time.sleep(0.02)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)

def lerp_color(c1, c2, t):
    return QColor(
        int(c1.red()   + (c2.red()   - c1.red())   * t),
        int(c1.green() + (c2.green() - c1.green()) * t),
        int(c1.blue()  + (c2.blue()  - c1.blue())  * t),
        int(c1.alpha() + (c2.alpha() - c1.alpha()) * t),
    )

# =============================================================================
#  Dashboard UI
# =============================================================================
class DashboardTitle(QWidget):
    def __init__(self, main_app, text, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.text = text
        self.setFixedHeight(60)
        self.phase = 0.0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(30)
        
    def _tick(self):
        self.phase += 0.2
        self.update()
        
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        link_accent = self.main_app.config.get("link_system_accent", False)
        if link_accent:
            r, g, b = get_system_accent_color(hex_format=False)
            base_col = QColor(r, g, b)
        else:
            base_col = QColor(0, 229, 255)

        p.setPen(Qt.NoPen)
        bg_col = QColor(base_col)
        bg_col.setAlphaF(0.10) # 10% opacity cyan/accent
        p.setBrush(bg_col)
        
        vol = 0.5
        freq = 0.5
        if hasattr(self.main_app, 'audio_mon'):
            vol = getattr(self.main_app.audio_mon, 'current_volume', 0.5)
            freq = getattr(self.main_app.audio_mon, 'current_frequency', 0.5)
            
        import math
        from PyQt5.QtGui import QPolygonF
        
        points = 60
        # Laser Wave 1
        poly = QPolygonF()
        poly.append(QPointF(0, h))
        for i in range(points + 1):
            x = (i / points) * w
            y_off = math.sin(x * 0.03 + self.phase) * (4 + vol * 20) + math.sin(x * 0.08 - self.phase) * (2 + freq * 10)
            poly.append(QPointF(x, (h / 2) + y_off))
        poly.append(QPointF(w, h))
        p.drawPolygon(poly)
        
        # Laser Wave 2
        poly2 = QPolygonF()
        poly2.append(QPointF(0, h))
        for i in range(points + 1):
            x = (i / points) * w
            y_off = math.cos(x * 0.04 - self.phase*1.5) * (3 + vol * 15) + math.sin(x * 0.1 + self.phase*0.8) * (2 + freq * 12)
            poly2.append(QPointF(x, (h / 2) + y_off + 10))
        poly2.append(QPointF(w, h))
        p.setBrush(QColor(base_col.red(), base_col.green(), base_col.blue(), int(255 * 0.05)))
        p.drawPolygon(poly2)
        
        # Data Bars
        p.setPen(QColor(base_col.red(), base_col.green(), base_col.blue(), int(255 * 0.20)))
        p.setBrush(Qt.NoBrush)
        num_bars = 30
        for i in range(num_bars):
            bar_x = (i / num_bars) * w
            bar_h = (math.sin(i * 0.5 + self.phase*2) + 1.0) * (5 + freq * 25)
            p.drawLine(QPointF(bar_x, h), QPointF(bar_x, h - bar_h))
        
        p.setPen(base_col)
        font = p.font()
        font.setPixelSize(26)
        font.setBold(True)
        p.setFont(font)
        p.drawText(self.rect(), Qt.AlignCenter, self.text)

class DashboardWindow(QDialog):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("AllMeD Dashboard")
        self.resize(850, 600)
        accent_hex = "#00E5FF"
        if self.main_app.config.get("link_system_accent", False):
            accent_hex = get_system_accent_color(hex_format=True)
            
        self.setStyleSheet(f"""
            QDialog {{ background-color: #121212; color: #E0E0E0; }}
            QGroupBox {{ border: 1px solid #333; border-radius: 8px; margin-top: 20px; font-weight: bold; color: {accent_hex}; padding: 15px 10px 10px 10px; }}
            QGroupBox::title {{ subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }}
            QLabel {{ color: #CCCCCC; font-weight: bold; }}
            QCheckBox {{ color: #CCCCCC; spacing: 10px; font-weight: bold; }}
            QCheckBox::indicator {{ width: 40px; height: 20px; border-radius: 10px; }}
            QCheckBox::indicator:unchecked {{ background-color: #333; }}
            QCheckBox::indicator:checked {{ background-color: {accent_hex}; }}
            QSlider::groove:horizontal {{ height: 6px; background: #333; border-radius: 3px; }}
            QSlider::handle:horizontal {{ background: {accent_hex}; width: 14px; margin: -4px 0; border-radius: 7px; }}
            QComboBox {{ background-color: #1E1E1E; color: #FFF; border: 1px solid #333; border-radius: 4px; padding: 4px; font-weight: bold; }}
        """)

        main_layout = QVBoxLayout(self)
        title = DashboardTitle(self.main_app, "AllMeD Control Dashboard")
        main_layout.addWidget(title)

        grid = QGridLayout()
        main_layout.addLayout(grid)

        def add_combo(layout, label, items, cur_val, callback):
            h = QHBoxLayout()
            h.addWidget(QLabel(label))
            cb = QComboBox()
            for text, data in items:
                cb.addItem(text, data)
            idx = cb.findData(cur_val)
            if idx >= 0: cb.setCurrentIndex(idx)
            cb.currentIndexChanged.connect(lambda i: callback(cb.itemData(i)))
            h.addWidget(cb)
            layout.addLayout(h)

        def add_slider(layout, label, min_v, max_v, cur_val, callback):
            h = QHBoxLayout()
            h.addWidget(QLabel(label))
            sl = QSlider(Qt.Horizontal)
            sl.setRange(min_v, max_v)
            sl.setValue(cur_val)
            val_lbl = QLabel(str(cur_val))
            def on_change(v):
                val_lbl.setText(str(v))
                callback(v)
            sl.valueChanged.connect(on_change)
            h.addWidget(sl)
            h.addWidget(val_lbl)
            layout.addLayout(h)

        # --- CORE ---
        v1 = QVBoxLayout()
        chk_glow = QCheckBox("Enable Ambient Glow"); chk_glow.setChecked(main_app.config.get("base_glow_enabled", True)); chk_glow.toggled.connect(main_app._toggle_base_glow); v1.addWidget(chk_glow)
        chk_audio = QCheckBox("Enable Audio Visualizations"); chk_audio.setChecked(main_app.config.get("glow_enabled", True)); chk_audio.toggled.connect(main_app._toggle_glow); v1.addWidget(chk_audio)
        chk_breath = QCheckBox("Enable Breathing"); chk_breath.setChecked(main_app.config.get("breathing", True)); chk_breath.toggled.connect(main_app._toggle_breathing); v1.addWidget(chk_breath)
        chk_mouse = QCheckBox("Enable Mouse Movement"); chk_mouse.setChecked(main_app.config.get("mouse_movement_enabled", True)); chk_mouse.toggled.connect(main_app._toggle_mouse_movement); v1.addWidget(chk_mouse)
        chk_startup = QCheckBox("Start with Windows"); chk_startup.setChecked(main_app.config.get("start_with_windows", False)); chk_startup.toggled.connect(main_app._toggle_startup); v1.addWidget(chk_startup)
        grp1 = QGroupBox("Core Modules"); grp1.setLayout(v1); grid.addWidget(grp1, 0, 0)

        
        # --- VISUALS ---
        v3 = QVBoxLayout()
        add_combo(v3, "Audio Driver Mode", [("Both", "both"), ("Volume Only", "volume"), ("Frequency Only", "frequency")], main_app.config.get("audio_visual_mode", "both"), lambda v: main_app._set_config_val("audio_visual_mode", v))
        add_combo(v3, "Audio Effect", [
            ("Pulsing Aura", "pulsing_aura"), ("Chroma Pulse", "chroma_pulse"),
            ("Equalizer Ring", "equalizer_ring"), ("Waveform Orbit", "waveform_orbit"), 
            ("Frequency Ripple", "frequency_ripple"), ("Particle Spark", "particle_spark")
        ], main_app.config.get("audio_effect", "pulsing_aura"), main_app._set_audio_effect)
        add_combo(v3, "Breathing Target", [("Both", "both"), ("App Only", "app"), ("Glow Only", "glow")], main_app.config.get("breathing_target", "both"), lambda v: main_app._set_config_val("breathing_target", v))
        add_combo(v3, "Mouse Target", [("Both", "both"), ("App Only", "app"), ("Glow Only", "glow")], main_app.config.get("mouse_movement_target", "both"), lambda v: main_app._set_config_val("mouse_movement_target", v))
        grp3 = QGroupBox("Visual Targets"); grp3.setLayout(v3); grid.addWidget(grp3, 1, 0)

        # --- SLIDERS ---
        v4 = QVBoxLayout()
        add_slider(v4, "App Size %", 20, 200, main_app.config.get("size_pct", 50), main_app._on_size)
        add_slider(v4, "App Opacity %", 10, 100, int(main_app.config.get("opacity", 0.9)*100), main_app._on_opacity)
        add_slider(v4, "Glow Size %", 10, 100, main_app.config.get("glow_size_pct", 50), main_app._on_glow_size)
        add_slider(v4, "Glow Opacity %", 10, 100, int(main_app.config.get("glow_opacity", 0.9)*100), main_app._on_glow_opacity)
        add_slider(v4, "App Hue °", 0, 360, main_app.config.get("hue", 190), main_app._on_hue)
        add_slider(v4, "Breath Speed %", 1, 100, main_app.config.get("breathing_speed", 50), main_app._on_breathing_speed)
        grp4 = QGroupBox("Adjustments"); grp4.setLayout(v4); grid.addWidget(grp4, 1, 1)

# =============================================================================
# =============================================================================
class AllmeButton(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._p = parent
        self.setMouseTracking(True)
        self.setCursor(Qt.SizeAllCursor)

        self._is_drag  = False
        self._drag_pos = QPoint()

        self._hover_zone  = None
        self._lpress_zone = None
        self._rpress_zone = None
        self._mpress_zone = None

        self._hover_inner = 0.0
        self._hover_left  = 0.0
        self._hover_right = 0.0

        self._lp_inner = 0.0; self._lp_left = 0.0; self._lp_right = 0.0
        self._rp_inner = 0.0; self._rp_left = 0.0; self._rp_right = 0.0
        self._mp_inner = 0.0; self._mp_left = 0.0; self._mp_right = 0.0

        self.last_click_time = 0.0

        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(25)

    def _calc_base_size(self):
        sz = 32.0 + 56.0 * (self._p.config.get("size_pct", 50) / 100.0)
        t_target = self._p.config.get("telemetry_target", "app_size")
        b_target = self._p.config.get("breathing_target", "both")
        b_enabled = self._p.config.get("breathing", True)
        m_target = self._p.config.get("mouse_movement_target", "both")
        m_enabled = self._p.config.get("mouse_movement_enabled", True)

        # Telemetry modulation for app_size or app_glow_size
        if t_target in ("app_size", "app_glow_size"):
            sz += self._p.telemetry_val * 45.0

        # Mouse movement speed modulation for app_size (when enabled & target allows app)
        if m_enabled and m_target in ("both", "app"):
            sz += self._p.smooth_accel * 30.0

        # Sine breathing modulation for app_size (only if breathing enabled and target allows app)
        if b_enabled and b_target in ("both", "app"):
            sine_val = (math.sin(self._p.breath_phase) + 1.0) / 2.0
            sz += sine_val * 6.0

        return sz

    def _zone(self, pos):
        cx = cy = self.width() / 2.0
        base_size = self._calc_base_size()

        inner_r = max(4.0, base_size * 0.22)
        outer_r = max(10.0, base_size * 0.464)

        dx, dy = pos.x() - cx, pos.y() - cy
        r = math.hypot(dx, dy)
        if r <= inner_r:
            return 'inner'
        if r <= outer_r:
            return 'left' if dx < 0 else 'right'
        return None

    def _tick(self):
        ti = 1.0 if self._hover_zone == 'inner' else 0.0
        tl = 1.0 if self._hover_zone == 'left'  else 0.0
        tr = 1.0 if self._hover_zone == 'right' else 0.0

        self._hover_inner += (ti - self._hover_inner) * 0.15
        self._hover_left  += (tl - self._hover_left)  * 0.15
        self._hover_right += (tr - self._hover_right) * 0.15

        for z, attr in [('inner', '_lp_inner'), ('left', '_lp_left'), ('right', '_lp_right')]:
            cur = getattr(self, attr)
            setattr(self, attr, 1.0 if self._lpress_zone == z else max(0.0, cur - 0.07))

        for z, attr in [('inner', '_rp_inner'), ('left', '_rp_left'), ('right', '_rp_right')]:
            cur = getattr(self, attr)
            setattr(self, attr, 1.0 if self._rpress_zone == z else max(0.0, cur - 0.07))

        for z, attr in [('inner', '_mp_inner'), ('left', '_mp_left'), ('right', '_mp_right')]:
            cur = getattr(self, attr)
            setattr(self, attr, 1.0 if self._mpress_zone == z else max(0.0, cur - 0.07))

        self.update()

    def paintEvent(self, _ev):
        try:
            self._paint_impl()
        except Exception as e:
            print(f"[Allme] Paint error: {e}", flush=True)

    def _paint_impl(self):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        cx = cy = self.width() / 2.0
        base_size = self._calc_base_size()

        inner_r = max(4.0, base_size * 0.22)
        outer_r = max(10.0, base_size * 0.464)

        # ── Configuration & Target Resolution ──
        t_target = self._p.config.get("telemetry_target", "app_size")
        hue_target = self._p.config.get("color_hue_target", "both")
        b_target = self._p.config.get("breathing_target", "both")
        b_enabled = self._p.config.get("breathing", True)
        custom_h = self._p.config.get("hue", 190)

        # Un-modulated base size for glow radius calculation (so app mouse movement, app size telemetry & app breathing don't expand glow)
        raw_glow_app_size = 32.0 + 56.0 * (self._p.config.get("size_pct", 50) / 100.0)
        if t_target in ("glow_size", "app_glow_size"):
            raw_glow_app_size += self._p.telemetry_val * 45.0
        glow_anchor_r = max(10.0, raw_glow_app_size * 0.464)

        # Telemetry gradient shifts (Cool Blue 200° -> Warning Red 0°, or Red 0° -> Blue 240°)
        if t_target in ("glow_color", "app_glow_color"):
            custom_h = int(200.0 * (1.0 - self._p.telemetry_val))
        elif t_target in ("app_color", "app_glow_color"):
            custom_h = int(240.0 * self._p.telemetry_val)

        # Opacity Modulation
        app_op = self._p.config.get("opacity", 0.9)
        glow_user_op = self._p.config.get("glow_opacity", 0.9)

        if t_target in ("app_opacity", "app_glow_opacity"):
            app_op = min(1.0, max(0.15, self._p.telemetry_val))
        if t_target in ("glow_opacity", "app_glow_opacity"):
            glow_user_op = min(1.0, max(0.15, self._p.telemetry_val))

        # ── 1. Calculate Core Metrics & Colors (used by both Base Glow & Visualizations) ──
        audio_fx_on = self._p.config.get("glow_enabled", True)

        # Volume & Frequency drive glow ONLY if audio visualizations are enabled
        vol_amp = self._p.audio_mon.current_volume if audio_fx_on else 0.0
        aud_freq = self._p.audio_mon.current_frequency if audio_fx_on else 0.0
        
        av_mode = self._p.config.get("audio_visual_mode", "both")
        if av_mode == "volume": aud_freq = 0.0
        if av_mode == "frequency": vol_amp = 0.0

        sine_val = (math.sin(self._p.breath_phase) + 1.0) / 2.0 if (b_enabled and b_target in ("both", "glow")) else 0.0

        intensity = min(1.0, max(0.08, 0.18 + (sine_val * 0.20) + (vol_amp * 0.85)))
        glow_alpha = int((50 + 195 * intensity) * glow_user_op)
        glow_alpha = min(245, max(0, glow_alpha))

        freq_factor = min(1.0, max(0.0, aud_freq))
        glow_sz_scale = self._p.config.get("glow_size_pct", 50) / 100.0
        glow_base_ext = 5.0 + 35.0 * glow_sz_scale + (sine_val * 12.0)
        glow_audio_ext = freq_factor * (10.0 + 50.0 * glow_sz_scale)
        if t_target in ("glow_size", "app_glow_size"):
            glow_audio_ext += self._p.telemetry_val * 55.0

        m_enabled = self._p.config.get("mouse_movement_enabled", True)
        m_tgt = self._p.config.get("mouse_movement_target", "both")
        mouse_glow_ext = (self._p.smooth_accel * 28.0) if (m_enabled and m_tgt in ("both", "glow")) else 0.0

        glow_radius = glow_anchor_r + glow_base_ext + glow_audio_ext + mouse_glow_ext

        if self._p.is_recording:
            glow_color = QColor(255, 40, 40, glow_alpha)
            outer_color = QColor(255, 40, 40, int(glow_alpha * 0.45))
        else:
            if self._p.config.get("link_system_accent", False):
                r, g, b = get_system_accent_color(hex_format=False)
                glow_color = QColor(r, g, b, glow_alpha)
                outer_color = QColor(r, g, b, int(glow_alpha * 0.45))
            else:
                h_glow = self._p.config.get("hue", 190)
                if hue_target in ("both", "glow"):
                    if t_target in ("glow_color", "app_glow_color"):
                        h_glow = int(200.0 * (1.0 - self._p.telemetry_val))
                    else:
                        h_glow = custom_h
                glow_color = QColor.fromHsv(h_glow, 255, 255, glow_alpha)
                outer_color = QColor.fromHsv(h_glow, 255, 255, int(glow_alpha * 0.45))

        effect = self._p.config.get("audio_effect", "pulsing_aura")

        if effect == "chroma_pulse":
            chroma_h = int((custom_h + freq_factor * 180.0 + time.time() * 60.0) % 360)
            glow_color = QColor.fromHsv(chroma_h, 255, 255, glow_alpha)
            outer_color = QColor.fromHsv(chroma_h, 255, 255, int(glow_alpha * 0.45))

        # ── 1a. Render Ambient Base Glow (if enabled) ──
        if self._p.config.get("base_glow_enabled", True):
            radial_outer = QRadialGradient(cx, cy, glow_radius + 14.0)
            radial_outer.setColorAt(0.0, outer_color)
            radial_outer.setColorAt(0.6, QColor(outer_color.red(), outer_color.green(), outer_color.blue(), int(glow_alpha * 0.15)))
            radial_outer.setColorAt(1.0, QColor(0, 0, 0, 0))
            p.setBrush(QBrush(radial_outer))
            p.setPen(Qt.NoPen)
            p.drawEllipse(QRectF(cx - (glow_radius + 14.0), cy - (glow_radius + 14.0), (glow_radius + 14.0)*2.0, (glow_radius + 14.0)*2.0))

            radial = QRadialGradient(cx, cy, glow_radius)
            radial.setColorAt(0.0, glow_color)
            radial.setColorAt(0.65, QColor(glow_color.red(), glow_color.green(), glow_color.blue(), int(glow_alpha * 0.45)))
            radial.setColorAt(1.0, QColor(0, 0, 0, 0))
            p.setBrush(QBrush(radial))
            p.setPen(Qt.NoPen)
            p.drawEllipse(QRectF(cx - glow_radius, cy - glow_radius, glow_radius * 2.0, glow_radius * 2.0))

        # ── Audio Visualizations (Controlled by "Enable Audio Overlay Visualizations" toggle) ──
        if self._p.config.get("glow_enabled", True):
            if effect == "equalizer_ring":
                num_bars = 24
                bar_pen = QPen(glow_color)
                bar_pen.setWidthF(2.0 + freq_factor * 2.0)
                p.setPen(bar_pen)
                for i in range(num_bars):
                    angle = (i / float(num_bars)) * 2.0 * math.pi
                    h_bar = 4.0 + (math.sin(angle * 3.0 + time.time() * 8.0) + 1.0) * 0.5 * (8.0 + 32.0 * vol_amp + 20.0 * freq_factor)
                    r_in = glow_anchor_r + 2.0
                    r_out = r_in + h_bar
                    p.drawLine(
                        QPointF(cx + r_in * math.cos(angle), cy + r_in * math.sin(angle)),
                        QPointF(cx + r_out * math.cos(angle), cy + r_out * math.sin(angle))
                    )

            elif effect == "waveform_orbit":
                wave_pen = QPen(glow_color); wave_pen.setWidthF(1.8 + freq_factor * 1.5)
                p.setPen(wave_pen); p.setBrush(Qt.NoBrush)
                pts = []
                freq_peaks = 4.0 + int(freq_factor * 12.0)
                for deg in range(0, 360, 5):
                    rad = math.radians(deg)
                    r_wave = glow_anchor_r + 4.0 + math.sin(rad * freq_peaks + time.time() * 10.0) * (3.0 + 14.0 * vol_amp)
                    pts.append(QPointF(cx + r_wave * math.cos(rad), cy + r_wave * math.sin(rad)))
                for i in range(len(pts)):
                    p.drawLine(pts[i], pts[(i+1) % len(pts)])

            elif effect == "frequency_ripple":
                for r_off in [5.0, 15.0, 25.0]:
                    rip_r = glow_anchor_r + ((r_off + time.time() * (30.0 + 50.0 * freq_factor)) % 35.0)
                    rip_alpha = int(max(0, 220 * (1.0 - (rip_r - glow_anchor_r) / 35.0) * (0.2 + 0.8 * vol_amp)))
                    rip_pen = QPen(QColor(glow_color.red(), glow_color.green(), glow_color.blue(), rip_alpha))
                    rip_pen.setWidthF(1.5 + freq_factor * 1.5)
                    p.setPen(rip_pen); p.setBrush(Qt.NoBrush)
                    p.drawEllipse(QPointF(cx, cy), rip_r, rip_r)

            elif effect == "particle_spark":
                p.setPen(Qt.NoPen)
                num_orbs = 12 + int(freq_factor * 12.0)
                for i in range(num_orbs):
                    angle = (i / float(num_orbs)) * 2.0 * math.pi + time.time() * (2.0 + 3.0 * freq_factor)
                    p_dist = glow_anchor_r + 6.0 + vol_amp * 22.0 * (math.sin(i * 1.5) * 0.5 + 0.5)
                    px_c = cx + p_dist * math.cos(angle)
                    py_c = cy + p_dist * math.sin(angle)
                    p_size = 3.0 + vol_amp * 5.0 + freq_factor * 3.0
                    p.setBrush(QBrush(glow_color))
                    p.drawEllipse(QRectF(px_c - p_size/2.0, py_c - p_size/2.0, p_size, p_size))

        # ── 2. 3-Zone Interactive Ring & Center Body ──
        if self._p.config.get("link_system_accent", False):
            r, g, b = get_system_accent_color(hex_format=False)
            c_base = QColor(int(r*0.1), int(g*0.1), int(b*0.1), int(220 * app_op))
            c_hover = QColor(int(r*0.2), int(g*0.2), int(b*0.2), int(230 * app_op))
        elif hue_target in ("both", "app"):
            h_app = custom_h
            c_base = QColor.fromHsv(h_app, 160, 45, int(220 * app_op))
            c_hover = QColor.fromHsv(h_app, 180, 65, int(230 * app_op))
        else:
            c_base   = QColor(22, 26, 36, int(220 * app_op))
            c_hover  = QColor(38, 48, 64, int(225 * app_op))

        c_lpress = QColor(0, 140, 240, int(220 * app_op))
        c_rpress = QColor(0, 200, 140, int(220 * app_op))
        c_mpress = QColor(255, 120, 0, int(220 * app_op))

        if self._p.screenshot_flash > 0:
            c_base = QColor(255, 255, 255, min(240, int((180 + 255 * self._p.screenshot_flash) * app_op)))

        def zone_col(h, lp, rp, mp=0.0):
            c = lerp_color(c_base, c_hover, h)
            c = lerp_color(c, c_lpress, lp)
            c = lerp_color(c, c_rpress, rp)
            c = lerp_color(c, c_mpress, mp)
            return c

        p.setPen(Qt.NoPen)

        # Left Ring
        lc = zone_col(self._hover_left, self._lp_left, self._rp_left, self._mp_left)
        p.setBrush(QBrush(lc))
        p.drawPie(QRectF(cx - outer_r, cy - outer_r, outer_r * 2, outer_r * 2), 90 * 16, 180 * 16)

        # Right Ring
        rc = zone_col(self._hover_right, self._lp_right, self._rp_right, self._mp_right)
        p.setBrush(QBrush(rc))
        p.drawPie(QRectF(cx - outer_r, cy - outer_r, outer_r * 2, outer_r * 2), 270 * 16, 180 * 16)

        # Divider lines
        div = QPen(QColor(255, 255, 255, int(20 * app_op))); div.setWidthF(1.0); div.setStyle(Qt.DashLine)
        p.setPen(div)
        p.drawLine(QPointF(cx, cy - outer_r + 1), QPointF(cx, cy - inner_r - 2))
        p.drawLine(QPointF(cx, cy + inner_r + 2), QPointF(cx, cy + outer_r - 1))

        # Ring separator
        sp = QPen(QColor(255, 255, 255, int(25 * app_op))); sp.setWidthF(1.0)
        p.setPen(sp); p.setBrush(Qt.NoBrush)
        p.drawEllipse(QPointF(cx, cy), inner_r + 2, inner_r + 2)

        # Center core
        ic = zone_col(self._hover_inner, self._lp_inner, self._rp_inner, self._mp_inner)
        p.setBrush(QBrush(ic)); p.setPen(Qt.NoPen)
        p.drawEllipse(QPointF(cx, cy), inner_r, inner_r)

        # ── 3. Icon / Favicon / Recording Overlay ──
        if self._p.is_recording:
            sq = inner_r * 0.8
            p.setBrush(QBrush(QColor(255, 50, 50)))
            p.setPen(Qt.NoPen)
            p.drawRect(QRectF(cx - sq/2.0, cy - sq/2.0, sq, sq))
        else:
            icon_pm = None
            if self._p.browser_active and self._p.favicon_pixmap:
                icon_pm = self._p.favicon_pixmap
            elif self._p.browser_active and self._p.browser_icon_pixmap:
                icon_pm = self._p.browser_icon_pixmap
            elif self._p.active_icon_pixmap:
                icon_pm = self._p.active_icon_pixmap

            if icon_pm:
                isz = inner_r * 1.5
                rx = cx - isz / 2.0; ry = cy - isz / 2.0
                p.drawPixmap(QRectF(rx, ry, isz, isz), icon_pm, QRectF(icon_pm.rect()))

        # Outer border linked smoothly to app_op
        if self._p.is_recording:
            border_c = QColor(255, 40, 40, int(240 * app_op))
        elif self._p.config.get("clickthrough", False):
            border_c = QColor(0, 230, 255, int(220 * app_op))
        elif self._p.config.get("lock_position", False):
            border_c = QColor(255, 165, 0, int(220 * app_op))
        elif self._p.is_fly_mode:
            border_c = QColor(138, 43, 226, int(220 * app_op))
        else:
            border_c = QColor(255, 255, 255, int(60 * app_op))

        bp = QPen(border_c); bp.setWidthF(2.0)
        p.setPen(bp); p.setBrush(Qt.NoBrush)
        p.drawEllipse(QPointF(cx, cy), outer_r, outer_r)
        p.end()

    # ── Mouse Events ──
    def mousePressEvent(self, event):
        pw = self._p
        ct_enabled = pw.config.get("clickthrough", False)
        ct_mode = pw.config.get("clickthrough_mode", "all")

        # Selective button pass-through logic
        if ct_enabled:
            if ct_mode == "all":
                event.ignore(); return
            elif ct_mode == "left" and event.button() == Qt.LeftButton:
                event.ignore(); return
            elif ct_mode == "right" and event.button() == Qt.RightButton:
                event.ignore(); return
            elif ct_mode == "middle" and event.button() == Qt.MiddleButton:
                event.ignore(); return

        click_pos = event.pos()
        z = self._zone(click_pos)

        if event.button() == Qt.LeftButton:
            mods = event.modifiers()
            if mods & Qt.AltModifier:
                QApplication.quit(); return
            if mods & Qt.ShiftModifier:
                pw.toggle_lock_position(); event.accept(); return
            if mods & Qt.ControlModifier:
                pw.toggle_fly_mode(); event.accept(); return

            if not pw.config.get("lock_position", False) and not pw.is_fly_mode and not pw.config.get("clickthrough", False):
                self._drag_pos = event.globalPos() - pw.frameGeometry().topLeft()
                self._is_drag  = False
            self._lpress_zone = z
            self.update()

        elif event.button() == Qt.RightButton:
            self._rpress_zone = z
            self.update()

        elif event.button() == Qt.MiddleButton:
            self._mpress_zone = z
            self.update()
            if z == 'inner':
                pw.toggle_recording()
            elif z in ('left', 'right'):
                pw.take_screenshot()
            elif pw.is_fly_mode:
                pw.quick_switch()
            else:
                pw.take_screenshot()
        event.accept()

    def mouseMoveEvent(self, event):
        pw = self._p
        pw.telemetry_mon.record_mouse()
        z = self._zone(event.pos())
        if z != self._hover_zone:
            self._hover_zone = z
            self.update()

        if event.buttons() & Qt.LeftButton and not pw.config.get("lock_position", False) and not pw.is_fly_mode and not pw.config.get("clickthrough", False):
            diff = event.globalPos() - (pw.frameGeometry().topLeft() + self._drag_pos)
            if diff.manhattanLength() > 4:
                self._is_drag = True
            if self._is_drag:
                pw.move(event.globalPos() - self._drag_pos)
                pw.config["pos_x"] = pw.x()
                pw.config["pos_y"] = pw.y()
                save_config(pw.config)
        event.accept()

    def mouseReleaseEvent(self, event):
        pw = self._p
        if event.button() == Qt.LeftButton:
            pz = self._lpress_zone
            self._lpress_zone = None
            self.update()
            if not self._is_drag:
                mods = event.modifiers()
                if not (mods & (Qt.AltModifier | Qt.ShiftModifier | Qt.ControlModifier)):
                    z = self._zone(event.pos())
                    if z == pz:
                        if z == 'inner':
                            pw.quick_switch()
                        elif z == 'left':
                            pw.cycle_left()
                        elif z == 'right':
                            pw.cycle_right()
            self._is_drag = False

        elif event.button() == Qt.RightButton:
            pz = self._rpress_zone
            self._rpress_zone = None
            self.update()
            z = self._zone(event.pos())
            if z == pz:
                if z == 'inner':
                    pw.tab_switch()
                elif z == 'left':
                    pw.tab_cycle_left()
                elif z == 'right':
                    pw.tab_cycle_right()

        elif event.button() == Qt.MiddleButton:
            self._mpress_zone = None
            self.update()
        event.accept()

    def contextMenuEvent(self, event):
        event.accept()

    def leaveEvent(self, _ev):
        self._hover_zone = None
        self.update()

# =============================================================================
#  AllmeWidget — Main Container Widget
# =============================================================================
class AllmeWidget(QWidget):
    middle_click_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.config = load_config()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint |
                            Qt.Tool | Qt.SubWindow | Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        px = QPixmap()
        try:
            icon_data = base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAPEElEQVR4nO1bC3BUZZb+///efncn"
                "6bw6AZLCDM4QgpKHIa0DSyiXwDiTwmGGaIEgE3cy4lAu7hRVzq6SB4igEFgGwYDyEliWHlhB"
                "rdnoLnY0ccnKI2IkMuFtAoQYkn4/7uPfOre7Z2Lo9CPdRmZ2vqpbSd97/8c5//nPOf855yL0N"
                "/z/Bh7tASmlw46JMaborw00BMHfZtvvFDTIxGfMqGaPHTum7ujo0FFKEyil+iFXUnNHh66xsVF"
                "TVVUli6TPeADHszOY5CAxxg3HjqmqysuVCCEGIUQQQixCSGa327UnTpzSKRQKEV4UBB4bDBne"
                "3NwJ/fATIeRBCMEzwWw2e2fOnOny3x86RsxgURwBE5s/fz6zfv36hOzsbLmfcP2mLTvGffRR"
                "86Qb12/ca7XZsjmOS/F6uTSEMe9bBEoYwtiVSsUNlVJ1K92Q+scH8qd0VC5aeKW0tPRrSqkG"
                "IcQ/u3mzHWPsCQwH/Ih5zihOAMI3bNiQmJWVBYRr1q3bOPHYe+/P6untNXIeb5Ygijr/eAIh"
                "GFYTiB8MIlIqQxQkhRKMiVMuY2/o9YlnSkqmfvDa5ldOI4QGEEJcTU2Ntba21huPeeN4dHLy"
                "5MnEoqIiWCXlsn983vihuWmB1e4oooKgI4R4EMYejCSiYdFwiLEpQgHxpoRSKhdFqkQYe9Uq"
                "xfnJeZMOHTHtfR8Y0d3d7Rk3bkc/QrViLNsCoxhQXV3N1tTUpMFWWrlybaHp6NFf2aw2I6wm"
                "IcTpI5rCzMgIJwcMEaEPgVIVEqlMqVJ8WVxcuPPf9u5oBGkwmUx9FRUVrpEyAUfbIDAQaPTy"
                "8nI9QkhnnFb2THf3jccopUqGITbpvRESHWKiIkiHQEU1EimJTJSTQtH5t3do5c/7+WlvbFUdB"
                "wT0DI+w3erz99tu6uXPnJu3bd/B7q9fWv2i3O4yEYSyw4hRRUHzfGv7ECFFIZFn2+o9mz6rb"
                "tuXVlo6ODvukSZP6RtBfdCvf2nouZerUXHXNqlem7Nqz73eCIOoZwlgponG1KOEgMZuKClGk8"
                "qKC++uO/seBQ1999RXNzs7ujmY7kIgHxJh++OGHWiC+7qX19+/as38LFamOIYxttIkHgKRh"
                "jL2EIc5TbWdXls9bOD8rK4ucPn06DeYaqeNEIh0Q9nxpaWkyrPybu956jYqiFmPi+rZFPhRA"
                "z0hOBCHOM6c/q507b+HPCwoKVO3t7clxlYAZM6pZUHh7D5juAbG/G4gPAMwEMIFhiOPU6c9q"
                "Fy55enZeXp5q7969YJbDAkc0CLVnIqRJ+EHe1G0Op7Pwu9jzkShHSqmMEOyoq3vxF4sXzL9Q"
                "U1PTU1tby4dpFxonTpxIKCkpSTROK1vR1dVdyTDs7buN+MGKURAFnVajPvVl+/+GiHUhzHu"
                "9TlfwbcECefelpSUaFfWvVTY3X39MWLcfSv/GLAlQTrtdkfJj8orHkUIyQ8dOqQajviwEnD16l"
                "V9dna2Pm/Kg1ssFttDDCNp/FHZ9wRjsDxIEKUDY8QAfUApZQlDrG/tbHhi+nTjZYzxrWHHQS"
                "FWPzs7WwG+vcVqMzIMsY8m8V4vhxwOB2IZJnqliImX5/jMF+pWgxSwDQ0N6oklgPqdiMuXLy"
                "eNHz8+OW/Kg5stFts0HwPi694GA0Mwstmd6EFjMUlI0OGjR9/j09JSwbCDlotSCpiBt3a+vn"
                "j6dOMlny64E+SOxj77icePHy9ft25jrtXmKAJnYzSI948PARKarE/C+/c0KJctq5L13e6nQ"
                "DxDSIRSMOaV+s1/B3ytrq6GY/odIMFuNjQ0qEB0jr33n7OoKOj+fJQdHuCRwARjvQghkthz"
                "PCfRsvb1Svn2rfUKzutFbrc7ii1BMSKI7+y8MAcObJWVlZJfMNRDZIOJf1VVlRJ5kb6nt89I"
                "CHGDsxVuOF4Qkcvl9HklaOSQMQRZbXbkcfsCP6ALHn/sZ7KJEyeSJ3/xtOdaV5eYmJCAw20H"
                "kFiCixuh9M7cdGWbzfJFS6XT4lAPkR38Y9BDZtP2beM8Hq+W+NvgUqH2rMPhtA8UFzCrqv9Z"
                "5nS6pVUcKTBBiOd4lJKsl8ZkWQZxHE/zp+Qxxz84qvz1syu8zZ+0CiAJ4ZgAkiuKQuJHH30y"
                "afmypWfAo21q+qZjxA5tBC9BW2hERVEHx9xQ2h/2LMfzyJCWjosK8+PqI4iiCH6+xFC3201T"
                "UpLJ2pfpZEVzr3ddF+v3D1AZEzb4GbqCH0or32oH5mCFl0n6n+6o/lPh5U87e14dnb4pCvhL"
                "fZHcUSTyeQEUUd/KaBD6nDgM7jGxjYNfBpHKU32X6kQe/T/DfwvfULX3t6uHa6o6S8KNHTJ+"
                "uBn+Lv6eBKjUcRgYoIprsDzv8pPaP8GdHfi/wA281geAi7zYgAAAABJRU5ErkJggg=="
            )
            px.loadFromData(icon_data)
        except Exception: pass

        if px.isNull():
            px = QPixmap(32, 32)
            px.fill(Qt.transparent)
            painter = QPainter(px)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QPen(QColor(0, 210, 255), 2))
            painter.setBrush(QBrush(QColor(25, 30, 45)))
            painter.drawEllipse(3, 3, 26, 26)
            painter.setBrush(QBrush(QColor(0, 210, 255)))
            painter.drawEllipse(12, 12, 8, 8)
            painter.end()

        self.app_icon = QIcon(px)
        self.setWindowIcon(self.app_icon)

        # Subsystems
        self.recorder = VideoRecorder()
        self.is_recording = False
        self.audio_mon = AudioMonitor()
        self.audio_mon.start()

        self.telemetry_val = 0.0
        self.telemetry_mon = TelemetryMonitor(self)
        self.telemetry_mon.start()

        self._fav_mgr = FaviconManager()
        self.is_fly_mode = False
        self.saved_position = None

        # State tracking
        self.active_icon_pixmap = None
        self.current_hwnd = None
        self.last_hwnd = None
        self.is_cycling = False
        self.cycle_list = []
        self.cycle_index = 0
        self.last_cycle_time = 0.0

        self.browser_active = False
        self.browser_hwnd = None
        self.browser_icon_pixmap = None
        self.favicon_pixmap = None
        self._tab_switch_dir = 1
        self._last_browser_title = ""

        # Visual dynamics & Mouse acceleration
        self.current_glow_intensity = 0.0
        self.current_glow_size_factor = 0.0
        self.current_icon_scale_factor = 0.0
        self.screenshot_flash = 0.0
        self.mouse_speed = 0.0
        self.last_mouse_speed = 0.0
        self.smooth_accel = 0.0
        self.last_mouse_pos = QCursor.pos()
        self.last_mouse_time = time.time()
        self.breath_phase = 0.0

        # UI Setup
        base_size = int(32 + 56 * (self.config.get("size_pct", 50) / 100.0))
        size_px = base_size + 280
        self.setFixedSize(size_px, size_px)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.button = AllmeButton(self)
        layout.addWidget(self.button)

        screen_geo = QApplication.primaryScreen().geometry()
        def_x = self.config.get("pos_x", -1)
        def_y = self.config.get("pos_y", -1)
        if def_x < 0 or def_y < 0:
            def_x = screen_geo.width() - size_px - 50
            def_y = screen_geo.height() - size_px - 100
        self.move(def_x, def_y)

        # Timers
        self.poll_timer = QTimer(self)
        self.poll_timer.timeout.connect(self._poll)
        self.poll_timer.start(120)

        self.anim_timer = QTimer(self)
        self.anim_timer.setInterval(10)
        self.anim_timer.timeout.connect(self._update_animation)
        self.anim_timer.start()

        self.fly_timer = QTimer(self)
        self.fly_timer.timeout.connect(self._update_fly)

        # Main Thread Win32 Hooks
        self.mouse_hook = MouseHook(self.middle_click_signal.emit)
        self.middle_click_signal.connect(self._on_global_middle)
        self.mouse_hook.install()

        self.keyboard_hook = KeyboardHook(self._on_key_pressed)
        self.keyboard_hook.install()

        # Win32 Flags
        hwnd = int(self.winId())
        ex = GetWindowLongW(hwnd, GWL_EXSTYLE)
        flags = ex | WS_EX_NOACTIVATE | WS_EX_TOOLWINDOW
        if self.config.get("clickthrough", False):
            flags |= WS_EX_TRANSPARENT
        SetWindowLongW(hwnd, GWL_EXSTYLE, flags)

        self._setup_tray()
        self.show()
        if self.config.get("always_on_top", True):
            self._enforce_always_on_top()

    def _on_key_pressed(self):
        if hasattr(self, "telemetry_mon"):
            self.telemetry_mon.record_key()

    def _enforce_always_on_top(self):
        if not self.config.get("always_on_top", True): return
        try:
            hwnd = int(self.winId())
            ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0010 | 0x0040)
        except Exception: pass
        self.raise_()

    def showEvent(self, e):
        super().showEvent(e)
        if self.config.get("always_on_top", True): self._enforce_always_on_top()

    def changeEvent(self, e):
        super().changeEvent(e)
        if e.type() in (QEvent.WindowStateChange, QEvent.ActivationChange, QEvent.ZOrderChange):
            if self.config.get("always_on_top", True): self._enforce_always_on_top()

    def _poll(self):
        if self.is_cycling and (time.time() - self.last_cycle_time > 2.0):
            self.is_cycling = False
            self.cycle_list = []

        active_id = get_active_window_id()
        if active_id and active_id != int(self.winId()):
            if active_id != self.current_hwnd:
                self.last_hwnd = self.current_hwnd
                self.current_hwnd = active_id
                self.active_icon_pixmap = get_window_icon(active_id)
                self.button.update()
        elif not active_id:
            if self.active_icon_pixmap is not None:
                self.active_icon_pixmap = None
                self.button.update()

        fg = GetForegroundWindow()
        if fg and fg != int(self.winId()):
            br = is_browser(fg)
            if br:
                title = get_window_title(fg)
                if fg != self.browser_hwnd or self.browser_icon_pixmap is None:
                    self.browser_hwnd = fg
                    self.browser_icon_pixmap = get_window_icon(fg)
                if title != self._last_browser_title:
                    self._last_browser_title = title
                    self._fav_mgr.request(fg)
            if br != self.browser_active:
                self.browser_active = br
                self.button.update()
        else:
            if self.browser_active:
                self.browser_active = False
                self.button.update()

        res = self._fav_mgr.poll_result()
        if res:
            _dom, data = res
            if data:
                pm = QPixmap()
                pm.loadFromData(data)
                if not pm.isNull():
                    self.favicon_pixmap = pm
                    self.button.update()

    def _update_animation(self):
        now = time.time()
        dt = max(0.001, now - self.last_mouse_time)
        cur_pos = QCursor.pos()
        dx = cur_pos.x() - self.last_mouse_pos.x()
        dy = cur_pos.y() - self.last_mouse_pos.y()
        current_speed = math.hypot(dx, dy) / dt

        self.last_mouse_pos = cur_pos
        self.last_mouse_time = now

        norm_speed = min(1.0, current_speed / 2000.0)
        self.smooth_accel += (norm_speed - self.smooth_accel) * 0.12

        # Thread-safe sample retrieval from Telemetry thread
        sample_val = self.telemetry_mon.get_sample()
        self.telemetry_val += (sample_val - self.telemetry_val) * 0.25

        vol_amplitude = self.audio_mon.current_volume
        audio_frequency = self.audio_mon.current_frequency

        if self.config.get("breathing", True):
            speed_pct = self.config.get("breathing_speed", 50)
            step = 0.008 + (speed_pct / 100.0) * 0.072  # Range 0.008 to 0.080
            self.breath_phase += step
            sine_val = (math.sin(self.breath_phase) + 1.0) / 2.0
            target_glow_intensity = 0.25 + (sine_val * 0.25) + (vol_amplitude * 0.85)
            target_glow_size = 0.20 + (sine_val * 0.15) + (audio_frequency * 0.80)
            
            m_enabled = self.config.get("mouse_movement_enabled", True)
            m_tgt = self.config.get("mouse_movement_target", "both")
            m_scale = self.smooth_accel * 16.0 if (m_enabled and m_tgt in ("both", "app")) else 0.0
            target_icon_scale = (sine_val * 2.0) + m_scale
        else:
            self.breath_phase = 0.0
            target_glow_intensity = 0.2 + (vol_amplitude * 0.8)
            target_glow_size = 0.2 + (audio_frequency * 0.8)

            m_enabled = self.config.get("mouse_movement_enabled", True)
            m_tgt = self.config.get("mouse_movement_target", "both")
            m_scale = self.smooth_accel * 12.0 if (m_enabled and m_tgt in ("both", "app")) else 0.0
            target_icon_scale = m_scale

        if target_glow_intensity > self.current_glow_intensity:
            self.current_glow_intensity = target_glow_intensity
        else:
            self.current_glow_intensity += (target_glow_intensity - self.current_glow_intensity) * 0.35

        if target_glow_size > self.current_glow_size_factor:
            self.current_glow_size_factor = target_glow_size
        else:
            self.current_glow_size_factor += (target_glow_size - self.current_glow_size_factor) * 0.35

        self.current_icon_scale_factor += (target_icon_scale - self.current_icon_scale_factor) * 0.10

        if self.screenshot_flash > 0:
            self.screenshot_flash -= 0.1
            if self.screenshot_flash < 0: self.screenshot_flash = 0.0

        self.button.update()

    # ── Media Capture Actions ──
    def take_screenshot(self):
        self.screenshot_flash = 1.0
        self.button.update()
        self.hide()
        QApplication.processEvents()
        try:
            with mss.mss() as sct:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(CAPTURES_DIR, "Screenshots", f"screenshot_{timestamp}.png")
                sct.shot(mon=-1, output=filename)
                self.tray_icon.showMessage("Allme", f"Screenshot saved to:\n{os.path.basename(filename)}",
                                           QSystemTrayIcon.Information, 2000)
        except Exception as e:
            print("Screenshot error:", e)
        finally:
            self.show()

    def toggle_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.recorder.start_recording()
            self.tray_icon.showMessage("Allme", "Video recording started...", QSystemTrayIcon.Information, 1500)
        else:
            self.is_recording = False
            self.recorder.stop_recording()
            self.tray_icon.showMessage("Allme", f"Video saved to:\n{os.path.basename(self.recorder.output_filepath)}",
                                       QSystemTrayIcon.Information, 2000)
        self.button.update()

    # ── Switcher Actions ──
    def quick_switch(self):
        user_wins = get_user_windows()
        if len(user_wins) <= 1: return
        if self.last_hwnd and is_valid_window(self.last_hwnd): switch_to_window(self.last_hwnd)

    def cycle_left(self): self._do_cycle(-1)
    def cycle_right(self): self._do_cycle(1)

    def _do_cycle(self, direction):
        now = time.time()
        if not self.is_cycling or not self.cycle_list or (now - self.last_cycle_time > 2.0):
            self.is_cycling = True
            self.cycle_list = get_user_windows()
            fg = get_active_window_id()
            self.cycle_index = self.cycle_list.index(fg) if fg in self.cycle_list else 0
        if not self.cycle_list:
            self.is_cycling = False; return
        self.cycle_index = (self.cycle_index + direction) % len(self.cycle_list)
        target = self.cycle_list[self.cycle_index]
        if is_valid_window(target): switch_to_window(target)
        self.last_cycle_time = now

    def _focus_browser(self):
        h = self.browser_hwnd
        if h and IsWindow(h):
            if IsIconic(h): ShowWindow(h, SW_RESTORE)
            SetForegroundWindow(h)
            time.sleep(0.05)

    def tab_switch(self):
        self._focus_browser()
        if self._tab_switch_dir == 1:
            send_ctrl_pageup(); self._tab_switch_dir = -1
        else:
            send_ctrl_pagedown(); self._tab_switch_dir = 1

    def tab_cycle_left(self):
        self._focus_browser(); send_ctrl_pageup(); self._tab_switch_dir = -1

    def tab_cycle_right(self):
        self._focus_browser(); send_ctrl_pagedown(); self._tab_switch_dir = 1

    # ── Lock, Clickthrough & Fly Mode ──
    def toggle_lock_position(self):
        if self.is_fly_mode:
            self.is_fly_mode = False
            self.fly_timer.stop()
            if self.saved_position: self.move(self.saved_position)
        l = not self.config.get("lock_position", False)
        self.config["lock_position"] = l
        save_config(self.config)
        s = "locked" if l else "unlocked"
        self.tray_icon.showMessage("Allme", f"Position {s}.", QSystemTrayIcon.Information, 1500)
        self.button.update()

    def toggle_clickthrough(self, checked):
        self.config["clickthrough"] = checked
        save_config(self.config)
        self._update_clickthrough_state()
        s = f"enabled ({self.config.get('clickthrough_mode', 'all')})" if checked else "disabled"
        self.tray_icon.showMessage("Allme", f"Clickthrough {s}.", QSystemTrayIcon.Information, 1500)
        self.button.update()

    def _set_clickthrough_mode(self, mode):
        self.config["clickthrough_mode"] = mode
        save_config(self.config)
        self._update_clickthrough_state()
        self.button.update()

    def _update_clickthrough_state(self):
        checked = self.config.get("clickthrough", False)
        mode = self.config.get("clickthrough_mode", "all")
        hwnd = int(self.winId())
        ex = GetWindowLongW(hwnd, GWL_EXSTYLE)
        # Full Win32 hardware pass-through for 'all' mode
        if checked and mode == "all":
            SetWindowLongW(hwnd, GWL_EXSTYLE, ex | WS_EX_TRANSPARENT)
        else:
            SetWindowLongW(hwnd, GWL_EXSTYLE, ex & ~WS_EX_TRANSPARENT)

    def toggle_fly_mode(self):
        if self.config.get("lock_position", False):
            self.tray_icon.showMessage("Allme", "Unlock position first.", QSystemTrayIcon.Warning, 2000)
            return
        self.is_fly_mode = not self.is_fly_mode
        if self.is_fly_mode:
            self.saved_position = self.pos()
            self.fly_timer.start(16)
            self.tray_icon.showMessage("Allme", "Fly mode ON — middle-click to switch windows.", QSystemTrayIcon.Information, 2000)
        else:
            self.fly_timer.stop()
            if self.saved_position: self.move(self.saved_position)
            self.tray_icon.showMessage("Allme", "Fly mode OFF.", QSystemTrayIcon.Information, 2000)
        self.button.update()

    def _update_fly(self):
        pos = QCursor.pos()
        tx = pos.x() + 20; ty = pos.y() + 20
        scr = QApplication.primaryScreen().geometry()
        if tx + self.width() > scr.right(): tx = pos.x() - self.width() - 20
        if ty + self.height() > scr.bottom(): ty = pos.y() - self.height() - 20
        self.move(tx, ty)

    def _on_global_middle(self):
        if self.is_fly_mode and self.isVisible(): self.quick_switch()

    # ── Persistent Submenu Builder Helper ──
    def _create_sub_menu(self, parent_menu, title):
        sub = PersistentMenu(title, self)
        sub.setStyleSheet(parent_menu.styleSheet())
        parent_menu.addMenu(sub)
        return sub

    # ── System Tray & Full Menu Engine ──
    def _setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.app_icon)
        self.tray_icon.setToolTip("Allme Widget")

        SLIDER_SS = """
            QSlider::groove:horizontal { height:4px; background:#374151; border-radius:2px; }
            QSlider::sub-page:horizontal { background:#00d2ff; border-radius:2px; }
            QSlider::handle:horizontal { background:#fff; width:12px; height:12px; margin:-4px 0; border-radius:6px; }
        """
        self.tray_menu = PersistentMenu("", self)
        self.tray_menu.setStyleSheet("""
            QMenu { background-color:#1e222b; color:#e1e4ea; border:1px solid #3a4253;
                    border-radius:8px; padding:6px; font-family:'Segoe UI',sans-serif; font-size:13px; }
            QMenu::item { padding:6px 24px 6px 12px; border-radius:4px; }
            QMenu::item:selected { background-color:#2c3444; color:#00d2ff; }
            QMenu::separator { height:1px; background:#3a4253; margin:4px 6px; }
        """)

        # Toggles
        self.action_ontop = QAction("Always on Top", self)
        self.action_ontop.setCheckable(True)
        self.action_ontop.setChecked(self.config.get("always_on_top", True))
        self.action_ontop.triggered.connect(self._toggle_ontop)
        self.tray_menu.addAction(self.action_ontop)

        self.action_lock = QAction("Lock Position", self)
        self.action_lock.setCheckable(True)
        self.action_lock.setChecked(self.config.get("lock_position", False))
        self.action_lock.triggered.connect(self.toggle_lock_position)
        self.tray_menu.addAction(self.action_lock)

        self.action_clickthrough = QAction("Clickthrough (Pass Mouse)", self)
        self.action_clickthrough.setCheckable(True)
        self.action_clickthrough.setChecked(self.config.get("clickthrough", False))
        self.action_clickthrough.triggered.connect(self.toggle_clickthrough)
        self.tray_menu.addAction(self.action_clickthrough)

        # 🖱️ Clickthrough Options Submenu
        ct_sub = self._create_sub_menu(self.tray_menu, "🖱️ Clickthrough Mode")
        cur_ct_m = self.config.get("clickthrough_mode", "all")
        ct_grp = QActionGroup(self); ct_grp.setExclusive(True)
        for label, mode_code in [("1. Pass All (Hardware Pass-Through)", "all"), ("2. Pass Left Click Only", "left"), ("3. Pass Right Click Only", "right"), ("4. Pass Middle Click Only", "middle")]:
            act = QAction(label, self)
            act.setCheckable(True)
            ct_grp.addAction(act)
            if cur_ct_m == mode_code: act.setChecked(True)
            act.triggered.connect(lambda _c, m=mode_code: self._set_clickthrough_mode(m))
            ct_sub.addAction(act)

        self.action_fly = QAction("Fly Mode (Follow Cursor)", self)
        self.action_fly.setCheckable(True)
        self.action_fly.setChecked(False)
        self.action_fly.triggered.connect(self.toggle_fly_mode)
        self.tray_menu.addAction(self.action_fly)

        if ENABLE_DASHBOARD_BUILD:
            self.action_dashboard = QAction("🎛️ Futuristic Dashboard", self)
            self.action_dashboard.triggered.connect(self.show_dashboard)
            self.tray_menu.addAction(self.action_dashboard)
            self.tray_menu.addSeparator()

        self.action_base_glow = QAction("Enable Ambient Glow", self)
        self.action_base_glow.setCheckable(True)
        self.action_base_glow.setChecked(self.config.get("base_glow_enabled", True))
        self.action_base_glow.triggered.connect(self._toggle_base_glow)
        self.tray_menu.addAction(self.action_base_glow)

        self.action_glow = QAction("Enable Audio Overlay Visualizations", self)
        self.action_glow.setCheckable(True)
        self.action_glow.setChecked(self.config.get("glow_enabled", True))
        self.action_glow.triggered.connect(self._toggle_glow)
        self.tray_menu.addAction(self.action_glow)

        self.action_breathing = QAction("Enable Breathing Animation", self)
        self.action_breathing.setCheckable(True)
        self.action_breathing.setChecked(self.config.get("breathing", True))
        self.action_breathing.triggered.connect(self._toggle_breathing)
        self.tray_menu.addAction(self.action_breathing)

        # 🫁 Breathing Target Submenu
        b_target_sub = self._create_sub_menu(self.tray_menu, "🫁 Breathing Target")
        cur_bt = self.config.get("breathing_target", "both")
        bt_grp = QActionGroup(self); bt_grp.setExclusive(True)
        for label, bt_code in [("1. Both (App & Glow)", "both"), ("2. App Only", "app"), ("3. Glow Only", "glow")]:
            act = QAction(label, self)
            act.setCheckable(True)
            bt_grp.addAction(act)
            if cur_bt == bt_code: act.setChecked(True)
            act.triggered.connect(lambda _c, t=bt_code: self._set_config_val("breathing_target", t))
            b_target_sub.addAction(act)

        self.action_mouse = QAction("Enable Mouse Movement Activity", self)
        self.action_mouse.setCheckable(True)
        self.action_mouse.setChecked(self.config.get("mouse_movement_enabled", True))
        self.action_mouse.triggered.connect(self._toggle_mouse_movement)
        self.tray_menu.addAction(self.action_mouse)

        # 🖱️ Mouse Movement Activity Target Submenu
        m_target_sub = self._create_sub_menu(self.tray_menu, "🖱️ Mouse Movement Target")
        cur_mt = self.config.get("mouse_movement_target", "both")
        mt_grp = QActionGroup(self); mt_grp.setExclusive(True)
        for label, mt_code in [("1. Both (App & Glow)", "both"), ("2. App Only", "app"), ("3. Glow Only", "glow")]:
            act = QAction(label, self)
            act.setCheckable(True)
            mt_grp.addAction(act)
            if cur_mt == mt_code: act.setChecked(True)
            act.triggered.connect(lambda _c, t=mt_code: self._set_config_val("mouse_movement_target", t))
            m_target_sub.addAction(act)

        self.action_startup = QAction("Start with Windows", self)
        self.action_startup.setCheckable(True)
        self.action_startup.setChecked(self.config.get("start_with_windows", False))
        self.action_startup.triggered.connect(self._toggle_startup)
        self.tray_menu.addAction(self.action_startup)

        self.tray_menu.addSeparator()

        # 🎨 Color Hue Target Submenu
        color_target_menu = self._create_sub_menu(self.tray_menu, "🎨 Color Hue Target")
        cur_ht = self.config.get("color_hue_target", "both")
        ht_grp = QActionGroup(self); ht_grp.setExclusive(True)
        for label, code in [("Both (App & Glow)", "both"), ("App Only", "app"), ("Glow Only", "glow")]:
            act = QAction(label, self)
            act.setCheckable(True)
            ht_grp.addAction(act)
            if cur_ht == code: act.setChecked(True)
            act.triggered.connect(lambda _c, c=code: self._set_color_hue_target(c))
            color_target_menu.addAction(act)
            
        color_target_menu.addSeparator()
        self.action_link_system_accent = QAction("Link System Accent", self)
        self.action_link_system_accent.setCheckable(True)
        self.action_link_system_accent.setChecked(self.config.get("link_system_accent", False))
        self.action_link_system_accent.triggered.connect(lambda ch: self._set_config_val("link_system_accent", ch))
        color_target_menu.addAction(self.action_link_system_accent)

        # 🎵 Audio Visualizations Submenu (Submenu 3 - Linked to Volume & Frequency)
        audio_fx_menu = self._create_sub_menu(self.tray_menu, "🎵 Audio Visualizations")
        
        # Audio Mode (Driver) Submenu
        av_mode_sub = self._create_sub_menu(audio_fx_menu, "🎛️ Audio Driver Mode")
        cur_av_m = self.config.get("audio_visual_mode", "both")
        av_m_grp = QActionGroup(self); av_m_grp.setExclusive(True)
        for label, m_code in [("1. Both (Volume & Frequency)", "both"), ("2. Volume Only", "volume"), ("3. Frequency Only", "frequency")]:
            act = QAction(label, self)
            act.setCheckable(True)
            av_m_grp.addAction(act)
            if cur_av_m == m_code: act.setChecked(True)
            act.triggered.connect(lambda _c, m=m_code: self._set_config_val("audio_visual_mode", m))
            av_mode_sub.addAction(act)
            
        audio_fx_menu.addSeparator()
        
        cur_fx = self.config.get("audio_effect", "pulsing_aura")
        fx_grp = QActionGroup(self); fx_grp.setExclusive(True)
        fx_items = [
            ("Pulsing Aura (Classic)", "pulsing_aura"),
            ("Chroma Pulse (Rainbow Shift)", "chroma_pulse"),
            ("Equalizer Ring (24 Spectrum Bars)", "equalizer_ring"),
            ("Waveform Orbit (Oscillating Ring)", "waveform_orbit"),
            ("Frequency Ripple (Shockwaves)", "frequency_ripple"),
            ("Particle Spark (12 Beat Orbs)", "particle_spark")
        ]
        for label, code in fx_items:
            act = QAction(label, self)
            act.setCheckable(True)
            fx_grp.addAction(act)
            if cur_fx == code: act.setChecked(True)
            act.triggered.connect(lambda _c, c=code: self._set_audio_effect(c))
            audio_fx_menu.addAction(act)

        
        self.tray_menu.addSeparator()

        # Sliders
        # Opacity
        oc = QWidget()
        ol = QHBoxLayout(oc); ol.setContentsMargins(12, 4, 12, 4)
        ol.addWidget(self._lbl("App Opacity:", "#d1d5db"))
        self.op_slider = QSlider(Qt.Horizontal); self.op_slider.setRange(0, 100)
        self.op_slider.setValue(int(self.config.get("opacity", 0.9) * 100))
        self.op_slider.setFixedWidth(100); self.op_slider.setStyleSheet(SLIDER_SS)
        self.op_slider.valueChanged.connect(self._on_opacity)
        ol.addWidget(self.op_slider)
        self.op_val = self._lbl(f"{int(self.config.get('opacity', 0.9)*100)}%", "#00d2ff")
        ol.addWidget(self.op_val)
        ow = QWidgetAction(self); ow.setDefaultWidget(oc); self.tray_menu.addAction(ow)

        # Glow Opacity
        goc = QWidget()
        gol = QHBoxLayout(goc); gol.setContentsMargins(12, 4, 12, 4)
        gol.addWidget(self._lbl("Glow Opacity:", "#d1d5db"))
        self.gop_slider = QSlider(Qt.Horizontal); self.gop_slider.setRange(0, 100)
        self.gop_slider.setValue(int(self.config.get("glow_opacity", 0.9) * 100))
        self.gop_slider.setFixedWidth(100); self.gop_slider.setStyleSheet(SLIDER_SS)
        self.gop_slider.valueChanged.connect(self._on_glow_opacity)
        gol.addWidget(self.gop_slider)
        self.gop_val = self._lbl(f"{int(self.config.get('glow_opacity', 0.9)*100)}%", "#00d2ff")
        gol.addWidget(self.gop_val)
        gow = QWidgetAction(self); gow.setDefaultWidget(goc); self.tray_menu.addAction(gow)

        # Glow Size
        gsc = QWidget()
        gsl = QHBoxLayout(gsc); gsl.setContentsMargins(12, 4, 12, 4)
        gsl.addWidget(self._lbl("Glow Size:", "#d1d5db"))
        self.gsz_slider = QSlider(Qt.Horizontal); self.gsz_slider.setRange(0, 100)
        self.gsz_slider.setValue(self.config.get("glow_size_pct", 50))
        self.gsz_slider.setFixedWidth(100); self.gsz_slider.setStyleSheet(SLIDER_SS)
        self.gsz_slider.valueChanged.connect(self._on_glow_size)
        gsl.addWidget(self.gsz_slider)
        self.gsz_val = self._lbl(f"{self.config.get('glow_size_pct', 50)}%", "#00d2ff")
        gsl.addWidget(self.gsz_val)
        gsw = QWidgetAction(self); gsw.setDefaultWidget(gsc); self.tray_menu.addAction(gsw)

        # Hue
        hc = QWidget()
        hl = QHBoxLayout(hc); hl.setContentsMargins(12, 4, 12, 4)
        hl.addWidget(self._lbl("Color Hue:", "#d1d5db"))
        self.hue_slider = QSlider(Qt.Horizontal); self.hue_slider.setRange(0, 360)
        self.hue_slider.setValue(self.config.get("hue", 190))
        self.hue_slider.setFixedWidth(100); self.hue_slider.setStyleSheet(SLIDER_SS)
        self.hue_slider.valueChanged.connect(self._on_hue)
        hl.addWidget(self.hue_slider)
        self.hue_val = self._lbl(f"{self.config.get('hue', 190)}°", "#00d2ff")
        hl.addWidget(self.hue_val)
        hw = QWidgetAction(self); hw.setDefaultWidget(hc); self.tray_menu.addAction(hw)

        # Breathing Speed
        bsc = QWidget()
        bsl = QHBoxLayout(bsc); bsl.setContentsMargins(12, 4, 12, 4)
        bsl.addWidget(self._lbl("Breathing Speed:", "#d1d5db"))
        self.bspeed_slider = QSlider(Qt.Horizontal); self.bspeed_slider.setRange(1, 100)
        self.bspeed_slider.setValue(self.config.get("breathing_speed", 50))
        self.bspeed_slider.setFixedWidth(100); self.bspeed_slider.setStyleSheet(SLIDER_SS)
        self.bspeed_slider.valueChanged.connect(self._on_breathing_speed)
        bsl.addWidget(self.bspeed_slider)
        self.bspeed_val = self._lbl(f"{self.config.get('breathing_speed', 50)}%", "#00d2ff")
        bsl.addWidget(self.bspeed_val)
        bsw = QWidgetAction(self); bsw.setDefaultWidget(bsc); self.tray_menu.addAction(bsw)

        # Size
        sc = QWidget()
        sl = QHBoxLayout(sc); sl.setContentsMargins(12, 4, 12, 4)
        sl.addWidget(self._lbl("App Size:", "#d1d5db"))
        self.sz_slider = QSlider(Qt.Horizontal); self.sz_slider.setRange(0, 100)
        self.sz_slider.setValue(self.config.get("size_pct", 50))
        self.sz_slider.setFixedWidth(100); self.sz_slider.setStyleSheet(SLIDER_SS)
        self.sz_slider.valueChanged.connect(self._on_size)
        sl.addWidget(self.sz_slider)
        self.sz_val = self._lbl(f"{self.config.get('size_pct', 50)}%", "#00d2ff")
        sl.addWidget(self.sz_val)
        sw = QWidgetAction(self); sw.setDefaultWidget(sc); self.tray_menu.addAction(sw)

        self.tray_menu.addSeparator()

        for hint in ("● Left Click   — Outer: Win Cycle  Center: Quick Switch",
                     "● Right Click  — Outer: Tab Cycle  Center: Tab Switch",
                     "● Middle Click — Outer: Screenshot Center: Rec On/Off"):
            a = QAction(hint, self); a.setEnabled(False); self.tray_menu.addAction(a)

        self.tray_menu.addSeparator()
        qa = QAction("Quit Allme", self)
        qa.triggered.connect(QApplication.quit)
        self.tray_menu.addAction(qa)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self._on_tray)
        self.tray_icon.show()

    def _lbl(self, text, color):
        l = QLabel(text)
        l.setStyleSheet(f"color:{color}; font-size:11px; font-weight:bold;")
        return l

    def _toggle_ontop(self, checked):
        self.config["always_on_top"] = checked
        save_config(self.config)
        self._enforce_always_on_top()

    def _toggle_base_glow(self, checked):
        self.config["base_glow_enabled"] = checked
        save_config(self.config)
        self.button.update()

    def _toggle_glow(self, checked):
        self.config["glow_enabled"] = checked
        save_config(self.config)
        self.button.update()

    def _toggle_breathing(self, checked):
        self.config["breathing"] = checked
        save_config(self.config)
        self.button.update()

    def _toggle_mouse_movement(self, checked):
        self.config["mouse_movement_enabled"] = checked
        save_config(self.config)
        self.button.update()

    def _toggle_startup(self, checked):
        self.config["start_with_windows"] = checked
        save_config(self.config)
        set_startup(checked)

    def _set_color_hue_target(self, target):
        self.config["color_hue_target"] = target
        save_config(self.config)
        self.button.update()

    def _set_audio_effect(self, effect):
        self.config["audio_effect"] = effect
        save_config(self.config)
        self.button.update()

    def _set_telemetry_source(self, source):
        self.config["telemetry_source"] = source
        save_config(self.config)
        self.button.update()

    def _set_telemetry_target(self, target):
        self.config["telemetry_target"] = target
        save_config(self.config)
        self.button.update()

    def _set_config_val(self, key, val):
        self.config[key] = val
        save_config(self.config)
        self.button.update()

    def _on_opacity(self, v):
        self.config["opacity"] = v / 100.0
        save_config(self.config)
        self.op_val.setText(f"{v}%")
        self.button.update()

    def _on_glow_opacity(self, v):
        self.config["glow_opacity"] = v / 100.0
        save_config(self.config)
        self.gop_val.setText(f"{v}%")
        self.button.update()

    def _on_glow_size(self, v):
        self.config["glow_size_pct"] = v
        save_config(self.config)
        self.gsz_val.setText(f"{v}%")
        self.button.update()

    def _on_hue(self, v):
        self.config["hue"] = v
        save_config(self.config)
        self.hue_val.setText(f"{v}°")
        self.button.update()

    def _on_breathing_speed(self, v):
        self.config["breathing_speed"] = v
        save_config(self.config)
        self.bspeed_val.setText(f"{v}%")
        self.button.update()

    def _on_size(self, v):
        self.config["size_pct"] = v
        save_config(self.config)
        self.sz_val.setText(f"{v}%")
        base_size = int(32 + 56 * (v / 100.0))
        size_px = base_size + 280
        self.setFixedSize(size_px, size_px)
        self.button.update()

    def show_dashboard(self):
        if not hasattr(self, 'dashboard_window'):
            self.dashboard_window = DashboardWindow(self)
        self.dashboard_window.show()
        self.dashboard_window.raise_()
        self.dashboard_window.activateWindow()

    def _on_tray(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.isVisible(): self.hide()
            else: self.show(); self.raise_()

    def closeEvent(self, event):
        if hasattr(self, "audio_mon"):
            self.audio_mon.running = False
        if hasattr(self, "telemetry_mon"):
            self.telemetry_mon.running = False
        if hasattr(self, "mouse_hook") and self.mouse_hook:
            self.mouse_hook.uninstall()
        if hasattr(self, "keyboard_hook") and self.keyboard_hook:
            self.keyboard_hook.uninstall()
        super().closeEvent(event)

# =============================================================================
#  Entry Point
# =============================================================================
if __name__ == "__main__":
    try:
        kill_previous_instances()
        time.sleep(0.1)

        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)

        w = AllmeWidget()
        sys.exit(app.exec_())
    except Exception as e:
        log_crash_report(type(e), e, e.__traceback__)
        raise e
