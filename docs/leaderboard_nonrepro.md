# 📈 NonRepro Leaderboard / 不可复现排行榜

> 按不可复现分数 (NonReproScore) 排序，分数越高表示开源/复现状况越差

📅 **Last Updated**: 2026-02-20 01:12 UTC

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
