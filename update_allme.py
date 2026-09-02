import os
import re

with open('allme.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove telemetry config defaults
code = re.sub(r'\s*"telemetry_source":\s*".*?",?\n', '\n', code)
code = re.sub(r'\s*"telemetry_target":\s*".*?",?\n', '\n', code)
code = re.sub(r'\s*"hdd_drive":\s*".*?",?\n', '\n', code)
code = re.sub(r'\s*"hdd_mode":\s*".*?",?\n', '\n', code)
code = re.sub(r'\s*"net_mode":\s*".*?",?\n', '\n', code)
code = re.sub(r'\s*"gpu_choice":\s*".*?",?\n', '\n', code)

# 2. Remove Telemetry Links box from DashboardWindow
code = re.sub(r'# --- TELEMETRY ---.*?\n\s*grp2 = QGroupBox\("Telemetry Links"\); grp2\.setLayout\(v2\); grid\.addWidget\(grp2, 0, 1\)\n', '', code, flags=re.DOTALL)

# 3. Remove Link Source & Link Sink submenus from _setup_tray
code = re.sub(r'# 📊 Submenu 4: Renamed to "Link Source".*?target_menu\.addAction\(act\)\n', '', code, flags=re.DOTALL)

# 4. Remove _set_telemetry_source & _set_telemetry_target methods if present
code = re.sub(r'\s*def _set_telemetry_source\(self, src\):.*?\n\s*self\.button\.update\(\)\n', '\n', code, flags=re.DOTALL)
code = re.sub(r'\s*def _set_telemetry_target\(self, tgt\):.*?\n\s*self\.button\.update\(\)\n', '\n', code, flags=re.DOTALL)

with open('allme.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("allme.py updated cleanly (Link Source & Link Sink removed).")
