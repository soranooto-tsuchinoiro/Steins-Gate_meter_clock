# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 数据文件配置
added_files = [
    ('img', 'img'),  # 将img目录添加到打包文件中
    ('assets/logo.ico', 'assets')  # 将logo.ico添加到assets目录
]

a = Analysis(
    ['main.py'],  # 主入口文件
    pathex=[],  # 搜索路径，可以根据需要添加
    binaries=[],  # 二进制文件（如DLL）
    datas=added_files,  # 数据文件
    hiddenimports=[],  # 隐藏导入（用于动态导入的模块）
    hookspath=[],  # hook文件路径
    hooksconfig={},  # hook配置
    runtime_hooks=[],  # 运行时hook
    excludes=[],  # 排除模块
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,  # 不打包为archive（设为True可调试）
)

# 创建PYZ
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 创建EXE配置
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DivergenceMeter',  # 程序名称
    debug=False,  # 调试模式
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 使用UPX压缩（需要安装UPX）
    console=False,  # 不显示控制台（与--windowed对应）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/logo.ico'],  # 程序图标
)