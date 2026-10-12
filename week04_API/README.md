# 第四次课：第一次 API 调用

## 📦 文件说明

| 文件 | 说明 |
|------|------|
| `week4_api_bot.py` | 命令行学科问答机器人主脚本 |
| `weekpath.py` | 路径工具（加载 .env，写日志到仓库根目录）|
| `.env.example` | 环境变量模板（复制为 `.env` 后填入密钥）|
| `requirements.txt` | Python 依赖 |
| `密钥安全自查表.md` | 密钥安全检查清单 |
| `chat_log.txt` | 对话日志（运行后自动生成，已在 .gitignore 排除）|

## 🚀 快速开始

### 1. 安装依赖
```bash
cd week04_API
pip install -r requirements.txt
```

### 2. 配置密钥
```bash
# 复制模板
copy .env.example .env

# 编辑 .env，把 DEEPSEEK_API_KEY=your_deepseek_key_here 换成你的真实密钥
```

### 3. 运行机器人
```bash
python week4_api_bot.py "把字句的教学难点有哪些"
```

### 4. 课堂实验问题（任选3个你的学科问题）

**汉语国际教育专业示例：**
- 把字句的教学难点有哪些
- HSK4级对词汇量的要求是多少
- 给一篇中级汉语作文写三段式评语

## 📊 课堂实验记录

### 参数体验记录

| 参数组合 | 观察到的现象 |
|----------|--------------|
| temperature=0.0, max_tokens=15 | |
| temperature=0.0, max_tokens=800 | |
| temperature=1.5, max_tokens=60 | |
| temperature=0.7, max_tokens=800 (默认) | |

### Token 用量记录

运行 `python week4_api_bot.py "用一句话说明什么是把字句"` 后：

- 输入 tokens: ___
- 输出 tokens: ___
- 总计: ___
- 费用: ___ 元

## 🔒 密钥安全

**每次提交前必须完成密钥安全自查表！**

详见 `密钥安全自查表.md`
