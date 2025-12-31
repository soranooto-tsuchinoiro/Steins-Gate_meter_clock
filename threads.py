"""
线程模块

图片生成线程，在后台异步生成显示内容
"""

from PyQt5.QtCore import QThread, pyqtSignal

from constants import TYPE_CLOCK
from image_utils import ImageGenerator


class ImageThread(QThread):
    """图片生成线程
    
    在独立线程中生成时钟或世界线图片，避免阻塞UI主线程
    生成的图片通过信号发送到主窗口进行显示
    """

    # 信号：发送生成的图片数据 (原始字节, 宽度, 高度)
    change_pic = pyqtSignal(bytes, int, int)

    def __init__(self, type_, config=None):
        """初始化图片生成线程
        
        Args:
            type_ (str): 显示类型，TYPE_CLOCK 或 TYPE_METER
            config (ConfigManager, optional): 配置管理器
        """
        super().__init__()
        self.type_ = type_
        self.last = type_
        self.gen = ImageGenerator(config)

    # ========================================================================
    # 公共方法 - 参数设置
    # ========================================================================

    def set_type(self, type_):
        """设置显示类型
        
        Args:
            type_ (str): 显示类型，TYPE_CLOCK 或 TYPE_METER
        """
        self.type_ = type_

    def set_duration(self, duration):
        """设置世界线显示持续时间
        
        Args:
            duration (int): 持续时间（毫秒）
        """
        self.gen.duration = duration

    # ========================================================================
    # 线程主方法
    # ========================================================================

    def run(self):
        """线程主循环
        
        根据当前显示类型生成相应的图片序列
        将图片转换为RGBA格式的原始字节数据后发送信号
        """
        while True:
            # 根据类型选择生成器
            generator = self.gen.clock if self.type_ == TYPE_CLOCK else self.gen.meter
            
            for pic in generator():
                # 检查类型是否改变，如果改变则切换生成器
                if self.last != self.type_:
                    self.last = self.type_
                    break
                
                # 转换为RGBA格式并提取原始字节数据
                rgba = pic.convert("RGBA")
                w, h = rgba.size
                raw = rgba.tobytes()
                
                # 发送图片数据信号
                self.change_pic.emit(raw, w, h)
