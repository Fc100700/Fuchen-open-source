#此文件为注册窗口UI
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtGui import QFont


class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(390, 480)
        icon = QtGui.QIcon("./image/Component/注册.png")  # 替换为实际的图标路径
        MainWindow.setWindowIcon(icon)

        # 设置应用程序图标
        app_icon = QtGui.QIcon("./image/Component/注册.png")  # 替换为实际的图标路径
        MainWindow.setWindowIcon(app_icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        font = QFont()
        font.setPointSize(15)

        self.Name_label = QtWidgets.QLabel(self.centralwidget)
        self.Name_label.setGeometry(60,50,60,25)
        self.Name_label.setFont(font)
        self.Name_label.setText("名称")
        self.pushButton_Name = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Name.setGeometry(QtCore.QRect(30, 50, 24, 24))
        self.pushButton_Name.setObjectName("pushButton_Name")
        self.pushButton_Name.setStyleSheet("QPushButton#pushButton_Name {"
                                           "    border-image: url(./image/Component/名称.png);"
                                           "}")

        self.image_random = QtWidgets.QPushButton(self.centralwidget)
        self.image_random.setGeometry(QtCore.QRect(320, 80, 26, 26))
        self.image_random.setObjectName("image_random")
        self.image_random.setStyleSheet("QPushButton#image_random {"
                                          "    border-image: url(./image/Component/随机.png);"
                                          "}")
        self.image_random.clicked.connect(self.random_name)

        
        self.Password_label = QtWidgets.QLabel(self.centralwidget)
        self.Password_label.setGeometry(QtCore.QRect(60, 120, 70, 25))
        self.Password_label.setFont(font)
        self.Password_label.setText("密码")
        self.Password_label.setObjectName("Password_label")
        self.pushButton_Password = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Password.setGeometry(QtCore.QRect(30, 120, 24, 24))
        self.pushButton_Password.setObjectName("pushButton_Password")
        self.pushButton_Password.setStyleSheet("QPushButton#pushButton_Password {"
                                           "    border-image: url(./image/Component/密码.png);"
                                           "}")
        
        self.Email_label = QtWidgets.QLabel(self.centralwidget)
        self.Email_label.setGeometry(QtCore.QRect(60, 190, 91, 25))
        self.Email_label.setFont(font)
        self.Email_label.setObjectName("label_3")
        self.Email_label.setText("邮箱")
        self.pushButton_Email = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Email.setGeometry(QtCore.QRect(30, 190, 24, 24))
        self.pushButton_Email.setObjectName("pushButton_Email")
        self.pushButton_Email.setStyleSheet("QPushButton#pushButton_Email {"
                                               "    border-image: url(./image/Component/邮箱.png);"
                                               "}")
        
        self.Check_label = QtWidgets.QLabel(self.centralwidget)
        self.Check_label.setGeometry(QtCore.QRect(60, 260, 91, 25))
        self.Check_label.setFont(font)
        self.Check_label.setText("验证码")
        self.Check_label.setObjectName("label_4")
        self.pushButton_Check = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Check.setGeometry(QtCore.QRect(30, 260, 24, 24))
        self.pushButton_Check.setObjectName("pushButton_Check")
        self.pushButton_Check.setStyleSheet("QPushButton#pushButton_Check {"
                                            "    border-image: url(./image/Component/验证码.png);"
                                            "}")

        self.prompt = QtWidgets.QLabel(self.centralwidget)
        self.prompt.setGeometry(QtCore.QRect(30, 400, 300,41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.prompt.setFont(font)
        self.prompt.setObjectName("prompt")

        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(30, 15, 150, 25))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.title.setText("账号注册")

        self.NameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.NameEdit.setGeometry(QtCore.QRect(30, 80,330, 31))
        self.NameEdit.setObjectName("lineEdit")
        font = QFont("等线", 15)
        line_style = "QLineEdit {border: 1px solid gray; border-radius: 10px; padding: 2px; background: #f7f8fe;}"
        self.NameEdit.setStyleSheet(line_style)
        self.NameEdit.setFont(font)
        self.image_random.raise_()


        self.PasswordEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.PasswordEdit.setGeometry(QtCore.QRect(30, 150, 330, 31))
        self.PasswordEdit.setObjectName("lineEdit_2")
        self.PasswordEdit.setStyleSheet(line_style)
        self.PasswordEdit.setFont(font)

        self.EmailEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.EmailEdit.setGeometry(QtCore.QRect(30, 220, 330, 31))
        self.EmailEdit.setObjectName("lineEdit_3")
        self.EmailEdit.setStyleSheet(line_style)
        self.EmailEdit.setFont(font)

        self.CheckEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.CheckEdit.setGeometry(QtCore.QRect(30, 290, 220, 31))
        self.CheckEdit.setObjectName("lineEdit_3")
        self.CheckEdit.setStyleSheet(line_style)
        self.CheckEdit.setFont(font)
        regex = QRegExp(r'\d{6}')
        validator = QRegExpValidator(regex)
        self.CheckEdit.setValidator(validator)

        self.SigninButton = QtWidgets.QPushButton(self.centralwidget)
        self.SigninButton.setGeometry(QtCore.QRect(30, 350, 330, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.SigninButton.setFont(font)
        self.SigninButton.setObjectName("pushButton")
        # 创建自定义按钮样式
        style = """
                    QPushButton#pushButton {
                        background-color: #55c3ff;
                        border: 2px solid #55c3ff;
                        color: white;
                        border-radius: 10px;
                    }
                    QPushButton#pushButton:hover {
                        background-color: #3e8eaa;
                        border: 2px solid #3e8eaa;
                    }
                    QPushButton#pushButton:pressed {
                        background-color: #27819f;
                        border: 2px solid #27819f;
                    }
                """

        # 将样式应用到QPushButton
        self.SigninButton.setStyleSheet(style)
        self.QuitButton = QtWidgets.QPushButton(self.centralwidget)
        self.QuitButton.setStyleSheet("QPushButton#pushButton_4 {"
                                           "    border-image: url(./image/quit.png);"
                                           "}")
        self.QuitButton.setGeometry(QtCore.QRect(340, 15, 21, 21))
        self.QuitButton.setObjectName("pushButton_4")
        self.QuitButton.setToolTip('关闭')
        self.QuitButton.raise_()

        #MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.prompt.setText(_translate("MainWindow", "注:邮箱将成为您是此账号所有者的唯一证明"))
        self.SigninButton.setText(_translate("MainWindow", "注册"))

    def random_name(self):
        try:
            with open('./mod/dic/name.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if lines:
                    random_line = random.choice(lines).strip()
                    self.NameEdit.setText(random_line)
        except FileNotFoundError:
            print("The file 'name.txt' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
