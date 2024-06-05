from PyQt6.QtWidgets import (QDialog, QLabel, QPushButton, QComboBox, QDialog, QMessageBox)
import json

class UserSelectionDialogDelete(QDialog):
    def __init__(self):
      super().__init__()
      self.change_account_window_opened = False
      
      self.setWindowTitle("Выберите пользователя")
      self.setFixedSize(250, 130)
      
      label_choose_user = QLabel("Выберите пользователя: ", self)
      label_choose_user.move(10, 10)

      delete_button = QPushButton("Удалить", self)
      delete_button.move(70, 100)

      cancel_button = QPushButton("Отмена", self)
      cancel_button.move(160, 100)
      cancel_button.clicked.connect(self.close)
      
      self.combo_box = QComboBox(self)
      self.combo_box.move(60, 45)
      
      with open( "json/user.json", "r") as data_json:
        self.user_json = json.load(data_json)
      
      for self.user in self.user_json:
        self.combo_box.addItem(f"{self.user}")
        delete_button.clicked.connect(lambda _, login=self.combo_box.currentText(): self.deleteUser(login))

    def deleteUser(self, login):
      if not self.change_account_window_opened:
        self.change_account_window_opened = True

        dialog = QMessageBox()
        dialog.setText("Вы точно хотите удалить пользователя?")
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        result = dialog.exec()
        
        if result == QMessageBox.StandardButton.Yes: 
          with open( "json/user.json", "w+") as json_file:
            if login in self.user_json:
              del self.user_json[login]

            json.dump(self.user_json, json_file)
          
          self.changeList(self.user_json)

    def changeList(self, user_json):
      self.combo_box.clear()

      for user in user_json:
        self.combo_box.addItem(f"{user}")