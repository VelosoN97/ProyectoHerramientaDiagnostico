
import platform
import psutil

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QProgressBar,
    QMessageBox,
    QStackedWidget
)

from PySide6.QtCore import Qt

from ui.memory_view import MemoryView


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
        self.description.setObjectName("cardDescription")

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

        # MENU LATERAL

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(230)

        sidebar_layout = QVBoxLayout(sidebar)

        sidebar_layout.setContentsMargins(
            20, 25, 20, 20
        )

        logo = QLabel("✚ PC MEDICINE")
        logo.setObjectName("logo")

        subtitle = QLabel("ADVANCED DIAGNOSTICS")
        subtitle.setObjectName("subtitle")

        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(subtitle)
        sidebar_layout.addSpacing(35)

        # CONTENEDOR DE PANTALLAS

        self.pages = QStackedWidget()

        # CREAR DASHBOARD

        self.dashboard_page = self.create_dashboard_page()

        # CREAR MEMORY ANALYZER

        self.memory_page = MemoryView()

        # AGREGAR PANTALLAS

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.memory_page)

        # OPCIONES DEL MENU

        menu_items = [
            "Dashboard",
            "Memory Analyzer",
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

            button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

            button.clicked.connect(
                lambda checked=False, name=item:
                self.navigate_to(name)
            )

            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        version = QLabel("PC Medicine v0.2")
        version.setObjectName("subtitle")

        sidebar_layout.addWidget(version)

        # AGREGAR ELEMENTOS PRINCIPALES

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

        self.apply_styles()

    def create_dashboard_page(self):

        content = QWidget()
        content.setObjectName("content")

        content_layout = QVBoxLayout(content)

        content_layout.setContentsMargins(
            35, 30, 35, 30
        )

        content_layout.setSpacing(20)

        # ENCABEZADO

        header = QHBoxLayout()

        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")

        self.status_label = QLabel(
            "Estado del equipo: Revisando"
        )

        self.status_label.setObjectName("statusLabel")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.status_label)

        content_layout.addLayout(header)

        # BIENVENIDA

        welcome = QLabel(
            "Bienvenido a PC Medicine. "
            "Supervisa la salud de tu computador."
        )

        welcome.setObjectName("description")

        content_layout.addWidget(welcome)

        # INFORMACION DEL EQUIPO

        info_card = QFrame()
        info_card.setObjectName("infoCard")

        info_layout = QVBoxLayout(info_card)

        info_title = QLabel(
            "INFORMACION DEL EQUIPO"
        )

        info_title.setObjectName("sectionTitle")

        self.computer_name = QLabel()
        self.operating_system = QLabel()
        self.architecture = QLabel()

        info_layout.addWidget(info_title)
        info_layout.addWidget(self.computer_name)
        info_layout.addWidget(self.operating_system)
        info_layout.addWidget(self.architecture)

        content_layout.addWidget(info_card)

        # TARJETAS DE MONITOREO

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

        self.disk_card = DiagnosticCard(
            "ALMACENAMIENTO",
            "0%",
            "Espacio utilizado"
        )

        cards_layout.addWidget(self.cpu_card)
        cards_layout.addWidget(self.ram_card)
        cards_layout.addWidget(self.disk_card)

        content_layout.addLayout(cards_layout)

        # BOTON ACTUALIZAR

        refresh_button = QPushButton(
            "Actualizar diagnostico"
        )

        refresh_button.setObjectName("refreshButton")

        refresh_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        refresh_button.clicked.connect(
            self.refresh_information
        )

        content_layout.addWidget(refresh_button)

        content_layout.addStretch()

        # PIE DE PAGINA

        footer = QLabel(
            "PC Medicine | Diagnostico y monitoreo informatico"
        )

        footer.setObjectName("subtitle")

        content_layout.addWidget(footer)

        return content

    def navigate_to(self, page_name):

        if page_name == "Dashboard":

            self.pages.setCurrentWidget(
                self.dashboard_page
            )

            self.refresh_information()

        elif page_name == "Memory Analyzer":

            self.pages.setCurrentWidget(
                self.memory_page
            )

            self.memory_page.refresh_memory()

        else:

            QMessageBox.information(
                self,
                "Modulo en desarrollo",
                f"El modulo {page_name} "
                "todavia se encuentra en desarrollo."
            )

    def refresh_information(self):

        try:

            # INFORMACION DEL EQUIPO

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

            # USO DEL PROCESADOR

            cpu = psutil.cpu_percent(interval=0.5)

            self.cpu_card.update_card(
                f"{cpu:.1f}%",
                int(cpu)
            )

            # USO DE MEMORIA RAM

            memory = psutil.virtual_memory()

            self.ram_card.update_card(
                f"{memory.percent:.1f}%",
                int(memory.percent)
            )

            # ALMACENAMIENTO

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
                f"No se pudo obtener toda "
                f"la informacion: {error}"
            )

    def apply_styles(self):

        self.setStyleSheet("""

            QMainWindow {
                background-color: #101C30;
            }

            #sidebar {
                background-color: #0B1525;
            }

            #logo {
                color: #55C8FF;
                font-size: 21px;
                font-weight: bold;
            }

            #subtitle {
                color: #8295AC;
                font-size: 10px;
            }

            #menuButton {
                background-color: transparent;
                color: #B9C9DA;
                text-align: left;
                border: none;
                padding: 13px;
                border-radius: 7px;
                font-size: 13px;
            }

            #menuButton:hover {
                background-color: #183B5B;
                color: white;
            }

            #content {
                background-color: #101C30;
            }

            #pageTitle {
                color: white;
                font-size: 27px;
                font-weight: bold;
            }

            #description {
                color: #9AADC2;
                font-size: 13px;
            }

            #statusLabel {
                color: #55C8FF;
                font-size: 12px;
            }

            #infoCard, #diagnosticCard {
                background-color: #192A40;
                border: 1px solid #29415C;
                border-radius: 12px;
                padding: 12px;
            }

            #infoCard QLabel {
                color: #D5E2EF;
                font-size: 12px;
            }

            #sectionTitle, #cardTitle {
                color: #55C8FF;
                font-weight: bold;
                font-size: 12px;
            }

            #cardValue {
                color: white;
                font-size: 25px;
                font-weight: bold;
            }

            #cardDescription {
                color: #9AADC2;
                font-size: 11px;
            }

            QProgressBar {
                background-color: #293D54;
                border: none;
                border-radius: 3px;
            }

            QProgressBar::chunk {
                background-color: #55C8FF;
                border-radius: 3px;
            }

            #refreshButton {
                background-color: #1676AE;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 12px;
                font-weight: bold;
            }

            #refreshButton:hover {
                background-color: #2196D2;
            }

        """)
