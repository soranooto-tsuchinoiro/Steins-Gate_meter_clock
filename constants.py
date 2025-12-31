"""
常量定义模块
"""

# 显示模式，clock 时钟模式，meter 世界线
TYPE_CLOCK = "clock"
TYPE_METER = "meter"


# 随机表盘（meter）闪动持续时间（毫秒）
def get_meter_flash_duration_ms(config):
    return config.get_flash_duration_ms()


# ImageGenerator 中随机等待的短/长时长（毫秒），用于 meter 模式的节奏控制
def get_random_wait_short_ms(config):
    return config.get_random_wait_short_ms()


# 显示时间区间（分钟列表）
def get_display_minutes(config):
    return config.get_display_minutes()


# 是否在窗口显示时不抢占焦点（True 将尝试不激活窗口）
SHOW_WITHOUT_ACTIVATING = True

# 主定时器轮询时间（毫秒），用于检测时间和显示/隐藏逻辑
MAIN_TIMER_INTERVAL_MS = 100

# 时钟帧更新间隔（毫秒），控制时钟图片生成频率
CLOCK_FRAME_INTERVAL_MS = 500

# 存放数字图片的目录名（相对于代码文件夹）
IMAGE_DIR_NAME = "img"
# 期望在资源目录中存在的数字/小数点文件名键集合
IMAGE_DIGITS = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "null")

# 托盘图标的提示文本（tooltip）
TRAY_TOOLTIP = "Divergence Meter Clock"
# 托盘图标的尺寸（像素，正方形）
TRAY_ICON_SIZE = 64

# 报时前是否先触发 meter（世界线变动）
# True: 报时前先短时显示 meter；False: 不先触发 meter
TRIGGER_METER_BEFORE_ANNOUNCE = True

# α 世界线
ATTRACTOR_FIELD_α = (
    "0.934587",
    "0.815524",
    "0.751354",
    "0.615483",
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
# β 世界线
ATTRACTOR_FIELD_β = (
    "1.818520",
    "1.467093",
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
# R 世界线
ATTRACTOR_FIELD_R = ("1.048595", "1.048597")
# χ 世界线 "Steins;Gate 世界线 1.048596"
ATTRACTOR_FIELD_χ = (
    "1.048264",
    "1.048596",
    "1.048599",
    "1.048728",
    "1.049326",
)
# γ 世界线
ATTRACTOR_FIELD_γ = (
    "2.224529",
    "2.615074",
)
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
    ATTRACTOR_FIELD_R,
    ATTRACTOR_FIELD_χ,
    ATTRACTOR_FIELD_γ,
    ATTRACTOR_FIELD_δ,
    ATTRACTOR_FIELD_ε,
)
