import hashlib
import logging
import shutil
import string
import subprocess
import traceback
import json
import win32com
import win32gui
import win32con
import pyautogui
import time
import random
import os
import requests
import pygetwindow as gw
import re
import pyperclip
from PIL import Image
from PyQt5.QtCore import QThread, pyqtSignal
from bs4 import BeautifulSoup
import pandas as pd
from colorama import Fore
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
def is_running_as_exe():
    return hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS')


os.environ['NO_PROXY'] = 'https://fcyang.cn'
os.environ['NO_PROXY'] = 'https://www.lanzoup.com/'
os.environ['NO_PROXY'] = 'http://myip.ipip.net'
os.environ['NO_PROXY'] = 'http://api.openweathermap.org/data/2.5/weather'
os.environ['NO_PROXY'] = 'https://q1.qlogo.cn/'
os.environ['NO_PROXY'] = 'https://music.163.com'
os.environ['NO_PROXY'] = 'https://q1.qlogo.cn/'
os.environ['NO_PROXY'] = 'https://q1.qlogo.cn/'



def print_fuchen():
    # 定义每个字母的10行结构（7列宽）
    letters = {
        'F': [
            '███████',
            '█      ',
            '█      ',
            '█      ',
            '██████ ',
            '█      ',
            '█      ',
            '█      ',
            '█      ',
        ],
        'U': [
            '█     █',
            '█     █',
            '█     █',
            '█     █',
            '█     █',
            '█     █',
            '█     █',
            '█     █',
            ' █████ ',
        ],
        'C': [
            '  █████',
            ' █     ',
            '█      ',
            '█      ',
            '█      ',
            '█      ',
            '█      ',
            ' █     ',
            '  █████',
        ],
        'H': [
            '█     █',
            '█     █',
            '█     █',
            '█     █',
            '███████',
            '█     █',
            '█     █',
            '█     █',
            '█     █',
        ],
        'E': [
            '███████',
            '█      ',
            '█      ',
            '█      ',
            '██████ ',
            '█      ',
            '█      ',
            '█      ',
            '███████',
        ],
        'N': [
            '█     █',
            '██    █',
            '█ █   █',
            '█  █  █',
            '█   █ █',
            '█    ██',
            '█     █',
            '█     █',
            '█     █',
        ],
        ' ': ['      '] * 9  # 空格分隔
    }

    # 组合字母 "F U C H E N"（中间加空格）
    word = ['F', ' ', 'U', ' ', 'C', ' ', 'H', ' ', 'E', ' ', 'N']
    # 逐行输出
    for row in range(9):
        line = []
        for char in word:
            line.append(letters[char][row])
        print(' '.join(line))  # 字母间用空格分隔


def parse_version(version_str):
    """解析版本号字符串，返回前两位数字组成的元组"""
    # 去除所有非数字和点的字符
    cleaned = re.sub(r'[^\d.]', '', version_str)
    parts = cleaned.split('.') if cleaned else []

    version = []
    for part in parts[:2]:  # 只取前两部分
        version.append(int(part) if part.isdigit() else 0)

    # 补足两位（主版本.次版本）
    while len(version) < 2:
        version.append(0)

    return tuple(version[:2])

def update_console_theme(theme):
    with open("config.json", "r") as file:
        U_data = json.load(file)
    U_data["console_theme"] = theme
    with open("config.json", "w") as file:
        json.dump(U_data, file, indent=4)
# json配置文件内容
config_dic = {
            "Remember": False,
            "AutoLogin": False,
            "Account": "",
            "Password": "",
            "Sound": True,
            "Initial": False,
            "Theme": "White",
            "Path": None,
            "ClosePrompt": True,
            "CloseExecute": "Close",
            "ReStart": False,
            "FPS": 30,
            "transparent": 80,
            "position": [[None, None], [None, None]],
            "tourist_status": False,
            'tourist_number':0,
            "update": False,
            "console_theme":'dark'
        }

keycode_dict = {

    # === 鼠标按键 ===
    "鼠标中键": 4,  "鼠标右键": 2,  "侧键后退":8, "侧键前退":16,
    # === 字母和数字键 ===
    "a": 65, "b": 66, "c": 67, "d": 68, "e": 69, "f": 70, "g": 71,
    "h": 72, "i": 73, "j": 74, "k": 75, "l": 76, "m": 77, "n": 78,
    "o": 79, "p": 80, "q": 81, "r": 82, "s": 83, "t": 84, "u": 85,
    "v": 86, "w": 87, "x": 88, "y": 89, "z": 90,
    "0": 48, "1": 49, "2": 50, "3": 51, "4": 52,
    "5": 53, "6": 54, "7": 55, "8": 56, "9": 57,

    # === 数字小键盘 ===
    "numpad0": 96, "numpad1": 97, "numpad2": 98, "numpad3": 99,
    "numpad4": 100, "numpad5": 101, "numpad6": 102, "numpad7": 103,
    "numpad8": 104, "numpad9": 105,
    "numpad*": 106, "numpad+": 107, "numpadenter": 108,
    "numpad-": 109, "numpad.": 110, "numpad/": 111,

    # === 功能键 ===
    "f1": 112, "f2": 113, "f3": 114, "f4": 115, "f5": 116,
    "f6": 117, "f7": 118, "f8": 119, "f9": 120, "f10": 121,
    "f11": 122, "f12": 123,

    # === 控制键 ===
    "backspace": 8, "tab": 9, "clear": 12, "enter": 13,
    "shift": 16, "control": 17, "alt": 18, "capslock": 20,
    "esc": 27, "spacebar": 32, "pageup": 33, "pagedown": 34,
    "end": 35, "home": 36, "leftarrow": 37, "uparrow": 38,
    "rightarrow": 39, "downarrow": 40, "insert": 45, "delete": 46,
    "numlock": 144,
    ";": 186, "=": 187, ",": 188, "-": 189, ".": 190, "/": 191,
    "`": 192, "[": 219, "\\": 220, "]": 221, "'": 222,

    # === 多媒体键 ===
    "volumeup": 175, "volumedown": 174, "volumemute": 173,
    "mediastop": 179, "browserback": 172, "mail": 180,
    "search": 170, "favorites": 171
}
def get_exefile_name():
    process_name = sys.argv[0]
    file_name = os.path.basename(process_name)
    Fuchen_name, Fuchen_type = os.path.splitext(file_name)
    return Fuchen_name, Fuchen_type, file_name


def get_dwonload_link():
    try:
        # 目标 URL
        url = 'https://fcyang.cn'

        # 使用 requests 获取页面内容
        response = requests.get(url)
        print(response.status_code)
        # 检查请求是否成功
        if response.status_code == 200:
            # 解析 HTML 内容
            soup = BeautifulSoup(response.text, 'html.parser')

            version_div = soup.find(id="download_version")
            if version_div and "link" in version_div.attrs:
                link = version_div["link"]
                return link
    except:
        return "ERROR"


def get_update_data(local_version):
    try:
        # 目标 URL
        url = 'https://fcyang.cn'

        # 使用 requests 获取页面内容
        response = requests.get(url)

        # 检查请求是否成功
        if response.status_code == 200:
            # 解析 HTML 内容
            soup = BeautifulSoup(response.text, 'html.parser')
            version = None
            link = None

            version_div = soup.find(id="version")
            if version_div and "data-version" in version_div.attrs:
                version = version_div["data-version"]


            version_div = soup.find(id="update_link")
            if version_div and "link" in version_div.attrs:
                link = version_div["link"]
            local_version_list = local_version.split('.')
            if len(local_version_list) == 3:
                if '-' in local_version_list[2]:
                    local_version_list[2] = local_version_list[2].split('-')[0]
            get_version_list = version.split('.')
            command = '当前版本已是最新版 无需更新'
            update = False
            update_link = None
            if len(local_version_list) == 2 and len(get_version_list) == 3:
                command = f"发现新版本{version} 是否更新?"
                update = True
                update_link = link
            elif len(local_version_list) == 3 and len(get_version_list) == 3:
                if int(local_version_list[2]) < int(get_version_list[2]):
                    command = f"发现新版本{version} 是否更新?"
                    update = True
                    update_link = link
            elif len(local_version_list) == 2 and len(get_version_list) == 2:
                if int(local_version_list[1]) < int(get_version_list[1]):
                    command = f"发现新版本{version} 是否更新?"
                    update = True
                    update_link = link
            return command, update, update_link

        else:
            return f"请求失败，状态码: {response.status_code}"
    except Exception as e:
        traceback.print_exc()
        return "版本信息获取失败 请重试"


def initialization():  # 初始化
    try:  # 读取JSON文件 若未检测到则初始化
        if not os.path.exists('config.json'):
            raise Exception("未找到配置文件 即将开始初始化")
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                config = json.load(f)
            if config['update'] == True:
                raise Exception("更新初始化")
    except Exception as e:  # 初始化
        if str(e) == "未找到配置文件 即将开始初始化":
            with open("config.json", "w") as json_file:
                json.dump(config_dic, json_file, indent=4)
        else:
            # 读取 JSON 文件
            with open('config.json', 'r') as f:
                config = json.load(f)
            config['update'] = False
            # 重新写入文件（覆盖原文件）
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)  # indent 保持美观格式
        # 创建快捷方式
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        Fuchen_name = get_exefile_name()[0]
        shortcut_name = f'{Fuchen_name}.lnk'
        original_file_path = rf'{os.getcwd()}\{Fuchen_name}.exe'
        shortcut_path = os.path.join(desktop_path, shortcut_name)
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = original_file_path
        shortcut.WorkingDirectory = os.path.dirname(original_file_path)  # 设置快捷方式的起始位置为exe文件所在的文件夹
        shortcut.save()
        # 文件夹路径
        folder_pathP = r'C:\Fuchen'
        # 创建文件夹
        if not os.path.exists(folder_pathP):
            os.makedirs(folder_pathP)
        # 创建文本文件的路径
        file_pathP = os.path.join(folder_pathP, 'path.txt')
        # 获取脚本当前目录
        current_directory = os.getcwd()
        # 将当前目录写入文件
        with open(file_pathP, 'w') as file:
            file.write(current_directory)

        # 创建文本文件的路径
        file_path = os.path.join(folder_pathP, '关于此文件夹.txt')
        # 将当前目录写入文件
        with open(file_path, 'w') as file:
            file.write("此文件夹为Fuchen文件夹\n主要记录了Fuchen的初始化路径 以用来安装扩展包等\n如删除文件夹 可能会导致扩展包安装不成功\n此文件夹占用内存较小 不建议删除\n更多软件信息请登录官网:https://fcyang.cn/查看")


def copy_config_file(file_path):

    # 读取 JSON 文件
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        json_data = {}

    # 更新 JSON 数据
    # 1. 添加缺少的键值
    for key, default_value in config_dic.items():
        if key not in json_data:
            json_data[key] = default_value

    # 2. 删除多余的键值
    extra_keys = [key for key in json_data if key not in config_dic]
    for key in extra_keys:
        del json_data[key]

    # 重新写入 JSON 文件
    with open('config.json', "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)


def QQ_Information_Update(rest):
    try:
        # 读取文本文件内容
        with open('./mod/dic/name.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # 从列表中随机选择一行
        random_line = random.choice(lines[0:2304])
        folder_path = './mod/picture'
        # 检查文件夹是否存在
        if not os.listdir(folder_path):
            return "Not Found"
        else:
            # 获取文件夹中的所有文件（不包括子文件夹）
            files = [f for f in os.listdir(folder_path) if
                     os.path.isfile(os.path.join(folder_path, f))]
            random_file = random.choice(files)
            # 构建完整的文件路径
            file_path = os.path.abspath(os.path.join(folder_path, random_file))
            # 从文件名中提取数字部分
            file_name = os.path.basename(file_path)
            number = re.search(r'\d+', file_name).group()

            def fetch_nickname(url):
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        print(data)
                        if data.get('code') == 200:
                            if data.get('code') == 200:
                                # 尝试第一种数据结构（name在根级）
                                if 'name' in data:
                                    return data.get('name')
                                # 尝试第二种数据结构（name在data对象内）
                                elif 'data' in data and isinstance(data['data'], dict):
                                    return data['data'].get('name')
                except:
                    pass
                return None

            # 要尝试的API列表（替换为实际API地址）
            api_urls = [
                f"https://api.ilingku.com/int/v1/qqname?qq={number}",
                f"http://api.mmp.cc/api/qqname?qq={number}"
            ]

            # 遍历所有API地址尝试获取
            for url in api_urls:
                nickname = fetch_nickname(url)
                if nickname:  # 获取成功立即终止循环
                    break
            else:
                # 全部请求都失败时保持原值（这里用pass示意，实际需替换为你的原值变量）
                pass
        # 获取窗口对象 修改头像
        QQwindow = gw.getWindowsWithTitle("QQ")[0]
        window_position = (QQwindow.left + 50, QQwindow.top + 80)
        # 执行点击操作
        pyautogui.click(window_position)
        time.sleep(rest)

        QQwindow = gw.getWindowsWithTitle("我的资料")[0]
        window_position = (QQwindow.left + 670, QQwindow.top + 50)
        # 执行点击操作
        pyautogui.click(window_position)
        time.sleep(rest)

        QQwindow = gw.getWindowsWithTitle("编辑资料")[0]  # 修改名称
        window_position = (QQwindow.left + 100, QQwindow.top + 100)
        # 执行点击操作
        for i in range(3):
            pyautogui.click(window_position)

        pyperclip.copy(nickname)
        # 等待一段时间，以确保复制操作完成
        time.sleep(rest)
        # 模拟键盘按键粘贴字符串
        pyautogui.hotkey('ctrl', 'v')
        # 执行点击操作
        window_position = (QQwindow.left + 260, QQwindow.top + 720)
        time.sleep(rest)
        pyautogui.click(window_position)

        time.sleep(rest)
        QQwindow = gw.getWindowsWithTitle("我的资料")[0]  # 修改头像
        window_position = (QQwindow.left + 100, QQwindow.top + 450)
        # 执行点击操作
        pyautogui.click(window_position)

        time.sleep(rest)
        QQwindow = gw.getWindowsWithTitle("更换头像")[0]
        window_position = (QQwindow.left + 80, QQwindow.top + 60)
        pyautogui.click(window_position)
        time.sleep(0.6)

        QQwindow = gw.getWindowsWithTitle("打开")[0]
        window_position = (QQwindow.left + 240, QQwindow.top + QQwindow.height - 70)
        # 执行点击操作
        pyautogui.click(window_position)

        pyperclip.copy(file_path)

        # 等待一段时间，以确保复制操作完成
        time.sleep(0.1)

        # 模拟键盘按键粘贴字符串
        pyautogui.hotkey('ctrl', 'v')

        window_weight = QQwindow.width
        window_height = QQwindow.height
        target_y_relative = window_height - 70  # 相对于窗口左上角的y坐标
        target_x_relative = window_weight - 50
        # 计算在屏幕上的绝对坐标
        target_x = QQwindow.left + target_x_relative
        target_y = QQwindow.top + target_y_relative
        # 执行点击操作
        pyautogui.click(target_x, target_y)

        QQwindow = gw.getWindowsWithTitle("更换头像")[0]
        window_position = (QQwindow.left + 250, QQwindow.top + 600)
        # 执行点击操作
        pyautogui.click(window_position)
        return 0
    except Exception as e:
        traceback.print_exc()
        print(e)
        return e


def hash_string(input_str, algorithm='sha256'):
    # 创建哈希对象
    if algorithm == 'sha256':
        hasher = hashlib.sha256()
    elif algorithm == 'sha512':
        hasher = hashlib.sha512()
    else:
        raise ValueError("不支持的算法，请输入 sha256 或 sha512")

    # 更新哈希对象（仅处理原始字符串）
    hasher.update(input_str.encode('utf-8'))

    # 返回十六进制摘要
    return hasher.hexdigest()


def Convert_File(put, output, put_file, output_folder, file_name, self):
    output_path = output_folder + '\\' + file_name + '.' + output
    def convert_image_format():
        # 打开待转换图片
        image = Image.open(put_file)
        output_format = output.upper()
        # 进行图片格式转换并保存
        if output_format == "PNG":
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.save(output_path, format="PNG")
        elif output_format == "JPG":
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.save(output_path, format="JPEG", quality=100)  # 设置高质量参数
        elif output_format == "GIF":
            image.save(output_path, format="GIF")
        elif output_format == "PDF":
            image.save(output_path, 'PDF', resolution=100.0)
        else:
            raise Exception("文件格式错误")

    try:
        convert_image_format()
        return 0
    except Exception as e:
        print(e)
        return e


def QQ_Group_Obtain(mode, output_folder ,id, Sex, Year, join_Date, send_Date, group_Lv):
    try:
        if mode == 'Edge':
            driver = webdriver.Edge()
        elif mode == 'Chrome':
            driver = webdriver.Chrome()
        elif mode == 'Ie':
            driver = webdriver.Ie()
        else:
            raise Exception("选择类型错误 请重试")
        # 打开网页
        driver.get('https://qun.qq.com/member.html')
    except:
        return "Open Failed"
    # 等待元素存在，然后等待元素不可见，然后进行下一步操作
    try:
        # 等待元素存在  数字为最长等待时间
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "loginWin"))
        )
        #play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
        result = pyautogui.confirm(
            "请在浏览器中登录QQ并关闭此窗口再进行下一步操作\n\n若要取消操作请点击取消关闭此窗口")
        if result == "Cancel":
            driver.quit()
            return "Cancel"
        # 等待元素不可见
        WebDriverWait(driver, 100).until_not(
            EC.visibility_of_element_located((By.ID, "loginWin"))
        )
        #play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
        result = pyautogui.confirm(
            "登录成功 接下来请先关闭此窗口再进行群聊选择\n\n若要取消操作请点击取消关闭此窗口")
        if result == 'Cancel':
            driver.quit()
            return "Cancel"
        try:  # 群选择成功
            # 等待元素出现
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-dialog.on"))
            )

            # 等待元素消失
            WebDriverWait(driver, 100).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-dialog.on"))
            )
        except:  # 跳过群选择
            pass
        result = pyautogui.confirm(
            "群聊已确认 接下来程序将自动处理数据 请勿关闭或点击浏览器窗口 点击确认以继续\n\n若要取消操作请点击取消关闭此窗口")
        if result == 'Cancel':
            driver.quit()
            return "Cancel"
        # 使用XPath提取元素内容
        element = driver.find_element(By.XPATH, '//span[@id="groupTit"]')
        text = element.text
        # 模拟滚动
        SCROLL_PAUSE_TIME = 0.5  # 滚动间隔时间
        # 获取页面初始高度
        number = 0
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            number = number + 1
            # 模拟滚动到页面底部
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # 等待页面加载
            time.sleep(SCROLL_PAUSE_TIME)

            # 计算新高度并判断是否到达页面底部
            new_height = driver.execute_script("return document.body.scrollHeight")
            print("\r正在处理第{}个页面".format(number), end="")
            if new_height == last_height:
                break
            last_height = new_height

        # 等待页面加载完全
        time.sleep(2)

        # 获取整个网页的 HTML 内容
        html_content = driver.page_source

        # 将 HTML 内容保存到文件
        with open('./temp/page_content.html', 'w', encoding='utf-8') as file:
            file.write(html_content)

        # 关闭浏览器
        driver.quit()

        # 处理特殊字符(非法字符)
        def remove_nonprintable_chars(text):
            cleaned_text = ''
            for char in text:
                if char.isalnum() or char in string.printable or char.isspace():
                    cleaned_text += char
            return cleaned_text

        # 从本地文件中读取HTML内容（将 'your_file.html' 替换为你的文件路径）
        with open('./temp/page_content.html', 'r', encoding='utf-8') as file:
            html_content = file.read()

        # 创建 BeautifulSoup 对象
        soup = BeautifulSoup(html_content, 'html.parser')
        # 找到具有指定 id 的表格元素
        table = soup.find('table', {'id': 'groupMember'})
        # 在表格中找到所有包含 'list' 类的 tbody 元素
        tbody_elements = table.find_all('tbody', class_='list')
        data = []  # 列表用于存储提取的数据

        for tbody in tbody_elements:
            # 在每个 tbody 中找到具有 'mb' 类的元素并提取信息
            elements = tbody.find_all(class_=lambda x: x and 'mb' in x)
            for element in elements:
                try:
                    # 提取并清理（或处理）数据
                    gender = remove_nonprintable_chars(
                        element.find_all('td')[1].text.strip())  # 序号
                    name = remove_nonprintable_chars(
                        element.find_all('td')[2].text.strip())  # 名称
                    group_name = remove_nonprintable_chars(
                        element.find_all('td')[3].text.strip())  # 群名称
                    Qid = remove_nonprintable_chars(
                        element.find_all('td')[4].text.strip())  # QQ号
                    sex = remove_nonprintable_chars(
                        element.find_all('td')[5].text.strip())  # 性别
                    QQ_year = remove_nonprintable_chars(
                        element.find_all('td')[6].text.strip())  # QQ年龄
                    join_date = remove_nonprintable_chars(
                        element.find_all('td')[7].text.strip())  # 进群日期
                    group_lv = remove_nonprintable_chars(
                        element.find_all('td')[8].text.strip())  # 群等级
                    send_date = remove_nonprintable_chars(
                        element.find_all('td')[9].text.strip())  # 最后发言日期

                    # 以字典格式存储提取的数据
                    dic = {"序号": gender,
                           '名称': name,
                           '群昵称': group_name, }
                    if id:
                        dic['QQ号'] = Qid
                    if Sex:
                        dic['性别'] = sex
                    if Year:
                        dic['QQ年龄'] = QQ_year
                    if join_Date:
                        dic['进群日期'] = join_date
                    if send_Date:
                        dic['最后发言日期'] = send_date
                    if group_Lv:
                        dic['群等级'] = group_lv
                    data.append(dic)
                except:
                    pass

        df = pd.DataFrame(data)
        df.to_excel(output_folder + f'\\{text}.xlsx', index=False)
        return f"文件保存成功: \n{output_folder}\\{text}.xlsx"
    except Exception as e:
        print(e)
        traceback.print_exc()
        return e


def write_update_bat():
    """
        生成自动清理文件夹的批处理脚本

        :param target_folder: 需要删除的目标文件夹绝对路径
        :param output_path: 生成的bat文件保存路径
        """
    now_path = os.getcwd()

    bat_script = f'''@echo off
    setlocal enabledelayedexpansion

    :: 配置要删除的文件夹路径
    set "target_folder={now_path.replace(os.sep, '/')}"

    :CHECK_EXIST
    if not exist "!target_folder!" (
        echo 文件夹不存在，无需删除
        exit /b
    )

    :DELETE_ATTEMPT
    echo 正在尝试删除 [!target_folder!]...
    rmdir /s /q "!target_folder!" 2>nul

    if exist "!target_folder!" (
        echo 文件夹被占用，等待3秒后重试...
        timeout /t 3 /nobreak >nul
        goto DELETE_ATTEMPT
    ) else (
        echo 文件夹删除成功！
        echo 正在删除批处理文件自身...
        (goto) 2>nul & (
            timeout /t 1 /nobreak >nul
            del /f /q "%~f0"
        )
        exit /b
    )

    endlocal
    '''

    with open('C:\\Fuchen\\Fuchen_Update.bat', 'w', encoding='gbk') as f:  # Windows系统建议使用GBK编码
        f.write(bat_script)

def run_update_bat(bat_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    #bat_path = "C:\\Fuchen\\Fuchen_Update.bat"

    # 创建独立进程配置
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    try:
        # 使用Popen启动独立进程
        subprocess.Popen(
            ["cmd.exe", "/C", bat_path],  # 显式调用cmd解释器
            shell=False,  # 避免额外shell层次
            startupinfo=startupinfo,  # 隐藏控制台窗口
            stdin=subprocess.DEVNULL,  # 断开输入流
            stdout=subprocess.DEVNULL,  # 丢弃标准输出
            stderr=subprocess.DEVNULL,  # 丢弃错误输出
            close_fds=True  # 关闭所有文件描述符
        )
        print("批处理文件已启动，Python脚本继续执行...")
    except Exception as e:
        print(f"启动失败: {str(e)}")

def new_update(new_path,old_path,sp):
    # 获取旧版本文件夹路径（假设EXEA在旧文件夹内）
    OLD_DIR = old_path
    try:
        print(OLD_DIR)
        print(new_path)
    except:
        traceback.print_exc()
    if is_running_as_exe():
        # 定义新版本路径（根据实际下载位置调整）
        NEW_EXE_PATH = new_path  # 示例路径

        # 生成批处理脚本内容
        bat_content = f"""
        @echo off
        echo 等待1秒...
        timeout /t 1 /nobreak >nul
        echo 继续执行
        
        REM 终止所有旧进程
        taskkill /F /IM "Fuchen.exe" >nul
        
        echo 等待1秒...
        timeout /t 1 /nobreak >nul
        echo 继续执行
        
        REM 启动新版本
        start "" "{sp}"
    
    
        REM 强制删除旧文件夹（包括自身）
        rd /s /q "{OLD_DIR}"
    
        REM 删除批处理自身（最后一步）
        del "%~f0"
        """

        # 将脚本写入临时目录（避免路径占用）
        bat_path = os.path.join('C:\\Fuchen', "cleanup_script.bat")
        with open(bat_path, "w") as f:
            f.write(bat_content)

        # 以隐藏窗口方式启动清理脚本
        subprocess.Popen(
            ["cmd.exe", "/C", bat_path],
            shell=True
        )
        logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + f"旧版程序路径：{old_path}")
        logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + f"新版程序路径：{new_path}")
        logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "旧版程序已退出")
        # 立即退出旧进程（释放文件占用）
        sys.exit(0)

class WindowController:
    def __init__(self):
        self.current_hwnd = None
        self.window_rect_cache = {}
        self.default_pause = 0.25
        self.variables = {}  # 新增变量存储字典

    def load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            content = re.sub(r'//.*?$|/\*.*?\*/', '', content, flags=re.MULTILINE | re.DOTALL)
            config = json.loads(content)
            # 转换结构键名为英文
            config = self.translate_config_keys(config)
            # 读取全局设置
            self.default_pause = config.get('settings', {}).get('global_interval', 0.5)
            # 存储变量（保留变量名的原始语言）
            self.variables = {k: v for k, v in config.get('settings', {}).items() if k != 'global_interval'}
            return config

    def translate_config_keys(self, config):
        key_mapping = {
            # 结构键名映射
            '设置': 'settings',
            '场景': 'scenarios',
            '窗口': 'window',
            '标题': 'title',
            '步骤': 'steps',
            '操作': 'action',
            '全局间隔': 'global_interval',
            '次数': 'times',
            '等待': 'wait',
            '相对': 'relative',
            '持续时间': 'duration',
            '文本': 'text',
            '按键': 'keys',
            '关闭': 'close',
            '热键': 'hotkey',
            '输入': 'typewrite',
            '点击': 'click',
            '拖拽': 'drag',
            '坐标X': 'x',
            '坐标Y': 'y',
            '间隔': 'interval',
            '按钮': 'button'
        }
        return self._translate_keys_recursive(config, key_mapping)

    def _translate_keys_recursive(self, obj, mapping):
        if isinstance(obj, dict):
            translated = {}
            for k, v in obj.items():
                # 转换当前层级的键名
                new_key = mapping.get(k, k)
                # 递归处理子对象
                translated[new_key] = self._translate_keys_recursive(v, mapping)
            return translated
        elif isinstance(obj, list):
            return [self._translate_keys_recursive(item, mapping) for item in obj]
        else:
            return obj

    def resolve_parameter(self, value):
        """增强版变量解析，支持$前缀和数组索引"""
        if isinstance(value, list):
            return [self.resolve_parameter(item) for item in value]
        elif isinstance(value, str) and value.startswith("$"):
            # 移除$前缀并处理数组索引
            var_expression = value[1:]

            # 处理数组索引格式（如 "var_name[0]"）
            if '[' in var_expression and ']' in var_expression:
                var_part = var_expression.split('[', 1)[0]
                index = int(var_expression.split('[', 1)[1].split(']', 1)[0])
                var_value = self.variables.get(var_part)

                if isinstance(var_value, (list, tuple)) and index < len(var_value):
                    return var_value[index]
                raise ValueError(f"无效的变量索引: {value}")

            # 处理普通变量
            if var_expression in self.variables:
                return self.variables[var_expression]
            raise ValueError(f"未定义的变量: {value}")

        # 非变量值直接返回
        return value

    def find_window(self, title):
        if title == '微信':
            hwnd = win32gui.FindWindow("WeChatMainWndForPC", "微信")
            if hwnd == 0:
                raise WindowNotFoundError(f"Window not found: {title}")
            return hwnd
        elif title == 'QQ':
            hwnd = win32gui.FindWindow('TXGuiFoundation', title)  #旧版QQ
            if hwnd == 0:
                hwnd = win32gui.FindWindow('Chrome_RenderWidgetHostHWND', 'Chrome Legacy Window')  #新版QQ
                if hwnd == 0:
                    raise WindowNotFoundError(f"Window not found: Chrome Legacy Window #新版QQ")
                return hwnd
            return hwnd
        hwnd = win32gui.FindWindow(None, title)
        if hwnd == 0:
            raise WindowNotFoundError(f"Window not found: {title}")
        return hwnd

    def activate_window(self, hwnd, wait_time=1.0):
        if hwnd != self.current_hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            self.current_hwnd = hwnd
            time.sleep(wait_time)
            self.window_rect_cache[hwnd] = win32gui.GetWindowRect(hwnd)

    def get_window_origin(self, hwnd):
        if hwnd not in self.window_rect_cache:
            self.window_rect_cache[hwnd] = win32gui.GetWindowRect(hwnd)
        rect = self.window_rect_cache[hwnd]
        return (rect[0], rect[1])

    def execute_scenario(self, scenario):
        try:
            window_cfg = scenario["window"]
            # 解析带变量的窗口标题
            raw_title = window_cfg["title"]
            resolved_title = self.resolve_parameter(raw_title) if isinstance(raw_title, str) else raw_title

            hwnd = self.find_window(resolved_title)
            self.activate_window(hwnd, window_cfg.get("wait", 0.1))
            self.execute_steps(scenario["steps"], hwnd)


        except WindowNotFoundError as e:
            print(f"⚠️ 跳过场景: {str(e)}")
        except Exception as e:
            print(f"❌ 场景执行失败: {str(e)}")

    def execute_steps(self, steps, hwnd):
        origin_x, origin_y = self.get_window_origin(hwnd)

        for step in steps:
            try:
                self.execute_single_step(step, hwnd, origin_x, origin_y)
                time.sleep(step.get("pause", 0.5))
            except Exception as e:
                print(f"⏭️ 步骤跳过: {str(e)}")
                continue


    def execute_single_step(self, step, hwnd, origin_x, origin_y):
        # 解析所有参数中的变量
        resolved_step = {k: self.resolve_parameter(v) for k, v in step.items()}
        action = resolved_step["action"]

        if action == "click":
            x = resolved_step.get("x", 0)
            y = resolved_step.get("y", 0)
            if resolved_step.get("relative", True):
                x += origin_x
                y += origin_y

            pyautogui.click(
                x=x,
                y=y,
                clicks=resolved_step.get("clicks", 1),
                interval=resolved_step.get("interval", 0.1),
                button=resolved_step.get("button", "left")
            )
        elif action == "typewrite":
            pyautogui.typewrite(
                resolved_step["text"],
                interval=resolved_step.get("interval", 0.1)
            )
        elif action == "hotkey":
            pyautogui.hotkey(*resolved_step["keys"])
        elif action == "close":
            win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        else:
            raise ValueError(f"未知操作类型: {action}")

    def handle_click(self, step, origin_x, origin_y):
        x, y = step["x"], step["y"]
        if step.get("relative", True):
            x += origin_x
            y += origin_y

        pyautogui.click(
            x=x,
            y=y,
            clicks=step.get("clicks", 1),
            interval=step.get("interval", 0.1),
            button=step.get("button", "left")
        )

    def handle_drag(self, step, origin_x, origin_y):
        start_x = step["start_x"] + (origin_x if step.get("relative", True) else 0)
        start_y = step["start_y"] + (origin_y if step.get("relative", True) else 0)
        end_x = step["end_x"] + (origin_x if step.get("relative", True) else 0)
        end_y = step["end_y"] + (origin_y if step.get("relative", True) else 0)

        pyautogui.dragTo(
            x=end_x, y=end_y,
            duration=step.get("duration", 0.5),
            button=step.get("button", "left")
        )


class WindowNotFoundError(Exception):
    pass

