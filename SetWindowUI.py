from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QIcon, QPixmap, QPalette, QBrush, QPainterPath
from PyQt5.QtWidgets import QFileDialog, QButtonGroup, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import ui.style
import json
import os
import pyautogui
import extend_install
from PIL import Image
import ui.buttons
from ui.style import style_lineEdit


style_CheckBox = ui.style.style_CheckBox
style_Radio = ui.style.style_Radio
style_Spin = ui.style.style_Spin
style_Double = ui.style.style_Double

style_font_11 = QtGui.QFont()
style_font_11.setFamily("等线")
style_font_11.setPointSize(11)

style_font_10 = QtGui.QFont()
style_font_10 .setFamily("等线")
style_font_10.setPointSize(10)

style_font_9 = QtGui.QFont()
style_font_9.setFamily("等线")
style_font_9.setPointSize(9)

style_font_black_10 = QtGui.QFont()
style_font_black_10.setFamily("黑体")
style_font_black_10.setPointSize(10)

style_font_black_9 = QtGui.QFont()
style_font_black_9.setFamily("黑体")
style_font_black_9.setPointSize(9)


class SetWindow(QtWidgets.QDialog):
    def __init__(self, lis):
        global windows, Log, Sound, ClosePrompt, ClsoeExecute, window_s, Theme ,transparent, FPS
        super().__init__()

        windows = lis[0]
        cv2_available = lis[1]
        Log = lis[2]
        Sound = lis[3]
        ClosePrompt = lis[4]
        CloseExecute = lis[5]
        window_s = lis[6]
        Theme = lis[7]
        transparent = lis[8]
        FPS = lis[9]


        x = windows.x() + 500 - 270
        y = windows.y() + 300 - 170
        self.setGeometry(x, y, 540, 340)
        self.setFixedSize(540, 340)
        icon = QIcon("./image/Component/提示.png")
        self.setWindowIcon(icon)
        self.border_width = 8
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # 设置 窗口无边框和背景透明


        self.Button_Close = ui.buttons.CloseButton(self)
        self.Button_Close.setGeometry(495, 15, 26, 26)
        self.Button_Close.setToolTip('关闭')
        self.Button_Close.setIcon(QIcon("./image/quit.png"))
        self.Button_Close.setIconSize(QtCore.QSize(24, 24))
        self.Button_Close.setObjectName("Button_Close")

        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)

        self.setWindowTitle("设置")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 20, 70, 20))
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.pushButton = ui.buttons.AnimatedButton(self)
        self.pushButton.setGeometry(QtCore.QRect(370, 292, 150, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("保存")

        self.check_autologin = QtWidgets.QCheckBox(self)
        self.check_autologin.setGeometry(QtCore.QRect(20, 50, 161, 20))
        self.check_autologin.setFont(font)
        self.check_autologin.setObjectName("check_autologin")
        self.check_autologin.setStyleSheet(style_CheckBox)

        if Log == True:
            self.check_autologin.setChecked(True)

        self.check_sound = QtWidgets.QCheckBox(self)
        self.check_sound.setGeometry(QtCore.QRect(20, 90, 160, 20))
        self.check_sound.setFont(font)
        self.check_sound.setObjectName("check_sound")
        self.check_sound.setStyleSheet(style_CheckBox)

        if Sound == True:
            self.check_sound.setChecked(True)

        self.check_closeprompt = QtWidgets.QCheckBox(self)
        self.check_closeprompt.setGeometry(QtCore.QRect(20, 130, 160, 20))
        self.check_closeprompt.setFont(font)
        self.check_closeprompt.setObjectName("checkBox_5")
        self.check_closeprompt.setStyleSheet(style_CheckBox)


        self.check_closeprompt.setText("关闭时提示操作")

        self.group_close = QButtonGroup(self)
        self.radioButton_close = QtWidgets.QRadioButton(self)
        self.radioButton_close.setGeometry(QtCore.QRect(22, 160, 160, 20))
        self.radioButton_close.setFont(style_font_10)
        self.radioButton_close.setObjectName("radioButton_close")
        if CloseExecute == "Close":
            self.radioButton_close.setChecked(True)
        self.radioButton_close.setText("关闭软件")

        self.radioButton_minisize = QtWidgets.QRadioButton(self)
        self.radioButton_minisize.setGeometry(QtCore.QRect(100, 160, 160, 20))
        self.radioButton_minisize.setFont(style_font_10)
        self.radioButton_minisize.setObjectName("radioButton_minisize")
        if CloseExecute == "Hide":
            self.radioButton_minisize.setChecked(True)
        self.radioButton_minisize.setText("最小化到托盘")

        self.check_closeprompt.stateChanged.connect(self.sync_checkbox)
        if ClosePrompt == True:
            self.check_closeprompt.setChecked(True)

        self.group_close.addButton(self.radioButton_close)
        self.group_close.addButton(self.radioButton_minisize)

        self.checkBox_start = QtWidgets.QCheckBox(self)
        self.checkBox_start.setGeometry(QtCore.QRect(20, 190, 160, 20))
        self.checkBox_start.setFont(font)
        self.checkBox_start.setObjectName("checkBox_start")
        self.checkBox_start.setText("开机自启动")
        self.checkBox_start.setStyleSheet(style_CheckBox)

        self.checkBox_float = QtWidgets.QCheckBox(self)
        self.checkBox_float.setGeometry(QtCore.QRect(20, 230, 160, 20))
        self.checkBox_float.setFont(font)
        self.checkBox_float.setObjectName("checkBox_5")
        self.checkBox_float.setText("开启悬浮窗")
        self.checkBox_float.setStyleSheet(style_CheckBox)

        self.group_theme = QButtonGroup(self)
        self.radioButton_white = QtWidgets.QRadioButton(self)
        self.radioButton_white.setGeometry(QtCore.QRect(240, 40, 89, 20))
        self.radioButton_white.setFont(font)
        self.radioButton_white.setObjectName("radioButton_white")
        self.radioButton_white.setStyleSheet(style_Radio)

        self.radioButton_custom = QtWidgets.QRadioButton(self)
        self.radioButton_custom.setGeometry(QtCore.QRect(240, 70, 160, 20))
        self.radioButton_custom.setFont(font)
        self.radioButton_custom.setObjectName("radioButton_custom")
        self.radioButton_custom.setStyleSheet(style_Radio)

        self.line_Custom = ui.style.DraggableLineEdit('setpic', self)  # 自定义图片背景输入栏
        self.line_Custom.setGeometry(QtCore.QRect(240, 95, 211, 20))
        self.line_Custom.setObjectName("line_Custom")
        self.line_Custom.setPlaceholderText("支持jpg png bmp gif格式图片")
        self.line_Custom.setStyleSheet(style_lineEdit)
        self.line_Custom.setFont(style_font_9)

        #self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2 = ui.buttons.CustomButton(self, radius=2, start_color=QColor(207, 207, 207, 0),
                                               hover_color=QColor(33, 150, 243, 255),
                                               border_color=QColor(33, 120, 255), border_width=1,
                                               font_color=QColor(0, 0, 0))
        self.pushButton_2.setGeometry(QtCore.QRect(460, 94, 51, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setFont(style_font_10)
        #self.pushButton_2.setStyleSheet(ui.style.style_white_blue_button)

        self.Slider_label = QtWidgets.QLabel(self)
        self.Slider_label.setGeometry(QtCore.QRect(240, 125, 80, 12))
        self.Slider_label.setObjectName("FPS_label")
        self.Slider_label.setText("背景不透明度:")
        self.Slider_label.setFont(style_font_10)

        self.slider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setMinimum(20)  # 下限
        self.slider.setMaximum(90)  # 上限
        self.slider.setValue(transparent)
        self.slider.setGeometry(QtCore.QRect(323, 125, 150, 15))
        self.slider.valueChanged[int].connect(self.onSliderChange)

        self.radioButton_trend = QtWidgets.QRadioButton(self)
        self.radioButton_trend.setGeometry(QtCore.QRect(240, 150, 111, 20))
        self.radioButton_trend.setFont(font)
        self.radioButton_trend.setObjectName("radioButton_trend")
        self.radioButton_trend.setStyleSheet(style_Radio)

        self.trand_problem = QtWidgets.QPushButton(self)
        self.trand_problem.setGeometry(QtCore.QRect(335, 152, 18, 18))
        if cv2_available == True:
            self.trand_problem.setStyleSheet("QPushButton {"
                                             "    border-image: url(./image/Component/提示.png);"
                                             "    background-color: rgba(245,245,245,0);"
                                             "}")
            self.trand_problem.clicked.connect(lambda: self.problem('problem'))
        else:
            self.trand_problem.setStyleSheet("QPushButton {"
                                             "    border-image: url(./image/Component/下载.png);"
                                             "    background-color: rgba(245,245,245,0);"
                                             "}")
            self.trand_problem.clicked.connect(lambda: self.problem('download'))

        self.line_Trend = ui.style.DraggableLineEdit('video', self)  # 动态视频输入栏
        self.line_Trend.setGeometry(QtCore.QRect(240, 175, 211, 20))
        self.line_Trend.setObjectName("line_Trend")
        self.line_Trend.setPlaceholderText("支持mp4 mov flv avi格式视频")
        self.line_Trend.setStyleSheet(style_lineEdit)
        self.line_Trend.setFont(style_font_9)

        #self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3 = ui.buttons.CustomButton(self, radius=2, start_color=QColor(207, 207, 207, 0),
                                                     hover_color=QColor(33, 150, 243, 255),
                                                     border_color=QColor(33, 120, 255), border_width=1,
                                                     font_color=QColor(0, 0, 0))
        self.pushButton_3.setGeometry(QtCore.QRect(460, 174, 51, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setFont(style_font_10)
        #self.pushButton_3.setStyleSheet(ui.style.style_white_blue_button)

        self.FPS_label = QtWidgets.QLabel(self)
        self.FPS_label.setGeometry(QtCore.QRect(240, 210, 130, 12))
        self.FPS_label.setObjectName("FPS_label")
        self.FPS_label.setText("动态主题刷新率/每秒:")
        self.FPS_label.setFont(style_font_10)

        self.FPS_spinBox = QtWidgets.QSpinBox(self)  # FPS
        self.FPS_spinBox.setGeometry(QtCore.QRect(370, 205, 60, 22))
        self.FPS_spinBox.setMaximum(9999)
        self.FPS_spinBox.setValue(FPS)
        self.FPS_spinBox.setObjectName("FPS_spinBox")
        self.FPS_spinBox.setStyleSheet(style_Spin)
        self.FPS_spinBox.setMinimum(1)
        self.FPS_spinBox.repaint()
        self.FPS_spinBox.setMaximum(60)
        if cv2_available == False:
            self.radioButton_trend.setEnabled(False)
            self.radioButton_trend.setToolTip("需要安装扩展内容")
            self.line_Trend.setPlaceholderText("需要先安装CV2扩展包才可使用")
            self.line_Trend.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.FPS_spinBox.setEnabled(False)

        self.group_theme.addButton(self.radioButton_white)
        self.group_theme.addButton(self.radioButton_custom)
        self.group_theme.addButton(self.radioButton_trend)

        # 要检查的文件名
        file_name = 'Fuchen_Start_File.bat'
        result = self.check_startup_file(file_name)
        self.First = False
        if result:
            self.checkBox_start.setChecked(True)
            self.First = True
        if window_s == True:
            self.checkBox_float.setChecked(True)
        else:
            self.checkBox_float.setChecked(False)

        if Theme == "White":
            self.radioButton_white.setChecked(True)
        elif Theme == 'Custom':
            self.radioButton_custom.setChecked(True)
            with open('config.json', 'r') as file:  # 填充自定义图片壁纸的输入栏
                config = json.load(file)
            # 添加新元素到数据结构
            Path_Custom = config["Path"]
            self.line_Custom.setText(Path_Custom)
        elif Theme == 'Trend':
            self.radioButton_trend.setChecked(True)
            with open('config.json', 'r') as file:  # 填充自定义图片壁纸的输入栏
                config = json.load(file)
            # 添加新元素到数据结构
            Path_Trend = config["Path"]
            self.line_Trend.setText(Path_Trend)
        else:
            self.radioButton_white.setChecked(True)

        self.label.setText("设置")

        self.check_sound.setText("点击提示音")
        self.check_autologin.setText("自动登录")
        self.radioButton_white.setText("白色主题")
        self.radioButton_custom.setText("自定义背景图片")
        self.radioButton_trend.setText("动态主题")
        self.pushButton_2.setText("选择")
        self.pushButton_3.setText("选择")
        self.Button_Close.clicked.connect(self.clos)
        self.pushButton.clicked.connect(self.set)
        self.pushButton_2.clicked.connect(lambda: self.select_bf("Image"))
        self.pushButton_3.clicked.connect(lambda: self.select_bf("Video"))

    def clos(self):
        self.close()

    def sync_checkbox(self, state):
        if state == 2:
            self.radioButton_close.setEnabled(False)
            self.radioButton_minisize.setEnabled(False)
        elif state == 0:
            self.radioButton_close.setEnabled(True)
            self.radioButton_minisize.setEnabled(True)

    def problem(self, type):
        if type == 'download':
            window = extend_install.DownloadDialog(self)
            window.exec_()
        else:
            pyautogui.confirm("此功能对电脑占用较高\n不推荐使用大于20秒的视频 否则可能会过多占用内存!!!")
        '''dialog = SundryUI.DownloadDialog()
        result = dialog.exec_()  # 阻塞式显示

        if result == QDialog.Accepted:
            if dialog.selected_method == "manual":
                print("执行手动下载操作...")
            elif dialog.selected_method == "auto":
                print("执行自动下载操作...")
        else:
            print("用户关闭了窗口")'''
        '''if pyautogui.confirm(
                "动态主题需要安装扩展包 点击确认跳转下载界面\n 注意: 不推荐使用大于20秒的视频 可能会过多占用内存!!!") == "OK":
            link = windows.cv2_download_link()
            if link == "ERROR":
                result = pyautogui.confirm("链接获取失败 请重新尝试")
                if result == "OK":
                    webbrowser.open("http://fcyang.cn/others/help.html")
            else:
                webbrowser.open(link)webbrowser.open("https://wwzh.lanzout.com/ivTvj2g8e99e")'''

    def onSliderChange(self, value):
        '''transparent = value
        windows.update()'''
        pass

    def check_startup_file(self, file_name):
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows',
                                      'Start Menu', 'Programs', 'Startup')
        file_path = os.path.join(startup_folder, file_name)

        if os.path.exists(file_path):
            return 1
        else:
            return 0

    def select_bf(self, ty):
        if ty == "Image":
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "",
                                                       "图片文件 (*.jpg *.jpeg *.png *.bmp *.gif)",
                                                       options=options)
            if file_name:
                self.line_Custom.setText(file_name)
            '''else:
                pyautogui.confirm("未选择文件！")'''
        elif ty == "Video":
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(self, "选择视频", "",
                                                       "视频文件 (*.mp4 *.mov *.flv *.avi)",
                                                       options=options)
            if file_name:
                self.line_Trend.setText(file_name)
            '''else:
                pyautogui.confirm("未选择文件！")'''

    def set(self):
        global Log, Sound, ClosePrompt, CloseExecute, window_s, Theme ,transparent, FPS
        if self.check_sound.isChecked():
            Sound = True
        else:
            Sound = False
        if self.check_autologin.isChecked():
            Log = True
        else:
            Log = False
        if self.check_closeprompt.isChecked():
            ClosePrompt = True
        else:
            ClosePrompt = False
        if self.radioButton_close.isChecked():
            CloseExecute = "Close"
        else:
            CloseExecute = "Hide"
        with open('config.json', 'r') as file:
            config = json.load(file)
        transparent = self.slider.value()
        windows.update()
        config["AutoLogin"] = Log
        config["Sound"] = Sound
        config["ClosePrompt"] = ClosePrompt
        config["CloseExecute"] = CloseExecute
        config["transparent"] = transparent
        if self.FPS_spinBox.value() != FPS:
            config["FPS"] = self.FPS_spinBox.value()
            FPS = self.FPS_spinBox.value()
        # 将更新后的数据写入 JSON 文件
        with open('config.json', 'w') as file:
            json.dump(config, file, indent=4)
        n = True
        if (self.checkBox_start.isChecked()) and (self.First == False):
            try:
                exe_file_name = 'Fuchen.exe'
                startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows',
                                              'Start Menu', 'Programs', 'Startup')
                bat_file_path = os.path.join(startup_folder, 'Fuchen_Start_File.bat')

                with open(bat_file_path, 'w') as file:
                    file.write(f'cd /d {os.path.dirname(os.path.abspath(__file__))}\n')
                    file.write(f'start {exe_file_name}')

                print(f'成功创建并写入.bat文件到启动文件夹: {bat_file_path}')
                self.First = True
            except Exception as e:
                pyautogui.confirm(e)
        elif (self.checkBox_start.isChecked() == False) and (self.First == True):
            try:
                # 要移除的文件名
                file_name = 'Fuchen_Start_File.bat'
                startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows',
                                              'Start Menu', 'Programs', 'Startup')
                file_path = os.path.join(startup_folder, file_name)

                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f'{file_name} 已从启动文件夹中移除')
                else:
                    print(f'{file_name} 不存在于启动文件夹中')
                self.First = False
            except Exception as e:
                pyautogui.confirm(e)
        if self.radioButton_white.isChecked():
            if Theme == "Trend":
                windows.stop_dynamic_background()
            windows.should_draw = "White"  # 清空背景图片
            style = "color: black;"
            windows.setStyleSheet(style)
            # 读取 JSON 文件
            with open('config.json', 'r') as file:
                config = json.load(file)
            config["Theme"] = "White"
            # 将更新后的数据写入 JSON 文件
            with open('config.json', 'w') as file:
                json.dump(config, file, indent=4)
            Theme = "White"

        if self.radioButton_custom.isChecked():
            try:
                if Theme == "Trend":
                    windows.stop_dynamic_background()
                file_name = self.line_Custom.text()
                with open('config.json', 'r') as file:
                    config = json.load(file)
                if config["Theme"] != "Custom" or config[
                    "Path"] != file_name:  # 这个判断是为了防止目前的背景和选择的背景相同而设置 因此当选择的文件和现有设置的文件相同时 将不会执行
                    if file_name != '':
                        windows.should_draw = "Custom"
                        # 读取 JSON 文件
                        with open('config.json', 'r') as file:
                            config = json.load(file)
                        config["Theme"] = "Custom"
                        config["Path"] = file_name
                        # 将更新后的数据写入 JSON 文件
                        with open('config.json', 'w') as file:
                            json.dump(config, file, indent=4)
                        im = Image.open(file_name)
                        reim = im.resize((1000, 600))  # 宽*高

                        reim.save('./temp/background_custom.png',
                                  dpi=(400, 400))  ##200.0,200.0分别为想要设定的dpi值

                        palette = QPalette()
                        palette.setBrush(QPalette.Background,
                                         QBrush(QPixmap('./temp/background_custom.png')))
                        windows.setPalette(palette)
                        Theme = "Custom"
                    else:
                        n = False
                        pyautogui.confirm("请选择文件!")
            except Exception as e:
                print(e)
        if self.radioButton_trend.isChecked():
            file_name_V = self.line_Trend.text()
            with open('config.json', 'r') as file:
                config = json.load(file)
            if config["Theme"] != "Trend" or config["Path"] != file_name_V:
                if config["Theme"] != "Trend":
                    if file_name_V != '':
                        windows.should_draw = "Trend"
                        # 读取 JSON 文件
                        with open('config.json', 'r') as file:
                            config = json.load(file)
                        config["Theme"] = f"Trend"
                        config["Path"] = file_name_V
                        # 将更新后的数据写入 JSON 文件
                        with open('config.json', 'w') as file:
                            json.dump(config, file, indent=4)
                        self.pushButton.setText("正在加载 请等待")
                        self.pushButton.repaint()
                        windows.deal_pictures(file_name_V)
                        windows.execute_trend()
                        self.pushButton.setText("设置")
                        Theme = "Trend"
                elif config["Path"] != file_name_V:
                    with open('config.json', 'r') as file:
                        config = json.load(file)
                    config["Theme"] = f"Trend"
                    config["Path"] = file_name_V
                    # 将更新后的数据写入 JSON 文件
                    with open('config.json', 'w') as file:
                        json.dump(config, file, indent=4)
                    self.pushButton.setText("正在加载 请等待")
                    self.pushButton.repaint()
                    windows.deal_pictures(file_name_V)
                    windows.execute_trend_again()
                    self.pushButton.setText("设置")
        if self.checkBox_float.isChecked() and window_s == False:
            windows.open_floating_window()
            window_s = True
        elif self.checkBox_float.isChecked() == False and window_s == True:
            windows.close_floating_window()
            window_s = False
        Set = [Log, Sound, ClosePrompt, CloseExecute, window_s, Theme ,transparent, FPS]
        windows.setValue(Set)
        if n == True:
            pyautogui.confirm("设置成功!")

    def paintEvent(self, event):
        # 阴影
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)

        pat = QPainter(self)
        pat.setRenderHint(pat.Antialiasing)
        pat.fillPath(path, QBrush(Qt.white))

        color = QColor(171, 171, 171, 70)

        for i in range(10):
            i_path = QPainterPath()
            i_path.setFillRule(Qt.WindingFill)
            ref = QRectF(10 - i, 10 - i, self.width() - (10 - i) * 2,
                         self.height() - (10 - i) * 2)
            # i_path.addRect(ref)
            i_path.addRoundedRect(ref, self.border_width, self.border_width)
            color.setAlpha(int(150 - i ** 0.5 * 50))
            pat.setPen(color)
            pat.drawPath(i_path)

        # 圆角
        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.Antialiasing)  # 抗锯齿
        pat2.setBrush(Qt.white)
        pat2.setPen(Qt.transparent)

        rect = self.rect()
        rect.setLeft(9)
        rect.setTop(9)
        rect.setWidth(rect.width() - 9)
        rect.setHeight(rect.height() - 9)
        pat2.drawRoundedRect(rect, 4, 4)

    def mousePressEvent(self, e):
        if e.y() <= 25:  # 30像素的标题栏高度
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if hasattr(self, 'start_point'):
            relpos = e.globalPos() - self.start_point
            self.move(self.window_point + relpos)

    def mouseReleaseEvent(self, e):
        if hasattr(self, 'start_point'):
            delattr(self, 'start_point')
class this:
    def x():
        return 500
    def y():
        return 300
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SETWINDOW = SetWindow([this, True, False, False, False, "Close", False, "White", 50, 30]) #self, cv2_available, Log, Sound, ClosePrompt, CloseExecute, window_s, Theme, transparent,FPS
    SETWINDOW.show()
    sys.exit(app.exec_())