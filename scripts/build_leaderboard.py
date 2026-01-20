#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开了吗 / Open Lah? - Leaderboard 生成脚本

从 GitHub API 读取 Issues，计算分数，生成排行榜 Markdown 文件。
仅使用 Python 标准库。

Usage:
    python scripts/build_leaderboard.py

Environment Variables:
    GITHUB_TOKEN: GitHub Personal Access Token (可选，但推荐设置以避免 API 限制)
    GITHUB_REPOSITORY: owner/repo 格式 (在 GitHub Actions 中自动设置)
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ============================================================================
# 配置
# ============================================================================

# 分数映射
OPENNESS_SCORES = {
    "open/full": 1.0,
    "open/partial": 0.4,
    "open/broken": 0.2,
    "open/empty": 0.1,
    "open/none": 0.0,
}

REPRO_PENALTIES = {
    "repro/match": 0.0,
    "repro/partial": 0.4,
    "repro/mismatch": 1.0,
    "repro/none": 1.0,
    "repro/unknown": 0.7,
}

HEAT_VALUES = {
    "heat/1": 1,
    "heat/2": 2,
    "heat/3": 3,
}

# 输出目录
DOCS_DIR = "docs"

# ============================================================================
# GitHub API
# ============================================================================

def get_github_token() -> Optional[str]:
    """获取 GitHub Token"""
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def get_repo() -> str:
    """获取仓库名称 (owner/repo)"""
    # 优先使用环境变量
    repo = os.environ.get("GITHUB_REPOSITORY")
    if repo:
        return repo
    
    # 尝试从 git remote 获取
    try:
        import subprocess
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True
        )
        url = result.stdout.strip()
        # 解析 git@github.com:owner/repo.git 或 https://github.com/owner/repo.git
        match = re.search(r"github\.com[:/]([^/]+/[^/]+?)(?:\.git)?$", url)
        if match:
            return match.group(1)
    except Exception:
        pass
    
    print("❌ 无法确定仓库名称，请设置 GITHUB_REPOSITORY 环境变量")
    sys.exit(1)


def fetch_issues(repo: str, token: Optional[str] = None) -> List[dict]:
    """从 GitHub API 获取所有 open issues"""
    issues = []
    page = 1
    per_page = 100
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "OpenLah-Leaderboard-Bot",
    }
    if token:
        headers["Authorization"] = f"token {token}"
    
    while True:
        url = f"https://api.github.com/repos/{repo}/issues?state=open&per_page={per_page}&page={page}"
        request = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
                if not data:
                    break
                issues.extend(data)
                if len(data) < per_page:
                    break
                page += 1
        except urllib.error.HTTPError as e:
            print(f"❌ GitHub API 错误: {e.code} {e.reason}")
            if e.code == 403:
                print("   可能是 API 限制，请设置 GITHUB_TOKEN 环境变量")
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"❌ 网络错误: {e.reason}")
            sys.exit(1)
    
    return issues


# ============================================================================
# Issue 解析
# ============================================================================

def extract_labels(issue: dict) -> Dict[str, str]:
    """从 issue 中提取标签"""
    labels = {}
    for label in issue.get("labels", []):
        name = label.get("name", "")
        if name.startswith("open/"):
            labels["open"] = name
        elif name.startswith("repro/"):
            labels["repro"] = name
        elif name.startswith("heat/"):
            labels["heat"] = name
    return labels


def parse_body_field(body: str, field_pattern: str) -> Optional[str]:
    """从 issue body 中解析字段值"""
    if not body:
        return None
    # 匹配 "### 字段名\n\n值" 格式
    pattern = rf"###\s*{field_pattern}[^\n]*\n+([^\n#]+)"
    match = re.search(pattern, body, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_from_body(body: str) -> Dict[str, str]:
    """从 issue body 中提取状态信息（作为标签的 fallback）"""
    extracted = {}
    
    if not body:
        return extracted
    
    # 尝试解析开源状态
    open_match = re.search(r"(open/(?:none|empty|broken|partial|full))", body, re.IGNORECASE)
    if open_match:
        extracted["open"] = open_match.group(1).lower()
    
    # 尝试解析复现状态
    repro_match = re.search(r"(repro/(?:none|partial|mismatch|match|unknown))", body, re.IGNORECASE)
    if repro_match:
        extracted["repro"] = repro_match.group(1).lower()
    
    # 尝试解析热度
    heat_match = re.search(r"(heat/[123])", body, re.IGNORECASE)
    if heat_match:
        extracted["heat"] = heat_match.group(1).lower()
    
    return extracted


def is_paper_tracking(issue: dict) -> bool:
    """检查 issue 是否是 paper tracking"""
    labels = [l.get("name", "") for l in issue.get("labels", [])]
    return "paper/tracking" in labels


# ============================================================================
# 分数计算
# ============================================================================

def calculate_scores(labels: Dict[str, str]) -> Tuple[float, float, int, float, float]:
    """
    计算各项分数
    
    Returns:
        (openness, repro_penalty, heat, nonrepro_score, heat_weighted_score)
    """
    openness = OPENNESS_SCORES.get(labels.get("open", ""), 0.0)
    repro_penalty = REPRO_PENALTIES.get(labels.get("repro", ""), 0.7)
    heat = HEAT_VALUES.get(labels.get("heat", ""), 1)
    
    nonrepro_score = (1 - openness) * repro_penalty
    heat_weighted_score = heat * nonrepro_score
    
    return openness, repro_penalty, heat, nonrepro_score, heat_weighted_score


# ============================================================================
# 数据处理
# ============================================================================

class PaperEntry:
    """论文条目"""
    
    def __init__(self, issue: dict):
        self.issue = issue
        self.number = issue.get("number", 0)
        self.title = issue.get("title", "").replace("[Paper] ", "").strip()
        self.url = issue.get("html_url", "")
        self.updated_at = issue.get("updated_at", "")
        self.created_at = issue.get("created_at", "")
        self.body = issue.get("body", "") or ""
        
        # 从标签提取状态
        self.labels = extract_labels(issue)
        
        # 如果标签缺失，从 body 兜底
        body_extracted = extract_from_body(self.body)
        for key in ["open", "repro", "heat"]:
            if key not in self.labels and key in body_extracted:
                self.labels[key] = body_extracted[key]
        
        # 计算分数
        (
            self.openness,
            self.repro_penalty,
            self.heat,
            self.nonrepro_score,
            self.heat_weighted_score,
        ) = calculate_scores(self.labels)
    
    @property
    def open_label(self) -> str:
        return self.labels.get("open", "N/A")
    
    @property
    def repro_label(self) -> str:
        return self.labels.get("repro", "N/A")
    
    @property
    def heat_label(self) -> str:
        return self.labels.get("heat", "N/A")
    
    @property
    def updated_date(self) -> str:
        if self.updated_at:
            try:
                dt = datetime.fromisoformat(self.updated_at.replace("Z", "+00:00"))
                return dt.strftime("%Y-%m-%d")
            except Exception:
                pass
        return "N/A"


def process_issues(issues: List[dict]) -> List[PaperEntry]:
    """处理 issues 列表"""
    entries = []
    for issue in issues:
        # 跳过 pull requests
        if "pull_request" in issue:
            continue
        # 只处理 paper/tracking
        if not is_paper_tracking(issue):
            continue
        entries.append(PaperEntry(issue))
    return entries


# ============================================================================
# Markdown 生成
# ============================================================================

def generate_header(title: str, description: str) -> str:
    """生成 Markdown 头部"""
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    return f"""# {title}

> {description}

📅 **Last Updated**: {now}

---

"""


def generate_table_header() -> str:
    """生成表格头部"""
    return """| Rank | Paper | Heat | Open | Repro | NonRepro | HeatWeighted | Updated |
|------|-------|------|------|-------|----------|--------------|---------|
"""


def generate_table_row(rank: int, entry: PaperEntry) -> str:
    """生成表格行"""
    # 截断标题
    title = entry.title[:50] + "..." if len(entry.title) > 50 else entry.title
    paper_link = f"[{title}]({entry.url})"
    
    return (
        f"| {rank} "
        f"| {paper_link} "
        f"| {entry.heat} "
        f"| {entry.open_label} "
        f"| {entry.repro_label} "
        f"| {entry.nonrepro_score:.2f} "
        f"| {entry.heat_weighted_score:.2f} "
        f"| {entry.updated_date} |\n"
    )


def generate_footer(repo: str) -> str:
    """生成页脚"""
    return f"""
---

📊 **计算公式 / Scoring Formula**:
- `Openness`: open/full=1.0, open/partial=0.4, open/broken=0.2, open/empty=0.1, open/none=0.0
- `ReproPenalty`: repro/match=0.0, repro/partial=0.4, repro/mismatch=1.0, repro/none=1.0, repro/unknown=0.7
- `NonReproScore = (1 - Openness) × ReproPenalty`
- `HeatWeightedScore = Heat × NonReproScore`

🔗 [返回主页](../README.md) | [查看所有 Issues](https://github.com/{repo}/issues?q=is%3Aissue+is%3Aopen+label%3Apaper%2Ftracking)
"""


def write_leaderboard(
    filename: str,
    title: str,
    description: str,
    entries: List[PaperEntry],
    sort_key,
    reverse: bool = True,
    repo: str = "",
):
    """生成并写入排行榜文件"""
    # 排序
    sorted_entries = sorted(entries, key=sort_key, reverse=reverse)
    
    # 生成内容
    content = generate_header(title, description)
    content += generate_table_header()
    
    for rank, entry in enumerate(sorted_entries, 1):
        content += generate_table_row(rank, entry)
    
    if not sorted_entries:
        content += "| - | 暂无数据 / No data yet | - | - | - | - | - | - |\n"
    
    content += generate_footer(repo)
    
    # 写入文件
    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 生成: {filepath} ({len(sorted_entries)} entries)")


# ============================================================================
# Main
# ============================================================================

def main():
    print("🏆 开了吗 / Open Lah? - Leaderboard 生成器")
    print("=" * 50)
    
    # 获取配置
    token = get_github_token()
    repo = get_repo()
    
    print(f"📍 仓库: {repo}")
    print(f"🔑 Token: {'已设置' if token else '未设置 (可能受 API 限制)'}")
    print()
    
    # 确保 docs 目录存在
    os.makedirs(DOCS_DIR, exist_ok=True)
    
    # 获取 issues
    print("📥 获取 Issues...")
    issues = fetch_issues(repo, token)
    print(f"   共获取 {len(issues)} 个 open issues")
    
    # 处理 issues
    entries = process_issues(issues)
    print(f"   其中 {len(entries)} 个是 paper/tracking")
    print()
    
    # 生成排行榜
    print("📊 生成排行榜...")
    
    # 1. NonRepro 排行榜（按不可复现分数降序）
    write_leaderboard(
        filename="leaderboard_nonrepro.md",
        title="📈 NonRepro Leaderboard / 不可复现排行榜",
        description="按不可复现分数 (NonReproScore) 排序，分数越高表示开源/复现状况越差",
        entries=entries,
        sort_key=lambda e: (e.nonrepro_score, e.heat),
        reverse=True,
        repo=repo,
    )
    
    # 2. HeatWeighted 排行榜（按热度加权分数降序）
    write_leaderboard(
        filename="leaderboard_heatweighted.md",
        title="🔥 HeatWeighted Leaderboard / 热度加权排行榜",
        description="按热度加权分数 (HeatWeightedScore) 排序，高热度但难复现的论文排名更高",
        entries=entries,
        sort_key=lambda e: (e.heat_weighted_score, e.heat),
        reverse=True,
        repo=repo,
    )
    
    # 3. Recent 排行榜（按更新时间降序）
    write_leaderboard(
        filename="leaderboard_recent.md",
        title="🕐 Recent Leaderboard / 最近更新排行榜",
        description="按最近更新时间排序，展示最新的跟踪记录",
        entries=entries,
        sort_key=lambda e: e.updated_at,
        reverse=True,
        repo=repo,
    )
    
    print()
    print("✅ 排行榜生成完成！")


if __name__ == "__main__":
    main()
