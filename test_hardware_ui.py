import sys

from PySide6.QtWidgets import QApplication
from ui.hardware_view import HardwareView

app = QApplication(sys.argv)

window = HardwareView()
window.resize(1100, 750)
window.setWindowTitle("PC Medicine - Hardware")

window.show()

sys.exit(app.exec())