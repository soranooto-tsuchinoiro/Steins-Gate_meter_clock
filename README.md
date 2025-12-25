# Divergence Meter 时钟应用

## 📁 项目结构

```
divergence_meter/
├── main.py                 # 程序入口
├── constants.py           # 常量定义
├── image_utils.py         # 图片处理工具
├── ui_components.py       # UI组件基类
├── threads.py             # 线程管理
├── tray_icon.py          # 系统托盘图标
├── time_manager.py       # 时间管理器
├── main_window.py        # 主窗口类
├── README.md             # 说明文档
└── img/                  # 图片资源目录
    ├── 0.png
    ├── 1.png
    ├── 2.png
    ├── 3.png
    ├── 4.png
    ├── 5.png
    ├── 6.png
    ├── 7.png
    ├── 8.png
    ├── 9.png
    └── ..png
```

## 🔧 模块说明

### 1. constants.py
定义应用程序常量
- `TYPE_CLOCK`: 时钟模式
- `TYPE_METER`: 随机数表盘模式

### 2. image_utils.py
图片处理相关功能
- `ImageOptionMixin`: 图片操作混入类(水平拼接、添加边框)
- `ImageGenerator`: 图片生成器(生成时钟和随机数图片)

### 3. ui_components.py
UI组件基类
- `FramelessWindow`: 无边框可拖拽窗口基类,支持拖动和缩放

### 4. threads.py
线程管理
- `ImageThread`: 图片生成线程,持续生成时钟或随机数图片

### 5. tray_icon.py
系统托盘功能
- `TrayIconManager`: 系统托盘图标管理器,提供菜单和图标

### 6. time_manager.py
时间管理功能
- `TimeManager`: 时间检查器,判断是否在显示窗口内

### 7. main_window.py
主窗口类
- `Divergence`: 主窗口,整合所有功能模块

### 8. main.py
程序入口
- `main()`: 应用程序启动函数

## 📦 依赖项

```bash
pip install PyQt5 Pillow
```

## 🚀 运行方式

1. 确保所有文件在同一目录下
2. 确保 `img/` 文件夹包含 0-9 和点的图片文件
3. 运行主程序:

```bash
python main.py
```

## ✨ 功能特性

### 自动显示/隐藏
- **整点**: X:59:50 - X:00:10 (显示20秒)
- **半点**: X:29:50 - X:30:10 (显示20秒)

### 显示逻辑
1. 距离整点/半点10秒时自动触发
2. 先显示随机数(3秒)
3. 再切换到时钟显示
4. 超出时间窗口后自动隐藏

### 交互功能
- **右键**: 手动触发随机数显示
- **双击**: 最大化/还原窗口
- **任意键**: 隐藏窗口
- **左键拖动**: 移动窗口
- **右下角拖动**: 调整窗口大小

### 系统托盘
- **单击/双击**: 显示/隐藏窗口
- **显示菜单**: 手动显示窗口
- **隐藏菜单**: 手动隐藏窗口
- **自动隐藏模式**: 切换自动显示/隐藏功能
- **退出**: 关闭应用程序

## 🎯 使用建议

1. **首次运行**: 程序会根据当前时间决定是否显示
2. **系统托盘**: 关闭窗口后程序仍在后台运行,可通过托盘图标控制
3. **自动模式**: 默认开启,可通过托盘菜单关闭
4. **手动控制**: 关闭自动模式后可完全手动控制窗口显示

## 📝 注意事项

- 确保 `img/` 目录包含所有必需的图片文件(0-9.png 和 ..png)
- 程序需要系统托盘支持
- 建议在支持透明窗口的系统上运行以获得最佳效果

## 🔄 模块依赖关系

```
main.py
  └── main_window.py
        ├── constants.py
        ├── ui_components.py
        ├── threads.py
        │     ├── image_utils.py
        │     └── constants.py
        ├── tray_icon.py
        └── time_manager.py
```

## 📄 许可证

请根据您的需求添加相应的许可证信息。
