# DollyNav - 智能对话导航

基于自然语言的智能导航 Web 应用，支持复杂条件查询和智能排序。

## 功能特性

- 🗣️ **自然语言查询**：用日常语言描述需求，无需学习复杂搜索语法
- 🤖 **智能解析**：支持 LLM 或规则引擎解析用户意图
- 🗺️ **地图可视化**：高德地图集成，实时展示搜索结果
- 🚇 **复杂条件**：支持距离、品牌、地铁站等多维度筛选
- 📱 **响应式设计**：完美适配桌面和移动设备

## 技术栈

### 后端
- **FastAPI** - 高性能异步 Web 框架
- **Python 3.9+** - 编程语言
- **高德地图 API** - 地图数据服务
- **通义千问/OpenAI** - 自然语言处理（可选）

### 前端
- **Next.js 14** - React 框架
- **TypeScript** - 类型安全
- **Tailwind CSS** - 样式框架
- **高德地图 JS API** - 地图展示

## 快速开始

### 前置要求

- Python 3.9+
- Node.js 18+
- 高德地图 API Key（[申请地址](https://lbs.amap.com/)）
- （可选）通义千问 API Key 或 OpenAI API Key

### 1. 克隆项目

```bash
git clone <repository-url>
cd Dolly
```

### 2. 后端配置

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 API Keys
```

**.env 配置说明：**

```env
# 必填：高德地图 Web 服务 API Key
AMAP_API_KEY=your_amap_api_key_here

# 可选：LLM API Key（至少配置一个，或不配置使用规则引擎）
DASHSCOPE_API_KEY=your_dashscope_api_key_here  # 通义千问
# 或
OPENAI_API_KEY=your_openai_api_key_here  # OpenAI

# 服务配置
HOST=0.0.0.0
PORT=8000
```

**启动后端：**

```bash
# 开发模式
python -m app.main

# 或使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端将运行在 `http://localhost:8000`

API 文档：`http://localhost:8000/docs`

### 3. 前端配置

```bash
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.local.example .env.local
# 编辑 .env.local 文件
```

**.env.local 配置说明：**

```env
# 后端 API 地址
NEXT_PUBLIC_API_URL=http://localhost:8000

# 高德地图 Web JS API Key（需要单独申请 Web 端 Key）
NEXT_PUBLIC_AMAP_KEY=your_amap_web_key_here
```

**启动前端：**

```bash
npm run dev
```

前端将运行在 `http://localhost:3000`

### 4. 访问应用

打开浏览器访问：`http://localhost:3000`

## 使用示例

### 查询示例

1. **基础查询**
   - "附近的星巴克"
   - "1公里内的便利店"

2. **复杂条件**
   - "附近5公里内离地铁站口最近的3个知名经济型连锁酒店门店"
   - "500米内24小时营业的药店"
   - "2公里内评分最高的川菜馆"

3. **品牌筛选**
   - "附近的如家酒店"
   - "最近的全家便利店"

## API 接口

### 1. 解析查询

```http
POST /api/parse-query
Content-Type: application/json

{
  "message": "附近5公里内离地铁站最近的3个经济型酒店",
  "location": {
    "lat": 39.9042,
    "lng": 116.4074
  }
}
```

### 2. 搜索地点

```http
POST /api/search
Content-Type: application/json

{
  "category": "酒店",
  "subcategory": "经济型酒店",
  "radius": 5000,
  "limit": 3,
  "sort_by": "距离地铁站最近",
  "brands": ["如家", "汉庭"],
  "proximity": "地铁站",
  "location": {
    "lat": 39.9042,
    "lng": 116.4074
  }
}
```

### 3. 路线规划

```http
POST /api/route
Content-Type: application/json

{
  "origin": {
    "lat": 39.9042,
    "lng": 116.4074
  },
  "destination": {
    "lat": 39.9088,
    "lng": 116.4577
  },
  "mode": "walking"
}
```

## 项目结构

```
Dolly/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── main.py         # FastAPI 应用入口
│   │   ├── config.py       # 配置管理
│   │   ├── models/         # 数据模型
│   │   ├── routers/        # API 路由
│   │   └── services/       # 业务逻辑
│   ├── requirements.txt    # Python 依赖
│   └── .env.example        # 环境变量示例
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── app/           # Next.js 页面
│   │   └── components/    # React 组件
│   ├── package.json       # Node 依赖
│   └── .env.local.example # 环境变量示例
├── tutors.html            # Tutors 页面
└── README.md              # 项目文档
```

## 常见问题

### 1. 获取高德地图 API Key

1. 访问 [高德开放平台](https://lbs.amap.com/)
2. 注册并登录
3. 进入控制台 → 应用管理 → 我的应用
4. 创建新应用，添加 Key
   - **Web 服务 API**：用于后端（AMAP_API_KEY）
   - **Web 端（JS API）**：用于前端（NEXT_PUBLIC_AMAP_KEY）

### 2. LLM 配置说明

- **不配置 LLM**：使用内置规则引擎，功能有限但免费
- **通义千问**：国内访问快，有免费额度
- **OpenAI**：效果好，需要科学上网

### 3. 位置权限

首次访问需要授权浏览器获取位置，如果拒绝：
- 应用会使用默认位置（北京天安门）
- 可以手动输入地址（未来版本支持）

### 4. 后端服务未启动

如果前端提示"搜索失败，请检查后端服务"：
1. 确认后端已启动：`http://localhost:8000/health`
2. 检查 CORS 配置
3. 查看后端控制台错误日志

## 开发说明

### 后端开发

```bash
cd backend

# 安装开发依赖
pip install -r requirements.txt

# 运行测试（如有）
pytest

# 代码格式化
black app/
```

### 前端开发

```bash
cd frontend

# 开发模式（热重载）
npm run dev

# 构建生产版本
npm run build

# 启动生产服务
npm start
```

## 部署

### 后端部署（Railway/Vercel）

```bash
# 使用 Railway CLI
railway up

# 或使用 Docker
docker build -t dolly-nav-backend ./backend
docker run -p 8000:8000 dolly-nav-backend
```

### 前端部署（Vercel）

```bash
# 使用 Vercel CLI
cd frontend
vercel
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题，请提交 Issue 或联系开发者。

