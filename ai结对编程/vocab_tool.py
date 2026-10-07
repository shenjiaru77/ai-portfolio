# W3 生词表 CSV -> 自动生成练习题（含扩展功能）
# 运行：python vocab_tool.py
import os
import csv
import sys

# 让 weekpath.py 能被找到（weekpath.py 放在本文件同一目录的 weekpath.py）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import weekpath  # noqa: E402  统一解析 data/ 路径，换目录也不会找不到文件

DATA = weekpath.data_path("生词表.csv")


# ── ① 读：把 CSV 读成字典列表 ────────────────────────────────
def load_words(path=DATA):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ── ② 筛：按 HSK 等级筛选（排序输出）────────────────────────
def filter_by_level(words, level="4"):
    # sorted() 来自官方教程「列表」章节：按词汇升序排列，输出更稳定有序
    return sorted(
        [w for w in words if str(w["HSK等级"]) == str(level)],
        key=lambda w: w["词汇"]
    )


# ── ③ 统：统计词性分布 ──────────────────────────────────────
def count_by_pos(words):
    d = {}
    for w in words:
        d[w["词性"]] = d.get(w["词性"], 0) + 1
    return d


# ── ④ 写：生成造句练习题 ────────────────────────────────────
def gen_exercises(words, out=None):
    out = out or weekpath.root_path("练习.txt")
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
    out = out or weekpath.root_path("练习_按词性.txt")
    pos_map = {}
    for w in words:
        pos = w["词性"]
        if pos not in pos_map:
            pos_map[pos] = []
        pos_map[pos].append(w["词汇"])

    with open(out, "w", encoding="utf-8") as f:
        for pos, vocab_list in pos_map.items():
            f.write("【%s】\n" % pos)
            for v in sorted(vocab_list):
                f.write("  - %s\n" % v)
            f.write("\n")


def gen_fill_blank(words, out=None):
    """
    【扩展功能 ②】生成填空题
    把造句题中的目标词挖空成 ____。
    示例：用"坚持"造一个句子。（动词）
          → 用"____"造一个句子。（动词）
    """
    out = out or weekpath.root_path("练习_填空.txt")
    with open(out, "w", encoding="utf-8") as f:
        for w in words:
            line = "用\"%s\"造一个句子。（%s）\n" % (w["词汇"], w["词性"])
            f.write(line.replace(w["词汇"], "____"))


if __name__ == "__main__":
    words = load_words()
    lv4 = filter_by_level(words, "4")
    print("总词汇 %d 个，其中 HSK4 词汇 %d 个，词性分布：%s"
          % (len(words), len(lv4), count_by_pos(lv4)))

    out = weekpath.root_path("练习.txt")
    gen_exercises(lv4, out)
    print("已生成：%s" % out)

    # 扩展功能输出
    group_by_pos(lv4)
    print("已生成：%s" % weekpath.root_path("练习_按词性.txt"))

    gen_fill_blank(lv4)
    print("已生成：%s" % weekpath.root_path("练习_填空.txt"))
