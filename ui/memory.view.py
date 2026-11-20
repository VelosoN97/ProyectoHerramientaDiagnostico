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

        #tarjetas de informacion

        cards_layout = QHBoxLayout()

        self.total_label = self.create_card(
            cards_layout,
            "RAM TOTAL"
        )

        self.used_label = self.create_card(
            cards_layout,
            "RAM UTILIZADA"
        )

        self.available_label = self.create_card(
            cards_layout,
            "RAM DISPONIBLE"
        )

        self.percent_label = self.create_card(
            cards_layout,
            "USO DE MEMORIA"
        )

        main_layout.addLayout(cards_layout)

        #estados de memoria

        status_frame = QFrame()
        status_frame.setObjectName("statusFrame")

        status_layout = QHBoxLayout(status_frame)

        status_title = QLabel("Estado de memoria")
        status_title.setObjectName("sectionTitle")

        self.status_label = QLabel("Analizando...")
        self.status_label.setObjectName("statusLabel")

        status_layout.addWidget(status_title)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()

        main_layout.addWidget(status_frame)

        #informacion fisica

        physical_frame = QFrame()
        physical_frame.setObjectName("statusFrame")

        physical_layout = QVBoxLayout(physical_frame)

        physical_title = QLabel(
            "INFORMACION DE MEMORIA FISICA"
        )
        physical_title.setObjectName("sectionTitle")

        self.physical_label = QLabel(
            "Obteniendo informacion..."
        )
        self.physical_label.setObjectName("description")

        physical_layout.addWidget(physical_title)
        physical_layout.addWidget(self.physical_label)

        main_layout.addWidget(physical_frame)