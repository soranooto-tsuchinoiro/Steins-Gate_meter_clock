"""
主窗口类
"""

import io
import time

from PIL import Image
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget

from constants import (
    LABEL_HEIGHT_PCT,
    LABEL_WIDTH_PCT,
    MAIN_TIMER_INTERVAL_MS,
    METER_FLASH_DURATION_MS,
    TOP_OFFSET_PCT,
    TRIGGER_METER_BEFORE_ANNOUNCE,
    TYPE_CLOCK,
    TYPE_METER,
)
from threads import ImageThread
from time_manager import TimeManager
from tray_icon import TrayIconManager
from ui_components import FramelessWindow


class Divergence(FramelessWindow):
    """主窗口类"""

    def __init__(self, type_=TYPE_CLOCK):
        """初始化显示窗口、定时器与托盘"""
        super().__init__()
        self.type_ = type_

        # UI组件
        self.label = None
        self.worker = None
        self.origin_pic_size = None
        self.pixmap = None

        # 自动隐藏相关
        self.last_second = -1
        self.manual_show_mode = False

        # 定时器
        self.timer = None
        self.meter_timer = None

        # 托盘管理器
        self.tray_manager = None

        # 时间管理器
        self.time_manager = TimeManager()
        # 是否在报时前先触发 meter（可由托盘菜单切换）
        self.trigger_meter_before_announce = TRIGGER_METER_BEFORE_ANNOUNCE

        # 初始化
        self._init_ui()
        self._init_timers()
        self._init_tray()

    def _init_ui(self):
        """初始化UI组件"""
        self.label = QLabel(self)
        # 根据屏幕可用区域按百分比计算初始窗口与标签尺寸
        screen = QApplication.primaryScreen()
        if screen is None:
            screen_geom = QApplication.desktop().availableGeometry()
        else:
            screen_geom = screen.availableGeometry()

        screen_w = screen_geom.width()
        screen_h = screen_geom.height()

        label_w = int(screen_w * LABEL_WIDTH_PCT)
        label_h = int(screen_h * LABEL_HEIGHT_PCT)

        # 将窗口大小设置为标签大小并定位到屏幕中央，距离顶部5%
        self.resize(label_w, label_h)
        self.label.resize(label_w, label_h)
        x = screen_geom.x() + (screen_w - label_w) // 2
        y = screen_geom.y() + int(screen_h * TOP_OFFSET_PCT)
        self.move(x, y)

        self.worker = ImageThread(self.type_)
        self.worker.change_pic.connect(self.show_image)
        self.worker.start()

    def _init_timers(self):
        """初始化定时器"""
        # 主定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._check_time_and_toggle)
        self.timer.start(MAIN_TIMER_INTERVAL_MS)

        # Meter闪动定时器
        self.meter_timer = QTimer(self)
        self.meter_timer.setSingleShot(True)
        self.meter_timer.timeout.connect(self._stop_meter_flash)

    def _init_tray(self):
        """初始化系统托盘"""
        self.tray_manager = TrayIconManager(self)
        self.tray_manager.create_tray_icon()

    # ========================================================================
    # 窗口显示控制
    # ========================================================================

    def manual_show_window(self):
        """手动显示窗口"""
        self.manual_show_mode = True
        self.show()

    def manual_hide_window(self):
        """手动隐藏窗口"""
        self.manual_show_mode = False
        self.hide()

    # ========================================================================
    # 时间检查与自动显示/隐藏
    # ========================================================================

    def is_in_display_window(self):
        """检查当前时间是否在显示窗口内"""
        return self.time_manager.is_in_display_window()

    def _check_time_and_toggle(self):
        """定时器回调函数: 检查时间并控制窗口显示/隐藏"""
        if self.manual_show_mode:
            return

        current_time = time.localtime()
        current_second = current_time.tm_sec

        if current_second == self.last_second:
            return

        self.last_second = current_second

        # 检查是否应该触发 meter 模式（可配置：是否在报时前先触发）
        if self.time_manager.should_trigger_meter():
            if self.trigger_meter_before_announce:
                self.trigger_random_meter_once()

        # 检查是否在显示窗口内
        should_show = self.is_in_display_window()

        if should_show and not self.isVisible():
            self.show()
        elif not should_show and self.isVisible():
            self.hide()
            if self.type_ == TYPE_METER:
                self.type_ = TYPE_CLOCK
                self.worker.set_type(self.type_)

    # ========================================================================
    # Meter模式相关
    # ========================================================================

    def trigger_random_meter_once(self):
        """单次触发随机数字展示逻辑"""
        self.type_ = TYPE_METER
        self.worker.set_type(self.type_)
        self.meter_timer.start(METER_FLASH_DURATION_MS)
        if not self.isVisible():
            self.show()

    def _stop_meter_flash(self):
        """结束短时随机闪动, 恢复时钟模式"""
        if self.type_ == TYPE_METER:
            self.type_ = TYPE_CLOCK
            self.worker.set_type(self.type_)

    # ========================================================================
    # 图片显示
    # ========================================================================

    def show_image(self, raw_bytes, width, height):
        """接收线程发来的原始 RGBA bytes 并更新标签（在 GUI 线程）
        使用原始像素数据构建 QImage，比在主线程中保存/解析 PNG 快得多，
        可显著减少快速切换时的界面卡顿。
        """
        try:
            bytes_per_line = width * 4
            qt_image = QImage(
                raw_bytes, width, height, bytes_per_line, QImage.Format_RGBA8888
            )
        except Exception:
            # 兼容性回退：如果构造失败，尝试通过 PNG 数据路径（更慢）
            buffer = io.BytesIO()
            img = Image.frombytes("RGBA", (width, height), raw_bytes)
            img.save(buffer, format="PNG")
            qt_image = QImage.fromData(buffer.getvalue(), "PNG")

        self.origin_pic_size = qt_image.size()
        self.pixmap = QPixmap.fromImage(qt_image)
        self.label.setPixmap(self.pixmap)

    def paintEvent(self, event):
        """按窗口尺寸缩放并居中图片"""
        if (self.origin_pic_size is not None) and (self.pixmap is not None):
            size = self.geometry().size()
            win_w = size.width()
            win_h = size.height()

            origin_w = self.origin_pic_size.width()
            origin_h = self.origin_pic_size.height()

            scale = min(win_w / origin_w, win_h / origin_h)
            new_w = int(origin_w * scale)
            new_h = int(origin_h * scale)

            frame = self.frameGeometry()
            pos_x = (frame.width() - new_w) // 2
            pos_y = (frame.height() - new_h) // 2

            self.pixmap = self.pixmap.scaled(new_w, new_h, Qt.IgnoreAspectRatio)
            self.label.resize(new_w, new_h)
            self.label.move(pos_x, pos_y)
            self.label.setPixmap(self.pixmap)

        QWidget.paintEvent(self, event)

    # ========================================================================
    # 事件处理
    # ========================================================================

    def keyPressEvent(self, event):
        """按键时隐藏窗口"""
        self.hide()
        if self.manual_show_mode:
            self.manual_show_mode = False

    def mousePressEvent(self, event):
        """右键切换模式并可显示窗口"""
        if event.button() == Qt.RightButton:
            self.trigger_random_meter_once()
        FramelessWindow.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        """双击切换最大化/还原"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def quit_application(self):
        """退出应用程序"""
        if self.tray_manager:
            self.tray_manager.hide()
        QApplication.quit()
