from PyQt5.QtWidgets import QApplication

from grc_scanner.gui.main_window import MainWindow

app = QApplication([])

window = MainWindow()

window.show()

app.exec_()