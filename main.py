"""
程序入口
"""

import sys
from PyQt5.QtWidgets import QApplication

from main_window import Divergence
from constants import TYPE_METER


def main():
    """启动应用并根据时间设置初始状态"""
    app = QApplication(sys.argv)
    
    # 设置应用程序属性,允许在没有窗口时继续运行
    app.setQuitOnLastWindowClosed(False)
    
    # 创建主窗口
    main_window = Divergence()
    
    # 根据当前时间决定初始显示状态
    if main_window.is_in_display_window():
        # 在显示窗口内,自动切换到 meter 模式
        main_window.type_ = TYPE_METER
        main_window.worker.set_type(main_window.type_)
        main_window.show()
        main_window.was_visible = True
    else:
        # 不在显示窗口内,隐藏窗口
        main_window.hide()
        main_window.was_visible = False
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
