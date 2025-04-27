import os,random,socket,ssl,sys,time,traceback,requests,re,json,struct
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QPushButton, QLineEdit, QMessageBox, QHBoxLayout, \
    QApplication



def Check(input_str):  # 检测名称
    # 定义允许的字符集合：中文、大小写英文字母、数字、- . ? ~ _
    allowed_characters = re.compile(r'^[\u4e00-\u9fa5a-zA-Z0-9\-.?~_]+$')
    return not bool(allowed_characters.match(input_str))


def Check_Password(input_str):
    # 定义允许的字符集合：大小写英文字母、数字、- . ? ~ _
    allowed_characters = re.compile(r'^[a-zA-Z0-9\-.?~_]+$')
    return not bool(allowed_characters.match(input_str))


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return 0
    else:
        return 1

def TypedJSONClient(msg_type,payload):
    data = {"type": msg_type, "data": payload}
    # 发送请求
    json_data = json.dumps(data).encode('utf-8')
    header = struct.pack('>I', len(json_data))
    s.sendall(header + json_data)


def recv_json(sock):
    """接收JSON数据（带长度前缀）"""
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


class Register(QDialog):
    def __init__(self, sock):
        super().__init__()
        global s
        s = sock
        self.username_input = None  # 用户名输入框
        self.password_input = None  # 密码输入框
        self.email_input = None  # 邮箱输入框
        self.code_input = None  # 验证码输入框（已存在）
        self.initUI()
        self.countdown = 60  # 验证码倒计时时长
        self.result_value = None  #注册结果
        self.Email = None

    def initUI(self):
        # 窗口设置
        self.setWindowTitle('注册账号')
        self.setFixedSize(380, 500)  # 调整后的窗口尺寸
        self.setStyleSheet("background-color: #f0f2f5;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # 设置应用程序图标
        app_icon = QIcon("./image/Component/注册.png")  # 替换为实际的图标路径
        self.setWindowIcon(app_icon)


        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)  # 减少边距
        main_layout.setSpacing(15)

        # 标题
        title = QLabel("注册账号")
        title.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        title.setStyleSheet("color: #1a73e8;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # 表单容器
        form_widget = QWidget()
        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(0, 0, 0, 0)

        # 用户名输入
        self.username = self.create_input("用户名", "请输入用户名")
        form_layout.addWidget(self.username)
        self.image_random = QPushButton(self.username)
        self.image_random.setGeometry(QRect(280, 35, 26, 26))
        self.image_random.setObjectName("image_random")
        self.image_random.setStyleSheet("QPushButton#image_random {"
                                        "    border-image: url(./image/Component/随机.png);"
                                        "background-color: transparent"
                                        "}")
        self.image_random.clicked.connect(self.random_name)
        self.image_random.raise_()

        # 密码输入
        self.password = self.create_input("密码", "请输入密码", is_password=True)
        form_layout.addWidget(self.password)

        # 邮箱输入
        self.email = self.create_input("邮箱", "请输入邮箱")
        form_layout.addWidget(self.email)

        # 验证码输入
        self.verify_code = self.create_verify_code_input()
        form_layout.addWidget(self.verify_code)

        form_widget.setLayout(form_layout)
        main_layout.addWidget(form_widget)

        # 注册按钮
        btn_register = QPushButton("立即注册")
        btn_register.setCursor(Qt.PointingHandCursor)
        btn_register.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1a73e8, stop:1 #4a90e2);
                color: white;
                border-radius: 20px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover { background-color: #1662c4; }
        """)
        btn_register.clicked.connect(self.start_register)
        main_layout.addWidget(btn_register)

        # 底部间距
        main_layout.addStretch(1)

        self.setLayout(main_layout)
    def random_name(self):
        try:
            with open('./mod/dic/name.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if lines:
                    random_line = random.choice(lines).strip()
                    self.username_input.setText(random_line)
        except FileNotFoundError:
            print("The file 'name.txt' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")


    def create_input(self, label, placeholder, is_password=False):
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # 标签
        lbl = QLabel(label)
        lbl.setFont(QFont("Microsoft YaHei", 10))
        lbl.setStyleSheet("color: #5f6368; padding-bottom: 3px;")
        layout.addWidget(lbl)

        # 输入框
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setFont(QFont("Microsoft YaHei", 11))
        line_edit.setMinimumHeight(38)
        # 根据类型保存引用
        if label == "用户名":
            self.username_input = line_edit
        elif label == "密码":
            self.password_input = line_edit
        elif label == "邮箱":
            self.email_input = line_edit

        '''if is_password:
            line_edit.setEchoMode(QLineEdit.Password)

        if is_password:
            line_edit.setEchoMode(QLineEdit.Password)'''
        line_edit.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #dadce0;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QLineEdit:focus { border-color: #1a73e8; }
        """)
        layout.addWidget(line_edit)

        container.setLayout(layout)
        return container

    def create_verify_code_input(self):
        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 输入框部分
        input_group = QWidget()
        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(0, 0, 0, 0)

        lbl_code = QLabel("验证码")
        lbl_code.setFont(QFont("Microsoft YaHei", 10))
        lbl_code.setStyleSheet("color: #5f6368; padding-bottom: 3px;")
        v_layout.addWidget(lbl_code)

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("请输入验证码")
        self.code_input.setFont(QFont("Microsoft YaHei", 11))
        self.code_input.setMinimumHeight(38)
        self.code_input.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #dadce0;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QLineEdit:focus { border-color: #1a73e8; }
        """)
        v_layout.addWidget(self.code_input)
        input_group.setLayout(v_layout)

        # 按钮部分
        self.btn_get_code = QPushButton("获取验证码")
        self.btn_get_code.setFixedSize(100, 38)  # 调整按钮尺寸
        self.btn_get_code.setFont(QFont("Microsoft YaHei", 10))
        self.btn_get_code.setCursor(Qt.PointingHandCursor)
        self.btn_get_code.setStyleSheet("QPushButton{border-radius: 5px; background-color: #8ed7ff; color: white;}")
        '''self.btn_get_code.setStyleSheet("""
            QPushButton {
                background-color: #e8f0fe;
                color: #1a73e8;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #d2e3fc; }
            QPushButton:disabled { 
                background-color: #f8f9fa;
                color: #bdc1c6;
            }
        """)'''
        self.btn_get_code.clicked.connect(self.get_code)

        layout.addWidget(input_group)
        layout.addWidget(self.btn_get_code)
        layout.setAlignment(self.btn_get_code, Qt.AlignBottom)  # 按钮底部对齐

        container.setLayout(layout)
        return container

    def get_code(self):
        self.Email = self.email_input.text()
        if validate_email(self.Email) == 0:
            # send_encry("**--*Registration*--**")
            TypedJSONClient('registration',
                            {'step': 'Email', 'email': self.Email})
            time.sleep(0.3)
            # send_encry(f'Email {self.ui2.EmailEdit.text()}')
            self.btn_get_code.setEnabled(False)
            style = "QPushButton{border-radius: 5px; background-color: #e0e0e0; color: black;}"
            self.btn_get_code.setStyleSheet(style)
            result = recv_json(s)
            print(result,result.get("type"))
            if result.get("type") == 'registration_response':
                if result.get("data") == 'Successfully_send':
                    print('发送成功')
                    self.remaining_time = 60
                    self.timer.start(1000)
                    self.update_timer()
                    QMessageBox.information(self, '提示', "验证码发送成功!")
                else:
                    self.btn_get_code.setEnabled(True)
                    QMessageBox.information(self, '提示',"验证码发送失败")
        else:
            QMessageBox.information(self, '提示',"请输入正确的邮箱")

    def update_timer(self):  # 验证码更新
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.btn_get_code.setText(f"剩余时间: {self.remaining_time}秒")
        else:
            self.timer.stop()
            self.btn_get_code.setText("获取验证码")
            self.btn_get_code.setEnabled(True)
            style = "QPushButton{border-radius: 5px; background-color: #55c3ff; color: white;}"
            self.btn_get_code.setStyleSheet(style)
    def start_register(self):
        try:
            #global Email
            input_name = self.username_input.text()
            input_password = self.password_input.text()
            input_email = self.Email
            input_check = self.code_input.text()
            # 邮箱格式处理（用户名保留大小写，域名强制小写）
            try:
                local_part, domain_part = input_email.split('@')
                input_email = f"{local_part}@{domain_part.lower()}"
            except:
                input_email = input_email

            if not (0 < len(input_name) < 11):
                QMessageBox.information(self,'提示', '名称只能为1-10位')
                return 0
            if not (7 < len(input_password) < 16):
                QMessageBox.information(self,'提示', '密码只能为8-15位')
                return 0
            if len(input_email) == 0:
                QMessageBox.information(self,'提示', '请输入邮箱')
                return 0
            if len(input_check) != 6:
                QMessageBox.information(self,'提示','请输入六位验证码')
                return 0
            if validate_email(input_email) == 1:
                QMessageBox.information(self,'提示', '邮箱格式不正确')
                return 0
            if Check(input_name) == 1:
                QMessageBox.information(self,'提示', '名称只能包含中文 26个大小写字母以及  .  -  _  =  ')
                return 0
            if Check_Password(input_password) == 1:
                QMessageBox.information(self,'提示', '密码只能包含26个大小写字母以及  .  -  _  =  ')
                return 0
            if not self.Email:
                QMessageBox.information(self,'提示','未发送验证码 请发送后再尝试')
                return 0

            time.sleep(0.3)
            try:
                res = requests.get('http://myip.ipip.net', timeout=5).text
                # 提取城市信息
                split_res = res.split('  ')
                city_info = split_res[-2]  # 倒数第二个元素是城市信息
                city_info = city_info.split(' ')
                city_info = city_info[-1]
                city_name = city_info
            except:
                city_name = 'Unknown'
            # 发送注册请求
            TypedJSONClient('registration', {
                'step': 'start_register',
                'username': input_name,
                'password': input_password,
                'email': input_email,  # 使用处理后的邮箱
                'code': input_check,
                'city': city_name  # 添加地理位置信息
            })
            response = recv_json(s)
            print(response)
            if response.get("type") == 'registration_response':
                data = response.get("data", {})

                if data.get("status") == 'Successfully':
                    # 处理注册成功逻辑
                    user_id = data.get("user_id")
                    self.show_success_message(user_id)

                elif data.get("status") == 'Error_Email':
                    self.show_error_message("邮箱已被注册")

                elif data.get("status") == 'Invalid_Code':
                    self.show_error_message("验证码错误或已过期")

                else:
                    self.show_error_message("注册失败，未知错误")

            else:
                self.show_error_message("无效的服务器响应")
        except:
            traceback.print_exc()
        '''if Check_Email == 'Right_Check':
            Reg_Staus = s.recv(1024)
            Reg_Staus = send_decry(Reg_Staus)
            Reg_Staus = Reg_Staus.split()
            if Reg_Staus[0] == 'Successfully':
                self.close()
                window_login.close()
                # 获取桌面路径
                def get_desktop_path():
                    return os.path.join(os.path.expanduser("~"), "Desktop")
                desktop_path = get_desktop_path()
                file_name = 'Fuchen账号.txt'
                file_path = os.path.join(desktop_path, file_name)
                # 写入文件
                with open(file_path, "w", encoding='utf-8') as file:
                    file.write(
                        f"您已注册成功 \n系统随机分配的账号ID为:{Reg_Staus[1]}  密码:{self.ui2.PasswordEdit.text()}\n")
                    file.write(f"请妥善保管账号和密码 请勿泄露给他人！\n感谢您的使用")
                pyautogui.alert(f"账号注册成功!您的ID为:{Reg_Staus[1]}"
                                f"账号ID由服务器自动分配 登录时需用ID登录而不是用户名\n\n"
                                f"为了避免您忘记账号 现已将您的账号ID文件创建到桌面 >>Fuchen账号.txt中\n"
                                f"请您尽快记住账号并妥当保管文件 以防丢失账号 泄露账号等情况\n\n"
                                f"在此非常感谢您使用我的软件\n"
                                f"请关闭此窗口 或点击确认按钮 登录线上模式使用吧!")
            else:
                pyautogui.confirm("注册失败")
                self.close()

        elif Check_Email == 'Error_Email':
            self.pushButton3.setEnabled(False)
            MyThread(play_warning_sound)
            pyautogui.confirm("邮箱已被注册! 请更换邮箱后注册")
            self.pushButton3.setEnabled(True)
        else:
            pyautogui.confirm("验证码不正确")'''

    def show_success_message(self, user_id):
        # 创建账号文件（保持原有逻辑）
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        with open(os.path.join(desktop_path, 'Fuchen账号.txt'), "w", encoding='utf-8') as f:
            f.write(f"注册成功\nID: {user_id}\n密码: {self.password_input.text()}\n请妥善保管")

        # 弹窗提示
        QMessageBox.information(
            self,
            "注册成功",
            f"您的ID为: {user_id}\n账号信息已自动填入登录界面 请前往登录\n账号信息已保存至桌面文件",
            QMessageBox.Ok
        )
        #self.close()
        self.result_value = ['注册成功', user_id, self.password_input.text()]  # 保存需要返回的数据
        self.accept()  # 触发 Accepted 状态


    def show_error_message(self, text):
        QMessageBox.critical(
            self,
            "注册失败",
            text,
            QMessageBox.Ok
        )
        self.code_input.clear()

    def on_register(self):
        # 这里添加注册逻辑
        print("注册按钮被点击")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    context.load_verify_locations("certificate.pem")
    s = context.wrap_socket(s, server_hostname='fcyang.cn')
    IP = '127.0.0.1'
    Port = 9999  # 端口号
    s.settimeout(10)
    s.connect((IP, Port))
    window = Register(s,'')
    window.show()
    sys.exit(app.exec_())