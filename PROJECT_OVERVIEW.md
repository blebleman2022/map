# DollyNav 项目总览

## 📁 项目结构

```
Dolly/
├── backend/                    # 后端服务（FastAPI）
│   ├── app/
│   │   ├── main.py            # 应用入口
│   │   ├── config.py          # 配置管理
│   │   ├── models/            # 数据模型
│   │   │   ├── request.py     # 请求模型
│   │   │   └── response.py    # 响应模型
│   │   ├── routers/           # API 路由
│   │   │   ├── parse.py       # 查询解析
│   │   │   ├── search.py      # 地点搜索
│   │   │   └── route.py       # 路线规划
│   │   └── services/          # 业务逻辑
│   │       ├── llm_service.py    # LLM 解析服务
│   │       ├── amap_service.py   # 高德地图服务
│   │       └── ranking_service.py # 排序服务
│   ├── requirements.txt       # Python 依赖
│   ├── .env                   # 环境变量
│   ├── .env.example          # 环境变量示例
│   ├── run.bat               # 启动脚本
│   └── test_api.py           # API 测试
│
├── frontend/                  # 前端应用（Next.js）
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx    # 布局组件
│   │   │   ├── page.tsx      # 主页面
│   │   │   └── globals.css   # 全局样式
│   │   └── components/       # React 组件
│   │       ├── Header.tsx    # 头部导航
│   │       ├── SearchBox.tsx # 搜索框
│   │       ├── ResultList.tsx # 结果列表
│   │       └── MapView.tsx   # 地图视图
│   ├── package.json          # Node 依赖
│   ├── .env.local           # 环境变量
│   ├── .env.local.example   # 环境变量示例
│   └── run.bat              # 启动脚本
│
├── tutors.html               # Tutors 页面
├── test.html                 # 测试页面
│
├── start.bat                 # 一键启动脚本
├── test_setup.py            # 环境检查脚本
│
├── README.md                 # 项目文档
├── SETUP.md                  # 安装指南
├── QUICKSTART.md            # 快速开始
├── PROJECT_OVERVIEW.md      # 本文件
└── .gitignore               # Git 忽略文件
```

## 🔧 技术架构

### 后端架构

```
用户请求
    ↓
FastAPI 路由
    ↓
┌─────────────────────────────────┐
│  1. 解析服务 (LLM/规则引擎)      │
│     - 自然语言 → 结构化参数      │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  2. 地图服务 (高德 API)          │
│     - POI 搜索                   │
│     - 地铁站查询                 │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  3. 排序服务                     │
│     - 距离计算                   │
│     - 多维度排序                 │
└─────────────────────────────────┘
    ↓
JSON 响应
```

### 前端架构

```
用户界面
    ↓
┌─────────────────────────────────┐
│  SearchBox 组件                  │
│  - 输入查询                      │
│  - 提交搜索                      │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  API 调用                        │
│  1. /api/parse-query            │
│  2. /api/search                 │
└─────────────────────────────────┘
    ↓
┌──────────────┬──────────────────┐
│ ResultList   │   MapView        │
│ - 列表展示   │   - 地图标记     │
│ - 详情信息   │   - 信息窗口     │
└──────────────┴──────────────────┘
```

## 🌊 数据流

### 1. 查询解析流程

```
用户输入: "附近5公里内离地铁站最近的3个经济型酒店"
    ↓
LLM/规则引擎解析
    ↓
结构化参数:
{
  "category": "酒店",
  "subcategory": "经济型酒店",
  "radius": 5000,
  "limit": 3,
  "sort_by": "距离地铁站最近",
  "proximity": "地铁站"
}
```

### 2. 搜索流程

```
结构化参数
    ↓
高德地图 POI 搜索
    ↓
原始结果 (50个)
    ↓
品牌筛选
    ↓
地铁站距离计算
    ↓
多维度排序
    ↓
Top 3 结果
```

### 3. 展示流程

```
搜索结果
    ↓
┌──────────────────┬─────────────────┐
│  ResultList      │   MapView       │
│  ┌────────────┐  │   ┌───────────┐ │
│  │ [1] 如家   │  │   │ 📍1       │ │
│  │ 2.3km      │  │   │ 📍2       │ │
│  │ 🚇150m     │  │   │ 📍3       │ │
│  │ [导航]     │  │   │ 🔵用户    │ │
│  └────────────┘  │   └───────────┘ │
└──────────────────┴─────────────────┘
```

## 🔑 核心功能实现

### 1. 自然语言解析

**方案 A：LLM（通义千问/OpenAI）**
- 优点：理解复杂语义，准确率高
- 缺点：需要 API Key，有成本

**方案 B：规则引擎**
- 优点：免费，响应快
- 缺点：功能有限

### 2. 地图搜索

使用高德地图 API：
- `place/around` - 周边搜索
- `direction/walking` - 路线规划
- `geocode/geo` - 地理编码

### 3. 智能排序

排序维度：
1. 距离地铁站（如指定）
2. 距离用户
3. 评分（未来）
4. 品牌知名度

### 4. 地图可视化

使用高德地图 JS API：
- 标记用户位置
- 标记搜索结果
- 信息窗口
- 自动调整视野

## 📊 性能指标

### 响应时间

- 查询解析：< 500ms（LLM）/ < 50ms（规则）
- 地图搜索：< 300ms
- 总响应时间：< 1s（LLM）/ < 500ms（规则）

### 并发能力

- 后端：100+ 并发（FastAPI 异步）
- 前端：无限制（静态资源）

### API 配额

- 高德地图：30万次/天（免费）
- 通义千问：100万 tokens/月（免费）

## 🔐 安全考虑

### API Key 保护

- 后端 Key：存储在 `.env`，不暴露给前端
- 前端 Key：使用环境变量，构建时注入
- Git 忽略：`.env` 文件不提交

### CORS 配置

- 仅允许前端域名访问
- 生产环境需配置白名单

### 频率限制

- 可选：添加 Redis 限流
- 防止 API 滥用

## 🚀 部署方案

### 开发环境

- 后端：`python -m app.main`
- 前端：`npm run dev`

### 生产环境

**后端：**
- Railway / Vercel / 阿里云
- 使用 Gunicorn + Uvicorn Workers

**前端：**
- Vercel（推荐）
- 自动 CI/CD

## 📈 未来扩展

### 功能扩展

- [ ] 用户登录/注册
- [ ] 收藏功能
- [ ] 历史记录云同步
- [ ] 多轮对话
- [ ] 语音输入
- [ ] 路线对比
- [ ] 实时路况

### 技术优化

- [ ] Redis 缓存
- [ ] 数据库持久化
- [ ] 服务端渲染（SSR）
- [ ] PWA 支持
- [ ] 性能监控

## 🐛 调试技巧

### 后端调试

```bash
# 查看日志
python -m app.main

# API 文档
http://localhost:8000/docs

# 健康检查
http://localhost:8000/health
```

### 前端调试

```bash
# 开发模式
npm run dev

# 查看构建
npm run build

# 浏览器控制台
F12 → Console
```

### 常用命令

```bash
# 后端测试
cd backend
python test_api.py

# 环境检查
python test_setup.py

# 清理缓存
rm -rf backend/__pycache__
rm -rf frontend/.next
```

## 📞 技术支持

遇到问题？

1. 查看 [QUICKSTART.md](QUICKSTART.md)
2. 查看 [SETUP.md](SETUP.md)
3. 运行 `python test_setup.py`
4. 查看后端日志和浏览器控制台
5. 提交 Issue

---

**版本**: 1.0.0  
**最后更新**: 2025-01-04

