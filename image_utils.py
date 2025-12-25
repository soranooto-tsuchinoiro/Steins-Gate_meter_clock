"""
图片处理相关工具类
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
    RANDOM_WAIT_LONG_MS,
    RANDOM_WAIT_SHORT_MS,
)

# 模块级开关：用于控制 `_generate_clock` 返回不同格式的时间字符串（默认 False）
NULL_FLAG = False


class ImageOptionMixin:
    """图片操作混入类"""

    @staticmethod
    def concat_h(img_list):
        """水平拼接图片列表"""
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
        """为图片添加边框"""
        return ImageOps.expand(img, border=(0, 0))


class ImageGenerator(ImageOptionMixin):
    """图片生成器"""

    def __init__(self):
        """初始化图片映射"""
        self._img_map = self._get_img_map()

    @staticmethod
    def _get_img_map() -> dict:
        """加载数字与小数点图片"""
        dir_path = os.path.abspath(os.path.dirname(__file__))
        return {
            i: Image.open(os.path.join(dir_path, IMAGE_DIR_NAME, f"{i}.jpg"))
            for i in IMAGE_DIGITS
        }

    @staticmethod
    def _random_wait_time() -> Callable:
        """返回随机等待时间闭包"""
        i = 1

        def core():
            nonlocal i
            if i >= 20:
                i = 1
                return RANDOM_WAIT_LONG_MS
            else:
                i += random.choice([0, 0, 0, 1, 1, 2])
                return RANDOM_WAIT_SHORT_MS

        return core

    def _generate_clock(self, next_wait_ms: int = None) -> list:
        """生成当前时间字符串（返回字符列表）。"""
        global NULL_FLAG
        if NULL_FLAG:
            time_list = list(datetime.datetime.now().strftime("%H%M%S"))
            time_list.insert(2, "null")
            time_list.insert(5, "null")
        else:
            time_list = list(datetime.datetime.now().strftime("%H.%M.%S"))
        # 切换全局标志为相反值
        NULL_FLAG = not NULL_FLAG
        return time_list

    def _generate_meter(self, next_wait_ms: int = None) -> str:
        """生成随机数表盘字符串。
        当 `next_wait_ms` 表示一个较长的展示期（等于 RANDOM_WAIT_LONG_MS）时，
        从 `ATTRACTOR_FIELD` 中随机选取一个子集合，再从子集合中随机选取一个值返回用于长时展示。
        否则保留原先的快速随机逻辑。
        """
        from constants import ATTRACTOR_FIELD, RANDOM_WAIT_LONG_MS

        # 如果接下来将是长时间展示，则从 ATTRACTOR_FIELD 中取值用于展示
        if next_wait_ms is not None and next_wait_ms >= RANDOM_WAIT_LONG_MS:
            group = random.choice(ATTRACTOR_FIELD)
            return list(random.choice(group))

        # 快速随机刷新逻辑（保持原样），返回列表格式以供 generate_image 使用
        num_list = [str(random.randint(0, 9)) for _ in range(7)]
        num_list.insert(1, ".")
        return num_list

    def generate_image(self, num_list: list):
        """将字符串拼接为带边框图片"""
        img_list = [self._img_map[i] for i in num_list]
        img = self.concat_h(img_list)
        return img

    def generate(self, gen_img_list: Callable, gen_wait_time: Callable) -> Iterable:
        """组合生成图片并控制节奏"""
        while True:
            # 先决定本次展示之后的等待时长（用于告知生成函数是否为“长时展示”）
            wait = gen_wait_time()

            img_list = gen_img_list(wait)
            if not img_list:
                break

            img = self.generate_image(img_list)
            yield img

            if not wait:
                break
            time.sleep(wait / 1000)

    def meter(self, wait_time=None) -> Iterable:
        """生成随机数图片流"""
        wait_time = self._random_wait_time() if not wait_time else wait_time
        return self.generate(self._generate_meter, wait_time)

    def clock(self) -> Iterable:
        """生成时钟图片流"""
        return self.generate(self._generate_clock, lambda: CLOCK_FRAME_INTERVAL_MS)
