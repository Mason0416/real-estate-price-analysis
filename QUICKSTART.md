# ⚡ 快速開始指南

## 5 分鐘內啟動應用

### macOS/Linux

```bash
# 1. 進入項目目錄
cd /Users/mason/AI_project

# 2. 運行自動安裝腳本
chmod +x setup.sh
./setup.sh

# 3. 啟動後端 (終端 1)
cd backend
source venv/bin/activate
uvicorn main:app --reload

# 4. 啟動前端 (終端 2)
cd frontend
npm run dev

# 5. 打開瀏覽器
# 訪問 http://localhost:5173
```

### Windows

```cmd
# 1. 進入項目目錄
cd C:\path\to\AI_project

# 2. 運行自動安裝腳本
setup.bat

# 3. 啟動後端 (終端 1)
cd backend
venv\Scripts\activate
uvicorn main:app --reload

# 4. 啟動前端 (終端 2)
cd frontend
npm run dev

# 5. 打開瀏覽器
# 訪問 http://localhost:5173
```

## 手動安裝 (如果自動腳本失敗)

### 後端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

pip install -r requirements.txt
uvicorn main:app --reload
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 使用應用

1. **輸入房屋信息**
   - 地址、開價、坪數、屋齡、建物類型等

2. **可選：調整權重**
   - 點擊「進階設定」按鈕
   - 使用滑桿調整各項因素的重要程度

3. **點擊「開始分析」**
   - 系統會查詢相似案例
   - 計算合理價格區間
   - 分析周邊環境
   - 生成綜合分數

4. **查看結果**
   - 價格合理性評估
   - 周邊生活機能
   - 相似成交案例
   - 購買建議

## 測試數據

系統已預加載台北市範例數據：
- 信義區：3 套電梯大樓
- 大安區：2 套公寓

試試以下地址：
- `台北市信義區光復路` - 34-40 坪
- `台北市大安區大安路` - 30-32 坪

## 常見問題

**Q: 看到 "找不到相似的成交案例" 錯誤？**  
A: 確認輸入的地址包含正確的區名（信義、大安等），並確保坪數和屋齡在合理範圍內。

**Q: 後端無法啟動？**  
A: 檢查 Python 版本 (3.9+)，確保虛擬環境已激活。

**Q: 前端無法加載？**  
A: 檢查 Node.js 版本 (18+) 和 npm 是否已安裝。

**Q: API 連接失敗？**  
A: 確保後端在 `http://localhost:8000` 上運行。

## 文件位置

| 文件 | 位置 |
|------|------|
| 前端主應用 | `frontend/src/App.jsx` |
| 後端主應用 | `backend/main.py` |
| 核心分析邏輯 | `backend/analysis.py` |
| 數據庫配置 | `backend/database.py` |
| 組件列表 | `frontend/src/components/` |

## 下一步

✅ 應用成功運行後，可以：

1. 測試不同的房屋條件組合
2. 調整權重看分數如何變化
3. 查看相似案例與開價的關係
4. 理解價格合理性的判斷邏輯

🔧 如需修改或擴展功能：

1. 查看 `STRUCTURE.md` 了解項目結構
2. 檢查 `backend/analysis.py` 的計算邏輯
3. 根據需要修改前端組件或後端算法

📚 更多信息見 `README.md`
