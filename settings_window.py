"""
设置对话框
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)


class SettingsDialog(QDialog):
    """设置对话框"""

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("设置参数")
        self.setStyleSheet("background-color: lightblue;")
        self.setModal(True)
        # 移除帮助按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        # 随机等待时间短
        self.random_wait_short_spin = QSpinBox()
        self.random_wait_short_spin.setRange(10, 1000)
        self.random_wait_short_spin.setValue(self.config.get_random_wait_short_ms())
        form_layout.addRow("闪动间隔时间 (ms):", self.random_wait_short_spin)

        # 闪动持续时间
        self.flash_duration_spin = QSpinBox()
        self.flash_duration_spin.setRange(1000, 20000)
        self.flash_duration_spin.setValue(self.config.get_flash_duration_ms())
        form_layout.addRow("闪动总持续时间 (ms):", self.flash_duration_spin)

        # 显示时间区间（分钟列表，如 0,30）
        self.display_minutes_edit = QLineEdit()
        display_minutes = self.config.get_display_minutes()
        self.display_minutes_edit.setText(",".join(map(str, display_minutes)))
        form_layout.addRow("报时时间节点 (分钟):", self.display_minutes_edit)

        layout.addLayout(form_layout)

        # 按钮
        button_layout = QHBoxLayout()
        save_button = QPushButton("完成")
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_settings(self):
        self.config.set_random_wait_short_ms(self.random_wait_short_spin.value())
        self.config.set_flash_duration_ms(self.flash_duration_spin.value())
        self.config.set_display_minutes(self.display_minutes_edit.text())
        # 解析显示时间区间
        try:
            display_minutes = [
                int(x.strip())
                for x in self.display_minutes_edit.text().split(",")
                if x.strip()
            ]
            self.config.set_display_minutes(display_minutes)
        except ValueError:
            pass  # 忽略无效输入
        self.config.save()
        self.accept()
