# 🎉 MVP 設置完成指南

## 已解決的問題

✅ PostCSS/Tailwind 配置已更正為 ES Module 格式  
✅ 前端 Vite 開發服務器已驗證正常運行  
✅ 所有必需的配置文件已創建  

## 立即開始 (3 步驟)

### 第 1 步：檢查環境

```bash
cd /Users/mason/AI_project
chmod +x check-env.sh
./check-env.sh
```

需要的版本：
- Node.js 18+
- npm 8+
- Python 3.9+
- pip 20+

### 第 2 步：安裝依賴

```bash
# 自動安裝 (推薦)
chmod +x setup.sh
./setup.sh

# 或手動安裝
# 後端
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 前端 (新終端)
cd frontend
npm install
```

### 第 3 步：啟動應用

**終端 1 - 後端服務器：**
```bash
cd /Users/mason/AI_project/backend
source venv/bin/activate
uvicorn main:app --reload
```

你應該看到：
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**終端 2 - 前端開發服務器：**
```bash
cd /Users/mason/AI_project/frontend
npm run dev
```

你應該看到：
```
VITE v5.x.x  ready in XXX ms
➜  Local:   http://localhost:5173/
```

**終端 3 - 打開瀏覽器：**
```bash
# 訪問應用
http://localhost:5173
```

## 應用已就緒 ✨

### 主要頁面
- **房屋信息輸入表單** - 在左側，輸入地址、開價、坪數等
- **分析結果** - 在右側，顯示合理價格、分數、建議等
- **進階設定** - 點擊按鈕調整各項因素的權重

### 測試用例

試試以下地址組合：

**案例 1 - 信義區電梯大樓**
```
地址: 台北市信義區光復路
開價: 1200 萬元
坪數: 35 坪
屋齡: 8 年
建物類型: 電梯大樓
樓層: 8 / 總層: 12
車位: 有
```

**案例 2 - 大安區公寓**
```
地址: 台北市大安區大安路
開價: 950 萬元
坪數: 30 坪
屋齡: 12 年
建物類型: 公寓
樓層: 3 / 總層: 5
車位: 無
```

## 功能演示

### 基礎分析流程
1. 填寫房屋信息
2. 點擊「開始分析」
3. 查看結果

### 權重自定義
1. 點擊「進階設定」
2. 調整各項因素的權重百分比
3. 權重總和應為 100%
4. 提交分析查看加權結果

## 項目文件位置

| 文件 | 用途 |
|------|------|
| `frontend/src/App.jsx` | 主應用 |
| `backend/main.py` | API 伺服器 |
| `backend/analysis.py` | 分析邏輯 |
| `README.md` | 完整文檔 |
| `STRUCTURE.md` | 項目結構 |
| `QUICKSTART.md` | 快速開始 |

## API 端點

### 分析房屋
**POST** `http://localhost:8000/analyze`

請求範例：
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "address": "台北市信義區光復路",
    "askingPrice": 1200,
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
  }'
```

### 健康檢查
**GET** `http://localhost:8000/health`

## 疑難排解

### 問題：Port 5173 已被占用

```bash
# macOS/Linux - 找到佔用 5173 的進程
lsof -i :5173
# 或
pkill -f vite

# 或改用其他 port
cd frontend
npm run dev -- --port 3000
```

### 問題：Port 8000 已被占用

```bash
# macOS/Linux - 找到佔用 8000 的進程
lsof -i :8000
# 或改用其他 port
uvicorn main:app --reload --port 8001
```

### 問題：找不到相似案例

- 確認地址包含正確的台北市區名（信義、大安等）
- 確保坪數在 25-50 之間
- 確保屋齡在 5-15 年之間

### 問題：API 連接失敗

- 檢查後端是否在運行
- 檢查 CORS 是否已啟用 (已預設啟用)
- 確認 API URL 正確 (`http://localhost:8000`)

## 下一步

✅ 應用已運行，現在可以：

1. **測試功能**
   - 試試各種房屋組合
   - 調整權重觀察結果變化
   - 檢查相似案例的合理性

2. **探索代碼**
   - `backend/analysis.py` - 理解分析邏輯
   - `frontend/src/components/` - 查看前端組件
   - `backend/database.py` - 了解數據結構

3. **擴展功能**
   - 添加更多房屋數據到數據庫
   - 修改評分算法
   - 增加更多分析維度

## 獲得幫助

查看詳細文檔：
- `README.md` - 完整功能說明
- `STRUCTURE.md` - 代碼組織說明
- `QUICKSTART.md` - 快速參考

## 重要提醒

⚠️ 當前 MVP 限制：
- 使用模擬數據，非真實房地產交易數據
- 地理位置計算使用模擬值
- 相似案例基於簡單規則匹配
- 不涉及房價預測或投資建議

🚀 生產就緒版本會包括：
- 真實實價登錄數據
- 真實地理編碼 API
- 機器學習模型
- 用戶認證和數據持久化

---

**祝你使用愉快！** 🏠📊
