# 开了吗 / Open Lah? 🔬

> **论文开源/复现跟踪系统** — A Paper Open-Source & Reproducibility Tracking System

[![Leaderboard](https://img.shields.io/badge/📊-Leaderboard-blue)](docs/index.md)
[![Issues](https://img.shields.io/github/issues/OWNER/REPO)](../../issues)

---

## 🌏 这是什么 / What is this?

**中文**：「开了吗」是一个社区驱动的论文开源与复现状态跟踪系统。我们使用 GitHub Issues 作为数据库，通过标签系统记录每篇论文的开源程度和复现状态，自动生成排行榜，让学术界的开源情况透明可查。

**English**: "Open Lah?" is a community-driven tracking system for paper open-source status and reproducibility. We use GitHub Issues as our database, with a label system to record each paper's openness level and reproduction status, automatically generating leaderboards for transparency in academic open-source practices.

---

## 📜 原则 / Principles

### 1. 证据优先 / Evidence First
- 所有状态判定必须附带证据链接（代码仓库、复现报告、Issue 讨论等）
- All status determinations must include evidence links (code repos, reproduction reports, issue discussions, etc.)

### 2. 不投票审判 / No Voting Judgments
- 我们不对论文质量做主观评价，只记录客观的开源/复现事实
- We don't make subjective judgments on paper quality; we only record objective open-source/reproduction facts

### 3. 可追溯 / Traceable
- 每条记录都是一个 Issue，所有修改历史可查，状态变更需说明理由
- Each record is an Issue; all modification history is visible, and status changes require explanations

---

## 📝 提交流程 / Submission Process

### 提交新论文跟踪 / Submit New Paper Tracking

1. 点击 [New Issue](../../issues/new/choose)
2. 选择 **「📄 Paper Tracking」** 模板
3. 填写必填字段：
   - 论文标题 / Paper Title
   - 论文链接 / Paper Link
   - 热度等级 / Heat Level (1-3)
   - 开源状态 / Open Status
   - 代码链接 / Code Link
   - 复现状态 / Repro Status
   - 证据链接 / Evidence Links
4. 提交后等待社区验证（status/needs-triage → status/verified）

### 提名热门论文 / Nominate Hot Papers

1. 点击 [New Issue](../../issues/new/choose)
2. 选择 **「🔥 Topic Nomination」** 模板
3. 填写论文链接和热度预估
4. 社区成员可认领并创建完整的 Paper Tracking Issue

---

## 🏷️ 标签说明 / Labels Explained

### 开源状态 / Open Status (`open/*`)

| Label | 说明 / Description | Openness Score |
|-------|---------------------|----------------|
| `open/full` | 完整开源：代码、权重、数据全部可用 | 1.0 |
| `open/partial` | 部分开源：核心代码可用，但缺少部分组件 | 0.4 |
| `open/broken` | 损坏开源：代码存在但无法运行 | 0.2 |
| `open/empty` | 空仓库：声称开源但仓库为空 | 0.1 |
| `open/none` | 未开源：没有公开代码 | 0.0 |

### 复现状态 / Repro Status (`repro/*`)

| Label | 说明 / Description | Repro Penalty |
|-------|---------------------|---------------|
| `repro/match` | 完全复现：结果与论文一致 | 0.0 |
| `repro/partial` | 部分复现：主要结果可复现，细节有差异 | 0.4 |
| `repro/mismatch` | 无法复现：结果与论文明显不符 | 1.0 |
| `repro/none` | 无法尝试：因开源不足无法复现 | 1.0 |
| `repro/unknown` | 未知：尚无复现报告 | 0.7 |

### 热度等级 / Heat Level (`heat/*`)

| Label | 说明 / Description |
|-------|---------------------|
| `heat/1` | 普通论文 / Regular paper |
| `heat/2` | 热门论文 / Hot paper (100+ citations or significant attention) |
| `heat/3` | 顶流论文 / Top paper (flagship work, widely discussed) |

### 问题标签 / Issue Tags (`tag/*`)

| Label | 说明 / Description |
|-------|---------------------|
| `tag/no-weights` | 缺少预训练权重 |
| `tag/no-train-code` | 缺少训练代码 |
| `tag/bug-mismatch` | 代码有 bug 导致结果不符 |
| `tag/data-missing` | 数据集不可获取 |
| `tag/underdocumented` | 文档不足 |
| `tag/not-generalizable` | 结果不可泛化 |

### 状态标签 / Status (`status/*`)

| Label | 说明 / Description |
|-------|---------------------|
| `status/needs-triage` | 待验证：新提交，等待社区核实 |
| `status/verified` | 已验证：信息经社区确认 |
| `status/disputed` | 有争议：状态判定存在分歧 |

---

## 📊 排行榜说明 / Leaderboard Explained

我们自动生成三个排行榜：

### 1. [NonRepro 排行榜](docs/leaderboard_nonrepro.md)
按 **不可复现分数** 排序，分数越高表示开源/复现状况越差。

### 2. [HeatWeighted 排行榜](docs/leaderboard_heatweighted.md)
按 **热度加权分数** 排序，高热度但难复现的论文排名更高。

### 3. [Recent 排行榜](docs/leaderboard_recent.md)
按 **最近更新时间** 排序，展示最新的跟踪记录。

### 计算公式 / Scoring Formula

```
Openness = open/full→1.0 | open/partial→0.4 | open/broken→0.2 | open/empty→0.1 | open/none→0.0

ReproPenalty = repro/match→0.0 | repro/partial→0.4 | repro/mismatch→1.0 | repro/none→1.0 | repro/unknown→0.7

Heat = heat/1→1 | heat/2→2 | heat/3→3

NonReproScore = (1 - Openness) × ReproPenalty

HeatWeightedScore = Heat × NonReproScore
```

**解读**：
- `NonReproScore` 越高 = 开源越差 + 复现越难
- 完全开源（open/full）的论文 NonReproScore = 0
- 完全复现（repro/match）的论文 NonReproScore = 0
- 高热度（heat/3）但难复现的论文会在 HeatWeighted 榜单更靠前

---

## 🤝 行为准则 / Code of Conduct

1. **客观公正**：只记录事实，不进行人身攻击或主观评价
2. **提供证据**：所有判定必须附带可验证的证据
3. **善意推定**：对作者保持善意，开源是贡献不是义务
4. **及时更新**：当状态改变时（如作者后续开源），及时更新记录
5. **尊重隐私**：不泄露非公开信息，不骚扰论文作者

---

## 🔗 快速链接 / Quick Links

- 📊 **[排行榜总览 / Leaderboard Index](docs/index.md)**
- 📈 [NonRepro 排行榜](docs/leaderboard_nonrepro.md)
- 🔥 [HeatWeighted 排行榜](docs/leaderboard_heatweighted.md)
- 🕐 [Recent 排行榜](docs/leaderboard_recent.md)
- 📝 [提交新论文 / Submit Paper](../../issues/new?template=paper_tracking.yml)
- 💡 [提名热门论文 / Nominate Topic](../../issues/new?template=topic_nomination.yml)

---

## 📄 License

MIT License - 数据由社区贡献，欢迎合理使用。

---

<p align="center">
  <i>「开了吗？」—— 让学术开源透明可查</i><br>
  <i>"Open Lah?" — Making academic open-source transparent and traceable</i>
</p>
