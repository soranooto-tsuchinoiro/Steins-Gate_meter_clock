"""
图片处理工具模块

负责生成时钟和世界线显示所需的图片
"""

import datetime
import os
import random
import time
from typing import Callable, Iterable

from PIL import Image, ImageOps

from constants import (
    CLOCK_FRAME_INTERVAL_MS,
    IMAGE_DIGITS,
    IMAGE_DIR_NAME,
    get_random_wait_short_ms,
)

# 模块级变量：控制时钟显示格式切换（使用null还是.作为分隔符）
NULL_FLAG = False


class ImageOptionMixin:
    """图片操作混入类
    
    提供图片拼接、边框等基础操作方法
    """

    @staticmethod
    def concat_h(img_list):
        """水平拼接图片列表
        
        Args:
            img_list (list): PIL.Image对象列表
            
        Returns:
            PIL.Image: 拼接后的图片
        """
        total_width = sum(img.width for img in img_list)
        max_height = max(img.height for img in img_list)

        dst = Image.new("RGB", (total_width, max_height))
        offset = 0
        for img in img_list:
            dst.paste(img, (offset, 0))
            offset += img.width

        return dst

    @staticmethod
    def add_border(img, w, h):
        """为图片添加边框
        
        Args:
            img (PIL.Image): 原始图片
            w (int): 边框宽度
            h (int): 边框高度
            
        Returns:
            PIL.Image: 添加边框后的图片
        """
        return ImageOps.expand(img, border=(0, 0))


class ImageGenerator(ImageOptionMixin):
    """图片生成器
    
    负责生成时钟和世界线显示所需的图片序列
    """

    def __init__(self, config=None, duration=None):
        """初始化图片生成器
        
        Args:
            config (ConfigManager, optional): 配置管理器
            duration (int, optional): 显示持续时间（毫秒）
        """
        self.config = config
        self.duration = duration
        self._img_map = self._get_img_map()

    # ========================================================================
    # 私有方法 - 资源加载
    # ========================================================================

    @staticmethod
    def _get_img_map():
        """加载数字与小数点图片资源
        
        Returns:
            dict: 图片映射字典 {字符: PIL.Image对象}
        """
        dir_path = os.path.abspath(os.path.dirname(__file__))
        return {
            i: Image.open(os.path.join(dir_path, IMAGE_DIR_NAME, f"{i}.jpg"))
            for i in IMAGE_DIGITS
        }

    # ========================================================================
    # 私有方法 - 时钟生成逻辑
    # ========================================================================

    def _generate_clock(self, next_wait_ms=None):
        """生成当前时间字符串
        
        交替使用"."和"null"作为时间分隔符，产生动态效果
        
        Args:
            next_wait_ms (int, optional): 下次等待时间（未使用）
            
        Returns:
            list: 时间字符列表，如['0','9','.','3','0','.','4','5']
        """
        global NULL_FLAG
        if NULL_FLAG:
            time_list = list(datetime.datetime.now().strftime("%H%M%S"))
            time_list.insert(2, "null")
            time_list.insert(5, "null")
        else:
            time_list = list(datetime.datetime.now().strftime("%H.%M.%S"))
        
        # 切换分隔符标志
        NULL_FLAG = not NULL_FLAG
        return time_list

    # ========================================================================
    # 私有方法 - 世界线生成逻辑
    # ========================================================================

    def _generate_meter(self, next_wait_ms=None):
        """生成世界线变动率字符串
        
        如果next_wait_ms表示长时显示，则从预定义的世界线数据中选择
        否则快速随机生成数字
        
        Args:
            next_wait_ms (int, optional): 下次等待时间
            
        Returns:
            list: 世界线数字字符列表，如['1','.','0','4','8','5','9','6']
        """
        from constants import ATTRACTOR_FIELD

        # 长时间展示模式：从真实世界线数据中选择
        if next_wait_ms is not None and next_wait_ms >= get_random_wait_short_ms(
            self.config
        ):
            group = random.choice(ATTRACTOR_FIELD)
            return list(random.choice(group))

        # 快速随机刷新模式：生成随机数字
        num_list = [str(random.randint(0, 9)) for _ in range(7)]
        num_list.insert(1, ".")
        return num_list

    # ========================================================================
    # 私有方法 - 等待时间控制
    # ========================================================================

    def _random_wait_time(self):
        """返回随机等待时间生成器
        
        控制世界线闪动的节奏：前19次快速闪动，第20次长时间显示
        
        Returns:
            Callable: 等待时间生成函数
        """
        accumulated = 0
        i = 1

        def core():
            nonlocal accumulated, i
            if i >= 20:
                # 第20次：返回剩余时间用于长时显示
                remaining = self.duration - accumulated
                accumulated = 0
                i = 1
                return remaining
            else:
                # 前19次：短时快速闪动
                wait = get_random_wait_short_ms(self.config) if self.config else 60
                accumulated += wait
                i += random.choice([0, 0, 0, 1, 1, 2])
                return wait

        return core

    # ========================================================================
    # 公共方法 - 图片生成
    # ========================================================================

    def generate_image(self, num_list):
        """将字符列表拼接为图片
        
        Args:
            num_list (list): 字符列表
            
        Returns:
            PIL.Image: 拼接后的图片
        """
        img_list = [self._img_map[i] for i in num_list]
        img = self.concat_h(img_list)
        return img

    def generate(self, gen_img_list, gen_wait_time):
        """生成图片流的通用方法
        
        Args:
            gen_img_list (Callable): 字符列表生成函数
            gen_wait_time (Callable): 等待时间生成函数
            
        Yields:
            PIL.Image: 生成的图片
        """
        while True:
            # 先决定本次展示之后的等待时长
            wait = gen_wait_time()

            img_list = gen_img_list(wait)
            if not img_list:
                break

            img = self.generate_image(img_list)
            yield img

            if not wait:
                break
            time.sleep(wait / 1000)

    # ========================================================================
    # 公共方法 - 模式特定生成器
    # ========================================================================

    def meter(self, wait_time=None):
        """生成世界线变动率图片流
        
        Args:
            wait_time (Callable, optional): 自定义等待时间函数
            
        Yields:
            PIL.Image: 世界线图片序列
        """
        wait_time = self._random_wait_time() if not wait_time else wait_time
        return self.generate(self._generate_meter, wait_time)

    def clock(self):
        """生成时钟图片流
        
        Yields:
            PIL.Image: 时钟图片序列
        """
        return self.generate(self._generate_clock, lambda: CLOCK_FRAME_INTERVAL_MS)
