import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSize, Qt, QRectF, QPointF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QPen, QBrush

sys.path.insert(0, os.path.dirname(__file__))
import allme

def generate_screenshots():
    app = QApplication(sys.argv)
    
    widget = allme.AllmeWidget()
    widget.show()
    app.processEvents()
    
    # Process animation frames
    for _ in range(25):
        widget._update_animation()
        widget.button.update()
        app.processEvents()
        
    raw_pix = widget.button.grab()
    
    # Create a sleek dark backdrop container for the widget image
    canvas_w = raw_pix.width()
    canvas_h = raw_pix.height() + 40
    
    composite = QPixmap(canvas_w, canvas_h)
    composite.fill(Qt.transparent)
    
    p = QPainter(composite)
    p.setRenderHint(QPainter.Antialiasing)
    
    # Draw sleek dark card background
    p.setBrush(QBrush(QColor(24, 28, 38)))
    p.setPen(QPen(QColor(56, 68, 90), 2))
    p.drawRoundedRect(QRectF(10, 10, canvas_w - 20, canvas_h - 20), 12, 12)
    
    # Draw raw widget pixmap
    p.drawPixmap(0, 0, raw_pix)
    
    # Draw clear zone labels at bottom
    font = QFont("Segoe UI", 9, QFont.Bold)
    p.setFont(font)
    
    p.setPen(QPen(QColor(0, 210, 255)))
    p.drawText(QRectF(20, canvas_h - 40, (canvas_w - 40) / 3, 25), Qt.AlignCenter, "◄ Left Sector")
    
    p.setPen(QPen(QColor(255, 255, 255)))
    p.drawText(QRectF(20 + (canvas_w - 40) / 3, canvas_h - 40, (canvas_w - 40) / 3, 25), Qt.AlignCenter, "● Center Core")
    
    p.setPen(QPen(QColor(0, 210, 255)))
    p.drawText(QRectF(20 + 2 * (canvas_w - 40) / 3, canvas_h - 40, (canvas_w - 40) / 3, 25), Qt.AlignCenter, "Right Sector ►")
    
    p.end()
    
    composite.save("widget_preview.png")
    print("Saved enhanced widget_preview.png")
    
    # 2. Dashboard Snapshot
    dash = allme.DashboardWindow(widget)
    dash.show()
    app.processEvents()
    pix_dash = dash.grab()
    pix_dash.save("dashboard_preview.png")
    print("Saved dashboard_preview.png")
    
    # 3. Menu Snapshot
    if hasattr(widget, 'tray_menu'):
        widget.tray_menu.show()
        app.processEvents()
        pix_menu = widget.tray_menu.grab()
        pix_menu.save("menu_preview.png")
        print("Saved menu_preview.png")

if __name__ == '__main__':
    generate_screenshots()
