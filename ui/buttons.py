from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QVBoxLayout, QToolButton
from PyQt5.QtCore import QPropertyAnimation, pyqtProperty, Qt
from PyQt5.QtGui import QColor, QPainter, QLinearGradient, QFont, QPen
import sys


class AnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化渐变的起始颜色和结束颜色
        self._start_color = QColor(65, 204, 242)  # 初始渐变起点颜色 #12D8FA
        self._end_color = QColor(47, 128, 237)  # 初始渐变终点颜色 #1FA2FF

        self.hover_start_color = QColor(47, 128, 237)  # 悬停渐变起点颜色 #0DB9F4
        self.hover_end_color = QColor(65, 204, 242)  # 悬停渐变终点颜色 #1A8CE4

        # 定义动画用于改变颜色
        self.animation = QPropertyAnimation(self, b"start_color")
        self.animation.setDuration(300)  # 动画时长500毫秒
        self.animation.setStartValue(self._start_color)
        self.animation.setEndValue(self.hover_start_color)

        self.end_animation = QPropertyAnimation(self, b"end_color")
        self.end_animation.setDuration(300)  # 动画时长500毫秒
        self.end_animation.setStartValue(self._end_color)
        self.end_animation.setEndValue(self.hover_end_color)

        self.setStyleSheet("border-radius: 10px; border: none; color: white; padding: 1px;")

    def enterEvent(self, event):
        """鼠标进入时，开始颜色变化动画"""
        self.animation.setDirection(QPropertyAnimation.Forward)
        self.end_animation.setDirection(QPropertyAnimation.Forward)
        self.animation.start()
        self.end_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开时，恢复颜色"""
        self.animation.setDirection(QPropertyAnimation.Backward)
        self.end_animation.setDirection(QPropertyAnimation.Backward)
        self.animation.start()
        self.end_animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        """重写paintEvent来手动绘制渐变背景色"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # 创建线性渐变
        gradient = QLinearGradient(0, 0, rect.width(), rect.height())
        gradient.setColorAt(0, self._start_color)
        gradient.setColorAt(1, self._end_color)

        # 使用渐变背景色绘制按钮
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 5, 5)  # 圆角矩形

        super().paintEvent(event)

    @pyqtProperty(QColor)
    def start_color(self):
        return self._start_color

    @start_color.setter
    def start_color(self, color):
        self._start_color = color
        self.update()

    @pyqtProperty(QColor)
    def end_color(self):
        return self._end_color

    @end_color.setter
    def end_color(self, color):
        self._end_color = color
        self.update()


class MainAnimatedButton(QToolButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._color = QColor(0, 123, 255, 0)  # 初始透明颜色
        self.hover_color = QColor(0, 123, 255, 80)  # 悬停颜色

        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(330)  # 动画时长500毫秒
        self.animation.setStartValue(self._color)
        self.animation.setEndValue(self.hover_color)

        #self.setFixedSize(200, 50)  # 设置按钮尺寸
        self.setStyleSheet("border-radius: 10px; border: none; color: black; padding: 5px;")
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)  # 设置图标和文字并排显示

    def enterEvent(self, event):
        """鼠标进入时，开始颜色变化动画"""
        self.animation.setDirection(QPropertyAnimation.Forward)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开时，恢复颜色"""
        self.animation.setDirection(QPropertyAnimation.Backward)
        self.animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        """重写paintEvent来手动绘制按钮的背景色"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # 绘制带有渐变效果的背景色
        if self._color.alpha() > 0:  # 仅当背景颜色不透明时绘制
            painter.setBrush(self._color)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(rect, 5, 5)  # 圆角矩形

        super().paintEvent(event)

    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.update()  # 每次颜色变化时更新按钮显示

class CloseButton(QToolButton):
    def __init__(self, parent=None, radius=5, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._color = QColor(255,0,0,0)  # 初始透明颜色
        self.hover_color = QColor(255,0,0,100)  # 悬停颜色

        self.radius = radius

        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(330)  # 动画时长
        self.animation.setStartValue(self._color)
        self.animation.setEndValue(self.hover_color)

        self.setStyleSheet("border: none;  padding: 1px;")

    def enterEvent(self, event):
        """鼠标进入时，开始颜色变化动画"""
        self.animation.setDirection(QPropertyAnimation.Forward)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开时，恢复颜色"""
        self.animation.setDirection(QPropertyAnimation.Backward)
        self.animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        """重写paintEvent来手动绘制按钮的背景色"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # 绘制带有渐变效果的背景色
        if self._color.alpha() > 0:  # 仅当背景颜色不透明时绘制
            painter.setBrush(self._color)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(rect, self.radius, self.radius)  # 圆角矩形

        super().paintEvent(event)

    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.update()  # 每次颜色变化时更新按钮显示

class ComponentButton(QToolButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._color = QColor(255,255,255,0)  # 初始透明颜色
        self.hover_color = QColor(255,255,255,170)  # 悬停颜色

        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(330)  # 动画时长500毫秒
        self.animation.setStartValue(self._color)
        self.animation.setEndValue(self.hover_color)

        self.setStyleSheet("border: none;  padding: 1px;")

    def enterEvent(self, event):
        """鼠标进入时，开始颜色变化动画"""
        self.animation.setDirection(QPropertyAnimation.Forward)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开时，恢复颜色"""
        self.animation.setDirection(QPropertyAnimation.Backward)
        self.animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        """重写paintEvent来手动绘制按钮的背景色"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # 绘制带有渐变效果的背景色
        if self._color.alpha() > 0:  # 仅当背景颜色不透明时绘制
            painter.setBrush(self._color)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(rect, 5, 5)  # 圆角矩形

        super().paintEvent(event)

    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.update()  # 每次颜色变化时更新按钮显示

class NormolAnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._color = QColor(71, 163, 224)  # 初始颜色 #12D8FA
        self.hover_color = QColor(23, 138, 214)  # 悬停颜色 #0DB9F4

        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(500)  # 动画时长500毫秒
        self.animation.setStartValue(self._color)
        self.animation.setEndValue(self.hover_color)

        #self.setFixedSize(200, 50)  # 设置按钮尺寸
        self.setStyleSheet("border-radius: 10px; border: none; color: white; padding: 5px;")

    def enterEvent(self, event):
        """鼠标进入时，开始颜色变化动画"""
        self.animation.setDirection(QPropertyAnimation.Forward)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开时，恢复颜色"""
        self.animation.setDirection(QPropertyAnimation.Backward)
        self.animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        """重写paintEvent来手动绘制按钮的背景色"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # 绘制带有渐变效果的背景色
        gradient = self._color
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 5, 5)  # 圆角矩形

        super().paintEvent(event)

    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.update()  # 每次颜色变化时更新按钮显示

class MoreAnimatedButton(QPushButton):
    def __init__(self, parent=None, radius=5, start_color=QColor(71, 163, 224), hover_color=QColor(23, 138, 214), *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._color = start_color  # 初始颜色
        self.hover_color = hover_color  # 悬停颜色
        self.radius = radius  # 圆角半径

        # 定义动画
        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(500)  # 动画时长500毫秒
        self.animation.setStartValue(self._color)
        self.animation.setEndValue(self.hover_color)

        # 设置样式
        self.setStyleSheet("border-radius: {}px; border: none; color: white; padding: 1px;".format(self.radius))

    def enterEvent(self, event):
        """鼠标进入时，开始颜色变化动画"""
        self.animation.setDirection(QPropertyAnimation.Forward)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开时，恢复颜色"""
        self.animation.setDirection(QPropertyAnimation.Backward)
        self.animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        """重写paintEvent来手动绘制按钮的背景色"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # 绘制背景色
        gradient = self._color
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, self.radius, self.radius)  # 圆角矩形

        super().paintEvent(event)

    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.update()  # 每次颜色变化时更新按钮显示

class MaxAnimatedButton(QPushButton):
    def __init__(self, parent=None, radius=5, start_color=QColor(71, 163, 224), start_color_2 = QColor(0,0,0),hover_color=QColor(23, 138, 214),hover_color_2 = QColor(0,0,0), *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # 初始化渐变的起始颜色和结束颜色
        '''self._start_color = QColor(65, 204, 242)  # 初始渐变起点颜色 #12D8FA
        self._end_color = QColor(47, 128, 237)  # 初始渐变终点颜色 #1FA2FF

        self.hover_start_color = QColor(47, 128, 237)  # 悬停渐变起点颜色 #0DB9F4
        self.hover_end_color = QColor(65, 204, 242)  # 悬停渐变终点颜色 #1A8CE4'''

        # 定义动画用于改变颜色
        self._start_color = start_color  # 初始颜色
        self._end_color = start_color_2
        self.hover_start_color = hover_color
        self.hover_end_color = hover_color_2

        self.animation = QPropertyAnimation(self, b"start_color")
        self.animation.setDuration(300)  # 动画时长500毫秒
        self.animation.setStartValue(self._start_color)
        self.animation.setEndValue(self.hover_start_color)

        self.end_animation = QPropertyAnimation(self, b"end_color")
        self.end_animation.setDuration(300)  # 动画时长500毫秒
        self.end_animation.setStartValue(self._end_color)
        self.end_animation.setEndValue(self.hover_end_color)

        self.setStyleSheet("border-radius: 10px; border: none; color: white; padding: 5px;")

        '''self._color = start_color  # 初始颜色
        self.hover_color = hover_color  # 悬停颜色
        self.radius = radius  # 圆角半径

        # 定义动画
        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(500)  # 动画时长500毫秒
        self.animation.setStartValue(self._color)
        self.animation.setEndValue(self.hover_color)

        # 设置样式
        self.setStyleSheet("border-radius: {}px; border: none; color: white; padding: 5px;".format(self.radius))'''

    def enterEvent(self, event):
        """鼠标进入时，开始颜色变化动画"""
        self.animation.setDirection(QPropertyAnimation.Forward)
        self.end_animation.setDirection(QPropertyAnimation.Forward)
        self.animation.start()
        self.end_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开时，恢复颜色"""
        self.animation.setDirection(QPropertyAnimation.Backward)
        self.end_animation.setDirection(QPropertyAnimation.Backward)
        self.animation.start()
        self.end_animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        """重写paintEvent来手动绘制渐变背景色"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # 创建线性渐变
        gradient = QLinearGradient(0, 0, rect.width(), rect.height())
        gradient.setColorAt(0, self._start_color)
        gradient.setColorAt(1, self._end_color)

        # 使用渐变背景色绘制按钮
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 5, 5)  # 圆角矩形

        super().paintEvent(event)

    @pyqtProperty(QColor)
    def start_color(self):
        return self._start_color

    @start_color.setter
    def start_color(self, color):
        self._start_color = color
        self.update()

    @pyqtProperty(QColor)
    def end_color(self):
        return self._end_color

    @end_color.setter
    def end_color(self, color):
        self._end_color = color
        self.update()

class FloatAnimatedButton(QWidget):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._color = QColor(241, 241, 255)  # 初始背景颜色
        self.hover_color = QColor(79, 176, 255)  # 悬停背景颜色
        self.text_color = QColor(20, 190, 255)  # 初始字体颜色
        self.hover_text_color = QColor(255, 255, 255)  # 悬停字体颜色

        self.text = text
        font = QFont("等线", 10)  # 设置字体为等线（等线）和字号为10
        self.setFont(font)

        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(500)  # 动画时长500毫秒
        self.animation.setStartValue(self._color)
        self.animation.setEndValue(self.hover_color)

        self.text_animation = QPropertyAnimation(self, b"textColor")
        self.text_animation.setDuration(500)  # 动画时长500毫秒
        self.text_animation.setStartValue(self.text_color)
        self.text_animation.setEndValue(self.hover_text_color)

    def enterEvent(self, event):
        """鼠标进入时，开始颜色变化动画"""
        self.animation.setDirection(QPropertyAnimation.Forward)
        self.text_animation.setDirection(QPropertyAnimation.Forward)
        self.animation.start()
        self.text_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开时，恢复颜色"""
        self.animation.setDirection(QPropertyAnimation.Backward)
        self.text_animation.setDirection(QPropertyAnimation.Backward)
        self.animation.start()
        self.text_animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        """重写paintEvent来手动绘制按钮的背景色和字体"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # 绘制背景色
        painter.setBrush(self._color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 8, 8)  # 圆角矩形

        # 绘制边框
        painter.setPen(QColor(79, 176, 255))  # 边框颜色
        painter.drawRoundedRect(rect, 8, 8)  # 圆角矩形边框

        # 绘制按钮文本
        painter.setPen(self.text_color)  # 使用当前的字体颜色
        painter.drawText(rect, Qt.AlignCenter, self.text)

    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.update()  # 每次颜色变化时更新按钮显示

    @pyqtProperty(QColor)
    def textColor(self):
        return self.text_color

    @textColor.setter
    def textColor(self, color):
        self.text_color = color
        self.update()  # 每次文本颜色变化时更新按钮显示

class CustomButton(QPushButton):
    def __init__(self, parent=None, radius=5, start_color=QColor(0, 0, 0), hover_color=QColor(0, 0, 0),
                 border_color=QColor(0, 0, 0), font_color=QColor(255, 255, 255), border_width=1, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._color = start_color  # 初始颜色
        self._original_border_color = border_color  # 保存初始边框颜色
        self._original_hover_color = hover_color  # 保存初始悬停颜色
        self.hover_color = hover_color  # 当前悬停颜色
        self.radius = radius  # 圆角半径
        self.border_color = border_color  # 当前边框颜色
        self.font_color = font_color  # 字体颜色
        self.border_width = border_width

        # 定义动画
        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(300)  # 动画时长500毫秒
        self.animation.setStartValue(self._color)
        self.animation.setEndValue(self.hover_color)

        # 设置字体颜色
        self.setStyleSheet(f"color: {self.font_color.name()}; border-radius: {self.radius}px; padding: 1px;")

    def setEnabled(self, enabled: bool):
        """重写 setEnabled 方法以动态修改边框和背景颜色"""
        super().setEnabled(enabled)
        if enabled:
            self.border_color = self._original_border_color  # 恢复为初始边框颜色
        else:
            self.border_color = QColor(100, 100, 100)  # 设置为灰色边框
        self.update()

    def enterEvent(self, event):
        """鼠标进入时，开始颜色变化动画"""
        if self.isEnabled():
            self.animation.setDirection(QPropertyAnimation.Forward)
            self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开时，恢复颜色"""
        if self.isEnabled():
            self.animation.setDirection(QPropertyAnimation.Backward)
            self.animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        """重写paintEvent来手动绘制按钮的背景色"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # 调整绘制区域以防止边框被裁剪
        border_width = self.border_width
        adjusted_rect = rect.adjusted(border_width, border_width, -border_width, -border_width)

        # 绘制背景色
        painter.setBrush(self._color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(adjusted_rect, self.radius, self.radius)  # 圆角矩形

        # 绘制边框
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(self.border_color, border_width))
        painter.drawRoundedRect(adjusted_rect, self.radius, self.radius)  # 圆角矩形

        super().paintEvent(event)

    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.update()  # 每次颜色变化时更新按钮显示



class LoginAnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化渐变的起始颜色和结束颜色
        self._start_color = QColor(18, 216, 250)  # 初始渐变起点颜色 #12D8FA
        self._end_color = QColor(31, 162, 255)  # 初始渐变终点颜色 #1FA2FF

        #self.hover_start_color = QColor(31, 162, 255)  # 悬停渐变起点颜色 #0DB9F4
        #self.hover_end_color = QColor(18, 216, 250)  # 悬停渐变终点颜色 #1A8CE4
        self.hover_start_color = QColor(13, 185, 244)  # 悬停渐变起点颜色 #0DB9F4
        self.hover_end_color = QColor(26, 140, 228)  # 悬停渐变终点颜色 #1A8CE4

        # 定义动画用于改变颜色
        self.animation = QPropertyAnimation(self, b"start_color")
        self.animation.setDuration(500)  # 动画时长500毫秒
        self.animation.setStartValue(self._start_color)
        self.animation.setEndValue(self.hover_start_color)

        self.end_animation = QPropertyAnimation(self, b"end_color")
        self.end_animation.setDuration(300)  # 动画时长500毫秒
        self.end_animation.setStartValue(self._end_color)
        self.end_animation.setEndValue(self.hover_end_color)

        #self.setFixedSize(200, 50)  # 设置按钮尺寸
        self.setStyleSheet("border-radius: 10px; border: none; color: white; padding: 5px;")

    def enterEvent(self, event):
        """鼠标进入时，开始颜色变化动画"""
        self.animation.setDirection(QPropertyAnimation.Forward)
        self.end_animation.setDirection(QPropertyAnimation.Forward)
        self.animation.start()
        self.end_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开时，恢复颜色"""
        self.animation.setDirection(QPropertyAnimation.Backward)
        self.end_animation.setDirection(QPropertyAnimation.Backward)
        self.animation.start()
        self.end_animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        """重写paintEvent来手动绘制渐变背景色"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # 创建线性渐变
        gradient = QLinearGradient(0, 0, rect.width(), rect.height())
        gradient.setColorAt(0, self._start_color)
        gradient.setColorAt(1, self._end_color)

        # 使用渐变背景色绘制按钮
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 15, 15)  # 圆角矩形

        super().paintEvent(event)

    @pyqtProperty(QColor)
    def start_color(self):
        return self._start_color

    @start_color.setter
    def start_color(self, color):
        self._start_color = color
        self.update()

    @pyqtProperty(QColor)
    def end_color(self):
        return self._end_color

    @end_color.setter
    def end_color(self, color):
        self._end_color = color
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Animated Gradient Button Example")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        button = AnimatedButton("Hover over me")
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
