import json
import random
import shutil
import time
import webbrowser
import zipfile
import os

import psutil
import requests
import re
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QDialog, QLabel, QPushButton, QProgressBar, QHBoxLayout
from lxml import etree
import urllib.parse

import function

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

def rand_ip():
    """生成随机IP地址"""
    first_part = ["218", "218", "66", "66", "218", "218", "60", "60", "202", "204", "66", "66", "66", "59", "61", "60",
                  "222", "221", "66", "59", "60", "60", "66", "218", "218", "62", "63", "64", "66", "66", "122", "211"]
    return f"{random.choice(first_part)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"


def get_lanzou_direct_url(url_update):
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


# 工作线程类
class UnzipWorker(QObject):
    progress_updated = pyqtSignal(int)  # 进度更新信号 (0-100)
    finished = pyqtSignal()             # 完成信号
    error_occurred = pyqtSignal(str)    # 错误信号

    def __init__(self, zip_path, extract_dir):
        super().__init__()
        self.zip_path = zip_path
        self.extract_dir = extract_dir

    def run(self):
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                total_size = sum(file.file_size for file in zip_ref.infolist())
                extracted_size = 0

                for file in zip_ref.infolist():
                    zip_ref.extract(file, "./_internal")
                    extracted_size += file.file_size
                    progress = int((extracted_size / total_size) * 100)
                    self.progress_updated.emit(progress)

            self.finished.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))

class DownloadDialog(QDialog):
    def __init__(self, window):
        super().__init__()
        self.selected_method = None
        self.window = window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("CV2扩展包安装")
        self.setFixedSize(300, 100)

        icon = QIcon("./image/Component/下载.png")
        self.setWindowIcon(icon)

        # 创建布局和部件
        self.layout = QVBoxLayout()
        self.label = QLabel("请选择你的下载方式\n自动下载处于测试阶段 如果下载失败请手动下载")

        # 按钮布局
        self.btn_layout = QHBoxLayout()
        self.btn_auto = QPushButton("自动下载")
        self.btn_manual = QPushButton("手动下载")


        # 连接信号

        self.btn_auto.clicked.connect(self.select_auto)
        self.btn_manual.clicked.connect(self.select_manual)

        # 将部件添加到布局
        self.btn_layout.addWidget(self.btn_auto)
        self.btn_layout.addWidget(self.btn_manual)


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
            if line.startswith("cv2_install_execute"):
                cv2_zip_file = line.split(": ")[1]
                break
        if not cv2_zip_file:
            cv2_zip_file = 'https://fcyang.cn/others/help.html'
            return
        webbrowser.open(cv2_zip_file)

        self.accept()


    def select_auto(self):
        self.label.setText("正在解析链接 请稍后\n窗口可能会未响应 请耐心等待")

        self.btn_manual.deleteLater()
        self.btn_auto.setVisible(False)
        self.btn_manual.setVisible(False)
        self.btn_auto.deleteLater()
        self.btn_layout.deleteLater()
        self.repaint()


        # 获取链接中的数据
        url = "https://fcyang.cn/data.txt"
        response = requests.get(url)
        lines = response.text.splitlines()
        cv2_zip_file = None

        for line in lines:
            if line.startswith("cv2_zip_file"):
                cv2_zip_file = line.split(": ")[1]
                break
        if not cv2_zip_file:
            self.label.setText("解析失败，请重试。")
            return

        lanzouyun_url = cv2_zip_file
        print("正在解析链接 请稍后")
        file_name = 'cv2.zip'
        self.label.setText("链接解析完毕正在下载\n过程中可能出现未响应 请耐心等待")
        ## 获取download_url
        download_url = get_lanzou_direct_url(lanzouyun_url)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)
        self.repaint()
        ## 下载文件
        download_file(download_url, file_name)

        # 获取文件大小（字节）
        size_bytes = os.path.getsize(file_name)

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
        try:  # 防止用户二次安装扩展包 (有可能删除失败)
            def find_and_kill_locks(folder_path):
                """找到占用文件夹的进程并结束"""
                for proc in psutil.process_iter(attrs=['pid', 'name']):
                    try:
                        for file in proc.open_files():
                            if folder_path in file.path:
                                print(f"Terminating process {proc.info['name']} (PID: {proc.info['pid']})")
                                proc.terminate()
                                proc.wait()
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        continue

            def delete_folder(folder_path):
                """解除占用后删除文件夹"""
                if os.path.exists(folder_path):
                    print(f"检测占用: {folder_path}...")
                    find_and_kill_locks(folder_path)
                    print(f"正在删除: {folder_path}...")
                    shutil.rmtree(folder_path, ignore_errors=True)
                    print("文件已删除")

            folder_to_delete = "./_internal/cv2"
            delete_folder(folder_to_delete)
        except:
            pass
        # 创建线程和工作对象
        self.thread = QThread()
        self.worker = UnzipWorker(file_name, "./_internal/cv2")

        # 将工作对象移动到线程
        self.worker.moveToThread(self.thread)

        # 连接信号
        self.thread.started.connect(self.worker.run)
        self.worker.progress_updated.connect(self.progress_bar.setValue)
        self.worker.finished.connect(lambda: self.on_finished(file_name))
        self.worker.error_occurred.connect(self.on_error)

        # 线程结束时自动清理
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # 启动线程
        self.thread.start()

    def on_finished(self,file_name):
        print("解压完成！")
        self.label.setText("解压成功!您已成功安装扩展包 重启软件后生效\n请勿二次安装扩展包")
        try:
            self.window.trand_problem.setVisible(False)
        except:
            pass
        time.sleep(0.5)
        os.remove(file_name)

    def on_error(self, msg):
        self.label.setText(f"文件解压失败\n{msg}")
        print(f"发生错误: {msg}")



if __name__ == "__main__":
    app = QApplication([])
    dialog = DownloadDialog('')
    dialog.show()
    app.exec_()
