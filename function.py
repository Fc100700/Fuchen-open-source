import string
import subprocess
import traceback
import json
import win32com
import pyautogui
import time
import random
import os
import requests
import pygetwindow as gw
import re
import pyperclip
from PIL import Image
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys


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
    except:  # 初始化
        config = {
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
            "transparent": 30,
            "position": [[None, None], [None, None]]
        }
        with open("config.json", "w") as json_file:
            json.dump(config, json_file, indent=4)
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
            # 发送GET请求
            url = f"https://api.oioweb.cn/api/qq/info?qq={number}"  # 替换为实际的API端点
            try:
                response = requests.get(url)
                # 通过API调用来获取图片所对应用户的名称
                if response.status_code == 200:  # 调用成功
                    # 将JSON字符串解析为Python字典
                    data = response.json()
                    if data["code"] == 200:  # 调用成功
                        nickname = data["result"]["nickname"]
                    else:  # 调用失败
                        nickname = random_line
                else:  # 调用失败
                    nickname = random_line
            except:
                nickname = random_line

            print(nickname)

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
        return e


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
#write_update_bat()