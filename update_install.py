import json
import random
import shutil
import time
import traceback
import webbrowser
import zipfile
import os
import py7zr
import psutil
import requests
import re
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QTimer, QPropertyAnimation, Qt, QPoint
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QDialog, QLabel, QPushButton, QProgressBar, QHBoxLayout, \
    QGraphicsOpacityEffect, QWidget
from bs4 import BeautifulSoup
from lxml import etree
import urllib.parse

import function
import ui.style
'''此文件为自动安装扩展包脚本'''

os.environ['NO_PROXY'] = 'https://fcyang.cn'
os.environ['NO_PROXY'] = 'https://www.lanzoup.com/'

## 请求lanzouyun_url，获取transfer_url
def get_transfer_url(host_url, lanzouyun_url):
    lanzouyun_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'ccept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'codelen=1; pc_ad1=1',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    lanzouyun_response = requests.get(url=lanzouyun_url, headers=lanzouyun_headers)
    # print('[*] lanzouyun_response:', lanzouyun_response.text)

    if lanzouyun_response.status_code == 200:
        page_text = lanzouyun_response.text
        parser = etree.HTMLParser(encoding="utf-8")
        handled_html = etree.HTML(page_text, parser=parser)
        # 获取transfer_url地址
        transfer_url_src = handled_html.xpath('/html/body/div[3]/div[2]/div[4]/iframe/@src')[0]
        # 获取文件名称
        file_name = handled_html.xpath('/html/body/div[3]/div[1]/text()')[0]
        ## transfer_url
        transfer_url = host_url + transfer_url_src


        return (file_name, transfer_url)
    else:
        print('[*] 无法请求此链接，可能链接不存在或网络错误')
        exit()

def rand_ip():
    """生成随机IP地址"""
    first_part = ["218", "218", "66", "66", "218", "218", "60", "60", "202", "204", "66", "66", "66", "59", "61", "60",
                  "222", "221", "66", "59", "60", "60", "66", "218", "218", "62", "63", "64", "66", "66", "122", "211"]
    return f"{random.choice(first_part)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"


def get_lanzou_direct_url(url_update):
    '''headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "X-Forwarded-For": rand_ip(),
        "Client-IP": rand_ip()
    }

    try:
        # 处理原始URL
        url_parts = url.split(".com/")
        if len(url_parts) < 2:
            raise Exception("无效的蓝奏云链接格式")

        processed_url = f"https://www.lanzoup.com/{url_parts[-1]}"

        # 第一次请求获取页面内容
        print("正在请求初始页面:", processed_url)
        response = requests.get(processed_url, headers=headers, timeout=10)
        response.raise_for_status()

        if "文件取消分享了" in response.text:
            raise Exception("文件已取消分享")


        # 提取iframe链接
        iframe_match = re.search(r'<iframe.*?src=["\']/(.*?)["\']', response.text, re.DOTALL)
        if not iframe_match:
            raise Exception("无法提取iframe链接，可能页面结构已更新")

        iframe_url = f"https://www.lanzoup.com/{iframe_match.group(1)}"
        print("发现iframe地址:", iframe_url)

        # 请求iframe页面
        print("正在请求iframe页面...")
        iframe_response = requests.get(iframe_url, headers=headers, timeout=10)
        iframe_response.raise_for_status()


        # 提取签名参数
        sign_match = re.search(r"wp_sign\s*=\s*['\"](.*?)['\"]", iframe_response.text)
        if not sign_match:
            raise Exception("无法提取签名参数，可能页面结构已更新")

        sign = sign_match.group(1)
        print("获取到签名参数:", sign)

        # 查找post请求地址
        post_url_match = re.search(r'/ajaxm\.php\?file=\d+', iframe_response.text)
        if not post_url_match:
            raise Exception("无法提取POST请求地址")

        post_url = f"https://www.lanzoux.com{post_url_match.group()}"
        print("构建POST地址:", post_url)

        data = {
            "action": "downprocess",
            "signs": "?ctdf",
            "sign": sign,
            "kd": 1
        }

        # 发送POST请求
        print("正在发送POST请求...")
        post_headers = headers.copy()
        post_headers["Referer"] = iframe_url
        post_headers["Origin"] = "https://www.lanzoup.com"
        post_headers["Content-Type"] = "application/x-www-form-urlencoded"

        post_response = requests.post(post_url, headers=post_headers, data=data, timeout=10)
        print("POST响应状态码:", post_response.status_code)
        print("POST响应内容:", post_response.text)

        try:
            result = post_response.json()
        except json.JSONDecodeError:
            raise Exception(f"无效的JSON响应，服务器返回：{post_response.text[:200]}")

        if result.get("zt") != 1:
            raise Exception(f"获取下载链接失败：{result.get('inf', '未知错误')}")

        # 获取中间链接
        intermediate_url = f"{result['dom']}/file/{result['url']}"
        print("中间链接:", intermediate_url)

        # 获取最终直链
        print("正在获取最终直链...")
        final_headers = {
            "Referer": "https://developer.lanzoug.com",
            "Cookie": "down_ip=1; expires=Sat, 16-Nov-2019 11:42:54 GMT; path=/; domain=.baidupan.com",
            "User-Agent": headers["User-Agent"]
        }

        final_response = requests.head(intermediate_url,
                                       headers=final_headers,
                                       allow_redirects=False,
                                       timeout=10)

        direct_url = final_response.headers.get("Location")
        if not direct_url:
            direct_url = intermediate_url

        # 清理URL参数
        direct_url = re.sub(r'[?&]pid=.*?(?=&|$)', '', direct_url)
        return direct_url
    except requests.exceptions.RequestException as e:

        raise Exception(f"网络请求失败: {str(e)}")'''
    try:
        # 使用示例
        update_str = "Fuchen Get Url"
        update_key = function.hash_string(update_str, 'sha256')
        print(update_key)
        url = f"https://fcyang.cn/get_url.php?url={url_update}&key={update_key}"

        try:
            # 发送 GET 请求
            response = requests.get(url)

            # 检查请求是否成功
            if response.status_code == 200:
                # 解析 JSON 响应
                data = response.json()
                print(data)

                # 提取 downUrl
                down_url = data.get("downUrl")

                print("提取的下载链接:", down_url)
                return down_url
            else:
                print("请求失败，状态码:", response.status_code)

        except requests.exceptions.RequestException as e:
            print("请求发生错误:", e)
        except ValueError as e:
            print("JSON 解析错误:", e)
    except:
        raise Exception(f"网络请求失败: {str(e)}")

## 下载文件
def download_file(download_url, file_name):
    download_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'down_ip=1',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    download_response = requests.get(url=download_url, headers=download_headers)
    file_data = download_response.content
    with open('./' + file_name, 'wb') as save_file:
        # 保存文件数据
        save_file.write(file_data)
        save_file.close()

    print('文件下载完成')


class UnzipWorker(QObject):
    progress_updated = pyqtSignal(int)  # 进度更新信号 (0-100)
    finished = pyqtSignal()  # 完成信号
    error_occurred = pyqtSignal(str)  # 错误信号

    def __init__(self, zip_path, extract_dir):
        super().__init__()
        self.zip_path = zip_path
        self.extract_dir = extract_dir
        if os.path.exists(self.extract_dir):
            shutil.rmtree(self.extract_dir)
        else:
            print('不存在')
        self.timer = None
        self.extract_thread = None

    def run(self):
        try:
            total_size = self.get_uncompressed_size()
            os.makedirs(self.extract_dir, exist_ok=True)

            # 初始化进度更新定时器
            self.timer = QTimer()
            self.timer.timeout.connect(lambda: self.update_progress(total_size))
            self.timer.start(300)  # 每300毫秒更新一次

            # 启动解压线程
            self.extract_thread = ExtractThread(self.zip_path, self.extract_dir)
            self.extract_thread.finished.connect(self.on_extraction_finished)
            self.extract_thread.error_occurred.connect(self.on_error)
            self.extract_thread.start()

        except Exception as e:
            self.error_occurred.emit(str(e))

    def get_uncompressed_size(self):
        """获取7z文件解压后的总大小"""
        try:
            with py7zr.SevenZipFile(self.zip_path, 'r') as archive:
                return sum(file.uncompressed for file in archive.list())
        except Exception as e:
            raise Exception(f"获取压缩包大小时出错: {str(e)}")

    def update_progress(self, total_size):
        """更新解压进度"""
        try:
            current_size = sum(
                os.path.getsize(os.path.join(root, file))
                for root, _, files in os.walk(self.extract_dir)
                for file in files
            )
            progress = min(int((current_size / total_size) * 100), 100)
            self.progress_updated.emit(progress)
        except Exception as e:
            self.error_occurred.emit(f"更新进度时出错: {str(e)}")

    def on_extraction_finished(self):
        """解压完成处理"""
        if self.timer.isActive():
            self.timer.stop()
        self.progress_updated.emit(100)
        self.finished.emit()

    def on_error(self, error_msg):
        """错误处理"""
        if self.timer and self.timer.isActive():
            self.timer.stop()
        self.error_occurred.emit(error_msg)


class ExtractThread(QThread):
    """解压文件的工作线程"""
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, zip_path, extract_dir):
        super().__init__()
        self.zip_path = zip_path
        self.extract_dir = extract_dir

    def run(self):
        try:
            with py7zr.SevenZipFile(self.zip_path, 'r') as archive:
                archive.extractall(path=self.extract_dir)
            self.finished.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))



class DownloadWorker(QObject):
    progress_updated = pyqtSignal(int)  # 下载进度更新信号 (0-100)
    speed_updated = pyqtSignal(str)    # 下载速度更新信号
    finished = pyqtSignal()            # 下载完成信号
    error_occurred = pyqtSignal(str)   # 错误信号

    def __init__(self, download_url, file_name, expected_size):
        super().__init__()
        self.download_url = download_url
        self.file_name = file_name
        self.expected_size = expected_size  # 目标文件大小 (字节)
        self._is_downloading = True

    def run(self):
        try:
            download_headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'max-age=0',
                'cookie': 'down_ip=1',
                'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
            }

            start_time = time.time()
            downloaded_size = 0

            with requests.get(self.download_url, headers=download_headers, stream=True) as response:
                response.raise_for_status()
                with open(self.file_name, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if not self._is_downloading:
                            break
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)
                            elapsed_time = time.time() - start_time
                            speed = downloaded_size / elapsed_time  # 下载速度 (字节/秒)
                            progress = int((downloaded_size / self.expected_size) * 100)

                            # 更新进度条和下载速度
                            self.progress_updated.emit(progress)
                            self.speed_updated.emit(f"{speed / 1024 / 1024:.2f} MB/s")

            # 如果下载完成但大小不匹配，仍将进度设置为100%
            '''if abs(downloaded_size - self.expected_size) > 10240:  # 容许1KB误差
                self.progress_updated.emit(100)'''
            self.progress_updated.emit(100)

            self.finished.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))


class DownloadDialog(QDialog):
    def __init__(self, lis):
        super().__init__()
        self.window = lis[0]
        self.now_version = lis[1]
        self.new_version = lis[2]
        self.update_status = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle("软件更新")
        self.setFixedSize(450, 250)  # 增大窗口尺寸
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # 去掉默认标题栏

        # 设置窗口图标
        icon = QIcon("./image/same/更新.png")
        self.setWindowIcon(icon)

        # 设置窗口背景
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #cceeff, stop:1 #66ccff);

                border-radius: 8px;
            }
            QLabel {
                color: #ecf0f1;
                font-family: 'Microsoft YaHei';
                font-size: 14px;
            }
            QProgressBar {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid #2980b9;
                border-radius: 6px;
                height: 20px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2ecc71, stop:1 #27ae60);
                border-radius: 5px;
            }
        """)

        # 创建动画效果
        self.opacity_effect = QGraphicsOpacityEffect(self)
        #self.setGraphicsEffect(self.opacity_effect)
        self.opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_anim.setDuration(300)

        # 创建控件
        self.create_widgets()
        QTimer.singleShot(1000, self.start_autoupdate)

    def fade_close(self):
        """带淡出效果的关闭"""
        self.opacity_anim.setStartValue(1.0)
        self.opacity_anim.setEndValue(0.0)
        self.opacity_anim.finished.connect(self.close)
        self.opacity_anim.start()

    def create_widgets(self):
        # 主布局
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 20)

        self.main_layout.setSpacing(10)

        # ---------------- 自定义标题栏 ----------------
        title_bar = QHBoxLayout()
        title_bar.setContentsMargins(10, 5, 10, 5)

        self.title_label = QLabel("自动更新")
        self.title_label.setStyleSheet("color: #2c3e50; font-size: 16px;")



        btn_close = QPushButton("✕")
        btn_close.setFixedSize(24, 24)
        btn_close.setStyleSheet("""
                    QPushButton {
                        border: none;
                        background-color: transparent;
                        font-size: 16px;
                        color: #2c3e50;
                    }
                    QPushButton:hover {
                        color: red;
                    }
                """)
        btn_close.clicked.connect(self.fade_close)

        title_bar.addWidget(self.title_label)
        title_bar.addStretch()
        title_bar.addWidget(btn_close)

        title_container = QWidget()
        title_container.setLayout(title_bar)
        title_container.setFixedHeight(35)
        title_container.setStyleSheet(
            "background-color: #cceeff; border-top-left-radius: 8px;")

        self.main_layout.addWidget(title_container)



        self.main_layout.addSpacing(30)

        # 图标标签
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap("./image/same/更新.png").scaled(64, 64))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedHeight(64)

        # 文本标签
        self.label = QLabel(f"发现新版本 {self.new_version}\n正在准备自动更新...")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; font-weight: 500;")

        # 手动更新按钮
        self.btn_manual = QPushButton("手动更新")
        self.btn_manual.setCursor(Qt.PointingHandCursor)
        self.btn_manual.setStyleSheet("""
            QPushButton {
                background: rgba(52, 152, 219, 0.8);
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(41, 128, 185, 0.9);
            }
        """)

        # 取消按钮
        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background: rgba(231, 76, 60, 0.8);
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(192, 57, 43, 0.9);
            }
        """)

        # 组装界面


        self.main_layout.addWidget(icon_label)
        self.main_layout.addWidget(self.label)

        # 连接信号
        self.btn_manual.clicked.connect(self.select_manual)
        self.btn_cancel.clicked.connect(self.fade_close)

        self.setLayout(self.main_layout)

        # 添加鼠标拖动支持
        self.draggable = True
        self.mouse_drag_pos = QPoint()



    def start_autoupdate(self):
        result = self.select_auto()
        if result and (result != '更新成功'):
            self.label.setText(result+'\n请手动更新')
            # 按钮容器
            button_container = QHBoxLayout()
            button_container.setSpacing(15)
            button_container.setContentsMargins(0, 10, 0, 0)
            button_container.addStretch()
            button_container.addWidget(self.btn_manual)
            button_container.addWidget(self.btn_cancel)
            button_container.addStretch()
            self.main_layout.addLayout(button_container)
            self.repaint()
            self.update()


    def select_auto(self):
        self.repaint()
        self.update()
        self.label.setText("正在解析链接 请稍后\n窗口可能会未响应 请耐心等待\n如解析时间超过十秒请使用手动更新")


        self.repaint()

        try:
            # 获取链接中的数据
            url = "https://fcyang.cn/data.txt"
            response = requests.get(url)
            lines = response.text.splitlines()
            update_zip_file = None

            for line in lines:
                if line.startswith("update_file_link"):
                    update_zip_file = line.split(": ")[1]
                    break
            if not update_zip_file:
                self.label.setText("解析失败")
                raise "解析失败"
        except:
            self.label.setText('链接获取失败 请手动更新')
            return "链接获取失败"
        try:
            self.label.setText('链接获取成功 正在解析请稍后\n如解析时间过长请手动更新')
            lanzouyun_url = update_zip_file
            print("正在解析链接 请稍后")
            ## 获取host_url
            host_url = 'https://' + lanzouyun_url.split('/')[2]
            transfer_data = get_transfer_url(host_url, lanzouyun_url)
            file_name = transfer_data[0]
            print(file_name)
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    download_url = get_lanzou_direct_url(lanzouyun_url)
                    self.label.setText('解析成功 正在下载 请稍后')
                    self.repaint()
                    break  # 解析成功，跳出循环
                except:
                    traceback.print_exc()
                    self.label.setText(f'第 {attempt + 1} 次解析失败\n正在重新尝试解析')
                    self.repaint()
                    print(f'第 {attempt + 1} 次解析失败')
                    time.sleep(0.6)

                    if attempt == max_retries - 1:  # 如果已达最大重试次数
                        raise  # 重新抛出最后一次的异常
            else:  # 如果循环正常结束（未触发 break）
                raise RuntimeError("五次解析均失败")
        except:
            self.label.setText('五次链接解析均失败 请手动更新')
            return '链接解析失败'
        try:

            #解析文件大小 文件名
            # 1. 发送网络请求获取网页内容
            url = lanzouyun_url
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # 确保请求成功

            # 2. 解析 HTML 内容
            soup = BeautifulSoup(response.text, "html.parser")

            # 3. 提取文件大小
            file_size_span = soup.find("span", class_="p7", string="文件大小：")
            if file_size_span:
                file_size = file_size_span.next_sibling.strip()  # 提取文件大小文本
                print("文件大小:", file_size)
                size_str = file_size.strip()  # 去掉两端的空格
                number, unit = size_str.split()  # 拆分数字和单位
                number = float(number)  # 转换数字为浮动类型

                if unit.upper() == 'M':  # 如果单位是 M
                    number = number * 1024 * 1024  # 转换为字节
                elif unit.upper() == 'K':  # 如果单位是 K
                    number = number * 1024  # 转换为字节
                elif unit.upper() == 'B':  # 如果单位是 B
                    number = number  # 字节数不变
                else:
                    number = 0

            else:
                number = 0
                print("未找到文件大小信息")
        except:
            self.label.setText('文件大小解析失败 请手动更新')
            return '文件大小解析失败'

        self.file_name = file_name
        self.file_size = number

        self.download_layout = QVBoxLayout()
        self.download_layout.setContentsMargins(20, 0, 20, 0)

        # 添加进度条和速度标签
        self.progress_bar = QProgressBar()
        self.progress_bar.setFont(ui.style.style_font_9)
        #self.progress_bar.setFixedWidth(350)
        self.speed_label = QLabel("下载速度：0 MB/s")
        self.speed_label.setFont(ui.style.style_font_9)
        self.speed_label.setFixedHeight(30)
        self.download_layout.addWidget(self.speed_label)
        self.download_layout.addWidget(self.progress_bar)
        self.main_layout.addLayout(self.download_layout)
        self.main_layout.addSpacing(20)
        self.repaint()

        # 启动下载任务
        self.thread = QThread()
        self.worker = DownloadWorker(download_url, file_name, number)

        # 连接信号
        self.thread.started.connect(self.worker.run)
        self.worker.progress_updated.connect(self.progress_bar.setValue)
        self.worker.speed_updated.connect(self.speed_label.setText)
        self.worker.finished.connect(self.on_download_finished)
        self.worker.error_occurred.connect(self.on_error)

        # 清理线程
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # 启动线程
        self.worker.moveToThread(self.thread)
        self.thread.start()
        return "更新成功"

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.draggable:
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.draggable:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    def select_manual(self):
        # 获取链接中的数据
        url = "https://fcyang.cn/data.txt"
        response = requests.get(url)
        lines = response.text.splitlines()
        update_zip_file = None

        for line in lines:
            if line.startswith("formal_link"):
                update_zip_file = line.split(": ")[1]
                break
        if not update_zip_file:
            update_zip_file = 'https://fcyang.cn/others/help.html'
            return
        webbrowser.open(update_zip_file)
        self.result = 'cancel_update'
        self.accept()

    def select_cancel(self):
        self.result = 'cancel_update'
        self.accept()

    def on_download_finished(self):
        print("开始解压")
        self.repaint()
        self.label.setText("下载完成！正在解压...")
        self.progress_bar.setValue(100)
        # 获取文件大小（字节）
        size_bytes = os.path.getsize(self.file_name)

        # 将字节转换为MB
        size_mb = size_bytes / (1024 * 1024)
        # 保留两位小数
        self.label.setText(f"已下载完毕 {round(size_mb, 2)}MB\n无需进行任何操作 耐心等待即可")
        self.progress_bar.setValue(100)
        self.repaint()
        time.sleep(1)
        self.label.setText("即将解压")
        self.repaint()
        time.sleep(1)

        self.label.setText("正在解压\n请不要关闭程序")
        self.speed_label.setVisible(False)
        self.repaint()
        time.sleep(1)

        # 创建线程和工作对象
        self.thread_unzip = QThread()
        back_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
        old_path = os.path.join(back_path, f'Fuchen_{self.new_version}')
        self.worker_unzip = UnzipWorker(self.file_name, old_path)

        # 将工作对象移动到线程
        self.worker_unzip.moveToThread(self.thread_unzip)

        # 连接信号
        self.thread_unzip.started.connect(self.worker_unzip.run)
        self.worker_unzip.progress_updated.connect(self.progress_bar.setValue)
        self.worker_unzip.finished.connect(lambda: self.on_finished(old_path,self.file_name))
        self.worker_unzip.error_occurred.connect(self.on_error)

        # 线程结束时自动清理
        self.worker_unzip.finished.connect(self.thread_unzip.quit)
        self.worker_unzip.finished.connect(self.worker_unzip.deleteLater)
        self.thread_unzip.finished.connect(self.thread_unzip.deleteLater)

        # 启动线程
        self.thread_unzip.start()

    def on_finished(self,temp_dir,file_name):
        try:
            print("解压完成 正在安装")
            self.label.setText("解压成功 正在安装\n请勿关闭窗口")
            name = os.path.splitext(self.file_name)[0]
            # 找到解压后的文件夹
            extracted_root = os.path.join(temp_dir, name)

            if os.path.isdir(extracted_root):
                # 将内容移动到目标目录
                for item in os.listdir(extracted_root):
                    source = os.path.join(extracted_root, item)
                    destination = os.path.join(temp_dir, item)
                    shutil.move(source, destination)
                if os.path.exists(extracted_root):
                    shutil.rmtree(extracted_root)

            time.sleep(0.5)
            os.remove(file_name)
            self.label.setText("安装成功!您已成功更新\n请等待系统下一步操作")
            self.repaint()
            time.sleep(1)
            self.result = 'update_successful'
            self.accept()
        except Exception as e:
            traceback.print_exc()
            print(e)
            self.label.setText("解压失败 请打开 软件根目录/Fuchen.zip 手动解压")


    def on_error(self, msg):
        self.label.setText(f"更新失败\n{msg}\n请手动更新")
        print(f"更新失败: {msg}\n")

    def closeEvent(self, event):
        # 当用户点击右上角的关闭按钮时，将返回值设置为“取消更新”
        self.result = "cancel_update"
        super().closeEvent(event)


def show_update_dialog(lis):
    app = QApplication([])
    dialog = DownloadDialog(lis)
    dialog.exec_()  # 显示对话框并等待用户操作
    return dialog.result


if __name__ == "__main__":
    app = QApplication([])
    dialog = DownloadDialog(['', 'V1.64', 'V1.65'])
    dialog.show()
    app.exec_()


