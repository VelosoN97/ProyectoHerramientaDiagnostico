import platform
import psutil 

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt

class DiagnosticCard(QFrame):
    def __init__(self, title, value, description):
        super().__init__()

        self.setObjectName("diagnosticCard")

        layout = QVBoxLayout(self)

        self.title = QLabel(title)
        self.title.setObjectName("cardTitle")

        self.value = QLabel(value)
        self.value.setObjectName("cardValue")

        self.description = QLabel(description)
        self.value.setObjectName("cardDescription")

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(7)

        layout.addWidget(self.title)
        layout.addWidget(self.value)
        layout.addWidget(self.description)
        layout.addWidget(self.progress)

        layout.setSpacing(12)

    def update_card(self, value, percentage):
        self.value.setText(value)
        self.progress.setValue(percentage)