"""
时间管理相关功能
"""

import time


class TimeManager:
    # 时间管理器

    def __init__(self, config):
        self.config = config

    # 检查当前时间是否在显示窗口内
    # 默认整点: X:59:50 - X:00:10 (20秒)
    # 半点: X:29:50 - X:30:10 (20秒)
    def is_in_display_window(self):
        current_time = time.localtime()
        minute = current_time.tm_min
        second = current_time.tm_sec

        display_minutes = self.config.get_display_minutes()

        for min_val in display_minutes:
            # 检查是否在指定分钟的显示窗口
            if minute == abs((int(min_val) - 1) % 60) and second >= 50:
                return True
            if minute == min_val and second <= 10:
                return True

        return False

    # 检查是否应该触发 meter 模式(在第50秒时)
    def should_trigger_meter(self):
        current_time = time.localtime()
        minute = current_time.tm_min
        second = current_time.tm_sec

        display_minutes = self.config.get_display_minutes()

        # 在指定分钟前10秒触发
        for min_val in display_minutes:
            if minute == abs((int(min_val) - 1) % 60) and second == 50:
                return True

        return False
