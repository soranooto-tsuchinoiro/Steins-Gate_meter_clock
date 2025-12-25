# build.py
import os
import shutil
import subprocess
import sys


def clean_build_dirs():
    """清理构建目录"""
    dirs_to_remove = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除: {dir_name}")


def build_exe():
    """使用PyInstaller构建EXE"""
    cmd = [
        "pyinstaller",
        "--upx-dir",
        "D:/upx-5.0.2-win64"  # upx目录
        "--clean",
        "DivergenceMeter.spec",
    ]

    print("开始打包...")
    print("执行命令:", " ".join(cmd))

    try:
        subprocess.run(cmd, check=True)
        print("\n打包完成!")
        print(f"EXE文件位置: {os.path.join('dist', 'DivergenceMeter.exe')}")
        print(
            f"文件大小: {os.path.getsize(os.path.join('dist', 'DivergenceMeter.exe')) / 1024 / 1024:.2f} MB"
        )
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # 清理之前的构建
    clean_build_dirs()

    # 开始构建
    build_exe()
