"""
设置对话框模块

提供用户可配置参数的设置界面
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
    """设置对话框
    
    允许用户配置以下参数：
    - 闪动间隔时间
    - 闪动总持续时间
    - 报时时间节点
    """

    def __init__(self, config, parent=None):
        """初始化设置对话框
        
        Args:
            config (ConfigManager): 配置管理器实例
            parent (QWidget, optional): 父窗口
        """
        super().__init__(parent)
        self.config = config
        
        # 初始化UI
        self._init_ui()
        self._create_widgets()
        self._create_layout()

    # ========================================================================
    # 私有方法 - UI初始化
    # ========================================================================

    def _init_ui(self):
        """初始化对话框基本属性"""
        self.setWindowTitle("设置参数")
        self.setStyleSheet("background-color: lightblue;")
        self.setModal(True)
        
        # 移除帮助按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def _create_widgets(self):
        """创建所有输入控件"""
        # 闪动间隔时间（毫秒）
        self.random_wait_short_spin = QSpinBox()
        self.random_wait_short_spin.setRange(10, 1000)
        self.random_wait_short_spin.setValue(self.config.get_random_wait_short_ms())

        # 闪动总持续时间（毫秒）
        self.flash_duration_spin = QSpinBox()
        self.flash_duration_spin.setRange(1000, 20000)
        self.flash_duration_spin.setValue(self.config.get_flash_duration_ms())

        # 报时时间节点（分钟列表，如 0,30）
        self.display_minutes_edit = QLineEdit()
        display_minutes = self.config.get_display_minutes()
        self.display_minutes_edit.setText(",".join(map(str, display_minutes)))

    def _create_layout(self):
        """创建对话框布局"""
        # 主布局
        main_layout = QVBoxLayout()

        # 表单布局
        form_layout = QFormLayout()
        form_layout.addRow("闪动间隔时间 (ms):", self.random_wait_short_spin)
        form_layout.addRow("闪动总持续时间 (ms):", self.flash_duration_spin)
        form_layout.addRow("报时时间节点 (分钟):", self.display_minutes_edit)
        main_layout.addLayout(form_layout)

        # 按钮布局
        button_layout = self._create_button_layout()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def _create_button_layout(self):
        """创建按钮布局
        
        Returns:
            QHBoxLayout: 按钮布局对象
        """
        button_layout = QHBoxLayout()
        
        # 完成按钮
        save_button = QPushButton("完成")
        save_button.clicked.connect(self.save_settings)
        
        # 取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        return button_layout

    # ========================================================================
    # 公共方法 - 设置保存
    # ========================================================================

    def save_settings(self):
        """保存设置并关闭对话框
        
        验证并保存所有配置项到配置管理器
        """
        # 保存闪动参数
        self.config.set_random_wait_short_ms(self.random_wait_short_spin.value())
        self.config.set_flash_duration_ms(self.flash_duration_spin.value())
        
        # 解析并保存显示时间节点
        self._save_display_minutes()
        
        # 持久化到磁盘
        self.config.save()
        
        # 关闭对话框
        self.accept()

    # ========================================================================
    # 私有方法 - 数据处理
    # ========================================================================

    def _save_display_minutes(self):
        """解析并保存显示时间节点
        
        从输入框中解析逗号分隔的分钟数列表
        """
        try:
            display_minutes = [
                int(x.strip())
                for x in self.display_minutes_edit.text().split(",")
                if x.strip()
            ]
            self.config.set_display_minutes(display_minutes)
        except ValueError:
            # 忽略无效输入，保持原有设置
            pass
