# 房屋價格合理性分析平台 MVP

一個幫助購屋者判斷房屋開價是否合理的 AI 分析平台。

## 核心功能

✅ 輸入房屋資訊（地址、開價、坪數、屋齡、建物型態、樓層、車位等）  
✅ 預設或自訂購屋因素權重  
✅ 查詢相似房屋成交案例  
✅ 計算合理價格區間  
✅ 分析周邊環境（捷運、醫院、學校、公園距離）  
✅ 生成綜合合理性分數  
✅ 提供購買建議

## 技術棧

**Frontend:**
- React 18
- Vite
- TailwindCSS

**Backend:**
- FastAPI
- SQLAlchemy
- SQLite

## 快速開始

### 前置需求

- Node.js 18+
- Python 3.9+
- npm 或 yarn

### 安裝與運行

#### 1. 後端設置

```bash
# 進入後端目錄
cd backend

# 創建虛擬環境
python -m venv venv

# 啟動虛擬環境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 運行後端服務 (localhost:8000)
uvicorn main:app --reload
```

#### 2. 前端設置

在新的終端視窗中：

```bash
# 進入前端目錄
cd frontend

# 安裝依賴
npm install

# 運行開發服務器 (localhost:5173)
npm run dev
```

### 訪問應用

打開瀏覽器訪問 `http://localhost:5173`

## 使用流程

1. 輸入目標房屋資訊
2. （可選）點擊「進階設定」調整各項因素的重要程度
3. 點擊「開始分析」
4. 查看分析結果，包括：
   - 合理價格區間
   - 價格合理性評估
   - 周邊生活機能評分
   - 相似成交案例
   - 綜合合理性分數
   - 購買建議

## API 端點

### POST /analyze

分析房屋價格合理性

**請求參數：**
```json
{
  "address": "台北市信義區光復路",
  "askingPrice": 1000,
  "area": 35,
  "age": 8,
  "buildingType": "building",
  "floor": 8,
  "totalFloors": 12,
  "parking": "yes",
  "layout": "3房2廳1衛",
  "weights": {
    "price": 30,
    "mrt": 20,
    "hospital": 10,
    "school": 15,
    "park": 10,
    "age": 10,
    "area": 0,
    "floor": 0,
    "parking": 5
  }
}
```

**響應範例：**
```json
{
  "asking_price": 1000,
  "reasonable_price_range": {
    "min": 1100,
    "max": 1200
  },
  "price_assessment": "價格合理",
  "weighted_score": 75.5,
  "nearby_facilities": {
    "mrt": {"distance": 450, "rating": "便利"},
    "hospital": {"distance": 650, "rating": "便利"},
    "school": {"distance": 300, "rating": "非常便利"},
    "park": {"distance": 500, "rating": "便利"}
  },
  "similar_cases": [...],
  "recommendation": "這間房子各項條件都不錯，價格也很合理，值得認真考慮。"
}
```

## 數據說明

### 相似案例篩選條件

- **地理位置：** 同區優先
- **建物型態：** 必須相同
- **坪數：** ±20% 範圍內
- **屋齡：** ±5 年範圍內
- **成交時間：** 近期數據優先

### 評分標準

- **價格合理性：** 與中位數單價的差距
- **設施便利性：** 根據距離判斷
- **屋況分數：** 基於屋齡和樓層位置
- **綜合分數：** 根據用戶設置的權重計算

## 目錄結構

```
/
├── frontend/              # React 前端應用
│   ├── src/
│   │   ├── components/    # React 組件
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
├── backend/               # FastAPI 後端
│   ├── main.py            # 主應用
│   ├── database.py        # 數據庫配置
│   ├── schemas.py         # Pydantic 模型
│   ├── analysis.py        # 核心分析邏輯
│   └── requirements.txt
└── README.md
```

## MVP 限制

⚠️ 當前不包含以下功能：
- 登入系統
- 房屋推薦
- 房價預測
- 投資報酬預測
- 地圖展示
- 收藏/保存功能
- 真實房地產數據（使用模擬數據）

## 未來改進

- 集成真實實價登錄數據
- 更精確的地理位置計算
- 機器學習模型優化價格估算
- 用戶賬戶系統
- 房屋對比功能
- 市場趨勢分析

## 常見問題

**Q: 相似案例不足怎麼辦？**  
A: 確認房屋資訊輸入無誤，特別是建物型態和區域。在現有數據庫中，請盡量選擇台北市中心位置。

**Q: 分數如何計算？**  
A: 綜合分數是各項評分按照用戶設置的權重加權平均，滿分 100。

**Q: 可以預測未來房價嗎？**  
A: 不行。本平台只分析當前開價是否合理，不做任何房價預測。

## 許可證

MIT
