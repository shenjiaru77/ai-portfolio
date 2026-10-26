# -*- coding: utf-8 -*-
"""
W6 双引擎封装：LocalEngine（本地 Ollama）+ APIEngine（云端 MiniMax）+ LLM 统一入口

用法：
    from llm import LLM
    print(LLM().ask("给《愚公移山》出一道HSK4阅读题", prefer="local"))
    print(LLM().ask("设计一份完整教案", prefer="api"))

设计原则：业务代码只认 llm.ask()，换引擎只改一个参数。
"""
import os
import re
import sys

import requests
import openai
from dotenv import load_dotenv

# 加载仓库根目录的 .env（本文件位于 week06_双引擎/）
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT, ".env"))


class LocalEngine:
    """本地引擎：直接 http 调 Ollama 的 /api/chat，不依赖 SDK 版本。"""

    def __init__(self, model=None):
        # 模型名不写死：换 4b 只改环境变量 LOCAL_MODEL
        self.model = model or os.getenv("LOCAL_MODEL", "qwen2.5:0.5b")
        # 地址也可配：默认本机 Ollama；测试/换机器时改 OLLAMA_HOST
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")

    def ask(self, prompt, temperature=0.7, max_tokens=800):
        session = requests.Session()
        session.trust_env = False  # 机房/校园网代理会把 localhost 也送去代理
        r = session.post(
            self.host + "/api/chat",
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "options": {"temperature": temperature, "num_predict": max_tokens},
                "stream": False,
            },
            timeout=60,  # 首次装载模型可能要 30 秒，不设超时会永久卡住
        )
        r.raise_for_status()  # 模型名打错返回 404，让错误当场暴露
        return r.json()["message"]["content"]


class APIEngine:
    """云端引擎：MiniMax（OpenAI 兼容接口）。

    客户端按需创建——没配密钥时不能连纯本地模式都进不去。
    """

    BASE_URL = "https://www.minimax.cn/v1"
    MODEL = "MiniMax-M2.7"

    def __init__(self):
        self.client = None  # 先不建客户端！

    def _ensure_client(self):
        if self.client is None:
            key = os.getenv("MINIMAX_API_KEY", "").strip()
            if not key or key.startswith("sk-xxxx"):
                raise RuntimeError("未配置有效的 MINIMAX_API_KEY")
            self.client = openai.OpenAI(base_url=self.BASE_URL, api_key=key)

    def ask(self, prompt, temperature=0.7, max_tokens=800):
        self._ensure_client()  # 第一次真调用才建客户端
        r = self.client.chat.completions.create(
            model=self.MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = r.choices[0].message.content
        # MiniMax 会带 <think>...</think> 思考标签，去掉只留回答
        return re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()


class LLM:
    """统一入口：ask(prompt, prefer='local'|'api')，失败自动切换到另一边。"""

    def __init__(self, local_model=None):
        self.local = LocalEngine(local_model)
        self.api = APIEngine()

    def ask(self, prompt, prefer="local", **kw):
        # prefer='local' → 先本地后云端；prefer='api' → 先云端后本地
        first, second = (self.local, self.api) if prefer == "local" else (self.api, self.local)
        try:
            return first.ask(prompt, **kw)
        except Exception as e:
            # 三纪律：不吞异常、打印切换原因、返回真实结果
            print("[首选引擎失败，自动切换] %s: %s" % (type(e).__name__, e))
            return second.ask(prompt, **kw)


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "给《愚公移山》出一道HSK4阅读题"
    prefer = os.getenv("PREFER", "local")
    ans = LLM().ask(q, prefer=prefer)
    print("\n--- 回答 ---")
    print(ans)
