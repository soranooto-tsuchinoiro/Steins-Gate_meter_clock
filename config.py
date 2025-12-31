"""
配置文件管理模块

负责应用程序配置的读取、写入和持久化
"""

import os
from PyQt5.QtCore import QSettings, QStandardPaths


class ConfigManager:
    """配置文件管理器
    
    管理应用程序的所有配置项，包括窗口位置、大小、显示参数等
    配置文件存储在用户目录的 .Steins-Gate_meter_clock/config.ini
    """

    def __init__(self):
        """初始化配置管理器，创建配置目录和文件"""
        # 获取用户主目录
        home_dir = QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0]
        config_dir = os.path.join(home_dir, ".Steins-Gate_meter_clock")
        
        # 确保配置目录存在
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        config_file = os.path.join(config_dir, "config.ini")
        self.settings = QSettings(config_file, QSettings.IniFormat)

        # 如果配置文件不存在，设置默认值
        if not os.path.exists(config_file):
            self._set_defaults()

    # ========================================================================
    # 私有方法 - 初始化
    # ========================================================================

    def _set_defaults(self):
        """设置默认配置值"""
        self.settings.setValue("window_width", 400)
        self.settings.setValue("window_height", 200)
        self.settings.setValue("window_x", -1)  # -1表示未设置，使用屏幕中央
        self.settings.setValue("window_y", -1)
        self.settings.setValue("flash_duration_ms", 5000)
        self.settings.setValue("random_wait_short_ms", 60)
        self.settings.setValue("display_minutes", [0, 30])
        self.settings.sync()

    # ========================================================================
    # 公共方法 - 窗口尺寸配置
    # ========================================================================

    def get_window_width(self):
        """获取窗口宽度
        
        Returns:
            int: 窗口宽度（像素），默认400
        """
        return self.settings.value("window_width", 400, type=int)

    def set_window_width(self, value):
        """设置窗口宽度
        
        Args:
            value (int): 窗口宽度（像素）
        """
        self.settings.setValue("window_width", value)

    def get_window_height(self):
        """获取窗口高度
        
        Returns:
            int: 窗口高度（像素），默认200
        """
        return self.settings.value("window_height", 200, type=int)

    def set_window_height(self, value):
        """设置窗口高度
        
        Args:
            value (int): 窗口高度（像素）
        """
        self.settings.setValue("window_height", value)

    # ========================================================================
    # 公共方法 - 窗口位置配置
    # ========================================================================

    def get_window_x(self):
        """获取窗口X坐标
        
        如果未设置（值为-1），则自动计算屏幕中央位置
        
        Returns:
            int: 窗口X坐标（像素）
        """
        value = self.settings.value("window_x", -1, type=int)
        if value == -1:
            # 计算屏幕中央X坐标
            from PyQt5.QtWidgets import QApplication
            screen = QApplication.primaryScreen()
            if screen is None:
                screen_geom = QApplication.desktop().availableGeometry()
            else:
                screen_geom = screen.availableGeometry()
            return (screen_geom.width() - self.get_window_width()) // 2
        return value

    def set_window_x(self, value):
        """设置窗口X坐标
        
        Args:
            value (int): 窗口X坐标（像素）
        """
        self.settings.setValue("window_x", value)

    def get_window_y(self):
        """获取窗口Y坐标
        
        如果未设置（值为-1），则自动计算屏幕中央位置
        
        Returns:
            int: 窗口Y坐标（像素）
        """
        value = self.settings.value("window_y", -1, type=int)
        if value == -1:
            # 计算屏幕中央Y坐标
            from PyQt5.QtWidgets import QApplication
            screen = QApplication.primaryScreen()
            if screen is None:
                screen_geom = QApplication.desktop().availableGeometry()
            else:
                screen_geom = screen.availableGeometry()
            return (screen_geom.height() - self.get_window_height()) // 2
        return value

    def set_window_y(self, value):
        """设置窗口Y坐标
        
        Args:
            value (int): 窗口Y坐标（像素）
        """
        self.settings.setValue("window_y", value)

    # ========================================================================
    # 公共方法 - 显示效果配置
    # ========================================================================

    def get_flash_duration_ms(self):
        """获取世界线闪动持续时间
        
        Returns:
            int: 闪动持续时间（毫秒），默认5000
        """
        return self.settings.value("flash_duration_ms", 5000, type=int)

    def set_flash_duration_ms(self, value):
        """设置世界线闪动持续时间
        
        Args:
            value (int): 闪动持续时间（毫秒）
        """
        self.settings.setValue("flash_duration_ms", value)

    def get_random_wait_short_ms(self):
        """获取随机等待短时长
        
        Returns:
            int: 短时等待时长（毫秒），默认60
        """
        return self.settings.value("random_wait_short_ms", 60, type=int)

    def set_random_wait_short_ms(self, value):
        """设置随机等待短时长
        
        Args:
            value (int): 短时等待时长（毫秒）
        """
        self.settings.setValue("random_wait_short_ms", value)

    # ========================================================================
    # 公共方法 - 报时时间配置
    # ========================================================================

    def get_display_minutes(self):
        """获取显示时间节点列表
        
        Returns:
            list: 分钟数列表，默认[0, 30]表示整点和半点
        """
        return self.settings.value("display_minutes", [0, 30], type=list)

    def set_display_minutes(self, value):
        """设置显示时间节点列表
        
        Args:
            value (list): 分钟数列表
        """
        self.settings.setValue("display_minutes", value)

    # ========================================================================
    # 公共方法 - 配置持久化
    # ========================================================================

    def save(self):
        """保存所有设置到磁盘"""
        self.settings.sync()
