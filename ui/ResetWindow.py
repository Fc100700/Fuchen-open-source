import socket,ssl,sys,time,traceback,re,json,struct
from PyQt5.QtCore import QRect, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QStackedWidget, QDialog, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QLineEdit, QPushButton, \
    QMessageBox, QApplication


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



class SlideStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super(SlideStackedWidget, self).__init__(parent)
        self.animation_duration = 500
        self._current_animation = []

    def slide_to_index(self, index, direction='left'):
        if index == self.currentIndex():
            return

        current_widget = self.currentWidget()
        next_widget = self.widget(index)

        offsetX = self.width()
        offsetY = self.height()

        if direction == 'left':
            next_widget.setGeometry(QRect(offsetX, 0, offsetX, offsetY))
            end_old = QRect(-offsetX, 0, offsetX, offsetY)
            end_new = QRect(0, 0, offsetX, offsetY)
        elif direction == 'right':
            next_widget.setGeometry(QRect(-offsetX, 0, offsetX, offsetY))
            end_old = QRect(offsetX, 0, offsetX, offsetY)
            end_new = QRect(0, 0, offsetX, offsetY)
        else:
            return

        next_widget.show()
        next_widget.raise_()

        anim_old = QPropertyAnimation(current_widget, b"geometry")
        anim_new = QPropertyAnimation(next_widget, b"geometry")

        anim_old.setDuration(self.animation_duration)
        anim_new.setDuration(self.animation_duration)
        anim_old.setEasingCurve(QEasingCurve.OutQuad)
        anim_new.setEasingCurve(QEasingCurve.OutQuad)

        anim_old.setStartValue(current_widget.geometry())
        anim_old.setEndValue(end_old)
        anim_new.setStartValue(next_widget.geometry())
        anim_new.setEndValue(end_new)

        self._current_animation = [anim_old, anim_new]

        def on_finish():
            self.setCurrentIndex(index)
            current_widget.hide()

        anim_new.finished.connect(on_finish)
        anim_old.start()
        anim_new.start()


class Reset(QDialog):
    def __init__(self,sock):
        super().__init__()
        global s
        s = sock
        self.initUI()
        self.setWindowTitle("密码重置")
        self.setFixedSize(400, 290)

    def initUI(self):
        # 创建堆叠布局
        self.stacked_layout = SlideStackedWidget()

        # 创建两个页面
        self.page1 = self.create_page1()
        self.page2 = self.create_page2()

        self.stacked_layout.addWidget(self.page1)
        self.stacked_layout.addWidget(self.page2)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_layout)
        self.setLayout(main_layout)

        # 设置样式
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f8;
                font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
            }

            QLabel {
                font-size: 15px;
                color: #2c3e50;
            }

            QLineEdit {
                border: 1px solid #ced6e0;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
                background-color: #ffffff;
                color: #34495e;
            }

            QLineEdit:focus {
                border: 1px solid #3498db;
                background-color: #ffffff;
            }

            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 6px 0px;
                border-radius: 6px;
                font-size: 15px;
            }
            QPushButton#get_code_btn{
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }

            QPushButton:disabled {
                background-color: #bdc3c7;
            }

            QVBoxLayout, QHBoxLayout {
                spacing: 4px;
            }
        """)

    def create_page1(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(15)

        title = QLabel("重置密码 - 验证身份")
        title.setFont(QFont("Arial", 16, QFont.Bold))

        email_label = QLabel("注册邮箱:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("请输入注册邮箱")

        code_layout = QHBoxLayout()
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("请输入验证码")
        self.get_code_btn = QPushButton("获取验证码")
        self.get_code_btn.clicked.connect(self.send_verification_code)
        self.get_code_btn.setFixedWidth(70)
        self.get_code_btn.setObjectName('get_code_btn')

        code_layout.addWidget(self.code_input)
        code_layout.addWidget(self.get_code_btn)

        self.verify_btn = QPushButton("验证")
        self.verify_btn.clicked.connect(self.verify_code)

        layout.addWidget(title)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addLayout(code_layout)
        layout.addWidget(self.verify_btn)

        page.setLayout(layout)
        return page

    def create_page2(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(15)

        title = QLabel("设置新密码")
        title.setFont(QFont("Arial", 16, QFont.Bold))

        pwd_label = QLabel("新密码:")
        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setPlaceholderText("请输入新密码")

        confirm_label = QLabel("确认密码:")
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setPlaceholderText("请再次输入密码")

        self.submit_btn = QPushButton("提交")
        self.submit_btn.clicked.connect(self.submit_password)

        layout.addWidget(title)
        layout.addWidget(pwd_label)
        layout.addWidget(self.pwd_input)
        layout.addWidget(confirm_label)
        layout.addWidget(self.confirm_input)
        layout.addWidget(self.submit_btn)

        page.setLayout(layout)
        return page

    def send_verification_code(self):
        email = self.email_input.text()
        if validate_email(email) != 0:
            QMessageBox.warning(self, "错误", "邮箱格式不正确")
            return

        # 发送验证码请求
        TypedJSONClient('password_reset',
                        {'step': 'request_code', 'email': email})

        response = recv_json(s)
        print(response)
        if response.get('type') == 'password_reset_response':
            if response.get('data').get("status") == 'code_sent':
                # 启动倒计时
                self.get_code_btn.setEnabled(False)
                self.countdown = 60
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.update_countdown)
                self.timer.start(1000)
                QMessageBox.information(self, "成功", "验证码已发送")
            elif response.get('data').get("message") == '邮箱未注册':
                time.sleep(0.5)
                QMessageBox.warning(self, "错误", "邮箱未注册 验证码发送失败")
            else:
                time.sleep(0.5)
                QMessageBox.warning(self, "错误", "验证码发送失败")

    def update_countdown(self):
        self.countdown -= 1
        self.get_code_btn.setText(f"重新发送({self.countdown})")
        if self.countdown <= 0:
            self.timer.stop()
            self.get_code_btn.setEnabled(True)
            self.get_code_btn.setText("获取验证码")

    def verify_code(self):
        try:
            email = self.email_input.text()
            code = self.code_input.text()

            # 发送验证请求
            TypedJSONClient('password_reset',
                            {'step': 'verify_code',
                             'email': email,
                             'code': code})

            response = recv_json(s)
            if response.get('type') == 'password_reset_response':
                data = response.get('data', {})
                if data.get('status') == 'valid_code':
                    self.stacked_layout.slide_to_index(1, direction='left')
                else:
                    QMessageBox.warning(self, "错误", data.get('message', '验证失败'))
        except:
            traceback.print_exc()

    def submit_password(self):
        new_password = self.pwd_input.text()
        confirm_password = self.confirm_input.text()

        if new_password != confirm_password:
            QMessageBox.warning(self, "错误", "两次密码输入不一致")
            return

        # 发送密码重置请求
        TypedJSONClient('password_reset',
                        {'step': 'reset_password',
                         'new_password': new_password})

        response = recv_json(s)
        print(response)
        if response.get('type') == 'password_reset_response':
            if response.get('data').get("status") == 'password_updated':
                QMessageBox.information(self, "成功", "密码已成功重置")
                self.close()
            else:
                QMessageBox.warning(self, "错误", "密码重置失败")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    context.load_verify_locations("../certificate.pem")
    s = context.wrap_socket(s, server_hostname='fcyang.cn')
    IP = '127.0.0.1'
    Port = 9999  # 端口号
    s.settimeout(10)
    s.connect((IP, Port))
    window = Reset(s)
    window.show()
    sys.exit(app.exec_())