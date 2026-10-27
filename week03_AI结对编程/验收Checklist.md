# 第 3 周 · 离场验收 Checklist

> 依据：`第三周_Python速成_AI结对编程.pptx` 第 15 页
> 验收标准：逐项打钩，再离开教室 / 再提交

## 交付物验收

- [x] **`vocab_tool.py` 能独立运行**：`python vocab_tool.py` 有输出、不报错
- [x] **`练习.txt` 内容正确**：至少包含筛选后目标等级（HSK4）的生词造句题
- [x] **能说清四个函数分别干什么**：读（load_words）/ 筛（filter_by_level）/ 统（count_by_pos）/ 写（gen_exercises）
- [x] **`AI辅助编程实录.md` 四段齐全**：任务与提示词 / AI 初版代码 / 我的修改点（≥3 条且写明为什么）/ 最终版 vs 初版差异
- [x] **`git log` 可见本周提交**，GitHub 网页端能看到脚本与实录
- [x] **已记下作业**：官方教程选读 / 扩展 1 个功能 / 语法卡片复习

## PPT 要求的运行输出（实测一致）

```
$ python vocab_tool.py
总词汇 14 个，其中 HSK4 词汇 4 个，词性分布：{'动词': 3, '名词': 1}
已生成：...\week03_AI结对编程\练习.txt
已生成：...\week03_AI结对编程\练习_按词性.txt
已生成：...\week03_AI结对编程\练习_填空.txt
```

## PPT 四条语法点自检

| 语法点 | 在代码里的位置 | 能讲清吗 |
|--------|----------------|----------|
| 变量 | `words = load_words()`、`lv4 = filter_by_level(...)` | ✅ |
| 条件 if | `if str(w["HSK等级"]) == str(level)` | ✅ |
| 循环 for | `for w in words:` | ✅ |
| 函数 def | `load_words / filter_by_level / count_by_pos / gen_exercises` | ✅ |

## PPT「三条纪律」自检

- [x] 不粘贴自己读不懂的代码（实录里每条修改都写了原因）
- [x] 先猜输出再运行（实录里记录了预期输出与实际输出对比）
- [x] 报错先自己读 30 秒（实录记录了 KeyError 的定位过程）

## PPT 三个高频报错自检

| 报错 | 本仓库是否已规避 | 规避方式 |
|------|------------------|----------|
| `KeyError: 'HSK等级'` | ✅ | 表头字段名与 CSV 一致，加了 `str()` 防类型不一致 |
| `FileNotFoundError` | ✅ | `weekpath.data_path()` / `root_path()` 统一解析，不写死相对路径 |
| `UnicodeDecodeError` | ✅ | 所有 `open()` 都写 `encoding="utf-8"` |

## PPT 本周红线自检

- [x] 本周不用任何密钥（W4 才引入 API）
- [x] 绝不 paste 读不懂的代码进仓库
- [x] 提交前 `git status` 看一眼，确认没把 `.env` 带上
