# Divergence Meter Clock

一个基于《命运石之门》(Steins;Gate)的世界线变动率探测器桌面应用程序。该应用可以在桌面上显示数字时钟或模拟世界线变动的随机数字，支持自动报时和手动触发功能。代码基本都是AI写的，不太会python。

## 项目介绍

Divergence Meter Clock 是一款致敬《命运石之门》的桌面小工具，它可以：

- **当前时间显示**：以辉光管风格显示当前时间（HH.MM.SS）
- **随机世界线**：模拟世界线变动率探测器，显示来自不同吸引力场域(α、β、Steins Gate等)的世界线数值
- **自动报时**：仅在在整点和半点前后自动弹出显示
- **系统托盘**：最小化到系统托盘，支持常显模式和报时模式切换

## 环境依赖

### 系统要求
- 操作系统：Windows
- Python版本：Python 3.12.10+

### Python依赖库
```
Pillow==10.2.0
PyQt5==5.15.10
```

## 安装和运行指南

### 1. 克隆或下载项目
```bash
git clone https://github.com/soranooto-tsuchinoiro/Steins-Gate_meter_clock.git
cd divergence-meter-clock
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

或手动安装：
```bash
pip install PyQt5 Pillow
```

### 3. 准备资源文件
确保项目根目录下存在 `img` 文件夹，其中包含以下数字图片文件：
- `0.jpg` 到 `9.jpg`（数字0-9的尼克西管样式图片）
- `.jpg`（小数点图片）
- `null.jpg`（空白分隔符图片）

可选：在 `assets` 文件夹中放置 `logo.ico` 作为系统托盘图标。

### 4. 运行程序
```bash
python main.py
```

## 目录结构描述

```
divergence-meter-clock/
├── main.py                 # 程序入口，初始化应用程序
├── main_window.py          # 主窗口类，控制显示逻辑和用户交互
├── constants.py            # 常量定义（显示模式、世界线数值、UI参数等）
├── image_utils.py          # 图片处理工具类，生成时钟和世界线图片
├── threads.py              # 图片生成线程，异步生成显示内容
├── time_manager.py         # 时间管理器，控制自动显示时间窗口
├── tray_icon.py            # 系统托盘图标管理器
├── ui_components.py        # UI基础组件（无边框窗口等）
├── img/                    # 数字图片资源文件夹
│   ├── 0.jpg - 9.jpg      # 数字0-9的尼克西管图片
│   ├── ..jpg              # 小数点图片
│   └── null.jpg           # 空白分隔符图片
├── assets/                 # 可选资源文件夹
│   └── logo.ico           # 系统托盘图标（可选）
├── DivergenceMeter.spec  # pyinstaller exe打包配置
├── bulid.py  # 打包脚本
└── README.md              # 项目说明文档
```

## 使用说明

### 自动报时模式（默认）

程序启动后会自动在以下时间显示：
- **整点报时**：每小时的 `X:59:50` 至 `X:00:10`（共20秒）
- **半点报时**：每小时的 `X:29:50` 至 `X:30:10`（共20秒）

如果启用了"报时前世界线变动"选项，程序会在 `X:59:50` 和 `X:29:50` 时先显示3秒的世界线变动动画。

### 手动控制

#### 系统托盘菜单
右键点击系统托盘图标可以访问以下选项：
- **切换常显模式/切换报时模式**：在常显和自动报时模式之间切换
- **报时前世界线变动**：勾选后，报时前会先显示世界线变动动画
- **退出**：关闭应用程序

#### 窗口交互
- **左键拖动**：移动窗口位置
- **右键点击**：手动触发世界线变动模式（显示3秒随机数字）
- **双击**：切换最大化/正常大小
- **拖动右下角**：调整窗口大小

### 配置选项

在 `constants.py` 中可以自定义以下参数：

```python
# UI尺寸配置（相对屏幕百分比）
LABEL_WIDTH_PCT = 0.30          # 窗口宽度占屏幕30%
LABEL_HEIGHT_PCT = 0.20         # 窗口高度占屏幕20%
TOP_OFFSET_PCT = 0.05           # 窗口距离屏幕顶部5%

# 显示时长配置
METER_FLASH_DURATION_MS = 3000  # 世界线模式持续3秒
CLOCK_FRAME_INTERVAL_MS = 500   # 时钟刷新间隔500毫秒

# 功能开关
TRIGGER_METER_BEFORE_ANNOUNCE = True  # 报时前是否先触发世界线变动
SHOW_WITHOUT_ACTIVATING = True        # 显示时不抢占焦点
```

### 世界线说明

程序内置了《命运石之门》中的多个吸引力场域世界线：
- **α世界线**
- **β世界线**
- **Steins;Gate世界线**
- **R世界线**
- **χ世界线**
- **γ世界线**
- **δ世界线**
- **ε世界线**

在世界线模式下，程序会从这些预定义的数值中随机选择并显示。

## 版本更新摘要

### v1.0.0（当前版本）
- ✨ 实现时钟模式和世界线模式双重显示
- ✨ 自动整点/半点报时功能
- ✨ 系统托盘集成，支持后台运行
- ✨ 无边框窗口，支持拖动、缩放和置顶
- ✨ 可配置的报时前世界线变动提示
- ✨ 常显模式和报时模式切换
- 🎨 辉光管管风格的视觉效果
- ⚡ 优化图片渲染性能，使用原始RGBA数据传输

## 常见问题解答

### Q1: 程序启动后看不到窗口？
**A:** 这是正常现象。在报时模式下，程序只在整点和半点前后自动显示。您可以：
- 等待下一个报时时间（如14:59:50或15:29:50）
- 右键点击系统托盘图标，选择"切换常显模式"以持续显示

### Q2: 如何自定义窗口大小和位置？
**A:** 有两种方法：
1. 在窗口显示时，左键拖动可移动位置，拖动右下角可调整大小
2. 修改 `constants.py` 中的 `LABEL_WIDTH_PCT`、`LABEL_HEIGHT_PCT` 和 `TOP_OFFSET_PCT` 参数

### Q3: 数字图片显示不正常或缺失？
**A:** 请确保 `img` 文件夹包含所有必需的图片文件（0.jpg到9.jpg、.jpg、null.jpg）。图片格式应为JPG，且尺寸应保持一致。

### Q4: 如何修改报时时间？
**A:** 编辑 `time_manager.py` 中的 `is_in_display_window()` 和 `should_trigger_meter()` 方法，可以自定义报时的时间窗口。

### Q5: 程序占用CPU较高怎么办？
**A:** 可以调整以下参数来降低资源占用：
- 增加 `MAIN_TIMER_INTERVAL_MS`（主定时器间隔）
- 增加 `CLOCK_FRAME_INTERVAL_MS`（时钟刷新间隔）
- 在不需要显示时切换到报时模式

### Q6: 如何添加自定义的世界线数值？
**A:** 在 `constants.py` 中找到世界线定义部分，按照相同格式添加自定义数值元组，然后将其添加到 `ATTRACTOR_FIELD` 集合中。

### Q7: 窗口总是显示在最前面，影响其他操作？
**A:** 这是设计特性（类似于真实的桌面小工具）。如果需要临时隐藏，可以按任意键或右键托盘图标选择隐藏。若要永久改变此行为，需修改 `ui_components.py` 中的 `Qt.WindowStaysOnTopHint` 标志。

### Q8: 程序能在macOS/Linux上运行吗？
**A:** 可以。程序使用PyQt5开发，支持跨平台运行。但系统托盘图标在不同平台上的显示效果可能略有差异。

---

## 致谢

本项目灵感来源于《命运石之门》(Steins;Gate)及其世界线变动率探测器的概念。

灵感与参考项目：
[mikusa](https://www.himiku.com/tools/steinsgate/)

[obgnail/divergence_meter_clock: 命运石之门同款世界线变动率探测仪](https://github.com/obgnail/divergence_meter_clock)

[Asterecho/Nixie: 西梅时钟+辉光管时钟](https://github.com/Asterecho/Nixie)

**El Psy Kongroo.**