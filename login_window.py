import time
import json
import traceback
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.Qt import QDesktopServices

import Login
from ui.ResetWindow import Reset
from ui.RegisterWindow import Register


class LoginWindow(QMainWindow):  # 实例化登录窗口
    # 添加自定义信号
    login_successful = pyqtSignal(dict)  # 发送包含用户信息的字典

    def __init__(self, s, connect_status, stdout_stream, stderr_stream, globals_dict=None):
        super().__init__()
        self.s = s
        self.connect_status = connect_status
        self.stdout_stream = stdout_stream
        self.stderr_stream = stderr_stream

        # 从全局字典中获取必要的变量
        self.globals = globals_dict or {}
        self.remember = self.globals.get('remember', False)
        self.AutoLogin = self.globals.get('AutoLogin', False)
        self.Account = self.globals.get('Account', '')
        self.Password = self.globals.get('Password', '')
        self.Number_People = self.globals.get('Number_People', '加载中...')
        self.Version = self.globals.get('Version', 'V1.0')
        self.city_name = self.globals.get('city_name', 'Unknown')
        self.system = self.globals.get('system', '')
        self.computer_name = self.globals.get('computer_name', '')

        # 初始化UI
        self.ui = Login.Ui_MainWindow()
        self.ui.setupUi(self)
        self.reset_window_status = False
        self.register_window_status = False
        self.reset_window = None
        self.register_window = None
        self.register_saved_state = {}  # 新增：保存注册窗口状态
        self.reset_saved_state = {}  # 新增：保存重置窗口状态

        if self.remember == True:
            self.ui.checkBox.click()
        if self.AutoLogin == True:
            self.ui.checkBox2.click()

        self.ui.Account_lineEdit.setText(str(self.Account))
        self.ui.Password_lineEdit.setText(str(self.Password))
        self.setWindowTitle("Fuchen 登录")
        icon = QIcon(".image/window.ico")
        self.setWindowIcon(icon)
        self.ui.pushButton_signin.clicked.connect(self.reg)  # 注册按钮
        self.ui.Login_Button.clicked.connect(lambda: self.LOGIN("login"))  # 登录按钮

        self.ui.pushButton_tourist.clicked.connect(lambda: self.LOGIN("tourist_login"))  # 游客登录
        self.ui.pushButton_short.clicked.connect(self.showMinimized)  # 最小化按钮
        self.ui.pushButton_more.clicked.connect(self.open_file_background)

        self.ui.pushButton_quit.clicked.connect(self.close)  # 关闭窗口按钮

        self.open_memory_hotkey = QShortcut(QKeySequence("Ctrl+1"), self)
        self.open_memory_hotkey.activated.connect(lambda: self.key("memory"))
        self.open_autologin_hotkey = QShortcut(QKeySequence("Ctrl+2"), self)
        self.open_autologin_hotkey.activated.connect(lambda: self.key("autologin"))

        self.ui.Account_lineEdit.returnPressed.connect(self.ui.Password_lineEdit.setFocus)
        self.ui.Password_lineEdit.returnPressed.connect(lambda: self.LOGIN("login"))
        font = QFont("等线", 14)
        self.ui.Account_lineEdit.setFont(font)
        self.ui.Password_lineEdit.setFont(font)
        self.ui.Number_Label.setText(f'当前在线人数:{self.Number_People}')
        self.ui.Number_Label.setVisible(False)

        self.ui.Version_Label.setText(f'版本:{self.Version}')
        self.ui.Version_Label.move(self.ui.Number_Label.pos().x(),self.ui.Number_Label.pos().y() )
        self.ui.pushButton_reword.clicked.connect(self.rew)

    def open_file_background(self):
        result = QMessageBox.information(self, "提示",
                                         "登录界面背景图片可自定义\n若文件夹中存放多个图片将随机选择一张\n点击确认将打开图片文件夹")
        if result == QMessageBox.Ok:
            folder_path = 'C:\\Fuchen\\image'
            url = QUrl.fromLocalFile(folder_path)
            QDesktopServices.openUrl(url)

    def closeEvent(self, e):
        self.close()
        if self.reset_window_status == True:
            self.reset_window.close()
        if self.register_window_status == True:
            self.register_window.close()

    def key(self, types):
        if types == 'memory':
            if self.ui.checkBox.isChecked():
                self.ui.checkBox.setChecked(False)
            else:
                self.ui.checkBox.setChecked(True)
        else:
            if self.ui.checkBox2.isChecked():
                self.ui.checkBox2.setChecked(False)
            else:
                self.ui.checkBox2.setChecked(True)

    def mousePressEvent(self, e):
        if e.y() <= 30:  # 30像素的标题栏高度
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if hasattr(self, 'start_point'):
            relpos = e.globalPos() - self.start_point
            self.move(self.window_point + relpos)

    def mouseReleaseEvent(self, e):
        if hasattr(self, 'start_point'):
            delattr(self, 'start_point')

    def LOGIN(self, mode):  # 登录函数
        try:
            if mode == 'login':
                self.ui.Login_Button.setEnabled(False)
                time.sleep(0.1)
                Account = self.ui.Account_lineEdit.text()
                Password = self.ui.Password_lineEdit.text()
                if (len(Account) != 6) and ('@' not in Account):  # 非邮箱非数字
                    if self.AutoLogin == True:
                        self.show()
                    QMessageBox.information(self, '提示', "账号为6位数字或邮箱 请重新输入!")
                    self.ui.Login_Button.setEnabled(True)
                    return 0
                if not (7 < len(Password) < 16):
                    if self.AutoLogin == True:
                        self.show()
                    QMessageBox.information(self, '提示', "密码为8-15位 请重新输入!")
                    self.ui.Login_Button.setEnabled(True)
                    return 0
                if (len(Account) == 6) and (not Account.isdigit()):  # 数字类型错误
                    QMessageBox.information(self, '提示', "账号为6位数字或邮箱 请重新输入!")
                    self.ui.Login_Button.setEnabled(True)
                    return 0
                if '@' in Account:
                    # 通过 '@' 分割邮箱
                    local_part, domain_part = Account.split('@')
                    # 只将域名部分转换为小写
                    domain_part = domain_part.lower()
                    # 将用户名和处理后的域名拼接起来
                    Account = f"{local_part}@{domain_part}"
                    del local_part, domain_part
                self.TypedJSONClient('login', {'user_input': Account, 'password': Password, 'position': self.city_name,
                                               'system': self.system, 'computer_name': self.computer_name})
                time.sleep(0.1)
                request = self.recv_json(self.s)
                if request.get('type') == 'login_status':
                    log_ST = request.get('data')
                    log_ST = log_ST.get("status")
                if log_ST == "pass":
                    print("密码正确 登录成功 正在加载中")
                elif log_ST == "Cooling":
                    QMessageBox.information(self, '提示', "账号密码输入次数过多 账号已被锁定!请于一小时后重新登录")
                else:
                    print("密码错误 请重试")
            elif mode == 'tourist_login':
                self.TypedJSONClient('login_tourist',
                                     {'position': self.city_name})
                self.ui.Login_Button.setEnabled(False)

                Account = "游客"
                Password = "None"
                time.sleep(0.1)
                request = self.recv_json(self.s)
                if request.get('type') == 'login_status':
                    log_ST = request.get('data')
                    log_ST = log_ST.get("status")
            elif mode == 'offline_login':
                self.ui.Login_Button.setEnabled(False)
                Account = "离线"
                Password = "None"
                time.sleep(0.1)
                log_ST = 'pass'
            else:
                log_ST = 'fail'
            if log_ST == 'pass':  # 密码正确
                self.ui.pushButton_signin.setEnabled(False)
                self.ui.Login_Button.setEnabled(False)
                self.ui.pushButton_short.setEnabled(False)
                self.ui.pushButton_quit.setEnabled(False)
                self.ui.Login_Button.setText("正在加载用户数据")
                self.ui.Login_Button.repaint()
                # 记录开始时间
                start_time = time.time()

                # 更新全局变量
                self.globals['Account'] = Account
                self.globals['Password'] = Password

                if self.connect_status != None:
                    request = self.recv_json(self.s)
                    request_type = request.get('type')
                    request_data = request.get('data')
                    if request_type == 'login_successfully':
                        if "@" in Account:
                            Account = request_data.get("account")
                            self.globals['Account'] = Account
                        self.globals['Name'] = request_data.get("name")
                        self.globals['Email'] = request_data.get("email")
                        self.globals['avatar_status'] = request_data.get("avatar_status")
                        self.globals['avatar_date'] = request_data.get("avatar_date")
                        self.globals['exp'] = request_data.get("exp")
                else:
                    self.globals['Name'] = '游客'
                    self.globals['Email'] = None
                    self.globals['avatar_status'] = False
                    self.globals['avatar_date'] = '2000-1-1'
                    self.globals['exp'] = 100

                time.sleep(0.1)
                if self.globals.get('avatar_status') == True:
                    try:
                        self.ui.Login_Button.setText("正在加载用户头像")
                        self.ui.Login_Button.repaint()
                        print(f'正在加载用户头像 账号: {Account}')
                        # 接收图片文件大小
                        file_size = int(self.s.recv(1024).decode().rstrip('\n'))
                        with open('./temp/avatar.png', 'wb') as file:
                            total_received = 0
                            while total_received < file_size:
                                chunk = self.s.recv(2048)
                                time.sleep(0.05)
                                if chunk == '\n':  # 检测到结束标记
                                    break
                                if not chunk:
                                    break
                                file.write(chunk)
                                total_received += len(chunk)
                                progress_percentage = round(total_received / file_size * 100, 2)  # 将进度转换为百分比并保留两位小数
                                self.ui.Login_Button.setText(f"正在加载用户头像 {progress_percentage}%")
                                self.ui.Login_Button.repaint()
                        print('文件写入完成')
                        self.globals['avatar_load_status'] = True
                        self.ui.Login_Button.setText("头像加载成功")
                    except Exception as e:
                        print("文件接收类型错误", e)
                        self.ui.Login_Button.setText("头像加载失败")
                    self.ui.Login_Button.repaint()
                    time.sleep(0.2)

                if self.ui.checkBox.isChecked() and self.ui.checkBox2.isChecked():  # 记住密码 自动登录
                    with open('config.json', 'r') as file:
                        config = json.load(file)
                    # 添加新元素到数据结构
                    config["Remember"] = True
                    config["Account"] = f"{self.ui.Account_lineEdit.text()}"
                    config["Password"] = f"{self.ui.Password_lineEdit.text()}"
                    config["AutoLogin"] = True
                    self.globals['AutoLogin'] = True
                    # 将更新后的数据写入 JSON 文件
                    with open('config.json', 'w') as file:
                        json.dump(config, file, indent=4)
                elif self.ui.checkBox.isChecked():  # 记住密码
                    # 读取 JSON 文件
                    with open('config.json', 'r') as file:
                        config = json.load(file)
                    # 添加新元素到数据结构
                    config["Remember"] = True
                    config["Account"] = f"{self.ui.Account_lineEdit.text()}"
                    config["Password"] = f"{self.ui.Password_lineEdit.text()}"
                    # 将更新后的数据写入 JSON 文件
                    with open('config.json', 'w') as file:
                        json.dump(config, file, indent=4)
                elif self.ui.checkBox2.isChecked():  # 自动登录
                    # 读取 JSON 文件
                    with open('config.json', 'r') as file:
                        config = json.load(file)
                    # 添加新元素到数据结构
                    config["AutoLogin"] = True
                    self.globals['AutoLogin'] = True
                    # 将更新后的数据写入 JSON 文件
                    with open('config.json', 'w') as file:
                        json.dump(config, file, indent=4)
                else:  # 不记住密码/自动登录
                    with open('config.json', 'r') as file:
                        config = json.load(file)
                    # 添加新元素到数据结构
                    config["Remember"] = False
                    config["Account"] = ""
                    config["Password"] = ""
                    config["AutoLogin"] = False
                    # 将更新后的数据写入 JSON 文件
                    with open('config.json', 'w') as file:
                        json.dump(config, file, indent=4)
                self.close()

                # 设置登录成功状态
                self.login_success = True

                # 读取JSON文件中的配置
                with open('config.json', 'r') as file:
                    config = json.load(file)

                self.globals['window_s'] = False
                self.globals['Sound'] = config.get("Sound", True)
                self.globals['ClosePrompt'] = config.get("ClosePrompt", True)
                self.globals['CloseExecute'] = config.get("CloseExecute", "Close")
                self.globals['Theme'] = config.get("Theme", "White")  # 主题
                self.globals['transparent'] = config.get("transparent", 30)
                self.globals['FPS'] = config.get("FPS", 16)

                if self.globals['Theme'] == "Custom":
                    self.globals['Path_Custom_S'] = config.get("Path")
                elif self.globals['Theme'] == "Trend":
                    self.globals['Path_Trend_S'] = config.get("Path")
                # 准备要发送的数据
                login_data = {
                    'Account': Account,
                    'Name': self.globals.get('Name'),
                    'avatar_status': self.globals.get('avatar_status'),
                    'avatar_load_status': self.globals.get('avatar_load_status', False),
                    'avatar_date': self.globals.get('avatar_date', '2000-1-1'),
                    'email': self.globals.get('Email', None),
                    'exp': self.globals.get('exp', 100),
                    # 添加其他需要传递的数据
                }

                # 发送登录成功信号，带上数据
                self.login_successful.emit(login_data)
                # 登录成功，返回给主程序处理
                return True

            elif log_ST == "cooling":
                QMessageBox.information(self, '提示', "账号密码输入次数过多 账号已被锁定!请于一小时后重新登录")
                return False
            else:
                self.ui.Login_Button.setEnabled(False)
                if self.AutoLogin == True:
                    self.show()
                time.sleep(0.5)
                QMessageBox.information(self, '提示', "密码错误")
                self.ui.Login_Button.setEnabled(True)
                return False

        except Exception as e:
            traceback.print_exc()
            QMessageBox.information(self, "未知错误", str(e))
            return False

    def reg(self):
        if self.register_window_status is False:
            self.register_window_status = True
            self.register_window = Register(self.s)
            '''# 恢复注册窗口状态
            self.register_window.username.setText(
                self.register_saved_state.get('account', ''))
            self.register_window.password.setText(
                self.register_saved_state.get('password', ''))
            self.register_window.email.setText(
                self.register_saved_state.get('email', ''))
            self.register_window.verify_code.setEnabled(
                self.register_saved_state.get('submit_enabled', True))
            self.register_window.countdown = self.register_saved_state.get('countdown', True)

            result = self.register_window.exec_()'''

            self.register_window.exec_()
            if self.register_window.result_value != None:
                if self.register_window.result_value[0] == '注册成功':
                    self.ui.Account_lineEdit.setText(self.register_window.result_value[1])
                    self.ui.Password_lineEdit.setText(self.register_window.result_value[2])
                    self.ui.checkBox.setChecked(True)
            #self.register_saved_state = self.register_window.saved_state
            self.register_window_status = False

    def rew(self):
        if self.reset_window_status == False:
            self.reset_window_status = True
            self.reset_window = Reset(self.s)
            self.reset_window.exec_()
            self.reset_window_status = False

    # 帮助函数，从主程序复制过来
    def TypedJSONClient(self, msg_type, payload):
        import json
        import struct
        data = {"type": msg_type, "data": payload}
        # 发送请求
        json_data = json.dumps(data).encode('utf-8')
        header = struct.pack('>I', len(json_data))
        self.s.sendall(header + json_data)

    def recv_json(self, sock):
        """接收JSON数据（带长度前缀）"""
        import json
        import struct
        try:
            # 读取4字节长度头
            header = sock.recv(4)
            if len(header) != 4:
                return None
            data_len = struct.unpack('>I', header)[0]

            # 分块读取数据
            chunks = []
            bytes_received = 0
            while bytes_received < data_len:
                chunk = sock.recv(min(data_len - bytes_received, 4096))
                if not chunk:
                    break
                chunks.append(chunk)
                bytes_received += len(chunk)
            return json.loads(b''.join(chunks).decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"JSON解码失败: {e}")
            return {'error': 'Invalid JSON'}
        except struct.error:
            return None
