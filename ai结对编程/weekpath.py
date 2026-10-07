"""
weekpath.py — 路径约定工具（与 vocab_tool.py 同目录）
确保脚本从任意目录运行都能找到：
  - data/生词表.csv（随脚本的数据文件）
  - 练习.txt 等产物（统一写到仓库根目录）
"""
import os

_HERE = os.path.dirname(os.path.abspath(__file__))   # 本文件所在目录（workspace 根目录）
_DATA_DIR = os.path.join(_HERE, "data")              # data/ 目录


def data_path(filename):
    """返回 data/ 目录下指定文件的绝对路径。"""
    return os.path.join(_DATA_DIR, filename)


def root_path(filename):
    """返回仓库根目录下指定文件的绝对路径（即本文件所在目录）。"""
    return os.path.join(_HERE, filename)
