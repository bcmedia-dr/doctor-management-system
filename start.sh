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
echo "📝 預設帳號："
echo "   管理員 - 帳號: admin  密碼: admin123"
echo "   一般用戶 - 帳號: user   密碼: user123"
echo ""
echo "按 Ctrl+C 停止系統"
echo "========================"

python3 app.py
