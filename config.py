from PyQt5 import QtCore, QtWidgets
import configparser
import os

secret_key = 'dsafdsafasfdddddddddsaewrwerweareawrwa645264654654234324'


def crypto_xor(message: str, secret: str) -> str:
    new_chars = list()
    i = 0
    for num_chr in (ord(c) for c in message):
        num_chr ^= ord(secret[i])
        new_chars.append(num_chr)
        i += 1
        if i >= len(secret):
            i = 0
    return ''.join(chr(c) for c in new_chars)


def encrypt_xor(message: str, secret: str) -> str:
    return crypto_xor(message, secret).encode('utf-8').hex()


def decrypt_xor(message_hex: str, secret: str) -> str:
    message = bytes.fromhex(message_hex).decode('utf-8')
    return crypto_xor(message, secret)


def click_save(window):
    server = window.server.text()
    login = window.login.text()
    password = window.password.text()
    path_for_files = window.PathForFiles.text()
    xor_password = encrypt_xor(password, secret_key)
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'server': server,
                         'login': login,
                         'path_for_files': path_for_files,
                         'password': xor_password}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def read_config():
    config = configparser.ConfigParser()
    if os.path.exists('config.ini'):
        config.read('config.ini')
        server = config['DEFAULT']['server']
        login = config['DEFAULT']['login']
        path_for_files = config['DEFAULT']['path_for_files']
        ui.server.setText(server)
        ui.login.setText(login)
        ui.PathForFiles.setText(path_for_files)


def click_close():
    MainWindow.close()


def switch_password_vision(self):
    if ui.ShowPasswordCheckBox.isChecked():
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
    else:
        self.password.setEchoMode(QtWidgets.QLineEdit.Normal)


class UiMainWindow(object):
    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(331, 265)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.saveButtion = QtWidgets.QPushButton(self.centralwidget)
        self.saveButtion.setGeometry(QtCore.QRect(70, 200, 81, 23))
        self.saveButtion.setObjectName("saveButtion")
        self.server = QtWidgets.QLineEdit(self.centralwidget)
        self.server.setGeometry(QtCore.QRect(90, 20, 211, 20))
        self.server.setObjectName("server")
        self.PathForFiles = QtWidgets.QLineEdit(self.centralwidget)
        self.PathForFiles.setGeometry(QtCore.QRect(90, 60, 211, 20))
        self.PathForFiles.setObjectName("PathForFiles")
        self.login = QtWidgets.QLineEdit(self.centralwidget)
        self.login.setGeometry(QtCore.QRect(90, 100, 211, 20))
        self.login.setObjectName("login")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setGeometry(QtCore.QRect(90, 140, 211, 20))
        self.password.setObjectName("password")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 41, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 100, 21, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 140, 47, 16))
        self.label_3.setObjectName("label_3")
        self.CloseButtion = QtWidgets.QPushButton(self.centralwidget)
        self.CloseButtion.setGeometry(QtCore.QRect(200, 200, 75, 23))
        self.CloseButtion.setObjectName("CloseButtion")
        self.ShowPasswordCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.ShowPasswordCheckBox.setGeometry(QtCore.QRect(110, 170, 111, 17))
        self.ShowPasswordCheckBox.setObjectName("ShowPasswordCheckBox")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 60, 61, 16))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 331, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionsave = QtWidgets.QAction(MainWindow)
        self.actionsave.setObjectName("actionsave")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.saveButtion.setText(_translate("MainWindow", "Save"))
        self.saveButtion.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.label.setText(_translate("MainWindow", "server"))
        self.label_2.setText(_translate("MainWindow", "login"))
        self.label_3.setText(_translate("MainWindow", "password"))
        self.CloseButtion.setText(_translate("MainWindow", "Close"))
        self.ShowPasswordCheckBox.setText(_translate("MainWindow", "show password"))
        self.label_4.setText(_translate("MainWindow", "path for files"))
        self.actionsave.setText(_translate("MainWindow", "save"))
        self.saveButtion.pressed.connect(lambda: click_save(self))
        self.CloseButtion.pressed.connect(lambda: click_close())
        self.ShowPasswordCheckBox.pressed.connect(lambda: switch_password_vision(self))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(MainWindow)
    read_config()
    MainWindow.show()
    sys.exit(app.exec_())
