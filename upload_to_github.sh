#!/bin/bash

# GitHub上传脚本

echo "🚀 准备上传到GitHub..."
echo ""

# 检查是否已初始化Git
if [ ! -d ".git" ]; then
    echo "📦 初始化Git仓库..."
    git init
fi

# 检查是否有远程仓库
if ! git remote | grep -q origin; then
    echo ""
    echo "⚠️  尚未设置GitHub远程仓库"
    echo ""
    read -p "请输入你的GitHub仓库地址 (例如: https://github.com/用户名/仓库名.git): " repo_url
    
    if [ -z "$repo_url" ]; then
        echo "❌ 未输入仓库地址，退出"
        exit 1
    fi
    
    git remote add origin "$repo_url"
    echo "✅ 已添加远程仓库: $repo_url"
fi

echo ""
echo "📝 添加文件到Git..."
git add .

echo ""
echo "💾 提交更改..."
read -p "请输入提交信息 (直接回车使用默认): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Update: 医师管理系统"
fi

git commit -m "$commit_msg"

echo ""
echo "📤 推送到GitHub..."
echo "   如果这是第一次推送，可能需要设置分支..."
git branch -M main 2>/dev/null
git push -u origin main

echo ""
echo "✅ 完成！"
echo ""
echo "📋 下一步："
echo "   1. 访问 https://render.com"
echo "   2. 登录并点击 'New +' → 'Blueprint'"
echo "   3. 选择你的GitHub仓库"
echo "   4. Render会自动检测render.yaml并开始部署"
echo ""
echo "   详细说明请查看: GITHUB_DEPLOY.md"
