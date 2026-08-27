#!/bin/bash

echo "🚀 醫師管理系統啟動腳本"
echo "========================"

# 檢查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 找不到 Python3，請先安裝"
    exit 1
fi

# 安裝套件
echo "📦 安裝套件..."
pip install -r requirements.txt

# 初始化資料庫
echo "🗄️ 初始化資料庫..."
python3 init_db.py

# 啟動應用
echo "✅ 啟動系統..."
echo ""
echo "🌐 開啟瀏覽器訪問：http://localhost:8080"
echo ""
echo "📝 登入帳號：admin / user"
echo "   密碼請使用 ADMIN_PASSWORD / USER_PASSWORD 環境變數設定"
echo ""
echo "按 Ctrl+C 停止系統"
echo "========================"

python3 app.py
