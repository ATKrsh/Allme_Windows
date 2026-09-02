import re
import ast

with open('allme.py', 'r', encoding='utf-8') as f:
    text = f.read()

print("--- SEARCHING FOR MENUS & ACTIONS ---")
for i, line in enumerate(text.split('\n'), 1):
    if any(k in line for k in ['addAction', 'addMenu', 'QAction', 'PersistentMenu', 'create_sub_menu', '_setup_tray']):
        print(f"L{i}: {line.strip().encode('ascii', 'replace').decode('ascii')}")
