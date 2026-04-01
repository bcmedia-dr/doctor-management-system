# CLAUDE.md

此檔案為 Claude Code (claude.ai/code) 在此專案中操作時的指引文件。

## 專案概述

這是一個**醫師管理系統** — 以 Flask 為基礎的網頁應用程式，用於管理醫師聯絡資訊、科別、合作狀態與社群媒體資訊。設計供 5 人小型團隊協作使用，具備角色權限控制與雲端部署支援。

**主要功能：**
- 醫師 CRUD 操作（新增、查詢、編輯、刪除，刪除限管理員）
- 角色權限：管理員（可刪除）vs 一般使用者（唯讀／可寫）
- Excel 匯出／匯入功能
- 響應式 Bootstrap 5 介面
- 本地 SQLite 或雲端 PostgreSQL 資料庫支援
- 已包含 Render.com 部署設定

## ⚠️ 最重要規則（每次都要遵守）

### 此專案只能操作 `doctor` table，絕對不能動診所系統的資料

雲端 PostgreSQL（`doctor-db`）被**兩個系統共用**：

| 系統 | Repo | 可操作的 table |
|------|------|---------------|
| 醫師管理系統（本專案） | `bcmedia-dr/doctor-management-system` | `doctor` |
| 診所管理系統 | `bcmedia-dr/clinic-management-system` | `clinic`、`health_mall`、`campaign`、`campaign_clinic`、`baiwei_doctor`、`audit_log` |

**禁止事項：**
- 不能對 `clinic`、`health_mall`、`campaign`、`campaign_clinic`、`baiwei_doctor`、`audit_log` 做任何 SELECT / INSERT / UPDATE / DELETE
- 不能執行 `db.drop_all()`（會清空所有 table，包含診所資料）
- 不能修改 `doctor` table 的 schema 而不同步通知診所系統

---

## 快速啟動

### 本地開發

```bash
# 安裝相依套件
pip install -r requirements.txt

# 初始化資料庫（含範例資料）
python init_db.py

# 啟動開發伺服器
python app.py
# 網址：http://localhost:8080
```

### 使用 start.sh（macOS/Linux）
```bash
./start.sh
```

## 技術架構

- **後端：** Flask 3.0.0 + Flask-SQLAlchemy ORM
- **資料庫：** 本地 SQLite（`instance/doctors.db`），生產環境 PostgreSQL
- **前端：** Bootstrap 5.3.0 + 原生 JavaScript（無框架）
- **部署：** Render.com（設定檔 `render.yaml`）
- **Excel 匯出：** openpyxl 3.1.2

## 系統架構

### 資料庫模型（`app.py`）
單一 `Doctor` 模型，欄位如下：
- 基本資訊：`name`、`email`、`specialty`、`gender`、`status`
- 合作資訊：`contact_person`、`current_brand`、`price_range`
- 社群媒體：`has_social_media`、`social_media_link`
- 時間戳記：`created_at`、`updated_at`

> **重要：** `name` 與 `email` 目前在業務邏輯上儲存同一個值（醫師名稱）。前端表格顯示優先用 `email`，編輯 modal 填入優先用 `name`，兩者優先順序相反，是已知的設計問題。搜尋功能（後端）只查 `email` 欄位。

### 身份驗證
簡易 session 驗證，帳號密碼寫死在 [app.py:74-85](app.py#L74-L85)：
- 管理員：帳號 `admin`
- 一般用戶：帳號 `user`
- 裝飾器 `@admin_required` 保護刪除等敏感路由

⚠️ **注意：** 帳號密碼為明文寫死。修改請直接編輯 [app.py:74-85](app.py#L74-L85) 後重新部署。

### 檔案結構
```
.
├── app.py                 # Flask 主程式、DB 模型、API 路由
├── init_db.py            # 資料庫初始化（含範例資料）
├── export.py             # Excel 匯出工具（openpyxl）
├── import_data.py        # Excel 匯入邏輯
├── migrate_db.py         # 手動執行的 schema 遷移腳本
├── requirements.txt      # Python 相依套件
├── render.yaml           # Render.com 雲端部署設定
├── templates/
│   └── index.html        # 單頁應用（含內嵌 CSS/JS）
└── instance/
    └── doctors.db        # 本地 SQLite 資料庫（初始化後產生）
```

### API 路由
全部定義於 `app.py`：
- `GET /` — 提供 index.html
- `POST /login` — Session 登入驗證
- `POST /logout` — 清除 session
- `GET /check_auth` — 確認目前登入狀態
- `GET /api/doctors` — 列出所有醫師（支援篩選：`search`、`specialty`、`status`、`gender`）
- `POST /api/doctors` — 新增醫師（任何已登入使用者）
- `PUT /api/doctors/<id>` — 更新醫師（任何已登入使用者）
- `DELETE /api/doctors/<id>` — 刪除醫師（限管理員，需 `@admin_required`）
- `GET /api/stats` — 儀表板統計數據
- `GET /api/export` — 產生 Excel 匯出（透過 `send_file` 回傳檔案）
- `POST /api/import` — 從上傳的 Excel 批量匯入醫師

### 前端（單頁應用）
`templates/index.html` 是完整的單頁應用：
- 登入 modal（JavaScript session 處理）
- 統計儀表板卡片
- 醫師列表含即時搜尋／篩選
- 編輯 modal（CRUD 操作）
- Excel 匯出／匯入按鈕
- 無需建置步驟，由 Flask 直接提供

## 資料庫操作

### 初始化資料庫
```bash
python init_db.py
```
建立資料表並填入 8 筆範例資料。可重複執行（會先檢查資料是否已存在）。

### 重置資料庫
```bash
python reset_db.py  # 刪除所有資料並重建 schema
```

### 修改資料庫 Schema
1. 更新 `app.py` 中的 `Doctor` model
2. 刪除 `instance/doctors.db`
3. 重新執行 `python init_db.py`

**注意：** 雲端部署時需另外處理 migration（目前未設定 migration 工具）。`migrate_db.py` 為手動執行腳本，**勿放入啟動流程**，以免誤觸 `drop_all()` 清空生產資料。

## 重要說明

### 帳號管理
- **帳號密碼寫死於 [app.py:74-85](app.py#L74-L85)**
- 雲端部署前必須修改
- 目前無使用者資料表
- 任何帳號變更都需重新建置／部署

### 資料匯出格式
`export.py` 產生的 Excel 格式：
- 標題列（藍底白字，凍結首列）
- 欄位順序：醫師、科別、性別、狀態、聯絡窗口、合作品牌、報價區間、經營社群、醫師社群
- 支援 UTF-8，欄寬已調整

### 生產環境部署（Render）
- 資料庫網址透過環境變數 `DATABASE_URL` 注入
- Python 版本 3.11，定義於 `render.yaml`
- 免費方案每月 750 小時（5 人小團隊足夠）
- 首次部署後需在 Render Shell 手動執行 `python init_db.py`

## 常見任務

### 新增 Doctor model 欄位
1. 在 `app.py` 的 `Doctor` class 新增欄位
2. 更新同檔案的 `to_dict()` 方法
3. 在 `templates/index.html` 表單區塊新增欄位
4. 在 `templates/index.html` 表格區塊新增欄位
5. 若需出現在 Excel，更新 `export.py`
6. 重新初始化：`rm instance/doctors.db && python init_db.py`

### 修改帳號密碼
編輯 [app.py:74-85](app.py#L74-L85)（`/login` 路由）直接改寫帳號密碼。

### 自訂科別選項
編輯 `templates/index.html` 的兩個位置：
- 篩選下拉選單（約第 127 行）
- 新增／編輯表單下拉選單（約第 237 行）

### 除錯資料庫
```bash
python -c "from app import app, db, Doctor; \
  app.app_context().push(); \
  print(Doctor.query.all())"
```

## 測試方式
目前無自動化測試，手動測試流程：
- 執行 `python app.py` 後開啟 http://localhost:8080
- 用管理員帳號登入（應出現刪除按鈕）
- 用一般用戶登入（不應出現刪除按鈕）
- 確認篩選／搜尋功能正常
- 測試 Excel 匯出下載

## Git Push 方式

Remote URL 已內嵌 PAT，可直接執行，無需互動輸入帳密：

```bash
git add . && git commit -m "說明" && git push
```

- **此專案 repo：** `bcmedia-dr/doctor-management-system`
- **勿與診所系統混淆：** `bcmedia-dr/clinic-management-system` 是另一個獨立專案
- Push 成功後 Render 會自動偵測並部署（約 3–5 分鐘）

## 部署清單
- [ ] 修改 [app.py:74-85](app.py#L74-L85) 的管理員／用戶密碼
- [ ] 本地測試 `python app.py`
- [ ] `git add . && git commit -m "說明" && git push`
- [ ] 連結 repo 至 Render.com
- [ ] 首次部署後在 Render Shell 執行 `python init_db.py`
- [ ] 在 Render 儀表板確認資料庫連線正常

## 安全注意事項
- 帳號密碼明文存在版本控制（上線前必須處理）
- 簡易 session 驗證（目前未強制 HTTPS）
- 醫師欄位無輸入驗證
- 若實作多用戶系統，應加入密碼雜湊（bcrypt）
