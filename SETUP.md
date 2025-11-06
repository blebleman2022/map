# DollyNav 本地部署指南

## 快速开始（Windows）

### 方式一：一键启动（推荐）

1. 双击运行 `start.bat`
2. 按照提示配置 API Keys
3. 等待服务启动完成
4. 访问 `http://localhost:3000`

### 方式二：手动启动

#### 1. 后端启动

```bash
cd backend

# 创建虚拟环境（首次）
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖（首次）
pip install -r requirements.txt

# 配置环境变量（首次）
copy .env.example .env
# 编辑 .env 文件，填入 API Keys

# 启动服务
python -m app.main
```

或直接双击 `backend/run.bat`

#### 2. 前端启动

```bash
cd frontend

# 安装依赖（首次）
npm install

# 配置环境变量（首次）
copy .env.local.example .env.local
# 编辑 .env.local 文件，填入 API Keys

# 启动服务
npm run dev
```

或直接双击 `frontend/run.bat`

## API Key 获取指南

### 1. 高德地图 API Key

#### 步骤：

1. 访问 [高德开放平台](https://lbs.amap.com/)
2. 注册并登录账号
3. 进入 **控制台** → **应用管理** → **我的应用**
4. 点击 **创建新应用**
   - 应用名称：DollyNav
   - 应用类型：Web 服务
5. 添加 Key：
   - **Key 1（Web 服务）**：用于后端
     - 服务平台：Web 服务
     - 复制 Key 到 `backend/.env` 的 `AMAP_API_KEY`
   - **Key 2（Web 端 JS API）**：用于前端
     - 服务平台：Web 端（JS API）
     - 复制 Key 到 `frontend/.env.local` 的 `NEXT_PUBLIC_AMAP_KEY`

#### 注意事项：

- Web 服务 API 和 Web 端 JS API 是两个不同的 Key
- 免费额度：30万次/天
- 需要实名认证

### 2. LLM API Key（可选）

#### 选项 A：通义千问（推荐国内用户）

1. 访问 [阿里云百炼](https://dashscope.aliyun.com/)
2. 注册并登录
3. 进入 **API-KEY 管理**
4. 创建新的 API Key
5. 复制 Key 到 `backend/.env` 的 `DASHSCOPE_API_KEY`

**优势：**
- 国内访问快
- 免费额度：100万 tokens/月
- 无需科学上网

#### 选项 B：OpenAI

1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册并登录
3. 进入 **API Keys**
4. 创建新的 API Key
5. 复制 Key 到 `backend/.env` 的 `OPENAI_API_KEY`

**优势：**
- 效果更好
- 支持更多模型

**劣势：**
- 需要科学上网
- 需要绑定信用卡

#### 选项 C：不使用 LLM（规则引擎）

如果不配置任何 LLM API Key，系统会自动使用内置的规则引擎：

**优势：**
- 完全免费
- 无需额外配置
- 响应速度快

**劣势：**
- 功能有限
- 只能识别简单查询
- 不支持复杂语义理解

## 环境变量配置示例

### backend/.env

```env
# 必填：高德地图 Web 服务 API Key
AMAP_API_KEY=your_amap_web_service_key_here

# 可选：LLM API Key（至少配置一个，或都不配置使用规则引擎）
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
# 或
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# 服务配置（可选）
HOST=0.0.0.0
PORT=8000
```

### frontend/.env.local

```env
# 后端 API 地址
NEXT_PUBLIC_API_URL=http://localhost:8000

# 必填：高德地图 Web JS API Key
NEXT_PUBLIC_AMAP_KEY=your_amap_js_api_key_here
```

## 验证安装

### 1. 检查后端

访问：`http://localhost:8000/health`

应该返回：
```json
{"status": "ok"}
```

访问：`http://localhost:8000/docs`

应该看到 Swagger API 文档

### 2. 检查前端

访问：`http://localhost:3000`

应该看到应用首页

### 3. 测试功能

1. 在搜索框输入："附近的星巴克"
2. 点击搜索
3. 应该看到：
   - 解析结果展示
   - 地点列表
   - 地图标记

## 常见问题

### 1. Python 虚拟环境激活失败

**问题：** `venv\Scripts\activate` 报错

**解决：**
```bash
# 使用完整路径
.\venv\Scripts\activate

# 或使用 PowerShell
.\venv\Scripts\Activate.ps1
```

### 2. pip 安装依赖失败

**问题：** 网络超时或下载失败

**解决：**
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. npm 安装依赖失败

**问题：** 网络超时或下载失败

**解决：**
```bash
# 使用淘宝镜像
npm install --registry=https://registry.npmmirror.com
```

### 4. 端口被占用

**问题：** 8000 或 3000 端口已被使用

**解决：**

修改端口：
- 后端：编辑 `backend/.env`，设置 `PORT=8001`
- 前端：运行 `npm run dev -- -p 3001`

### 5. 地图不显示

**问题：** 地图区域空白

**解决：**
1. 检查 `NEXT_PUBLIC_AMAP_KEY` 是否正确
2. 检查浏览器控制台错误
3. 确认使用的是 **Web 端 JS API** Key，不是 Web 服务 Key

### 6. 搜索无结果

**问题：** 点击搜索后无结果

**解决：**
1. 检查后端是否启动：`http://localhost:8000/health`
2. 检查 `AMAP_API_KEY`（后端）是否正确
3. 查看浏览器控制台和后端日志
4. 确认位置权限已授权

### 7. LLM 解析失败

**问题：** 查询解析不准确

**解决：**
1. 检查 LLM API Key 是否正确
2. 查看后端日志中的错误信息
3. 如果不需要 LLM，删除 `.env` 中的 LLM 配置，使用规则引擎

## 性能优化

### 1. 后端优化

```bash
# 使用生产级 ASGI 服务器
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 2. 前端优化

```bash
# 构建生产版本
npm run build
npm start
```

## 下一步

- 查看 [README.md](README.md) 了解更多功能
- 访问 API 文档：`http://localhost:8000/docs`
- 尝试更多查询示例

## 技术支持

如遇到问题，请：
1. 查看本文档的常见问题部分
2. 检查后端和前端的控制台日志
3. 提交 Issue 并附上错误信息

