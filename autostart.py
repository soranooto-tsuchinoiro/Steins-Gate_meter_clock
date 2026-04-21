"""
开机自启管理模块

通过 Windows 注册表实现开机自启功能的启用、禁用和路径修正。
"""

import sys

import winreg


# 注册表子键路径
REG_SUB_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"

# 开机自启注册项名称
REG_VALUE_NAME = "DivergenceMeterClock"


def _get_exe_path():
    """获取当前可执行文件的绝对路径

    Returns:
        str: 当前 exe 或 python 脚本的绝对路径
    """
    return sys.executable if getattr(sys, "frozen", False) else sys.argv[0]


def is_enabled():
    """检查是否已启用开机自启

    Returns:
        bool: 是否已启用
    """
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            REG_SUB_KEY,
            0,
            winreg.KEY_READ,
        )
        winreg.QueryValueEx(key, REG_VALUE_NAME)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False


def enable():
    """启用开机自启，将当前程序路径写入注册表"""
    exe_path = _get_exe_path()
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            REG_SUB_KEY,
            0,
            winreg.KEY_SET_VALUE,
        )
        winreg.SetValueEx(key, REG_VALUE_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
        winreg.CloseKey(key)
    except PermissionError:
        pass  # 权限不足时静默失败


def disable():
    """禁用开机自启，从注册表删除启动项"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            REG_SUB_KEY,
            0,
            winreg.KEY_SET_VALUE,
        )
        winreg.DeleteValue(key, REG_VALUE_NAME)
        winreg.CloseKey(key)
    except FileNotFoundError:
        pass  # 注册项已不存在时忽略


def get_registered_path():
    """获取注册表中记录的启动路径

    Returns:
        str or None: 注册表中的路径，如果未设置则返回 None
    """
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            REG_SUB_KEY,
            0,
            winreg.KEY_READ,
        )
        value, _ = winreg.QueryValueEx(key, REG_VALUE_NAME)
        winreg.CloseKey(key)
        # 移除可能存在的引号
        return value.strip('"')
    except FileNotFoundError:
        return None


def fix_path_if_needed():
    """检查并修正注册表中的路径（如果已启用但路径不同）

    如果开机自启已启用，但注册表中的路径与当前 exe 路径不一致，
    则用当前路径覆盖注册表中的旧路径。
    """
    if not is_enabled():
        return

    registered = get_registered_path()
    current = _get_exe_path()

    # 如果路径不一致，更新为当前路径
    if registered and registered != current:
        enable()
