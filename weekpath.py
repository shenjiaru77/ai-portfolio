"""
weekpath.py（仓库根目录）— 统一注册各周目录 + 加载 .env

用途：
  1. 集中加载根目录 .env（Windows 下 os.getenv() 读不到 .env，必须显式加载）
  2. 把各周目录注册进 sys.path，供跨周 import：W7/W8 里 `from llm import LLM` 找不到时，
     先 `import weekpath`（或 `from weekpath import *`）再 import llm。

与 week04_API/weekpath.py 的接口保持一致（load_dotenv + root_path），
所以 W4 的脚本从根目录 import 也不会坏。
"""
import os
import sys

from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.abspath(__file__))

# 加载仓库根目录的 .env
load_dotenv(os.path.join(ROOT, ".env"))


def root_path(filename):
    """返回仓库根目录下指定文件的绝对路径。"""
    return os.path.join(ROOT, filename)


# 固定三行：注册各周目录进 sys.path，跨周 import 才找得到
for _week in ("week01_仓库初始化", "week02_Prompt工程", "week03_AI结对编程",
              "week04_API", "week05_LocalDeploy", "week06_双引擎"):
    _p = os.path.join(ROOT, _week)
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)
