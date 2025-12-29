import sys
import requests
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


API_URL = "http://127.0.0.1:8000/start"


class LanaOverlay(QLabel):
    def __init__(self):
        super().__init__("Lana · Click to listen")

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 160);
                padding: 14px 28px;
                border-radius: 20px;
                font-weight: bold;
            }
        """)

        self.setFont(QFont("SF Pro", 14))
        self.adjustSize()
        self.move_to_top_center()

    def move_to_top_center(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = 40
        self.move(x, y)

    def mousePressEvent(self, event):
        self.setText("🎙 Listening...")
        QApplication.processEvents()

        try:
            r = requests.post(API_URL, timeout=2)
            if r.ok:
                self.setText("Lana · Click to listen")
            else:
                self.setText("⚠️ Lana error")
        except Exception:
            self.setText("❌ Lana offline")


def main():
    app = QApplication(sys.argv)
    overlay = LanaOverlay()
    overlay.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

