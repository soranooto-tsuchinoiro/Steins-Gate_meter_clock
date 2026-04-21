"""
系统托盘图标模块

管理系统托盘图标和右键菜单
"""

import io
import os

from PIL import Image, ImageDraw
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon

from autostart import disable, enable, is_enabled
from constants import TRAY_ICON_SIZE, TRAY_TOOLTIP
from settings_window import SettingsDialog


class TrayIconManager:
    """系统托盘图标管理器

    负责创建和管理系统托盘图标，提供快捷菜单功能
    """

    def __init__(self, parent):
        """初始化托盘图标管理器

        Args:
            parent (QWidget): 父窗口对象（主窗口）
        """
        self.parent = parent
        self.tray_icon = None
        self.mode_action = None
        self.display_mode = "timed"  # 默认报时模式

    # ========================================================================
    # 公共方法 - 托盘创建和管理
    # ========================================================================

    def create_tray_icon(self):
        """创建系统托盘图标

        优先使用项目中的logo.ico文件，若不存在则动态生成图标
        """
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        self.tray_icon = QSystemTrayIcon(self.parent)

        # 设置图标
        icon = self._load_icon()
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip(TRAY_TOOLTIP)

        # 创建右键菜单
        tray_menu = self._create_menu()
        self.tray_icon.setContextMenu(tray_menu)

        # 显示托盘图标
        self.tray_icon.show()

    def hide(self):
        """隐藏托盘图标"""
        if self.tray_icon:
            self.tray_icon.hide()

    # ========================================================================
    # 私有方法 - 图标加载
    # ========================================================================

    def _load_icon(self):
        """加载托盘图标

        优先尝试从assets/logo.ico加载，失败则动态生成

        Returns:
            QIcon: 托盘图标对象
        """
        try:
            base_dir = os.path.abspath(os.path.dirname(__file__))
            icon_path = os.path.join(base_dir, "assets", "logo.ico")
            if os.path.exists(icon_path):
                return QIcon(icon_path)
        except Exception:
            pass

        # 回退到动态生成图标
        return self._create_icon_image()

    def _create_icon_image(self):
        """动态创建托盘图标图像

        生成一个简化的世界线变动率显示样式的图标

        Returns:
            QIcon: 生成的图标对象
        """
        width = TRAY_ICON_SIZE
        height = TRAY_ICON_SIZE
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # 绘制黑色背景
        draw.rectangle([0, 0, width, height], fill=(0, 0, 0, 255))

        # 绘制简化的数字表示（7个白色方块）
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

    # ========================================================================
    # 私有方法 - 菜单创建
    # ========================================================================

    def _create_menu(self):
        """创建托盘右键菜单

        Returns:
            QMenu: 菜单对象
        """
        tray_menu = QMenu()

        # 显示模式切换菜单项
        self.mode_action = QAction("切换常显模式", self.parent)
        self.mode_action.triggered.connect(self._toggle_display_mode)
        tray_menu.addAction(self.mode_action)

        # 报时前世界线变动选项（可勾选）
        pre_announce_action = self._create_pre_announce_action()
        tray_menu.addAction(pre_announce_action)

        # 开机自启选项（可勾选）
        autostart_action = self._create_autostart_action()
        tray_menu.addAction(autostart_action)

        tray_menu.addSeparator()

        # 设置参数菜单项
        settings_action = QAction("设置参数", self.parent)
        settings_action.triggered.connect(self._open_settings)
        tray_menu.addAction(settings_action)

        tray_menu.addSeparator()

        # 退出菜单项
        quit_action = QAction("退出", self.parent)
        quit_action.triggered.connect(self.parent.quit_application)
        tray_menu.addAction(quit_action)

        return tray_menu

    def _create_pre_announce_action(self):
        """创建"报时前世界线变动"菜单项

        Returns:
            QAction: 菜单项对象
        """
        pre_announce_action = QAction("报时前世界线变动", self.parent)
        pre_announce_action.setCheckable(True)

        # 读取父对象的当前设置
        pre_announce_action.setChecked(
            getattr(self.parent, "trigger_meter_before_announce", True)
        )

        def _toggle_pre_announce(checked):
            """切换报时前世界线变动设置"""
            try:
                self.parent.trigger_meter_before_announce = bool(checked)
            except Exception:
                pass

        pre_announce_action.triggered.connect(_toggle_pre_announce)
        return pre_announce_action

    def _create_autostart_action(self):
        """创建"开机自启"菜单项

        Returns:
            QAction: 菜单项对象
        """
        autostart_action = QAction("开机自启", self.parent)
        autostart_action.setCheckable(True)
        autostart_action.setChecked(is_enabled())

        def _toggle_autostart(checked):
            """切换开机自启设置"""
            if checked:
                enable()
            else:
                disable()

        autostart_action.triggered.connect(_toggle_autostart)
        return autostart_action

    # ========================================================================
    # 私有方法 - 菜单动作处理
    # ========================================================================

    def _toggle_display_mode(self):
        """切换显示模式：常显模式 <-> 报时模式"""
        if self.display_mode == "timed":
            # 切换到常显模式
            self.display_mode = "always"
            self.mode_action.setText("切换报时模式")
            self.parent.manual_show_window()
        else:
            # 切换到报时模式
            self.display_mode = "timed"
            self.mode_action.setText("切换常显模式")
            self.parent.manual_hide_window()

    def _open_settings(self):
        """打开设置对话框"""
        dialog = SettingsDialog(self.parent.config, self.parent)
        dialog.exec_()
