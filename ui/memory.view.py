from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QTableWidget, QTableWidgetItem, 
    QHeaderView, QMessageBox
)

from PySide6.QtCore import Qt

from modules.memory import (
    get_memory_summary,
    get_physical_memory,
    get_top_processes,
    get_memory_status
)

class MemoryView(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PC Medicine - Memory Analyzer")
        self.setMinimumSize(950, 650)

        self.create_interface()
        self.refresh_memory()

    def create_interface(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)

        #encabezado

        title = QLabel("Memory Analyzer")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Analisis y monitoreo de memoria RAM"
        )
        description.setObjectName("description")

        main_layout.addWidget(title)
        main_layout.addWidget(description)