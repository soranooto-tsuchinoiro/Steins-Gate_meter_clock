"""
系统托盘图标相关功能
"""

import io
import os
from PIL import Image, ImageDraw
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from constants import TRAY_TOOLTIP, TRAY_ICON_SIZE


class TrayIconManager:
    """系统托盘图标管理器"""

    def __init__(self, parent):
        self.parent = parent
        self.tray_icon = None
        self.show_action = None
        self.hide_action = None
        self.auto_hide_action = None

    def create_tray_icon(self):
        """创建系统托盘图标"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        self.tray_icon = QSystemTrayIcon(self.parent)
        # 优先使用项目 assets/logo.ico 作为托盘图标（若存在），否则回退到动态生成图标
        try:
            base_dir = os.path.abspath(os.path.dirname(__file__))
            icon_path = os.path.join(base_dir, 'assets', 'logo.ico')
            if os.path.exists(icon_path):
                self.tray_icon.setIcon(QIcon(icon_path))
            else:
                self.tray_icon.setIcon(self._create_icon_image())
        except Exception:
            self.tray_icon.setIcon(self._create_icon_image())
        self.tray_icon.setToolTip(TRAY_TOOLTIP)

        # 创建菜单
        tray_menu = self._create_menu()
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._on_activated)
        self.tray_icon.show()

    def _create_menu(self):
        """创建托盘菜单"""
        tray_menu = QMenu()

        # 合并显示/隐藏为单个菜单项，手动触发时关闭报时模式
        def _toggle_visibility():
            if self.parent.isVisible():
                self.parent.manual_hide_window()
            else:
                self.parent.manual_show_window()
            # 手动触发显示/隐藏时，关闭自动报时模式
            try:
                self.parent.auto_hide_enabled = False
                if hasattr(self, "auto_hide_action") and self.auto_hide_action:
                    self.auto_hide_action.setChecked(False)
            except Exception:
                pass

        toggle_action = QAction("显示/隐藏", self.parent)
        toggle_action.triggered.connect(_toggle_visibility)
        tray_menu.addAction(toggle_action)

        tray_menu.addSeparator()

        # 报时模式（自动显示/隐藏）切换
        self.auto_hide_action = QAction("报时模式", self.parent)
        self.auto_hide_action.setCheckable(True)
        self.auto_hide_action.setChecked(self.parent.auto_hide_enabled)
        self.auto_hide_action.triggered.connect(self.parent.toggle_auto_hide)
        tray_menu.addAction(self.auto_hide_action)

        tray_menu.addSeparator()

        # 报时前世界线变动选项（是否在报时前先触发 meter）
        pre_announce_action = QAction("报时前世界线变动", self.parent)
        pre_announce_action.setCheckable(True)
        # 读取父对象的属性（Divergence.trigger_meter_before_announce）作为初始状态
        pre_announce_action.setChecked(
            getattr(self.parent, "trigger_meter_before_announce", True)
        )

        def _toggle_pre_announce(checked):
            try:
                self.parent.trigger_meter_before_announce = bool(checked)
            except Exception:
                pass

        pre_announce_action.triggered.connect(_toggle_pre_announce)
        tray_menu.addAction(pre_announce_action)

        # 退出菜单项
        quit_action = QAction("退出", self.parent)
        quit_action.triggered.connect(self.parent.quit_application)
        tray_menu.addAction(quit_action)

        return tray_menu

    def _create_icon_image(self):
        """创建托盘图标图像"""
        width = TRAY_ICON_SIZE
        height = TRAY_ICON_SIZE
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # 绘制黑色背景
        draw.rectangle([0, 0, width, height], fill=(0, 0, 0, 255))

        # 绘制简化的数字表示
        block_size = 4
        spacing = 2
        start_x = 8
        start_y = height // 2 - block_size

        for i in range(7):
            x = start_x + i * (block_size + spacing)
            draw.rectangle(
                [x, start_y, x + block_size, start_y + block_size * 2],
                fill=(255, 255, 255, 255),
            )

        # 转换为 QIcon
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        qt_image = QImage.fromData(buffer.getvalue(), "PNG")
        pixmap = QPixmap.fromImage(qt_image)
        return QIcon(pixmap)

    def _on_activated(self, reason):
        """托盘图标激活事件"""
        if reason in (QSystemTrayIcon.DoubleClick, QSystemTrayIcon.Trigger):
            if self.parent.isVisible():
                self.parent.manual_hide_window()
            else:
                self.parent.manual_show_window()

    def hide(self):
        """隐藏托盘图标"""
        if self.tray_icon:
            self.tray_icon.hide()
