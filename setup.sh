#!/bin/bash

echo "🏠 房屋價格合理性分析平台 - 安裝腳本"
echo "=========================================="
echo ""

# 設置後端
echo "📦 設置後端..."
cd backend

# 檢查 Python 版本
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ 使用 Python $python_version"

# 創建虛擬環境
if [ ! -d "venv" ]; then
    echo "建立虛擬環境..."
    python -m venv venv
fi

# 啟動虛擬環境
source venv/bin/activate

# 安裝依賴
echo "安裝 Python 依賴..."
pip install -r requirements.txt

# 返回根目錄
cd ..

# 設置前端
echo ""
echo "📦 設置前端..."
cd frontend

# 檢查 Node 版本
node_version=$(node --version)
echo "✓ 使用 Node $node_version"

# 安裝依賴
echo "安裝 Node 依賴..."
npm install

# 返回根目錄
cd ..

echo ""
echo "✅ 安裝完成！"
echo ""
echo "接下來的步驟："
echo ""
echo "1️⃣  啟動後端服務器："
echo "   cd backend"
echo "   source venv/bin/activate  # macOS/Linux"
echo "   uvicorn main:app --reload"
echo ""
echo "2️⃣  在另一個終端啟動前端服務器："
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3️⃣  打開瀏覽器訪問："
echo "   http://localhost:5173"
echo ""
