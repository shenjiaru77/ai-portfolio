# W6 双引擎封装：llm.py

> 业务代码只认 `llm.ask()`，本地/云端切换只改一个参数。

## 文件说明

| 文件 | 说明 |
|------|------|
| `llm.py` | 三个类：`LocalEngine`（本地 Ollama）、`APIEngine`（云端 MiniMax）、`LLM`（统一入口 + 双向回退 + 失败重试） |
| `run_test.py` | 三路径实测小工具，打印测试条件/耗时/回答，支持传 max_tokens |
| `week06_test_log.md` | 边界测试记录（5 组，四列）+ 200 字反思 |
| `homework_rag_prep.md` | 作业 3：RAG 预习，学科文本 + 「模型不知道具体数字怎么办」的思考 |

## 依赖安装

```powershell
pip install openai requests python-dotenv
```

## 快速使用

```python
from llm import LLM

print(LLM().ask("给《愚公移山》出一道HSK4阅读题", prefer="local"))
print(LLM().ask("设计一份完整教案", prefer="api"))
```

## 三路径实测

```powershell
cd week06_双引擎

# ① 正常本地（Ollama 运行中）
python run_test.py "给《愚公移山》出一道HSK4阅读题" local

# ② 关掉 Ollama 再跑（观察自动切换日志）
python run_test.py "给《愚公移山》出一道HSK4阅读题" local

# ③ prefer='api'
python run_test.py "给《愚公移山》出一道HSK4阅读题" api

# ④ 作业2：调小 max_tokens 观察截断
python run_test.py "用一句话说明什么是把字句" local 20
```

## 异常回退与重试机制

| 情况 | 行为 |
|------|------|
| `prefer='local'` 本地正常 | 直接返回本地答案 |
| `prefer='local'` 本地挂 | 打印 `[首选引擎失败，自动切换]`，走云端 |
| `prefer='api'` 云端正常 | 直接返回云端答案 |
| `prefer='api'` 云端挂 | 打印切换日志，回退本地 |
| 瞬时错误（连接失败/超时） | 同一引擎重试 1 次（共 2 次尝试）后再回退 |
| 确定性错误（401/402/404） | 不重试，直接回退 |

## prefer 怎么选（判断依据）

| 教学任务 | prefer | 理由 |
|----------|--------|------|
| 批改学生作文/成绩与评语 | `local` | 未成年人数据不出本机，隐私红线优先 |
| 批量生成格式固定的练习 | `local` | 高频调用不计 token，小模型够用 |
| 复杂教案设计/多步推理/长文改写 | `api` | 云端质量明显更好，值得花 token |
| 教室断网/平台限流演示 | `local` | 离线可用是硬约束 |
| 拿不准时的课堂默认 | `local` | 失败会自动切云端，自带兜底 |

## 作业 1：失败重试的实现与理由

三选一里选了「失败重试（最多 2 次再回退）」：

- **理由**：双引擎的核心承诺是「打不死」。真实课堂最常见的失败不是模型答错，而是网络抖一下、Ollama 刚启动还没就绪——这类瞬时错误重试一次往往就恢复。
- **实现**：`LLM._try_engine()` 对每个引擎最多尝试 `RETRY_TIMES=2` 次；只对 `ConnectionError / Timeout` 这类瞬时错误重试，`401/402/404` 直接放弃回退。
- **为什么不做多轮对话**：会改变 `ask()` 的接口语义（要传 messages 历史），更适合 W7 之后再做。
- **为什么不做费用打印**：费用估算依赖平台单价，放到 RAG/助手阶段更有意义。

## 跨周 import（讲义第七节的坑）

根目录新建了 `weekpath.py`，把各周目录注册进 `sys.path`：

```python
import weekpath          # 先导入根目录的 weekpath
from llm import LLM      # W7/W8 里这样就能找到 week06 的 llm.py
```

已实测：在仓库根目录运行 `import weekpath; from llm import LLM` 成功，W4 的 `weekpath` 兼容不受影响。

## 密钥纪律

- 密钥只从环境变量读（`MINIMAX_API_KEY`），绝不写进代码
- `.env` 在 `.gitignore` 里，push 前先 `git status` 确认没有 `.env`
