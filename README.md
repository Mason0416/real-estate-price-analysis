# 🏠 房屋價格合理性分析平台
### Real Estate Price Reasonableness Analysis Platform

[![Frontend License](https://img.shields.io/github/license/Mason0416/real-estate-price-analysis?color=blue)](LICENSE)
[![React](https://img.shields.io/badge/Frontend-React%20%7C%20Vite%20%7C%20Tailwind-blueviolet)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%7C%20SQLite%20%7C%20SQLAlchemy-green)](https://fastapi.tiangolo.com/)
[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-orange)](https://mason0416.github.io/real-estate-price-analysis/)

---

## 📌 專案簡介

房屋價格合理性分析平台是一個協助購屋者判斷**「當前房屋開價是否合理」**的智慧化決策輔助平台。

本專案的核心定位**並非預測未來房價走勢**，而是聚焦於**「購屋當下的價格合理性判斷」**。透過整合歷史實價登錄資料、周邊生活機能、相似成交案例以及使用者自訂權重，降低買賣雙方的資訊不對稱，協助消費者做出更明智的購屋決策。

### 💡 核心分析方向
* **是否值得購買**：綜合硬體指標與周邊機能，給出綜合評級指數。
* **是否價格偏高**：以同區域、同類型相似物件實價登錄為基礎，評估溢價程度。
* **是否應該議價**：依據開價偏離合理區間的比例，提供具體的議價指引。
* **是否有更高 CP 值選擇**：協助挖掘同價格帶或條件相近的成交市場基準。

---

## ✨ 核心功能

1. 🎯 **房價合理性分析**：精準評估房屋開價偏離市場中位數的百分比，輸出語意化評估等級。
2. 📊 **市場合理價格區間估算**：依據實價登錄計算出合理的價格波動範圍。
3. 💰 **建議自備款估算**：自動計算購屋所需之 30% 基本自備款，作為財務規劃參考。
4. 🏥 **周邊生活機能分析**：綜合評估捷運站、醫院、學校、公園等生活設施的便利度。
5. 🚇 **距離精確度量**：度量房屋至各重要設施的精確距離（公尺），計算對應評分。
6. 🔢 **五級評分系統**：將價格合理性、周邊機能、屋齡及樓層等指標轉化為直觀的 1~5 分評級。
7. ⚙️ **使用者自訂權重**：支持自訂各指標的重要性權重，系統在前端提交時自動進行比例轉換（Normalize）。
8. 🏢 **相似成交案例比對**：篩選出同類型、坪數與屋齡相近的歷史實價登錄案例。
9. 📱 **響應式網頁設計**：採用簡潔典雅的卡片式報告風格，完美適應手機與桌面版瀏覽器。
10. 🔌 **前後端分離架構**：前端基於 React & Vite 構建，後端提供極速的 FastAPI Restful API。

---

## 🏗️ 技術架構

* **前端 (Frontend)**:
  * React 18 & Vite
  * Tailwind CSS (客製化卡片式報告視覺設計)
* **後端 (Backend)**:
  * FastAPI (Python 異步高效 Web 框架)
  * SQLite (輕量級關聯式資料庫)
  * SQLAlchemy (ORM 資料庫操作)
* **部署 (Deployment)**:
  * 前端：GitHub Pages
  * 後端：Render

---

## 📁 專案架構

```bash
real-estate-price-analysis/
├── frontend/                  # React 前端專案
│   ├── src/
│   │   ├── components/        # UI 元件 (InputForm, ResultDisplay, WeightSettings 等)
│   │   ├── App.jsx            # 主程式邏輯
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── backend/                   # FastAPI 後端專案
│   ├── main.py                # 應用程式進入點與 API 路由
│   ├── analysis.py            # 核心合理性評估與評分運算邏輯
│   ├── database.py            # 資料庫連接與 TransactionRecord 宣告
│   ├── schemas.py             # Pydantic 資料驗證模型
│   ├── property_analysis.db   # SQLite 實價登錄資料庫
│   ├── requirements.txt       # Python 套件依賴清單
│   └── runtime.txt            # Python 運行版本設定
│
└── README.md                  # 專案說明文件
```

---

## 📊 評分機制

平台引入五級評分系統，所有維度（價格、機能、屬性）在後端均量化為 `20 / 40 / 60 / 80 / 100`，並由前端直觀映射至 `1~5分`。

### 1. 五級分映射關係
* **1 分 (20)**：很差 / 價格明顯偏高
* **2 分 (40)**：偏差 / 建議議價
* **3 分 (60)**：普通 / 略高
* **4 分 (80)**：不錯 / 合理
* **5 分 (100)**：很好 / 價格合理偏低 (非常推薦購買)

### 2. 生活機能距離評分規則 (🚇 捷運 / 🏥 醫院 / 🎓 學校 / 🌳 公園)
| 距離區間 | 機能得分 | 前端星級 |
| :--- | :---: | :---: |
| 距離 $\le$ 250m | 100 | ⭐⭐⭐⭐⭐ (5分) |
| 距離 $\le$ 500m | 80 | ⭐⭐⭐⭐ (4分) |
| 距離 $\le$ 1000m | 60 | ⭐⭐⭐ (3分) |
| 距離 $\le$ 1500m | 40 | ⭐⭐ (2分) |
| 距離 $>$ 1500m | 20 | ⭐ (1分) |

---

## 🚀 本地開發與運行

### 前端 (Frontend)
1. 進入前端目錄：
   ```bash
   cd frontend
   ```
2. 安裝套件：
   ```bash
   npm install
   ```
3. 啟動 Vite 開發伺服器：
   ```bash
   npm run dev
   ```

### 後端 (Backend)
1. 進入後端目錄：
   ```bash
   cd backend
   ```
2. 安裝 Python 套件：
   ```bash
   pip install -r requirements.txt
   ```
3. 運行 Uvicorn 服務：
   ```bash
   uvicorn main:app --reload
   ```

* API 互動式文件預設網址：`http://localhost:8000/docs`

---

## 🔌 API 規格說明

### 價格合理性評估
* **Endpoint**: `POST /analyze`
* **Content-Type**: `application/json`

#### Request Payload 範例
```json
{
  "address": "台北市大安區復興南路一段390號",
  "askingPrice": 1688,
  "area": 30,
  "age": 10,
  "buildingType": "電梯大樓",
  "floor": 5,
  "totalFloors": 12,
  "parking": "有",
  "layout": "2房1廳1衛",
  "weights": {
    "price": 20,
    "mrt": 20,
    "hospital": 20,
    "school": 20,
    "park": 20
  }
}
```

#### Response 範例
```json
{
  "asking_price": 1688,
  "reasonable_price_range": {
    "min": 1580,
    "max": 1720
  },
  "price_assessment": "合理",
  "weighted_score": 80,
  "nearby_facilities": {
    "mrt": {
      "distance": 180,
      "score": 100
    },
    "hospital": {
      "distance": 450,
      "score": 80
    },
    "school": {
      "distance": 800,
      "score": 60
    },
    "park": {
      "distance": 320,
      "score": 80
    }
  },
  "similar_cases": [
    {
      "address": "台北市大安區復興南路一段模擬案例一",
      "price": 1600,
      "area": 30,
      "age": 10,
      "transaction_date": "2024-01"
    }
  ],
  "recommendation": "這間房子各項條件都不錯，價格也在合理範圍內，可以考慮看房。"
}
```

---

## 🌐 線上部署

* **前端網址 (GitHub Pages)**: [https://mason0416.github.io/real-estate-price-analysis/](https://mason0416.github.io/real-estate-price-analysis/)
* **後端 API 網址 (Render)**: `https://<YOUR_RENDER_BACKEND_URL>.onrender.com`

---

## 🛠️ 未來發展規劃

1. 🔌 **串接真實實價登錄 API**：改以內政部實價登錄 API 替代模擬資料庫，提供即時的行情數據。
2. 🗺️ **地圖視覺化**：整合 Leaflet 或 Google Maps，在地圖上直觀標示標的物、成交案例與周邊生活設施。
3. 🏠 **附近替代物件推薦**：基於相似度演算法，推薦同區域中性價比 (CP 值) 更高的其他在售物件。
4. 🤖 **AI 智慧購屋建議**：結合 LLM 深入分析特定物件的優缺點，生成專屬購屋評估報告。
5. 📈 **更完整的房價特徵模型**：將格局朝向、建材結構、採光、公設比等更多變數納入計分模型。
6. 🧮 **房貸試算與負擔評估**：內建房貸本息攤還試算，並結合收支比分析買方的財務負擔能力。
7. 🎓 **學區與嫌惡設施分析**：增設優質學區加權功能，並主動標示周邊嫌惡設施距離。
