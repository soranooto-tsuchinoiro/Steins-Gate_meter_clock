"""
时间管理模块

负责判断当前时间是否在显示窗口内，以及是否应该触发世界线变动
"""

import time


class TimeManager:
    """时间管理器
    
    根据配置的报时时间节点，判断何时显示窗口和触发世界线变动
    """

    def __init__(self, config):
        """初始化时间管理器
        
        Args:
            config (ConfigManager): 配置管理器实例
        """
        self.config = config

    # ========================================================================
    # 公共方法 - 时间判断
    # ========================================================================

    def is_in_display_window(self):
        """检查当前时间是否在显示窗口内
        
        显示窗口定义：
        - 对于配置的每个分钟数（如0, 30）
        - 在该分钟前10秒到后10秒显示（共20秒）
        - 例如：整点显示为 X:59:50 - X:00:10
        
        Returns:
            bool: 是否在显示窗口内
        """
        current_time = time.localtime()
        minute = current_time.tm_min
        second = current_time.tm_sec

        display_minutes = self.config.get_display_minutes()

        for min_val in display_minutes:
            # 检查是否在指定分钟前10秒（前一分钟的50-59秒）
            if minute == abs((int(min_val) - 1) % 60) and second >= 50:
                return True
            # 检查是否在指定分钟后10秒（当前分钟的0-10秒）
            if minute == min_val and second <= 10:
                return True

        return False

    def should_trigger_meter(self):
        """检查是否应该触发世界线变动模式
        
        触发时机：在指定分钟前10秒（第50秒）时触发
        例如：在 X:59:50 触发整点报时前的世界线变动
        
        Returns:
            bool: 是否应该触发世界线变动
        """
        current_time = time.localtime()
        minute = current_time.tm_min
        second = current_time.tm_sec

        display_minutes = self.config.get_display_minutes()

        # 在指定分钟前10秒（第50秒）触发
        for min_val in display_minutes:
            if minute == abs((int(min_val) - 1) % 60) and second == 50:
                return True

        return False
