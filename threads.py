"""
线程相关类
"""

from PyQt5.QtCore import QThread, pyqtSignal

from constants import TYPE_CLOCK
from image_utils import ImageGenerator


class ImageThread(QThread):
    # 图片生成线程

    change_pic = pyqtSignal(bytes, int, int)

    def __init__(self, type_, config=None):
        super().__init__()
        self.type_ = type_
        self.last = type_
        self.gen = ImageGenerator(config)

    def set_type(self, type_):
        self.type_ = type_

    def set_duration(self, duration):
        self.gen.duration = duration

    def run(self):
        while True:
            generator = self.gen.clock if self.type_ == TYPE_CLOCK else self.gen.meter
            for pic in generator():
                if self.last != self.type_:
                    self.last = self.type_
                    break
                rgba = pic.convert("RGBA")
                w, h = rgba.size
                raw = rgba.tobytes()
                self.change_pic.emit(raw, w, h)
