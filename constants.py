"""
常量定义模块
"""

# 显示模式，clock 时钟模式，meter 世界线
TYPE_CLOCK = "clock"
TYPE_METER = "meter"

# UI 大小/位置相关（百分比，相对于可用屏幕尺寸）
# `LABEL_WIDTH_PCT` / `LABEL_HEIGHT_PCT`：显示区（QLabel）相对于屏幕宽/高的比例
# `TOP_OFFSET_PCT`：窗口顶部距离屏幕顶部的比例（例如 0.1 表示 10%）
LABEL_WIDTH_PCT = 0.30
LABEL_HEIGHT_PCT = 0.20
TOP_OFFSET_PCT = 0.05

# 是否在窗口显示时不抢占焦点（True 将尝试不激活窗口）
SHOW_WITHOUT_ACTIVATING = True

# 主定时器轮询时间（毫秒），用于检测时间和显示/隐藏逻辑
MAIN_TIMER_INTERVAL_MS = 100

# 随机表盘（meter）闪动持续时间（毫秒）
METER_FLASH_DURATION_MS = 3000

# 时钟帧更新间隔（毫秒），控制时钟图片生成频率
CLOCK_FRAME_INTERVAL_MS = 500

# 存放数字图片的目录名（相对于代码文件夹）
IMAGE_DIR_NAME = "img"
# 期望在资源目录中存在的数字/小数点文件名键集合
IMAGE_DIGITS = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "null")

# ImageGenerator 中随机等待的短/长时长（毫秒），用于 meter 模式的节奏控制
RANDOM_WAIT_SHORT_MS = 60
RANDOM_WAIT_LONG_MS = 2000

# 托盘图标的提示文本（tooltip）
TRAY_TOOLTIP = "Divergence Meter Clock"
# 托盘图标的尺寸（像素，正方形）
TRAY_ICON_SIZE = 64

# 报时前是否先触发 meter（世界线变动）
# True: 报时前先短时显示 meter；False: 不先触发 meter
TRIGGER_METER_BEFORE_ANNOUNCE = True

# α世界线
ATTRACTOR_FIELD_α = (
    "0.571082",
    "0.571024",
    "0.571015",
    "0.523307",
    "0.523299",
    "0.509736",
    "0.456923",
    "0.456914",
    "0.456903",
    "0.409420",
    "0.409431",
    "0.337187",
    "0.337161",
    "0.334581",
    "0.337337",
    "0.328403",
    "0.000000",
)
# β世界线
ATTRACTOR_FIELD_β = (
    "1.382733",
    "1.143688",
    "1.130426",
    "1.130238",
    "1.130205",
    "1.130206",
    "1.130207",
    "1.130208",
    "1.130209",
    "1.130210",
    "1.130211",
    "1.130212",
    "1.129954",
    "1.129848",
    "1.123581",
    "1.097302",
    "1.081163",
    "1.064756",
    "1.064750",
    "1.055821",
    "1.053649",
)
# Steins;Gate 世界线
ATTRACTOR_FIELD_STEINS_GATE = ("1.048596",)
# R 世界线
ATTRACTOR_FIELD_R = ("1.048595", "1.048597")
# X 世界线
ATTRACTOR_FIELD_X = ("1.048599", "1.049326", "1.048728")
# γ 世界线
ATTRACTOR_FIELD_γ = ("2.615074",)
# δ 世界线
ATTRACTOR_FIELD_δ = (
    "3.019430",
    "3.030493",
    "3.182879",
    "3.130238",
    "3.372329",
    "3.386019",
    "3.406288",
    "3.600104",
    "3.667293",
)
# ε 世界线
ATTRACTOR_FIELD_ε = (
    "4.456441",
    "4.493624",
    "4.530805",
    "4.456442",
    "4.493623",
    "4.530806",
    "4.389117",
)
# Ω 世界线（不使用）
ATTRACTOR_FIELD_Ω = ("-0.275349", "-0.195284")
# 世界线集合
ATTRACTOR_FIELD = (
    ATTRACTOR_FIELD_α,
    ATTRACTOR_FIELD_β,
    ATTRACTOR_FIELD_STEINS_GATE,
    ATTRACTOR_FIELD_R,
    ATTRACTOR_FIELD_X,
    ATTRACTOR_FIELD_γ,
    ATTRACTOR_FIELD_δ,
    ATTRACTOR_FIELD_ε,
)
