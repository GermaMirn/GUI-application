import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, 
     QLineEdit, QPushButton, QCheckBox, QMessageBox)
from PyQt6.QtGui import QFont, QIcon
from mainWindow.MainWindowForAdmin import MainWindowForAdmin
from mainWindow.MainWindowForUser import MainWindowUser
from mainWindow.dialogWindow.registration import NewUserDialogRegistration    
import json, hashlib


class LoginWindow(QWidget):
    def __init__(self): 
        super().__init__()
        self.initializeUI()

        self.checkedRole = False

    def initializeUI(self):
        self.setFixedSize(360, 220)
        self.setWindowTitle("Бюро технической инвентаризации/вход")
        self.setWindowIcon(QIcon("images/pyqt_logo.png")) 

        self.setUpWindow()
        self.show()

    def setUpWindow(self):
        self.login_is_successful = False

        login_label = QLabel("Логин", self)
        login_label.setFont(QFont("Arial", 20))
        login_label.move(160, 10)

        username_label = QLabel("Логин: ", self)
        username_label.move(20, 54)

        self.username_edit = QLineEdit(self)
        self.username_edit.resize(250, 24)
        self.username_edit.move(90, 50)

        password_label = QLabel("Пароль: ", self)
        password_label.move(20, 86)

        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.resize(250, 24)
        self.password_edit.move(90, 82)
        
        self.show_password_cb = QCheckBox("Показать пароль", self)
        self.show_password_cb.move(90, 110)
        self.show_password_cb.toggled.connect(self.displayPasswordIfChecked)

        self.check_role = QCheckBox("Администратор", self)
        self.check_role.move(220, 110)
        self.check_role.toggled.connect(self.checkRole)

        login_button = QPushButton("Войти", self)
        login_button.resize(320, 34)
        login_button.move(20, 140)
        login_button.clicked.connect(self.clickLoginButton)

        not_member_label = QLabel("вы можете: ", self)
        not_member_label.move(20, 186)

        sign_up_button = QPushButton("Зарегистрироваться", self)
        sign_up_button.move(120, 180)
        sign_up_button.clicked.connect(self.createNewUser)

    def closeEvent(self, event):
        if self.login_is_successful == True:
            event.accept()
        else:
            answer = QMessageBox.question(self, "Выход из приложения?",
                "Вы хотите выйти из приложения?", 
                QMessageBox.StandardButton.No | \
                QMessageBox.StandardButton.Yes, 
                QMessageBox.StandardButton.Yes)
            if answer == QMessageBox.StandardButton.Yes:
                event.accept()
            if answer == QMessageBox.StandardButton.No:
                event.ignore() 

    def displayPasswordIfChecked(self, checked):
        if checked:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        elif checked == False:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

    def checkRole(self, checked):
        if checked:
            self.checkedRole = checked
        else:
            self.checkedRole = checked


    def clickLoginButton(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        if self.checkedRole:
            try:
                with open("json/admin.json", "r") as admin_json:
                    admin_db = json.load(admin_json)
                    if username in admin_db and admin_db[username]["password"] == hashlib.md5(password.encode()).hexdigest():
                        QMessageBox.information(self, "Login Successful!", 
                        "Login Successful!", QMessageBox.StandardButton.Ok, 
                        QMessageBox.StandardButton.Ok)
                        self.login_is_successful = True
                        self.close()
                        self.openApplicationWindow("admin", username)
                    else:
                        QMessageBox.warning(self, "Ошибка",
                        "Логин или пароль с ошибкой.", 
                        QMessageBox.StandardButton.Close, 
                        QMessageBox.StandardButton.Close)
            except :
                QMessageBox.warning(self, "Ошибка",
                "Неизвестная ошибка.", 
                QMessageBox.StandardButton.Close, 
                QMessageBox.StandardButton.Close)
        else:
            try:
                with open("json/user.json", "r") as user_json:
                    user_db = json.load(user_json)
                    if username in user_db and user_db[username]["password"] == hashlib.md5(password.encode()).hexdigest():
                        QMessageBox.information(self, "Login Successful!", 
                        "Login Successful!", QMessageBox.StandardButton.Ok, 
                        QMessageBox.StandardButton.Ok)
                        self.login_is_successful = True
                        self.close()
                        self.openApplicationWindow("user", username)
                    else:
                        QMessageBox.warning(self, "Ошибка",
                        "Логин или пароль с ошибкой.", 
                        QMessageBox.StandardButton.Close, 
                        QMessageBox.StandardButton.Close)
            except :
                QMessageBox.warning(self, "Ошибка",
                "Неизвестная ошибка.", 
                QMessageBox.StandardButton.Close, 
                QMessageBox.StandardButton.Close)

    def createNewUser(self):
        self.create_new_user_window = NewUserDialogRegistration()
        self.create_new_user_window.show()

    def openApplicationWindow(self, role, login):
        if role == "admin":
            self.main_window = MainWindowForAdmin(login, role)
        else:
            self.main_window = MainWindowUser(login, role)
        self.main_window.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec())