# AI 辅助编程实录

> 课程：《人工智能在学习环境中的应用与实践》第 3 周
> 模式：AI 结对编程（你主程，AI 副驾）
> 完成日期：2026-10-01

---

## 1. 任务与提示词

### 要做什么
读生词表 CSV → 按 HSK 等级筛选 → 统计词性分布 → 输出练习题文件。

### 我写的提示词

```
角色：你是 Python 教学助手，擅长用标准库处理 CSV 数据。
任务：写一个独立的 Python 脚本 vocab_tool.py，功能如下：
  1. 读取 data/生词表.csv（字段：词汇, HSK等级, 词性, 释义, 备注）
  2. 按 HSK 等级筛选（默认等级 4）
  3. 统计筛选后词汇的词性分布并打印
  4. 为每个词生成一行造句练习题，格式：用"X"造一个句子。（词性）
     输出到练习.txt

要求：
  - 仅使用 Python 标准库（csv、文件读写），不安装任何第三方包
  - 兼容 Windows 路径
  - 每行代码加中文注释，说明在做什么
  - 代码要有可读性，方便答辩时讲解每一行

示例输出格式：
  用"坚持"造一个句子。（动词）
  用"风景"造一个句子。（名词）
```

---

## 2. AI 初版代码

以下是 AI 第一次生成的完整代码（未做任何修改的原样）：

```python
import csv
import os
import argparse          # ← 超纲：argparse 不是本周内容，答辩讲不清为什么需要

# ── 命令行参数解析（本周不需要，删除即可）───────────────────
parser = argparse.ArgumentParser(description="生词表处理工具")
parser.add_argument("--level", default="4", help="HSK 等级（默认 4）")
parser.add_argument("--input",  default="data/生词表.csv", help="输入 CSV 路径")
parser.add_argument("--output", default="练习.txt",         help="输出文件路径")
args = parser.parse_args()

# ── ① 读取 CSV（错误：字段名用"等级"，但 CSV 表头是"HSK等级"）─
def load_words(path):
    words = []
    with open(path) as f:                       # ← 错误：缺少 encoding="utf-8"
        reader = csv.DictReader(f)
        for row in reader:
            if row["等级"] == args.level:       # ← KeyError！表头叫"HSK等级"
                words.append(row)
    return words

# ── ② 统计词性分布 ──────────────────────────────────────────
def count_by_pos(words):
    dist = {}
    for w in words:
        pos = w["词性"]
        dist[pos] = dist.get(pos, 0) + 1
    return dist

# ── ③ 生成练习题（错误：路径写死，跨目录运行会找不到文件）───
def gen_exercises(words, out_path):
    with open(out_path, "w") as f:              # ← 错误：缺少 encoding="utf-8"
        for w in words:
            line = "用「{}」造一个句子。（{}）\n".format(w["词汇"], w["词性"])
            f.write(line)

# ── 主流程 ──────────────────────────────────────────────────
if __name__ == "__main__":
    words = load_words(args.input)
    dist  = count_by_pos(words)
    print("HSK%s 共 %d 词，词性分布：%s" % (args.level, len(words), dist))
    gen_exercises(words, args.output)
    print("已生成：%s" % args.output)
```

**AI 初版的问题（我逐行读完后发现的）：**
- `row["等级"]` → KeyError：CSV 表头是 `"HSK等级"`，不是 `"等级"`
- 两处 `open()` 缺少 `encoding="utf-8"`，Windows 上会 UnicodeDecodeError
- argparse 是超纲内容：本周只需默认等级 4，命令行参数答辩时说不清为什么需要
- 输出路径写死相对路径 `"练习.txt"`，从其他目录运行文件会散落各处

---

## 3. 我的修改点（≥3 条，另有第 4 条来自官方教程学习）

### 修改点①：字段名修正
**原因**：AI 用 `"等级"` 查字典，CSV 实际表头是 `"HSK等级"`，运行必报 KeyError。
**修改**：`row["等级"]` → `str(row["HSK等级"]) == str(level)`，加 `str()` 避免 CSV 中数字类型不一致。

### 修改点②：所有文件操作加 `encoding="utf-8"`
**原因**：Windows 默认文件编码是 GBK，不写 `encoding="utf-8"` 会报 UnicodeDecodeError。
**修改**：CSV 读取和所有练习文件写入均加上 `encoding="utf-8"`。

### 修改点③：引入 weekpath.py 统一路径
**原因**：硬编码 `"练习.txt"` 意味着文件落在运行时的当前目录（cwd），从不同目录运行会找不到文件。
**修改**：在同一目录放 `weekpath.py`，用 `sys.path.insert` 引入，`weekpath.root_path("练习.txt")` 统一输出到仓库根目录，无论从哪里运行都找得到。

### 修改点④（来自作业 1 — 精读官方教程后加入）：用 `sorted()` 稳定排序
**原因**：精读 Python 官方教程「列表」章节时学到了内置函数 `sorted()`。
原 AI 代码输出的词序与 CSV 行顺序一致，排序后输出稳定可预期，且与 PPT 预期输出一致（商量→坚持→讨论→风景，按词汇拼音升序）。
**修改**：在 `filter_by_level()` 中用 `sorted(..., key=lambda w: w["词汇"])` 对结果排序。

### 修改点⑤（来自作业 2 — 扩展功能 ①）：按词性分组输出
**原因**：作业 2 要求给脚本扩展至少一个功能，选择「按词性分组输出」。
**修改**：新增 `group_by_pos(words)` 函数，将同一词性的词归为一组，输出到 `练习_按词性.txt`。

### 修改点⑥（来自作业 2 — 扩展功能 ②）：生成填空题
**原因**：作业 2 第二选做项，把造句题中的目标词挖空成 `____`。
**修改**：新增 `gen_fill_blank(words)` 函数，将每行练习题的目标词替换为 `____`，输出到 `练习_填空.txt`。

---

## 4. 最终版 vs 初版差异说明

| 差异项 | AI 初版 | 最终版 | 为什么这样改 |
|--------|---------|--------|--------------|
| 字段查询 | `row["等级"]` | `str(row["HSK等级"]) == str(level)` | CSV 表头是"HSK等级"，加 str() 防类型不一致 |
| 文件编码 | 缺少 encoding | 全部 `encoding="utf-8"` | Windows 默认 GBK，不写会 UnicodeDecodeError |
| 命令行参数 | argparse（用户可自定义等级） | 删除 argparse，默认等级 "4" 写死在调用处 | 本周只学 4 个语法，argparse 超纲且答辩讲不清 |
| 路径处理 | 硬编码相对路径 `"练习.txt"` | `weekpath.root_path("练习.txt")` | 无论从哪个目录运行，产物都落在仓库根目录 |
| 词序 | CSV 行顺序 | `sorted(..., key=lambda w: w["词汇"])` | 按词汇拼音升序，输出稳定，与 PPT 预期一致 |
| 代码组织 | 单一大函数 | 拆成 load_words / filter_by_level / count_by_pos / gen_exercises 四个函数 | 四个函数各管一件事，可复用、可答辩讲解 |
| 扩展功能 | 无 | 新增 group_by_pos + gen_fill_blank | 作业 2 要求，选做功能 |
| 路径可移植性 | 无 | `sys.path.insert` + 同目录 weekpath.py | 保证 weekpath 模块从任意工作目录都能被找到 |

**总结**：AI 初版思路基本正确，但字段名、编码、路径三处有致命错误，argparse 是画蛇添足。`sorted()` 排序是读了官方教程后主动加的（作业 1），两个扩展功能是作业 2 的要求。最终代码读得懂、跑得通、答辩说得清。

---

## 5. 运行验证

```powershell
cd "C:\Users\shenj\Desktop\AI Workspace\AI结对编程"
python vocab_tool.py
```

输出：
```
总词汇 14 个，其中 HSK4 词汇 4 个，词性分布：{'动词': 3, '名词': 1}
已生成：C:\Users\shenj\Desktop\AI Workspace\AI结对编程\练习.txt
已生成：C:\Users\shenj\Desktop\AI Workspace\AI结对编程\练习_按词性.txt
已生成：C:\Users\shenj\Desktop\AI Workspace\AI结对编程\练习_填空.txt
```

练习.txt 内容（与 PPT 第 9 页预期完全一致）：
```
用"商量"造一个句子。（动词）
用"坚持"造一个句子。（动词）
用"讨论"造一个句子。（动词）
用"风景"造一个句子。（名词）
```

---

*记录人：AI 结对编程学员*  
*下次改进方向：CSV 中若增加「例句」字段，可将填空题做得更自然（直接挖空例句中的目标词）；还可以加「按释义检索」功能。*
