# 🏠 AI 房屋價格合理性分析平台

> 結合 AI 與實價登錄資料的房屋價格合理性分析平台，協助購屋者做出更好的決策。

---

# 🌐 線上展示

前端網站：

https://mason0416.github.io/real-estate-price-analysis/

後端 API 文件：

https://YOUR_RENDER_BACKEND.onrender.com/docs

---

# 📌 專案介紹

本專案是一個 AI 房屋價格合理性分析平台，目標是協助正在看房、準備購屋的使用者，快速判斷房屋開價是否合理。

本系統不預測未來房價，而是聚焦於：

> 「這間房子現在這個價格是否值得購買？」

系統會分析：

- Taiwan real estate transaction records (實價登錄)
- House attributes
- Nearby facilities and accessibility
- User preference weights

並輸出：

- Reasonable price range
- Price fairness analysis
- Weighted house score
- Final buying suggestion

---

# ✨ 主要功能

## 🔍 房屋價格合理性分析

使用者可輸入：

- Address
- Asking price
- Area (坪數)
- Building age
- Building type
- Floor information
- Parking information

系統分析：

- Reasonable market price
- Whether the house is overpriced
- Whether negotiation is recommended
- Buying suggestions

---

## 🏙️ 周邊生活機能分析

系統會分析：

- MRT distance
- Hospital distance
- School distance
- Park distance

and evaluates overall convenience.

---

## 📊 相似成交案例比較

系統會根據以下條件搜尋相似成交案例：

- Location
- Area
- Building age
- Building type
- Floor

using Taiwan real estate transaction data.

---

## ⚖️ 權重調整系統

使用者可以：

- Use default equal weights
- Or customize preference weights

Example adjustable weights:

- Price
- MRT accessibility
- School distance
- Building age
- Parking
- Park accessibility

系統會根據使用者偏好重新計算綜合合理性分數。

---

# 🧠 系統定位

本系統不是：

❌ House price prediction AI  
❌ Investment return prediction system  
❌ Real estate market forecasting tool

本系統是：

✅ Home buying decision assistant  
✅ House price fairness analysis platform  
✅ Real-time buying support system

---

# 🏗️ 技術架構

## Frontend

- React
- Vite
- TailwindCSS

---

## Backend

- FastAPI
- Python

---

## Database

- SQLite
- SQLAlchemy ORM

---

## Deployment

### Frontend

- GitHub Pages

### Backend

- Render

---

# 📁 專案結構

```bash
project/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── requirements.txt
│   ├── runtime.txt
│   └── property_analysis.db
│
└── README.md
```

---

# 🚀 本地開發

## Clone 專案

```bash
git clone https://github.com/Mason0416/real-estate-price-analysis.git
cd real-estate-price-analysis
```

---

# 🚀 前端啟動

```bash
cd frontend
npm install
npm run dev
```

前端預設：

```bash
http://localhost:5173
```

---

# 🚀 後端啟動

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

後端預設：

```bash
http://localhost:8000
```

API 文件：

```bash
http://localhost:8000/docs
```

---

# 🌐 GitHub Pages 部署

## vite.config.js

```js
export default defineConfig({
  plugins: [react()],
  base: '/real-estate-price-analysis/',
})
```

---

## 部署前端

```bash
cd frontend
npm run build
npm run deploy
```

---

# ☁️ Render 後端部署

## Render 設定

### Root Directory

```bash
backend
```

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## runtime.txt

```txt
python-3.11.9
```

---

# 🔌 API 串接

## frontend/.env.production

```env
VITE_API_URL=https://YOUR_RENDER_BACKEND.onrender.com
```

---

## Frontend API Example

```js
const API_URL =
  import.meta.env.VITE_API_URL || 'http://localhost:8000';

const response = await fetch(`${API_URL}/analyze`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(payload),
});
```

---

# 📊 分析流程

```text
使用者輸入房屋資訊
        ↓
地址轉換為經緯度
        ↓
搜尋相似實價登錄資料
        ↓
計算合理價格區間
        ↓
分析周邊生活機能
        ↓
套用使用者權重
        ↓
輸出購屋建議
```

---

# 📌 價格判斷邏輯

```text
低於合理價格 5% → 價格偏低
合理價格 ±5% → 價格合理
高於合理價格 5~10% → 略高
高於合理價格 10% 以上 → 明顯偏高
```

---

# 🛠️ 未來功能

- Real-time transaction data updates
- Interactive maps
- House recommendation engine
- User authentication
- AI chat analysis
- PostgreSQL + PostGIS
- Advanced similarity algorithms

---

# 👨‍💻 作者

魏宇浩  
政治大學資訊科學系

---

# 📄 授權

MIT License

