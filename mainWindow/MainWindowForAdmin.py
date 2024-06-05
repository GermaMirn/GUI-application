import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, 
    QMessageBox, QTextEdit, QFileDialog, QInputDialog, 
    QFontDialog, QColorDialog, QToolBar, QStatusBar)
from PyQt6.QtCore import Qt, QSize, QDate, QTime, QTimer
from PyQt6.QtGui import QIcon, QTextCursor, QColor, QAction, QFont
from mainWindow.dialogWindow import importData, InfoAboutProg, dataBaseUsers, delUser, registration

class MainWindowForAdmin(QMainWindow):
    def __init__(self, login, role):
        super().__init__()
        self.change_account_window_opened = False
        self.role = role
        self.login = login
        self.statusToolbar = True
        self.statusToolbarState = True
        
        self.initializeUI(login)

    def initializeUI(self, login):
        self.setMinimumSize(500, 600)
        self.setWindowTitle("Бюро технической инвентаризации/панель пользователя")
        self.setWindowIcon(QIcon("images/pyqt_logo.png"))

        self.setUpMainWindow(login)
        self.createActions()
        self.createMenu()
        self.createToolBar()
        self.show()

    def setUpMainWindow(self, login):
        self.login_is_successful = False

        self.getDateTime()

        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self.removeHighlights)
        self.setCentralWidget(self.text_edit)

    def getDateTime(self):
        if self.statusToolbarState:
            timer = QTimer(self)
            timer.timeout.connect(self.updateDateTime)
            timer.start(1000)

            self.statusToolbarState = False
        
        else:
            self.setStatusBar(None)
            self.statusToolbarState = True
    
    def updateDateTime(self):
        if self.statusToolbarState == False :
            date = QDate.currentDate().toString("dd MM yyyy")
            time = QTime.currentTime().toString("hh:mm:ss")

            self.statusbar = QStatusBar(self)
            self.statusBar().showMessage(f"Добро пожаловать: {self.login}     дата: {date}   время: {time}")
        
            return date, time

    def createActions(self):
        self.open_act = QAction(QIcon("images/open_file.png"), "Открыть файл")
        self.open_act.setShortcut("Ctrl+O")
        self.open_act.triggered.connect(self.openFile)

        self.save_act = QAction(QIcon("images/save_file.png"), "Сохранить файл")
        self.save_act.setShortcut("Ctrl+S")
        self.save_act.triggered.connect(self.saveToFile)

        self.importData = QAction(QIcon("images/import.png"), "Импорт")
        self.importData.setShortcut("Ctrl+H")
        self.importData.triggered.connect(self.importDataDialog)

        self.quit_act = QAction(QIcon("images/exit.png"), "Выход")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(self.closeEventForButton)

        self.undo_act = QAction(QIcon("images/undo.png"), "Отменить")
        self.undo_act.setShortcut("Ctrl+Z")
        self.undo_act.triggered.connect(self.text_edit.undo)

        self.redo_act = QAction(QIcon("images/redo.png"), "Повторить")
        self.redo_act.setShortcut("Ctrl+Shift+Z")
        self.redo_act.triggered.connect(self.text_edit.redo)

        self.cut_act = QAction(QIcon("images/cut.png"), "Вырезать")
        self.cut_act.setShortcut("Ctrl+X")
        self.cut_act.triggered.connect(self.text_edit.cut)

        self.copy_act = QAction(QIcon("images/copy.png"), "Копировать")
        self.copy_act.setShortcut("Ctrl+C")
        self.copy_act.triggered.connect(self.text_edit.copy)

        self.paste_act = QAction(QIcon("images/paste.png"), "Вставить")
        self.paste_act.setShortcut("Ctrl+V")
        self.paste_act.triggered.connect(self.text_edit.paste)

        self.find_act = QAction(QIcon("images/find.png"), "Найти")
        self.find_act.setShortcut("Ctrl+F")
        self.find_act.triggered.connect(self.searchText)

        self.font_act = QAction(QIcon("images/font.png"), "Шрифт")
        self.font_act.setShortcut("Ctrl+T")
        self.font_act.triggered.connect(self.chooseFont)

        self.color_act = QAction(QIcon("images/color.png"), "Цвет")
        self.color_act.setShortcut("Ctrl+Shift+C")
        self.color_act.triggered.connect(self.chooseFontColor)

        self.highlight_act = QAction(QIcon("images/highlight.png"), "Выделять")
        self.highlight_act.setShortcut("Ctrl+Shift+H")
        self.highlight_act.triggered.connect(self.chooseFontBackgroundColor)

        self.trueStateToolbar = QAction(QIcon("images/click.png"), "Панель инструментов")
        self.trueStateToolbar.setShortcut("Ctrl+Y")
        self.trueStateToolbar.triggered.connect(self.createToolBar)

        self.trueStateToolbarState = QAction(QIcon("images/click.png"), "Строка состояния")
        self.trueStateToolbarState.setShortcut("Ctrl+T")
        self.trueStateToolbarState.triggered.connect(self.getDateTime)

        self.directories = QAction(QIcon("images/db.png"), "Информация о пользователях")
        self.directories.setShortcut("Ctrl+B")
        self.directories.triggered.connect(self.dbUsers)

        self.change_account = QAction(QIcon("images/changeAccount.png"), "Сменить аккаунт")
        self.change_account.setShortcut("Ctrl+G")
        self.change_account.triggered.connect(self.changeAccount)

        self.about_program = QAction(QIcon("images/about.png"), "О программе")
        self.about_program.setShortcut("Ctrl+R")
        self.about_program.triggered.connect(self.getDataAboutProgramm)

    def createMenu(self):
        self.menuBar().setNativeMenuBar(True)

        file_menu = self.menuBar().addMenu("Файл")
        file_menu.addSeparator()
        file_menu.addAction(self.open_act)
        file_menu.addAction(self.save_act)
        file_menu.addAction(self.importData)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_act)

        edit_menu = self.menuBar().addMenu("Правка")
        edit_menu.addAction(self.undo_act)
        edit_menu.addAction(self.redo_act) 
        edit_menu.addSeparator()       
        edit_menu.addAction(self.cut_act) 
        edit_menu.addAction(self.copy_act) 
        edit_menu.addAction(self.paste_act) 
        edit_menu.addSeparator()
        edit_menu.addAction(self.find_act)

        fromat = self.menuBar().addMenu("Формат")
        fromat.addAction(self.font_act)
        fromat.addAction(self.color_act)
        fromat.addAction(self.highlight_act)

        view = self.menuBar().addMenu("Вид")
        view.addAction(self.trueStateToolbar)
        view.addAction(self.trueStateToolbarState)

        directories = self.menuBar().addMenu("Справочник")
        directories.addAction(self.directories)
        directories.addAction(self.change_account)

        reference = self.menuBar().addMenu("Справка")
        reference.addAction(self.about_program)

    def openFile(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", 
            "HTML Files (*.html);;Text Files (*.txt)")

        if file_name:
            with open(file_name, "r") as f:
                notepad_text = f.read()
            self.text_edit.setText(notepad_text)

    def saveToFile(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл",
            "","HTML Files (*.html);;Text Files (*.txt)")

        if file_name.endswith(".txt"):
            notepad_text = self.text_edit.toPlainText()
            with open(file_name, "w") as f:            
                f.write(notepad_text)
        elif file_name.endswith(".html"):
            notepad_richtext = self.text_edit.toHtml()
            with open(file_name, "w") as f:            
                f.write(notepad_richtext)
        else:
            QMessageBox.information(
                self, "Не сохранено", "Текст не сохранен.", 
                QMessageBox.StandardButton.Ok)
            
    def importDataDialog(self):
        self.dataDialogImport = importData.ImportDataDialog()
        self.dataDialogImport.show()

    def searchText(self):
        find_text, ok = QInputDialog.getText(
            self, "Поиск текста", "Нашло:")

        if ok:
            extra_selections = []
            self.text_edit.moveCursor(QTextCursor.MoveOperation.Start)
            color = QColor(Qt.GlobalColor.gray)

            while(self.text_edit.find(find_text)):
                selection = QTextEdit.ExtraSelection()  
                selection.format.setBackground(color)

                selection.cursor = self.text_edit.textCursor()
                extra_selections.append(selection)

            self.text_edit.setExtraSelections(extra_selections)

    def removeHighlights(self):
        self.text_edit.setExtraSelections([])
            
    def chooseFont(self):
        current = self.text_edit.currentFont()

        opt = QFontDialog.FontDialogOption.DontUseNativeDialog
        font, ok = QFontDialog.getFont(current, self, 
            options=opt)
        if ok:
            self.text_edit.setCurrentFont(font) 
                
    def chooseFontColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setTextColor(color)

    def chooseFontBackgroundColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setTextBackgroundColor(color)
    
    def dbUsers(self):
        if self.role == "admin":
            self.db_users_show = dataBaseUsers.userShow(self.login, self.role)
            self.db_users_show.show()
        else:
            msgBox = QMessageBox()
            msgBox.setText("Нету доступа!")
            msgBox.setIcon(QMessageBox.Icon.Information)
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)

            msgBox.exec()
    
    def changeAccount(self):
        if not self.change_account_window_opened:
            self.change_account_window_opened = True

            dialog = QMessageBox()
            dialog.setText("Вы точно хотите сменить пользователя?")
            dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            result = dialog.exec()
            
            if result == QMessageBox.StandardButton.Yes:
                from login import LoginWindow
                self.change_account_move = LoginWindow()
                self.change_account_move.show()

                self.close()
    
    def getDataAboutProgramm(self):
        self.infoAboutProgramm = InfoAboutProg.InfoDialog()
        self.infoAboutProgramm.show()

    def closeEventForButton(self):
        dialog = QMessageBox()
        dialog.setText("Хотите закрыть окно?")
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        result = dialog.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.close()
    
    def closeEvent(self, event):
        if not self.change_account_window_opened:
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
        
    def createToolBar(self):
        if self.statusToolbar == True:
            self.toolbar = QToolBar("Главная панель инструментов")
            self.toolbar.setIconSize(QSize(16, 16))
            self.addToolBar(self.toolbar)

            self.create_tool_user = QAction(QIcon("images/accept.png"), "Зарегистрировать пользователя")
            self.create_tool_user.triggered.connect(self.createNewUser)

            self.delete_tool_user = QAction(QIcon("images/cansel.png"), "Удалить пользователя")
            self.delete_tool_user.triggered.connect(self.deleteUser)

            self.standart_3 = QAction(QIcon("images/tool.png"), "эелемент 3")
            self.standart_4 = QAction(QIcon("images/tool.png"), "эелемент 4")

            self.toolbar.addAction(self.create_tool_user)
            self.toolbar.addAction(self.delete_tool_user)

            self.toolbar.addAction(self.standart_3)
            self.toolbar.addAction(self.standart_4)
            self.toolbar.addAction(self.quit_act)
            self.statusToolbar = False
        else:
            self.removeToolBar(self.toolbar)
        
            self.statusToolbar = True

    def createNewUser(self):
        self.create_new_user = registration.NewUserDialogRegistration()
        self.create_new_user.show()
    
    def deleteUser(self):
        self.delete_user = delUser.UserSelectionDialogDelete()
        self.delete_user.show()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindowForAdmin()
  sys.exit(app.exec())