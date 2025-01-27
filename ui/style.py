from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QLineEdit
import os
from pyautogui import confirm


class CustomWidget(QtWidgets.QWidget):  # 绘制客户端窗口方框分割线
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        painter.setPen(pen)

        brush = QtGui.QColor(200, 200, 255, 0)  # 透明背景色
        painter.setBrush(brush)

        # 绘制一个方框
        corner_radius = 5
        rect = self.rect().adjusted(5, 5, -5, -5)
        painter.drawRoundedRect(rect, corner_radius, corner_radius)

class DraggableLineEdit(QLineEdit):
    def __init__(self, file_type='txt', parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)  # 允许拖放
        # 根据 file_type 设置允许的文件扩展名
        if file_type == 'picture':
            self.allowed_extensions = ['.jpg', '.png', '.gif', '.docx', '.pdf']
        elif file_type == 'setpic':
            self.allowed_extensions = ['.jpg', '.png', '.bmp', '.gif']
        elif file_type == 'video':
            self.allowed_extensions = ['.mp4', '.mov', '.flv', '.avi']
        elif file_type == 'txt':
            self.allowed_extensions = ['.txt']
        else:
            self.allowed_extensions = []  # 为空时不允许任何文件类型

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()  # 获取第一个文件路径
                file_extension = os.path.splitext(file_path)[1].lower()

                # 检查文件扩展名是否在允许的类型中
                if file_extension in self.allowed_extensions:
                    file_path = file_path.replace("/", "\\")
                    self.setText(file_path)  # 显示文件路径
                else:
                    confirm(f"仅支持以下文件类型: {', '.join(self.allowed_extensions)}", "文件类型错误")
                    #self.clear()


style_lineEdit = """
            QLineEdit {
                border: 1px solid gray;
                border-radius: 2px;
                background: transparent;
            }
            QLineEdit:hover {
                border: 1px solid rgb(0, 120, 215);
            }
        """
style_CheckBox = ''' QCheckBox {font-family: '等线';
                                color: black;}
                    QCheckBox::indicator:unchecked {
                                image: url(./image/Component/复选框.png);}
                    QCheckBox::indicator:checked {
                                image: url(./image/Component/复选框2.png);}
                    QCheckBox::indicator {
                                padding-top: 1px;
                                width: 16px;
                                height: 16px;
                                border: none;}'''
style_Radio = '''QRadioButton {
                    font-family: '等线';
                    color: black;}
                QRadioButton::indicator:unchecked {
                    image: url(./image/Component/选择.svg);}
                QRadioButton::indicator {
                    padding-top: 1px;
                    width: 16px;
                    height: 16px;
                    border: none;}
                QRadioButton::indicator:checked {
                    image: url(./image/Component/选择2.svg);}'''
style_Spin = '''QSpinBox {
                            border: 1px solid gray;
                            border-radius: 3px;  /* 设置圆角 */
                            background: transparent;
                            font: 14px;
                            font-family: Calibri;
                            }
                QSpinBox:hover {
                    border: 1px solid rgb(0, 120, 215);
                }
                QSpinBox::up-button {
                            subcontrol-origin: border;
                            subcontrol-position: top right; 
                            width: 13px; 
                            border-image: url('./image/Component/箭头 上.png');  /* 设置上调按钮的图像 */
                            }
                QSpinBox::down-button {
                            subcontrol-origin: border;
                            subcontrol-position: bottom right; 
                            width: 13px; 
                            border-image: url('./image/Component/箭头 下.png');  /* 设置下调按钮的图像 */
                            }'''
style_Double = """QDoubleSpinBox {
                            border: 1px solid gray;
                            border-radius: 3px;  /* 设置圆角 */
                            background: transparent;
                            font: 14px;
                            font-family: Calibri;
                            }
                QDoubleSpinBox:hover {
                    border: 1px solid rgb(0, 120, 215);
                }
                QDoubleSpinBox::up-button {
                            subcontrol-origin: border;
                            subcontrol-position: top right; 
                            width: 13px; 
                            border-image: url('./image/Component/箭头 上.png');  /* 设置上调按钮的图像 */
                            }
                QDoubleSpinBox::down-button {
                            subcontrol-origin: border;
                            subcontrol-position: bottom right; 
                            width: 13px; 
                            border-image: url('./image/Component/箭头 下.png');  /* 设置下调按钮的图像 */
                            }"""

#主界面更新公告
style_information_TextBrowser = '''QTextBrowser {
                                        background: transparent;
                                        border: 2px solid #ccc;
                                        border-radius: 5px;
                                        color: black;
                                        background-color: rgba(255, 255, 255, 150);
                                    }
                                    QScrollBar:vertical {
                                        border: none;
                                        background: #F5F5F5;
                                        width: 10px;
                                        /* 滚动条宽度 */
                                        border-radius: 5px;
                                        /* 设置滚动条的圆角 */
                                        margin: 0px 0 0px 0;
                                        /* 取消上下按钮时可能需要调整margin来防止空白 */
                                    }
                                    QScrollBar::handle:vertical {
                                        background: #E2E2E2;
                                        min-height: 20px;
                                        border-radius: 5px;
                                        /* 设置滑块的圆角 */
                                    }
                                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                                        height: 0px;
                                        /* 隐藏上下按钮 */
                                        border: none;
                                        /* 取消边框 */
                                        background: none;
                                        /* 取消背景 */
                                    }
                                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                        background: none;
                                    }'''
#文本输入框
style_textEdit= '''QTextEdit {
                        background: transparent;
                        border: 1px solid #989898;
                        border-radius: 3px;
                        color: black;
                        background-color: transparent;
                    }
                    QScrollBar:vertical {
                        border: none;
                        background: #F5F5F5;
                        width: 10px;
                        /* 滚动条宽度 */
                        border-radius: 5px;
                        /* 设置滚动条的圆角 */
                        margin: 0px 0 0px 0;
                        /* 取消上下按钮时可能需要调整margin来防止空白 */
                    }
                    QScrollBar::handle:vertical {
                        background: #E2E2E2;
                        min-height: 20px;
                        border-radius: 5px;
                        /* 设置滑块的圆角 */
                    }
                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                        height: 0px;
                        /* 隐藏上下按钮 */
                        border: none;
                        /* 取消边框 */
                        background: none;
                        /* 取消背景 */
                    }
                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                        background: none;
                    }'''

style_verticalScrollBar = """
                            QTextBrowser {
                                background: #C0C0C0;
                                width: 5px;
                                margin:0px; 
                                border: none; 
                                border-radius: 1px;
                                font-family: "等线";
                                font-size: 15pt;}
                            QScrollBar:vertical {
                                border: none;
                                background: #F5F5F5;
                                width: 10px;
                                /* 滚动条宽度 */
                                border-radius: 5px;
                                /* 设置滚动条的圆角 */
                                margin: 0px 0 0px 0;
                                /* 取消上下按钮时可能需要调整margin来防止空白 */
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
                            """
#用户使用协议文本框
style_agreement_TextBrowser = """QTextBrowser {
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
                                }"""
style_white_blue_button = """
                        QPushButton {
                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                            background-color: transparent;    /* 设置透明背景 */
                            border-radius: 2px;    /* 设置圆角 */
                        }
                        QPushButton:hover {
                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                        }
                    """
style_white_blue_toolbutton = """
                        QToolButton {
                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                            background-color: transparent;    /* 设置透明背景 */
                            border-radius: 2px;    /* 设置圆角 */
                        }
                        QToolButton:hover {
                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                        }
                    """
style_font_7 = QtGui.QFont()
style_font_7.setFamily("等线")
style_font_7.setPointSize(7)

style_font_8 = QtGui.QFont()
style_font_8.setFamily("等线")
style_font_8.setPointSize(7)

style_font_9 = QtGui.QFont()
style_font_9.setFamily("等线")
style_font_9.setPointSize(9)

style_font_10 = QtGui.QFont()
style_font_10 .setFamily("等线")
style_font_10.setPointSize(10)

style_font_11 = QtGui.QFont()
style_font_11.setFamily("等线")
style_font_11.setPointSize(11)

style_font_12 = QtGui.QFont()
style_font_12.setFamily("等线")
style_font_12.setPointSize(12)

style_font_black_10 = QtGui.QFont()
style_font_black_10.setFamily("黑体")
style_font_black_10.setPointSize(10)

style_font_black_9 = QtGui.QFont()
style_font_black_9.setFamily("黑体")
style_font_black_9.setPointSize(9)

style_font_black_16 = QtGui.QFont()
style_font_black_16.setFamily("黑体")
style_font_black_16.setPointSize(16)