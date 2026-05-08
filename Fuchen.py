import time


t0 = time.perf_counter()
import logging
import os, sys, json, re, time, random, string, shutil, platform, threading, traceback
import psutil
import socket, ssl
import struct
import webbrowser
import keyboard as keys
import pyautogui
import requests
import win32com.client
import win32gui, win32api, win32con
import win32clipboard as w
import winsound
import ctypes
from ctypes import wintypes
import subprocess
import pygetwindow as gw
import function
import update_install
import SundryUI, SocketThread, new_mainpage  #
from SocketThread import socket_information

# 使用新的登录窗口类
import login_window

try:
    import op  # 计数文件
except:
    pass
from playsound3 import playsound
from PIL import Image, ImageFilter
from pypinyin import pinyin, Style  #
from collections import deque
from datetime import datetime, date
from pynput import mouse, keyboard
from pynput.keyboard import Key, Controller as KeyboardController, KeyCode
from pynput.mouse import Button, Controller as MouseController
from PyQt5.QtCore import Qt, QTimer, QUrl, QTranslator, pyqtSignal, QObject, QThread
from PyQt5.QtGui import (
    QColor,
    QIcon,
    QPixmap,
    QKeySequence,
    QDesktopServices,
    QPalette,
    QBrush,
    QImage,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QFileDialog,
    QLabel,
    QShortcut,
    QDialog,
    QGraphicsOpacityEffect,
    QInputDialog,
    QFrame,
    QSizePolicy,
)
from PyQt5 import QtCore, QtGui

print("导入库耗时:", time.perf_counter() - t0)
logging.basicConfig(filename="INFOR.log", level=logging.ERROR)


def log_exception(*args):
    # 记录异常信息到日志文件中
    logging.exception(
        str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())) + "错误:" + str(args)
    )
    print("错误:", args)


sys.excepthook = log_exception  # 日志
with open("INFOR.log", "a") as file:
    file.write(
        str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()) + "  软件运行" + "\n")
    )


class TimedStream(QObject):
    text_written = pyqtSignal(str, str)

    def __init__(self, original_stream, stream_type):
        super().__init__()
        self.original_stream = original_stream
        self.stream_type = stream_type
        self.buffer = ""
        self.history = []

    def write(self, text):
        self.buffer += text
        while "\n" in self.buffer:
            index = self.buffer.find("\n")
            line = self.buffer[:index]
            self.buffer = self.buffer[index + 1 :]
            self._process_line(line)

    def _process_line(self, line):
        """timestamp = datetime.now().strftime('[%H:%M:%S] ')
        full_line = f"{timestamp}{line}"

        self.history.append((full_line, self.stream_type))
        self.original_stream.write(f"{full_line}\n")  # 保持原始输出
        self.text_written.emit(full_line, self.stream_type)"""

        timestamp = datetime.now().strftime("[%H:%M:%S] ")
        if self.stream_type == "stderr":
            full_line = f"{timestamp}[ERROR] {line}"  # 添加错误标签
        else:
            full_line = f"{timestamp}{line}"
        self.history.append((full_line, self.stream_type))
        if self.original_stream is not None:
            self.original_stream.write(f"{full_line}\n")

        self.text_written.emit(full_line, self.stream_type)

    def flush(self):
        if self.buffer:
            self._process_line(self.buffer)
            self.buffer = ""
        # 确保原始流存在
        if self.original_stream is not None:
            self.original_stream.flush()

    def __getattr__(self, name):
        return getattr(self.original_stream, name)


# 最早初始化流重定向
stdout_stream = TimedStream(sys.stdout, "stdout")
stderr_stream = TimedStream(sys.stderr, "stderr")
sys.stdout = stdout_stream
sys.stderr = stderr_stream

function.print_fuchen()


class MyThread(threading.Thread):  # 多线程封装（我也看不懂反正就是这么用的）
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.daemon = True
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)


class ScriptRecordWorker(QObject):
    finished = pyqtSignal(bool, str, object)

    def __init__(self, file_path, wait_time, end_key_text, screen_width, screen_height):
        super().__init__()
        self.file_path = file_path
        self.wait_time = wait_time
        self.end_key_text = end_key_text
        self.screen_width = max(1, int(screen_width))
        self.screen_height = max(1, int(screen_height))

    @staticmethod
    def _resolve_end_key(end_key_text):
        end_key_map = {
            "ESC": Key.esc,
            "F8": Key.f8,
            "F9": Key.f9,
            "F10": Key.f10,
            "END": Key.end,
        }
        return end_key_map.get(end_key_text, Key.esc)

    def run(self):
        mouse_listener = None
        keyboard_listener = None
        cursor_position = None
        success = True
        error_text = ""

        try:
            time.sleep(self.wait_time)
            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")

            current_position = pyautogui.position()
            cursor_position = (current_position.x, current_position.y)
            print("开始记录自动脚本")

            records = []
            end_key = self._resolve_end_key(self.end_key_text)

            last_time = time.perf_counter()
            last_move_time = last_time
            last_move_position = None

            move_sample_ms = 12
            move_min_delta = 3

            def append_record(event_type, action, data):
                nonlocal last_time
                current_time = time.perf_counter()
                interval = max(0, int((current_time - last_time) * 1000))
                records.append([interval, event_type, action, data])
                last_time = current_time

            def normalize_position(x, y):
                return [
                    round(x / self.screen_width, 6),
                    round(y / self.screen_height, 6),
                ]

            def build_key_desc(key):
                if isinstance(key, Key):
                    vk = getattr(getattr(key, "value", None), "vk", 0)
                    return [vk if vk is not None else 0, key.name.upper()]
                if isinstance(key, KeyCode):
                    vk = key.vk if key.vk is not None else 0
                    if key.char:
                        return [vk, key.char.lower()]
                    return [vk, "NUMPAD"]
                key_char = getattr(key, "char", None)
                key_vk = getattr(key, "vk", 0)
                if key_char:
                    return [key_vk if key_vk is not None else 0, key_char.lower()]
                return [
                    key_vk if key_vk is not None else 0,
                    str(key).replace("Key.", "").upper(),
                ]

            def on_move(x, y):
                nonlocal last_move_time, last_move_position
                now = time.perf_counter()
                if (now - last_move_time) * 1000 < move_sample_ms:
                    return
                if last_move_position is not None:
                    if (
                        abs(x - last_move_position[0]) < move_min_delta
                        and abs(y - last_move_position[1]) < move_min_delta
                    ):
                        return
                rx, ry = normalize_position(x, y)
                append_record("M", "mouse move", [x, y, rx, ry])
                last_move_position = (x, y)
                last_move_time = now

            def on_click(x, y, button, pressed):
                action = ""
                if button == mouse.Button.left:
                    action = "mouse left down" if pressed else "mouse left up"
                elif button == mouse.Button.right:
                    action = "mouse right down" if pressed else "mouse right up"
                elif button == mouse.Button.middle:
                    action = "mouse middle down" if pressed else "mouse middle up"
                if action:
                    rx, ry = normalize_position(x, y)
                    append_record("M", action, [x, y, rx, ry])

            def on_scroll(x, y, dx, dy):
                append_record("M", "mouse scroll", [dx, dy])

            debounce_interval = 25
            last_key_down = {"key": None, "time": 0.0}

            def on_press(key):
                now = time.perf_counter()
                if key == end_key:
                    return False

                if (
                    key == last_key_down["key"]
                    and (now - last_key_down["time"]) * 1000 < debounce_interval
                ):
                    return

                key_desc = build_key_desc(key)
                append_record("K", "key down", key_desc)
                last_key_down["key"] = key
                last_key_down["time"] = now

            def on_release(key):
                if key == end_key:
                    return

                key_desc = build_key_desc(key)
                append_record("K", "key up", key_desc)

            mouse_listener = mouse.Listener(
                on_click=on_click, on_move=on_move, on_scroll=on_scroll
            )
            keyboard_listener = keyboard.Listener(
                on_press=on_press, on_release=on_release
            )

            mouse_listener.start()
            keyboard_listener.start()
            keyboard_listener.join()

            json_records = []
            for interval, event_type, action, data in records:
                json_record = {
                    "interval": interval,
                    "type": "keyboard" if event_type == "K" else "mouse",
                    "action": None,
                    "details": {},
                }

                if event_type == "K":
                    json_record["action"] = action.split()[-1]
                    json_record["details"] = {
                        "code": int(data[0]) if data[0] is not None else 0,
                        "name": data[1].upper()
                        if isinstance(data[1], str)
                        else str(data[1]),
                    }
                else:
                    if "move" in action:
                        json_record["action"] = "move"
                        json_record["details"] = {
                            "x": data[0],
                            "y": data[1],
                            "rx": data[2],
                            "ry": data[3],
                        }
                    elif "scroll" in action:
                        json_record["action"] = "scroll"
                        json_record["details"] = {"dx": data[0], "dy": data[1]}
                    else:
                        button = action.split()[1]
                        json_record["action"] = action.split()[-1]
                        json_record["details"] = {
                            "button": button,
                            "x": data[0],
                            "y": data[1],
                            "rx": data[2],
                            "ry": data[3],
                        }
                json_records.append(json_record)

            payload = {
                "meta": {
                    "version": 2,
                    "screen": {
                        "width": self.screen_width,
                        "height": self.screen_height,
                    },
                },
                "records": json_records,
            }

            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)

            print("记录完毕")
        except Exception:
            success = False
            error_text = traceback.format_exc()
            print(error_text)
        finally:
            if keyboard_listener is not None:
                keyboard_listener.stop()
            if mouse_listener is not None:
                mouse_listener.stop()
            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
            self.finished.emit(success, error_text, cursor_position)


class ScriptExecuteWorker(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str, object)

    def __init__(
        self,
        file_path,
        wait_time,
        count,
        speed,
        end_key_text,
        screen_width,
        screen_height,
    ):
        super().__init__()
        self.file_path = file_path
        self.wait_time = wait_time
        self.count = count
        self.speed = max(0.01, speed)
        self.end_key_text = end_key_text
        self.screen_width = max(1, int(screen_width))
        self.screen_height = max(1, int(screen_height))

    @staticmethod
    def _resolve_end_key(end_key_text):
        end_key_map = {
            "ESC": Key.esc,
            "F8": Key.f8,
            "F9": Key.f9,
            "F10": Key.f10,
            "END": Key.end,
        }
        return end_key_map.get(end_key_text, Key.esc)

    @staticmethod
    def _get_key(key_code, key_char):
        special_keys = {
            "ALT": Key.alt,
            "ALT_GR": Key.alt_gr,
            "ALT_L": Key.alt_l,
            "ALT_R": Key.alt_r,
            "BACKSPACE": Key.backspace,
            "CAPS_LOCK": Key.caps_lock,
            "CMD": Key.cmd,
            "CTRL_L": Key.ctrl_l,
            "CTRL_R": Key.ctrl_r,
            "DELETE": Key.delete,
            "DOWN": Key.down,
            "END": Key.end,
            "ENTER": Key.enter,
            "ESC": Key.esc,
            "F1": Key.f1,
            "F2": Key.f2,
            "F3": Key.f3,
            "F4": Key.f4,
            "F5": Key.f5,
            "F6": Key.f6,
            "F7": Key.f7,
            "F8": Key.f8,
            "F9": Key.f9,
            "F10": Key.f10,
            "F11": Key.f11,
            "F12": Key.f12,
            "F13": Key.f13,
            "F14": Key.f14,
            "F15": Key.f15,
            "F16": Key.f16,
            "F17": Key.f17,
            "F18": Key.f18,
            "F19": Key.f19,
            "F20": Key.f20,
            "F21": Key.f21,
            "F22": Key.f22,
            "HOME": Key.home,
            "INSERT": Key.insert,
            "LEFT": Key.left,
            "NUM_LOCK": Key.num_lock,
            "PAGE_DOWN": Key.page_down,
            "PAGE_UP": Key.page_up,
            "RIGHT": Key.right,
            "SCROLL_LOCK": Key.scroll_lock,
            "SHIFT": Key.shift,
            "SHIFT_R": Key.shift_r,
            "SPACE": Key.space,
            "TAB": Key.tab,
            "UP": Key.up,
            "PRINT_SCREEN": Key.print_screen,
            "MENU": Key.menu,
        }
        key_char = key_char or ""
        key_upper = key_char.upper()
        if key_upper in special_keys:
            return special_keys[key_upper]
        if "NUMPAD" in key_upper or key_code in range(96, 106) or key_code == 110:
            numpad_keys = {
                96: KeyCode(vk=96),
                97: KeyCode(vk=97),
                98: KeyCode(vk=98),
                99: KeyCode(vk=99),
                100: KeyCode(vk=100),
                101: KeyCode(vk=101),
                102: KeyCode(vk=102),
                103: KeyCode(vk=103),
                104: KeyCode(vk=104),
                105: KeyCode(vk=105),
                110: KeyCode(vk=110),
            }
            if key_code in numpad_keys:
                return numpad_keys[key_code]
        if len(key_char) == 1:
            return KeyCode(char=key_char)
        if key_code is not None:
            return KeyCode(vk=key_code)
        raise ValueError(f"无法识别的按键: code={key_code}, char={key_char}")

    def _scale_position(self, x, y, record_screen):
        if x is None or y is None:
            return None, None
        record_width = record_screen.get("width", 0)
        record_height = record_screen.get("height", 0)
        if record_width > 0 and record_height > 0:
            x = int(round(x * self.screen_width / record_width))
            y = int(round(y * self.screen_height / record_height))
        x = max(0, min(self.screen_width - 1, int(x)))
        y = max(0, min(self.screen_height - 1, int(y)))
        return x, y

    def _resolve_position(self, data, record_screen):
        x, y, rx, ry = data
        if rx is not None and ry is not None:
            x = int(round(rx * self.screen_width))
            y = int(round(ry * self.screen_height))
            x = max(0, min(self.screen_width - 1, int(x)))
            y = max(0, min(self.screen_height - 1, int(y)))
            return x, y
        return self._scale_position(x, y, record_screen)

    def run(self):
        listener = None
        original_pause = pyautogui.PAUSE
        stop_event = threading.Event()
        cursor_position = None
        success = True
        error_text = ""
        start_time = time.time()

        try:
            end_key = self._resolve_end_key(self.end_key_text)

            def key_listener():
                nonlocal listener

                def on_press(key):
                    try:
                        if key == end_key:
                            stop_event.set()
                            print(f"检测到 {self.end_key_text}，脚本终止中...")
                            return False
                    except Exception as e:
                        print(f"按键监听异常: {e}")

                listener = keyboard.Listener(on_press=on_press)
                listener.start()
                listener.join()

            listener_thread = threading.Thread(target=key_listener, daemon=True)
            listener_thread.start()

            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
            current_position = pyautogui.position()
            cursor_position = (current_position.x, current_position.y)
            time.sleep(self.wait_time)

            mouse_controller = MouseController()
            keyboard_controller = KeyboardController()

            def wait_with_stop(milliseconds):
                delay = max(0, milliseconds) / 1000.0
                return stop_event.wait(delay)

            pyautogui.PAUSE = 0

            with open(self.file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)

            if isinstance(raw_data, dict):
                json_records = raw_data.get("records", [])
                record_screen = raw_data.get("meta", {}).get("screen", {})
            elif isinstance(raw_data, list):
                json_records = raw_data
                record_screen = {}
            else:
                raise ValueError("脚本文件格式错误")

            records = []
            for json_record in json_records:
                event_type = json_record.get("type")
                action = json_record.get("action")
                interval = int(json_record.get("interval", 0))
                details = json_record.get("details", {})

                if event_type == "keyboard":
                    key_name = details.get("name", "")
                    key_code = details.get("code", 0)
                    try:
                        key_code = int(key_code)
                    except (TypeError, ValueError):
                        key_code = 0
                    record = [
                        interval,
                        "K",
                        f"key {action}",
                        [
                            key_code,
                            key_name.lower()
                            if isinstance(key_name, str)
                            else str(key_name),
                        ],
                    ]
                    records.append(record)
                    continue

                if event_type != "mouse":
                    continue

                if action == "move":
                    record = [
                        interval,
                        "M",
                        "mouse move",
                        [
                            details.get("x"),
                            details.get("y"),
                            details.get("rx"),
                            details.get("ry"),
                        ],
                    ]
                elif action == "scroll":
                    record = [
                        interval,
                        "M",
                        "mouse scroll",
                        [details.get("dx", 0), details.get("dy", 0)],
                    ]
                else:
                    button = details.get("button", "left")
                    record = [
                        interval,
                        "M",
                        f"mouse {button} {action}",
                        [
                            details.get("x"),
                            details.get("y"),
                            details.get("rx"),
                            details.get("ry"),
                        ],
                    ]
                records.append(record)

            for record in records:
                record[0] = int(record[0] / self.speed)

            for i in range(self.count):
                if stop_event.is_set():
                    break

                for record in records:
                    if stop_event.is_set():
                        print("脚本执行已终止。")
                        break

                    if wait_with_stop(record[0]):
                        print("脚本执行已终止。")
                        break

                    if record[1] == "M":
                        if "mouse move" in record[2]:
                            x, y = self._resolve_position(record[3], record_screen)
                            if x is None or y is None:
                                continue
                            mouse_controller.position = (x, y)
                        elif "mouse left down" in record[2]:
                            x, y = self._resolve_position(record[3], record_screen)
                            if x is None or y is None:
                                continue
                            mouse_controller.position = (x, y)
                            mouse_controller.press(Button.left)
                        elif "mouse left up" in record[2]:
                            x, y = self._resolve_position(record[3], record_screen)
                            if x is None or y is None:
                                continue
                            mouse_controller.position = (x, y)
                            mouse_controller.release(Button.left)
                        elif "mouse right down" in record[2]:
                            x, y = self._resolve_position(record[3], record_screen)
                            if x is None or y is None:
                                continue
                            mouse_controller.position = (x, y)
                            mouse_controller.press(Button.right)
                        elif "mouse right up" in record[2]:
                            x, y = self._resolve_position(record[3], record_screen)
                            if x is None or y is None:
                                continue
                            mouse_controller.position = (x, y)
                            mouse_controller.release(Button.right)
                        elif "mouse middle down" in record[2]:
                            x, y = self._resolve_position(record[3], record_screen)
                            if x is None or y is None:
                                continue
                            mouse_controller.position = (x, y)
                            mouse_controller.press(Button.middle)
                        elif "mouse middle up" in record[2]:
                            x, y = self._resolve_position(record[3], record_screen)
                            if x is None or y is None:
                                continue
                            mouse_controller.position = (x, y)
                            mouse_controller.release(Button.middle)
                        elif "mouse scroll" in record[2]:
                            dx, dy = record[3]
                            mouse_controller.scroll(dx, dy)
                    elif record[1] == "K":
                        key_code, key_char = record[3]
                        key = self._get_key(key_code, key_char)
                        if "down" in record[2]:
                            keyboard_controller.press(key)
                        elif "up" in record[2]:
                            keyboard_controller.release(key)

                self.progress.emit(i + 1)

            end_time = time.time()
            print(f"实际执行时间:{(end_time - start_time):.2f}秒")
        except Exception:
            success = False
            error_text = traceback.format_exc()
            print(error_text)
        finally:
            if listener is not None:
                listener.stop()
            pyautogui.PAUSE = original_pause
            self.finished.emit(success, error_text, cursor_position)


def play_prompt_sound(file_path):
    global Sound
    try:
        if Sound:
            MyThread(playsound, file_path)
            # winsound.PlaySound(file_path, winsound.SND_FILENAME)
    except Exception as e:
        logging.exception(
            str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()))
            + "错误:"
            + str(e)
        )


def play_warning_sound():
    # 设置警告音频文件路径
    try:
        sound_file = "C:\\Windows\\Media\\Windows Foreground.wav"
        winsound.PlaySound(sound_file, winsound.SND_FILENAME)
    except Exception as e:
        logging.exception(
            str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()))
            + "错误:"
            + str(e)
        )


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 创建 SSL 上下文（客户端模式）
context = ssl.create_default_context()

# 如果你使用的是自签名证书，需要加载服务器证书用于验证（可选，建议）
context.load_verify_locations("certificate.pem")

s = context.wrap_socket(s, server_hostname="fcyang.cn")


def set_variables(vars_dict, namespace=None):
    """
    通过变量名字符串动态修改指定命名空间中的变量值
    :param vars_dict: 字典格式 {变量名: 新值}
    :param namespace: 命名空间字典，默认使用全局作用域
    """
    namespace = namespace or globals()
    assignments = "; ".join([f"{k} = {repr(v)}" for k, v in vars_dict.items()])
    exec(assignments, namespace)


def TypedJSONClient(msg_type, payload):
    data = {"type": msg_type, "data": payload}
    # 发送请求
    json_data = json.dumps(data).encode("utf-8")
    header = struct.pack(">I", len(json_data))
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


function.initialization()

with open("config.json", "r") as file:
    config = json.load(file)
AutoLogin = config.get("AutoLogin", False)
remember = config.get("Remember", False)
Account = config.get("Account", "") if remember else ""
Password = config.get("Password", "") if remember else ""
position_status = config["position"] != [[None, None], [None, None]]
initial = config.get("Initial", True)
positions = config.get("position", [[None, None], [None, None]])
textedit_position = positions[0]
send_position = positions[1]
del positions

Click_Times_ = 1000
Click_Pauses = 0.1
Random_list = [1, 2, 3]
handle_position = [30, -60]
Click_Pause = 0.01
res = False
Version = "V1.81"


try:
    # 获取数据文本
    url = "https://fcyang.cn/data.txt"
    response = requests.get(url, proxies={"http": None, "https": None})
    data = response.text

    # 解析键值对
    config = {}
    for line in data.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            config[key.strip()] = value.strip()

    # 提取目标字段
    formal_version = config.get("formal_version")
    formal_link = config.get("formal_link")
except:
    traceback.print_exc()
    formal_version = "V1.0.0"

Number_People = "加载中..."

IP = "fcyang.cn"  # IP地址192.168.2.75 47.116.75.93
Port = 30000  # 端口号
information = "正在加载公告..."
sys_list = []  # 控制台内容列表
exp_status = None
avatar_load_status = False  # 头像加载
connect_status = None
Fuchen_name, Fuchen_type, Fuchen_fullname = function.get_exefile_name()
Name = None
mode = None
avatar_date = None
exp = None
access_token = None
refresh_token = None
print("配置加载成功")
try:  # 连接服务器
    s.settimeout(10)
    s.connect((IP, Port))
    connect_status = True
except Exception as e:
    traceback.print_exc()
    logging.exception(
        str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())) + "错误:" + str(e)
    )
    pyautogui.confirm("服务器连接失败\n请留意服务器公告查询最新消息\n")

try:  # 处理信息\公告
    if connect_status == None:
        raise Exception()
    time.sleep(0.1)

    TypedJSONClient("Get Notice", "None")
    request = recv_json(s)
    request_data = request.get("data")
    Server_Version = request_data.get("Version")
    Number_People = request_data.get("Number")
    link = request_data.get("Link")
    information = request_data.get("Notice")
    try:
        status = request_data.get("status")
        if status == "Fuchen Maintenance":
            pyautogui.confirm("服务器正在维护 请稍后")
            sys.exit()
    except:
        pass

    try:
        information = re.sub("~~space~~", " ", information)
        information = re.sub("~~next~~", "\n", information)
        print(
            f""
            f"--------------------------------------------------------------------------\n"
            f"更新日志:\n"
            f"{information}\n"
            f"--------------------------------------------------------------------------"
        )
    except Exception as e:
        logging.exception(
            str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()))
            + "错误:"
            + str(e)
        )
except Exception as e:
    traceback.print_exc()
    logging.exception(
        str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())) + "错误:" + str(e)
    )
    if connect_status != None:  # 服务器连接成功 但数据接收失败
        pyautogui.confirm(
            "数据接收失败 请重新启动软件\n如多次重试失败 请尝试更新到最新版客户端"
        )
        os._exit(0)
    else:  # 服务器连接失败 以离线模式启动
        result = pyautogui.confirm("服务器连接失败 是否以离线模式启动?")
        if result == "OK":
            formal_version = Version
            information = (
                "当前是离线模式 \n部分状态可能未正常显示\n部分功能可能无法正常使用"
            )
        else:
            sys.exit()

if function.parse_version(Version) < function.parse_version(formal_version):
    try:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        update_window = update_install.show_update_dialog(["", Version, formal_version])
        if update_window == "update_successful":
            # 创建快捷方式
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_name = f"Fuchen.lnk"
            shortcut_path = os.path.join(desktop_path, shortcut_name)
            back_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
            new_version_path = os.path.join(back_path, f"Fuchen_{formal_version}")

            new_exe_path = rf"{new_version_path}\{Fuchen_name}.exe"

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = new_exe_path
            shortcut.WorkingDirectory = os.path.dirname(
                new_exe_path
            )  # 设置快捷方式的起始位置为exe文件所在的文件夹
            shortcut.save()

            def copy_scripts_safe(src_folder, dst_folder):
                os.makedirs(dst_folder, exist_ok=True)
                for item in os.listdir(src_folder):
                    s = os.path.join(src_folder, item)
                    d = os.path.join(dst_folder, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)

            try:
                # 迁移旧版数据
                copy_scripts_safe("./scripts", rf"{new_version_path}\scripts")
                copy_scripts_safe("./mod/music", rf"{new_version_path}\mod\music")
                copy_scripts_safe("./mod/picture", rf"{new_version_path}\mod\picture")
                copy_scripts_safe("./mod/xlsx", rf"{new_version_path}\mod\xlsx")

            except Exception as e:
                pass

            with open(f"{new_version_path}\\Fuchen.tmp", "w") as f:
                f.write(f"{os.getcwd()}")
            OLD_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
            function.new_update(new_exe_path, OLD_DIR, shortcut_path)
            sys.exit()
        elif update_window == "cancel_update":
            sys.exit()
        else:
            sys.exit()
        os._exit(0)
    except Exception as e:
        traceback.print_exc()
        logging.exception(
            str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()))
            + "错误:"
            + str(e)
        )
        print(f"{str(e)}")
        sys.exit()


def check_process_exists(process_name):
    for process in psutil.process_iter(attrs=["pid", "name"]):
        if process.info["name"] == process_name:
            return True
    return False


try:
    res = requests.get("http://myip.ipip.net", timeout=5).text
    # 提取城市信息
    split_res = res.split("  ")
    city_info = split_res[-2]  # 倒数第二个元素是城市信息
    city_info = city_info.split(" ")
    city_name = city_info[-1]
    # city_name = city_info[-2]+city_info[-1]+(split_res[-1].replace('\n',''))
    # city_name = city_info
    # del city_info
except Exception as e:
    city_name = "Unknown"
    city_info = ["中国", "Unknown", "Unknown"]
    logging.exception(
        str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())) + "错误:" + str(e)
    )

system = platform.system()  # 系统类型
computer_name = platform.node()  # 计算机网络名称
APP_VERSION = 0x2023ABCD
# Windows API 常量
WM_SYSCOMMAND = 0x0112
SC_MINIMIZE = 0xF020
SC_RESTORE = 0xF120


# 在类定义前添加共享内存结构体定义
class SharedParams(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("version", ctypes.c_int),
        ("hotkey", ctypes.c_int),
        ("interval", ctypes.c_double),
        ("clickType", ctypes.c_int),
    ]


class Ui_Form(new_mainpage.MainWindow):  # 主窗口
    trigger_click_record_signal = pyqtSignal()
    trigger_click_execute_signal = pyqtSignal()
    _tourist_prompt_signal = pyqtSignal()

    def __init__(self, stdout_stream, stderr_stream):
        super(Ui_Form, self).__init__()
        self.stdout_stream = stdout_stream
        self.stderr_stream = stderr_stream
        self.setStyleSheet("""QDialog {
                background-color: #ffffff;
                border-radius: 8px;
                font-size: 16px;
                color: #333333;
                padding: 4px;
            }""")

        self.open_status = False
        self.c_thread_object = None
        self.first_image = False
        self._is_maximized = False  # 跟踪最大化状态
        self.record_status = False
        self.execute_status = False
        self.number_prompt_window = None
        if Theme == "White":
            self.should_draw = "White"
        elif Theme == "Custom":
            self.should_draw = "Custom"
        else:
            self.should_draw = "White"
        self.window_icon = (
            False  # 右下角图标存在或不存在 布尔值 存在为True不存在为False
        )
        self.setupUi(self)
        self.trigger_click_record_signal.connect(self.Click_Record)
        self.trigger_click_execute_signal.connect(self.Click_Record_execute)
        self._tourist_prompt_signal.connect(self._on_tourist_prompt)
        self.apply_hotkey_bindings()
        self.title_bar.Button_SetTop.clicked.connect(self.upwindow)
        self.title_bar.Button_Close.clicked.connect(self.clo)  # 退出按钮

        self.open_window_hotkey = QShortcut(QKeySequence("Ctrl+o"), self)
        self.open_window_hotkey.activated.connect(self.open_console_window)

        self.open_window_hotkey = QShortcut(QKeySequence("F12"), self)
        self.open_window_hotkey.activated.connect(self.open_console_window)

        self.title_bar.console_action.triggered.connect(self.open_console_window)

        # self.title_bar.action_option1.triggered.connect(self.open_set_window)  # 设置按钮
        self.title_bar.action_option2.triggered.connect(self.about)
        self.title_bar.action_option3.triggered.connect(self.open_help_window)
        self.title_bar.action_option4.triggered.connect(self.LogRecord)
        self.title_bar.action_option5.triggered.connect(self.open_website)
        self.title_bar.action_option6.triggered.connect(self.open_view_window)
        self.title_bar.action_option7.triggered.connect(self.empyt_log)
        self.title_bar.action_option8.triggered.connect(self.clear_temp)
        self.title_bar.action_option9.triggered.connect(self.restart_app)
        self.title_bar.action_option10.triggered.connect(self.open_website_help)
        self.title_bar.action_option11.triggered.connect(self.opensource_link)

        self.avatar.clicked.connect(self.open_user_window)
        self.username.clicked.connect(self.open_user_window)
        self.userid.clicked.connect(self.open_user_window)

        self.RClick_Radio.clicked.connect(self.update_shared_params)
        self.MClick_Radio.clicked.connect(self.update_shared_params)
        self.LClick_Radio.clicked.connect(self.update_shared_params)
        self._3D.valueChanged.connect(self.update_shared_params)
        self._3pushButton_6.clicked.connect(lambda: MyThread(self.open_click))
        self._3pushButton_7.clicked.connect(lambda: MyThread(self.break_click))

        self._3pushButton_4.setMenu(self.createMenu())
        self.weather_label.setCursor(Qt.PointingHandCursor)  # 鼠标变手型
        self.weather_label.mousePressEvent = self.change_city_name  # 绑定点击事件

        self.config_editor_button.clicked.connect(self.open_fileedit_window)
        self.show_count_checkbox.stateChanged.connect(self.open_number_prompt_window)
        # self._3spinBox_3.valueChanged.connect(self.number_total_changed)
        self.color_change_button.clicked.connect(self.number_prompt_window_color)
        # self._3pushButton.clicked.connect(self.Click_Record)  # 记录自动脚本
        # self._3pushButton_2.clicked.connect(self.Click_Record_execute)

        # ----消息发送控件----#
        self.old_QQ.toggled.connect(lambda checked: self.QQ_change("old"))
        self.new_QQ.toggled.connect(lambda checked: self.QQ_change("new"))
        self._2pushButton2.clicked.connect(self.gain_handle)
        self.handle_send_btn.clicked.connect(self.Handle_Send)

        self.QQ_StartSend_At_Button.clicked.connect(self.Send_QQ)  # page2(QQ)页面 绑定
        self.QQ_Send_Copy_startsend_button.clicked.connect(self.Send_Copy)  # 复制内容
        self.QQ_Seq_Start_button.clicked.connect(self.order_send)
        self.record_position_button.clicked.connect(self.open_record_window)

        self.btn_custom_start.clicked.connect(self.handle_auto_execute)
        self.btn_get_position.clicked.connect(self.start_detection)
        # ----team---#
        self.create_team_button.clicked.connect(self.team)  # 创建队伍

        self.button_copy_id.clicked.connect(self.copy_team_number)  # 复制id
        self.add_team_button.clicked.connect(self.join_team)

        self.team_btn_start.clicked.connect(self.team_c)  # 开始执行
        # ----工具页面----#

        self.view_music.clicked.connect(lambda: self.open_folder("music"))
        self.btn_download_music.clicked.connect(self.download)

        self.pic_confirm_button.clicked.connect(self.mixPicture)

        self.btn_download_qq.clicked.connect(lambda: MyThread(self.download_image))
        self.qq_information_edit_button.clicked.connect(self.QQ_image_update)
        self.save_setting_btn.clicked.connect(self.save_setting_option)

        self.btn_get_group.clicked.connect(lambda: MyThread(self.QQ_Group_information))

        # ----设置页面----#

        self.version_button.clicked.connect(self.check_update)
        self.update_status_button.clicked.connect(self.get_connect_status)

        """
        self.uim.Start_Click_Radio.clicked.connect(lambda: self.record_change('click'))
        self.uim.Start_Hotkey_Radio.clicked.connect(lambda: self.record_change('hotkey'))
        self.uim.Hotkey_record_button.clicked.connect(self.record_hotkey_setting)

        self.uim.Execute_Click_Radio.clicked.connect(lambda: self.execute_change('click'))
        self.uim.Execute_Hotkey_Radio.clicked.connect(lambda: self.execute_change('hotkey'))
        self.uim.Hotkey_execute_button.clicked.connect(self.execute_hotkey_setting)

        self.uim._3pushButton_5.clicked.connect(self.mouseinfo)

        
        self.uim.reflash.clicked.connect(lambda: self.uim.populateMenu('scripts'))


        self.uim.talk_lineEdit.returnPressed.connect(self.send_talk)

        """

        self.image_cache = deque(maxlen=30)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.is_topmost = False
        self.border_width = 8
        self.record_thread = None
        self.execute_thread = None
        self.record_worker = None
        self.execute_worker = None

        self.hotkey_record_status = None
        self.hotkey_execute_status = None

        MainWindow.setWindowTitle("Fuchen 浮沉制作")

        icon = QIcon("image/window.ico")  # 设置窗口图标
        self.setWindowIcon(icon)

        MyThread(self.Update_weather)
        MyThread(self.tourist_prompt)
        MyThread(self.setting_page_check)

        self.weather_timer = QtCore.QTimer(self)
        self.weather_timer.timeout.connect(self.Update_weather)
        self.weather_timer.start(1200000)  # 更新时间的间隔，单位为毫秒

        self.run_timer = QtCore.QTimer(self)
        self.run_timer.timeout.connect(self.updateTime)
        self.startTime = QtCore.QTime.currentTime()
        self.run_timer.start(1000)  # 每秒更新一次

        self.global_timer = QtCore.QTimer(self)
        self.global_timer.timeout.connect(self.get_current_time_string)
        self.global_timer.start(1000)  # 更新时间的间隔，单位为毫秒

        # self.data_thread = DataThread()
        self.data_thread = SocketThread.DataThread([self, s])
        self.data_thread.show_message_signal.connect(self.handle_message)
        self.data_thread.team_send_response.connect(self.deal_team_send)
        self.data_thread.team_state_needs_reset.connect(self.reset_team_ui)
        self.data_thread.start()

        # 将文本分割成行
        global information
        lines = information.split("\n")

        # 生成HTML内容
        html_content = f"""
        <p style='color: rgba(255,255,255,0.95); margin:2px;'>
            <b>📢{lines[0]}</b><br/>
            {"".join([f"· {line}<br/>" for line in lines[1:]])}
            <a href='https://fcyang.cn/others/log.html' 
           style='color: #ffdd55; text-decoration: none;'>[详情]</a>
        </p>
        """
        self.notice_browser.setHtml(html_content)

    def setting_page_check(self):
        if Account == "游客":
            self.avatar.setEnabled(False)
            self.username.setEnabled(False)
            self.userid.setEnabled(False)
            self.button_3.setEnabled(False)
            self.avatar.setToolTip("游客暂不支持该功能")
            self.username.setToolTip("游客暂不支持该功能")
            self.userid.setToolTip("游客暂不支持该功能")
            self.button_3.setToolTip("游客暂不支持该功能")

        if AutoLogin == True:
            self.auto_login_check.setChecked(True)
        else:
            self.auto_login_check.setChecked(False)
        if Sound == True:
            self.sound_check.setChecked(True)
        else:
            self.sound_check.setChecked(False)
        if ClosePrompt == True:
            self.close_check.setChecked(True)
        else:
            self.close_check.setChecked(False)
        if CloseExecute == "Close":
            self.close_radio.setChecked(True)
        elif CloseExecute == "Hide":
            self.tray_radio.setChecked(True)
        else:
            self.close_radio.setChecked(False)
            self.tray_radio.setChecked(False)
        # 要检查的文件名
        file_name = "Fuchen_Start_File.bat"
        startup_folder = os.path.join(
            os.getenv("APPDATA"),
            "Microsoft",
            "Windows",
            "Start Menu",
            "Programs",
            "Startup",
        )
        file_path = os.path.join(startup_folder, file_name)
        self.First = False
        if os.path.exists(file_path):
            self.boot_check.setChecked(True)
            self.First = True
        else:
            self.boot_check.setChecked(False)
        if window_s == True:
            self.float_check.setChecked(True)
        else:
            self.float_check.setChecked(False)
        if Theme == "White":
            self.bg_default.setChecked(True)
        elif Theme == "Custom":
            try:
                self.bg_custom.setChecked(True)
                with open("config.json", "r") as file:  # 填充自定义图片壁纸的输入栏
                    config = json.load(file)
                # 添加新元素到数据结构
                Path_Custom = config["Path"]
                self.bg_custom_path.setText(Path_Custom)
            except Exception as e:
                print(e)
        else:
            self.bg_default.setChecked(True)
        self.opacity_slider.setValue(transparent)

    def open_number_prompt_window(self, state):
        if state == Qt.Checked:
            self.number_prompt_window = ui.number_prompt.NotificationWindow()
            self.number_prompt_window.show()
            self.color_change_button.setVisible(True)
        else:
            self.number_prompt_window = ui.number_prompt.NotificationWindow()
            self.number_prompt_window.close()
            self.color_change_button.setVisible(False)

    def handle_number_window(self, type, now, total):
        if self.number_prompt_window != None:
            self.number_prompt_window.update_operation(type)
            self.number_prompt_window.update_now_number(now)
            self.number_prompt_window.update_total_number(total)
        pass

    def number_prompt_window_color(self):
        if self.number_prompt_window != None:
            self.number_prompt_window.update_color()

    def number_now_changed(self, value):
        if self.number_prompt_window != None:
            self.number_prompt_window.update_now_number(value)

    def number_total_changed(self, value):
        if self.number_prompt_window != None:
            self.number_prompt_window.update_total_number(value)

    def save_setting_option(self):
        global \
            AutoLogin, \
            Sound, \
            ClosePrompt, \
            CloseExecute, \
            window_s, \
            Theme, \
            transparent, \
            FPS

        if self.auto_login_check.isChecked():
            AutoLogin = True
        else:
            AutoLogin = False
        if self.sound_check.isChecked():
            Sound = True
        else:
            Sound = False
        if self.close_check.isChecked():
            ClosePrompt = True
        else:
            ClosePrompt = False
        if self.close_radio.isChecked():
            CloseExecute = "Close"
        else:
            CloseExecute = "Hide"
        with open("config.json", "r") as file:
            config = json.load(file)
        transparent = self.opacity_slider.value()
        config["AutoLogin"] = AutoLogin
        config["Sound"] = Sound
        config["ClosePrompt"] = ClosePrompt
        config["CloseExecute"] = CloseExecute
        config["transparent"] = transparent
        # 将更新后的数据写入 JSON 文件
        with open("config.json", "w") as file:
            json.dump(config, file, indent=4)
        n = True
        if (self.boot_check.isChecked()) and (self.First == False):
            try:
                exe_file_name = "Fuchen.exe"
                startup_folder = os.path.join(
                    os.getenv("APPDATA"),
                    "Microsoft",
                    "Windows",
                    "Start Menu",
                    "Programs",
                    "Startup",
                )
                bat_file_path = os.path.join(startup_folder, "Fuchen_Start_File.bat")

                with open(bat_file_path, "w") as file:
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
                    file.write(f'cd /d "{parent_dir}"\n')
                    file.write(f"start {exe_file_name}")

                print(f"成功创建并写入.bat文件到启动文件夹: {bat_file_path}")
                self.First = True
            except Exception as e:
                pyautogui.confirm(e)
        elif (self.boot_check.isChecked() == False) and (self.First == True):
            try:
                # 要移除的文件名
                file_name = "Fuchen_Start_File.bat"
                startup_folder = os.path.join(
                    os.getenv("APPDATA"),
                    "Microsoft",
                    "Windows",
                    "Start Menu",
                    "Programs",
                    "Startup",
                )
                file_path = os.path.join(startup_folder, file_name)

                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"{file_name} 已从启动文件夹中移除")
                else:
                    print(f"{file_name} 不存在于启动文件夹中")
                self.First = False
            except Exception as e:
                pyautogui.confirm(e)
        if self.float_check.isChecked() and window_s == False:
            self.open_floating_window()
            window_s = True
        elif self.float_check.isChecked() == False and window_s == True:
            self.close_floating_window()
            window_s = False
        self.repaint()
        if self.bg_default.isChecked():
            self.should_draw = "White"  # 清空背景图片
            self.sidebar.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1))
            self.stack.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1))
            # 重置调色板为默认（例如白色主题）
            default_palette = QApplication.palette()
            self.setPalette(default_palette)
            # 读取 JSON 文件
            with open("config.json", "r") as file:
                config = json.load(file)
            config["Theme"] = "White"
            # 将更新后的数据写入 JSON 文件
            with open("config.json", "w") as file:
                json.dump(config, file, indent=4)
            Theme = "White"

        if self.bg_custom.isChecked():
            try:
                file_name = self.bg_custom_path.text()
                with open("config.json", "r") as file:
                    config = json.load(file)
                if (
                    config["Theme"] != "Custom" or config["Path"] != file_name
                ):  # 这个判断是为了防止目前的背景和选择的背景相同而设置 因此当选择的文件和现有设置的文件相同时 将不会执行
                    if file_name != "":
                        self.should_draw = "Custom"
                        # 读取 JSON 文件
                        with open("config.json", "r") as file:
                            config = json.load(file)
                        config["Theme"] = "Custom"
                        config["Path"] = file_name
                        # 将更新后的数据写入 JSON 文件
                        with open("config.json", "w") as file:
                            json.dump(config, file, indent=4)
                        im = Image.open(file_name)
                        reim = im.resize((1000, 600))  # 宽*高
                        reim.save(
                            "./temp/background_custom.png", dpi=(400, 400)
                        )  ##200.0,200.0分别为想要设定的dpi值
                        # 打开图片
                        image = Image.open("./temp/background_custom.png")
                        # 应用高斯模糊，radius参数控制模糊程度（半径越大越模糊）
                        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=5))
                        # 保存处理后的图片
                        blurred_image.save("./temp/background_custom.png")

                        palette = QPalette()
                        palette.setBrush(
                            QPalette.Background,
                            QBrush(QPixmap("./temp/background_custom.png")),
                        )
                        self.setPalette(palette)
                        self.repaint()
                        self.update()  # 新增此行

                        Theme = "Custom"

                    else:
                        n = False
                        pyautogui.confirm("请选择文件!")
                trp = transparent / 100
                # 设置整体透明度（会影响所有子元素）
                self.sidebar.setGraphicsEffect(QGraphicsOpacityEffect(opacity=trp))
                self.stack.setGraphicsEffect(QGraphicsOpacityEffect(opacity=trp - 0.1))
            except Exception as e:
                print(e)

        if n == True:
            pyautogui.confirm("设置成功!")

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def tourist_prompt(self):
        if Account == "游客":
            try:
                with open("config.json", "r") as f:
                    config = json.load(f)
                config["tourist_number"] += 1
                with open("config.json", "w") as f:
                    json.dump(config, f, indent=4)

                with open("config.json") as f:
                    config = json.load(f)

                tourist_status = config["tourist_status"]
                tourist_number = config["tourist_number"]

                if not tourist_status and tourist_number in (5, 20, 100):
                    time.sleep(random.randint(5, 15))
                    self._tourist_prompt_signal.emit()
            except:
                pass
        else:
            try:
                # 读取 JSON 文件
                with open("config.json", "r") as f:
                    config = json.load(f)

                # 修改数值（确保原值是整数）
                config["tourist_status"] = True

                # 重新写入文件（覆盖原文件）
                with open("config.json", "w") as f:
                    json.dump(config, f, indent=4)  # indent 保持美观格式
            except:
                pass

    def _on_tourist_prompt(self):
        with open("config.json") as f:
            config = json.load(f)
        tourist_number = config.get("tourist_number", 0)

        reply = QMessageBox.question(
            self,
            "提示",
            f"您已启动Fuchen {tourist_number} 次\n注册账号可以使用更全面的功能\n是否立即注册？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )
        if reply == QMessageBox.Yes:
            from ui.RegisterWindow import Register
            register_dialog = Register(s)
            register_dialog.exec_()
            if (register_dialog.result_value and
                    register_dialog.result_value[0] == "注册成功"):
                reply2 = QMessageBox.question(
                    self,
                    "注册成功",
                    "注册成功！是否立即重新启动软件并使用新账号登录？",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes,
                )
                if reply2 == QMessageBox.Yes:
                    self.restart_app()

    def get_current_time_string(self):
        global current_time_string
        current_time = time.localtime()  # 获取当前时间的时间结构
        current_time_string = (
            "[" + time.strftime("%H:%M:%S", current_time) + "]"
        )  # 格式化时间为字符串

    def restart_app(self):
        subprocess.Popen([Fuchen_fullname])
        self.close()
        os._exit(0)

    def get_update(self):
        result = function.get_update_data(Version)
        if type(result) == str:
            pyautogui.confirm(result)
            return 0
        else:
            if result[0] == None or result[1] == None:
                pyautogui.confirm("版本信息获取失败 请重试")
                return 0
            else:
                if result[1] == False:
                    pyautogui.confirm(result[0])
                else:
                    usru = pyautogui.confirm(result[0])
                    if usru == "OK":
                        webbrowser.open(result[2])

    def updateTime(self):
        currentTime = QtCore.QTime.currentTime()
        elapsedTime = self.startTime.secsTo(currentTime)

    def QQ_change(self, checked):  # 句柄发送位置切换
        global handle_position
        if checked == "old":
            handle_position = [30, -60]
        else:
            handle_position = [-30, -60]

    def get_connect_status(self):
        TypedJSONClient("get_connect_status", "N")
        try:
            color = QColor(36, 152, 42)
            self.status_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
            self.status_label.setText("与服务器状态: 已连接")
            result = socket_information.get(timeout=3)
            print(result)
        except:
            traceback.print_exc()
            print("与服务器断开连接")
            color = QColor(164, 38, 15)  # 使用RGB值设置颜色为红色
            self.status_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
            self.status_label.setText("与服务器状态: 断开连接")

    def response_value(self, value):
        # 通过全局变量字典获取
        param = globals()[value]
        return param

    def update_auth_tokens(self, new_access_token=None, new_refresh_token=None):
        global access_token, refresh_token
        access_token = new_access_token
        refresh_token = new_refresh_token

    def on_socket_reconnected(self, new_socket):
        global s
        s = new_socket
        new_mainpage.s = new_socket

    def clear_temp(self):
        # global Theme
        total_size = 0
        for dirpath, dirnames, filenames in os.walk("./temp"):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        if total_size != 0:
            total_size = float(total_size / 1024)
            if total_size < 1024:
                result = QMessageBox.question(
                    self,
                    "Fuchen",
                    f"缓存内容大小为:{round(total_size, 2)}KB\n清理缓存不影响正常使用 是否进行清除?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
                if result == QMessageBox.Yes:
                    shutil.rmtree("./temp")
                    # 重新创建空文件夹
                    os.mkdir("./temp")
                    pyautogui.confirm("缓存清除成功!")
            else:
                total_size = float(total_size / 1024)
                result = QMessageBox.question(
                    self,
                    "Fuchen",
                    f"缓存内容大小为:{round(total_size, 2)}MB\n清理缓存不影响正常使用 是否进行清除?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
                if result == QMessageBox.Yes:
                    shutil.rmtree("./temp")
                    # 重新创建空文件夹
                    os.mkdir("./temp")
                    pyautogui.confirm("缓存清除成功!")
        else:
            self.show_message_box("Fuchen", f"暂无缓存内容")

    def setValue(self, Set):
        global \
            AutoLogin, \
            Sound, \
            ClosePrompt, \
            CloseExecute, \
            window_s, \
            Theme, \
            transparent, \
            FPS
        AutoLogin = Set[0]
        Sound = Set[1]
        ClosePrompt = Set[2]
        CloseExecute = Set[3]
        window_s = Set[4]
        Theme = Set[5]
        transparent = Set[6]
        FPS = Set[7]

    def update_exp(self, value):
        global exp
        exp = value

    def update_position(self, value):
        global position_status, textedit_position, send_position
        position_status = True
        textedit_position = value[0]
        send_position = value[1]

    def update_handle_value(self, x, y):
        global handle_position
        handle_position[0] = x
        handle_position[1] = y

    def update_information(self, value):
        global Name
        Name = value

    def run_team_command(self, command):
        if command == "handle":
            MyThread(self.Handle_Send)
        elif command == "qq":
            MyThread(self.Send_QQ)
        elif command == "copy":
            MyThread(self.Send_Copy)
        elif command == "update":
            MyThread(self.QQ_image_update)
        elif command == "execute":
            MyThread(self.Click_Record_execute)

    def open_user_window(self):
        # 查找窗口
        usr_win = gw.getWindowsWithTitle("Fuchen个人信息")
        # 判断窗口是否存在
        if usr_win:
            usr_win[0].close()  # 关闭第一个匹配的窗口
        global exp

        lis = [self, Account, Name, avatar_date, exp, s, avatar_load_status]
        self.user_window = ui.userinfo.InfoPopup(lis)
        self.user_window.show()

    def open_help_window(self):
        self.help_window = SundryUI.Help()
        self.help_window.show()

    def open_view_window(self):
        lis = [self, s]
        self.view_window = SundryUI.View(lis)
        self.view_window.show()

    def open_floating_window(self):
        self.floating_window = SundryUI.floating_window(self)
        self.floating_window.show()

    def close_floating_window(self):
        self.floating_window = SundryUI.floating_window(self)
        self.floating_window.close()

    def open_point_window(self):
        self.point_window = SundryUI.ExpandingWindow()
        self.point_window.show()

    def open_record_window(self):
        import ui.RecordPosition

        self.record__position_window = ui.RecordPosition.record_position(self)
        self.record__position_window.exec_()

    def open_console_window(self):
        with open("config.json", "r") as file:
            config = json.load(file)
        if config["console_theme"] == "light":
            console_theme = "light"
        else:
            console_theme = "dark"
        self.console_window = ui.console_window.ConsoleWindow(
            [self.stdout_stream, self.stderr_stream, self, s, console_theme]
        )
        self.console_window.show()

    def open_fileedit_window(self):
        if self.file_lineEdit.text() == "":
            file_name = ""
        else:
            file_name = self.file_lineEdit.text()
        self.fileedit_window = ui.fileEdit.EditorWindow(file_name, self)
        self.fileedit_window.show()

    def clo(self):
        with open(f"config.json", "r") as file:
            U_data = json.load(file)
        next = U_data["ClosePrompt"]
        execute = U_data["CloseExecute"]
        if next == True:  # 是否提示关闭窗口
            self.abus = SundryUI.Quit_Prompt([self, self.window_icon])
            self.abus.exec_()
        else:  # 不提示关闭窗口
            if execute == "Close":
                self.close()

                # self.close_MainWindow()
                os._exit(0)
            else:
                SundryUI.Hide([self, self.window_icon])

    def play_sound(self):
        play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")

    """def send_talk(self):
        text = self.uim.talk_lineEdit.text()
        text = re.sub(' ', '~~space~~', text)
        send_encry("20030 "+text)
        self.uim.talk_lineEdit.clear()"""

    def closeEvent(self, e):
        try:
            if self.open_status == True:
                self._stop_click_process()
            try:
                self._cleanup_click_shared_memory()
            except:
                pass

            os._exit(0)
        except Exception as e:
            print(e)

    # 新增城市修改方法
    def change_city_name(self, event):
        global city_name

        # 创建输入对话框
        dialog = QInputDialog(self)
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle("修改城市")
        dialog.setLabelText("请输入城市名称:")
        dialog.setTextValue(str(city_name))
        # dialog.setWindowFlags(Qt.FramelessWindowHint)

        # 设置对话框整体样式
        dialog.setStyleSheet("""
            QDialog {
                background: rgba(121, 188, 237, 0.9);
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,0.25);
            }
            QLabel {
                color: white;
                font: 500 13px 'Microsoft YaHei';
                background: transparent;
            }
            QLineEdit {
                background: rgba(255,255,255,0.15);
                color: white;
                font: 500 13px 'Microsoft YaHei';
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,0.25);
                padding: 5px;
            }
            QPushButton {
                background: rgba(255,255,255,0.1);
                color: white;
                font: 500 12px 'Microsoft YaHei';
                border-radius: 6px;
                padding: 6px;
                min-width: 60px;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.2);
            }
        """)

        # 调整对话框尺寸
        dialog.resize(300, 150)
        """# 计算居中位置并移动对话框[6,7,8](@ref)
        screen_geometry = QApplication.desktop().availableGeometry()
        x = (screen_geometry.width() - dialog.width()) // 2
        y = (screen_geometry.height() - dialog.height()) // 2
        dialog.move(x, y)"""
        if dialog.exec_() == QDialog.Accepted:
            new_city = dialog.textValue().strip()
            if new_city:
                city_name = new_city
                self.Update_weather()

    def Update_weather(self):  # 获取天气
        def get_response():
            try:
                print("开始更新天气 请稍后")
                api_key = "dce92b382ffb9409ca31ae4c1b240d4f"
                # 发送请求获取IP地址信息
                """res = requests.get('http://myip.ipip.net', timeout=5).text
                # 提取城市信息
                split_res = res.split('  ')
                city_info = split_res[-2]  # 倒数第二个元素是位置信息
                city_info = city_info.split(' ')
                country = city_info[-3]
                city_info = city_info[-1]"""
                # global city_name, weather_status, temperature, humidity, weather_info
                self.weather_label.setText("正在获取天气...")
                global city_name, city_info
                country = city_info[-3]
                if country[-2:] == "中国":
                    # city_name = city_info
                    pinyin_list = pinyin(city_name, style=Style.NORMAL)
                    # 从拼音列表中提取拼音并连接成字符串
                    pinyin_str = "".join([item[0] for item in pinyin_list])
                    # 设置API请求的URL
                    base_url = "http://api.openweathermap.org/data/2.5/weather"
                    url = f"{base_url}?q={pinyin_str}&appid={api_key}"
                    # 发送API请求并获取响应
                    response = requests.get(url, timeout=15)
                    data = response.json()
                    # 提取天气信息
                    if data["cod"] == 200:
                        temperature = data["main"]["temp"] - 273.15  # 摄氏度
                        temp = round(temperature)
                        humidity = data["main"]["humidity"]  # 湿度
                        weather_main = data["weather"][0]["main"]
                        weather_id = data["weather"][0]["id"]

                        # 根据天气类型设置emoji和描述
                        emoji, weather_desc = "🌡️", "未知天气"
                        if weather_main == "Clear":
                            emoji, weather_desc = "☀️", "晴天"
                        elif weather_main == "Clouds":
                            if 801 <= weather_id <= 802:
                                emoji, weather_desc = "⛅", "晴间多云"
                            elif 803 <= weather_id <= 804:
                                emoji, weather_desc = "☁️", "多云"
                        elif weather_main == "Rain":
                            emoji, weather_desc = "🌧️", "下雨"
                        elif weather_main == "Drizzle":
                            emoji, weather_desc = "🌧️", "小雨"
                        elif weather_main == "Thunderstorm":
                            emoji, weather_desc = "⛈️", "雷雨"
                        elif weather_main == "Snow":
                            emoji, weather_desc = "🌨️", "下雪"
                        elif weather_main in ("Mist", "Fog"):
                            emoji, weather_desc = "🌫️", "雾"
                        elif weather_main == "Haze":
                            emoji, weather_desc = "🌫️", "霾"
                        elif weather_main == "Squall":
                            emoji, weather_desc = "💨", "大风"
                        elif weather_main == "Tornado":
                            emoji, weather_desc = "🌪️", "龙卷风"

                        # 更新天气标签
                        # 生成完整显示文本
                        full_text = f"{emoji} {temp}°C {weather_desc} | {city_name}"

                        # 获取字体度量
                        font_metrics = self.weather_label.fontMetrics()
                        available_width = self.weather_label.width() - 10  # 保留边距

                        # 自动缩短文本算法
                        def shorten_text(text, max_width):
                            if font_metrics.horizontalAdvance(text) <= max_width:
                                return text
                            # 逐步移除城市名的最后一个字符
                            parts = text.split(" | ")
                            base = parts[0] + " | "
                            city = parts[1]
                            for i in range(len(city) - 1, 0, -1):
                                shortened = base + city[:i] + "…"
                                if (
                                    font_metrics.horizontalAdvance(shortened)
                                    <= max_width
                                ):
                                    return shortened
                            return text[:3] + "…"  # 保底方案

                        # 应用自适应缩短
                        display_text = shorten_text(full_text, available_width)

                        # 设置显示文本和悬浮提示
                        self.weather_label.setText(display_text)
                        self.weather_label.setToolTip(full_text)  # 悬浮显示完整信息
                        weather_status = True
                        print(
                            f"天气获取成功 城市:{city_name} 温度:{temp}°C 湿度:{humidity}%"
                        )
                    else:
                        self.weather_label.setText("天气获取失败")
                        weather_status = False
                        print("天气获取失败")
                else:
                    self.weather_label.setText("当前位置暂不支持天气解析")
                    print("当前位置暂不支持天气解析")
            except requests.exceptions.Timeout:
                self.weather_label.setText("获取天请求超时")
                print(f"获取天气请求超时")
            except Exception as e:
                traceback.print_exc()
                self.weather_label.setText("天气获取失败")
                print(f"天气获取失败: {str(e)}")

        MyThread(get_response)

    def open_folder(self, page):  # 浏览QQ头像下载文件夹
        if page == "picture":
            folder_path = "./mod/picture"
            url = QUrl.fromLocalFile(folder_path)
            QDesktopServices.openUrl(url)

        elif page == "music":
            folder_path = self.music_savepath.text()
            url = QUrl.fromLocalFile(folder_path)
            QDesktopServices.openUrl(url)

        elif page == "xlsx":
            folder_path = ".mod/xlsx"
            url = QUrl.fromLocalFile(folder_path)
            QDesktopServices.openUrl(url)

    def init_shared_memory(self):
        # 确保kernel32的API正确定义
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

        # 定义CloseHandle（需要补充这部分声明）
        CloseHandle = kernel32.CloseHandle
        CloseHandle.argtypes = [wintypes.HANDLE]
        CloseHandle.restype = wintypes.BOOL

        # 定义UnmapViewOfFile（虽然当前函数未使用，但后续需要）
        UnmapViewOfFile = kernel32.UnmapViewOfFile
        UnmapViewOfFile.argtypes = [wintypes.LPCVOID]
        UnmapViewOfFile.restype = wintypes.BOOL

        # 定义CreateFileMappingW（已有定义需要保留）
        CreateFileMappingW = kernel32.CreateFileMappingW
        CreateFileMappingW.argtypes = [
            wintypes.HANDLE,
            ctypes.c_void_p,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPCWSTR,
        ]
        CreateFileMappingW.restype = wintypes.HANDLE

        # 定义MapViewOfFile（已有定义需要保留）
        MapViewOfFile = kernel32.MapViewOfFile
        MapViewOfFile.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.DWORD,
            ctypes.c_size_t,
        ]
        MapViewOfFile.restype = wintypes.LPVOID

        # 共享内存参数
        SHM_NAME = "Local\\ClickParamsSharedMemory"
        SHM_SIZE = ctypes.sizeof(SharedParams)

        # 创建共享内存
        h_map = CreateFileMappingW(
            wintypes.HANDLE(-1),
            None,
            0x04,  # PAGE_READWRITE
            0,
            SHM_SIZE,
            SHM_NAME,
        )
        if h_map == 0:
            error = ctypes.GetLastError()
            # 重要修改：这里必须先声明CloseHandle才能调用
            CloseHandle(h_map)  # 清理无效句柄
            raise ctypes.WinError(error)

        # 映射内存
        ptr = MapViewOfFile(
            h_map,
            0xF001F,  # FILE_MAP_ALL_ACCESS
            0,
            0,
            SHM_SIZE,
        )
        if not ptr:
            error = ctypes.GetLastError()
            CloseHandle(h_map)  # 映射失败时关闭句柄
            raise ctypes.WinError(error)

        return h_map, ptr

    def write_shared_memory(self, ptr, hotkey, interval, click_type):
        params = SharedParams()
        params.version = APP_VERSION
        params.hotkey = int(hotkey)
        params.interval = interval
        params.clickType = click_type
        ctypes.memmove(ptr, ctypes.byref(params), ctypes.sizeof(params))

    def update_shared_params(self):
        """更新共享内存参数"""
        if hasattr(self, "shm_ptr"):
            # 转换当前参数
            hotkey = self._convert_hotkey_to_code()
            if hotkey == 8888:
                self.show_message_box("提示", "按键错误 请重新输入")
                return 0
            interval = float(self._3D.value())
            print(interval)
            click_type = self._get_current_click_type()  # 新增获取点击类型方法
            if interval != 0:
                # 写入共享内存
                self.write_shared_memory(self.shm_ptr, hotkey, interval, click_type)

    def _get_current_click_type(self):
        """获取当前点击类型的数字表示"""
        if self.LClick_Radio.isChecked():
            return 0
        elif self.MClick_Radio.isChecked():
            return 1
        else:
            return 2

    def _start_click_process(self):
        click_exe = os.path.abspath("./mod/more/click.exe")
        if not os.path.exists(click_exe):
            raise FileNotFoundError(f"未找到连点器程序: {click_exe}")
        creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        return subprocess.Popen(
            [click_exe, str(APP_VERSION)],
            creationflags=creation_flags,
        )

    def _stop_click_process(self):
        proc = getattr(self, "c_thread_object", None)
        if not proc:
            return
        try:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=2)
        finally:
            self.c_thread_object = None

    def _cleanup_click_shared_memory(self):
        if not hasattr(self, "shm_ptr"):
            return
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

        UnmapViewOfFile = kernel32.UnmapViewOfFile
        UnmapViewOfFile.argtypes = [ctypes.c_void_p]
        UnmapViewOfFile.restype = wintypes.BOOL

        CloseHandle = kernel32.CloseHandle
        CloseHandle.argtypes = [wintypes.HANDLE]
        CloseHandle.restype = wintypes.BOOL

        UnmapViewOfFile(ctypes.c_void_p(self.shm_ptr))
        CloseHandle(self.shm_handle)

        del self.shm_ptr
        del self.shm_handle

    def open_click(self):  # 开启连点器部分
        if (self.RClick_Radio.isChecked()) and (self.sort == "鼠标右键"):
            pyautogui.confirm("点击按键和监听热键不可相同!")
            return 0
        elif (self.MClick_Radio.isChecked()) and (self.sort == "鼠标中键"):
            pyautogui.confirm("点击按键和监听热键不可相同!")
            return 0
        try:
            print("开启中")
            self._3pushButton_6.setText("正在开启...")
            self._3pushButton_6.setEnabled(False)
            try:
                # 转换点击类型为数字
                click_type = self._get_current_click_type()
                # 转换热键为数字
                hotkey = self._convert_hotkey_to_code()  # 需要实现这个转换方法
                interval = float(self._3D.value())

                if self.high_speed_radio.isChecked():
                    # 创建共享内存
                    h_map, ptr = self.init_shared_memory()
                    self.write_shared_memory(ptr, hotkey, interval, click_type)

                    # 启动click.exe
                    self.c_thread_object = self._start_click_process()

                    # 保存句柄和指针用于后续清理
                    self.shm_handle = h_map
                    self.shm_ptr = ptr
                self.open_status = True
                self._3pushButton_6.setText("连点器已开启")
                self._3pushButton_7.setVisible(True)
                self.high_speed_radio.setEnabled(False)
                self.low_speed_radio.setEnabled(False)
            except KeyboardInterrupt:
                # 处理 Ctrl+C 中断
                self._stop_click_process()
                self._cleanup_click_shared_memory()
                sys.exit()
            except Exception as e:
                traceback.print_exc()
                print(e)
                self._3pushButton_6.setText("开启失败")
                self._3pushButton_7.setVisible(True)
                # 处理其他异常
                pyautogui.confirm(f"Error: {e}")
                self._stop_click_process()
                self._cleanup_click_shared_memory()
            """finally:
                # 确保在程序退出时终止 程序
                C_thread.terminate()"""
        except Exception as e:
            print(e)
            pyautogui.confirm(e)

    def break_click(self):  # 关闭连点器
        try:
            if getattr(self, "open_status", False):
                # 先停掉子进程
                self._stop_click_process()

                # 再清理共享内存（只有高速模式才会有这俩属性）
                self._cleanup_click_shared_memory()

                # 恢复 UI 和标志位
                self.open_status = False
                self._3pushButton_6.setText("开启连点器")
                self._3pushButton_6.setEnabled(True)
                self._3D.setEnabled(True)
                self._3pushButton_7.setVisible(False)
                self.high_speed_radio.setEnabled(False)
                self.low_speed_radio.setEnabled(False)
        except Exception as e:
            traceback.print_exc()
            print(e)
            pyautogui.confirm(str(e))

    def _convert_hotkey_to_code(self):
        # 返回对应的键值或默认值
        return function.keycode_dict.get(self.sort.lower(), 8888)

    def gain_handle(self):  # 获取句柄
        self.showMinimized()

        def on_click(x, y, button, pressed):
            if pressed:
                if button == mouse.Button.left:  # 如果是左键点击
                    hwnd = win32gui.WindowFromPoint((x, y))  # 获取句柄
                    self._2lineEdit_3.setText(str(hwnd))  # 设置句柄到lineEdit
                    listener.stop()  # 停止监听
                elif button == mouse.Button.right:  # 如果是右键点击
                    listener.stop()

        def click_listener():
            global listener
            listener = mouse.Listener(on_click=on_click)
            listener.start()
            listener.join()

        click_listener()
        self.showNormal()

    def handle_auto_execute(self):
        # 获取所有配置数据示例
        configurations = []
        for group in self.operation_groups:
            config = {
                "handle": group.edit_handle.text(),
                "action": group.combo_action.currentText(),
                "param": group.edit_param.text(),
            }
            configurations.append(config)

        if configurations != []:
            for i in range(self.spin_executions.value()):
                for x in configurations:
                    action = x["action"]
                    if action == "点击":
                        try:
                            hwnd = int(x["handle"])
                            win32gui.SetForegroundWindow(hwnd)
                            time.sleep(0.5)  # 等待窗口聚焦
                            parts = x["param"].split(",")
                            click_x = int(parts[0])
                            click_y = int(parts[1])
                            long_position = win32api.MAKELONG(
                                click_x, click_y
                            )  # 模拟鼠标指针 传送到指定坐标
                            win32api.PostMessage(
                                hwnd,
                                win32con.WM_LBUTTONDOWN,
                                win32con.MK_LBUTTON,
                                long_position,
                            )  # 模拟鼠标按下
                            win32api.PostMessage(
                                hwnd,
                                win32con.WM_LBUTTONUP,
                                win32con.MK_LBUTTON,
                                long_position,
                            )  # 模拟鼠标弹起
                        except Exception as e:
                            traceback.print_exc()
                    elif action == "右键":
                        try:
                            hwnd = int(x["handle"])
                            print(hwnd, type(hwnd))
                            win32gui.SetForegroundWindow(hwnd)
                            time.sleep(0.5)  # 等待窗口聚焦
                            parts = x["param"].split(",")
                            click_x = int(parts[0])
                            click_y = int(parts[1])
                            long_position = win32api.MAKELONG(
                                click_x, click_y
                            )  # 模拟鼠标指针 传送到指定坐标
                            print(long_position, type(long_position))
                            win32api.PostMessage(
                                hwnd,
                                win32con.WM_RBUTTONDOWN,
                                win32con.MK_RBUTTON,
                                long_position,
                            )  # 模拟鼠标按下
                            win32api.PostMessage(
                                hwnd,
                                win32con.WM_RBUTTONUP,
                                win32con.MK_RBUTTON,
                                long_position,
                            )  # 模拟鼠标弹起
                        except Exception as e:
                            traceback.print_exc()
                    elif action == "粘贴":
                        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                        # 按下 Ctrl 键
                        win32api.keybd_event(ord("V"), 0, 0, 0)
                        # 按下 V 键
                        win32api.keybd_event(ord("V"), 0, win32con.KEYEVENTF_KEYUP, 0)
                        # 放开 V 键
                        win32api.keybd_event(
                            win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0
                        )
                        # 放开 Ctrl 键
                    elif action == "按键":
                        # 向指定窗口发送 Enter 键
                        win32api.keybd_event(x, 0, 0, 0)  # 按下 Enter 键
                        win32api.keybd_event(
                            win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0
                        )  # 放开 Enter 键
                    elif action == "回车":
                        # 向指定窗口发送 Enter 键
                        win32api.keybd_event(
                            win32con.VK_RETURN, 0, 0, 0
                        )  # 按下 Enter 键
                        win32api.keybd_event(
                            win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0
                        )  # 放开 Enter 键
                    elif action == "等待":
                        time.sleep(int(x["param"]))

                time.sleep(self.spin_interval.value())
            print("执行完毕")

    def start_detection(self):
        # self.mask = page.ScreenMask(self)
        self.mask = new_mainpage.ScreenMask(self)
        self.mask.showFullScreen()

    def mouseinfo(self):  # 鼠标信息
        pyautogui.mouseInfo()

    def QQ_Group_information(self):  # QQ群信息获取
        play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
        if self.Edge_Radio.isChecked():
            mode = "Edge"
        elif self.Chrome_Radio.isChecked():
            mode = "Chrome"
        elif self.Ie_Radio.isChecked():
            mode = "Ie"
        else:
            pyautogui.confirm("文件选择类型错误 请重试!")
            return 0
        Qid = self.checkBox_qid.isChecked()
        sex = self.checkBox_sex.isChecked()
        QQ_year = self.checkBox_qq_year.isChecked()
        join_date = self.checkBox_join_date.isChecked()
        send_date = self.checkBox_send_date.isChecked()
        group_lv = self.checkBox_group_lv.isChecked()
        folder = self.lineEdit_group_path.text()
        result = function.QQ_Group_Obtain(
            mode, folder, Qid, sex, QQ_year, join_date, send_date, group_lv
        )
        if (
            str(type(result))
            == "<class 'selenium.common.exceptions.NoSuchWindowException'>"
        ):
            pyautogui.confirm("操作取消")
        elif result == "Cancel":
            pyautogui.confirm("操作取消")
        elif str(result[0:6]) == "文件保存成功":
            pyautogui.confirm(result)
        else:
            pyautogui.confirm(result, "错误:")

    def check_update(self):
        local_ver = Version
        url = "https://fcyang.cn/data.txt"

        try:
            response = requests.get(url)
            response.raise_for_status()

            config = {}
            for line in response.text.splitlines():
                line = line.strip()
                if line and ":" in line:
                    key, value = line.split(":", 1)
                    config[key.strip()] = value.strip()

            server_ver = config.get("last_version")
            last_link = config.get("last_link")

            print(f"Last Version: {server_ver}")
            print(f"Last Link: {last_link}")

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return

        def parse_version(version):
            cleaned = re.sub(r"^[^\d.]*", "", version, flags=re.IGNORECASE)
            parts = cleaned.split(".")
            nums = []
            for part in parts:
                try:
                    nums.append(int(part))
                except ValueError:
                    nums.append(0)
            return nums

        local_parts = parse_version(local_ver)
        server_parts = parse_version(server_ver)

        max_length = max(len(local_parts), len(server_parts))
        update_needed = False

        # 比较所有对应的版本号部分
        for i in range(max_length):
            local_num = local_parts[i] if i < len(local_parts) else 0
            server_num = server_parts[i] if i < len(server_parts) else 0

            if server_num > local_num:
                update_needed = True
                break
            elif server_num < local_num:
                QMessageBox.information(self, "提示:", "当前已是最新版本 无需更新")
                return

        # 如果前面部分完全相同，检查服务器是否有额外非零子版本
        if not update_needed and len(server_parts) > len(local_parts):
            for i in range(len(local_parts), len(server_parts)):
                if server_parts[i] > 0:
                    update_needed = True
                    break

        if update_needed:
            result = pyautogui.confirm(f"发现新版本: {server_ver}，是否更新？")
            if result == "OK":
                webbrowser.open(last_link)
        else:
            QMessageBox.information(self, "提示:", "当前已是最新版本 无需更新")

    def download_image(self):  # 下载QQ头像
        if exp < 20:
            pyautogui.confirm(
                "该功能需要Lv2才能使用!\n按ctrl+o 或按f12 打开控制台 输入签到 签到一天即可使用!"
            )
            return 0
        self.btn_download_qq.setEnabled(False)

        def generate_random_number():
            # 生成随机位数（6到10之间）
            digits = random.randint(7, 10)
            # 生成随机数字字符串
            first_digit = random.randint(1, 9)  # 生成1到9之间的随机数作为第一位
            remaining_digits = "".join(
                random.choices("0123456789", k=digits - 1)
            )  # 生成剩余位数的随机数字字符串
            random_number = str(first_digit) + remaining_digits

            return random_number

        def compare_images(image_path):
            image = Image.open(image_path)
            width, height = image.size
            return width == height == 40

        success = 0
        total = 0
        for i in range(self.qq_image_down_spinbox.value()):
            random_number = generate_random_number()
            url = f"https://q1.qlogo.cn/g?b=qq&nk={random_number}&s=640"
            response = requests.get(url)
            total = total + 1
            if response.status_code == 200:
                with open(f"./mod/picture/{random_number}.jpg", "wb") as file:
                    file.write(response.content)

                image_path = f"./mod/picture/{random_number}.jpg"

                if compare_images(image_path):
                    os.remove(f"./mod/picture/{random_number}.jpg")
                else:
                    success = success + 1
                    self.successfully_download_times.setText(f"有效次数: {success} 次")
            self.total_download_times.setText(f"总下载次数: {total} 次")
        if success == 0:
            pass
            self.successfully_download_times.setText("有效次数: 0 次")
        self.btn_download_qq.setEnabled(True)
        MyThread(play_warning_sound)
        pyautogui.confirm(
            f"图片下载成功!\n本次已成功下载{success}张图片(已删除默认头像)"
        )

    def QQ_image_update(self):  # QQ个人信息资料一键更新
        result = pyautogui.confirm(
            "此功能只适用于旧版QQ! 请确认QQ版本后再使用\n请确保QQ主窗口已经打开 若打开则点击确认按钮 修改资料时 请勿移动鼠标\n若出现修改失败的情况 可能是间隔时间过小 略微调大即可"
        )
        if result != "OK":
            return 0
        try:
            rest = self.qq_image_update_spinbox_interval.value()
            result = function.QQ_Information_Update(rest)
            if result == 0:
                MyThread(play_warning_sound)
                pyautogui.confirm("资料修改成功")
            elif result == "Not Found":
                pyautogui.confirm("需要先下载图片才可使用")
                return 0
            else:
                raise Exception(result)
        except Exception as e:
            MyThread(play_warning_sound)
            pyautogui.confirm(e)
            traceback.print_exc()

    def Handle_Send(self):  # 句柄式发送消息
        def setText(aString):  # 设置剪贴板文本
            w.OpenClipboard()
            w.EmptyClipboard()
            w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
            w.CloseClipboard()

        def getWindowSize(hwnd):  # 获取窗口的宽度和高度
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            return width, height

        def doClick(cx, cy, hwnd):
            width, height = getWindowSize(hwnd)  # 获取窗口的尺寸
            click_x = width + cx
            click_y = height + cy  # 计算相对底部的y坐标HELLO
            long_position = win32api.MAKELONG(
                click_x, click_y
            )  # 模拟鼠标指针 传送到指定坐标
            win32api.SendMessage(
                hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position
            )  # 模拟鼠标按下
            win32api.SendMessage(
                hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position
            )  # 模拟鼠标弹起
            # 发送 Ctrl+V 来像聊天框粘贴信息

            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            # 按下 Ctrl 键
            win32api.keybd_event(ord("V"), 0, 0, 0)
            # 按下 V 键
            win32api.keybd_event(ord("V"), 0, win32con.KEYEVENTF_KEYUP, 0)
            # 放开 V 键
            win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            # 放开 Ctrl 键

            # 向指定窗口发送 Enter 键
            win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)  # 按下 Enter 键
            win32api.keybd_event(
                win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0
            )  # 放开 Enter 键

        def send_qq(hwnd, msg):
            if msg != "###UNCOPY###":  # 当字符不等于这个时 复制内容
                setText(msg)
            # 投递剪贴板消息到QQ窗体
            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
            times = self.handle_send_times.value()
            wait_time = self.handle_send_interval.value()
            self.handle_number_window("QQ句柄式发送", 0, times)
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.5)  # 等待窗口聚焦

            for i in range(int(times)):
                doClick(
                    handle_position[0], handle_position[1], hwnd
                )  # 点击 (30, height-60)
                self.number_now_changed(i + 1)
                time.sleep(wait_time)  # 等待操作完成

        hwnd = self._2lineEdit_3.text()
        massage = self._2textEdit.toPlainText()
        if hwnd == "":
            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
            pyautogui.confirm("请输入句柄")
        elif massage == "":
            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
            pyautogui.confirm("请输入需要发送的消息")
        else:
            try:
                send_qq(int(hwnd), massage)
                self.open_point_window()
            except Exception as e:
                pyautogui.confirm(f"发送失败 错误信息如下:\n {e}")

    def Send_QQ(self):  # @QQ
        # 要检查的进程名称
        target_process_name = "QQ.exe"
        if check_process_exists(target_process_name):
            if position_status == False:
                pyautogui.confirm("需要先设置位置才能开始发送")
                return 0
            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
            target_number = self.QQ_StartSend_At_target_lineedit.text()
            pause_time = self.QQ_StartSend_At_pause_doublespb.value()
            times = self.QQ_StartSend_At_times_spinbox.value()
            number_send = False
            if target_number == "":
                pyautogui.confirm("请输入QQ号")
            elif pause_time == 0.0:
                pyautogui.confirm("请输入间隔")
            elif (
                len(target_number) > 11
                or len(target_number) <= 5
                or not target_number.isdigit()
            ):
                pyautogui.confirm("请输入正确的QQ号")
            else:
                time.sleep(3)
                pyautogui.PAUSE = pause_time
                if self.QQ_StartSend_At_number_checkbox.isChecked():
                    number_send = True
                self.showMinimized()
                self.handle_number_window("QQ@指定用户", 0, times)
                number = 0
                while True:
                    if keys.is_pressed("F10"):  # 按下F10退出
                        self.showNormal()
                        self.open_point_window()
                        break
                    number = number + 1  # Increment at the start
                    if (
                        times != 0 and number > times
                    ):  # Change condition to number > times
                        self.showNormal()
                        self.open_point_window()
                        break
                    pyautogui.click(textedit_position)
                    pyautogui.write(f"@{target_number}")
                    time.sleep(0.02)
                    pyautogui.press("enter")
                    pyautogui.hotkey("ctrl", "v")
                    if number_send == True:
                        pyautogui.write(
                            str(number)
                        )  # Already incremented, so no change needed
                    randfigure = random.choice(Random_list)  # 随机符号
                    if randfigure == 1:
                        pyautogui.press(".")
                    elif randfigure == 2:
                        pyautogui.press("。")
                    else:
                        pyautogui.press(",")
                    pyautogui.click(send_position)
                    self.number_now_changed(number)

        else:
            pyautogui.confirm("QQ未启动")

    def Send_Copy(self):  # 发送复制消息
        # 要检查的进程名称
        target_process_name = "QQ.exe"
        if check_process_exists(target_process_name):
            if position_status == False:
                pyautogui.confirm("需要先设置位置才能开始发送")
                return 0
            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
            time.sleep(3)
            pause_time = self.QQ_Send_Copy_pause_doublespb.value()
            times = self.QQ_Send_Copy_times_spinbox.value()
            pyautogui.PAUSE = pause_time
            number = 0
            start_time = time.time()
            self.showMinimized()
            self.handle_number_window("QQ复制内容发送", 0, times)
            while True:
                if keys.is_pressed("F10"):  # 按下F10退出
                    self.showNormal()
                    self.open_point_window()
                    end_time = time.time()
                    # 计算执行时间
                    execution_time = end_time - start_time
                    # 打印执行时间
                    print(f"执行时间: {execution_time} 秒")
                    break
                number = number + 1
                if times != 0 and number > times:
                    self.showNormal()
                    self.open_point_window()
                    break
                pyautogui.click(textedit_position)
                pyautogui.hotkey("ctrl", "v")  # 粘贴
                time.sleep(0.02)
                randfigure = random.choice(Random_list)  # 随机字符输入
                if randfigure == 1:
                    pyautogui.press(".")
                elif randfigure == 2:
                    pyautogui.press("。")
                else:
                    pyautogui.press(",")
                pyautogui.click(send_position)  # 点击第二处位置
                self.number_now_changed(number)
            print(f"本次Fuchen累计发送{number}条消息")
        else:
            pyautogui.confirm("QQ未启动!")

    def order_send(self):
        import pyperclip

        if self.QQ_Seq_lineEdit == "":
            pyautogui.confirm("请先选择文件")
            return 0
        target_process_name = "QQ.exe"
        if not check_process_exists(target_process_name):
            pyautogui.confirm("请先启动QQ！")
            return 0
        if position_status == False:
            pyautogui.confirm("需要先设置位置才能开始发送")
            return 0
        play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
        time.sleep(3)
        wait_time = self.QQ_Seq_doublebox.value()
        if self.QQ_Seq_combobox.currentText() == "顺序发送":
            pyautogui.PAUSE = wait_time
            for i in range(self.QQ_Seq_Times_spinBox.value()):
                with open(self.QQ_Seq_lineEdit.text(), "r", encoding="utf-8") as file:
                    # 逐行读取文件内容
                    for line in file:
                        # 去除行尾的换行符
                        line = line.strip()
                        # 打印该行内容（可以查看复制内容是否正确）
                        if keys.is_pressed("F10"):  # 按下F10退出
                            self.open_point_window()
                            break
                        # 复制该行内容到剪切板
                        pyperclip.copy(line)
                        pyautogui.click(textedit_position)
                        # time.sleep(wait_time)
                        pyautogui.hotkey("ctrl", "v")
                        time.sleep(0.02)
                        pyautogui.click(send_position)
                        # 暂停等待用户操作或观察复制内容
        else:
            pyautogui.PAUSE = wait_time
            # 读取文件内容到列表中
            with open(self.QQ_Seq_lineEdit.text(), "r", encoding="utf-8") as file:
                lines = file.readlines()
            # 随机选择一行
            for i in range(self.QQ_Seq_Times_spinBox.value()):
                random_line = random.choice(lines).strip()
                if keys.is_pressed("F10"):  # 按下F10退出
                    self.showNormal()
                    self.open_point_window()
                    break
                # 复制该行内容到剪切板
                pyperclip.copy(random_line)
                pyautogui.click(textedit_position)
                # time.sleep(wait_time)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(0.02)
                pyautogui.click(send_position)

    def handle_minimize(self):  # 通过主进程最小化
        self.showMinimized()

    def handle_restore(self):  # 通过主进程恢复
        self.showNormal()
        self.repaint()  # 或者调用 update() 来刷新界面

    def record_hotkey_setting(self):
        if self.hotkey_execute_status != None:
            self.hotkey_execute_status()
        # 创建并显示热键对话框（模态对话框）
        dialog = ui.hotkey_record.HotkeyDialog(self)
        if dialog.exec_() == QDialog.Accepted:  # 等待对话框关闭
            hotkey = dialog.hotkey
            if hotkey == "":
                return
            if hotkey == self.uim.execute_hotkey:
                pyautogui.confirm("记录按键不可与执行按键相同")
                return
            self.uim.record_hotkey = hotkey
            if self.hotkey_record_status == None:
                self.hotkey_record_status = keys.add_hotkey(
                    hotkey, self.start_recording
                )
            else:
                self.hotkey_record_status()
                self.hotkey_record_status = keys.add_hotkey(
                    hotkey, self.start_recording
                )
            self.uim.Hotkey_record_button.setText(f"当前热键：{hotkey}")
            print("获取到的热键：", hotkey)
        if self.uim.execute_hotkey != "未设置":
            self.hotkey_execute_status = keys.add_hotkey(
                self.uim.execute_hotkey, self.start_executing
            )

    def on_record_finished(self):
        self.handle_restore()
        self.record_thread = None

    def execute_hotkey_setting(self):
        if self.hotkey_record_status != None:
            self.hotkey_record_status()
        # 创建并显示热键对话框（模态对话框）
        dialog = ui.hotkey_record.HotkeyDialog(self)
        if dialog.exec_() == QDialog.Accepted:  # 等待对话框关闭
            hotkey = dialog.hotkey
            if hotkey == "":
                return
            if hotkey == self.uim.record_hotkey:
                pyautogui.confirm("执行按键不可与记录按键相同")
                return
            self.uim.execute_hotkey = hotkey
            if self.hotkey_execute_status == None:
                self.hotkey_execute_status = keys.add_hotkey(
                    hotkey, self.start_executing
                )
            else:
                self.hotkey_execute_status()
                self.hotkey_execute_status = keys.add_hotkey(
                    hotkey, self.start_executing
                )
            self.uim.Hotkey_execute_button.setText(f"当前热键：{hotkey}")
            print("获取到的热键：", hotkey)
        if self.uim.record_hotkey != "未设置":
            self.hotkey_record_status = keys.add_hotkey(
                self.uim.record_hotkey, self.start_recording
            )

    def on_execute_finished(self):
        self.handle_restore()
        self.execute_thread = None

    def _on_record_worker_finished(self, success, error_text, cursor_position):
        if cursor_position is not None:
            try:
                pyautogui.moveTo(cursor_position[0], cursor_position[1])
            except Exception:
                pass
        if not success and error_text:
            print(error_text)
        self.record_status = False
        self.handle_restore()
        self.record_thread = None
        self.record_worker = None

    def _on_execute_worker_progress(self, value):
        self.number_now_changed(value)

    def _on_execute_worker_finished(self, success, error_text, cursor_position):
        if cursor_position is not None:
            try:
                pyautogui.moveTo(cursor_position[0], cursor_position[1])
            except Exception:
                pass
        if not success and error_text:
            print(error_text)
        self.execute_status = False
        self.handle_restore()
        self.execute_thread = None
        self.execute_worker = None

    def Click_Record(self):  # 记录自动脚本
        # 确保在主线程执行
        if QThread.currentThread() != self.thread():
            self.trigger_click_record_signal.emit()
            return
        if self.execute_status == True:  # 防止和执行同时进行
            return
        if self.record_status == True:  # 防止重复执行
            return
        file_path = self.file_lineEdit.text().strip()
        if file_path == "":
            QMessageBox.information(self, "提示", f"配置文件为空 请先选则文件")
            return 0
        self.record_status = True

        screen = app.primaryScreen()
        if screen is not None:
            screen_width = max(1, screen.size().width())
            screen_height = max(1, screen.size().height())
        else:
            size = pyautogui.size()
            screen_width = max(1, size[0])
            screen_height = max(1, size[1])

        try:
            self.handle_minimize()
            self.record_thread = QThread(self)
            self.record_worker = ScriptRecordWorker(
                file_path=file_path,
                wait_time=self.wait_doubleSpinBox.value(),
                end_key_text=self.end_key_combo.currentText(),
                screen_width=screen_width,
                screen_height=screen_height,
            )
            self.record_worker.moveToThread(self.record_thread)

            self.record_thread.started.connect(self.record_worker.run)
            self.record_worker.finished.connect(self._on_record_worker_finished)
            self.record_worker.finished.connect(self.record_thread.quit)
            self.record_worker.finished.connect(self.record_worker.deleteLater)
            self.record_thread.finished.connect(self.record_thread.deleteLater)

            self.record_thread.start()
        except Exception:
            traceback.print_exc()
            self.record_status = False
            self.handle_restore()
            self.record_thread = None
            self.record_worker = None

    def validate_script_ready_for_execute(self, file_path):
        if not os.path.isfile(file_path):
            return False, "配置文件不存在"

        try:
            if os.path.getsize(file_path) == 0:
                return False, "配置文件为空，无法执行"
        except OSError:
            return False, "配置文件读取失败，无法执行"

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except json.JSONDecodeError:
            return False, "配置文件格式错误，无法执行"
        except Exception:
            return False, "配置文件读取失败，无法执行"

        if isinstance(raw_data, dict):
            records = raw_data.get("records", [])
        elif isinstance(raw_data, list):
            records = raw_data
        else:
            return False, "配置文件格式错误，无法执行"

        if not isinstance(records, list) or len(records) == 0:
            return False, "配置文件内容为空，无法执行"

        return True, ""

    def Click_Record_execute(self):  # 执行自动脚本
        # 确保在主线程执行
        if QThread.currentThread() != self.thread():
            self.trigger_click_execute_signal.emit()
            return
        if self.record_status == True:  # 防止和记录同时进行
            return
        if self.execute_status == True:  # 防止重复执行
            return
        file_path = self.file_lineEdit.text().strip()
        if file_path == "":
            QMessageBox.information(self, "提示", f"配置文件为空 请先选则文件")
            return 0

        valid, msg = self.validate_script_ready_for_execute(file_path)
        if not valid:
            QMessageBox.information(self, "提示", msg)
            return 0

        self.execute_status = True

        count = self._3spinBox_3.value()
        self.showMinimized()
        self.handle_number_window("执行自动脚本", 0, count)

        screen = app.primaryScreen()
        if screen is not None:
            screen_width = max(1, screen.size().width())
            screen_height = max(1, screen.size().height())
        else:
            size = pyautogui.size()
            screen_width = max(1, size[0])
            screen_height = max(1, size[1])

        try:
            self.execute_thread = QThread(self)
            self.execute_worker = ScriptExecuteWorker(
                file_path=file_path,
                wait_time=self.wait_doubleSpinBox.value(),
                count=count,
                speed=self.spinbox_play_speed.value() / 100,
                end_key_text=self.end_key_combo.currentText(),
                screen_width=screen_width,
                screen_height=screen_height,
            )
            self.execute_worker.moveToThread(self.execute_thread)

            self.execute_thread.started.connect(self.execute_worker.run)
            self.execute_worker.progress.connect(self._on_execute_worker_progress)
            self.execute_worker.finished.connect(self._on_execute_worker_finished)
            self.execute_worker.finished.connect(self.execute_thread.quit)
            self.execute_worker.finished.connect(self.execute_worker.deleteLater)
            self.execute_thread.finished.connect(self.execute_thread.deleteLater)

            self.execute_thread.start()
        except Exception:
            traceback.print_exc()
            self.execute_status = False
            self.handle_restore()
            self.execute_thread = None
            self.execute_worker = None

    def key_menu_com(self, types, key):
        if types == "record":
            self.end_key = key
            self.end_key_button.setText(f"{key}")
        elif types == "execute":
            self.end_execute_key = key
            self.end_execute_button.setText(f"{key}")

    def join_team(self):
        id = self.add_team_lineEdit.text()
        if len(id) != 30:
            self.show_message_box("提示", "队伍id不正确!")
        else:
            TypedJSONClient("join_team", {"number": id})

    def set_variables(self, vars_dict, namespace=None):
        """
        通过变量名字符串动态修改指定命名空间中的变量值
        :param vars_dict: 字典格式 {变量名: 新值}
        :param namespace: 命名空间字典，默认使用全局作用域
        """
        namespace = namespace or globals()
        assignments = "; ".join([f"{k} = {repr(v)}" for k, v in vars_dict.items()])
        exec(assignments, namespace)

    def team(self):  # 创建队伍
        self.create_team_button.setVisible(False)  # 创建队伍按钮
        self.add_team_lineEdit.setVisible(False)  # 加入队伍标签
        self.add_team_button.setVisible(False)
        self.button_copy_id.setVisible(True)  # 复制ID按钮
        characters = string.ascii_letters + string.digits
        global random_string
        random_string = "".join(random.choices(characters, k=30))
        self.add_team_ID.setText(f"队伍ID为:{random_string}")
        self.add_team_ID.setVisible(True)
        TypedJSONClient("create_team", {"number": random_string})

    def team_c(self):
        captain = self.user1.combo_options.currentIndex()
        member = self.user2.combo_options.currentIndex()
        types = None
        if member == 0:
            types = "handle_send"
        elif member == 1:
            types = "user_send"
        elif member == 2:
            types = "copy_send"
        elif member == 3:
            types = "information_update"
        elif member == 4:
            types = "record_execute"
        else:
            types = "unknown"
        if types == "unknown":
            self.show_message_box("提示", "未知类型")
            return
        TypedJSONClient("team_execute", {"types": types})
        if captain == 0:
            self.Handle_Send()
        elif captain == 1:
            self.Send_QQ()
        elif captain == 2:
            self.Send_Copy()
        elif captain == 3:
            self.QQ_image_update()
        elif captain == 4:
            self.Click_Record_execute()
        else:
            self.show_message_box("提示", "未知类型")

    def deal_team_send(self, types):
        if types == "handle_send":
            self.team_execute_prompt.setText(f"即将发送QQ句柄消息")
            self.Handle_Send()
        elif types == "user_send":
            self.team_execute_prompt.setText(f"即将发送@QQ消息")
            self.Handle_Send()
        elif types == "copy_send":
            self.team_execute_prompt.setText(f"即将发送QQ复制消息")
            self.Handle_Send()
        elif types == "information_update":
            self.team_execute_prompt.setText(f"即将进行QQ信息更新")
            self.Handle_Send()
        elif types == "record_execute":
            self.team_execute_prompt.setText(f"即将开始执行自动脚本")
            self.Handle_Send()
        else:
            self.team_execute_prompt.setText(f"未知类型 错误!")
            self.show_message_box("提示", "未知类型")

    def copy_team_number(self):
        global random_string
        clipboard = QApplication.clipboard()
        clipboard.setText(f"{random_string}")

    def showEvent(self, e):
        if self.first_image == False:
            if Theme == "Custom":  # 自定义图片背景设置
                with open("config.json", "r") as file:
                    config = json.load(file)
                Path_Custom_S = config.get("Path")
                print(Path_Custom_S)
                self.should_draw = "Custom"
                im = Image.open(Path_Custom_S)
                reim = im.resize((self.width(), self.height()))  # 宽*高
                reim.save(
                    "./temp/background_custom.png", dpi=(400, 400)
                )  ##200.0,200.0分别为想要设定的dpi值
                # 打开图片
                image = Image.open("./temp/background_custom.png")
                # 应用高斯模糊，radius参数控制模糊程度（半径越大越模糊）
                blurred_image = image.filter(ImageFilter.GaussianBlur(radius=5))
                # 保存处理后的图片
                blurred_image.save("./temp/background_custom.png")

                palette = QPalette()
                palette.setBrush(
                    QPalette.Background, QBrush(QPixmap("./temp/background_custom.png"))
                )

                self.setPalette(palette)
                trp = transparent / 100
                # 设置整体透明度（会影响所有子元素）
                self.sidebar.setGraphicsEffect(QGraphicsOpacityEffect(opacity=trp))
                self.stack.setGraphicsEffect(QGraphicsOpacityEffect(opacity=trp - 0.1))
                print("成功设置背景")

                del Path_Custom_S
                self.first_image = True

    def show_message_box(self, head, message):
        QMessageBox.question(self, head, message, QMessageBox.Yes)

    def handle_message(self, title, content):
        reply = QMessageBox.information(self, title, content, QMessageBox.Yes)


if __name__ == "__main__":
    try:
        # 适应高DPI设备
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        # 适应Windows缩放
        QtGui.QGuiApplication.setAttribute(
            QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
    except Exception as e:
        logging.exception(
            str(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()))
            + "错误:"
            + str(e)
        )
    app = QApplication(sys.argv)
    translator = QTranslator()
    translator.load("./mod/trans/qt_zh_CN.qm")
    app.installTranslator(translator)
    if initial == False:
        import ui.Agreement

        win = ui.Agreement.AgreementWindow()
        win.show()
        app.exec_()
        if ui.Agreement.User_Agree == False:
            sys.exit()
        else:
            with open("config.json", "r") as file:
                config = json.load(file)
            config["Initial"] = True
            with open("config.json", "w") as json_file:
                json.dump(config, json_file, indent=4)
    # 创建全局变量字典，传递给登录窗口
    globals_dict = {
        "remember": remember,
        "AutoLogin": AutoLogin,
        "Account": Account,
        "Password": Password,
        "Number_People": Number_People,
        "Version": Version,
        "city_name": city_name,
        "system": system,
        "computer_name": computer_name,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    window_login = login_window.LoginWindow(
        s, connect_status, stdout_stream, stderr_stream, globals_dict
    )

    # 连接信号到处理函数
    def handle_login_success(login_data):
        # 延迟导入UI模块
        global ui
        import ui.userinfo, ui.console_window, ui.fileEdit, ui.hotkey_record, ui.number_prompt

        # 更新全局变量
        for key, value in login_data.items():
            if key in globals():
                globals()[key] = value
        # 关闭登录窗口，显示主窗口
        global \
            window_s, \
            Ask, \
            Theme, \
            Sound, \
            ClosePrompt, \
            CloseExecute, \
            Path_Custom_S, \
            transparent, \
            FPS
        window_s = False
        # 读取JSON文件
        with open("config.json", "r") as file:
            config = json.load(file)
        Sound = config.get("Sound", True)
        ClosePrompt = config.get("ClosePrompt", True)
        CloseExecute = config.get("CloseExecute", "Close")
        Theme = config.get("Theme", "White")  # 主题
        if Theme not in ("White", "Custom"):
            Theme = "White"
        if Theme == "Custom":
            Path_Custom_S = config.get("Path")
        transparent = config.get("transparent", 30)
        FPS = config.get("FPS", 16)
        new_mainpage.Name = Name
        new_mainpage.Account = Account
        new_mainpage.Version = Version
        new_mainpage.information = information
        new_mainpage.avatar_load_status = avatar_load_status
        new_mainpage.position_status = position_status
        new_mainpage.textedit_position = textedit_position
        new_mainpage.send_position = send_position
        new_mainpage.mode = Account
        new_mainpage.s = s

        windows = Ui_Form(stdout_stream, stderr_stream)
        windows.show()

    # 连接信号到槽函数
    window_login.login_successful.connect(handle_login_success)
    if AutoLogin == True and connect_status != None:
        time.sleep(0.1)
        login_result = window_login.LOGIN("login")
    elif connect_status == None:  # 离线模式
        login_result = window_login.LOGIN("offline_login")
    else:
        window_login.show()
    sys.exit(app.exec_())
os._exit(0)
