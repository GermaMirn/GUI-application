from PyQt6.QtWidgets import ( QDialog, QLabel, QPushButton)
from PyQt6.QtGui import QIcon, QFont


class InfoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.initializeUI()

    def initializeUI(self):
        self.setFixedSize(360, 300)
        self.setWindowTitle("Бюро технической инвентаризации/панель пользователя/информационное окно")
        self.setWindowIcon(QIcon("images/pyqt_logo.png"))
        self.setUpWindow()
        
    def setUpWindow(self):
        self.setWindowTitle("Информационное окно")
        
        layout = QLabel("Информация о программе", self)
        layout.setFont(QFont("Arial", 15))
        layout.move(20, 20)
        
        close_button = QPushButton("Закрыть", self)
        close_button.clicked.connect(self.close)
        close_button.move(270, 270)