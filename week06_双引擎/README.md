# W6 双引擎封装：llm.py

> 业务代码只认 `llm.ask()`，本地/云端切换只改一个参数。

## 文件说明

| 文件 | 说明 |
|------|------|
| `llm.py` | 三个类：`LocalEngine`（本地 Ollama）、`APIEngine`（云端 MiniMax）、`LLM`（统一入口） |
| `run_test.py` | 三路径实测小工具，打印测试条件/耗时/回答 |
| `week06_test_log.md` | 边界测试记录（≥3 组，四列） |

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

# ③ prefer='api'（云端不可用/未配密钥时会回退本地）
python run_test.py "给《愚公移山》出一道HSK4阅读题" api
```

## 异常回退机制

| 情况 | 行为 |
|------|------|
| `prefer='local'` 本地正常 | 直接返回本地答案 |
| `prefer='local'` 本地挂 | 打印 `[首选引擎失败，自动切换]`，走云端 |
| `prefer='api'` 云端正常 | 直接返回云端答案 |
| `prefer='api'` 云端挂 | 打印切换日志，回退本地 |

## prefer 怎么选（判断依据）

| 教学任务 | prefer | 理由 |
|----------|--------|------|
| 批改学生作文/成绩与评语 | `local` | 未成年人数据不出本机，隐私红线优先 |
| 批量生成格式固定的练习 | `local` | 高频调用不计 token，小模型够用 |
| 复杂教案设计/多步推理/长文改写 | `api` | 云端质量明显更好，值得花 token |
| 教室断网/平台限流演示 | `local` | 离线可用是硬约束 |
| 拿不准时的课堂默认 | `local` | 失败会自动切云端，自带兜底 |

## 密钥纪律

- 密钥只从环境变量读（`MINIMAX_API_KEY`），绝不写进代码
- `.env` 在 `.gitignore` 里，push 前先 `git status` 确认没有 `.env`
