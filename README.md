# ai-portfolio

人工智能在学习环境中的应用与实践 —— 课程作品集（每周一个独立文件夹）

---

## 📚 课程目录

| 周次 | 文件夹 | 主题 | 核心产出 |
|------|--------|------|----------|
| W1 | [week01_仓库初始化/](week01_仓库初始化/) | 仓库初始化与 AI 任务单 | `hello.py`、`ai.任务单.md` |
| W2 | [week02_Prompt工程/](week02_Prompt工程/) | Prompt 工程 | 8 个学科模板 + R1–R4 迭代实录 |
| W3 | [week03_AI结对编程/](week03_AI结对编程/) | AI 结对编程 | `vocab_tool.py`、语法卡片 W3 |
| W4 | [week04_API/](week04_API/) | 第一次 API 调用 | `week4_api_bot.py`、密钥安全自查表 |
| W5 | [week05_LocalDeploy/](week05_LocalDeploy/) | 本地部署入门 | `ollama_notes.md`（本地 vs 云端对比） |
| W6 | [week06_双引擎/](week06_双引擎/) | 双引擎封装 | `llm.py`、5 组边界测试记录 |

---

## 🔑 选周速查

### W1 · 仓库初始化
建 GitHub 仓库、跑通 `hello.py`、用任务单记录过程。学会 `git add / commit / push`。

### W2 · Prompt 工程
8 个汉语教学模板（出题 / 批改 / 口语 / 改写 / 教案 / 文化 / 生词 / 近义词），
每个都做了 R1→R4 迭代，核心方法是**结构化输出约束**。

### W3 · AI 结对编程
用 Python 处理生词表：筛选 HSK4、统计词性、生成练习题。
重点是**逐行读 AI 代码**，修掉字段名、编码、路径 4 个坑。

### W4 · 第一次 API 调用
用 Python 调云端 API，命令行学科问答机器人；密钥安全五条铁律。

### W5 · 本地部署入门
Ollama 装进本机、按内存选模型、本地 vs 云端 5 问对比；量化 ≠ MCP。

### W6 · 双引擎封装
`LocalEngine + APIEngine + LLM`，`prefer` 一键切换，双向异常回退。

---

## 🔧 环境与密钥

- `weekpath.py`（根目录）：统一加载 `.env`、把各周目录注册进 `sys.path`，供跨周 import
- `.env`：**只在本地**，已被 `.gitignore` 忽略，绝不提交
- 依赖：`openai`、`requests`、`python-dotenv`；本地模型用 Ollama

---

## 📝 说明

每个周文件夹内都有自己的 `README.md`，写清本周做了什么、产出什么、学到什么。
以远端提交记录为考核证据。
