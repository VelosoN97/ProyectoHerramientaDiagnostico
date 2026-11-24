import sys

from PySide6.QtWidgets import QApplication
from ui.memory_view import MemoryView

app = QApplication(sys.argv)

window = MemoryView()
window.show()

sys.exit(app.exec())