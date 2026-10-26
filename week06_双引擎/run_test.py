# -*- coding: utf-8 -*-
"""三路径实测小工具：打印测试条件、耗时、回答开头，方便把证据贴进 week06_test_log.md。

用法：
    python run_test.py "给《愚公移山》出一道HSK4阅读题" local
    python run_test.py "给《愚公移山》出一道HSK4阅读题" api
"""
import sys
import time

from llm import LLM


def main():
    prompt = sys.argv[1] if len(sys.argv) > 1 else "给《愚公移山》出一道HSK4阅读题"
    prefer = sys.argv[2] if len(sys.argv) > 2 else "local"

    print("=" * 60)
    print("[测试条件] prefer=%s | 问题=%s" % (prefer, prompt))
    print("=" * 60)

    t0 = time.time()
    try:
        ans = LLM().ask(prompt, prefer=prefer)
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
