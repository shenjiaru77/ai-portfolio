# -*- coding: utf-8 -*-
"""三路径实测小工具：打印测试条件、耗时、回答开头，方便把证据贴进 week06_test_log.md。

用法：
    python run_test.py "问题" local                # 默认 max_tokens=800
    python run_test.py "问题" local 20             # 作业2：调小 max_tokens 观察截断
    python run_test.py "问题" api 800
"""
import sys
import time

from llm import LLM


def main():
    prompt = sys.argv[1] if len(sys.argv) > 1 else "给《愚公移山》出一道HSK4阅读题"
    prefer = sys.argv[2] if len(sys.argv) > 2 else "local"
    max_tokens = int(sys.argv[3]) if len(sys.argv) > 3 else 800

    print("=" * 60)
    print("[测试条件] prefer=%s | max_tokens=%d | 问题=%s" % (prefer, max_tokens, prompt))
    print("=" * 60)

    t0 = time.time()
    try:
        ans = LLM().ask(prompt, prefer=prefer, max_tokens=max_tokens)
        cost = time.time() - t0
        head = ans.replace("\n", " ")[:300]
        print("\n[耗时] %.2f 秒" % cost)
        print("[回答前300字] %s" % head)
        print("\n[结果] 成功")
    except Exception as e:
        cost = time.time() - t0
        print("\n[耗时] %.2f 秒" % cost)
        print("[结果] 失败：%s: %s" % (type(e).__name__, e))


if __name__ == "__main__":
    main()
