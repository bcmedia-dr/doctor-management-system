# 🚀 部署檢查清單

## 部署前準備

### ✅ 檔案檢查
- [ ] app.py
- [ ] export.py
- [ ] init_db.py
- [ ] requirements.txt
- [ ] render.yaml
- [ ] templates/index.html
- [ ] README.md
- [ ] .gitignore

### ✅ GitHub 設定
- [ ] 已建立 GitHub repository
- [ ] 已將程式碼推送到 GitHub
- [ ] repository 為 public 或已授權 Render 訪問

### ✅ Render 設定
- [ ] 已註冊 Render 帳號
- [ ] 已連接 GitHub 帳號
- [ ] 已選擇 Blueprint 部署方式

## 部署步驟

### 1. GitHub 上傳
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的帳號/專案名稱.git
git push -u origin main
```

### 2. Render 部署
1. 登入 [Render.com](https://render.com)
2. 點選 "New +" → "Blueprint"
3. 選擇你的 GitHub repository
4. Render 會自動偵測 `render.yaml`
5. 點選 "Apply" 開始部署
6. 等待 5-10 分鐘

### 3. 初始化資料庫
部署完成後：
1. 進入 Render Dashboard
2. 點選你的服務
3. 點選 "Shell" 標籤
4. 執行：`python init_db.py`
5. 確認顯示：成功新增 8 筆範例醫師資料

### 4. 測試系統
- [ ] 訪問提供的網址（如：https://your-app.onrender.com）
- [ ] 測試登入（admin / admin123）
- [ ] 測試新增醫師
- [ ] 測試編輯醫師
- [ ] 測試刪除醫師（需主管權限）
- [ ] 測試搜尋功能
- [ ] 測試篩選功能
- [ ] 測試匯出 Excel

### 5. 安全設定
- [ ] 修改預設密碼（編輯 app.py）
- [ ] 修改 SECRET_KEY（編輯 app.py 第 7 行）
- [ ] 重新部署（git push）

### 6. 分享給團隊
- [ ] 將網址分享給團隊成員
- [ ] 提供登入帳密
- [ ] 說明使用規則（誰是主管、誰是一般用戶）

## 常見問題排除

### 問題 1：部署失敗
**檢查**：
- render.yaml 格式是否正確
- requirements.txt 是否完整
- GitHub repository 是否公開或已授權

### 問題 2：無法訪問網站
**檢查**：
- Render 服務是否顯示 "Live"
- 是否使用 HTTPS（不是 HTTP）
- 瀏覽器快取（嘗試無痕模式）

### 問題 3：登入失敗
**檢查**：
- 帳號密碼是否正確
- 是否已初始化資料庫
- 瀏覽器 Cookie 是否啟用

### 問題 4：資料無法儲存
**檢查**：
- 資料庫是否成功建立
- Render Logs 中是否有錯誤訊息
- 嘗試重啟服務

### 問題 5：匯出 Excel 失敗
**檢查**：
- openpyxl 是否正確安裝
- 是否有權限訪問 /tmp 目錄
- 檢查 Render Logs

## 維護建議

### 定期備份
- 每週匯出 Excel 備份一次
- 儲存在 Google Drive 或其他雲端空間

### 監控使用狀況
- 定期檢查 Render Dashboard
- 注意免費額度使用量（750 小時/月）
- 超過額度系統會自動休眠

### 更新系統
如需更新功能：
1. 在本地修改程式碼
2. git add .
3. git commit -m "更新說明"
4. git push
5. Render 會自動重新部署

## 🎉 部署成功！

恭喜！你的醫師管理系統已成功部署到雲端。

**下一步**：
1. 修改預設密碼
2. 測試所有功能
3. 培訓團隊成員使用
4. 開始錄入真實資料

**網址範例**：
```
https://doctor-management-system-xxxx.onrender.com
```

把這個網址加入書籤，方便日後使用！
