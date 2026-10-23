# Home Device Platform 居家設備監控平台

一個可擴充的居家設備監控與控制平台。後端定時讀取各裝置的感測資料，套用控制規則，並記錄遙測與事件；前端提供適合手機操作的儀表板，可以查看狀態並手動控制。

第一個支援的裝置是**自動抽水機**：用上下兩個浮球開關偵測水位，水位高時啟動抽水，降到低水位時停止。

> 狀態：開發中。目前以模擬裝置（Mock driver）開發，尚未接上實體硬體。

## 功能（第一階段）

- 抽水機自動控制：上下水位之間有緩衝區間，避免馬達頻繁啟停。
- 安全保護：超過最長連續運轉時間就強制停機並鎖定；兩個浮球的訊號互相矛盾時發出警報。
- 手動模式：可以從網頁直接啟動或停止抽水機。
- 資料記錄：保存遙測資料與事件，並在詳細頁用圖表呈現。
- 裝置註冊表：新增其他裝置類型時，不需要改動既有的裝置程式碼。

## 架構

```
home-device-platform/
├── backend/    # FastAPI REST API、SQLite 資料庫、背景輪詢與控制邏輯
├── frontend/   # React + TypeScript + Vite 儀表板
└── device/     # 硬體抽象層：Driver 介面與各裝置實作（Mock、GPIO、Modbus）
```

| 模組 | 職責 |
|---|---|
| `backend/` | 提供 REST API；背景輪詢器定時向 driver 讀取資料、套用控制規則、寫入 SQLite |
| `frontend/` | 總覽頁與裝置詳細頁，定時向 API 取得最新狀態 |
| `device/` | 定義統一的 Driver 介面，上層只需要「讀取遙測」與「下達指令」，不需要知道底層是模擬、GPIO 還是 Modbus RTU |

`device/` 是可獨立安裝的 Python 套件，`backend/` 直接 import 使用。

## 技術棧

- **後端**：Python、FastAPI、SQLAlchemy 2、SQLite、pydantic-settings、pytest
- **前端**：React 19、TypeScript、Vite、CSS Modules、Recharts
- **硬體（規劃中）**：Raspberry Pi、浮球開關、GPIO 繼電器，之後改用 Modbus RTU（RS-485）繼電器

## 設定

複製範例設定檔，再依需要修改：

```bash
cp .env.example .env
```

`.env` 不納入版本控制；`.env.example` 只有範例值，不含任何密鑰。

| 變數 | 說明 | 預設值 |
|---|---|---|
| `BACKEND_HOST` / `BACKEND_PORT` | 後端監聽位址與埠號 | `127.0.0.1` / `8741` |
| `FRONTEND_PORT` | 前端開發伺服器埠號 | `5174` |
| `CORS_ORIGINS` | 允許的前端來源 | `http://127.0.0.1:5174,http://localhost:5174` |
| `DATABASE_URL` | SQLite 路徑 | `sqlite:///./home_device.db` |
| `POLL_INTERVAL_SECONDS` | 背景輪詢間隔（秒） | `2` |
| `MAX_RUN_SECONDS` | 抽水機最長連續運轉秒數 | `600` |

安裝與啟動方式會在前後端完成後補上。

## Roadmap

- [ ] 第一階段：模擬抽水機，跑通「讀取感測 → 控制邏輯 → 儲存資料 → 網頁監控」完整流程
- [ ] 第二階段：接上 Raspberry Pi、浮球開關與 GPIO 繼電器，完成實體杯水抽水展示
- [ ] 第三階段：改用 Modbus RTU（RS-485）繼電器
- [ ] 之後：Telegram 警報通知、更多裝置類型（例如淹水偵測、自動澆花）