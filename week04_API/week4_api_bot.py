# W4 命令行学科问答机器人（API 版）
# 运行：python week4_api_bot.py "你的问题"
# 学科：汉语国际教育

import os
import sys
from pathlib import Path

# 动态添加项目根目录到 Python 路径，确保能找到 weekpath 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import weekpath  # 统一加载 .env + 解析路径

import openai

# ==================== 配置区 ====================
# MiniMax 配置
BASE_URL = "https://www.minimax.cn/v1"
MODEL = "MiniMax-M2.7"
# ==============================================

_client = None


def get_client():
    """按需创建客户端：没配密钥时报错能落到 __main__ 里给人话提示，
    而不是在 import 阶段抛一串看不懂的 OpenAIError。
    """
    global _client
    if _client is None:
        key = os.getenv("MINIMAX_API_KEY")
        if not key:
            raise RuntimeError("未配置 MINIMAX_API_KEY")
        _client = openai.OpenAI(base_url=BASE_URL, api_key=key)
    return _client


def ask(question, temperature=0.7, max_tokens=800):
    """调用 AI API 获取回答"""
    r = get_client().chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    content = r.choices[0].message.content

    # MiniMax 模型会输出 <think>...</think> 思考标签，去掉思考过程只留回答
    import re
    content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()

    return content


if __name__ == "__main__":
    # 检查密钥是否配置
    if not os.getenv("MINIMAX_API_KEY"):
        print("错误：未设置 MINIMAX_API_KEY。")
        print("  处理：复制 .env.example 为 .env 并填入密钥，重启终端后重试。")
        sys.exit(1)

    # 获取命令行问题，默认问题
    q = " ".join(sys.argv[1:]) or "把字句的教学难点有哪些"

    try:
        ans = ask(q)  # 只调用一次：每调一次都计费
    except openai.APITimeoutError:
        print("错误：请求超时，请检查网络或调大 timeout。")
        sys.exit(1)

    print(ans)  # 终端打印

    # 追加对话日志到代码包根目录
    log_path = weekpath.root_path("chat_log.txt")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"Q: {q}\nA: {ans}\n\n")

    print(f"\n[日志已追加到: {log_path}]")
