from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QScrollArea, QLabel, QMessageBox, QHBoxLayout, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import json
from mainWindow.dialogWindow.delUser import UserSelectionDialogDelete
from mainWindow.dialogWindow.registration import NewUserDialogRegistration
from mainWindow.dialogWindow.changeDataUser import ChangeDataUser 


class userShow(QMainWindow):
    def __init__(self, login, role):
        super().__init__()
        self.role = role
        self.login = login
        self.initializaUI()

    def initializaUI(self):
        self.setFixedSize(900, 810)
        self.setWindowTitle("Бюро технической инвентаризации/панель пользователя/пользователи")
        self.setWindowIcon(QIcon("images/users.png")) 
        
        self.setUpWindow()
        self.show()

    def setUpWindow(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout()

        layout.addWidget(self.leftPart())
        with open( "json/user.json", "r") as data_json:
            user_json = json.load(data_json)
            layout.addWidget(self.rightPart())

        central_widget.setLayout(layout)

    def leftPart(self):
        with open("json/user.json") as user_json:
            user_json_date = json.load(user_json)
            number_member = 0
            for i in user_json_date:
                number_member += 1
            users = QLabel(f"Сотрудники (Всего: {number_member})", self)
        users.setFixedWidth(177)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMaximumSize(300, 745)

        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)

        with open("json/user.json") as user_json:
            self.user_json_data = json.load(user_json)

            for self.user in self.user_json_data:
                self.label = QPushButton(f"{self.user}")
                self.label.clicked.connect(lambda _, user=self.user: self.getDataAboutUser(user))
                content_layout.addWidget(self.label)
        
        if self.role == "admin":
            with open("json/admin.json") as admin_json:
                self.admin_json_data = json.load(admin_json)

        self.scroll_area.setWidget(self.content_widget)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    
        add_button = QPushButton("Регестрировать", self)
        add_button.move(20, 780)
        add_button.setFixedWidth(120)
        add_button.clicked.connect(self.createNewUser)

        del_button = QPushButton("Удаление", self)
        del_button.move(170, 780)
        del_button.clicked.connect(self.deleteUser)

        return self.scroll_area

    def rightPart(self):
        users_data = QLabel("Персональные данные: ", self)
        users_data.setFixedWidth(177)
        users_data.move(400, 25)

        user_name = QLabel("Имя: ", self)
        user_name.setFixedWidth(177)
        user_name.move(440, 65)

        if self.role == "user":
            self.first_name_data = QLabel(f"{self.user_json_data[self.login]["full_name"].split()[0]}", self)
        else:
            self.first_name_data = QLabel(f"{self.admin_json_data[self.login]["full_name"].split()[0]}", self)

        self.first_name_data.setFixedWidth(177)
        self.first_name_data.move(540, 65)

        last_name_label = QLabel('Фамилия:', self)
        last_name_label.setFixedWidth(177)
        last_name_label.move(440, 100)

        if self.role == "user":
            self.last_name_data = QLabel(f"{self.user_json_data[self.login]["full_name"].split()[1]}", self)
        else:
            self.last_name_data = QLabel(f"{self.admin_json_data[self.login]["full_name"].split()[1]}", self)

        self.last_name_data.setFixedWidth(177)
        self.last_name_data.move(540, 100)


        patronymic_label = QLabel('Отчество:', self)
        patronymic_label.setFixedWidth(177)
        patronymic_label.move(440, 135)

        if self.role == "user":
            self.patronymic_data = QLabel(f"{self.user_json_data[self.login]["full_name"].split()[2]}", self)
        else:
            self.patronymic_data = QLabel(f"{self.admin_json_data[self.login]["full_name"].split()[2]}", self)

        self.patronymic_data.setFixedWidth(177)
        self.patronymic_data.move(540, 135)

        passport_label = QLabel("Паспортные данные: ", self)
        passport_label.setFixedWidth(177)
        passport_label.move(400, 195)

        passport_series = QLabel("Серия: ", self)
        passport_series.setFixedWidth(177)
        passport_series.move(440, 235)

        if self.role == "user":
            self.passport_series_date = QLabel(f"{self.user_json_data[self.login]["passport_details"]["series"]}", self)
        else:
            self.passport_series_date = QLabel(f"{self.admin_json_data[self.login]["passport_details"]["series"]}", self)

        self.passport_series_date.setFixedWidth(177)
        self.passport_series_date.move(495, 235)

        passport_number = QLabel("Номер: ", self)
        passport_number.setFixedWidth(177)
        passport_number.move(590, 235)

        if self.role == "user":
            self.passport_number_date = QLabel(f"{self.user_json_data[self.login]["passport_details"]["number"]}", self)
        else:
            self.passport_number_date = QLabel(f"{self.admin_json_data[self.login]["passport_details"]["number"]}", self)

        self.passport_number_date.setFixedWidth(177)
        self.passport_number_date.move(650, 235)

        credit_card_label = QLabel("Банковская карта: ", self)
        credit_card_label.setFixedWidth(177)
        credit_card_label.move(400, 295)

        number_credit_card = QLabel("Номер счета: ", self)
        number_credit_card.setFixedWidth(177)
        number_credit_card.move(440, 335)

        if self.role == "user":
            self.number_credit_card_date = QLabel(f"{self.user_json_data[self.login]["bank_card"]["account_number"]}", self)
        else:
            self.number_credit_card_date = QLabel(f"{self.admin_json_data[self.login]["bank_card"]["account_number"]}", self)

        self.number_credit_card_date.setFixedWidth(177)
        self.number_credit_card_date.move(550, 335)

        validity = QLabel("Срок действия: ", self)
        validity.setFixedWidth(177)
        validity.move(440, 370)

        if self.role == "user":
            self.validity_date = QLabel(f"{self.user_json_data[self.login]["bank_card"]["validity"]}", self)
        else:
            self.validity_date = QLabel(f"{self.admin_json_data[self.login]["bank_card"]["validity"]}", self)

        self.validity_date.setFixedWidth(177)
        self.validity_date.move(550, 370)

        accrued = QLabel("Начислено:", self)
        accrued.setFixedWidth(177)
        accrued.move(400, 430)

        accrued_last = QLabel("Сумма последнего начисления: ", self)
        accrued_last.setFixedWidth(200)
        accrued_last.move(420, 485)

        if self.role == "user":
            self.accrued_last_date = QLabel(f"{self.user_json_data[self.login]["last_accrual_amount"][-1]}", self)
        else:
            self.accrued_last_date = QLabel(f"{self.admin_json_data[self.login]["last_accrual_amount"][-1]}", self)

        self.accrued_last_date.setFixedWidth(200)
        self.accrued_last_date.move(630, 485)

        change_data_button = QPushButton("Изменить", self)
        change_data_button.move(650, 780)
        change_data_button.clicked.connect(self.changeData)

        out_button = QPushButton("Выход", self)
        out_button.move(780, 780)
        out_button.clicked.connect(self.closeEventForButton)

        return QLabel("", self)

    def getDataAboutUser(self, user):
        with open("json/user.json", "r") as json_file:
            user_json_data = json.load(json_file)

        try:
            user_data = user_json_data[user]
            self.changeDataAboutUser(user_data)
            self.active_user = user
        except:
            QMessageBox.warning(self, "Ошибка",
                "Не получилось найти этого пользователся.", 
                QMessageBox.StandardButton.Close, 
                QMessageBox.StandardButton.Close)
            
    def changeDataAboutUser(self, user_data):
        try:
            user_fio_data = user_data["full_name"].split()
            user_passport_data = user_data["passport_details"]
            user_bank_data = user_data["bank_card"]

            try:
                self.first_name_data.setText(user_fio_data[0])
            except:
                self.first_name_data.setText("Ошибка")

            try:
                self.last_name_data.setText(user_fio_data[1])
            except:
                self.last_name_data.setText("Ошибка")
            
            try:
                self.patronymic_data.setText(user_fio_data[2])
            except:
                self.patronymic_data.setText("Ошибка")

            try:
                self.passport_series_date.setText(user_passport_data["series"])
            except:
                self.passport_series_date.setText("Ошибка")

            try:
                self.passport_number_date.setText(user_passport_data["number"])
            except:
                self.passport_number_date.setText("Ошибка")
            
            try:
                self.number_credit_card_date.setText(user_bank_data["account_number"])
            except:
                self.number_credit_card_date.setText("Ошибка")

            try:
                self.validity_date.setText(user_bank_data["validity"])
            except:
                self.validity_date.setText("Ошибка")

            try:
                self.accrued_last_date.setText(str(user_data["last_accrual_amount"][-1]))
            except:
                self.accrued_last_date.setText("0")

        except:
             QMessageBox.warning(self, "Ошибка", "Не получилось поменять данные.", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
             

    def createNewUser(self):
        self.create_new_user_window = NewUserDialogRegistration()
        self.create_new_user_window.show()

    def deleteUser(self):
        self.delete_user = UserSelectionDialogDelete()
        self.delete_user.show()

    def changeData(self):
        try:
            self.change_data_module = ChangeDataUser(self.active_user)
        except:
            self.change_data_module = ChangeDataUser(self.login)
        self.change_data_module.show()
    
    def closeEventForButton(self):
        dialog = QMessageBox()
        dialog.setText("Хотите закрыть окно?")
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        result = dialog.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.close()