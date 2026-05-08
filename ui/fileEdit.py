import sys
import json
import re
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QHBoxLayout,
)
from PyQt5.QtWidgets import QTextEdit, QWidget, QPlainTextEdit
from PyQt5.QtGui import QColor, QPainter, QTextFormat, QFont, QIcon
from PyQt5.QtCore import Qt, QRect, QSize


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(
            self.editor.blockBoundingGeometry(block)
            .translated(self.editor.contentOffset())
            .top()
        )
        bottom = top + int(self.editor.blockBoundingRect(block).height())

        # 设置行号字体
        font = QFont("等线", 10)  # 设置字体为“等线”，大小为10
        font.setWeight(QFont.Normal)  # 可选：设置字体粗细
        painter.setFont(font)

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(
                    0,
                    top,
                    self.width(),
                    self.editor.fontMetrics().height(),
                    Qt.AlignRight,
                    number,
                )
            block = block.next()
            top = bottom
            bottom = top + int(self.editor.blockBoundingRect(block).height())
            block_number += 1


class LineNumberTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.original_lines = []
        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def line_number_area_width(self):
        digits = len(str(self.blockCount()))
        return 10 + self.fontMetrics().width("9") * digits

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(
                0, rect.y(), self.lineNumberArea.width(), rect.height()
            )

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        )

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(
            self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        )
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(
                    0,
                    top,
                    self.lineNumberArea.width(),
                    self.fontMetrics().height(),
                    Qt.AlignRight,
                    number,
                )
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def set_original_text(self, text):
        self.original_lines = text.strip().split("\n")
        self.highlight_changed_lines()

    def highlight_changed_lines(self):
        self.setExtraSelections([])
        current_lines = self.toPlainText().strip().split("\n")
        selections = []
        for i, line in enumerate(current_lines):
            if (
                i >= len(self.original_lines)
                or line.strip() != self.original_lines[i].strip()
            ):
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(QColor("#d0e7ff"))  # 浅蓝色
                selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                cursor = self.textCursor()
                cursor.movePosition(cursor.Start)
                cursor.movePosition(cursor.Down, cursor.MoveAnchor, i)
                selection.cursor = cursor
                selections.append(selection)
        self.setExtraSelections(selections)

    def highlight_current_line(self):
        self.highlight_changed_lines()


class EditorWindow(QMainWindow):
    def __init__(self, file="", windows=None):
        super().__init__()
        self.original_data = None  # 存储原始 JSON 数据
        self.original_records = None
        self.script_meta = {}
        self.script_payload_type = "list"
        self.file_path = None  # 存储当前文件路径
        self.file = file
        self.initUI()

    def initUI(self):
        if self.file == "":
            # 设置窗口标题和大小
            self.setWindowTitle("脚本编辑器")
        else:
            self.setWindowTitle(self.file)
        self.resize(900, 600)  # 更现代化的宽高比
        icon = QIcon("./image/Component/提示.png")
        self.setWindowIcon(icon)
        self.setMinimumSize(700, 400)

        # 创建主部件和布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 创建文本编辑框
        self.text_edit = LineNumberTextEdit()
        self.text_edit.setReadOnly(False)  # 允许编辑
        self.text_edit.setStyleSheet(
            """
            QPlainTextEdit {
                background: transparent;
                border: 2px solid #ccc;
                color: black;
                background-color: rgba(255, 255, 255, 150);
                font-family: "等线";
                font-size: 13pt;
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

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                /* 隐藏上下按钮 */
                border: none;
                /* 取消边框 */
                background: none;
                /* 取消背景 */
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
            """
        )

        self.layout.addWidget(self.text_edit)

        # 按钮布局
        button_layout = QHBoxLayout()
        self.load_button = QPushButton("📂 加载配置文件")
        self.save_button = QPushButton("💾 保存配置文件")

        for btn in (self.load_button, self.save_button):
            btn.setFixedHeight(30)
            btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        font-size: 11pt;
                        font-family: 等线;
                        padding: 6px 20px;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)

        self.load_button.clicked.connect(self.load_file)
        self.save_button.clicked.connect(self.save_file)

        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)

        self.layout.addLayout(button_layout)

        if self.file != "":
            try:
                with open(self.file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                records, meta, payload_type = self._normalize_script_data(data)
                self.original_data = data
                self.original_records = records
                self.script_meta = meta
                self.script_payload_type = payload_type
                self.file_path = self.file
                self.display_records(records)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载文件失败: {str(e)}")

    def load_file(self):
        # 打开文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择配置文件", "", "JSON Files (*.json *.txt)"
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            records, meta, payload_type = self._normalize_script_data(data)
            self.original_data = data
            self.original_records = records
            self.script_meta = meta
            self.script_payload_type = payload_type
            self.file_path = file_path
            self.display_records(records)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载文件失败: {str(e)}")

    def _normalize_script_data(self, data):
        if isinstance(data, dict):
            records = data.get("records", [])
            meta = data.get("meta", {})
            payload_type = "dict"
        elif isinstance(data, list):
            records = data
            meta = {}
            payload_type = "list"
        else:
            raise ValueError("脚本文件格式错误")

        if not isinstance(records, list):
            raise ValueError("脚本文件中的 records 字段格式错误")
        if not isinstance(meta, dict):
            meta = {}
        return records, meta, payload_type

    def _get_meta_screen_size(self):
        screen = (
            self.script_meta.get("screen", {})
            if isinstance(self.script_meta, dict)
            else {}
        )
        width = screen.get("width") if isinstance(screen, dict) else None
        height = screen.get("height") if isinstance(screen, dict) else None
        if (
            isinstance(width, int)
            and width > 0
            and isinstance(height, int)
            and height > 0
        ):
            return width, height
        return None, None

    def _enrich_ratio_for_mouse_records(self, records):
        width, height = self._get_meta_screen_size()
        if width is None or height is None:
            return
        for record in records:
            if record.get("type") != "mouse":
                continue
            if record.get("action") not in ("move", "down", "up"):
                continue
            details = record.get("details", {})
            x = details.get("x")
            y = details.get("y")
            if x is None or y is None:
                continue
            details["rx"] = round(x / width, 6)
            details["ry"] = round(y / height, 6)

    def display_records(self, records):
        lines = []
        i = 0
        while i < len(records):
            record = records[i]
            interval = record["interval"]
            event_type = record["type"]
            action = record["action"]
            details = record["details"]

            if event_type == "mouse":
                if action == "move":
                    move_records = [record]
                    total_interval = interval
                    j = i + 1
                    while (
                        j < len(records)
                        and records[j]["type"] == "mouse"
                        and records[j]["action"] == "move"
                    ):
                        move_records.append(records[j])
                        total_interval += records[j]["interval"]
                        j += 1

                    if len(move_records) > 1:
                        first = move_records[0]
                        last = move_records[-1]
                        lines.append(
                            f"鼠标操作 鼠标移动: x:{first['details']['x']} y:{first['details']['y']} 间隔: {first['interval']}"
                        )
                        if len(move_records) > 2:
                            lines.append(
                                f"此处折叠 {len(move_records) - 2} 条鼠标移动记录"
                            )
                        lines.append(
                            f"鼠标操作 鼠标移动: x:{last['details']['x']} y:{last['details']['y']} 间隔: {total_interval - first['interval']}"
                        )
                        i = j
                    else:
                        lines.append(
                            f"鼠标操作 鼠标移动: x:{details['x']} y:{details['y']} 间隔: {interval}"
                        )
                        i += 1
                elif action in ["down", "up"]:
                    button_map = {"left": "左键", "right": "右键", "middle": "中键"}
                    action_map = {"down": "按下", "up": "松开"}
                    button = button_map.get(details["button"], details["button"])
                    action_cn = action_map.get(action, action)
                    lines.append(
                        f"鼠标操作 鼠标{button}{action_cn}: x:{details['x']} y:{details['y']} 间隔: {interval}"
                    )
                    i += 1
                elif action == "scroll":
                    lines.append(
                        f"鼠标操作 鼠标滚动: dx:{details['dx']} dy:{details['dy']} 间隔: {interval}"
                    )
                    i += 1
            elif event_type == "keyboard":
                key_name = details["name"]
                key_code = details["code"]
                action_map = {"down": "按下", "up": "抬起"}
                action_cn = action_map.get(action, action.capitalize())
                lines.append(
                    f"键盘操作 {action_cn} {key_name}(keycode {key_code}) 间隔: {interval}"
                )
                i += 1

        text = "\n".join(lines)
        self.text_edit.setPlainText(text)
        self.text_edit.set_original_text(text)  # 设置为原始内容（用于对比变更）

    def parse_text(self):
        """解析 QTextEdit 中的文本内容，转换为 JSON 格式"""
        lines = self.text_edit.toPlainText().split("\n")
        new_records = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            # 忽略折叠提示
            if re.match(r"^此处折叠 \d+ 条.*$", line):
                i += 1
                continue

            # 匹配鼠标移动
            move_match = re.match(
                r"鼠标操作 鼠标移动: x:(\d+) y:(\d+) 间隔: (\d+)", line
            )
            if move_match:
                x, y, interval = map(int, move_match.groups())
                new_records.append(
                    {
                        "interval": interval,
                        "type": "mouse",
                        "action": "move",
                        "details": {"x": x, "y": y},
                    }
                )
                i += 1
                # 检查是否为连续移动的第二行
                if i < len(lines) and lines[i].startswith("鼠标操作 鼠标移动:"):
                    next_match = re.match(
                        r"鼠标操作 鼠标移动: x:(\d+) y:(\d+) 间隔: (\d+)", lines[i]
                    )
                    if next_match:
                        x, y, interval = map(int, next_match.groups())
                        new_records.append(
                            {
                                "interval": interval,
                                "type": "mouse",
                                "action": "move",
                                "details": {"x": x, "y": y},
                            }
                        )
                        i += 1
                continue

            # 匹配鼠标按下/松开
            click_match = re.match(
                r"鼠标操作 鼠标(左键|右键|中键)(按下|松开): x:(\d+) y:(\d+) 间隔: (\d+)",
                line,
            )
            if click_match:
                button_cn, action_cn, x, y, interval = click_match.groups()
                button_map = {"左键": "left", "右键": "right", "中键": "middle"}
                action_map = {"按下": "down", "松开": "up"}
                new_records.append(
                    {
                        "interval": int(interval),
                        "type": "mouse",
                        "action": action_map[action_cn],
                        "details": {
                            "button": button_map[button_cn],
                            "x": int(x),
                            "y": int(y),
                        },
                    }
                )
                i += 1
                continue

            # 匹配鼠标滚动
            scroll_match = re.match(
                r"鼠标操作 鼠标滚动: dx:(-?\d+) dy:(-?\d+) 间隔: (\d+)", line
            )
            if scroll_match:
                dx, dy, interval = map(int, scroll_match.groups())
                new_records.append(
                    {
                        "interval": interval,
                        "type": "mouse",
                        "action": "scroll",
                        "details": {"dx": dx, "dy": dy},
                    }
                )
                i += 1
                continue

            # 匹配键盘操作
            key_match = re.match(
                r"键盘操作 (按下|抬起) (\w+)\(keycode (\d+)\) 间隔: (\d+)", line
            )
            if key_match:
                action_cn, key_name, key_code, interval = key_match.groups()
                action_map = {"按下": "down", "抬起": "up"}
                new_records.append(
                    {
                        "interval": int(interval),
                        "type": "keyboard",
                        "action": action_map[action_cn],
                        "details": {"code": int(key_code), "name": key_name},
                    }
                )
                i += 1
                continue

            i += 1
        return new_records

    def save_file(self):
        if not self.file_path or self.original_records is None:
            QMessageBox.warning(self, "警告", "请先加载配置文件")
            return

        # 解析当前文本内容
        new_records = self.parse_text()

        # 获取原始文本显示内容
        original_text = []
        i = 0
        while i < len(self.original_records):
            record = self.original_records[i]
            interval = record["interval"]
            event_type = record["type"]
            action = record["action"]
            details = record["details"]

            if event_type == "mouse" and action == "move":
                move_records = [record]
                total_interval = interval
                j = i + 1
                while (
                    j < len(self.original_records)
                    and self.original_records[j]["type"] == "mouse"
                    and self.original_records[j]["action"] == "move"
                ):
                    move_records.append(self.original_records[j])
                    total_interval += self.original_records[j]["interval"]
                    j += 1
                if len(move_records) > 1:
                    first = move_records[0]
                    last = move_records[-1]
                    original_text.append(
                        f"鼠标操作 鼠标移动: x:{first['details']['x']} y:{first['details']['y']} 间隔: {first['interval']}"
                    )
                    original_text.append(
                        f"鼠标操作 鼠标移动: x:{last['details']['x']} y:{last['details']['y']} 间隔: {total_interval - first['interval']}"
                    )
                    i = j
                else:
                    original_text.append(
                        f"鼠标操作 鼠标移动: x:{details['x']} y:{details['y']} 间隔: {interval}"
                    )
                    i += 1
            elif event_type == "mouse" and action in ["down", "up"]:
                button_map = {"left": "左键", "right": "右键", "middle": "中键"}
                action_map = {"down": "按下", "up": "松开"}
                button = button_map.get(details["button"], details["button"])
                action_cn = action_map.get(action, action)
                original_text.append(
                    f"鼠标操作 鼠标{button}{action_cn}: x:{details['x']} y:{details['y']} 间隔: {interval}"
                )
                i += 1
            elif event_type == "mouse" and action == "scroll":
                original_text.append(
                    f"鼠标操作 鼠标滚动: dx:{details['dx']} dy:{details['dy']} 间隔: {interval}"
                )
                i += 1
            elif event_type == "keyboard":
                key_name = details["name"]
                key_code = details["code"]
                action_map = {"down": "按下", "up": "抬起"}
                action_cn = action_map.get(action, action.capitalize())
                original_text.append(
                    f"键盘操作 {action_cn} {key_name}(keycode {key_code}) 间隔: {interval}"
                )
                i += 1

        # 获取当前文本内容

        current_text = self.text_edit.toPlainText().split("\n")
        current_text = [
            line.strip()
            for line in current_text
            if line.strip() and not line.strip().startswith("此处折叠")
        ]

        # 检查是否发生变化
        if current_text == original_text:
            QMessageBox.information(self, "提示", "内容未发生变化，无需保存")
            return

        # 构造最终 JSON 数据
        final_records = []
        i = 0
        original_i = 0
        while i < len(new_records):
            current = new_records[i]
            if (
                current.get("type") == "mouse"
                and current.get("action") == "move"
                and original_i < len(self.original_records)
            ):
                # 检查原始数据中是否有连续的鼠标移动
                move_records = []
                j = original_i
                while (
                    j < len(self.original_records)
                    and self.original_records[j].get("type") == "mouse"
                    and self.original_records[j].get("action") == "move"
                ):
                    move_records.append(self.original_records[j])
                    j += 1

                # 检查文本中是否有对应的两行鼠标移动
                if (
                    move_records
                    and i + 1 < len(new_records)
                    and new_records[i + 1].get("type") == "mouse"
                    and new_records[i + 1].get("action") == "move"
                ):
                    # 检查是否修改
                    first_new = new_records[i]
                    last_new = new_records[i + 1]
                    first_orig = move_records[0]
                    last_orig = move_records[-1]
                    total_orig_interval = sum(r["interval"] for r in move_records[1:])

                    # 如果首尾坐标或间隔有变化，则使用修改后的两行
                    if (
                        first_new["details"]["x"] != first_orig["details"]["x"]
                        or first_new["details"]["y"] != first_orig["details"]["y"]
                        or first_new["interval"] != first_orig["interval"]
                        or last_new["details"]["x"] != last_orig["details"]["x"]
                        or last_new["details"]["y"] != last_orig["details"]["y"]
                        or last_new["interval"] != total_orig_interval
                    ):
                        final_records.append(first_new)
                        final_records.append(last_new)
                    else:
                        # 未修改，保留原始序列
                        final_records.extend(move_records)
                    i += 2
                    original_i = j
                else:
                    # 单个鼠标移动，直接添加
                    final_records.append(current)
                    i += 1
                    original_i += 1
            else:
                # 其他操作直接添加
                final_records.append(current)
                i += 1
                original_i += 1

        if self.script_payload_type == "dict":
            self._enrich_ratio_for_mouse_records(final_records)
            meta = dict(self.script_meta) if isinstance(self.script_meta, dict) else {}
            meta.setdefault("version", 2)
            output_data = {"meta": meta, "records": final_records}
        else:
            output_data = final_records

        # 保存到文件
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            self.original_data = output_data
            self.original_records = final_records
            QMessageBox.information(self, "提示", "文件保存成功")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存文件失败: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = EditorWindow()
    editor.show()
    sys.exit(app.exec_())
