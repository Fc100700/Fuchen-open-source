import json
import logging
import os
import socket
import ssl
import struct
import threading
import traceback
from PyQt5.QtCore import QThread, pyqtSignal, QSize, Qt, QTimer
import time
from PyQt5.QtGui import QIcon, QColor, QPixmap
import pyautogui
import re
import queue

socket_information = queue.Queue()
sock_lock = threading.Lock()  # 在全局或类里定义锁


def TypedJSONClient(msg_type, payload):
    data = {"type": msg_type, "data": payload}
    # 发送请求
    json_data = json.dumps(data).encode("utf-8")
    header = struct.pack(">I", len(json_data))
    with sock_lock:
        s.sendall(header + json_data)


def recv_json(sock):
    """接收JSON数据（带长度前缀）"""
    try:
        # 读取4字节长度头
        header = sock.recv(4)
        if len(header) != 4:
            return None
        data_len = struct.unpack(">I", header)[0]

        # 分块读取数据
        chunks = []
        bytes_received = 0
        while bytes_received < data_len:
            chunk = sock.recv(min(data_len - bytes_received, 4096))
            if not chunk:
                break
            chunks.append(chunk)
            bytes_received += len(chunk)
        return json.loads(b"".join(chunks).decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"JSON解码失败: {e}")
        return {"error": "Invalid JSON"}
    except struct.error:
        return None


class MyThread(threading.Thread):  # 多线程封装（我也看不懂反正就是这么用的）
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.setDaemon(True)
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)


class HeartbeatThread(threading.Thread):
    def __init__(self, socket_obj, interval=5):
        super().__init__()
        self.daemon = True
        self.socket = socket_obj
        self.interval = interval
        self.running = True

    def run(self):
        while self.running:
            try:
                heartbeat_data = {"type": "heartbeat", "data": {"time": time.time()}}
                json_data = json.dumps(heartbeat_data).encode("utf-8")
                header = struct.pack(">I", len(json_data))
                with sock_lock:
                    self.socket.sendall(header + json_data)
                # print("[心跳] 已发送")
            except Exception as e:
                print(f"[心跳] 发送失败: {e}")
                self.running = False
            time.sleep(self.interval)

    def stop(self):
        self.running = False


class DataThread(QThread):
    signal = pyqtSignal(str)
    show_message_signal = pyqtSignal(str, str)  # (标题, 内容)
    team_send_response = pyqtSignal(str)  # (类型)
    connection_lost = pyqtSignal()  # 连接彻底断开（重连失败）
    team_state_needs_reset = pyqtSignal()  # 需要重置组队UI状态

    def __init__(self, lis):
        super().__init__()
        global windows, s
        windows = lis[0]
        s = lis[1]
        self.socket = s
        self.server_host = str(
            self._safe_response_value("IP", "fcyang.cn") or "fcyang.cn"
        )
        try:
            self.server_port = int(self._safe_response_value("Port", 30000))
        except (TypeError, ValueError):
            self.server_port = 30000
        self.server_hostname = str(self.server_host)
        self.cert_file = "certificate.pem"
        self.access_token = self._safe_response_value("access_token", None)
        self.refresh_token = self._safe_response_value("refresh_token", None)
        self.account = self._safe_response_value("Account", None)
        self.reconnecting = False
        self.heartbeat_thread = None
        QTimer.singleShot(5000, self._start_heartbeat)  # 5000 毫秒 = 5 秒

    def _safe_response_value(self, key, default=None):
        try:
            return windows.response_value(key)
        except Exception:
            return default

    def _start_heartbeat(self):
        if self.heartbeat_thread and self.heartbeat_thread.is_alive():
            return
        self.heartbeat_thread = HeartbeatThread(self.socket)
        self.heartbeat_thread.start()

    def _set_status(self, text, color):
        windows.status_label.setStyleSheet(f"color: {color.name()};")
        windows.status_label.setText(text)

    def _set_socket(self, new_socket):
        global s
        old_socket = self.socket
        self.socket = new_socket
        s = new_socket
        try:
            windows.on_socket_reconnected(new_socket)
        except Exception:
            pass
        if old_socket is not None and old_socket is not new_socket:
            try:
                old_socket.close()
            except Exception:
                pass

    def _send_json_direct(self, sock_obj, msg_type, payload):
        packet = {"type": msg_type, "data": payload}
        json_data = json.dumps(packet).encode("utf-8")
        header = struct.pack(">I", len(json_data))
        sock_obj.sendall(header + json_data)

    def _build_secure_socket(self):
        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.create_default_context()
        if os.path.exists(self.cert_file):
            context.load_verify_locations(self.cert_file)
        secure_sock = context.wrap_socket(
            raw_sock, server_hostname=self.server_hostname
        )
        secure_sock.settimeout(10)
        secure_sock.connect((self.server_host, self.server_port))
        return secure_sock

    def _apply_new_tokens(self, access_value, refresh_value):
        self.access_token = access_value
        self.refresh_token = refresh_value
        try:
            windows.update_auth_tokens(access_value, refresh_value)
        except Exception:
            pass

    def _try_token_reconnect(self, reconnect_socket):
        if not self.access_token:
            return False

        self._send_json_direct(
            reconnect_socket,
            "reconnect",
            {"access_token": self.access_token},
        )
        reconnect_response = recv_json(reconnect_socket)
        if not reconnect_response or reconnect_response.get("type") != "reconnect":
            return False

        reconnect_data = reconnect_response.get("data") or {}
        reconnect_status = reconnect_data.get("status")
        if reconnect_status == "success":
            return True
        if reconnect_status != "access_expired":
            return False

        if not self.refresh_token:
            return False

        self._send_json_direct(
            reconnect_socket,
            "refresh_token",
            {"refresh_token": self.refresh_token},
        )
        refresh_response = recv_json(reconnect_socket)
        if not refresh_response or refresh_response.get("type") != "refresh_token":
            return False

        refresh_data = refresh_response.get("data") or {}
        if refresh_data.get("status") != "success":
            return False

        new_access = refresh_data.get("access_token")
        new_refresh = refresh_data.get("refresh_token")
        if not new_access or not new_refresh:
            return False

        self._apply_new_tokens(new_access, new_refresh)

        self._send_json_direct(
            reconnect_socket,
            "reconnect",
            {"access_token": self.access_token},
        )
        second_reconnect_response = recv_json(reconnect_socket)
        if (
            not second_reconnect_response
            or second_reconnect_response.get("type") != "reconnect"
        ):
            return False

        second_data = second_reconnect_response.get("data") or {}
        return second_data.get("status") == "success"

    def _handle_disconnect(self):
        if self.reconnecting:
            return False

        self.reconnecting = True
        self.team_state_needs_reset.emit()
        try:
            if self.heartbeat_thread:
                self.heartbeat_thread.stop()

            reconnect_color = QColor(247, 166, 0)
            self._set_status("与服务器状态: 重连中...", reconnect_color)

            for _ in range(3):
                new_socket = None
                try:
                    new_socket = self._build_secure_socket()
                    if self._try_token_reconnect(new_socket):
                        self._set_socket(new_socket)
                        self._start_heartbeat()
                        connected_color = QColor(36, 152, 42)
                        self._set_status("与服务器状态: 已连接", connected_color)
                        print("重连成功")
                        return True
                    if new_socket is not None:
                        new_socket.close()
                except Exception as reconnect_error:
                    print(f"重连失败: {reconnect_error}")
                    if new_socket is not None:
                        try:
                            new_socket.close()
                        except Exception:
                            pass
                time.sleep(1.2)

            disconnected_color = QColor(164, 38, 15)
            self._set_status("与服务器状态: 断开连接", disconnected_color)
            self.connection_lost.emit()
            return False
        finally:
            self.reconnecting = False

    def run(self):
        time.sleep(0.5)
        # s.settimeout(90)
        while True:
            try:
                # 接收请求
                request = recv_json(self.socket)

                if not request:
                    print("客户端断开连接")
                    if self._handle_disconnect():
                        continue
                    break
                # 提取数据（带基本校验）
                """if not isinstance(request, dict):
                    send_json(s, {"status": "error", "message": "Invalid request format"})
                    continue"""

                request_type = request.get("type")
                request_data = request.get("data")

                if request_type != "heartbeat_ack":
                    print(f"收到请求: {request}")

                if not request_type or not request_data:
                    # send_json(ssl_socket, {"status": "error", "message": "Missing required fields"})
                    continue
                if request_type == "server_shutdown":
                    windows.close()
                    pyautogui.confirm(
                        "服务器已经关闭!\n感谢您本次的使用 服务器维护时间请关注官方公告!"
                    )

                elif request_type == "team_join_failed":
                    # windows.open_prompt_window("队伍不存在或加入失败")
                    pyautogui.confirm("队伍不存在或加入失败", "提示")
                elif request_type == "sign_in":
                    if request_data.get("status") == "successfully":
                        socket_information.put(
                            [request_data.get("information"), request_data.get("exp")]
                        )
                    else:
                        socket_information.put(request_data.get("information"))
                elif request_type == "join_team":  # 加入队伍 (队员加入[自己])
                    try:
                        if request_data.get("status") == False:
                            self.show_message_signal.emit(
                                "提示", "队伍不存在或加入失败"
                            )
                            continue
                        if request_data.get("model") == "member":
                            with sock_lock:
                                windows.add_team_lineEdit.setVisible(False)
                                windows.create_team_button.setVisible(
                                    False
                                )  # 创建队伍按钮
                                windows.add_team_button.setVisible(False)
                                windows.create_team_label_prompt.setVisible(True)
                                windows.user1.combo_options.setVisible(False)
                                windows.user2.combo_options.setVisible(False)
                                windows.team_btn_start.setVisible(False)
                                windows.team_layout.addWidget(
                                    windows.team_execute_prompt
                                )

                                captain_name = request_data.get("Name")
                                captain_acc = request_data.get("Account")

                                windows.user1.lbl_name.setText(f"{captain_name}[队长]")
                                windows.user1.lbl_id.setText(f"ID:{captain_acc}")
                                """windows.user1.avatar_user_team = QPixmap(f'./image/other_user.png').scaled(100, 100,
                                                                                                     Qt.KeepAspectRatio,
                                                                                                     Qt.SmoothTransformation)
                                windows.user1.avatar_frame.setPixmap(windows.user1.avatar_user_team)"""

                                windows.user2.lbl_name.setText(
                                    f"{windows.username.text()}[我]"
                                )
                                windows.user2.lbl_id.setText(
                                    f"{windows.username.text()}"
                                )
                                windows.user2.avatar_user_team = QPixmap(
                                    "./temp/avatar.png"
                                ).scaled(
                                    100,
                                    100,
                                    Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation,
                                )
                                windows.user2.avatar_frame.setPixmap(
                                    windows.user2.avatar_user_team
                                )

                                if request_data.get("Avatar") == True:
                                    print("接收头像")
                                    # 接收图片文件大小
                                    file_size = int(self.socket.recv(1024).decode())
                                    with open(
                                        f"./temp/{captain_acc}.jpg", "wb"
                                    ) as file:
                                        total_received = 0
                                        while total_received < file_size:
                                            chunk = self.socket.recv(2048)
                                            time.sleep(0.05)
                                            if not chunk:
                                                break
                                            file.write(chunk)
                                            total_received += len(chunk)
                                    windows.user1.avatar_user_team = QPixmap(
                                        f"./temp/{captain_acc}.jpg"
                                    ).scaled(
                                        100,
                                        100,
                                        Qt.KeepAspectRatio,
                                        Qt.SmoothTransformation,
                                    )
                                    windows.user1.avatar_frame.setPixmap(
                                        windows.user1.avatar_user_team
                                    )
                                else:
                                    windows.user1.avatar_user_team = QPixmap(
                                        "./image/float/fc.png"
                                    ).scaled(
                                        100,
                                        100,
                                        Qt.KeepAspectRatio,
                                        Qt.SmoothTransformation,
                                    )
                                    windows.user1.avatar_frame.setPixmap(
                                        windows.user1.avatar_user_team
                                    )
                                print("队伍加入成功!1")
                                self.show_message_signal.emit("提示", "队伍加入成功!")
                        else:
                            windows.user1.lbl_name.setText(
                                f"{windows.username.text()}[队长][我]"
                            )
                            windows.user1.lbl_id.setText(f"{windows.userid.text()}")
                            avatar_load_status = windows.response_value("avatar_status")
                            if avatar_load_status:
                                windows.user1.avatar_user_team = QPixmap(
                                    "./temp/avatar.png"
                                ).scaled(
                                    100,
                                    100,
                                    Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation,
                                )
                                windows.user1.avatar_frame.setPixmap(
                                    windows.user1.avatar_user_team
                                )
                            else:
                                windows.user1.avatar_user_team = QPixmap(
                                    "./image/float/fc.png"
                                ).scaled(
                                    100,
                                    100,
                                    Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation,
                                )
                                windows.user1.avatar_frame.setPixmap(
                                    windows.user1.avatar_user_team
                                )
                            member_name = request_data.get("Name")
                            member_acc = request_data.get("Account")
                            windows.user2.lbl_name.setText(f"{member_name}[队员]")
                            windows.user2.lbl_id.setText(f"ID:{member_acc}")

                            if request_data.get("Avatar") == True:
                                print("接收头像")
                                # 接收图片文件大小
                                with sock_lock:
                                    file_size = int(self.socket.recv(1024).decode())
                                    with open(f"./temp/{member_acc}.jpg", "wb") as file:
                                        total_received = 0
                                        while total_received < file_size:
                                            chunk = self.socket.recv(2048)
                                            time.sleep(0.2)
                                            if not chunk:
                                                break
                                            file.write(chunk)
                                            total_received += len(chunk)
                                icon = QIcon(
                                    f"./temp/{member_acc}.jpg"
                                )  # 将此处的路径替换为实际的图像路径
                                windows.user2.avatar_user_team = QPixmap(
                                    f"./temp/{member_acc}.jpg"
                                ).scaled(
                                    100,
                                    100,
                                    Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation,
                                )
                                windows.user2.avatar_frame.setPixmap(
                                    windows.user2.avatar_user_team
                                )
                            print("队伍加入成功!2")
                            self.show_message_signal.emit("提示", "队员加入成功!")
                        print("队伍加入成功!")
                    except Exception as e:
                        print(e)
                        traceback.print_exc()

                elif request_type == "get_connect_status":
                    socket_information.put("获取成功")

                elif request_type == "team_execute":
                    self.team_send_response.emit(request_data.get("types"))
                elif request_type == "heartbeat_ack":
                    color = QColor(36, 152, 42)
                    windows.status_label.setStyleSheet(
                        f"color: {color.name()};"
                    )  # 设置字体颜色
                    windows.status_label.setText("与服务器状态: 已连接")
                elif request_type == "team_close":
                    if request_data.get("types") == "member":
                        TypedJSONClient(
                            "team_close", {"types": "member"}
                        )  # 解除成员/队长状态
                        windows.quit_team_C()
                        self.show_message_signal.emit(
                            "提示", "队长已退出队伍 队伍已关闭!"
                        )
                        # pyautogui.confirm("队长已退出队伍 队伍已关闭!", "提示")
                    else:
                        TypedJSONClient("team_close", {"types": "captain"})
                        windows.quit_team_H()
                        self.show_message_signal.emit("提示", "队员已退出队伍!")
                        # pyautogui.confirm("队员已退出队伍!", "提示")
                elif request_type == "team_handle":  # 队员发送句柄消息
                    windows.team_execute_prompt.setText(f"即将发送QQ句柄消息")
                    try:
                        windows.run_team_command("handle")
                    except Exception as e:
                        print(e)
                elif request_type == "team_at_message":  # 队员发送@消息
                    windows.team_execute_prompt.setText(f"即将发送@QQ消息")
                    windows.run_team_command("qq")
                elif request_type == "team_copy_message":  # 队员发送复制消息
                    windows.team_execute_prompt.setText(f"即将发送QQ复制消息")
                    windows.run_team_command("copy")
                elif request_type == "team_qq_update":  # QQ信息更新
                    windows.team_execute_prompt.setText(f"即将进行QQ信息更新")
                    windows.run_team_command("update")
                elif request_type == "team_auto_script":  # 自动脚本
                    windows.team_execute_prompt.setText(f"即将开始执行自动脚本")
                    windows.run_team_command("execute")
                elif request_type == "team_unknown_error":  # 未知类型错误
                    windows.team_execute_prompt.setText(f"未知类型 错误!")
                    try:
                        pyautogui.confirm("ERROR! UNKNOWN")
                    except Exception as e:
                        print(e)

                elif request_type == "repetitive_login":  # 客户端登出
                    IP = request_data.get("IP")
                    position = request_data.get("position")
                    system = request_data.get("system")
                    computer_name = request_data.get("computer_name")
                    windows.status_label.setStyleSheet(f"color: red;")  # 设置字体颜色
                    windows.status_label.setText("与服务器状态: 断开连接")
                    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    pyautogui.confirm(
                        f"{now_time} 账号已在其他客户端登录 \n来自 IP:{IP} {position} \n操作系统名称:{system} 设备名称:{computer_name}\n本客户端已与服务器断开连接 如非本人操作请尽快修改密码!"
                    )
                    windows.close()
                    os._exit(0)
                elif request_type == "server_status_check":  # 服务器状态检测
                    color = QColor(36, 152, 42)
                    windows.status_label.setStyleSheet(
                        f"color: {color.name()};"
                    )  # 设置字体颜色
                    windows.status_label.setText("与服务器状态: 已连接")

                elif request_type == "experience_bonus":
                    socket_information.put(
                        "内部激活:1000经验添加成功 重启客户端即可生效"
                    )
            except socket.timeout:  # 专门捕获超时异常
                print("与服务器连接超时，尝试重连")
                if self._handle_disconnect():
                    continue
                break
            except Exception as e:
                err_text = str(e)
                disconnect_error = (
                    "WinError" in err_text
                    or "10053" in err_text
                    or "10054" in err_text
                    or "10038" in err_text
                    or "forcibly closed" in err_text
                    or "timed out" in err_text
                )
                if disconnect_error:
                    print("与服务器断开连接，尝试重连")
                    if self._handle_disconnect():
                        continue
                    pyautogui.confirm(
                        "已与服务器断开连接 请检测网络是否连接或联系管理员获取帮助"
                    )
                    break
                if "'utf-8' codec can't decode byte" in err_text:
                    continue

                print("An error occurred:", e)
                logging.exception(
                    str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()))
                    + "错误:"
                    + str(e)
                )
                traceback.print_exc()
                break
