
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
    QMessageBox
)

from PySide6.QtCore import Qt

from modules.hardware import get_hardware_info


class HardwareCard(QFrame):

    def __init__(self, title, value, description):
        super().__init__()

        self.setObjectName("hardwareCard")

        layout = QVBoxLayout(self)

        self.title = QLabel(title)
        self.title.setObjectName("hardwareCardTitle")

        self.value = QLabel(value)
        self.value.setObjectName("hardwareCardValue")
        self.value.setWordWrap(True)

        self.description = QLabel(description)
        self.description.setObjectName("hardwareCardDescription")
        self.description.setWordWrap(True)

        layout.addWidget(self.title)
        layout.addWidget(self.value)
        layout.addWidget(self.description)

        layout.setSpacing(10)

    def update_card(self, value):
        self.value.setText(str(value))


class HardwareView(QWidget):

    def __init__(self):
        super().__init__()

        self.create_interface()
        self.refresh_hardware()

    def create_interface(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)

        # CONTENEDOR CON SCROLL

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()

        self.content_layout = QVBoxLayout(content)

        self.content_layout.setContentsMargins(
            35, 30, 35, 30
        )

        self.content_layout.setSpacing(20)

        scroll.setWidget(content)

        main_layout.addWidget(scroll)

        # ENCABEZADO

        header = QHBoxLayout()

        title = QLabel("Hardware")
        title.setObjectName("hardwarePageTitle")

        self.status_label = QLabel(
            "Estado: Detectando componentes..."
        )

        self.status_label.setObjectName("hardwareStatus")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.status_label)

        self.content_layout.addLayout(header)

        description = QLabel(
            "Informacion detallada de los componentes fisicos "
            "de tu computador."
        )

        description.setObjectName("hardwareDescription")

        self.content_layout.addWidget(description)

        # TARJETAS RESUMEN

        cards_layout = QHBoxLayout()

        self.cpu_card = HardwareCard(
            "PROCESADOR",
            "Detectando...",
            "Modelo del procesador"
        )

        self.ram_card = HardwareCard(
            "MEMORIA RAM",
            "Detectando...",
            "Capacidad detectada"
        )

        self.gpu_card = HardwareCard(
            "GRAFICOS",
            "Detectando...",
            "Tarjeta grafica"
        )

        self.disk_card = HardwareCard(
            "ALMACENAMIENTO",
            "Detectando...",
            "Unidades detectadas"
        )

        cards_layout.addWidget(self.cpu_card)
        cards_layout.addWidget(self.ram_card)
        cards_layout.addWidget(self.gpu_card)
        cards_layout.addWidget(self.disk_card)

        self.content_layout.addLayout(cards_layout)

        # SECCIONES DE COMPONENTES

        self.cpu_section = self.create_section(
            "PROCESADOR"
        )

        self.motherboard_section = self.create_section(
            "PLACA MADRE"
        )

        self.bios_section = self.create_section(
            "BIOS"
        )

        self.gpu_section = self.create_section(
            "TARJETA GRAFICA"
        )

        self.ram_section = self.create_section(
            "MODULOS DE MEMORIA RAM"
        )

        self.disk_section = self.create_section(
            "UNIDADES DE ALMACENAMIENTO"
        )

        self.system_section = self.create_section(
            "INFORMACION DEL SISTEMA"
        )

        # BOTON ACTUALIZAR

        self.refresh_button = QPushButton(
            "Actualizar informacion del hardware"
        )

        self.refresh_button.setObjectName(
            "hardwareRefreshButton"
        )

        self.refresh_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.refresh_button.clicked.connect(
            self.refresh_hardware
        )

        self.content_layout.addWidget(
            self.refresh_button
        )

        # ULTIMA ACTUALIZACION

        self.update_label = QLabel(
            "Esperando deteccion..."
        )

        self.update_label.setObjectName(
            "hardwareUpdateLabel"
        )

        self.content_layout.addWidget(
            self.update_label
        )

        self.content_layout.addStretch()

        self.apply_styles()

    def create_section(self, title):

        section = QFrame()
        section.setObjectName("hardwareSection")

        layout = QVBoxLayout(section)

        layout.setContentsMargins(
            18, 15, 18, 15
        )

        section_title = QLabel(title)

        section_title.setObjectName(
            "hardwareSectionTitle"
        )

        layout.addWidget(section_title)

        self.content_layout.addWidget(section)

        return layout

    def clear_section(self, section):

        # CONSERVAR EL TITULO DE LA SECCION

        while section.count() > 1:

            item = section.takeAt(1)

            if item.layout():

                row = item.layout()

                while row.count():

                    child = row.takeAt(0)

                    if child.widget():
                        child.widget().deleteLater()

            elif item.widget():

                item.widget().deleteLater()

    def add_information(self, section, label, value):

        row = QHBoxLayout()

        name = QLabel(f"{label}:")

        name.setObjectName("hardwareInfoLabel")

        result = QLabel(str(value))

        result.setObjectName("hardwareInfoValue")
        result.setWordWrap(True)

        result.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        row.addWidget(name, 1)
        row.addWidget(result, 2)

        section.addLayout(row)

    def refresh_hardware(self):

        self.refresh_button.setEnabled(False)

        self.refresh_button.setText(
            "Analizando hardware..."
        )

        self.status_label.setText(
            "Estado: Analizando componentes..."
        )

        self.update_label.setText(
            "Obteniendo informacion del equipo..."
        )

        QApplication.processEvents()

        try:

            hardware = get_hardware_info()

            # LIMPIAR INFORMACION ANTERIOR

            sections = [
                self.cpu_section,
                self.motherboard_section,
                self.bios_section,
                self.gpu_section,
                self.ram_section,
                self.disk_section,
                self.system_section
            ]

            for section in sections:
                self.clear_section(section)

            # PROCESADOR

            cpus = hardware["cpu"]

            if cpus:

                cpu = cpus[0]

                self.cpu_card.update_card(
                    cpu["name"]
                )

                self.add_information(
                    self.cpu_section,
                    "Modelo",
                    cpu["name"]
                )

                self.add_information(
                    self.cpu_section,
                    "Fabricante",
                    cpu["manufacturer"]
                )

                self.add_information(
                    self.cpu_section,
                    "Nucleos",
                    cpu["cores"]
                )

                self.add_information(
                    self.cpu_section,
                    "Hilos",
                    cpu["threads"]
                )

                self.add_information(
                    self.cpu_section,
                    "Frecuencia maxima",
                    f'{cpu["max_frequency"]} MHz'
                )

            else:

                self.cpu_card.update_card("No detectado")

                self.add_information(
                    self.cpu_section,
                    "Estado",
                    "No se encontro informacion"
                )

            # PLACA MADRE

            boards = hardware["motherboard"]

            if boards:

                board = boards[0]

                self.add_information(
                    self.motherboard_section,
                    "Fabricante",
                    board["manufacturer"]
                )

                self.add_information(
                    self.motherboard_section,
                    "Modelo",
                    board["product"]
                )

                self.add_information(
                    self.motherboard_section,
                    "Version",
                    board["version"]
                )

            else:

                self.add_information(
                    self.motherboard_section,
                    "Estado",
                    "No se detecto informacion"
                )

            # BIOS

            bios_list = hardware["bios"]

            if bios_list:

                bios = bios_list[0]

                self.add_information(
                    self.bios_section,
                    "Fabricante",
                    bios["manufacturer"]
                )

                self.add_information(
                    self.bios_section,
                    "Version",
                    bios["version"]
                )

                self.add_information(
                    self.bios_section,
                    "Fecha",
                    bios["release_date"]
                )

            else:

                self.add_information(
                    self.bios_section,
                    "Estado",
                    "No se detecto informacion"
                )

            # TARJETA GRAFICA

            gpus = hardware["gpu"]

            if gpus:

                self.gpu_card.update_card(
                    gpus[0]["name"]
                )

                for index, gpu in enumerate(gpus, start=1):

                    self.add_information(
                        self.gpu_section,
                        f"GPU {index}",
                        gpu["name"]
                    )

                    self.add_information(
                        self.gpu_section,
                        "Fabricante",
                        gpu["manufacturer"]
                    )

                    self.add_information(
                        self.gpu_section,
                        "Memoria reportada",
                        f'{gpu["memory_gb"]} GB'
                    )

                    self.add_information(
                        self.gpu_section,
                        "Controlador",
                        gpu["driver_version"]
                    )

            else:

                self.gpu_card.update_card(
                    "No detectada"
                )

                self.add_information(
                    self.gpu_section,
                    "Estado",
                    "No se detectaron graficas"
                )

            # MEMORIA RAM

            ram_modules = hardware["ram"]

            total_ram = sum(
                module["capacity_gb"]
                for module in ram_modules
            )

            self.ram_card.update_card(
                f"{total_ram:.2f} GB"
            )

            if ram_modules:

                for index, module in enumerate(
                    ram_modules, start=1
                ):

                    self.add_information(
                        self.ram_section,
                        f"Registro {index}",
                        f'{module["manufacturer"]} | '
                        f'{module["capacity_gb"]} GB'
                    )

                    self.add_information(
                        self.ram_section,
                        "Numero de parte",
                        module["part_number"]
                    )

                    self.add_information(
                        self.ram_section,
                        "Velocidad",
                        f'{module["speed"]} MT/s'
                    )

                    self.add_information(
                        self.ram_section,
                        "Ubicacion",
                        module["device"]
                    )

            else:

                self.add_information(
                    self.ram_section,
                    "Estado",
                    "No se detectaron registros"
                )

            # ALMACENAMIENTO

            disks = hardware["disks"]

            self.disk_card.update_card(
                f"{len(disks)} unidad(es)"
            )

            if disks:

                for index, disk in enumerate(
                    disks, start=1
                ):

                    self.add_information(
                        self.disk_section,
                        f"Unidad {index}",
                        disk["model"]
                    )

                    self.add_information(
                        self.disk_section,
                        "Fabricante",
                        disk["manufacturer"]
                    )

                    self.add_information(
                        self.disk_section,
                        "Capacidad",
                        f'{disk["capacity_gb"]} GB'
                    )

                    self.add_information(
                        self.disk_section,
                        "Interfaz",
                        disk["interface"]
                    )

                    self.add_information(
                        self.disk_section,
                        "Tipo de medio reportado",
                        disk["media_type"]
                    )

            else:

                self.add_information(
                    self.disk_section,
                    "Estado",
                    "No se detectaron unidades"
                )

            # INFORMACION DEL SISTEMA

            system = hardware["system"]

            self.add_information(
                self.system_section,
                "Nombre del equipo",
                system["computer_name"]
            )

            self.add_information(
                self.system_section,
                "Sistema operativo",
                system["system"]
            )

            self.add_information(
                self.system_section,
                "Version de Windows",
                system["version"]
            )

            self.add_information(
                self.system_section,
                "Arquitectura",
                system["architecture"]
            )

            # RESULTADO

            self.status_label.setText(
                "Estado: Hardware detectado"
            )

            hora = datetime.now().strftime("%H:%M:%S")

            self.update_label.setText(
                f"Informacion actualizada correctamente | "
                f"Ultima revision: {hora}"
            )

        except Exception as error:

            self.status_label.setText(
                "Estado: Error de deteccion"
            )

            self.update_label.setText(
                "No se pudo completar la deteccion."
            )

            QMessageBox.warning(
                self,
                "Error de hardware",
                f"No se pudo obtener la informacion:\n{error}"
            )

        finally:

            self.refresh_button.setText(
                "Actualizar informacion del hardware"
            )

            self.refresh_button.setEnabled(True)

    def apply_styles(self):

        self.setStyleSheet("""

            QWidget {
                background-color: #101C30;
            }

            #hardwarePageTitle {
                color: white;
                font-size: 27px;
                font-weight: bold;
            }

            #hardwareDescription {
                color: #9AADC2;
                font-size: 13px;
            }

            #hardwareStatus {
                color: #55C8FF;
                font-size: 12px;
            }

            #hardwareCard {
                background-color: #192A40;
                border: 1px solid #29415C;
                border-radius: 12px;
                padding: 12px;
            }

            #hardwareCardTitle {
                color: #55C8FF;
                font-size: 11px;
                font-weight: bold;
            }

            #hardwareCardValue {
                color: white;
                font-size: 17px;
                font-weight: bold;
            }

            #hardwareCardDescription {
                color: #9AADC2;
                font-size: 10px;
            }

            #hardwareSection {
                background-color: #192A40;
                border: 1px solid #29415C;
                border-radius: 12px;
            }

            #hardwareSectionTitle {
                color: #55C8FF;
                font-size: 13px;
                font-weight: bold;
                padding-bottom: 8px;
            }

            #hardwareInfoLabel {
                color: #9AADC2;
                font-size: 12px;
                padding: 5px;
            }

            #hardwareInfoValue {
                color: #D5E2EF;
                font-size: 12px;
                padding: 5px;
            }

            #hardwareRefreshButton {
                background-color: #1676AE;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 12px;
                font-weight: bold;
            }

            #hardwareRefreshButton:hover {
                background-color: #2196D2;
            }

            #hardwareRefreshButton:disabled {
                background-color: #29415C;
                color: #9AADC2;
            }

            #hardwareUpdateLabel {
                color: #35D18A;
                font-size: 11px;
                padding: 5px;
            }

        """)
