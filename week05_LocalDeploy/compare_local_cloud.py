# -*- coding: utf-8 -*-
"""W5 对比脚本：同一组学科问题分别问「本地模型」和「云端 API」，打印可粘贴的 Markdown 表。

用法（在仓库根目录或本文件夹都能跑）：
    python week05_LocalDeploy/compare_local_cloud.py          # 默认 max_tokens=1000
    python week05_LocalDeploy/compare_local_cloud.py 2500     # 推理题给更大额度

前提：
    1) Ollama 已启动且已 pull 模型（默认 qwen2.5:0.5b）
    2) 仓库根目录 .env 里配好了 MINIMAX_API_KEY（没有也能跑，云端列会标「失败」）

注意：MiniMax-M2.7 是推理模型，会先输出 <think> 思考内容；
      max_tokens=300 时会把额度全花在思考上、回答为空，所以默认给 1000。
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import weekpath  # noqa: E402,F401  注册各周目录进 sys.path
from llm import LLM  # noqa: E402

QUESTIONS = [
    "给《愚公移山》出3道HSK4阅读题",
    "解释「把字句」的构成条件",
    "把教案要点扩成完整教案",
    "HSK4级对词汇量的要求是多少",
    "给中级汉语作文写三段式评语",
]

LOCAL_MODEL = os.getenv("LOCAL_MODEL", "qwen2.5:0.5b")
# 推理型云端模型会先花 token 思考；给太小会拿到空回答（实测 300 不够，1000 起步）
MAX_TOKENS = int(sys.argv[1]) if len(sys.argv) > 1 else 1000


def run_one(engine, prompt):
    """直接调某个引擎（不走 LLM 的回退），返回 (耗时, 是否成功, 回答前 80 字/错误信息)。"""
    t0 = time.time()
    try:
        ans = engine.ask(prompt, max_tokens=MAX_TOKENS)
        return time.time() - t0, True, ans.replace("\n", " ")[:80]
    except Exception as e:
        return time.time() - t0, False, "%s: %s" % (type(e).__name__, e)


def main():
    llm = LLM()
    print("本地模型：%s" % LOCAL_MODEL)
    print("提示：这里直接调两个引擎本身，不走 LLM 的自动回退，")
    print("      否则云端失败会回退到本地，对比表就失真了。")
    print("=" * 80)

    rows = []
    for i, q in enumerate(QUESTIONS, 1):
        print("[%d/5] %s" % (i, q))
        dt_local, ok_local, txt_local = run_one(llm.local, q)
        print("      本地 %.2fs %s" % (dt_local, "成功" if ok_local else "失败"))
        dt_api, ok_api, txt_api = run_one(llm.api, q)
        print("      云端 %.2fs %s" % (dt_api, "成功" if ok_api else "失败"))
        rows.append((i, q, dt_local, ok_local, txt_local, dt_api, ok_api, txt_api))

    print("\n" + "=" * 80)
    print("| # | 学科问题 | 本地耗时 | 本地质量 | 云端耗时 | 云端质量 |")
    print("|---|----------|----------|----------|----------|----------|")
    for (i, q, dtl, okl, tl, dta, oka, ta) in rows:
        print("| %d | %s | %.2f s | %s | %.2f s | %s |" % (
            i, q, dtl,
            ("%s%s" % ("✅ " if okl else "❌ ", tl)),
            dta,
            ("%s%s" % ("✅ " if oka else "❌ ", ta)),
        ))


if __name__ == "__main__":
    main()
