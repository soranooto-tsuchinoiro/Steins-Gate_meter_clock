"""
UI组件基类模块

提供无边框窗口等基础UI组件
"""

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget

from constants import SHOW_WITHOUT_ACTIVATING


class FramelessWindow(QWidget):
    """无边框可拖拽窗口基类
    
    提供以下功能：
    - 无边框窗口
    - 左键拖动移动窗口
    - 拖动右下角调整窗口大小
    - 始终置顶显示
    - 可选的不抢占焦点
    """

    def __init__(self):
        """初始化无边框窗口"""
        super().__init__()
        
        # 设置窗口标志：无边框、工具窗口（不显示在任务栏）、始终置顶
        flags = Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        
        # 设置黑色背景
        self.setStyleSheet("background-color: black;")
        
        # 如果配置为不抢占焦点，则设置相应属性
        if SHOW_WITHOUT_ACTIVATING:
            self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        
        # 启用鼠标追踪
        self.setMouseTracking(True)

        # 初始化拖动相关变量
        self._init_drag_variables()

    # ========================================================================
    # 私有方法 - 初始化
    # ========================================================================

    def _init_drag_variables(self):
        """初始化拖动和缩放相关的变量"""
        self.drag = False  # 是否正在拖动窗口
        self._padding = 10  # 右下角缩放区域的大小（像素）
        self.drag_position = QPoint(0, 0)  # 拖动时的鼠标相对位置
        
        self.resize_drag = False  # 是否正在缩放窗口
        self.resize_position = QPoint(0, 0)  # 缩放时的起始鼠标位置
        self.resize_width = 0  # 缩放时的起始窗口宽度
        self.resize_height = 0  # 缩放时的起始窗口高度

    # ========================================================================
    # 鼠标事件处理 - 拖动和缩放
    # ========================================================================

    def mouseMoveEvent(self, event):
        """处理鼠标移动事件
        
        根据当前状态执行拖动或缩放操作，并更新鼠标光标样式
        
        Args:
            event (QMouseEvent): 鼠标事件对象
        """
        if event.buttons() == Qt.LeftButton:
            if self.resize_drag:
                # 缩放模式：调整窗口大小
                dx = event.globalX() - self.resize_position.x()
                dy = event.globalY() - self.resize_position.y()
                width = max(self.resize_width + dx, self.minimumWidth())
                height = max(self.resize_height + dy, self.minimumHeight())
                self.resize(width, height)
            elif self.drag:
                # 拖动模式：移动窗口
                self.setCursor(QCursor(Qt.OpenHandCursor))
                self.move(event.globalPos() - self.drag_position)
        else:
            # 未按下左键：根据鼠标位置更新光标样式
            if self._is_in_resize_area(event):
                self.setCursor(Qt.SizeFDiagCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        """处理鼠标按下事件
        
        判断是开始拖动还是缩放操作
        
        Args:
            event (QMouseEvent): 鼠标事件对象
        """
        if event.button() == Qt.LeftButton:
            if self._is_in_resize_area(event):
                # 鼠标在右下角：开始缩放
                self.resize_drag = True
                self.resize_position = event.globalPos()
                self.resize_width = self.width()
                self.resize_height = self.height()
            else:
                # 鼠标在其他位置：开始拖动
                self.drag = True
                self.drag_position = event.globalPos() - self.pos()

    def mouseReleaseEvent(self, event):
        """处理鼠标释放事件
        
        结束拖动或缩放操作
        
        Args:
            event (QMouseEvent): 鼠标事件对象
        """
        if event.button() == Qt.LeftButton:
            self.drag = False
            self.resize_drag = False
            self.setCursor(QCursor(Qt.ArrowCursor))

    # ========================================================================
    # 辅助方法
    # ========================================================================

    def _is_in_resize_area(self, event):
        """判断鼠标是否在窗口右下角的缩放区域内
        
        Args:
            event (QMouseEvent): 鼠标事件对象
            
        Returns:
            bool: 是否在缩放区域内
        """
        return (
            (self.width() - event.x()) <= self._padding
            and (self.height() - event.y()) <= self._padding
        )
