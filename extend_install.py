import time
import webbrowser
import zipfile
import os
import requests
import re
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QDialog, QLabel, QPushButton, QProgressBar, QHBoxLayout
from lxml import etree
import urllib.parse
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

        print('\n[*] file_name:', file_name)
        print('[*] transfer_url:', transfer_url)

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
    # print('\n[*] transfer_response:')
    # print(transfer_response.text)

    ## 请求data
    # action=downprocess&signs=%3Fctdf&sign=BWMBPww9VGVVXFFuVGRWalo2V2pTPAs_aADNUYgJpV2NUclR3WztQNVIyBGcEYAE1UjgOMl8yUWIKNQ_c_c&ves=1&websign=&websignkey=z4Fd

    ## 第一次解析
    first_re_data = re.findall(r'data : ({.*?})', transfer_response.text)[0].replace(' ', '')
    print('\n[*] first_re_data:')
    print(first_re_data)

    signs = re.findall(r'signs\':(.*?),\'sign', first_re_data)[0]
    sign = re.findall(r'sign\':(.*?),\'ves', first_re_data)[0].strip("'")
    websignkey = re.findall(r'websignkey\':(.*?)}', first_re_data)[0]
    print('\n[*] signs:', signs)
    print('[*] sign:', sign)
    print('[*] websignkey:', websignkey)

    ajax_data = 'action=downprocess&signs=%s&sign=%s&ves=1&websign=&websignkey=%s' % (
    urllib.parse.quote(signs), sign, websignkey)
    print('\n[*] ajax_data:')
    print(ajax_data)

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

    # print('\n[*] ajax_headers:')
    # print(ajax_headers)

    ajax_response = requests.post(url=ajax_url, data=ajax_data, headers=ajax_headers)
    ajax_response_json = ajax_response.json()
    # print('\n[*] ajax_response_json:')
    # print(ajax_response_json)

    download_url = str(ajax_response_json["dom"] + '/' + 'file' + '/' + ajax_response_json["url"]).replace(r'\/', '/')

    print('\n[*] download_url:')
    print(download_url)
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

    print('\n[*] 文件下载完成')


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
                    zip_ref.extract(file, '.')
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
        ## 获取host_url
        host_url = 'https://' + lanzouyun_url.split('/')[2]
        ## 请求lanzouyun_url，获取transfer_url
        transfer_data = get_transfer_url(host_url, lanzouyun_url)
        file_name = transfer_data[0]
        transfer_url = transfer_data[1]
        self.label.setText("链接解析完毕正在下载\n过程中可能出现未响应 请耐心等待")
        ## 请求transfer_url，获取ajax_data
        ajax_data = get_ajax_data(lanzouyun_url, transfer_url)
        ## 获取download_url
        download_url = get_download_url(host_url, transfer_url, ajax_data)

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
        self.label.setText(f"已下载完毕 {round(size_mb, 2)}MB")
        self.progress_bar.setValue(100)
        self.repaint()
        time.sleep(1)
        self.label.setText("即将解压")
        time.sleep(1)
        # 创建线程和工作对象
        self.thread = QThread()
        self.worker = UnzipWorker(file_name, "")  # 修改为实际路径

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
        #self.btn_start.setEnabled(True)
        print("解压完成！")
        self.label.setText("解压成功!您已成功安装扩展包 重启软件后生效")
        try:
            self.window.trand_problem.setVisible(False)
        except:
            pass
        time.sleep(0.5)
        os.remove(file_name)

    def on_error(self, msg):
        #self.btn_start.setEnabled(True)
        print(f"发生错误: {msg}")



if __name__ == "__main__":
    app = QApplication([])
    dialog = DownloadDialog('')
    dialog.show()
    app.exec_()
