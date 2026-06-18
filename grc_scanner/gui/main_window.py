from PyQt5.QtWidgets import *

class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Enterprise GRC Scanner"
        )

        layout = QVBoxLayout()

        self.target = QLineEdit()

        self.target.setPlaceholderText(
            "Enter target"
        )

        self.button = QPushButton(
            "Start Scan"
        )

        layout.addWidget(self.target)
        layout.addWidget(self.button)

        self.setLayout(layout)