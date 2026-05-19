# 項目結構

```
AI_project/
│
├── frontend/                    # React 前端應用
│   ├── src/
│   │   ├── components/          # React 組件
│   │   │   ├── InputForm.jsx    # 房屋信息輸入表單
│   │   │   ├── WeightSettings.jsx  # 權重調整組件
│   │   │   └── ResultDisplay.jsx   # 結果展示組件
│   │   ├── App.jsx              # 主應用組件
│   │   ├── index.css            # Tailwind 樣式
│   │   └── main.jsx             # 入口文件
│   ├── index.html               # HTML 模板
│   ├── vite.config.js           # Vite 配置
│   ├── tailwind.config.js       # Tailwind 配置
│   ├── postcss.config.js        # PostCSS 配置
│   └── package.json             # Node 依賴
│
├── backend/                     # FastAPI 後端
│   ├── main.py                  # FastAPI 主應用
│   ├── database.py              # 數據庫配置和模型
│   ├── schemas.py               # Pydantic 數據驗證模型
│   ├── analysis.py              # 核心分析邏輯
│   ├── requirements.txt         # Python 依賴
│   ├── .env.example             # 環境變量示例
│   └── property_analysis.db     # SQLite 數據庫 (生成)
│
├── README.md                    # 項目文檔
├── .gitignore                   # Git 忽略文件
├── setup.sh                     # macOS/Linux 安裝腳本
├── setup.bat                    # Windows 安裝腳本
└── STRUCTURE.md                 # 本文件
```

## 文件說明

### 前端文件

- **App.jsx**: 主應用容器，管理狀態和路由
- **InputForm.jsx**: 房屋信息輸入表單，包含所有房屋屬性輸入字段
- **WeightSettings.jsx**: 權重調整面板，允許用戶自定義各項因素的重要程度
- **ResultDisplay.jsx**: 分析結果展示，包含價格區間、分數、周邊設施、相似案例等

### 後端文件

- **main.py**: FastAPI 應用，定義 API 端點
- **database.py**: SQLAlchemy 模型定義和數據庫連接
- **schemas.py**: Pydantic 數據驗證模型
- **analysis.py**: 核心分析算法，包括：
  - 地理編碼
  - 相似案例查找
  - 合理價格計算
  - 便利性評分
  - 綜合分數計算

## 數據流

```
用戶輸入 → 前端表單 → API 請求 → 後端分析 → 數據庫查詢 → 結果計算 → API 響應 → 結果展示
```

## 核心功能流程

### 1. 房屋信息輸入
用戶在前端表單中輸入房屋地址、開價、坪數等信息

### 2. 可選的權重調整
用戶可以選擇調整各項因素的重要程度（進階設定）

### 3. 後端分析
- 地址轉換為坐標
- 查詢相似成交案例
- 計算合理價格區間
- 分析周邊設施距離
- 評分各項因素
- 計算加權綜合分數

### 4. 結果展示
顯示分析結果、購買建議和相似案例

## 技術亮點

### 前端
- **Vite**: 快速的開發構建工具
- **React Hooks**: 函數式組件和狀態管理
- **TailwindCSS**: 實用優先的 CSS 框架
- **Axios**: HTTP 客戶端

### 後端
- **FastAPI**: 高性能的現代 Python Web 框架
- **SQLAlchemy**: ORM 數據庫映射
- **Pydantic**: 數據驗證和設置管理

## API 端點

### 分析端點
- **POST /analyze**: 分析房屋價格合理性

### 健康檢查
- **GET /health**: 服務器狀態檢查

### 根端點
- **GET /**: API 信息

## 環境配置

### 前端環境
- API 代理配置在 `vite.config.js` 中
- 自動代理 `/api/*` 到後端 `http://localhost:8000`

### 後端環境
- 數據庫 URL: `sqlite:///./property_analysis.db`
- CORS 允許所有來源

## 開發建議

1. **前端開發**: 使用 Vite 的熱模塊更新 (HMR) 進行快速迭代
2. **後端開發**: 使用 `--reload` 標誌自動重啟服務器
3. **數據庫**: 使用 SQLite 便於開發，生成數據庫時自動添加示例數據
4. **測試**: 可以直接在前端表單中測試各種房屋組合
