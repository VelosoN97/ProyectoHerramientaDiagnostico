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

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PC Medicine")
        self.setMinimumSize(1050, 650)

        self.create_interface()
        self.refresh_information()

    def create_interface(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        #Creacion menu lateral

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(230)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 25, 20, 20)

        logo = QLabel("✚ PC MEDICINE")
        logo.setObjectName("logo")

        subtitle = QLabel("ADVANCED DIAGNOSTICS")
        subtitle.setObjectName("subtitle")

        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(subtitle)
        sidebar_layout.addSpacing(35)

        menu_items = [
            "Dashboard",
            "Hardware",
            "Monitoreo",
            "Diagnostico",
            "Blue Screen",
            "Discos",
            "Informes"
        ]

        for item in menu_items:
            button = QPushButton(item)
            button.setObjectName("menuButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        version = QLabel("PC Medicine v0.1")
        version.setObjectName("subtitle")
        sidebar_layout.addWidget(version)

        #creacion panel principal

        content = QWidget()
        content.setObjectName("content")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(35, 30, 35, 30)
        content_layout.setSpacing(20)

        header = QHBoxLayout()

        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")

        self.status_label = QLabel("Estado del Equipo: Revisando")
        self.status_label.setObjectName("statusLabel")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.status_label)

        content_layout.addLayout(header)

        welcome = QLabel(
            "Bienvenido a PC Medicine. "
            "Supervisa la salud de tu computador."
        )
        welcome.setObjectName("description")

        content_layout.addWidget(welcome)

        #mostrar informacion del equipo

        info_card = QFrame()
        info_card.setObjectName("infoCard")

        info_layout = QVBoxLayout(info_card)

        info_title = QLabel("INFORMACION DEL EQUIPO")
        info_title.setObjectName("sectionTitle")

        self.computer_name = QLabel()
        self.operating_system = QLabel()
        self.architecture = QLabel()

        info_layout.addWidget(info_title)
        info_layout.addWidget(self.computer_name)
        info_layout.addWidget(self.operating_system)
        info_layout.addWidget(self.architecture)

        content_layout.addWidget(info_card)

        #tarjetas de monitoreo

        cards_layout = QHBoxLayout()

        self.cpu_card = DiagnosticCard(
            "PROCESADOR",
            "0%",
            "Uso actual de CPU"
        )

        self.ram_card = DiagnosticCard(
            "MEMORIA RAM",
            "0%",
            "Uso de memoria"
        )

        self.disk_card =  DiagnosticCard(
            "ALMACENAMIENTO",
            "0%",
            "Espacio utilizado"
        )

        cards_layout.addWidget(self.cpu_card)
        cards_layout.addWidget(self.ram_card)
        cards_layout.addWidget(self.disk_card)

        content_layout.addLayout(cards_layout)

        #creacion de boton de actualizacion

        refresh_button = QPushButton("Actualizar diagnostico")
        refresh_button.setObjectName("refreshButton")
        refresh_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        refresh_button.clicked.connect(
            self.refresh_information
        )

        content_layout.addWidget(refresh_button)

        content_layout.addStretch()

        footer = QLabel(
            "PC Medicine | Diagnostico y monitoreo informatico"
        )
        footer.setObjectName("subtitle")

        content_layout.addWidget(footer)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        self.apply_styles()

    def refresh_information(self):
        try:
            #Informacion del equipo
            self.computer_name.setText(
                f"Nombre del equipo: {platform.node()}"
            )

            self.operating_system.setText(
                f"Sistema operativo: "
                f"{platform.system()} {platform.release()}"
            )

            self.architecture.setText(
                f"Arquitectura: {platform.machine()}"
            )

            #Uso del procesador

            cpu = psutil.cpu_percent(interval=0.5)

            self.cpu_card.update_card(
                f"{cpu:.1f}%",
                int(cpu)
            )

            #uso de memoria ram

            memory = psutil.virtual_memory()

            self.ram_card.update_card(
                f"{memory.percent:.1f}%",
                int(memory.percent)
            )

            #almacenamiento

            disk = psutil.disk_usage("C:\\")

            self.disk_card.update_card(
                f"{disk.percent:.1f}%",
                int(disk.percent)
            )

            self.status_label.setText(
                "Estado del equipo: Monitoreo activo"
            )

        except Exception as error:
            QMessageBox.warning(
                self,
                "Error de diagnostico",
                f"No se pudo obtener toda la informacion: {error}"
            )