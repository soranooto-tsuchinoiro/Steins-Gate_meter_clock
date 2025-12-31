"""
主窗口模块

应用程序的主窗口类，负责：
- 图片显示和渲染
- 自动报时逻辑
- 用户交互处理
- 窗口显示控制
"""

import io

from PIL import Image
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget

from config import ConfigManager
from constants import (
    MAIN_TIMER_INTERVAL_MS,
    TRIGGER_METER_BEFORE_ANNOUNCE,
    TYPE_CLOCK,
    TYPE_METER,
    get_meter_flash_duration_ms,
)
from threads import ImageThread
from time_manager import TimeManager
from tray_icon import TrayIconManager
from ui_components import FramelessWindow


class Divergence(FramelessWindow):
    """主窗口类
    
    基于FramelessWindow实现的主显示窗口
    整合了图片显示、时间管理、托盘图标等功能
    """

    def __init__(self, type_=TYPE_CLOCK):
        """初始化主窗口
        
        Args:
            type_ (str): 初始显示类型，默认为时钟模式
        """
        super().__init__()
        
        # 基本状态
        self.type_ = type_
        self.config = ConfigManager()
        
        # UI组件
        self.label = None
        self.worker = None
        self.origin_pic_size = None
        self.pixmap = None
        
        # 显示控制
        self.last_second = -1
        self.manual_show_mode = False
        self.trigger_meter_before_announce = TRIGGER_METER_BEFORE_ANNOUNCE
        
        # 定时器
        self.timer = None
        self.meter_timer = None
        
        # 管理器
        self.time_manager = TimeManager(self.config)
        self.tray_manager = None
        
        # 初始化所有组件
        self._init_ui()
        self._init_timers()
        self._init_tray()

    # ========================================================================
    # 私有方法 - 初始化
    # ========================================================================

    def _init_ui(self):
        """初始化UI组件"""
        # 创建图片显示标签
        self.label = QLabel(self)

        # 从配置文件获取窗口参数
        width = self.config.get_window_width()
        height = self.config.get_window_height()
        x = self.config.get_window_x()
        y = self.config.get_window_y()

        # 设置窗口大小和位置
        self.resize(width, height)
        self.label.resize(width, height)
        self.move(x, y)

        # 创建并启动图片生成线程
        self.worker = ImageThread(self.type_, self.config)
        self.worker.change_pic.connect(self.show_image)
        self.worker.start()

    def _init_timers(self):
        """初始化定时器"""
        # 主定时器：用于时间检查和自动显示控制
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._check_time_and_toggle)
        self.timer.start(MAIN_TIMER_INTERVAL_MS)

        # 世界线闪动定时器：单次触发，用于停止世界线模式
        self.meter_timer = QTimer(self)
        self.meter_timer.setSingleShot(True)
        self.meter_timer.timeout.connect(self._stop_meter_flash)

    def _init_tray(self):
        """初始化系统托盘"""
        self.tray_manager = TrayIconManager(self)
        self.tray_manager.create_tray_icon()

    # ========================================================================
    # 公共方法 - 窗口显示控制
    # ========================================================================

    def manual_show_window(self):
        """手动显示窗口（常显模式）"""
        self.manual_show_mode = True
        self.show()

    def manual_hide_window(self):
        """手动隐藏窗口（报时模式）"""
        self.manual_show_mode = False
        self.hide()

    def is_in_display_window(self):
        """检查当前是否在显示时间窗口内
        
        Returns:
            bool: 是否应该显示窗口
        """
        return self.time_manager.is_in_display_window()

    # ========================================================================
    # 私有方法 - 自动显示控制
    # ========================================================================

    def _check_time_and_toggle(self):
        """定时检查时间并控制窗口显示/隐藏
        
        每100ms调用一次，处理以下逻辑：
        1. 检查是否需要触发世界线变动
        2. 检查是否在显示窗口内
        3. 自动显示或隐藏窗口
        """
        # 手动模式下不执行自动控制
        if self.manual_show_mode:
            return

        # 避免重复处理同一秒
        import time
        current_time = time.localtime()
        current_second = current_time.tm_sec

        if current_second == self.last_second:
            return
        self.last_second = current_second

        # 检查是否触发世界线变动
        if self.time_manager.should_trigger_meter():
            if self.trigger_meter_before_announce:
                self.trigger_random_meter_once()

        # 检查是否应该显示窗口
        should_show = self.is_in_display_window()

        if should_show and not self.isVisible():
            self.show()
        elif not should_show and self.isVisible():
            self.hide()
            # 隐藏时如果是世界线模式，切换回时钟模式
            if self.type_ == TYPE_METER:
                self.type_ = TYPE_CLOCK
                self.worker.set_type(self.type_)

    # ========================================================================
    # 公共方法 - 世界线模式控制
    # ========================================================================

    def trigger_random_meter_once(self):
        """单次触发世界线变动模式
        
        显示指定时长的世界线变动动画，然后自动切换回时钟模式
        """
        duration = get_meter_flash_duration_ms(self.config)
        self.worker.set_duration(duration)
        self.type_ = TYPE_METER
        self.worker.set_type(self.type_)
        self.meter_timer.start(duration)
        
        # 如果窗口未显示则显示
        if not self.isVisible():
            self.show()

    def _stop_meter_flash(self):
        """停止世界线闪动，恢复时钟模式"""
        if self.type_ == TYPE_METER:
            self.type_ = TYPE_CLOCK
            self.worker.set_type(self.type_)

    # ========================================================================
    # 公共方法 - 图片显示
    # ========================================================================

    def show_image(self, raw_bytes, width, height):
        """接收并显示图片
        
        从图片生成线程接收原始RGBA字节数据并显示
        使用原始字节数据比PNG格式更快，减少界面卡顿
        
        Args:
            raw_bytes (bytes): RGBA格式的原始图片数据
            width (int): 图片宽度
            height (int): 图片高度
        """
        try:
            # 尝试直接从原始字节构建QImage（最快）
            bytes_per_line = width * 4
            qt_image = QImage(
                raw_bytes, width, height, bytes_per_line, QImage.Format_RGBA8888
            )
        except Exception:
            # 兼容性回退：通过PNG数据路径（较慢）
            buffer = io.BytesIO()
            img = Image.frombytes("RGBA", (width, height), raw_bytes)
            img.save(buffer, format="PNG")
            qt_image = QImage.fromData(buffer.getvalue(), "PNG")

        self.origin_pic_size = qt_image.size()
        self.pixmap = QPixmap.fromImage(qt_image)
        self.label.setPixmap(self.pixmap)

    # ========================================================================
    # 事件处理 - 绘制
    # ========================================================================

    def paintEvent(self, event):
        """窗口绘制事件
        
        按窗口尺寸缩放并居中显示图片
        
        Args:
            event (QPaintEvent): 绘制事件对象
        """
        if (self.origin_pic_size is not None) and (self.pixmap is not None):
            size = self.geometry().size()
            win_w = size.width()
            win_h = size.height()

            origin_w = self.origin_pic_size.width()
            origin_h = self.origin_pic_size.height()

            # 计算缩放比例（保持宽高比）
            scale = min(win_w / origin_w, win_h / origin_h)
            new_w = int(origin_w * scale)
            new_h = int(origin_h * scale)

            # 计算居中位置
            frame = self.frameGeometry()
            pos_x = (frame.width() - new_w) // 2
            pos_y = (frame.height() - new_h) // 2

            # 更新标签
            self.pixmap = self.pixmap.scaled(new_w, new_h, Qt.IgnoreAspectRatio)
            self.label.resize(new_w, new_h)
            self.label.move(pos_x, pos_y)
            self.label.setPixmap(self.pixmap)

        QWidget.paintEvent(self, event)

    # ========================================================================
    # 事件处理 - 键盘和鼠标
    # ========================================================================

    def keyPressEvent(self, event):
        """键盘按键事件
        
        按任意键隐藏窗口
        
        Args:
            event (QKeyEvent): 键盘事件对象
        """
        self.hide()
        if self.manual_show_mode:
            self.manual_show_mode = False

    def mousePressEvent(self, event):
        """鼠标按下事件
        
        右键触发世界线变动模式
        
        Args:
            event (QMouseEvent): 鼠标事件对象
        """
        if event.button() == Qt.RightButton:
            self.trigger_random_meter_once()
        FramelessWindow.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件
        
        双击切换最大化/正常大小
        
        Args:
            event (QMouseEvent): 鼠标事件对象
        """
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # ========================================================================
    # 事件处理 - 窗口状态变化
    # ========================================================================

    def resizeEvent(self, event):
        """窗口大小改变事件
        
        保存新的窗口尺寸到配置
        
        Args:
            event (QResizeEvent): 尺寸变化事件对象
        """
        super().resizeEvent(event)
        
        # 保存新尺寸
        self.config.set_window_width(self.width())
        self.config.set_window_height(self.height())
        self.config.save()
        
        # 调整标签尺寸
        self.label.resize(self.width(), self.height())

    def moveEvent(self, event):
        """窗口移动事件
        
        保存新的窗口位置到配置
        
        Args:
            event (QMoveEvent): 移动事件对象
        """
        super().moveEvent(event)
        
        # 保存新位置
        self.config.set_window_x(self.x())
        self.config.set_window_y(self.y())
        self.config.save()

    # ========================================================================
    # 公共方法 - 应用程序控制
    # ========================================================================

    def quit_application(self):
        """退出应用程序"""
        if self.tray_manager:
            self.tray_manager.hide()
        QApplication.quit()
