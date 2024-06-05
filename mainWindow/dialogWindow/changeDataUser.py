import json
from PyQt6.QtWidgets import (QDialog, QLabel, QPushButton, QLineEdit, QMessageBox)
from PyQt6.QtGui import QFont, QIcon


class ChangeDataUser(QDialog):
  def __init__(self, login):
        super().__init__()
        self.login = login
        self.setModal(True)
        self.initializeUI()

  def initializeUI(self):
      self.setFixedSize(400, 260)
      self.setWindowTitle("Бюро технической инвентаризации/панель пользователя/пользователи/изменения данных")
      self.setWindowIcon(QIcon("images/pyqt_logo.png"))
      self.setUpWindow()

  def setUpWindow(self):
      with open("json/user.json", "r") as user_json:
        self.user_json_data = json.load(user_json)

      with open("json/admin.json", "r") as admin_json:
        self.admin_json_data = json.load(admin_json)

      change_label = QLabel("Данные для имзменения", self)
      change_label.setFont(QFont("Arial", 20))
      change_label.move(90, 10)

      fio_label = QLabel("ФИО: ", self)
      fio_label.move(15, 53)

      try:
        self.fio_label_line = QLineEdit(f"{self.user_json_data[self.login]["full_name"]}",self)
      except:
         self.fio_label_line = QLineEdit(f"{self.admin_json_data[self.login]["full_name"]}",self)

      self.fio_label_line.resize(230, 24)
      self.fio_label_line.move(163, 50)

      passport_series = QLabel("Серия пасспорта:", self)
      passport_series.move(15, 84)

      try:
        self.passport_series_line = QLineEdit(f"{self.user_json_data[self.login]["passport_details"]["series"]}",self)
      except:
         self.passport_series_line = QLineEdit(f"{self.admin_json_data[self.login]["passport_details"]["series"]}",self)

      self.passport_series_line.resize(230, 24)
      self.passport_series_line.move(163, 80)

      passport_number = QLabel("Номер пасспорта:", self)
      passport_number.move(15, 114)

      try:
        self.passport_number_line = QLineEdit(f"{self.user_json_data[self.login]["passport_details"]["number"]}", self)
      except:
         self.passport_number_line = QLineEdit(f"{self.admin_json_data[self.login]["passport_details"]["number"]}", self)

      self.passport_number_line.resize(230, 24)
      self.passport_number_line.move(163, 110)

      number_credit_card = QLabel("Номер счета карты:", self)
      number_credit_card.move(15, 144)

      try:
        self.number_credit_card_line = QLineEdit(f"{self.user_json_data[self.login]["bank_card"]["account_number"]}", self)
      except:
        self.number_credit_card_line = QLineEdit(f"{self.admin_json_data[self.login]["bank_card"]["account_number"]}", self)
         
      self.number_credit_card_line.resize(230, 24)
      self.number_credit_card_line.move(163, 140)

      validity = QLabel("Срок действия карты:", self)
      validity.move(15, 174)

      try:
        self.validity_line = QLineEdit(f"{self.user_json_data[self.login]["bank_card"]["validity"]}", self)
      except:
        self.validity_line = QLineEdit(f"{self.admin_json_data[self.login]["bank_card"]["validity"]}", self)

      self.validity_line.resize(230, 24)
      self.validity_line.move(163, 170)

      accrued_last = QLabel("Сумма послед начисл:", self)
      accrued_last.move(15, 204)

      self.accrued_last_line = QLineEdit(self)
      self.accrued_last_line.resize(230, 24)
      self.accrued_last_line.move(163, 200)

      change_button = QPushButton("Изменить", self)
      change_button.move(200, 230)
      change_button.clicked.connect(self.changeDataInJson)

      cansel_button =QPushButton("Отменить", self)
      cansel_button.move(300, 230)
      cansel_button.clicked.connect(self.closeEventForButton)

  def changeDataInJson(self):
      fio = self.fio_label_line.text()
      series_passport = self.passport_series_line.text()
      number_passport = self.passport_number_line.text()
      number_credit_card = self.number_credit_card_line.text()
      validity = self.validity_line.text()
      accrued_last = self.accrued_last_line.text()


      with open("json/user.json", "r") as json_file:
          self.user_json = json.load(json_file)
      
      try:
        if fio != "" and len(fio.split()) == 3:
            self.user_json[self.login]["full_name"] = fio
        else:
            QMessageBox.warning(self, "Ошибка",
              "Введите плолностью ФИО.", 
              QMessageBox.StandardButton.Close,
              QMessageBox.StandardButton.Close)
        try:
          series_passport_number = int(series_passport)
          print(len(series_passport))
          if len(series_passport) == 4:
              self.user_json[self.login]["passport_details"]["series"] = series_passport
          else:
              QMessageBox.warning(self, "Ошибка",
                "Введите 4 цифры.", 
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
        except:
          QMessageBox.warning(self, "Ошибка",
                "Введите 4 цифры, а не буквы.", 
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
        try:
          number_passport_int = int(number_passport)
          if len(number_passport) == 6:
              self.user_json[self.login]["passport_details"]["number"] = number_passport
          else:
              QMessageBox.warning(self, "Ошибка",
                "Введите 6 цифры.", 
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
        except:
          QMessageBox.warning(self, "Ошибка",
                "Введите 6 цифры, а не буквы.", 
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
        try:
          number_credit_card_int = int(number_credit_card)
          if len(number_credit_card) == 16:
              self.user_json[self.login]["bank_card"]["account_number"] = number_credit_card
          else:
              QMessageBox.warning(self, "Ошибка",
                "Введите 16 цифры.", 
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
        except:
          QMessageBox.warning(self, "Ошибка",
                "Введите 16 цифры, а не буквы.", 
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
        try:
          validity_number = int(validity)
          if len(validity) == 4:
              self.user_json[self.login]["bank_card"]["validity"] = validity
          else:
              QMessageBox.warning(self, "Ошибка",
                "Введите 4 цифры.", 
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
        except:
          QMessageBox.warning(self, "Ошибка",
                "Введите 4 цифры, а не буквы.", 
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
        try:
          accrued_last_number = int(accrued_last)
          if accrued_last_number > 0:
            self.user_json[self.login]["last_accrual_amount"].append(accrued_last_number)
          else:
            QMessageBox.warning(self, "Ошибка",
                "Введите положительное число.", 
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
        except:
          QMessageBox.warning(self, "Ошибка",
                "Введите цифры, а не буквы.", 
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
      except:
        QMessageBox.warning(self, "Ошибка",
              "Неизвестная ошибка.", 
              QMessageBox.StandardButton.Close, 
              QMessageBox.StandardButton.Close)
        
      with open("json/user.json", "w") as json_file:
        json.dump(self.user_json, json_file)
      
      self.close()
          

  def closeEventForButton(self):
        dialog = QMessageBox()
        dialog.setText("Хотите закрыть окно?")
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        result = dialog.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.close()