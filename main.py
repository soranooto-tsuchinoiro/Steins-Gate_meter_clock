"""
程序入口模块

应用程序的启动入口，负责初始化Qt应用和主窗口
"""

import sys

from PyQt5.QtWidgets import QApplication

from constants import TYPE_METER
from main_window import Divergence


def main():
    """启动应用程序
    
    初始化Qt应用，创建主窗口，并根据当前时间决定初始显示状态
    """
    # 创建Qt应用实例
    app = QApplication(sys.argv)

    # 允许在没有窗口时继续运行（托盘模式）
    app.setQuitOnLastWindowClosed(False)

    # 创建主窗口
    main_window = Divergence()

    # 根据当前时间决定初始状态
    if main_window.is_in_display_window():
        # 在显示窗口内：自动切换到世界线模式并显示
        main_window.type_ = TYPE_METER
        main_window.worker.set_type(main_window.type_)
        main_window.show()
    else:
        # 不在显示窗口内：隐藏窗口，仅显示托盘图标
        main_window.hide()

    # 启动应用程序事件循环
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
