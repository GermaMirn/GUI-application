from PyQt6.QtWidgets import ( QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QComboBox, QLineEdit, QRadioButton, QFrame, QGroupBox, QCheckBox, QMessageBox)
from PyQt6.QtGui import QIcon


class ImportDataDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Окно импорта данных")
        self.setFixedSize(620, 700)

        layout = QVBoxLayout()

        path_layout = QHBoxLayout()
        path_label = QLabel("Путь к файлу:")
        self.path_edit = QLineEdit()
        browse_button = QPushButton("Обзор")
        browse_button.clicked.connect(self.browse_file)

        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(browse_button)

        layout.addLayout(path_layout)

        method_label = QLabel("Способ импорта:")
        layout.addWidget(method_label)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setLineWidth(1)

        method_layout = QVBoxLayout()

        new_radio = QRadioButton("Импортировать данные в новый справочник")
        existing_radio = QRadioButton("Добавить копию данных к существующему справочнику")
        method_layout.addWidget(new_radio)
        method_layout.addWidget(existing_radio)

        frame.setLayout(method_layout)
        layout.addWidget(frame)

        params_label = QLabel("Параметры импорта:")
        layout.addWidget(params_label)

        params_groupbox = QGroupBox()
        params_layout = QVBoxLayout()

        ref_name_label = QLabel("Имя справочника:")
        sheet_name_label = QLabel("Имя листа:")
        divider_label = QLabel("Разделитель:")

        ref_name_combo = QComboBox()
        ref_name_combo.addItem("Справочник 1")
        ref_name_combo.addItem("Справочник 2")

        sheet_name_combo = QComboBox()
        sheet_name_combo.addItem("Лист 1")
        sheet_name_combo.addItem("Лист 2")

        divider_groupbox = QGroupBox()
        divider_layout = QVBoxLayout()

        radio_tab = QRadioButton("Табуляция")
        radio_semicolon = QRadioButton("Точка с запятой(;)")
        radio_comma = QRadioButton("Запятая(,)")
        radio_dot = QRadioButton("Точка(.)")
        radio_space = QRadioButton("Пробел")
        radio_custom = QRadioButton("Другое")

        divider_layout.addWidget(radio_tab)
        divider_layout.addWidget(radio_semicolon)
        divider_layout.addWidget(radio_comma)
        divider_layout.addWidget(radio_dot)
        divider_layout.addWidget(radio_space)
        divider_layout.addWidget(radio_custom)

        divider_groupbox.setLayout(divider_layout)

        checkbox_header = QCheckBox("Первая строка содержит заголовки столбцов")
        checkbox_check = QCheckBox("Проверять типы данных и структуру перед импортом")
        
        params_layout.addWidget(ref_name_label)
        params_layout.addWidget(ref_name_combo)
        params_layout.addWidget(sheet_name_label)
        params_layout.addWidget(sheet_name_combo)
        params_layout.addWidget(divider_label)
        params_layout.addWidget(divider_groupbox)
        params_layout.addWidget(checkbox_header)
        params_layout.addWidget(checkbox_check)

        params_groupbox.setLayout(params_layout)
        layout.addWidget(params_groupbox)
        buttons_layout = QHBoxLayout()

        import_button = QPushButton("Импорт", self)
        import_button.setIcon(QIcon("imges/accept.png"))

        cancel_button = QPushButton("Отмена", self)
        cancel_button.setIcon(QIcon("imges/cansel.png"))
        cancel_button.clicked.connect(self.clickOnCancel)

        buttons_layout.addStretch(1)
        buttons_layout.addWidget(import_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def browse_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите файл", "", "All Files")
        self.path_edit.setText(file_path)
    
    def clickOnCancel(self):
        dialog = QMessageBox()
        dialog.setText("Хотите закрыть окно?")
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        result = dialog.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.close()