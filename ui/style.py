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
    def __init__(self, file_type='', parent=None):
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
            self.allowed_extensions = ['*']  # 为空时允许任何类型

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
                # 如果允许任何类型('*')，直接接受文件
                if '*' in self.allowed_extensions:
                    file_path = file_path.replace("/", "\\")
                    self.setText(file_path)
                else:
                    file_extension = os.path.splitext(file_path)[1].lower()
                    # 检查文件扩展名是否在允许的类型中
                    if file_extension in self.allowed_extensions:
                        file_path = file_path.replace("/", "\\")
                        self.setText(file_path)  # 显示文件路径
                    else:
                        confirm(f"仅支持以下文件类型: {', '.join(self.allowed_extensions)}", "文件类型错误")
                    #self.clear()
style_console_browser_dark = """
            QTextBrowser {
            background-color: #2D2D2D;
            color: #E0E0E0;
            border: 1px solid #3D3D3D;
            border-top-left-radius: 0px;
            border-top-right-radius: 0px;  /* 仅顶部圆角 */
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;  /* 底部直角 */
            padding: 6px;
            font-family: 'Consolas';
            font-size: 11pt;
        }
            
            /* 垂直滚动条 */
            QScrollBar:vertical {
                background: #2D2D2D;
                width: 14px;
                margin: 14px 0 14px 0;
            }
            
            QScrollBar::handle:vertical {
                background: #4A4A4A;
                min-height: 30px;
                border-radius: 7px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #5A5A5A;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 14px;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            
            /* 水平滚动条 */
            QScrollBar:horizontal {
                background: #2D2D2D;
                height: 14px;
                margin: 0 14px 0 14px;
            }
            
            QScrollBar::handle:horizontal {
                background: #4A4A4A;
                min-width: 30px;
                border-radius: 7px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: #5A5A5A;
            }
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;
                width: 14px;
            }
            
            /* 通用箭头按钮 */
            QScrollBar::up-arrow, QScrollBar::down-arrow,
            QScrollBar::left-arrow, QScrollBar::right-arrow {
                border: none;
                width: 0;
                height: 0;
            }
            
            /* 角部填充 */
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #353535;
            }
            """

style_console_browser_light = """
            QTextBrowser {
            background-color: #F0F0F0;
            color: #333333;
            border: 1px solid #808080;
            border-top-left-radius: 0px;
            border-top-right-radius: 0px;
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;
            padding: 6px;
            font-family: 'Consolas';
            font-size: 11pt;
        }

            /* 垂直滚动条 */
            QScrollBar:vertical {
                background: #F0F0F0;  /* 与textbrowser背景一致 */
                width: 14px;
                margin: 14px 0 14px 0;
            }

            QScrollBar::handle:vertical {
                background: #999999;  /* 与边框色协调 */
                min-height: 30px;
                border-radius: 7px;
            }

            QScrollBar::handle:vertical:hover {
                background: #808080;  /* 与原始边框色一致 */
            }

            /* 水平滚动条 */
            QScrollBar:horizontal {
                background: #F0F0F0;  /* 与textbrowser背景一致 */
                height: 14px;
                margin: 0 14px 0 14px;
            }

            QScrollBar::handle:horizontal {
                background: #999999;  /* 统一垂直/水平把手颜色 */
                min-width: 30px;
                border-radius: 7px;
            }

            QScrollBar::handle:horizontal:hover {
                background: #808080;
            }

            /* 通用箭头和边角 */
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }

            QScrollBar::up-arrow, QScrollBar::down-arrow,
            QScrollBar::left-arrow, QScrollBar::right-arrow {
                border: none;
            }

            /* 角部填充改为背景色 */
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #F0F0F0;
            }
            """

style_console_title_bar_dark = """background-color: #202020;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;  /* 仅顶部圆角 */
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;  /* 底部直角 */"""
style_console_title_bar_light = """background-color: #E0E0E0;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;  /* 仅顶部圆角 */
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;  /* 底部直角 */"""

style_console_title_label_dark = "color: #E0E0E0; font-family: 'Microsoft YaHei';"
style_console_title_label_light = "color: #757575; font-family: 'Microsoft YaHei';"

save_button_style = '''/* 保存按钮样式 */
        QPushButton#save_button {
            background-color: transparent;
            border: none;
            padding: 0;
        }

        QPushButton#save_button:hover {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }

        QPushButton#save_button:pressed {
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 4px;
        }'''

style_console_lineedit_dark = """
        QLineEdit {
            background-color: #3A3A3A;
            color: #E0E0E0;
            border: 1px solid #4A4A4A;
            border-top-left-radius: 0;      /* 顶部直角 */
            border-top-right-radius: 0;     /* 顶部直角 */
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;  /* 底部圆角 */
            padding: 2px 6px;
            font-family: 'Consolas';
            font-size: 12pt;
        }

        QLineEdit:focus {
            border-top-left-radius: 0;
            border-top-right-radius: 0;  /* 保持焦点状态顶部直角 */
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
        }
        """

style_console_lineedit_light = """
        QLineEdit {
            background-color: #FFFFFF;
            color: #333333;
            border: 1px solid #C0C0C0;
            border-top-left-radius: 0;      /* 顶部直角 */
            border-top-right-radius: 0;     /* 顶部直角 */
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;  /* 底部圆角 */
            padding: 2px 6px;
            font-family: 'Consolas';
            font-size: 12pt;
        }

        QLineEdit:focus {
            border-top-left-radius: 0;
            border-top-right-radius: 0;  /* 保持焦点状态顶部直角 */
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
        }
        """

style_console_confirm_button_dark = '''/* 确认按钮样式 */
        QPushButton#confirm_button {
            background-color: #4A4A4A;
            color: #E0E0E0;
            border: 1px solid #5A5A5A;
            border-radius: 4px;
            padding: 2px 6px;
        }

        QPushButton#confirm_button:hover {
            background-color: #5A5A5A;
        }

        QPushButton#confirm_button:pressed {
            background-color: #3A3A3A;
        }'''

style_console_confirm_button_light = '''/* 确认按钮样式 */
        QPushButton#confirm_button {
            background-color: #D0D0D0;
            color: #333333;
            border: 1px solid #C0C0C0;
            border-radius: 4px;
            padding: 2px 6px;
        }

        QPushButton#confirm_button:hover {
            background-color: #C0C0C0;
        }

        QPushButton#confirm_button:pressed {
            background-color: #3A3A3A;
        }'''
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


style_Radio_Small = '''QRadioButton {
                    font-family: '等线';
                    color: black;}
                QRadioButton::indicator:unchecked {
                    image: url(./image/Component/选择.svg);}
                QRadioButton::indicator {
                    padding-top: 1px;
                    width: 12px;
                    height: 12px;
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

new_style_lineEdit = """
                        QLineEdit {
                            border: 1px solid #D0D5DD;
                            border-radius: 6px;
                            padding: 3px;
                            font: 13px '等线';
                            background: white;
                        }
                        QLineEdit:hover {
                            border: 1px solid #00BFFF;
                        }
                        QLineEdit:disabled {
                            border: 1px solid #E4E7EC;
                            background: #F9FAFB;
                            color: #98A2B3;
                        }"""

# 统一SpinBox样式
new_spinbox_style = """
                QSpinBox, QDoubleSpinBox {
                    border: 1px solid #D0D5DD;
                    border-radius: 6px;
                    padding: 5px 30px 5px 10px;
                    font: 13px '等线';
                    background: white;
                }
                QSpinBox:hover, QDoubleSpinBox:hover {
                    border: 1px solid #00BFFF;
                }
                QSpinBox::up-button, QDoubleSpinBox::up-button {
                                            subcontrol-origin: border;
                                            subcontrol-position: top right; 
                                            width: 12px;    /* 按钮宽度 */
                                            height: 12px;   /* 增加高度定义 */
                                            right: 5px;     /* 添加右侧偏移 */
                                            margin: 1px;    /* 防止紧贴边框 */
                                            border-image: url('./image/Component/new_up.png');  /* 设置上调按钮的图像 */
                                            }
                                QSpinBox::down-button, QDoubleSpinBox::down-button  {
                                            subcontrol-origin: border;
                                            subcontrol-position: bottom right; 
                                            width: 12px;    /* 按钮宽度 */
                                            height: 12px;   /* 增加高度定义 */
                                            right: 5px;     /* 添加右侧偏移 */
                                            margin: 1px;    /* 防止紧贴边框 */
                                            border-image: url('./image/Component/new_down.png');  /* 设置下调按钮的图像 */
                                            }"""


# 统一风格CheckBox
new_checkbox_style = """
                    QCheckBox {
                        spacing: 8px;
                        font: 13px '等线';
                        color: #344054;
                        min-height: 24px;
                    }
                    QCheckBox::indicator {
                        width: 16px;
                        height: 16px;
                        border: 1px solid #D0D5DD;
                        border-radius: 4px;
                        background: white;
                    }
                    QCheckBox::indicator:hover {
                        border-color: #00BFFF;
                        background: #F6FAFF;
                    }
                    QCheckBox::indicator:checked {
                        background: #00BFFF;
                        border-color: #00BFFF;
                        image: url("your_check_icon.png");  /* 替换为实际勾选图标路径 */
                    }
                    QCheckBox::indicator:disabled {
                        border-color: #E4E7EC;
                        background: #F9FAFB;
                    }
                    QCheckBox::indicator:checked:disabled {
                        background: #B3E5FF;
                        border-color: #B3E5FF;
                    }"""

new_style_comboBox = """
                    QComboBox {
                        border: 1px solid #D0D5DD;
                        border-radius: 6px;
                        padding: 5px 25px 5px 10px;
                        font: 13px '等线';
                        background: white;
                        selection-background-color: #F2F4F7;
                    }
                    QComboBox:hover {
                        border: 1px solid #00BFFF;
                    }
                    QComboBox:disabled {
                        border: 1px solid #E4E7EC;
                        background: #F9FAFB;
                        color: #98A2B3;
                    }
                    QComboBox::drop-down {
                        subcontrol-origin: padding;
                        subcontrol-position: top right;
                        width: 20px;
                        border: none;
                        border-left: 1px solid transparent;
                        border-radius: 0 6px 6px 0;
                        background: transparent;
                    }
                    QComboBox::down-arrow {
                        image: url('./image/Component/new_down.png'); /* 替换为您的箭头路径 */
                        width: 12px;
                        height: 12px;
                    }
                    QComboBox QAbstractItemView {
                        border: 1px solid #D0D5DD;
                        border-radius: 6px;
                        background: white;
                        outline: none;
                        margin: 2px 0;
                    }
                    QComboBox QAbstractItemView::item {
                        height: 28px;
                        padding: 0 8px;
                    }
                    QComboBox QAbstractItemView::item:hover {
                        background-color: #F9FAFB;
                    }
                    QComboBox QAbstractItemView::item:selected {
                        background-color: #F2F4F7;
                        color: black;
                    }"""

new_style_pushbutton = """
                QPushButton {
                    background-color: #4DA3FF;  /* 浅蓝色 */
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 5px 10px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #3D8FD3;  /* 稍深的水蓝色 */
                }
                QPushButton:pressed {
                    background-color: #2C7ABF;  /* 柔和的深蓝色 */
                }"""
style_font_Yahei = QtGui.QFont()
style_font_Yahei.setFamily("微软雅黑")


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