# 📊 开了吗 / Open Lah? — 排行榜

> 论文开源与复现状态排行榜 / Paper Open-Source & Reproducibility Leaderboard

---

## 🏆 排行榜 / Leaderboards

| 榜单 | 说明 | 链接 |
|------|------|------|
| 📈 **NonRepro** | 按不可复现分数排序，分数越高表示开源/复现状况越差 | [查看](leaderboard_nonrepro.md) |
| 🔥 **HeatWeighted** | 按热度加权分数排序，高热度但难复现的论文排名更高 | [查看](leaderboard_heatweighted.md) |
| 🕐 **Recent** | 按最近更新时间排序，展示最新的跟踪记录 | [查看](leaderboard_recent.md) |

---

## 📐 计算公式 / Scoring Formula

```
Openness = open/full→1.0 | open/partial→0.4 | open/broken→0.2 | open/empty→0.1 | open/none→0.0

ReproPenalty = repro/match→0.0 | repro/partial→0.4 | repro/mismatch→1.0 | repro/none→1.0 | repro/unknown→0.7

Heat = heat/1→1 | heat/2→2 | heat/3→3

NonReproScore = (1 - Openness) × ReproPenalty

HeatWeightedScore = Heat × NonReproScore
```

---

## 🏷️ 标签速查 / Label Quick Reference

### 开源状态 / Open Status

| Label | Score | 说明 |
|-------|-------|------|
| 🟢 `open/full` | 1.0 | 完整开源 |
| 🟡 `open/partial` | 0.4 | 部分开源 |
| 🟠 `open/broken` | 0.2 | 损坏开源 |
| 🔴 `open/empty` | 0.1 | 空仓库 |
| ⚫ `open/none` | 0.0 | 未开源 |

### 复现状态 / Repro Status

| Label | Penalty | 说明 |
|-------|---------|------|
| 🟢 `repro/match` | 0.0 | 完全复现 |
| 🟡 `repro/partial` | 0.4 | 部分复现 |
| 🔴 `repro/mismatch` | 1.0 | 无法复现 |
| ⚫ `repro/none` | 1.0 | 无法尝试 |
| ⚪ `repro/unknown` | 0.7 | 未知 |

---

## 🔗 快速链接 / Quick Links

- 📖 [项目主页 / README](../README.md)
- 📝 [提交新论文 / Submit Paper](../../../issues/new?template=paper_tracking.yml)
- 💡 [提名热门论文 / Nominate Topic](../../../issues/new?template=topic_nomination.yml)
- 🏷️ [查看所有标签 / All Labels](../../../labels)
- 📋 [查看所有 Issues](../../../issues?q=is%3Aissue+is%3Aopen+label%3Apaper%2Ftracking)

---

## 🤖 关于自动更新 / About Auto-Update

此排行榜由 GitHub Actions 自动生成和更新：
- **触发条件**：Issues 创建/编辑/标签变更时
- **定时更新**：每天 UTC 00:00
- **手动更新**：可在 Actions 页面手动触发

---

<p align="center">
  <i>「开了吗？」—— 让学术开源透明可查</i><br>
  <i>"Open Lah?" — Making academic open-source transparent</i>
</p>
