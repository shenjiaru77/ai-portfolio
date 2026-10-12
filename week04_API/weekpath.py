"""
weekpath.py — 路径约定工具（week04_API 专用）
确保脚本从任意目录运行都能找到：
  - .env 配置文件
  - chat_log.txt（统一写到仓库根目录）
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 仓库根目录（week04_API 的父目录）
_HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ENV_FILE = os.path.join(_HERE, ".env")

# 自动加载 .env 文件（Windows 下 os.getenv() 读不到 .env，必须显式加载）
load_dotenv(_ENV_FILE)


def root_path(filename):
    """返回仓库根目录下指定文件的绝对路径。"""
    return os.path.join(_HERE, filename)
