import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QTextBrowser, QPushButton, QDesktopWidget

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
        self.textBrowser.setStyleSheet("""
        QTextBrowser {
        font-family: '黑体'; /* 字体 */
        font-size: 17px; /* 字体大小 */
    }
        QScrollBar:vertical {
            border: none;
            background: #F5F5F5;
            width: 10px; /* 滚动条宽度 */
            border-radius: 5px; /* 设置滚动条的圆角 */
            margin: 0px 0 0px 0; /* 取消上下按钮时可能需要调整margin来防止空白 */
    }
    QScrollBar::handle:vertical {
            background: #E2E2E2;
        min-height: 20px;
        border-radius: 5px; /* 设置滑块的圆角 */
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px; /* 隐藏上下按钮 */
        border: none; /* 取消边框 */
        background: none; /* 取消背景 */
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
        """)

        # 在QTextBrowser中添加长文本
        # 从文本文件中读取长文本内容
        with open('./mod/term/about.txt', 'r', encoding='utf-8') as file:
            long_text = file.read()
        self.textBrowser.setText(long_text)

        style_font_11 = QtGui.QFont()
        style_font_11.setFamily("等线")
        style_font_11.setPointSize(11)
        # 创建并设置QPushButton
        self.pushButton = QPushButton('我同意用户使用协议', self)
        self.pushButton.setGeometry(0, 480, 300, 50)
        self.pushButton.setToolTip("需浏览完用户协议即可点击")
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
