"""
vocab_tool.py — 生词表 CSV 处理工具
功能：读生词表 → 按 HSK 等级筛选 → 统计词性分布 → 输出练习题
扩展功能：按词性分组输出 + 生成填空题

用法（从 week03_Python/ 目录运行）：
    python vocab_tool.py
    # 或
    py -3 vocab_tool.py
"""

import csv
import weekpath  # 路径约定工具（与本脚本同目录的 weekpath.py）

# ── 数据路径约定 ─────────────────────────────────────────────
DATA = weekpath.data_path("生词表.csv")          # data/生词表.csv（绝对路径）
OUT_EXERCISES  = weekpath.root_path("练习.txt")  # 仓库根目录 ../练习.txt
OUT_BY_POS     = weekpath.root_path("练习_按词性.txt")
OUT_FILL_BLANK = weekpath.root_path("练习_填空.txt")


# ── ① 读：把 CSV 读成字典列表 ────────────────────────────────
def load_words(path=DATA):
    """读取 CSV，返回字典列表（每行一个 dict）。"""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ── ② 筛：按 HSK 等级筛选 ───────────────────────────────────
def filter_by_level(words, level="4"):
    """返回指定 HSK 等级的生词列表，按词汇升序排列（稳定排序）。"""
    return sorted(
        [w for w in words if str(w["HSK等级"]) == str(level)],
        key=lambda w: w["词汇"]
    )


# ── ③ 统：统计词性分布 ──────────────────────────────────────
def count_by_pos(words):
    """返回 dict：{词性: 人数}，按首次出现顺序记录。"""
    d = {}
    for w in words:
        d[w["词性"]] = d.get(w["词性"], 0) + 1
    return d


# ── ④ 写：生成造句练习题 ────────────────────────────────────
def gen_exercises(words, out=None):
    """生成造句练习题，每行一条，写入 out 文件。"""
    out = out or OUT_EXERCISES
    with open(out, "w", encoding="utf-8") as f:
        for w in words:
            f.write("用\"%s\"造一个句子。（%s）\n" % (w["词汇"], w["词性"]))


# ════════════════════════════════════════════════════════════
# 扩展功能（作业 2：二选一或全做）
# ════════════════════════════════════════════════════════════

def group_by_pos(words, out=None):
    """
    【扩展功能 ①】按词性分组输出
    格式：词性
      - 词汇1
      - 词汇2
    """
    out = out or OUT_BY_POS
    # 按词性分组，保持首次出现顺序
    pos_map = {}
    for w in words:
        pos = w["词性"]
        if pos not in pos_map:
            pos_map[pos] = []
        pos_map[pos].append(w["词汇"])

    with open(out, "w", encoding="utf-8") as f:
        for pos, vocab_list in pos_map.items():
            f.write(f"【{pos}】\n")
            for v in sorted(vocab_list):
                f.write(f"  - {v}\n")
            f.write("\n")


def gen_fill_blank(words, out=None):
    """
    【扩展功能 ②】生成填空题
    把造句题中的目标词挖空成 ____。
    示例：用"坚持"造一个句子。（动词）
          → 用"____"造一个句子。（动词）
    """
    out = out or OUT_FILL_BLANK
    with open(out, "w", encoding="utf-8") as f:
        for w in words:
            line = "用\"%s\"造一个句子。（%s）\n" % (w["词汇"], w["词性"])
            blank_line = line.replace(w["词汇"], "____")
            f.write(blank_line)


# ── 主入口：直接运行脚本时执行全部输出 ──────────────────────
if __name__ == "__main__":
    # ① 读取全部生词
    all_words = load_words()

    # ② 筛选 HSK4
    lv4 = filter_by_level(all_words, "4")

    # ③ 统计词性分布（针对筛选后的 HSK4 词汇）
    pos_dist = count_by_pos(lv4)

    # 打印摘要（与 PPT 预期输出一致）
    print("总词汇 %d 个，其中 HSK4 词汇 %d 个，" % (len(all_words), len(lv4)))
    print("词性分布：%s" % pos_dist)

    # ④ 生成练习题（主交付物）
    gen_exercises(lv4)
    print("已生成：%s" % OUT_EXERCISES)

    # 扩展功能（作业 2）
    group_by_pos(lv4)
    print("已生成：%s" % OUT_BY_POS)

    gen_fill_blank(lv4)
    print("已生成：%s" % OUT_FILL_BLANK)
