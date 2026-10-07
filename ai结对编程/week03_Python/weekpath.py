"""
weekpath.py — 路径约定工具
确保 vocab_tool.py 从任意目录运行都能找到：
  - data/生词表.csv（随脚本包的数据文件）
  - 练习.txt 等产物（统一写到代码包根目录的上一级，即仓库根目录）
用法：照抄即可，无需深究原理。
"""
import os

# 本文件所在目录，即 week03_Python/
_HERE = os.path.dirname(os.path.abspath(__file__))

# 代码包根目录（week03_Python 的上一级，即仓库根目录）
_ROOT = os.path.dirname(_HERE)

# data/ 目录（与 weekpath.py 同级的 data/ 文件夹）
_DATA_DIR = os.path.join(_HERE, "data")


def data_path(filename):
    """
    返回 data/ 目录下指定文件的绝对路径。
    示例：weekpath.data_path("生词表.csv")
    """
    return os.path.join(_DATA_DIR, filename)


def root_path(filename):
    """
    返回仓库根目录下指定文件的绝对路径（week03_Python 的上一级）。
    脚本运行时从 week03_Python/ 执行则打印为 ../<filename>
    示例：weekpath.root_path("练习.txt")
    """
    return os.path.join(_ROOT, filename)
