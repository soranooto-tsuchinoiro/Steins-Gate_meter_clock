"""
时间管理相关功能
"""

import time


class TimeManager:
    """时间管理器"""

    @staticmethod
    def is_in_display_window():
        """
        检查当前时间是否在显示窗口内
        整点: X:59:50 - X:00:10 (20秒)
        半点: X:29:50 - X:30:10 (20秒)
        """
        current_time = time.localtime()
        minute = current_time.tm_min
        second = current_time.tm_sec

        # 检查是否在整点的显示窗口
        if minute == 59 and second >= 50:
            return True
        if minute == 0 and second <= 10:
            return True

        # 检查是否在半点的显示窗口
        if minute == 29 and second >= 50:
            return True
        if minute == 30 and second <= 10:
            return True

        return False

    @staticmethod
    def should_trigger_meter():
        """
        检查是否应该触发 meter 模式(在第50秒时)
        """
        current_time = time.localtime()
        minute = current_time.tm_min
        second = current_time.tm_sec

        # 在整点前10秒(59:50)或半点前10秒(29:50)触发
        if (minute == 59 and second == 50) or (minute == 29 and second == 50):
            return True

        return False
