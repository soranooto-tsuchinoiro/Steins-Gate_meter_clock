"""
线程相关类
"""

from PyQt5.QtCore import QThread, pyqtSignal

from image_utils import ImageGenerator
from constants import TYPE_CLOCK


class ImageThread(QThread):
    """图片生成线程"""

    # emit: raw_bytes, width, height
    change_pic = pyqtSignal(bytes, int, int)

    def __init__(self, type_):
        """初始化图片生成线程"""
        super().__init__()
        self.type_ = type_
        self.last = type_
        self.gen = ImageGenerator()

    def set_type(self, type_):
        """更新当前显示类型"""
        self.type_ = type_

    def run(self):
        """循环生成图片并发信号"""
        while True:
            generator = self.gen.clock if self.type_ == TYPE_CLOCK else self.gen.meter
            for pic in generator():
                if self.last != self.type_:
                    self.last = self.type_
                    break

                # Ensure RGBA bytes
                rgba = pic.convert("RGBA")
                w, h = rgba.size
                raw = rgba.tobytes()
                self.change_pic.emit(raw, w, h)
