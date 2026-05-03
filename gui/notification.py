from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer

class NotificationPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.msg_label = QLabel("...", self)
        self.msg_label.setStyleSheet("""
            QLabel {
                background-color: rgba(30, 33, 39, 240);
                color: #98c379;
                padding: 12px 20px;
                border-radius: 8px 8px 0 0;
                border: 1px solid #98c379;
                font-family: 'Consolas', sans-serif;
                font-size: 14px;
            }
        """)
        
        self.status_label = QLabel("...", self)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #98c379;
                color: #1e2127;
                padding: 4px;
                border-radius: 0 0 8px 8px;
                font-size: 10px;
                font-weight: bold;
            }
        """)
        self.status_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.msg_label)
        layout.addWidget(self.status_label)
        self.setLayout(layout)
        self.timer = QTimer(self); self.timer.timeout.connect(self.hide)

    def show_message(self, old, new, title, func, worker):
        self.msg_label.setText(f"[{title}]\n{old} -> {new}")
        self.status_label.setText(f"FUNC: {func} | MODE: {worker}")
        self.adjustSize()
        screen = self.screen().availableGeometry()
        self.move(screen.width() - self.width() - 20, screen.height() - self.height() - 50)
        self.show(); self.timer.start(2500)