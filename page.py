from datetime import datetime
import requests
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QPushButton, QButtonGroup, QMainWindow, QMenu, QDesktopWidget, QLineEdit, \
    QToolButton
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QCursor, QPainter, QColor, QIcon, QKeySequence, QFont, QLinearGradient
import oo
import ui.style
import os
import ui.oo
from ui.style import style_lineEdit

style_Radio = ui.style.style_Radio
style_Double = ui.style.style_Double
style_Spin = ui.style.style_Spin
style_CheckBox = ui.style.style_CheckBox
style_white_blue_button = ui.style.style_white_blue_button
style_white_blue_toolbutton = ui.style.style_white_blue_toolbutton
style_font_10 = ui.style.style_font_10
style_font_9 = ui.style.style_font_9
style_font_11 = ui.style.style_font_11
style_font_12 = ui.style.style_font_12
style_font_black_10 = ui.style.style_font_black_10
HImage_load_status = False
position_status = None
Name = None
Account = None
send_position = None
textedit_position = None
mode = 'login'
Version = '1.0.0'
information = '正在加载'


class CustomLineEdit(QLineEdit):  # 网易云链接解析输入框
    def __init__(self, ui_form_instance, parent=None):
        super().__init__(parent)
        self.ui_form_instance = ui_form_instance  # 保存传入的已初始化的 Ui_FormS 实例

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Paste):
            clipboard = QApplication.clipboard()
            url = clipboard.text()
            if '/#/' in url:
                url = url.replace('/#/', '/')
            if url.startswith('https://music.163.com/song?id'):
                try:
                    header = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}
                    res = requests.get(url, headers=header)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    keywords_tag = soup.find('meta', {'name': 'keywords'})
                    keywords_content = keywords_tag['content'] if keywords_tag else None
                    if keywords_content:
                        first_content = keywords_content.split('，')[0]
                        # 使用已初始化的实例设置文本
                        self.ui_form_instance._5lineEdit2.setText(first_content + ".mp3")
                except Exception as e:
                    print(e)
        super().keyPressEvent(event)

class Ui_FormS(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.setupUi(MainWindow)
        self.start_point = None
        self.window_point = None
        self.setMouseTracking(True)  # 确保捕获鼠标移动


    def setupUi(self, MainWindow):
        # 示例代码：在这里定义你的 UI 元素
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sort = "F9"
        self.end_key = "ESC"
        self.end_execute_key = "ESC"
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        MainWindow.setFixedSize(1000, 600)
        #MainWindow.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏任务栏
        MainWindow.setWindowTitle("Fuchen 浮沉制作")
        screen = QDesktopWidget().screenGeometry()
        window = MainWindow.geometry()


        self.weather_button = QtWidgets.QToolButton(MainWindow)  # 天气按钮(图标)
        self.weather_button.setObjectName("weather_button")
        self.weather_button.setGeometry(QtCore.QRect(5, 580, 80, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.weather_button.setFont(font)
        self.weather_button.setText(f"正在获取天气")
        self.weather_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.weather_button.setStyleSheet(
            "background-color: rgba(255,255,255,0); padding: 0;border: none; ")

        '''weather_thread = WeatherUpdater()
        weather_thread.start()

        self.weather_timer = QtCore.QTimer(M)
        self.weather_timer.timeout.connect(self.Update_weather)
        self.weather_timer.start(1200000)  # 更新时间的间隔，单位为毫秒'''

        self.version_label = QtWidgets.QLabel(MainWindow)
        self.version_label.setGeometry(QtCore.QRect(10, 500, 100, 20))
        self.version_label.setFont(font)
        self.version_label.setObjectName("version_label")
        self.version_label.setText(f"{Version}")

        self.run_label = QtWidgets.QLabel("运行时间 00:00:00", MainWindow)
        self.run_label.setFont(font)
        self.run_label.setGeometry(QtCore.QRect(10, 520, 200, 20))
        '''self.run_timer = QtCore.QTimer(self)
        self.run_timer.timeout.connect(self.updateTime)
        self.startTime = QtCore.QTime.currentTime()
        self.run_timer.start(1000)  # 每秒更新一次'''

        self.time_label = QtWidgets.QLabel(MainWindow)
        self.time_label.setGeometry(QtCore.QRect(10, 540, 100, 20))
        self.time_label.setFont(font)
        self.time_label.setText("当前时间 00:00:00")

        '''self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 更新时间的间隔，单位为毫秒'''

        '''self.global_timer = QtCore.QTimer(self)
        self.global_timer.timeout.connect(self.get_current_time_string)
        self.global_timer.start(1000)  # 更新时间的间隔，单位为毫秒

        self.data_thread = DataThread()
        self.data_thread.start()'''
        self.status_label = QtWidgets.QLabel(MainWindow)
        self.status_label.setGeometry(QtCore.QRect(10, 560, 70, 20))
        self.status_label.setFont(font)
        self.status_label.setText("与服务器状态:")

        self.serve_label = QtWidgets.QLabel(MainWindow)
        self.serve_label.setGeometry(QtCore.QRect(80, 560, 50, 20))
        self.serve_label.setFont(font)
        color = QtGui.QColor(36, 152, 42)  # 使用RGB值设置颜色为红色
        self.serve_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
        self.serve_label.setText("已连接")
        self.Button_Style = '''
                            QToolButton {
                                background: transparent;
                                padding: 0; /* Add this line */
                                border: none;
                            }
                            QToolButton:hover {
                                border-radius: 5px;

                                border-style: outset;
                                background-color: rgb(204,229,255);
                                border-color: rgb(204, 229, 255);
                            }'''

        self.Now_Button_Style = '''
                                QToolButton {
                                    background: transparent;
                                    border-radius: 5px;
                                    border-style: outset;
                                    background-color: rgb(96,160,235); /* 修改为选中后的颜色 */
                                    border-color: rgb(96,160,235); 
                                    padding: 0;
                                }'''
        self.button_sty = '''QToolButton {
                                        background: transparent;
                                        padding: 0; /* Add this line */
                                        border: none;}'''
        # 计算窗口居中时的位置
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.HButton = QtWidgets.QToolButton(MainWindow)
        self.HButton.setGeometry(QtCore.QRect(10, 20, 240, 90))
        global HImage_load_status
        if HImage_load_status == True:  # 判断头像是否成功加载
            self.HButton.setIcon(QIcon("./temp/HImage.png"))
        else:
            self.HButton.setIcon(QIcon("./image/float/fc.png"))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.HButton.setFont(font)
        self.HButton.setText(f" {Name}")
        self.HButton.setIconSize(QSize(80, 80))
        self.HButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.HButton.setObjectName("HButton")
        self.HButton.setStyleSheet(
            "QToolButton { background: transparent; padding: 0;border: none; }")
        self.HButton.setCursor(QCursor(Qt.PointingHandCursor))
        if mode == "tourist_login":
            self.HButton.setEnabled(False)
            self.HButton.setToolTip("游客登录无法编辑个人资料\n登录后可编辑")
        """移动滑块标签"""
        self.slabel = QtWidgets.QLabel(MainWindow)
        self.slabel.setGeometry(QtCore.QRect(10, 130, 240, 40))
        self.slabel.setObjectName("slabel")
        self.slabel.setStyleSheet("background-color: rgba(0,123,255,165); border-radius: 3px;")
        self.animation = QtCore.QPropertyAnimation(self.slabel, b"pos")

        '''第一个按钮'''
        #self.Button_1 = QtWidgets.QToolButton(MainWindow)
        self.Button_1 = ui.oo.MainAnimatedButton(MainWindow)
        self.Button_1.setGeometry(QtCore.QRect(10, 130, 240, 40))
        self.Button_1.setIcon(QIcon("./image/Component/点击.png"))
        self.Button_1.setObjectName("Button_1")
        self.Button_1.setText("   连点功能")
        self.Button_1.setIconSize(QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.Button_1.setFont(font)

        '''第二个按钮'''
        #self.Button_2 = QtWidgets.QToolButton(MainWindow)
        self.Button_2 = ui.oo.MainAnimatedButton(MainWindow)
        self.Button_2.setGeometry(QtCore.QRect(10, 190, 240, 40))
        self.Button_2.setIcon(QIcon("./image/Component/QQ.png"))
        self.Button_2.setObjectName("Button_2")
        self.Button_2.setText("   QQ消息")
        self.Button_2.setIconSize(QSize(30, 30))
        self.Button_2.setFont(font)

        #self.Button_3 = QtWidgets.QToolButton(MainWindow)
        self.Button_3 = ui.oo.MainAnimatedButton(MainWindow)
        self.Button_3.setGeometry(QtCore.QRect(10, 250, 240, 40))
        self.Button_3.setIcon(QIcon("./image/Component/组队.png"))
        self.Button_3.setObjectName("Button_3")
        self.Button_3.setText("   组队")
        self.Button_3.setIconSize(QSize(30, 30))
        self.Button_3.setFont(font)

        if mode == "tourist_login":
            self.Button_3.setEnabled(False)
            self.Button_3.setToolTip("该功能游客登录暂不可用")

        #self.Button_4 = QtWidgets.QToolButton(MainWindow)
        self.Button_4 = ui.oo.MainAnimatedButton(MainWindow)
        self.Button_4.setGeometry(QtCore.QRect(10, 310, 240, 40))
        self.Button_4.setIcon(QIcon("./image/Component/工具.png"))
        self.Button_4.setObjectName("Button_4")
        self.Button_4.setText("   工具")
        self.Button_4.setIconSize(QSize(30, 30))
        #self.Button_4.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # 设置按钮样式
        #self.Button_4.setStyleSheet(self.Button_Style)
        self.Button_4.setFont(font)

        #self.Button_More = QtWidgets.QPushButton(MainWindow)
        self.Button_More = ui.oo.ComponentButton(MainWindow)
        self.Button_More.setGeometry(QtCore.QRect(875, 8, 26, 26))
        self.Button_More.setToolTip('更多')
        self.Button_More.setObjectName("Button_More")
        self.Button_More.setIcon(QIcon("./image/same/更多.png"))
        self.Button_More.setIconSize(QtCore.QSize(21, 21))

        self.Button_More.setStyleSheet("""
            QToolButton {
                border: none;
                padding: 1px;
            }
            QToolButton::menu-indicator {
                width: 0px;
                height: 0px;
            }
        """)

        #self.Button_SetTop = QtWidgets.QPushButton(MainWindow)
        self.Button_SetTop = ui.oo.ComponentButton(MainWindow)
        self.Button_SetTop.setGeometry(QtCore.QRect(905, 8, 26, 26))
        self.Button_SetTop.setToolTip('置顶')
        self.Button_SetTop.setObjectName("Button_SetTop")
        self.Button_SetTop.setIcon(QIcon("./image/Component/Top.png"))
        self.Button_SetTop.setIconSize(QtCore.QSize(21, 21))


        self.Button_Minisize = ui.oo.ComponentButton(MainWindow)
        self.Button_Minisize.setGeometry(QtCore.QRect(935, 8, 26, 26))
        self.Button_Minisize.setIcon(QIcon("./image/short.png"))
        self.Button_Minisize.setIconSize(QtCore.QSize(19, 19))
        self.Button_Minisize.setObjectName("Button_Minisize")
        self.Button_Minisize.setToolTip('最小化')

        #self.Button_Close = QtWidgets.QPushButton(MainWindow)
        self.Button_Close = ui.oo.CloseButton(MainWindow)
        self.Button_Close.setGeometry(965, 8, 26, 26)
        self.Button_Close.setToolTip('关闭')
        self.Button_Close.setIcon(QIcon("./image/quit.png"))
        self.Button_Close.setIconSize(QtCore.QSize(24, 24))
        self.Button_Close.setObjectName("Button_Close")
        '''self.Button_Close.setStyleSheet("QPushButton#Button_Close {"
                                        "    border-image: url(./image/quit.png);"
                                        "    background-color: transparent;"
                                        "}"
                                        "QPushButton#Button_Close:hover {"
                                        "    background-color: rgba(255,0,0,100);"
                                        "    border-radius: 2px;"  # 设置悬停时的圆角半径为10像素
                                        "}")'''

        # 设置窗口位置
        MainWindow.move(x, y)
        self.is_topmost = False

        self.retranslateUi(MainWindow)
        self.textBrowser = QtWidgets.QTextBrowser(MainWindow)
        self.textBrowser.setGeometry(QtCore.QRect(10, 370, 240, 90))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setStyleSheet(ui.style.style_information_TextBrowser)

        font = QFont("等线", 12)
        self.textBrowser.setFont(font)
        self.textBrowser.setText(information)

        """右侧总框架"""
        self.stackedWidget = QtWidgets.QStackedWidget(MainWindow)
        self.stackedWidget.setGeometry(QtCore.QRect(260, 0, 740, 600))
        self.stackedWidget.setObjectName("stackedWidget")

        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.stackedWidget.addWidget(self.page_1)
        self.label_page1()

        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.label_page2()

        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.stackedWidget.addWidget(self.page_3)
        self.label_page3()

        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.stackedWidget.addWidget(self.page_4)
        self.label_page4()

        self.Button_More.raise_()
        self.Button_Minisize.raise_()
        self.Button_SetTop.raise_()
        self.Button_Close.raise_()


        self.stackedWidget.setCurrentIndex(0)



        self.Button_1.clicked.connect(lambda: self.move_label(self.Button_1))
        self.Button_2.clicked.connect(lambda: self.move_label(self.Button_2))
        self.Button_3.clicked.connect(lambda: self.move_label(self.Button_3))
        self.Button_4.clicked.connect(lambda: self.move_label(self.Button_4))
        self.Button_1.clicked.connect(self.bt_c1)
        self.Button_2.clicked.connect(self.bt_c2)
        self.Button_3.clicked.connect(self.bt_c3)
        self.Button_4.clicked.connect(self.bt_c4)

        # 创建一个菜单
        self.menu = QtWidgets.QMenu(MainWindow)
        '''self.menu.setStyleSheet("""
            QMenu {
                background-color: white;  /* 菜单背景色 */
                border: 1px solid #ccc;   /* 菜单边框 */
            }
            QMenu::item {
                padding: 2px 2px;        /* 控制文字与边界的间距，保持宽度正常 */
                spacing: 4px;             /* 图标与文字之间的间距 */
            }
            QMenu::item:selected {        /* 鼠标悬停时的样式 */
                background-color: #0078d7;  /* 蓝色背景 */
                color: white;              /* 白色文字 */
            }
            QMenu::icon {
                padding: 2px;  /* 图标的内边距，确保图标紧贴文字 */
            }
        """)'''

        self.action_option1 = self.menu.addAction(QIcon("./image/page_menu/setting.png"), "设置")
        self.action_option1.setFont(style_font_black_10)
        self.action_option2 = self.menu.addAction(QIcon("./image/page_menu/about.png"),"关于")
        self.action_option2.setFont(style_font_black_10)
        self.action_option3 = self.menu.addAction(QIcon("./image/page_menu/help.png"),"赞助")
        self.action_option3.setFont(style_font_black_10)
        self.action_option4 = self.menu.addAction(QIcon("./image/page_menu/log.png"),"日志")
        self.action_option4.setFont(style_font_black_10)
        self.action_option5 = self.menu.addAction(QIcon("./image/page_menu/web.png"),"官网")
        self.action_option5.setFont(style_font_black_10)
        self.action_option6 = self.menu.addAction("意见反馈")
        self.action_option6.setFont(style_font_black_10)
        self.action_option7 = self.menu.addAction("清空日志")
        self.action_option7.setFont(style_font_black_10)
        self.action_option8 = self.menu.addAction("清理缓存")
        self.action_option8.setFont(style_font_black_10)
        self.action_option9 = self.menu.addAction("重启软件")
        self.action_option9.setFont(style_font_black_10)
        self.action_option10 = self.menu.addAction("使用帮助")
        self.action_option10.setFont(style_font_black_10)
        self.action_option11 = self.menu.addAction("版本更新")
        self.action_option11.setFont(style_font_black_10)

        self.Button_More.setMenu(self.menu)
        self.Button_More.setPopupMode(QToolButton.InstantPopup)


    def update_time(self):
        current_time = QtCore.QDateTime.currentDateTime().toString("hh:mm:ss")
        self.time_label.setText('当前时间 ' + current_time)
        self.timer.start(1000 - QtCore.QTime.currentTime().msec())

    def paintEvent(self, event):
        painter = QPainter(self)
        # 左侧灰色矩形
        left_rect = QRect(0, 0, 260, 600)
        left_color = QColor(224, 224, 224)
        painter.fillRect(left_rect, left_color)

        # 右侧渐变矩形（从灰色到白色）
        right_rect = QRect(260, 0, 740, 600)
        gradient = QLinearGradient(right_rect.topLeft(), right_rect.bottomLeft())  # 从上到下的渐变
        gradient.setColorAt(0.0, QColor(230, 230, 230))  # 顶部为灰色
        gradient.setColorAt(1.0, QColor(241, 241, 241))  # 底部为白色
        painter.fillRect(right_rect, gradient)

    def move_label(self, button):
        # 移动标签到该按钮的右侧
        self.animation.setStartValue(self.slabel.pos())
        self.animation.setEndValue(QtCore.QPoint(button.x(), button.y()))
        self.animation.setDuration(135)
        self.animation.start()

    def Button_selection(self):
        self.Button_1.setStyleSheet(self.Button_Style)
        self.Button_2.setStyleSheet(self.Button_Style)
        self.Button_3.setStyleSheet(self.Button_Style)
        self.Button_4.setStyleSheet(self.Button_Style)

    def bt_c1(self):
        self.stackedWidget.setCurrentIndex(0)

    def bt_c2(self):
        self.stackedWidget.setCurrentIndex(1)

    def bt_c3(self):
        self.stackedWidget.setCurrentIndex(2)

    def bt_c4(self):
        self.stackedWidget.setCurrentIndex(3)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

    def label_page1(self):
        custom_widget5 = ui.style.CustomWidget(self.page_1)  # 连点框
        custom_widget5.setGeometry(QtCore.QRect(0, 0, 375, 270))
        custom_widget5.lower()

        custom_widget6 = ui.style.CustomWidget(self.page_1)  # 常见问题
        custom_widget6.setGeometry(QtCore.QRect(370, 0, 370, 270))
        custom_widget6.lower()

        custom_widget7 = ui.style.CustomWidget(self.page_1)  # 自动脚本框
        custom_widget7.setGeometry(QtCore.QRect(0, 265, 740, 335))
        custom_widget7.lower()

        font_11 = QtGui.QFont()
        font_11.setFamily("等线")
        font_11.setPointSize(11)
        self.LClick_Radio = QtWidgets.QRadioButton(self.page_1)
        self.LClick_Radio.setGeometry(QtCore.QRect(100, 70, 80, 25))
        self.LClick_Radio.setObjectName("LClick_Radio")
        self.LClick_Radio.setText("鼠标左键")
        self.LClick_Radio.setChecked(True)
        self.LClick_Radio.setStyleSheet(style_Radio)
        self.MClick_Radio = QtWidgets.QRadioButton(self.page_1)
        self.MClick_Radio.setGeometry(QtCore.QRect(190, 70, 80, 25))
        self.MClick_Radio.setObjectName("MClick_Radio")
        self.MClick_Radio.setText("鼠标中键")
        self.MClick_Radio.setStyleSheet(style_Radio)
        self.RClick_Radio = QtWidgets.QRadioButton(self.page_1)
        self.RClick_Radio.setGeometry(QtCore.QRect(280, 70, 80, 25))
        self.RClick_Radio.setObjectName("RClick_Radio")
        self.RClick_Radio.setText("鼠标右键")
        self.RClick_Radio.setStyleSheet(style_Radio)

        self.Sort_Click = QtWidgets.QLabel(self.page_1)  # 左键每秒点击次数
        self.Sort_Click.setGeometry(QtCore.QRect(25, 70, 60, 21))
        self.Sort_Click.setObjectName("Sort_Click")
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(11)
        self.Sort_Click.setFont(font)
        self.Sort_Click.setText("点击类型:")

        self._3label_5 = QtWidgets.QLabel(self.page_1)
        self._3label_5.setGeometry(QtCore.QRect(25, 20, 101, 31))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(18)
        self._3label_5.setFont(font)
        self._3label_5.setObjectName("_3label_5")
        self._3label_5.setText("连点功能")

        self._3label_8 = QtWidgets.QLabel(self.page_1)  # 左键每秒点击次数
        self._3label_8.setGeometry(QtCore.QRect(25, 120, 101, 21))
        self._3label_8.setObjectName("_3label_8")
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(11)
        self._3label_8.setFont(font)
        self._3label_8.setText("点间隔时间:")

        self._3D = QtWidgets.QDoubleSpinBox(self.page_1)  # 连点每次间隔
        self._3D.setGeometry(QtCore.QRect(130, 120, 150, 22))
        self._3D.setMinimum(0.001)
        self._3D.setValue(0.1)
        self._3D.setDecimals(3)
        self._3D.setMaximum(1000)
        self._3D.setObjectName("_3D")
        self._3D.setSingleStep(0.05)
        self._3D.setStyleSheet(style_Double)

        self._3pushButton_4 = QtWidgets.QPushButton(self.page_1)  # 左键点击
        self._3pushButton_4.setGeometry(QtCore.QRect(25, 170, 150, 35))
        self._3pushButton_4.setObjectName("_3pushButton_4")
        self._3pushButton_4.setCursor(QCursor(Qt.PointingHandCursor))
        self._3pushButton_4.setText(f"设置启停快捷键({self.sort})")
        self._3pushButton_4.setFont(style_font_10)
        self._3pushButton_4.setStyleSheet("""
                                            QPushButton {
                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                background-color: transparent;    /* 设置透明背景 */
                                                border-radius: 2px;    /* 设置圆角 */
                                            }
                                            QPushButton:hover {
                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                            }""")

        self._3pushButton_6 = QtWidgets.QPushButton(self.page_1)  # 开启连点器
        self._3pushButton_6.setGeometry(QtCore.QRect(180, 170, 125, 35))
        self._3pushButton_6.setObjectName("_3pushButton_6")
        self._3pushButton_6.setCursor(QCursor(Qt.PointingHandCursor))
        self._3pushButton_6.setText("开启连点器")
        self._3pushButton_6.setFont(style_font_10)
        self._3pushButton_6.setStyleSheet("""
                                            QPushButton {
                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                background-color: transparent;    /* 设置透明背景 */
                                                border-radius: 2px;    /* 设置圆角 */
                                            }
                                            QPushButton:hover {
                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                            }""")
        self._3pushButton_6.raise_()

        self._3pushButton_7 = QtWidgets.QPushButton(self.page_1)  # 连点器
        self._3pushButton_7.setGeometry(QtCore.QRect(310, 170, 50, 35))
        self._3pushButton_7.setObjectName("_3pushButton_7")
        self._3pushButton_7.setCursor(QCursor(Qt.PointingHandCursor))
        self._3pushButton_7.setText("关闭")
        self._3pushButton_7.setFont(style_font_10)
        self._3pushButton_7.setStyleSheet("""
                                            QPushButton {
                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                background-color: transparent;    /* 设置透明背景 */
                                                border-radius: 2px;    /* 设置圆角 */
                                            }
                                            QPushButton:hover {
                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                            }""")
        self._3pushButton_7.setVisible(False)

        self.problem_label = QtWidgets.QLabel(self.page_1)
        self.problem_label.setGeometry(QtCore.QRect(25, 220, 320, 40))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.problem_label.setFont(font)
        self.problem_label.setObjectName("problem_label")
        self.problem_label.setOpenExternalLinks(True)
        self.problem_label.setText(
            "若开启连点器后提示dll缺失<br><a href='https://wwt.lanzout.com/i1Sbx1uur2ta'>请安装运行库后再次尝试</a>")

        self.auto_label = QtWidgets.QLabel(self.page_1)
        self.auto_label.setGeometry(QtCore.QRect(25, 280, 150, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.auto_label.setFont(font)
        self.auto_label.setObjectName("auto_label")
        self.auto_label.setText("自动脚本功能")

        self.ques_label = QtWidgets.QLabel(self.page_1)
        self.ques_label.setGeometry(QtCore.QRect(390, 10, 150, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.ques_label.setFont(font)
        color = QtGui.QColor(29, 84, 237)  # 使用RGB值设置颜色为红色
        self.ques_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
        self.ques_label.setObjectName("ques_label")
        self.ques_label.setText("常见问题:")

        self.quest_label = QtWidgets.QLabel(self.page_1)
        self.quest_label.setGeometry(QtCore.QRect(390, 50, 350, 200))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.quest_label.setFont(font)
        self.quest_label.setObjectName("quest_label")
        self.quest_label.setFont(style_font_10)
        self.quest_label.setText("连点器目前是使用C++的exe进行调用的\n最高速度大概为400/S\n软件开启后 请等待几秒再开启连点器\n请不要频繁开启和关闭连点器 可能会崩溃\n\n"
                                 "自动脚本功能需要先点击记录按钮记录操作 esc退出记录\n"
                                 "在记录和执行自动脚本之前需要选择配置文件\n"
                                 "自动脚本功能的部分按键可能无法生效\n"
                                 "该功能会储存配置到本地 下次启动软件也还可以使用\n目前该功能执行的时间可能会比记录的时间长\n因为Python语言执行效率低 后期考虑优化\n目前实际执行会比记录的时间长5~20%左右\n\n鼠标信息可以查看很多信息")

        self.label_auto = QtWidgets.QLabel(self.page_1)  # 左键每秒点击次数
        self.label_auto.setGeometry(QtCore.QRect(25, 350, 101, 21))
        self.label_auto.setObjectName("label_auto")
        self.label_auto.setFont(font_11)
        self.label_auto.setText("配置文件")

        self.reflash = QtWidgets.QPushButton(self.page_1)
        self.reflash.setGeometry(QtCore.QRect(260, 350, 24, 24))
        self.reflash.setObjectName("reflash")
        self.reflash.setToolTip('刷新')
        self.reflash.setStyleSheet("QPushButton#reflash {"
                                   "    border-image: url(./image/Component/刷新.png);"
                                   "}")



        # 列出文件夹中的所有文件和文件夹
        files_in_folder = os.listdir("scripts")

        # 检查文件夹中是否有文件
        if len(files_in_folder) == 0:
            txt = "暂无配置文件 需要创建"
        else:
            txt = '选择配置文件'

        self.button_file = QPushButton(txt, self.page_1)
        self.button_file.setGeometry(100, 350, 150, 25)
        self.button_file.setIcon(QIcon('./image/Component/箭头 下.png'))
        self.button_file.clicked.connect(self.showMenu)
        self.button_file.setFont(style_font_9)
        self.button_file.setObjectName("button_file")
        self.button_file.setStyleSheet("""
                                        QPushButton {
                                            border: 1px solid #989898;    /* 设置为RGB颜色边框 */
                                            background-color: transparent;    /* 设置透明背景 */
                                            border-radius: 3px;    /* 设置圆角 */
                                        }
                                        QPushButton:hover {
                                                background-color: #a6a6a6;
                                                border: 1px solid #7d7d7d;
                                            }
                                    """)
        self.file_menu = QMenu(self.centralwidget)
        self.populateMenu('scripts')  # 替换为实际文件夹路径

        self.label_new = QtWidgets.QLabel(self.page_1)  # 左键每秒点击次数
        self.label_new.setGeometry(QtCore.QRect(25, 400, 101, 21))
        self.label_new.setObjectName("label_new")
        self.label_new.setFont(font_11)
        self.label_new.setText("新建配置文件")

        self.file_lineEdit = QtWidgets.QLineEdit(self.page_1)
        self.file_lineEdit.setGeometry(QtCore.QRect(130, 400, 150, 20))
        self.file_lineEdit.setObjectName("file_lineEdit")
        self.file_lineEdit.setStyleSheet("background: transparent;")
        self.file_lineEdit.setPlaceholderText("输入文件名称")
        self.file_lineEdit.setFont(style_font_9)
        self.file_lineEdit.setText(self.generate_initial_filename())

        self.button_create = QtWidgets.QPushButton(self.page_1)
        self.button_create.setGeometry(QtCore.QRect(280, 400, 50, 20))
        self.button_create.setObjectName("button_create")
        self.button_create.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_create.setText("创建")
        self.button_create.setStyleSheet("QPushButton#button_create {"
                                         "background-color: #3498db;"  # Blue background color
                                         "border-radius: 4px;"  # 10px border radius for rounded corners
                                         "color: white;"
                                         "padding: 300px 300px;"
                                         "text-align: center;"
                                         "text-decoration: none;"
                                         "font-size: 13px;"
                                         "font-family: SimSun, Arial, sans-serif;"
                                         "}")
        self.impor_button = QtWidgets.QPushButton(self.page_1)
        #self.impor_button = oo.NormolAnimatedButton(self.page_1)
        self.impor_button.setGeometry(QtCore.QRect(25, 500, 140, 22))
        #self.impor_button.setGeometry(QtCore.QRect(360, 510, 180, 25))
        self.impor_button.setObjectName("impor_button")
        self.impor_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.impor_button.setText("编辑选中的文件")
        self.impor_button.setFont(style_font_10)
        self.impor_button.setStyleSheet("""QPushButton {
                                            border: 1px solid #989898;    /* 设置为RGB颜色边框 */
                                            background-color: transparent;    /* 设置透明背景 */
                                            border-radius: 3px;    /* 设置圆角 */
                                        }
                                        QPushButton:hover {
                                                background-color: #a6a6a6;
                                                border: 1px solid #7d7d7d;
                                            }""")


        self.delete_button = QtWidgets.QPushButton(self.page_1)
        #self.delete_button = oo.NormolAnimatedButton(self.page_1)
        self.delete_button.setGeometry(QtCore.QRect(190, 500, 140, 22))
        self.delete_button.setObjectName("delete_button")
        self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.delete_button.setText("删除选中的文件")
        self.delete_button.setFont(style_font_10)
        self.delete_button.setStyleSheet("""QPushButton {
                                                    border: 1px solid #989898;    /* 设置为RGB颜色边框 */
                                                    background-color: transparent;    /* 设置透明背景 */
                                                    border-radius: 3px;    /* 设置圆角 */
                                                }
                                                QPushButton:hover {
                                                        background-color: #a6a6a6;
                                                        border: 1px solid #7d7d7d;
                                                    }""")

        # self._3pushButton = QtWidgets.QPushButton(self.page_1)
        self._3pushButton = oo.AnimatedButton(self.page_1)
        self._3pushButton.setGeometry(QtCore.QRect(25, 540, 140, 30))
        self._3pushButton.setObjectName("_3pushButton")
        self._3pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self._3pushButton.setText("记录自动脚本")
        self._3pushButton.setFont(style_font_10)

        self._3pushButton_2 = QtWidgets.QPushButton(self.page_1)
        self._3pushButton_2.setGeometry(QtCore.QRect(190, 540, 140, 30))
        self._3pushButton_2.setObjectName("_3pushButton_2")
        self._3pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
        self._3pushButton_2.setText("执行自动脚本")
        self._3pushButton_2.setStyleSheet("QPushButton#_3pushButton_2 {"
                                          "background-color: #4667ff;"
                                          "border-radius: 4px;"
                                          "color: white;"
                                          "padding: 300px 300px;"
                                          "text-align: center;"
                                          "text-decoration: none;"
                                          "}")
        self._3pushButton_2.setFont(style_font_10)

        self._3label_10 = QtWidgets.QLabel(self.page_1)  #
        self._3label_10.setGeometry(QtCore.QRect(25, 450, 60, 21))
        self._3label_10.setObjectName("_3label_10")
        self._3label_10.setFont(font_11)
        self._3label_10.setText("执行次数:")

        self._3spinBox_3 = QtWidgets.QSpinBox(self.page_1)  # 自动脚本执行次数
        self._3spinBox_3.setGeometry(QtCore.QRect(110, 450, 60, 22))
        self._3spinBox_3.setMaximum(9999)
        self._3spinBox_3.setValue(1)
        self._3spinBox_3.setObjectName("_3spinBox_3")
        self._3spinBox_3.setStyleSheet(style_Spin)

        self._3label_11 = QtWidgets.QLabel(self.page_1)
        self._3label_11.setGeometry(QtCore.QRect(360, 400, 150, 21))
        self._3label_11.setObjectName("_3label_11")
        self._3label_11.setFont(font_11)
        self._3label_11.setText("等待/秒后 记录/执行:")

        self.wait_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.page_1)  # 自动脚本等待执行时间
        self.wait_doubleSpinBox.setGeometry(QtCore.QRect(510, 400, 60, 22))
        self.wait_doubleSpinBox.setMaximum(1000)
        self.wait_doubleSpinBox.setMinimum(0)
        self.wait_doubleSpinBox.setValue(0)
        self.wait_doubleSpinBox.setObjectName("wait_doubleSpinBox")
        self.wait_doubleSpinBox.setStyleSheet(style_Double)

        self.label_replay_speed = QtWidgets.QLabel(self.page_1)
        self.label_replay_speed.setGeometry(QtCore.QRect(360, 450, 150, 21))
        self.label_replay_speed.setObjectName("label_replay_speed")
        self.label_replay_speed.setFont(font_11)
        self.label_replay_speed.setText("重播执行相对速度 % :")

        self.spinbox_play_speed = QtWidgets.QSpinBox(self.page_1)  # 自动脚本执行次数
        self.spinbox_play_speed.setGeometry(QtCore.QRect(510, 450, 60, 22))
        self.spinbox_play_speed.setMaximum(1000)
        self.spinbox_play_speed.setMinimum(1)
        self.spinbox_play_speed.setValue(100)
        self.spinbox_play_speed.setSingleStep(20)
        self.spinbox_play_speed.setObjectName("spinbox_play_speed")
        self.spinbox_play_speed.setStyleSheet(style_Spin)



        self._3pushButton_5 = QtWidgets.QPushButton(self.page_1)
        self._3pushButton_5.setGeometry(QtCore.QRect(360, 350, 91, 23))
        self._3pushButton_5.setObjectName("_3pushButton_4")
        self._3pushButton_5.setCursor(QCursor(Qt.PointingHandCursor))
        self._3pushButton_5.setText("鼠标信息")
        self._3pushButton_5.setFont(style_font_10)
        self._3pushButton_5.setStyleSheet("""
                                            QPushButton {
                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                background-color: transparent;    /* 设置透明背景 */
                                                border-radius: 2px;    /* 设置圆角 */
                                            }
                                            QPushButton:hover {
                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                            }""")



        self.label_end = QtWidgets.QLabel(self.page_1)
        self.label_end.setGeometry(QtCore.QRect(360, 500, 100, 21))
        self.label_end.setObjectName("label_end")
        self.label_end.setFont(font_11)
        self.label_end.setText("结束录制按键")

        self.end_key_button = QtWidgets.QPushButton(self.page_1)  # 结束按键设置
        self.end_key_button.setGeometry(QtCore.QRect(480, 500, 70, 25))
        self.end_key_button.setObjectName("end_key_button")
        self.end_key_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.end_key_button.setText(f"{self.end_key}")
        self.end_key_button.setFont(style_font_10)
        self.end_key_button.setStyleSheet("""
                                            QPushButton {
                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                background-color: transparent;    /* 设置透明背景 */
                                                border-radius: 2px;    /* 设置圆角 */
                                            }
                                            QPushButton:hover {
                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                            }""")

        self.lable_execute_end = QtWidgets.QLabel(self.page_1)
        self.lable_execute_end.setGeometry(QtCore.QRect(360, 550, 130, 21))
        self.lable_execute_end.setObjectName("lable_execute_end")
        self.lable_execute_end.setFont(font_11)
        self.lable_execute_end.setText("结束执行按键")

        self.end_execute_button = QtWidgets.QPushButton(self.page_1)  # 结束按键设置
        self.end_execute_button.setGeometry(QtCore.QRect(480, 550, 70, 25))
        self.end_execute_button.setObjectName("end_execute_button")
        self.end_execute_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.end_execute_button.setText(f"{self.end_execute_key}")
        self.end_execute_button.setFont(style_font_10)
        self.end_execute_button.setStyleSheet("""
                                                    QPushButton {
                                                        border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                        background-color: transparent;    /* 设置透明背景 */
                                                        border-radius: 2px;    /* 设置圆角 */
                                                    }
                                                    QPushButton:hover {
                                                        background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                        border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                    }""")

    def label_page2(self):
        custom_widget = ui.style.CustomWidget(self.page_2)  # 句柄框
        custom_widget.setGeometry(QtCore.QRect(0, 0, 510, 270))
        custom_widget.lower()

        custom_widget2 = ui.style.CustomWidget(self.page_2)  # 常见问题框
        custom_widget2.setGeometry(QtCore.QRect(505, 0, 235, 270))
        custom_widget2.lower()

        custom_widget3 = ui.style.CustomWidget(self.page_2)  # 模拟点击
        custom_widget3.setGeometry(QtCore.QRect(0, 265, 740, 335))
        custom_widget3.lower()

        self._2label_7 = QtWidgets.QLabel(self.page_2)
        self._2label_7.setGeometry(QtCore.QRect(20, 15, 151, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self._2label_7.setFont(font)
        self._2label_7.setObjectName("_2label_7")
        self._2label_7.setText("句柄式发送消息")

        self.pushButton_tooltip_handle = QtWidgets.QPushButton(self.page_2)
        self.pushButton_tooltip_handle.setGeometry(QtCore.QRect(180, 20, 24, 24))
        self.pushButton_tooltip_handle.setStyleSheet("QPushButton {"
                                                     "    border-image: url(./image/Component/提示3.png);"
                                                     "    background-color: rgba(245,245,245,0);"

                                                     "}")
        self.pushButton_tooltip_handle.setToolTip(
            "使用句柄进行消息发送:\n需要先点击取值按钮 然后再点击QQ聊天窗口 就可以发送消息了\n有时可能会发送失败 需打开任务管理器将QQ其他进程关闭\n只保留聊天框进程")

        self.old_QQ = QtWidgets.QRadioButton(self.page_2)
        self.old_QQ.setGeometry(QtCore.QRect(20, 60, 80, 20))
        self.old_QQ.setObjectName("old_QQ")
        self.old_QQ.setText("旧版QQ")
        self.old_QQ.setFont(style_font_11)
        self.old_QQ.setChecked(True)
        self.old_QQ.setStyleSheet(style_Radio)
        self.old_QQ.setToolTip("9.7.23及之前版本")

        self.new_QQ = QtWidgets.QRadioButton(self.page_2)
        self.new_QQ.setGeometry(QtCore.QRect(130, 60, 80, 20))
        self.new_QQ.setObjectName("new_QQ")
        self.new_QQ.setText("新版QQ")
        self.new_QQ.setFont(style_font_11)
        self.new_QQ.setStyleSheet(style_Radio)
        self.new_QQ.setToolTip("9.9.15及后续版本")

        group1 = QButtonGroup(self)
        group1.addButton(self.old_QQ)
        group1.addButton(self.new_QQ)

        self._2label_8 = QtWidgets.QLabel(self.page_2)
        self._2label_8.setGeometry(QtCore.QRect(20, 100, 51, 21))
        self._2label_8.setObjectName("_2label_8")
        self._2label_8.setFont(style_font_11)
        self._2label_8.setText("句柄:")

        self._2lineEdit_3 = QtWidgets.QLineEdit(self.page_2)  # 句柄值输入框
        self._2lineEdit_3.setGeometry(QtCore.QRect(70, 100, 150, 21))
        self._2lineEdit_3.setObjectName("_2lineEdit_3")
        #self._2lineEdit_3.setStyleSheet("background: transparent;")
        self._2lineEdit_3.setStyleSheet(style_lineEdit)
        self._2lineEdit_3.setPlaceholderText("句柄值")
        self._2lineEdit_3.setFont(style_font_10)

        self._2pushButton2 = QtWidgets.QPushButton(self.page_2)  # 获取句柄值
        self._2pushButton2.setGeometry(QtCore.QRect(20, 140, 200, 21))
        self._2pushButton2.setObjectName("_2pushButton2")
        self._2pushButton2.setCursor(QCursor(Qt.PointingHandCursor))
        self._2pushButton2.setText("点击此处后单击聊天窗口获取句柄")
        self._2pushButton2.setFont(style_font_10)
        self._2pushButton2.setStyleSheet("""
                                        QPushButton {
                                            border: 1px solid #989898;    /* 设置为RGB颜色#3498db的边框 */
                                            background-color: transparent;    /* 设置透明背景 */
                                            border-radius: 3px;    /* 设置圆角 */
                                        }
                                        QPushButton:hover {
                                            background-color: #CDCDCD;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                            border: 1px solid #989898;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                        }
                                    """)

        self._2label_10 = QtWidgets.QLabel(self.page_2)  # 句柄发送次数
        self._2label_10.setGeometry(QtCore.QRect(20, 180, 80, 22))
        self._2label_10.setObjectName("_2label_10")
        self._2label_10.setFont(style_font_11)
        self._2label_10.setText("发送次数:")

        self._2spinBox = QtWidgets.QSpinBox(self.page_2)  # 句柄式发送次数
        self._2spinBox.setGeometry(QtCore.QRect(120, 180, 100, 22))
        self._2spinBox.setMaximum(9999)
        self._2spinBox.setValue(10)
        self._2spinBox.setObjectName("_2spinBox")
        self._2spinBox.setStyleSheet(style_Spin)
        self._2spinBox.setMinimum(1)

        self._2label_speed = QtWidgets.QLabel(self.page_2)  # 句柄发送次数
        self._2label_speed.setGeometry(QtCore.QRect(20, 220, 85, 22))
        self._2label_speed.setObjectName("_2label_speed")
        self._2label_speed.setFont(style_font_11)
        self._2label_speed.setText("发送间隔/秒:")

        self._2doubleSpinBox_speed = QtWidgets.QDoubleSpinBox(self.page_2)
        self._2doubleSpinBox_speed.setGeometry(QtCore.QRect(120, 220, 100, 22))
        self._2doubleSpinBox_speed.setMinimum(0.01)
        self._2doubleSpinBox_speed.setValue(0.1)
        self._2doubleSpinBox_speed.setObjectName("_2doubleSpinBox_speed")
        self._2doubleSpinBox_speed.setSingleStep(0.05)
        self._2doubleSpinBox_speed.setStyleSheet(style_Double)

        self._2label_9 = QtWidgets.QLabel(self.page_2)  # 内容提示
        self._2label_9.setGeometry(QtCore.QRect(240, 60, 111, 22))
        self._2label_9.setObjectName("_2label_9")
        self._2label_9.setFont(style_font_11)
        self._2label_9.setText("需要发送的内容：")

        self._2textEdit = QtWidgets.QTextEdit(self.page_2)  # 句柄发送内容
        self._2textEdit.setGeometry(QtCore.QRect(240, 90, 260, 110))
        self._2textEdit.setObjectName("_2textEdit")
        self._2textEdit.setStyleSheet(ui.style.style_textEdit)
        self._2textEdit.setFont(style_font_11)
        self._2textEdit.setAcceptDrops(False)
        self._2textEdit.setPlaceholderText("在此处输入需要发送的内容\n注：不能使用数字作为开头")

        self._2pushButton_3 = oo.NormolAnimatedButton(self.page_2)
        self._2pushButton_3.setGeometry(QtCore.QRect(240, 220, 260, 26))
        self._2pushButton_3.setObjectName("_2pushButton_3")
        self._2pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
        self._2pushButton_3.setText("开始发送")
        self._2pushButton_3.setFont(style_font_11)

        """下方为模拟点击功能"""

        self.tlabel = QtWidgets.QLabel(self.page_2)
        self.tlabel.setGeometry(QtCore.QRect(20, 280, 200, 24))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.tlabel.setFont(font)
        self.tlabel.setObjectName("tlabel")
        self.tlabel.setText("模拟点击消息发送")


        self._2label = QtWidgets.QLabel(self.page_2)
        self._2label.setGeometry(QtCore.QRect(20, 320, 100, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self._2label.setFont(font)
        self._2label.setObjectName("_2label")
        self._2label.setText("@QQ功能")

        self.pushButton_tooltip_qq = QtWidgets.QPushButton(self.page_2)
        self.pushButton_tooltip_qq.setGeometry(QtCore.QRect(120, 320, 24, 24))
        self.pushButton_tooltip_qq.setStyleSheet("QPushButton {"
                                                 "    border-image: url(./image/Component/提示3.png);"
                                                 "    background-color: rgba(245,245,245,0);"
                                                 "}")
        self.pushButton_tooltip_qq.setToolTip(
            "此功能的作用是在群聊窗口中先输入\n@符号再输入QQ号来达到at功能 发送\n出去的内容将是qq号+复制的内容 该\n功能的作用是在群聊中对某位用户进\n行特定提醒 若选中输入后缀则在内容\n末尾添加本次发送的次数")

        self._2label_2 = QtWidgets.QLabel(self.page_2)
        self._2label_2.setGeometry(QtCore.QRect(20, 360, 50, 21))
        self._2label_2.setFont(style_font_10)
        self._2label_2.setObjectName("_2label_2")
        self._2label_2.setText("QQ号:")

        self._2lineEdit = QtWidgets.QLineEdit(self.page_2)
        self._2lineEdit.setGeometry(QtCore.QRect(70, 360, 130, 20))
        self._2lineEdit.setObjectName("_2lineEdit")
        self._2lineEdit.setStyleSheet(style_lineEdit)
        self._2lineEdit.setFont(style_font_9)
        self._2lineEdit.setPlaceholderText("输入需要@的QQ号")

        self._2label_3 = QtWidgets.QLabel(self.page_2)
        self._2label_3.setGeometry(QtCore.QRect(20, 390, 101, 20))
        self._2label_3.setFont(style_font_10)
        self._2label_3.setText("操作间隔 次/秒")

        self._2doubleSpinBox = QtWidgets.QDoubleSpinBox(self.page_2)
        self._2doubleSpinBox.setGeometry(QtCore.QRect(130, 390, 62, 20))
        self._2doubleSpinBox.setMinimum(0.01)
        self._2doubleSpinBox.setValue(0.05)
        self._2doubleSpinBox.setObjectName("_2doubleSpinBox")
        self._2doubleSpinBox.setSingleStep(0.02)
        self._2doubleSpinBox.setStyleSheet(style_Double)

        self._2checkBox = QtWidgets.QCheckBox(self.page_2)
        self._2checkBox.setGeometry(QtCore.QRect(20, 420, 121, 21))
        self._2checkBox.setObjectName("_2checkBox")
        self._2checkBox.setText("输入数字后缀")
        self._2checkBox.setToolTip("选中后 在发送时将在内容后添加此次发送的数字序号")
        self._2checkBox.setFont(style_font_10)
        self._2checkBox.setStyleSheet(style_CheckBox)

        self._2pushButton = oo.NormolAnimatedButton(self.page_2)
        self._2pushButton.setGeometry(QtCore.QRect(20, 450, 180, 25))
        self._2pushButton.setObjectName("_2pushButton")
        self._2pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self._2pushButton.setText("开始发送")
        self._2pushButton.setFont(style_font_10)

        self.label_copy = QtWidgets.QLabel(self.page_2)
        self.label_copy.setGeometry(QtCore.QRect(20, 490, 140, 24))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(15)
        self.label_copy.setFont(font)
        self.label_copy.setObjectName("label_copy")
        self.label_copy.setText("复制内容发送")

        self.pushButton_tooltip_copy = QtWidgets.QPushButton(self.page_2)
        self.pushButton_tooltip_copy.setGeometry(QtCore.QRect(150, 490, 24, 24))
        self.pushButton_tooltip_copy.setStyleSheet("QPushButton {"
                                                   "    border-image: url(./image/Component/提示3.png);"
                                                   "    background-color: rgba(245,245,245,0);"
                                                   "}")
        self.pushButton_tooltip_copy.setToolTip(
            "此功能的作用是在群聊中发送复制的内容\n此功能需要先复制要发送的内容\n点击开始发送将自动粘贴\n要发送的内容到聊天框中\n发送前仍需要先设置位置")

        self.copy_label = QtWidgets.QLabel(self.page_2)
        self.copy_label.setGeometry(QtCore.QRect(20, 520, 150, 20))
        self.copy_label.setObjectName("copy_label")
        self.copy_label.setFont(style_font_10)
        self.copy_label.setText("操作间隔 次/秒")

        self.copy_int = QtWidgets.QDoubleSpinBox(self.page_2)  # 复制发送次数
        self.copy_int.setGeometry(QtCore.QRect(130, 520, 60, 20))
        self.copy_int.setMinimum(0.01)
        self.copy_int.setValue(0.05)
        self.copy_int.setSingleStep(0.02)
        self.copy_int.setObjectName("copy_int")
        self.copy_int.setStyleSheet(style_Double)

        # self._2pushButton_4 = QtWidgets.QPushButton(self.page_2)
        self._2pushButton_4 = oo.NormolAnimatedButton(self.page_2)
        self._2pushButton_4.setGeometry(QtCore.QRect(20, 550, 180, 25))
        self._2pushButton_4.setObjectName("_2pushButton_4")
        self._2pushButton_4.setCursor(QCursor(Qt.PointingHandCursor))
        self._2pushButton_4.setText("发送复制内容")
        self._2pushButton_4.setFont(style_font_10)

        """位置记录"""
        self.label_positions = QtWidgets.QLabel(self.page_2)
        self.label_positions.setGeometry(QtCore.QRect(540, 380, 180, 40))
        self.label_positions.setFont(style_font_10)
        self.label_positions.setObjectName("_2label_2")
        self.label_positions.setText("此栏所有功能\n都需要先设置位置才能发送")

        self.label_position_status = QtWidgets.QLabel(self.page_2)
        self.label_position_status.setGeometry(QtCore.QRect(540, 430, 150, 16))
        self.label_position_status.setFont(style_font_10)
        self.label_position_status.setObjectName("label_position_status")
        if position_status != True:
            self.label_position_status.setText(
                '<font color="black">位置设置：</font> <font color="red">未设置</font>')
        else:
            self.label_position_status.setText(
                '<font color="black">位置设置：</font> <font color="green">已设置</font>')



        self.label_position_text = QtWidgets.QLabel(self.page_2)
        self.label_position_text.setGeometry(QtCore.QRect(540, 470, 180, 16))
        self.label_position_text.setFont(style_font_10)
        self.label_position_text.setObjectName("label_position_text")
        if position_status != True:
            self.label_position_text.setText(
                f'<font color="black">聊天框位置：</font> <font color="red">{textedit_position}</font>')
        else:
            self.label_position_text.setText(
                f'<font color="black">聊天框位置：</font> <font color="green">{textedit_position}</font>')

        self.label_position_send = QtWidgets.QLabel(self.page_2)
        self.label_position_send.setGeometry(QtCore.QRect(540, 510, 180, 16))
        self.label_position_send.setFont(style_font_10)
        self.label_position_send.setObjectName("label_position_send")
        if position_status != True:
            self.label_position_send.setText(
                f'<font color="black">发送键位置：</font> <font color="red">{send_position}</font>')
        else:
            self.label_position_send.setText(
                f'<font color="black">发送键位置：</font> <font color="green">{send_position}</font>')


        self.record_position_button = oo.NormolAnimatedButton(self.page_2)
        self.record_position_button.setGeometry(QtCore.QRect(540, 550, 160, 25))
        self.record_position_button.setObjectName("record_position_button")
        self.record_position_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.record_position_button.setText("记录按钮位置")
        self.record_position_button.setFont(style_font_10)


        '''self._2pushButton_5 = QtWidgets.QPushButton(self.page_2)
        self._2pushButton_5.setGeometry(QtCore.QRect(380, 520, 121, 31))
        self._2pushButton_5.setObjectName("_2pushButton_5")
        self._2pushButton_5.setCursor(QCursor(Qt.PointingHandCursor))
        self._2pushButton_5.setText("发送快捷消息")
        self._2pushButton_5.setStyleSheet("QPushButton#_2pushButton_5 {"
                                          "background-color: #3498db;"  # Blue background color
                                          "border-radius: 4px;"  # 10px border radius for rounded corners
                                          "color: white;"
                                          "padding: 100px 100px;"
                                          "text-align: center;"
                                          "text-decoration: none;"
                                          "font-size: 13px;"
                                          "font-family: SimSun, Arial, sans-serif;"
                                          "}")'''



        self._2label_4 = QtWidgets.QLabel(self.page_2)
        self._2label_4.setGeometry(QtCore.QRect(515, 20, 100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self._2label_4.setFont(font)
        color = QtGui.QColor(29, 84, 237)  # 使用RGB值设置颜色为红色
        self._2label_4.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
        self._2label_4.setObjectName("_2label_4")
        self._2label_4.setText("常见问题:")

        self._2label_5 = QtWidgets.QLabel(self.page_2)
        self._2label_5.setGeometry(QtCore.QRect(520, 40, 220, 200))
        self._2label_5.setObjectName("_2label_5")
        self._2label_5.setFont(style_font_10)
        self._2label_5.setText(
            "推荐使用：句柄式发送消息\n其他功能都是通过模拟点击来发送\n如果您没有其他需求不推荐使用\n如果您需要自定义句柄式内容\n请在内容框输入###UNCOPY###\n模拟点击退出方法:长按F10即可退出 \n或者按下ctrl+alt+del即可强制关闭\n"
            "有时可能会出现延时关闭的情况\n\n注:使用功能时请将QQ消息发送\n快捷键从CTRL+ENTER改为ENTER")

        self.label_order = QtWidgets.QLabel(self.page_2)
        self.label_order.setGeometry(QtCore.QRect(240, 320, 140, 24))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(15)
        self.label_order.setFont(font)
        self.label_order.setObjectName("label_order")
        self.label_order.setText("序列内容发送")

        self.order_select_label = QtWidgets.QLabel(self.page_2)
        self.order_select_label.setGeometry(QtCore.QRect(240, 360, 150, 20))
        self.order_select_label.setObjectName("order_select_label")
        self.order_select_label.setText("文件选择")
        self.order_select_label.setFont(style_font_10)

        #self.order_lineEdit = QtWidgets.QLineEdit(self.page_2)
        #self.order_lineEdit = DraggableLineEdit('txt', self.page_2)
        self.order_lineEdit = ui.style.DraggableLineEdit('txt', self.page_2)
        self.order_lineEdit.setGeometry(QtCore.QRect(300, 360, 220, 20))
        self.order_lineEdit.setObjectName("order_lineEdit")
        self.order_lineEdit.setStyleSheet(style_lineEdit)
        self.order_lineEdit.setPlaceholderText("选择或拖拽文件到此处")
        self.order_lineEdit.setFont(style_font_9)

        self.order_toolButton = QtWidgets.QToolButton(self.page_2)
        self.order_toolButton.setGeometry(QtCore.QRect(460, 390, 60, 18))
        self.order_toolButton.setObjectName("order_toolButton")
        self.order_toolButton.setText("选择文件")
        self.order_toolButton.setFont(style_font_9)
        self.order_toolButton.setStyleSheet("""
                                            QToolButton {
                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                background-color: transparent;    /* 设置透明背景 */
                                                border-radius: 2px;    /* 设置圆角 */
                                            }
                                            QToolButton:hover {
                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                            }
                                        """)

        self.order_radio_list = QtWidgets.QRadioButton(self.page_2)
        self.order_radio_list.setGeometry(QtCore.QRect(240, 420, 80, 20))
        self.order_radio_list.setObjectName("order_radio_list")
        self.order_radio_list.setText("顺序发送")
        self.order_radio_list.setChecked(True)
        self.order_radio_list.setStyleSheet(style_Radio)

        self.order_radio_random = QtWidgets.QRadioButton(self.page_2)
        self.order_radio_random.setGeometry(QtCore.QRect(400, 420, 80, 20))
        self.order_radio_random.setObjectName("order_radio_random")
        self.order_radio_random.setText("随机发送")
        self.order_radio_random.setStyleSheet(style_Radio)

        self.order_list_int_label = QtWidgets.QLabel(self.page_2)
        self.order_list_int_label.setGeometry(QtCore.QRect(240, 460, 150, 20))
        self.order_list_int_label.setObjectName("order_list_int_label")
        self.order_list_int_label.setText("遍数：")
        self.order_list_int_label.setFont(style_font_10)

        self.order_list_int = QtWidgets.QSpinBox(self.page_2)  # 顺序序列发送次数
        self.order_list_int.setGeometry(QtCore.QRect(280, 460, 60, 20))
        self.order_list_int.setMaximum(999)
        self.order_list_int.setValue(1)
        self.order_list_int.setObjectName("order_list_int")
        self.order_list_int.setStyleSheet(style_Spin)

        self.order_random_int_label = QtWidgets.QLabel(self.page_2)
        self.order_random_int_label.setGeometry(QtCore.QRect(400, 460, 150, 20))
        self.order_random_int_label.setObjectName("order_random_int_label")
        self.order_random_int_label.setText("条数：")
        self.order_random_int_label.setFont(style_font_10)
        self.order_random_int_label.setEnabled(False)

        self.order_random_int = QtWidgets.QSpinBox(self.page_2)  # 随机序列发送次数
        self.order_random_int.setGeometry(QtCore.QRect(450, 460, 70, 20))
        self.order_random_int.setMaximum(9999)
        self.order_random_int.setValue(10)
        self.order_random_int.setObjectName("order_random_int")
        self.order_random_int.setStyleSheet(style_Spin)
        self.order_random_int.setEnabled(False)

        self.order_list_speed = QtWidgets.QLabel(self.page_2)
        self.order_list_speed.setGeometry(QtCore.QRect(240, 500, 150, 20))
        self.order_list_speed.setObjectName("order_list_speed")
        self.order_list_speed.setText("操作间隔/秒")
        self.order_list_speed.setFont(style_font_10)

        self._2doubleSpinBox_order_list = QtWidgets.QDoubleSpinBox(self.page_2)
        self._2doubleSpinBox_order_list.setGeometry(QtCore.QRect(320, 500, 62, 20))
        self._2doubleSpinBox_order_list.setMinimum(0.01)
        self._2doubleSpinBox_order_list.setValue(0.1)
        self._2doubleSpinBox_order_list.setObjectName("_2doubleSpinBox_order_list")
        self._2doubleSpinBox_order_list.setSingleStep(0.05)
        self._2doubleSpinBox_order_list.setStyleSheet(style_Double)

        self.order_random_speed = QtWidgets.QLabel(self.page_2)
        self.order_random_speed.setGeometry(QtCore.QRect(400, 500, 150, 20))
        self.order_random_speed.setObjectName("order_random_speed")
        self.order_random_speed.setText("操作间隔/秒")
        self.order_random_speed.setFont(style_font_10)
        self.order_random_speed.setEnabled(False)

        self._2doubleSpinBox_order_random = QtWidgets.QDoubleSpinBox(self.page_2)
        self._2doubleSpinBox_order_random.setGeometry(QtCore.QRect(470, 500, 50, 20))
        self._2doubleSpinBox_order_random.setMinimum(0.01)
        self._2doubleSpinBox_order_random.setValue(0.1)
        self._2doubleSpinBox_order_random.setObjectName("_2doubleSpinBox_order_random")
        self._2doubleSpinBox_order_random.setSingleStep(0.05)
        self._2doubleSpinBox_order_random.setStyleSheet(style_Double)
        self._2doubleSpinBox_order_random.setEnabled(False)

        # self.order_pushButton = QtWidgets.QPushButton(self.page_2)
        self.order_pushButton = oo.NormolAnimatedButton(self.page_2)
        self.order_pushButton.setGeometry(QtCore.QRect(240, 550, 280, 25))
        self.order_pushButton.setObjectName("order_pushButton")
        self.order_pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.order_pushButton.setText("开始发送")
        self.order_pushButton.setFont(style_font_10)

    def label_page3(self):
        custom_widget9 = ui.style.CustomWidget(self.page_3)  # 创建队伍
        custom_widget9.setGeometry(QtCore.QRect(0, 0, 350, 160))
        custom_widget9.lower()

        custom_widget10 = ui.style.CustomWidget(self.page_3)  # 加入队伍
        custom_widget10.setGeometry(QtCore.QRect(345, 0, 395, 160))
        custom_widget10.lower()

        custom_widget11 = ui.style.CustomWidget(self.page_3)  # 交互队伍框
        custom_widget11.setGeometry(QtCore.QRect(0, 155, 740, 445))
        custom_widget11.lower()

        self.create_team_label = QtWidgets.QLabel(self.page_3)
        self.create_team_label.setGeometry(QtCore.QRect(30, 20, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.create_team_label.setFont(font)
        self.create_team_label.setObjectName("create_team_label")
        self.create_team_label.setText("创建队伍")

        self.create_team_button = QtWidgets.QToolButton(self.page_3)
        self.create_team_button.setGeometry(QtCore.QRect(45, 100, 260, 31))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(12)
        self.create_team_button.setFont(font)
        self.create_team_button.setObjectName("create_team_button")
        self.create_team_button.setText("点击创建队伍")
        self.create_team_button.setStyleSheet(style_white_blue_toolbutton)

        self.add_team_label_prompt_right = QtWidgets.QLabel(self.page_3)
        self.add_team_label_prompt_right.setGeometry(QtCore.QRect(100, 70, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.add_team_label_prompt_right.setFont(font)
        self.add_team_label_prompt_right.setObjectName("add_team_label_prompt_right")
        self.add_team_label_prompt_right.setText("队伍已加入！")
        self.add_team_label_prompt_right.setVisible(False)

        self.random_id_Label = QtWidgets.QLabel(self.page_3)
        self.random_id_Label.setGeometry(QtCore.QRect(20, 60, 325, 31))
        self.random_id_Label.setFont(style_font_11)
        self.random_id_Label.setObjectName("_4label")
        self.random_id_Label.setText("队伍ID为:")
        self.random_id_Label.setVisible(False)

        self.add_team_label = QtWidgets.QLabel(self.page_3)
        self.add_team_label.setGeometry(QtCore.QRect(370, 10, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.add_team_label.setFont(font)
        self.add_team_label.setObjectName("add_team_label")
        self.add_team_label.setText("加入队伍")

        self.add_team_label_prompt = QtWidgets.QLabel(self.page_3)
        self.add_team_label_prompt.setGeometry(QtCore.QRect(460, 70, 150, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.add_team_label_prompt.setFont(font)
        self.add_team_label_prompt.setObjectName("add_team_label_prompt")
        self.add_team_label_prompt.setText("队伍已加入")
        self.add_team_label_prompt.setVisible(False)

        self.create_team_label_prompt = QtWidgets.QLabel(self.page_3)
        self.create_team_label_prompt.setGeometry(QtCore.QRect(460, 70, 150, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.create_team_label_prompt.setFont(font)
        self.create_team_label_prompt.setObjectName("create_team_label_prompt")
        self.create_team_label_prompt.setText("队伍已创建!")
        self.create_team_label_prompt.setVisible(False)

        self.add_team_lineEdit = QtWidgets.QLineEdit(self.page_3)
        self.add_team_lineEdit.setGeometry(QtCore.QRect(430, 60, 280, 20))
        self.add_team_lineEdit.setObjectName("add_team_lineEdit")
        self.add_team_lineEdit.setStyleSheet(style_lineEdit)
        self.add_team_lineEdit.setPlaceholderText("输入队伍ID")
        self.add_team_lineEdit.setFont(style_font_10)

        self.add_team_ID = QtWidgets.QLabel(self.page_3)
        self.add_team_ID.setGeometry(QtCore.QRect(370, 60, 71, 16))
        self.add_team_ID.setFont(style_font_11)
        self.add_team_ID.setObjectName("add_team_ID")
        self.add_team_ID.setText("队伍ID:")

        self.add_team_button = QtWidgets.QToolButton(self.page_3)
        self.add_team_button.setGeometry(QtCore.QRect(370, 100, 340, 30))
        self.add_team_button.setObjectName("add_team_button")
        self.add_team_button.setText("加入")
        self.add_team_button.setFont(style_font_12)
        self.add_team_button.setStyleSheet(style_white_blue_toolbutton)

        self.button_copy_id = QtWidgets.QToolButton(self.page_3)
        self.button_copy_id.setGeometry(QtCore.QRect(45, 100, 260, 31))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(12)
        self.button_copy_id.setFont(font)
        self.button_copy_id.setObjectName("button_copy_id")
        self.button_copy_id.setText("点击复制ID")
        self.button_copy_id.setVisible(False)
        self.button_copy_id.setStyleSheet("""QToolButton {
                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                background-color: transparent;    /* 设置透明背景 */
                                                border-radius: 2px;    /* 设置圆角 */
                                            }
                                            QToolButton:hover {
                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                            }""")


        self.user1_image = QtWidgets.QToolButton(self.page_3)
        self.user1_image.setGeometry(QtCore.QRect(20, 180, 140, 140))
        global HImage_load_status

        if HImage_load_status == True:  # 判断头像是否成功加载
            icon = QtGui.QIcon("./temp/HImage.png")  # 将此处的路径替换为实际的图像路径
        else:
            icon = QtGui.QIcon("./image/float/fc.png")
        scaled_icon = icon.pixmap(QtCore.QSize(140, 140)).scaled(QtCore.QSize(140, 140),
                                                                 QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                                                                 QtCore.Qt.TransformationMode.SmoothTransformation)
        self.user1_image.setIcon(QtGui.QIcon(scaled_icon))
        self.user1_image.setIconSize(QSize(140, 140))
        self.user1_image.setObjectName("user1_image")
        self.user1_image.setStyleSheet(
            "QToolButton { background: transparent; padding: 0;border: none; }")

        self.user1_name = QtWidgets.QLabel(self.page_3)
        self.user1_name.setGeometry(QtCore.QRect(170, 210, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.user1_name.setFont(font)
        self.user1_name.setObjectName("label_5")
        self.user1_name.setText(f"{Name}[我]")

        self.user1_id = QtWidgets.QLabel(self.page_3)
        self.user1_id.setGeometry(QtCore.QRect(170, 240, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.user1_id.setFont(font)  # 一号id
        self.user1_id.setObjectName("label_7")
        self.user1_id.setText(f"ID:{Account}")

        self.user2_image = QtWidgets.QToolButton(self.page_3)
        self.user2_image.setGeometry(QtCore.QRect(360, 180, 140, 140))
        icon = QtGui.QIcon("./image/other_user.png")  # 将此处的路径替换为实际的图像路径
        scaled_icon = icon.pixmap(QtCore.QSize(140, 140)).scaled(QtCore.QSize(140, 140),
                                                                 QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                                                                 QtCore.Qt.TransformationMode.SmoothTransformation)
        self.user2_image.setIcon(QtGui.QIcon(scaled_icon))
        self.user2_image.setIconSize(QtCore.QSize(140, 140))
        self.user2_image.setObjectName("user2_image")
        #self.user2_image.setStyleSheet("QToolButton { background: transparent; padding: 0;border: none; }")

        self.user2_name = QtWidgets.QLabel(self.page_3)
        self.user2_name.setGeometry(QtCore.QRect(520, 210, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.user2_name.setFont(font)
        self.user2_name.setObjectName("label_6")
        self.user2_name.setText("等待用户加入")
        
        self.user2_id = QtWidgets.QLabel(self.page_3)
        self.user2_id.setGeometry(QtCore.QRect(520, 240, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.user2_id.setFont(font)
        self.user2_id.setObjectName("label_8")
        self.user2_id.setText("ID:")


        self.team_send_handle = QtWidgets.QRadioButton(self.page_3)
        self.team_send_handle.setGeometry(QtCore.QRect(20, 330, 131, 20))
        self.team_send_handle.setObjectName("team_send_handle")
        self.team_send_handle.setText("句柄式发送消息")
        self.team_send_handle.setChecked(True)
        self.team_send_handle.setStyleSheet(style_Radio)
        self.team_send_atqq = QtWidgets.QRadioButton(self.page_3)
        self.team_send_atqq.setGeometry(QtCore.QRect(20, 360, 89, 20))
        self.team_send_atqq.setObjectName("team_send_atqq")
        self.team_send_atqq.setText("@QQ")
        self.team_send_atqq.setStyleSheet(style_Radio)
        self.team_send_copy = QtWidgets.QRadioButton(self.page_3)
        self.team_send_copy.setGeometry(QtCore.QRect(20, 390, 89, 20))
        self.team_send_copy.setObjectName("team_send_copy")
        self.team_send_copy.setText("复制消息")
        self.team_send_copy.setStyleSheet(style_Radio)
        self.team_send_renew = QtWidgets.QRadioButton(self.page_3)
        self.team_send_renew.setGeometry(QtCore.QRect(20, 420, 89, 20))
        self.team_send_renew.setObjectName("team_send_renew")
        self.team_send_renew.setText("QQ个人信息更新")
        self.team_send_renew.setStyleSheet(style_Radio)
        self.team_send_exe = QtWidgets.QRadioButton(self.page_3)
        self.team_send_exe.setGeometry(QtCore.QRect(20, 450, 100, 20))
        self.team_send_exe.setObjectName("team_send_exe")
        self.team_send_exe.setText("执行自动脚本")
        self.team_send_exe.setStyleSheet(style_Radio)
        self.buttonGroup2 = QtWidgets.QButtonGroup(self.page_3)
        self.buttonGroup2.addButton(self.team_send_handle)
        self.buttonGroup2.addButton(self.team_send_atqq)
        self.buttonGroup2.addButton(self.team_send_copy)
        self.buttonGroup2.addButton(self.team_send_renew)
        self.buttonGroup2.addButton(self.team_send_exe)

        self.team_send_handle_c = QtWidgets.QRadioButton(self.page_3)
        self.team_send_handle_c.setGeometry(QtCore.QRect(370, 330, 121, 20))
        self.team_send_handle_c.setObjectName("team_send_handle_c")
        self.team_send_handle_c.setText("句柄式发送消息")
        self.team_send_handle_c.setChecked(True)
        self.team_send_handle_c.setStyleSheet(style_Radio)
        self.team_send_atqq_c = QtWidgets.QRadioButton(self.page_3)
        self.team_send_atqq_c.setGeometry(QtCore.QRect(370, 360, 89, 20))
        self.team_send_atqq_c.setObjectName("team_send_atqq_c")
        self.team_send_atqq_c.setText("@QQ")
        self.team_send_atqq_c.setStyleSheet(style_Radio)
        self.team_send_copy_c = QtWidgets.QRadioButton(self.page_3)
        self.team_send_copy_c.setGeometry(QtCore.QRect(370, 390, 89, 20))
        self.team_send_copy_c.setObjectName("team_send_copy_c")
        self.team_send_copy_c.setText("复制消息")
        self.team_send_copy_c.setStyleSheet(style_Radio)
        self.team_send_renew_c = QtWidgets.QRadioButton(self.page_3)
        self.team_send_renew_c.setGeometry(QtCore.QRect(370, 420, 89, 20))
        self.team_send_renew_c.setObjectName("team_send_renew_c")
        self.team_send_renew_c.setText("QQ个人信息更新")
        self.team_send_renew_c.setStyleSheet(style_Radio)
        self.team_send_exe_c = QtWidgets.QRadioButton(self.page_3)
        self.team_send_exe_c.setGeometry(QtCore.QRect(370, 450, 100, 20))
        self.team_send_exe_c.setObjectName("team_send_exe_c")
        self.team_send_exe_c.setText("执行自动脚本")
        self.team_send_exe_c.setStyleSheet(style_Radio)
        self.buttonGroup3 = QtWidgets.QButtonGroup(self.page_3)
        self.buttonGroup3.addButton(self.team_send_handle_c)
        self.buttonGroup3.addButton(self.team_send_atqq_c)
        self.buttonGroup3.addButton(self.team_send_copy_c)
        self.buttonGroup3.addButton(self.team_send_renew_c)
        self.buttonGroup3.addButton(self.team_send_exe_c)
        self.run_execute = QtWidgets.QToolButton(self.page_3)
        self.run_execute.setGeometry(QtCore.QRect(500, 510, 161, 51))
        self.run_execute.setObjectName("toolButton_3")
        self.run_execute.setText("开始执行")
        self.run_execute.setFont(style_font_12)
        self.run_execute.setStyleSheet("""QToolButton {
                                                          border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                          background-color: transparent;    /* 设置透明背景 */
                                                          border-radius: 2px;    /* 设置圆角 */
                                                          }
                                        QToolButton:hover {
                                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                            }""")
        self.run_execute.setVisible(False)

        self.talk_textBrowser = QtWidgets.QTextBrowser(self.page_3)#480 340
        self.talk_textBrowser.setGeometry(QtCore.QRect(20, 480, 240, 80))
        self.talk_textBrowser.setObjectName("talk_textBrowser")
        self.talk_textBrowser.setStyleSheet(ui.style.style_textEdit)

        font = QFont("等线", 12)
        self.talk_textBrowser.setFont(font)
        self.talk_textBrowser.setVisible(False)

        self.talk_lineEdit = QtWidgets.QLineEdit(self.page_3)
        self.talk_lineEdit.setGeometry(QtCore.QRect(20, 560, 240, 20))
        self.talk_lineEdit.setObjectName("talk_lineEdit")
        self.talk_lineEdit.setStyleSheet(style_lineEdit)
        self.talk_lineEdit.setPlaceholderText("说点什么....")
        self.talk_lineEdit.setFont(style_font_10)
        self.talk_lineEdit.setVisible(False)

        self.wait_label = QtWidgets.QLabel(self.page_3)
        self.wait_label.setGeometry(QtCore.QRect(20, 450, 240, 20))
        self.wait_label.setObjectName("wait_label")
        self.wait_label.setText("等待队长开始发送")
        self.wait_label.setFont(ui.style.style_font_black_16)
        self.wait_label.setVisible(False)
        pass

        for button in self.buttonGroup2.buttons():
            button.setVisible(False)
        for button in self.buttonGroup3.buttons():
            button.setVisible(False)
        pass

    def label_page4(self):
        custom_widget12 = ui.style.CustomWidget(self.page_4)  # 网易云音乐下载框
        custom_widget12.setGeometry(QtCore.QRect(0, 0, 300, 245))
        custom_widget12.lower()

        custom_widget13 = ui.style.CustomWidget(self.page_4)  # 网易云下框  作用:???未知
        custom_widget13.setGeometry(QtCore.QRect(0, 240, 300, 360))
        custom_widget13.lower()

        custom_widget14 = ui.style.CustomWidget(self.page_4)  # 图片格式转换框
        custom_widget14.setGeometry(QtCore.QRect(295, 0, 445, 245))
        custom_widget14.lower()

        custom_widget15 = ui.style.CustomWidget(self.page_4)  # 其他工具框
        custom_widget15.setGeometry(QtCore.QRect(295, 240, 445, 360))
        custom_widget15.lower()

        title_font = QtGui.QFont()
        title_font.setFamily("Arial")
        title_font.setPointSize(18)

        self._5label = QtWidgets.QLabel(self.page_4)
        self._5label.setGeometry(QtCore.QRect(10, 10, 180, 31))
        self._5label.setFont(title_font)
        self._5label.setObjectName("_5label")
        self._5label.setText("下载网易云音乐")

        self._5label_2 = QtWidgets.QLabel(self.page_4)
        self._5label_2.setGeometry(QtCore.QRect(15, 50, 80, 16))
        self._5label_2.setFont(style_font_10)
        self._5label_2.setObjectName("_5label_2")
        self._5label_2.setText("歌曲链接")

        self._5lineEdit = CustomLineEdit(self, self.page_4)  # 将当前的 Ui_FormS 实例传递进去
        self._5lineEdit.setGeometry(QtCore.QRect(15, 70, 271, 20))
        self._5lineEdit.setObjectName("_5lineEdit")
        self._5lineEdit.setStyleSheet(style_lineEdit)
        self._5lineEdit.setPlaceholderText("点击输入音乐链接(Ctrl+V粘贴可快速解析文件名)")
        self._5lineEdit.setFont(style_font_9)
        self._5lineEdit.setReadOnly(False)

        self._5label_3 = QtWidgets.QLabel(self.page_4)
        self._5label_3.setGeometry(QtCore.QRect(15, 100, 80, 16))
        self._5label_3.setFont(style_font_10)
        self._5label_3.setObjectName("_5label_3")
        self._5label_3.setText("保存文件名")

        self._5lineEdit2 = QtWidgets.QLineEdit(self.page_4)
        self._5lineEdit2.setGeometry(QtCore.QRect(15, 120, 271, 20))
        self._5lineEdit2.setObjectName("_5lineEdit2")
        self._5lineEdit2.setStyleSheet(style_lineEdit)
        self._5lineEdit2.setPlaceholderText("点击输入保存文件名(包含扩展名)")
        self._5lineEdit2.setFont(style_font_9)
        self._5lineEdit2.setReadOnly(False)

        self._5label_4 = QtWidgets.QLabel(self.page_4)
        self._5label_4.setGeometry(QtCore.QRect(15, 150, 81, 16))
        self._5label_4.setFont(style_font_10)
        self._5label_4.setObjectName("_5label_4")
        self._5label_4.setText("保存路径")

        self._5lineEdit3 = QtWidgets.QLineEdit(self.page_4)
        self._5lineEdit3.setGeometry(QtCore.QRect(15, 170, 271, 20))
        self._5lineEdit3.setObjectName("_5lineEdit3")
        self._5lineEdit3.setStyleSheet(style_lineEdit)
        self._5lineEdit3.setText(os.getcwd() + '\\mod\\music')
        self._5lineEdit3.setFont(style_font_9)

        # self._5toolButton = QtWidgets.QToolButton(self.page_4)
        self._5toolButton = oo.NormolAnimatedButton(self.page_4)
        self._5toolButton.setGeometry(QtCore.QRect(15, 200, 271, 31))
        self._5toolButton.setObjectName("_5toolButton")
        self._5toolButton.setText("下载")
        self._5toolButton.setCursor(QCursor(Qt.PointingHandCursor))
        self._5toolButton.setFont(style_font_11)

        self._5toolButton2 = QtWidgets.QToolButton(self.page_4)
        self._5toolButton2.setGeometry(QtCore.QRect(250, 150, 37, 18))
        self._5toolButton2.setObjectName("_5toolButton2")
        self._5toolButton2.setText("选择")
        self._5toolButton2.setFont(style_font_10)
        self._5toolButton2.setStyleSheet("""
            QToolButton {
                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                background-color: transparent;    /* 设置透明背景 */
                border-radius: 2px;    /* 设置圆角 */
            }
            QToolButton:hover {
                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
            }
        """)

        self.view_music = QtWidgets.QToolButton(self.page_4)
        self.view_music.setGeometry(QtCore.QRect(200, 150, 37, 18))
        self.view_music.setObjectName("view_music")
        self.view_music.setText("浏览")
        self.view_music.setFont(style_font_10)
        self.view_music.setStyleSheet("""
            QToolButton {
                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                background-color: transparent;    /* 设置透明背景 */
                border-radius: 2px;    /* 设置圆角 */
            }
            QToolButton:hover {
                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
            }
        """)

        self._5label5 = QtWidgets.QLabel(self.page_4)
        self._5label5.setGeometry(QtCore.QRect(305, 10, 180, 31))
        self._5label5.setFont(title_font)
        self._5label5.setObjectName("_5label5")
        self._5label5.setText("文件格式转换")

        self._5label6 = QtWidgets.QLabel(self.page_4)
        self._5label6.setGeometry(QtCore.QRect(305, 50, 80, 16))
        self._5label6.setFont(style_font_10)
        self._5label6.setObjectName("_5label6")
        self._5label6.setText("图片路径")

        #self._5lineEdit4 = QtWidgets.QLineEdit(self.page_4)  # 输入图片栏
        self._5lineEdit4 = ui.style.DraggableLineEdit('picture', self.page_4)  # 输入图片栏
        self._5lineEdit4.setGeometry(QtCore.QRect(305, 70, 370, 20))
        self._5lineEdit4.setObjectName("_5lineEdit4")
        self._5lineEdit4.setStyleSheet(style_lineEdit)
        self._5lineEdit4.setPlaceholderText("选择或拖拽文件到此处")
        self._5lineEdit4.setFont(style_font_9)

        self._5label7 = QtWidgets.QLabel(self.page_4)
        self._5label7.setGeometry(QtCore.QRect(305, 100, 100, 16))
        self._5label7.setFont(style_font_10)
        self._5label7.setObjectName("_5label7")
        self._5label7.setText("输出文件夹路径")

        self._5lineEdit5 = QtWidgets.QLineEdit(self.page_4)  # 酷狗保存文件名
        self._5lineEdit5.setGeometry(QtCore.QRect(305, 120, 370, 20))
        self._5lineEdit5.setObjectName("_5lineEdit5")
        self._5lineEdit5.setStyleSheet(style_lineEdit)
        self._5lineEdit5.setPlaceholderText("点击输入图片输出路径")
        self._5lineEdit5.setFont(style_font_9)

        self._5toolButton3 = QtWidgets.QToolButton(self.page_4)  # 输入图片路径
        self._5toolButton3.setGeometry(QtCore.QRect(680, 70, 51, 21))
        self._5toolButton3.setObjectName("_5toolButton3")
        self._5toolButton3.setText("选择")
        self._5toolButton3.setFont(style_font_10)
        self._5toolButton3.setStyleSheet("""
                                                                                    QToolButton {
                                                                                        border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                        background-color: transparent;    /* 设置透明背景 */
                                                                                        border-radius: 2px;    /* 设置圆角 */
                                                                                    }
                                                                                    QToolButton:hover {
                                                                                        background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                        border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                    }
                                                                                """)

        self._5toolButton4 = QtWidgets.QToolButton(self.page_4)  # 输出文件夹路径
        self._5toolButton4.setGeometry(QtCore.QRect(680, 120, 51, 21))
        self._5toolButton4.setObjectName("_5toolButton4")
        self._5toolButton4.setText("选择")
        self._5toolButton4.setFont(style_font_10)
        self._5toolButton4.setStyleSheet("""
                                                                                    QToolButton {
                                                                                        border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                        background-color: transparent;    /* 设置透明背景 */
                                                                                        border-radius: 2px;    /* 设置圆角 */
                                                                                    }
                                                                                    QToolButton:hover {
                                                                                        background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                        border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                    }
                                                                                """)
        self.groupPic = QtWidgets.QButtonGroup(self.centralwidget)
        self.JPG_radioButton = QtWidgets.QRadioButton(self.page_4)
        self.JPG_radioButton.setGeometry(QtCore.QRect(305, 160, 61, 18))
        self.JPG_radioButton.setObjectName("JPG_radioButton")
        self.JPG_radioButton.setText("JPG")
        self.JPG_radioButton.setChecked(True)
        self.JPG_radioButton.setStyleSheet(style_Radio)
        self.PNG_radioButton = QtWidgets.QRadioButton(self.page_4)
        self.PNG_radioButton.setGeometry(QtCore.QRect(380, 160, 61, 18))
        self.PNG_radioButton.setObjectName("PNG_radioButton")
        self.PNG_radioButton.setText("PNG")
        self.PNG_radioButton.setStyleSheet(style_Radio)
        self.GIF_radioButton = QtWidgets.QRadioButton(self.page_4)
        self.GIF_radioButton.setGeometry(QtCore.QRect(450, 160, 61, 18))
        self.GIF_radioButton.setObjectName("GIF_radioButton")
        self.GIF_radioButton.setText("GIF")
        self.GIF_radioButton.setStyleSheet(style_Radio)
        self.groupPic.addButton(self.JPG_radioButton)
        self.groupPic.addButton(self.PNG_radioButton)
        self.groupPic.addButton(self.GIF_radioButton)

        # self._5toolButton5 = QtWidgets.QToolButton(self.page_4)
        self._5toolButton5 = oo.NormolAnimatedButton(self.page_4)
        self._5toolButton5.setGeometry(QtCore.QRect(310, 200, 200, 31))
        self._5toolButton5.setObjectName("_5toolButton5")
        self._5toolButton5.setText("输出")
        self._5toolButton5.setFont(style_font_11)
        self._5toolButton5.setCursor(QCursor(Qt.PointingHandCursor))

        self.QQ_label = QtWidgets.QLabel(self.page_4)
        self.QQ_label.setGeometry(QtCore.QRect(20, 250, 180, 31))
        self.QQ_label.setFont(title_font)
        self.QQ_label.setObjectName("QQ_label")
        self.QQ_label.setText("QQ信息")

        self.QQ_label_t2 = QtWidgets.QLabel(self.page_4)
        self.QQ_label_t2.setGeometry(QtCore.QRect(20, 280, 180, 31))
        self.QQ_label_t2.setFont(style_font_10)
        self.QQ_label_t2.setObjectName("QQ_label_t2")
        self.QQ_label_t2.setText("随机下载QQ头像")

        self.QQ_label_t3 = QtWidgets.QLabel(self.page_4)
        self.QQ_label_t3.setGeometry(QtCore.QRect(120, 283, 26, 22))
        self.QQ_label_t3.setFont(style_font_11)
        self.QQ_label_t3.setObjectName("QQ_label_t3")
        self.QQ_label_t3.setStyleSheet(
            "color: GREEN;border-radius: 3px;")
        self.QQ_label_t3.setText("Lv2")

        self.QQ_spinBox = QtWidgets.QSpinBox(self.page_4)  # QQ图像下载次数
        self.QQ_spinBox.setGeometry(QtCore.QRect(20, 310, 90, 20))
        self.QQ_spinBox.setMinimum(1)
        self.QQ_spinBox.setValue(10)
        self.QQ_spinBox.setMaximum(9999)
        self.QQ_spinBox.setStyleSheet("background: transparent;")
        self.QQ_spinBox.setObjectName("QQ_spinBox")
        self.QQ_spinBox.setStyleSheet(style_Spin)

        self.QQ_Button_Dow = oo.AnimatedButton(self.page_4)
        self.QQ_Button_Dow.setGeometry(QtCore.QRect(120, 310, 80, 20))
        self.QQ_Button_Dow.setObjectName("QQ_Button_Dow")
        self.QQ_Button_Dow.setText("开始下载")
        self.QQ_Button_Dow.setFont(style_font_10)

        self.open_QQ = QPushButton('浏览图片文件夹', self.page_4)

        self.open_QQ.setGeometry(20, 360, 130, 20)
        self.open_QQ.setFont(style_font_10)
        self.open_QQ.setStyleSheet("""
                                                                                    QPushButton {
                                                                                        border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                        background-color: transparent;    /* 设置透明背景 */
                                                                                        border-radius: 2px;    /* 设置圆角 */
                                                                                    }
                                                                                    QPushButton:hover {
                                                                                        background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                        border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                    }
                                                                                """)

        # self.delete_image = QPushButton('一键清空文件夹', self.page_4)
        self.delete_image = oo.MoreAnimatedButton(self.page_4, radius=2, start_color=QColor(207, 207, 207),
                                                  hover_color=QColor(172, 172, 172))
        self.delete_image.setGeometry(150, 360, 130, 20)
        self.delete_image.setText("一键清空文件夹")
        self.delete_image.setFont(style_font_10)

        self.QQ_label_t3 = QtWidgets.QLabel(self.page_4)
        self.QQ_label_t3.setGeometry(QtCore.QRect(20, 330, 100, 31))
        self.QQ_label_t3.setFont(style_font_10)
        self.QQ_label_t3.setObjectName("QQ_label_t3")
        self.QQ_label_t3.setText("总下载次数:0次")

        self.QQ_label_t6 = QtWidgets.QLabel(self.page_4)
        self.QQ_label_t6.setGeometry(QtCore.QRect(120, 330, 100, 31))
        self.QQ_label_t6.setFont(style_font_10)
        self.QQ_label_t6.setObjectName("QQ_label_t6")
        self.QQ_label_t6.setText("有效次数:0次")

        self.QQ_label_t4 = QtWidgets.QLabel(self.page_4)
        self.QQ_label_t4.setGeometry(QtCore.QRect(20, 400, 180, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.QQ_label_t4.setFont(font)
        self.QQ_label_t4.setObjectName("QQ_label_t4")
        self.QQ_label_t4.setText("一键更换QQ资料")

        self.pushButton_tooltip_imformation = QtWidgets.QPushButton(self.page_4)
        self.pushButton_tooltip_imformation.setGeometry(QtCore.QRect(180, 405, 24, 24))
        self.pushButton_tooltip_imformation.setStyleSheet("QPushButton {"
                                                          "    border-image: url(./image/Component/提示3.png);"
                                                          "    background-color: rgba(245,245,245,0);"
                                                          "}")
        self.pushButton_tooltip_imformation.setToolTip(
            "此功能的作用是依次按顺序点击QQ更新用户资料的控件来实现更新资料的效果\n如无需要此功能请勿随意使用")

        self.QQ_label_t5 = QtWidgets.QLabel(self.page_4)
        self.QQ_label_t5.setGeometry(QtCore.QRect(20, 440, 180, 20))
        self.QQ_label_t5.setFont(style_font_10)
        self.QQ_label_t5.setObjectName("QQ_label_t5")
        self.QQ_label_t5.setText("设置点击间隔时间 次\\秒")

        self.QQ_Doxb = QtWidgets.QDoubleSpinBox(self.page_4)
        self.QQ_Doxb.setGeometry(QtCore.QRect(170, 440, 60, 20))
        self.QQ_Doxb.setMinimum(0.1)
        self.QQ_Doxb.setValue(0.3)
        self.QQ_Doxb.setSingleStep(0.1)
        self.QQ_Doxb.setMaximum(1)
        self.QQ_Doxb.setObjectName("QQ_Doxb")
        self.QQ_Doxb.setStyleSheet(style_Double)

        self.QQ_image = oo.NormolAnimatedButton(self.page_4)
        self.QQ_image.setGeometry(QtCore.QRect(20, 500, 260, 30))
        self.QQ_image.setObjectName("QQ_image")
        self.QQ_image.setText("更换")
        self.QQ_image.setFont(style_font_11)

        self.QQ_GLabel = QtWidgets.QLabel(self.page_4)
        self.QQ_GLabel.setGeometry(QtCore.QRect(310, 245, 200, 40))
        self.QQ_GLabel.setFont(title_font)
        self.QQ_GLabel.setObjectName("QQ_GLabel")
        self.QQ_GLabel.setText("QQ群信息获取")

        self.QQ_GLabel2 = QtWidgets.QLabel(self.page_4)
        self.QQ_GLabel2.setGeometry(QtCore.QRect(310, 300, 100, 16))
        self.QQ_GLabel2.setFont(style_font_10)
        self.QQ_GLabel2.setObjectName("QQ_GLabel2")
        self.QQ_GLabel2.setText("输出文件夹路径:")

        self.groupQQ = QtWidgets.QButtonGroup(self.centralwidget)

        self.QQ_Group_Save = QtWidgets.QLineEdit(self.page_4)  # QQ群信息保存路径
        self.QQ_Group_Save.setGeometry(QtCore.QRect(310, 330, 310, 20))
        self.QQ_Group_Save.setObjectName("QQ_Group_Save")
        self.QQ_Group_Save.setStyleSheet(style_lineEdit)
        self.QQ_Group_Save.setPlaceholderText("点击输入xlsx文件夹路径")
        self.QQ_Group_Save.setText(os.getcwd() + '\\mod\\xlsx')
        self.QQ_Group_Save.setFont(style_font_9)

        self.QQ_Group_Selec = QtWidgets.QToolButton(self.page_4)  # 输出文件夹路径
        self.QQ_Group_Selec.setGeometry(QtCore.QRect(625, 330, 51, 21))
        self.QQ_Group_Selec.setObjectName("QQ_Group_Selec")
        self.QQ_Group_Selec.setText("选择")
        self.QQ_Group_Selec.setFont(style_font_10)
        self.QQ_Group_Selec.setStyleSheet("""
                                                                                                                        QToolButton {
                                                                                                                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                            background-color: transparent;    /* 设置透明背景 */
                                                                                                                            border-radius: 2px;    /* 设置圆角 */
                                                                                                                        }
                                                                                                                        QToolButton:hover {
                                                                                                                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                                        }
                                                                                                                    """)

        self.QQ_Group_View = QtWidgets.QToolButton(self.page_4)  # 输出文件夹路径
        self.QQ_Group_View.setGeometry(QtCore.QRect(680, 330, 51, 21))
        self.QQ_Group_View.setObjectName("QQ_Group_View")
        self.QQ_Group_View.setText("浏览")
        self.QQ_Group_View.setFont(style_font_10)
        self.QQ_Group_View.setStyleSheet("""
                                                                                                                        QToolButton {
                                                                                                                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                            background-color: transparent;    /* 设置透明背景 */
                                                                                                                            border-radius: 2px;    /* 设置圆角 */
                                                                                                                        }
                                                                                                                        QToolButton:hover {
                                                                                                                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                                        }
                                                                                                                    """)

        self.Edge = QtWidgets.QRadioButton(self.page_4)
        self.Edge.setGeometry(QtCore.QRect(310, 360, 505, 18))
        self.Edge.setObjectName("Edge")
        self.Edge.setChecked(True)
        self.Edge.setText("Edge")
        self.Edge.setStyleSheet(style_Radio)

        self.Chrome = QtWidgets.QRadioButton(self.page_4)
        self.Chrome.setGeometry(QtCore.QRect(380, 360, 70, 18))
        self.Chrome.setObjectName("Chrome")
        self.Chrome.setText("Chrome")
        self.Chrome.setStyleSheet(style_Radio)

        self.IE = QtWidgets.QRadioButton(self.page_4)
        self.IE.setGeometry(QtCore.QRect(460, 360, 50, 18))
        self.IE.setObjectName("IE")
        self.IE.setText("IE")
        self.IE.setStyleSheet(style_Radio)

        self.groupQQ.addButton(self.Edge)
        self.groupQQ.addButton(self.Chrome)
        self.groupQQ.addButton(self.IE)

        self.Content_Label = QtWidgets.QLabel(self.page_4)
        self.Content_Label.setGeometry(QtCore.QRect(310, 390, 100, 16))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(11)
        self.Content_Label.setFont(font)
        self.Content_Label.setObjectName("Content_Label")
        self.Content_Label.setText("内容选择:")

        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(11)
        self.checkBox_gender = QtWidgets.QCheckBox(self.page_4)
        self.checkBox_gender.setGeometry(QtCore.QRect(310, 420, 80, 20))
        self.checkBox_gender.setFont(font)
        self.checkBox_gender.setObjectName("checkBox_gender")
        self.checkBox_gender.setText("序号")
        self.checkBox_gender.setChecked(True)
        self.checkBox_gender.setEnabled(False)
        self.checkBox_gender.setStyleSheet(style_CheckBox)

        self.checkBox_name = QtWidgets.QCheckBox(self.page_4)
        self.checkBox_name.setGeometry(QtCore.QRect(390, 420, 80, 20))
        self.checkBox_name.setFont(font)
        self.checkBox_name.setObjectName("checkBox_name")
        self.checkBox_name.setText("名称")
        self.checkBox_name.setChecked(True)
        self.checkBox_name.setEnabled(False)
        self.checkBox_name.setStyleSheet(style_CheckBox)

        self.checkBox_group_name = QtWidgets.QCheckBox(self.page_4)
        self.checkBox_group_name.setGeometry(QtCore.QRect(480, 420, 80, 20))
        self.checkBox_group_name.setFont(font)
        self.checkBox_group_name.setObjectName("checkBox_group_name")
        self.checkBox_group_name.setText("群昵称")
        self.checkBox_group_name.setChecked(True)
        self.checkBox_group_name.setEnabled(False)
        self.checkBox_group_name.setStyleSheet(style_CheckBox)

        self.checkBox_qid = QtWidgets.QCheckBox(self.page_4)
        self.checkBox_qid.setGeometry(QtCore.QRect(570, 420, 80, 20))
        self.checkBox_qid.setFont(font)
        self.checkBox_qid.setObjectName("checkBox_qid")
        self.checkBox_qid.setText("QQ号")
        self.checkBox_qid.setChecked(True)
        self.checkBox_qid.setStyleSheet(style_CheckBox)

        self.checkBox_sex = QtWidgets.QCheckBox(self.page_4)
        self.checkBox_sex.setGeometry(QtCore.QRect(660, 420, 80, 20))
        self.checkBox_sex.setFont(font)
        self.checkBox_sex.setObjectName("checkBox_sex")
        self.checkBox_sex.setText("性别")
        self.checkBox_sex.setChecked(True)
        self.checkBox_sex.setStyleSheet(style_CheckBox)

        self.checkBox_qq_year = QtWidgets.QCheckBox(self.page_4)
        self.checkBox_qq_year.setGeometry(QtCore.QRect(310, 450, 80, 20))
        self.checkBox_qq_year.setFont(font)
        self.checkBox_qq_year.setObjectName("checkBox_qq_year")
        self.checkBox_qq_year.setText("QQ年龄")
        self.checkBox_qq_year.setChecked(True)
        self.checkBox_qq_year.setStyleSheet(style_CheckBox)

        self.checkBox_join_date = QtWidgets.QCheckBox(self.page_4)
        self.checkBox_join_date.setGeometry(QtCore.QRect(390, 450, 90, 20))
        self.checkBox_join_date.setFont(font)
        self.checkBox_join_date.setObjectName("checkBox_join_date")
        self.checkBox_join_date.setText("进群日期")
        self.checkBox_join_date.setChecked(True)
        self.checkBox_join_date.setStyleSheet(style_CheckBox)

        self.checkBox_send_date = QtWidgets.QCheckBox(self.page_4)
        self.checkBox_send_date.setGeometry(QtCore.QRect(480, 450, 120, 20))
        self.checkBox_send_date.setFont(font)
        self.checkBox_send_date.setObjectName("checkBox_send_date")
        self.checkBox_send_date.setText("最后发言日期")
        self.checkBox_send_date.setChecked(True)
        self.checkBox_send_date.setStyleSheet(style_CheckBox)

        self.checkBox_group_lv = QtWidgets.QCheckBox(self.page_4)
        self.checkBox_group_lv.setGeometry(QtCore.QRect(610, 450, 80, 20))
        self.checkBox_group_lv.setFont(font)
        self.checkBox_group_lv.setObjectName("checkBox_group_lv")
        self.checkBox_group_lv.setText("群等级")
        self.checkBox_group_lv.setChecked(True)
        self.checkBox_group_lv.setStyleSheet(style_CheckBox)

        self.QQ_group = oo.NormolAnimatedButton(self.page_4)
        self.QQ_group.setGeometry(QtCore.QRect(310, 500, 200, 30))
        self.QQ_group.setObjectName("QQ_group")
        self.QQ_group.setText("获取")
        self.QQ_group.setFont(style_font_11)

    def checkRadio(self):
        if self.team_send_handle.isChecked():
            captain = 'handle'
        elif self.team_send_atqq.isChecked():
            captain = 'qq'
        elif self.team_send_copy.isChecked():
            captain = 'copy'
        elif self.team_send_renew.isChecked():
            captain = 'renew'
        elif self.team_send_exe.isChecked():
            captain = 'execute'
        else:
            captain = 'error'

        if self.team_send_handle_c.isChecked():
            member = 'handle'
        elif self.team_send_atqq_c.isChecked():
            member = 'qq'
        elif self.team_send_copy_c.isChecked():
            member = 'copy'
        elif self.team_send_renew_c.isChecked():
            member = 'renew'
        elif self.team_send_exe_c.isChecked():
            member = 'execute'
        else:
            member = 'error'

        return captain, member

    def populateMenu(self, folder_path):
        # 清空现有菜单项并填充新的菜单项
        self.file_menu.clear()
        files = [f for f in os.listdir(folder_path) if
                 os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            # 如果文件夹为空，调用 updateButtonText("")
            self.updateButtonText("暂无配置文件 需要创建")
            self.button_file.setIcon(QIcon())
        else:
            self.updateButtonText("选择配置文件")
            self.button_file.setIcon(QIcon('./image/Component/箭头 下.png'))
            # 如果有文件，则为每个文件创建一个菜单项
            for file in files:
                action = self.file_menu.addAction(file)
                action.triggered.connect(lambda checked, f=file: self.updateButtonText(f))

    def showMenu(self):
        self.file_menu.exec_(
            self.button_file.mapToGlobal(QtCore.QPoint(0, self.button_file.height())))

    def updateButtonText(self, file_name):
        # 更新按钮文本
        self.button_file.setText(file_name)

    def generate_initial_filename(self):
        date_str = datetime.now().strftime("%Y-%m-%d")
        directory = './scripts/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        files = [f for f in os.listdir(directory) if
                 f.startswith(date_str) and f.endswith('.txt')]
        max_number = 0
        for file in files:
            parts = file.replace('.txt', '').split('-')
            if len(parts) == 4:
                try:
                    number = int(parts[3])
                    if number > max_number:
                        max_number = number
                except ValueError:
                    continue
        next_number = max_number + 1
        return f"{date_str}-{next_number:02d}.txt"

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    uis = Ui_FormS()
    uis.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())