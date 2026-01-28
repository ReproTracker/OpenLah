# 🔥 HeatWeighted Leaderboard / 热度加权排行榜

> 按热度加权分数 (HeatWeightedScore) 排序，高热度但难复现的论文排名更高

📅 **Last Updated**: 2026-01-28 04:00 UTC

---

| Rank | Paper | Heat | Open | Repro | NonRepro | HeatWeighted | Updated |
|------|-------|------|------|-------|----------|--------------|---------|
| - | 暂无数据 / No data yet | - | - | - | - | - | - |

---

📊 **计算公式 / Scoring Formula**:
- `Openness`: open/full=1.0, open/partial=0.4, open/broken=0.2, open/empty=0.1, open/none=0.0
- `ReproPenalty`: repro/match=0.0, repro/partial=0.4, repro/mismatch=1.0, repro/none=1.0, repro/unknown=0.7
- `NonReproScore = (1 - Openness) × ReproPenalty`
- `HeatWeightedScore = Heat × NonReproScore`

🔗 [返回主页](../README.md) | [查看所有 Issues](https://github.com/ReproTracker/OpenLah/issues?q=is%3Aissue+is%3Aopen+label%3Apaper%2Ftracking)
