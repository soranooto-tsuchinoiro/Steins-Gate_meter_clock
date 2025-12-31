"""
配置文件管理模块
"""

import os

from PyQt5.QtCore import QSettings, QStandardPaths


class ConfigManager:
    """配置文件管理器"""

    def __init__(self):
        # 获取用户目录
        home_dir = QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0]
        config_dir = os.path.join(home_dir, ".Steins-Gate_meter_clock")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        config_file = os.path.join(config_dir, "config.ini")

        self.settings = QSettings(config_file, QSettings.IniFormat)

        # 如果文件不存在，设置默认值
        if not os.path.exists(config_file):
            self._set_defaults()

    def _set_defaults(self):
        """设置默认值"""
        self.settings.setValue("window_width", 400)
        self.settings.setValue("window_height", 200)
        self.settings.setValue("window_x", -1)  # -1表示未设置，使用屏幕中央
        self.settings.setValue("window_y", -1)
        self.settings.setValue("flash_duration_ms", 5000)
        self.settings.setValue("random_wait_short_ms", 60)
        self.settings.setValue("display_minutes", [0, 30])
        self.settings.sync()

    def get_window_width(self):
        return self.settings.value("window_width", 400, type=int)

    def set_window_width(self, value):
        self.settings.setValue("window_width", value)

    def get_window_height(self):
        return self.settings.value("window_height", 200, type=int)

    def set_window_height(self, value):
        self.settings.setValue("window_height", value)

    def get_window_x(self):
        value = self.settings.value("window_x", -1, type=int)
        if value == -1:
            # 计算屏幕中央
            from PyQt5.QtWidgets import QApplication

            screen = QApplication.primaryScreen()
            if screen is None:
                screen_geom = QApplication.desktop().availableGeometry()
            else:
                screen_geom = screen.availableGeometry()
            return (screen_geom.width() - self.get_window_width()) // 2
        return value

    def set_window_x(self, value):
        self.settings.setValue("window_x", value)

    def get_window_y(self):
        value = self.settings.value("window_y", -1, type=int)
        if value == -1:
            # 计算屏幕中央
            from PyQt5.QtWidgets import QApplication

            screen = QApplication.primaryScreen()
            if screen is None:
                screen_geom = QApplication.desktop().availableGeometry()
            else:
                screen_geom = screen.availableGeometry()
            return (screen_geom.height() - self.get_window_height()) // 2
        return value

    def set_window_y(self, value):
        self.settings.setValue("window_y", value)

    def get_flash_duration_ms(self):
        return self.settings.value("flash_duration_ms", 5000, type=int)

    def set_flash_duration_ms(self, value):
        self.settings.setValue("flash_duration_ms", value)

    def get_random_wait_short_ms(self):
        return self.settings.value("random_wait_short_ms", 60, type=int)

    def set_random_wait_short_ms(self, value):
        self.settings.setValue("random_wait_short_ms", value)

    def get_display_minutes(self):
        return self.settings.value("display_minutes", [0, 30], type=list)

    def set_display_minutes(self, value):
        self.settings.setValue("display_minutes", value)

    def save(self):
        """保存设置"""
        self.settings.sync()
