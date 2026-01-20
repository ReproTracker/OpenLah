#!/bin/bash
# ============================================================================
# 开了吗 / Open Lah? - Label 初始化脚本
# ============================================================================
#
# 使用说明 / Usage Instructions:
#
# 1. 安装 GitHub CLI (gh)
#    - macOS:   brew install gh
#    - Windows: winget install --id GitHub.cli
#    - Linux:   参考 https://github.com/cli/cli/blob/trunk/docs/install_linux.md
#
# 2. 登录 GitHub
#    gh auth login
#    (按提示选择 GitHub.com，推荐使用浏览器方式认证)
#
# 3. 进入仓库目录并运行脚本
#    cd your-repo
#    chmod +x scripts/init_labels.sh  # Linux/macOS 需要
#    ./scripts/init_labels.sh
#
# 4. 或者在 Windows PowerShell 中:
#    bash scripts/init_labels.sh
#
# ============================================================================

set -e

echo "🏷️  开了吗 / Open Lah? - 初始化 Labels..."
echo ""

# 检查 gh 是否安装
if ! command -v gh &> /dev/null; then
    echo "❌ 错误: 未找到 GitHub CLI (gh)"
    echo "   请先安装: https://cli.github.com/"
    exit 1
fi

# 检查是否已登录
if ! gh auth status &> /dev/null; then
    echo "❌ 错误: 请先登录 GitHub CLI"
    echo "   运行: gh auth login"
    exit 1
fi

# 检查是否在 git 仓库中
if ! git rev-parse --git-dir &> /dev/null; then
    echo "❌ 错误: 请在 git 仓库目录中运行此脚本"
    exit 1
fi

echo "📍 当前仓库: $(gh repo view --json nameWithOwner -q .nameWithOwner)"
echo ""

# 创建 label 的函数（如果已存在则跳过）
create_label() {
    local name="$1"
    local color="$2"
    local description="$3"
    
    if gh label create "$name" --color "$color" --description "$description" 2>/dev/null; then
        echo "✅ 创建: $name"
    else
        echo "⏭️  已存在: $name"
    fi
}

echo "=========================================="
echo "📂 创建 Issue 类型标签..."
echo "=========================================="
create_label "paper/tracking"    "0052CC" "论文跟踪 / Paper tracking issue"
create_label "topic/nomination"  "5319E7" "话题提名 / Topic nomination"

echo ""
echo "=========================================="
echo "📂 创建开源状态标签 (open/*)..."
echo "=========================================="
create_label "open/none"     "B60205" "未开源 / No code released"
create_label "open/empty"    "D93F0B" "空仓库 / Empty repository"
create_label "open/broken"   "E99695" "损坏开源 / Code exists but broken"
create_label "open/partial"  "FBCA04" "部分开源 / Partially open"
create_label "open/full"     "0E8A16" "完整开源 / Fully open-source"

echo ""
echo "=========================================="
echo "🔬 创建复现状态标签 (repro/*)..."
echo "=========================================="
create_label "repro/none"     "B60205" "无法尝试 / Cannot attempt reproduction"
create_label "repro/mismatch" "D93F0B" "无法复现 / Results don't match"
create_label "repro/partial"  "FBCA04" "部分复现 / Partially reproduced"
create_label "repro/match"    "0E8A16" "完全复现 / Fully reproduced"
create_label "repro/unknown"  "C5DEF5" "未知 / No reproduction attempts"

echo ""
echo "=========================================="
echo "🔥 创建热度标签 (heat/*)..."
echo "=========================================="
create_label "heat/1"  "BFD4F2" "普通论文 / Regular paper"
create_label "heat/2"  "FFA500" "热门论文 / Hot paper"
create_label "heat/3"  "FF0000" "顶流论文 / Top paper"

echo ""
echo "=========================================="
echo "🏷️ 创建问题标签 (tag/*)..."
echo "=========================================="
create_label "tag/no-weights"        "C2E0C6" "缺少预训练权重 / Missing weights"
create_label "tag/no-train-code"     "C2E0C6" "缺少训练代码 / Missing training code"
create_label "tag/bug-mismatch"      "FEF2C0" "代码有 bug / Code has bugs"
create_label "tag/data-missing"      "FEF2C0" "数据集不可获取 / Dataset unavailable"
create_label "tag/underdocumented"   "D4C5F9" "文档不足 / Insufficient docs"
create_label "tag/not-generalizable" "D4C5F9" "结果不可泛化 / Not generalizable"

echo ""
echo "=========================================="
echo "📋 创建状态标签 (status/*)..."
echo "=========================================="
create_label "status/needs-triage"  "EDEDED" "待验证 / Needs triage"
create_label "status/verified"      "0E8A16" "已验证 / Verified"
create_label "status/disputed"      "D93F0B" "有争议 / Disputed"

echo ""
echo "=========================================="
echo "✅ Labels 初始化完成！"
echo "=========================================="
echo ""
echo "你可以在 GitHub 仓库的 Issues > Labels 页面查看所有标签"
echo "URL: https://github.com/$(gh repo view --json nameWithOwner -q .nameWithOwner)/labels"
