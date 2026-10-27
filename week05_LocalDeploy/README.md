# 第 5 周 · 本地部署入门：把 AI 装进自己的电脑

> 课程：《人工智能在学习环境中的应用与实践》第 5 周（10/20 课）
> 机器：Windows / 内存 7.9 GB（≈8 GB）/ 无独立显卡
> Ollama 0.40.6　模型 `qwen2.5:0.5b`

## 本周做了什么

在自己的电脑上装 Ollama、拉一个小模型跑通对话，然后把「本地 vs 云端」的取舍写成一份可复用的选型笔记。

## 产出物

| 文件 | 说明 |
|------|------|
| [ollama_notes.md](ollama_notes.md) | **核心评分件**：安装踩坑、选型理由、5 问对比表、量化 vs MCP、隐私红线与脱敏 |
| [compare_local_cloud.py](compare_local_cloud.py) | 复现脚本：同一组 5 个学科问题分别问本地与云端，直接打印 Markdown 对比表 |

## 本机跑通证据

| 命令 | 结果 |
|------|------|
| `ollama --version` | `ollama version is 0.40.6` |
| `ollama list` | `qwen2.5:0.5b`，397 MB |
| `ollama run qwen2.5:0.5b "…"` | 正常返回回答，不报错 |
| `ollama ps` | SIZE 486 MB、PROCESSOR **100% CPU**、CONTEXT 4096 |

## 三条核心结论

1. **硬件决定量级**：8 GB 内存 + 无独显 → 0.5B~1.5B 是稳妥档位；7B 会换页，课堂等不起。
2. **量化 ≠ MCP**：量化解决「装不装得下」，MCP 解决「能不能用外部工具」，两者无关。
3. **隐私红线 > 质量 > 速度**：学生作文、成绩、未公开教案不出本机；上云前必须三步脱敏。

## 复现方式

```powershell
# 前提：Ollama 已启动；仓库根目录 .env 里配好 MINIMAX_API_KEY（没有则云端列标失败）
python week05_LocalDeploy/compare_local_cloud.py
# 推理型问题（如「把字句」）思考耗 token，可加大额度：
python week05_LocalDeploy/compare_local_cloud.py 2500
```
