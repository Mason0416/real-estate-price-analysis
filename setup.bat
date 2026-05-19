@echo off
setlocal enabledelayedexpansion

echo 房屋價格合理性分析平台 - 安裝腳本
echo ==================================
echo.

REM 設置後端
echo 設置後端...
cd backend

REM 檢查 Python 版本
python --version
if errorlevel 1 (
    echo 錯誤: 未找到 Python，請先安裝 Python 3.9+
    pause
    exit /b 1
)

REM 創建虛擬環境
if not exist "venv" (
    echo 建立虛擬環境...
    python -m venv venv
)

REM 啟動虛擬環境
call venv\Scripts\activate.bat

REM 安裝依賴
echo 安裝 Python 依賴...
pip install -r requirements.txt

REM 返回根目錄
cd ..

REM 設置前端
echo.
echo 設置前端...
cd frontend

REM 檢查 Node 版本
node --version
if errorlevel 1 (
    echo 錯誤: 未找到 Node.js，請先安裝 Node.js 18+
    pause
    exit /b 1
)

REM 安裝依賴
echo 安裝 Node 依賴...
call npm install

REM 返回根目錄
cd ..

echo.
echo 安裝完成！
echo.
echo 接下來的步驟：
echo.
echo 1. 啟動後端服務器：
echo    cd backend
echo    venv\Scripts\activate.bat
echo    uvicorn main:app --reload
echo.
echo 2. 在另一個終端啟動前端服務器：
echo    cd frontend
echo    npm run dev
echo.
echo 3. 打開瀏覽器訪問：
echo    http://localhost:5173
echo.
pause
