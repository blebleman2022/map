# DollyNav 快速开始指南

## 🚀 5分钟快速启动

### 第一步：获取高德地图 API Key

这是**必须**的步骤，否则应用无法运行。

1. 访问 https://lbs.amap.com/
2. 注册/登录账号
3. 进入 **控制台** → **应用管理** → **我的应用** → **创建新应用**
4. 添加两个 Key：
   - **Web 服务 API Key**（用于后端）
   - **Web 端 JS API Key**（用于前端）

> 💡 提示：两个 Key 是不同的，都需要创建！

### 第二步：配置环境变量

#### 后端配置

编辑 `backend/.env` 文件：

```env
AMAP_API_KEY=你的Web服务API_Key
```

#### 前端配置

编辑 `frontend/.env.local` 文件：

```env
NEXT_PUBLIC_AMAP_KEY=你的Web端JS_API_Key
```

### 第三步：启动服务

#### Windows 用户（推荐）

双击运行 `start.bat`，等待服务启动完成。

#### 手动启动

**终端 1 - 后端：**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

**终端 2 - 前端：**
```bash
cd frontend
npm install
npm run dev
```

### 第四步：访问应用

打开浏览器访问：http://localhost:3000

## 🎯 快速测试

### 1. 测试环境配置

```bash
python test_setup.py
```

### 2. 测试后端功能（无需 API Key）

```bash
cd backend
venv\Scripts\activate
python test_api.py
```

### 3. 测试完整功能

在浏览器中输入查询：

- "附近的星巴克"
- "1公里内的便利店"
- "附近5公里内离地铁站最近的3个经济型酒店"

## ❓ 常见问题

### Q1: 没有 LLM API Key 可以用吗？

**可以！** 不配置 LLM API Key，系统会自动使用规则引擎。

功能会受限，但基本查询可以正常使用。

### Q2: 地图不显示怎么办？

检查：
1. `frontend/.env.local` 中的 `NEXT_PUBLIC_AMAP_KEY` 是否正确
2. 使用的是 **Web 端 JS API Key**，不是 Web 服务 Key
3. 浏览器控制台是否有错误

### Q3: 搜索没有结果？

检查：
1. 后端是否启动：访问 http://localhost:8000/health
2. `backend/.env` 中的 `AMAP_API_KEY` 是否正确
3. 是否授权了浏览器位置权限

### Q4: 端口被占用？

修改端口：
- 后端：编辑 `backend/.env`，添加 `PORT=8001`
- 前端：运行 `npm run dev -- -p 3001`

## 📚 更多文档

- [完整安装指南](SETUP.md)
- [项目文档](README.md)
- [API 文档](http://localhost:8000/docs)（启动后端后访问）

## 🎉 开始使用

现在你可以：

1. 输入自然语言查询
2. 查看智能解析结果
3. 浏览地图上的搜索结果
4. 点击导航按钮获取路线

享受智能导航的便利！

