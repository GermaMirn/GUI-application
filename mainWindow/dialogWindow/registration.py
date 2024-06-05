import hashlib, json
from PyQt6.QtWidgets import (QDialog, QLabel, QPushButton, QLineEdit, QMessageBox)
from PyQt6.QtGui import QFont, QIcon


class NewUserDialogRegistration(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.initializeUI()

    def initializeUI(self):
        self.setFixedSize(360, 250)
        self.setWindowTitle("Бюро технической инвентаризации/регистрация")
        self.setWindowIcon(QIcon("images/pyqt_logo.png"))
        self.setUpWindow()

    def setUpWindow(self):
        login_label = QLabel("Регистрация", self)
        login_label.setFont(QFont("Arial", 20))
        login_label.move(120, 10)

        check_role = QLabel("Админ(пароль): ", self)
        check_role.move(15, 53)

        self.check_role = QLineEdit(self)
        self.check_role.resize(230, 24)
        self.check_role.move(123, 50)

        name_label = QLabel("Логин:", self)
        name_label.move(15, 84)

        self.login = QLineEdit(self)
        self.login.resize(230, 24)
        self.login.move(123, 80)

        full_name_label = QLabel("ФИО:", self)
        full_name_label.move(15, 114)

        self.full_name_edit = QLineEdit(self)
        self.full_name_edit.resize(230, 24)
        self.full_name_edit.move(123, 110)

        new_pswd_label = QLabel("Пароль:", self)
        new_pswd_label.move(15, 144)

        self.new_pswd_edit = QLineEdit(self)
        self.new_pswd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_pswd_edit.resize(230, 24)
        self.new_pswd_edit.move(123, 140)

        confirm_label = QLabel("Подтверждение:", self)
        confirm_label.move(15, 174)

        self.confirm_edit = QLineEdit(self)
        self.confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_edit.resize(230, 24)
        self.confirm_edit.move(123, 170)

        sign_up_button = QPushButton("Зарегистрировать", self)
        sign_up_button.resize(340, 32)
        sign_up_button.move(15, 210)
        sign_up_button.clicked.connect(self.confirmSignUp)

    def confirmSignUp(self):
        with open("json/admin.json", "r") as admin:
           admin_json_data = json.load(admin)
        
        with open("json/user.json", "r") as user:
           user_json_data = json.load(user)

        check_role = self.check_role.text()
        login = self.login.text()
        full_name = self.full_name_edit.text()
        pswd_text = self.new_pswd_edit.text()
        confirm_text = self.confirm_edit.text()

        if login == "" or pswd_text == "" or full_name == "":
          QMessageBox.warning(self, "Ошибка",
              "Пожалуйста введите ФИО, логин или пароль.", 
              QMessageBox.StandardButton.Close,
              QMessageBox.StandardButton.Close)
        elif pswd_text != confirm_text:
          QMessageBox.warning(self, "Ошибка",
              "Введенные пароли не совпадают.", 
              QMessageBox.StandardButton.Close,
              QMessageBox.StandardButton.Close)
        elif login in admin_json_data or login in user_json_data:
          QMessageBox.warning(self, "Ошибка",
              "Этот логин уже существует.", 
              QMessageBox.StandardButton.Close,
              QMessageBox.StandardButton.Close)
        elif len(full_name.split()) != 3:
           QMessageBox.warning(self, "Ошибка",
              "Введите плолностью ФИО.", 
              QMessageBox.StandardButton.Close,
              QMessageBox.StandardButton.Close)
        else:
          data_for_json = {}

          data_for_json["full_name"] = full_name
          data_for_json["login"] = login
          data_for_json["password"] = hashlib.md5(pswd_text.encode()).hexdigest()

          data_for_json["passport_details"] = {}
          data_for_json["passport_details"]["series"] = "пусто"
          data_for_json["passport_details"]["number"] = "пусто"

          data_for_json["bank_card"] = {}
          data_for_json["bank_card"]["account_number"] = "пусто"
          data_for_json["bank_card"]["validity"] = "пусто"

          data_for_json["last_accrual_amount"] = [0]

          if check_role == "123":
            with open("json/admin.json", "w") as admin_json:
              admin_json_data[login] = data_for_json
              json.dump(admin_json_data, admin_json)
            self.close()
          else:
            with open("json/user.json", "w") as user_json:
              user_json_data[login] = data_for_json
              json.dump(user_json_data, user_json)
            self.close()