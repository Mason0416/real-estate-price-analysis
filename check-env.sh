#!/bin/bash

echo "🔍 房屋價格合理性分析平台 - 環境檢查"
echo "========================================"
echo ""

# 檢查 Node.js
echo "檢查 Node.js..."
if command -v node &> /dev/null; then
    node_version=$(node --version)
    echo "✓ Node.js $node_version"
else
    echo "✗ 未找到 Node.js，請安裝 Node.js 18 或更新版本"
    exit 1
fi

# 檢查 npm
echo "檢查 npm..."
if command -v npm &> /dev/null; then
    npm_version=$(npm --version)
    echo "✓ npm $npm_version"
else
    echo "✗ 未找到 npm"
    exit 1
fi

# 檢查 Python
echo "檢查 Python..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    echo "✓ $python_version"
else
    echo "✗ 未找到 Python，請安裝 Python 3.9 或更新版本"
    exit 1
fi

# 檢查 pip
echo "檢查 pip..."
if command -v pip3 &> /dev/null; then
    pip_version=$(pip3 --version)
    echo "✓ $pip_version"
else
    echo "✗ 未找到 pip"
    exit 1
fi

echo ""
echo "✅ 所有環境依賴已滿足！"
echo ""
echo "接下來運行："
echo "  ./setup.sh (macOS/Linux) 或 setup.bat (Windows)"
