"""
UI组件基类
"""

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget
from constants import SHOW_WITHOUT_ACTIVATING


class FramelessWindow(QWidget):
    """无边框可拖拽窗口基类"""

    def __init__(self):
        """初始化无边框拖拽窗口"""
        super().__init__()
        # 无窗口边框，同时设置为工具窗口以便不在任务栏显示，并保持窗口始终置顶
        flags = Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        # 设置黑色背景
        self.setStyleSheet("background-color: black;")
        if SHOW_WITHOUT_ACTIVATING:
            # 在显示时尝试不抢占系统焦点
            self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setMouseTracking(True)

        # 初始化鼠标拖动相关的变量
        self.drag = False
        self._padding = 10
        self.drag_position = QPoint(0, 0)
        self.resize_drag = False
        self.resize_position = QPoint(0, 0)
        self.resize_width = 0
        self.resize_height = 0

    def mouseMoveEvent(self, event):
        """处理拖动或缩放时的移动"""
        if event.buttons() == Qt.LeftButton:
            if self.resize_drag:
                dx = event.globalX() - self.resize_position.x()
                dy = event.globalY() - self.resize_position.y()
                width = max(self.resize_width + dx, self.minimumWidth())
                height = max(self.resize_height + dy, self.minimumHeight())
                self.resize(width, height)
            elif self.drag:
                self.setCursor(QCursor(Qt.OpenHandCursor))
                self.move(event.globalPos() - self.drag_position)
        else:
            if (self.width() - event.x()) <= self._padding and (
                self.height() - event.y()
            ) <= self._padding:
                self.setCursor(Qt.SizeFDiagCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        """处理左键按下开始拖动或缩放"""
        if event.button() == Qt.LeftButton:
            if (self.width() - event.x()) <= self._padding and (
                self.height() - event.y()
            ) <= self._padding:
                self.resize_drag = True
                self.resize_position = event.globalPos()
                self.resize_width = self.width()
                self.resize_height = self.height()
            else:
                self.drag = True
                self.drag_position = event.globalPos() - self.pos()

    def mouseReleaseEvent(self, event):
        """处理左键释放结束拖动或缩放"""
        if event.button() == Qt.LeftButton:
            self.drag = False
            self.resize_drag = False
            self.setCursor(QCursor(Qt.ArrowCursor))
