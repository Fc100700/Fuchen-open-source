import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QTextBrowser, QPushButton, QDesktopWidget
import ui.style
import os


User_Agree = False


class AgreementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        screen = QDesktopWidget().screenGeometry()
        icon = QIcon("./image/window.ico")  # 设置窗口图标
        self.setWindowIcon(icon)

        # 计算窗口居中时的位置
        x = (screen.width() - 300 )// 2
        y = (screen.height() - 530) // 2
        self.setGeometry(x, y, 300, 530)  # 设置窗口位置和大小
        self.setWindowTitle('用户协议确认')  # 设置窗口标题
        self.setFixedSize(300,530)

        # 创建并设置QTextBrowser
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setGeometry(0, 0, 300, 480)
        self.textBrowser.verticalScrollBar().valueChanged.connect(self.checkScroll)  # 连接滚动条信号

        # 设置滚动条样式
        self.textBrowser.setStyleSheet(ui.style.style_agreement_TextBrowser)
        # 获取 main.py 所在的文件夹路径
        main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 构建图片的相对路径
        text_path = os.path.join(main_dir, './mod/term/', 'about.txt')

        # 在QTextBrowser中添加长文本
        # 从文本文件中读取长文本内容
        with open(text_path, 'r', encoding='utf-8') as file:
            long_text = file.read()
        self.textBrowser.setText(long_text)

        style_font_11 = QtGui.QFont()
        style_font_11.setFamily("等线")
        style_font_11.setPointSize(11)
        # 创建并设置QPushButton
        self.pushButton = QPushButton('我同意用户使用协议', self)
        self.pushButton.setGeometry(0, 480, 300, 50)
        self.pushButton.setToolTip("需要浏览用户协议后即可点击")
        self.pushButton.setFont(style_font_11)
        self.pushButton.setEnabled(False)  # 一开始设置为不可点击
        self.pushButton.clicked.connect(self.confirm)
    def confirm(self):
        global User_Agree
        User_Agree = True
        self.close()
    def checkScroll(self):
        # 检查是否滚动到底部
        if self.textBrowser.verticalScrollBar().value() == self.textBrowser.verticalScrollBar().maximum():
            self.pushButton.setEnabled(True)  # 激活按钮
            self.pushButton.setStyleSheet("""
                QPushButton {
                    background-color: #ADD8E6; /* 浅蓝色 */
                    color: black;
                    border: 2px solid #5A9BD3;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #87CEFA; /* 鼠标悬停时稍深的浅蓝色 */
                }
            """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AgreementWindow()
    win.show()
    sys.exit(app.exec_())
