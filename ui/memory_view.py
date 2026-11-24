
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox
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

        # ENCABEZADO

        title = QLabel("Memory Analyzer")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Analisis y monitoreo de memoria RAM"
        )
        description.setObjectName("description")

        main_layout.addWidget(title)
        main_layout.addWidget(description)

        # TARJETAS DE INFORMACION

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

        # ESTADO DE MEMORIA

        status_frame = QFrame()
        status_frame.setObjectName("statusFrame")

        status_layout = QHBoxLayout(status_frame)

        status_title = QLabel("Estado de memoria:")
        status_title.setObjectName("sectionTitle")

        self.status_label = QLabel("Analizando...")
        self.status_label.setObjectName("statusLabel")

        status_layout.addWidget(status_title)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()

        main_layout.addWidget(status_frame)

        # INFORMACION FISICA

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

        # TABLA DE PROCESOS

        process_title = QLabel(
            "PROCESOS CON MAYOR CONSUMO DE RAM"
        )
        process_title.setObjectName("sectionTitle")

        main_layout.addWidget(process_title)

        self.process_table = QTableWidget()

        self.process_table.setColumnCount(3)

        self.process_table.setHorizontalHeaderLabels([
            "PID",
            "Proceso",
            "Memoria utilizada (MB)"
        ])

        self.process_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.process_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.process_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.process_table.setAlternatingRowColors(True)

        main_layout.addWidget(self.process_table)

        # INDICADOR DE ACTUALIZACION

        self.update_label = QLabel(
            "Esperando actualizacion..."
        )

        self.update_label.setObjectName("updateLabel")

        main_layout.addWidget(self.update_label)

        # BOTON ACTUALIZAR

        self.refresh_button = QPushButton(
            "Actualizar analisis"
        )

        self.refresh_button.setObjectName("refreshButton")

        self.refresh_button.clicked.connect(
            self.refresh_memory
        )

        main_layout.addWidget(self.refresh_button)

        self.apply_styles()

    def create_card(self, layout, title):

        card = QFrame()
        card.setObjectName("memoryCard")

        card_layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        value_label = QLabel("0 GB")
        value_label.setObjectName("cardValue")

        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)

        layout.addWidget(card)

        return value_label

    def refresh_memory(self):

        self.refresh_button.setEnabled(False)

        try:

            # INDICADOR DE PROCESAMIENTO

            self.refresh_button.setText(
                "Actualizando..."
            )

            self.update_label.setText(
                "Analizando memoria del equipo..."
            )

            QApplication.processEvents()

            # RESUMEN DE MEMORIA

            memory = get_memory_summary()

            self.total_label.setText(
                f"{memory['total']} GB"
            )

            self.used_label.setText(
                f"{memory['used']} GB"
            )

            self.available_label.setText(
                f"{memory['available']} GB"
            )

            self.percent_label.setText(
                f"{memory['percent']}%"
            )

            # ESTADO DE MEMORIA

            status = get_memory_status()

            self.status_label.setText(status)

            if status == "CRITICO":

                self.status_label.setStyleSheet(
                    "color: #FF5555; font-weight: bold;"
                )

            elif status == "ADVERTENCIA":

                self.status_label.setStyleSheet(
                    "color: #F5B942; font-weight: bold;"
                )

            else:

                self.status_label.setStyleSheet(
                    "color: #35D18A; font-weight: bold;"
                )

            # INFORMACION DE MEMORIA FISICA

            physical = get_physical_memory()

            if physical:

                total_physical = sum(
                    module["capacity"]
                    for module in physical
                )

                manufacturers = sorted(set(
                    module["manufacturer"].strip()
                    for module in physical
                ))

                speeds = sorted(set(
                    module["speed"]
                    for module in physical
                    if module["speed"] is not None
                ))

                self.physical_label.setText(
                    f"Capacidad reportada por WMI: "
                    f"{total_physical:.2f} GB | "
                    f"Fabricante: {', '.join(manufacturers)} | "
                    f"Velocidad reportada: {speeds} MT/s"
                )

            else:

                self.physical_label.setText(
                    "No se pudo obtener informacion fisica."
                )

            # PROCESOS CON MAYOR CONSUMO

            processes = get_top_processes(limit=10)

            self.process_table.setRowCount(
                len(processes)
            )

            for row, process in enumerate(processes):

                pid_item = QTableWidgetItem(
                    str(process["pid"])
                )

                name_item = QTableWidgetItem(
                    process["name"]
                )

                memory_item = QTableWidgetItem(
                    f"{process['memory_mb']:.2f} MB"
                )

                pid_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                memory_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.process_table.setItem(
                    row, 0, pid_item
                )

                self.process_table.setItem(
                    row, 1, name_item
                )

                self.process_table.setItem(
                    row, 2, memory_item
                )

            # CONFIRMACION DE ACTUALIZACION

            self.update_label.setText(
                f"✓ Analisis actualizado correctamente | "
                f"Ultima actualizacion: "
                f"{datetime.now().strftime('%H:%M:%S')}"
            )

        except Exception as error:

            self.update_label.setText(
                "No se pudo completar la actualizacion."
            )

            QMessageBox.warning(
                self,
                "Error de diagnostico",
                f"No se pudo actualizar la memoria: {error}"
            )

        finally:

            # RESTAURAR BOTON

            self.refresh_button.setText(
                "Actualizar analisis"
            )

            self.refresh_button.setEnabled(True)

    def apply_styles(self):

        self.setStyleSheet("""
            QWidget {
                background-color: #101C30;
                color: white;
                font-family: Segoe UI;
            }

            #pageTitle {
                font-size: 26px;
                font-weight: bold;
            }

            #description {
                color: #9AADC2;
                font-size: 12px;
            }

            #memoryCard, #statusFrame {
                background-color: #192A40;
                border: 1px solid #29415C;
                border-radius: 10px;
                padding: 10px;
            }

            #cardTitle, #sectionTitle {
                color: #55C8FF;
                font-size: 11px;
                font-weight: bold;
            }

            #cardValue {
                color: white;
                font-size: 23px;
                font-weight: bold;
            }

            #statusLabel {
                font-size: 13px;
            }

            QTableWidget {
                background-color: #192A40;
                alternate-background-color: #20344D;
                color: white;
                border: 1px solid #29415C;
                gridline-color: #29415C;
            }

            QHeaderView::section {
                background-color: #183B5B;
                color: white;
                padding: 9px;
                border: none;
                font-weight: bold;
            }

            #refreshButton {
                background-color: #1676AE;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 7px;
                font-weight: bold;
            }

            #refreshButton:hover {
                background-color: #2196D2;
            }

            #refreshButton:disabled {
                background-color: #526477;
            }

            #updateLabel {
                color: #35D18A;
                font-size: 11px;
                padding: 5px;
            }
        """)
