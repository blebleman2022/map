@echo off
echo ========================================
echo DollyNav 智能对话导航 - 启动脚本
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)

REM 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)

echo [1/4] 检查后端环境...
cd backend

REM 检查虚拟环境
if not exist "venv" (
    echo [提示] 创建 Python 虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境并安装依赖
call venv\Scripts\activate
echo [提示] 安装后端依赖...
pip install -r requirements.txt -q

REM 检查 .env 文件
if not exist ".env" (
    echo [警告] 未找到 .env 文件，请配置后端环境变量
    echo [提示] 复制 .env.example 为 .env 并填入 API Keys
    copy .env.example .env
    echo.
    echo 请编辑 backend\.env 文件，填入以下信息：
    echo   - AMAP_API_KEY: 高德地图 API Key（必填）
    echo   - DASHSCOPE_API_KEY 或 OPENAI_API_KEY: LLM API Key（可选）
    echo.
    pause
)

echo [2/4] 启动后端服务...
start "DollyNav Backend" cmd /k "cd /d %CD% && venv\Scripts\activate && python -m app.main"
timeout /t 3 >nul

cd ..

echo [3/4] 检查前端环境...
cd frontend

REM 检查 node_modules
if not exist "node_modules" (
    echo [提示] 安装前端依赖（这可能需要几分钟）...
    call npm install
)

REM 检查 .env.local 文件
if not exist ".env.local" (
    echo [警告] 未找到 .env.local 文件，请配置前端环境变量
    copy .env.local.example .env.local
    echo.
    echo 请编辑 frontend\.env.local 文件，填入以下信息：
    echo   - NEXT_PUBLIC_API_URL: 后端地址（默认 http://localhost:8000）
    echo   - NEXT_PUBLIC_AMAP_KEY: 高德地图 Web JS API Key（必填）
    echo.
    pause
)

echo [4/4] 启动前端服务...
start "DollyNav Frontend" cmd /k "cd /d %CD% && npm run dev"

cd ..

echo.
echo ========================================
echo 启动完成！
echo ========================================
echo.
echo 后端服务: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo 前端应用: http://localhost:3000
echo.
echo 按任意键退出此窗口（服务将继续运行）
pause >nul

