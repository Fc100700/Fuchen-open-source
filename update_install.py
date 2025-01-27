import shutil
import time
import webbrowser
import zipfile
import os
import py7zr
import psutil
import requests
import re
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QDialog, QLabel, QPushButton, QProgressBar, QHBoxLayout
from bs4 import BeautifulSoup
from lxml import etree
import urllib.parse
import ui.style
'''此文件为自动安装扩展包脚本'''


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


## 请求transfer_url，获取ajax_data
def get_ajax_data(lanzouyun_url, transfer_url):
    transfer_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'ccept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'codelen=1; pc_ad1=1',
        'referer': lanzouyun_url,
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'iframe',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    transfer_response = requests.get(url=transfer_url, headers=transfer_headers)
    first_re_data = re.findall(r'data : ({.*?})', transfer_response.text)[0].replace(' ', '')

    signs = re.findall(r'signs\':(.*?),\'sign', first_re_data)[0]
    sign = re.findall(r'sign\':(.*?),\'ves', first_re_data)[0].strip("'")
    websignkey = re.findall(r'websignkey\':(.*?)}', first_re_data)[0]

    ajax_data = 'action=downprocess&signs=%s&sign=%s&ves=1&websign=&websignkey=%s' % (
    urllib.parse.quote(signs), sign, websignkey)
    return ajax_data


## 请求ajax_url，获取download_url
def get_download_url(host_url, transfer_url, ajax_data):
    ajax_url = host_url + '/' + 'ajaxm.php'
    ajax_headers = {
        'accept': 'application/json, text/javascript, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-length': '152',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'codelen=1; pc_ad1=1',
        'origin': host_url,
        'referer': transfer_url,
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44',
        'x-requested-with': 'XMLHttpRequest'

    }

    ajax_response = requests.post(url=ajax_url, data=ajax_data, headers=ajax_headers)
    ajax_response_json = ajax_response.json()

    download_url = str(ajax_response_json["dom"] + '/' + 'file' + '/' + ajax_response_json["url"]).replace(r'\/', '/')
    return download_url

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
        self.selected_method = None
        self.window = lis[0]
        self.now_version = lis[1]
        self.new_version = lis[2]
        self.initUI()

    def initUI(self):
        self.setWindowTitle("自动更新程序")
        self.setFixedSize(300, 100)

        icon = QIcon("./image/Component/下载.png")
        self.setWindowIcon(icon)

        # 创建布局和部件
        self.layout = QVBoxLayout()
        self.label = QLabel(f"当前版本为 {self.now_version} 已发布新版本{self.new_version}\n此版本为强制更新 请选择你的更新方式\n自动更新处于测试阶段 如果下载失败请网盘更新")
        self.label.setFont(ui.style.style_font_10)

        # 按钮布局
        self.btn_layout = QHBoxLayout()
        self.btn_auto = QPushButton("自动更新")
        self.btn_auto.setFont(ui.style.style_font_9)
        self.btn_manual = QPushButton("手动更新")
        self.btn_manual.setFont(ui.style.style_font_9)
        self.btn_cancel = QPushButton("取消更新")
        self.btn_cancel.setFont(ui.style.style_font_9)
        # 连接信号

        self.btn_auto.clicked.connect(self.select_auto)
        self.btn_manual.clicked.connect(self.select_manual)
        self.btn_cancel.clicked.connect(self.select_cancel)

        # 将部件添加到布局
        self.btn_layout.addWidget(self.btn_auto)
        self.btn_layout.addWidget(self.btn_manual)
        self.btn_layout.addWidget(self.btn_cancel)


        self.layout.addWidget(self.label)
        self.layout.addLayout(self.btn_layout)
        self.setLayout(self.layout)

    def select_manual(self):
        # 获取链接中的数据
        url = "https://fcyang.cn/data.txt"
        response = requests.get(url)
        lines = response.text.splitlines()
        cv2_zip_file = None

        for line in lines:
            if line.startswith("update_file_link"):
                cv2_zip_file = line.split(": ")[1]
                break
        if not cv2_zip_file:
            cv2_zip_file = 'https://fcyang.cn/others/help.html'
            return
        webbrowser.open(cv2_zip_file)
        self.result = 'cancel_update'
        self.accept()

    def select_cancel(self):
        self.result = 'cancel_update'
        self.accept()


    def select_auto(self):
        self.label.setText("正在解析链接 请稍后\n窗口可能会未响应 请耐心等待")

        self.btn_manual.deleteLater()
        self.btn_auto.setVisible(False)
        self.btn_manual.setVisible(False)
        self.btn_cancel.setVisible(False)
        self.repaint()


        # 获取链接中的数据
        url = "https://fcyang.cn/data.txt"
        response = requests.get(url)
        lines = response.text.splitlines()
        cv2_zip_file = None

        for line in lines:
            if line.startswith("update_file_link"):
                cv2_zip_file = line.split(": ")[1]
                break
        if not cv2_zip_file:
            self.label.setText("解析失败，请重试。")
            return

        lanzouyun_url = cv2_zip_file
        print("正在解析链接 请稍后")
        ## 获取host_url
        host_url = 'https://' + lanzouyun_url.split('/')[2]
        transfer_data = get_transfer_url(host_url, lanzouyun_url)
        file_name = transfer_data[0]
        print(file_name)
        transfer_url = transfer_data[1]
        self.label.setText("正在下载...\n过程中可能出现未响应 请耐心等待")
        ajax_data = get_ajax_data(lanzouyun_url, transfer_url)
        ## 获取download_url
        download_url = get_download_url(host_url, transfer_url, ajax_data)

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
            print(number)

        else:
            number = 0
            print("未找到文件大小信息")

        self.file_name = file_name
        self.file_size = number

        # 添加进度条和速度标签
        self.progress_bar = QProgressBar()
        self.progress_bar.setFont(ui.style.style_font_9)
        self.speed_label = QLabel("下载速度：0 MB/s")
        self.speed_label.setFont(ui.style.style_font_9)
        self.layout.addWidget(self.speed_label)
        self.layout.addWidget(self.progress_bar)
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

    def on_download_finished(self):
        print("开始解压")
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


