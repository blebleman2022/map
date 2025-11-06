"""测试环境配置脚本"""
import sys
import os

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✓ Python 版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python 版本过低: {version.major}.{version.minor}.{version.micro}")
        print("  需要 Python 3.9+")
        return False

def check_backend_env():
    """检查后端环境变量"""
    env_file = "backend/.env"
    if not os.path.exists(env_file):
        print(f"✗ 未找到 {env_file}")
        return False
    
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_amap = "AMAP_API_KEY=" in content and len(content.split("AMAP_API_KEY=")[1].split("\n")[0].strip()) > 0
    has_llm = ("DASHSCOPE_API_KEY=" in content or "OPENAI_API_KEY=" in content)
    
    if has_amap:
        print(f"✓ 后端环境变量已配置")
        if not has_llm:
            print("  ⚠ 未配置 LLM API Key，将使用规则引擎")
        return True
    else:
        print(f"✗ 后端环境变量未配置")
        print(f"  请编辑 {env_file}，填入 AMAP_API_KEY")
        return False

def check_frontend_env():
    """检查前端环境变量"""
    env_file = "frontend/.env.local"
    if not os.path.exists(env_file):
        print(f"✗ 未找到 {env_file}")
        return False
    
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_amap = "NEXT_PUBLIC_AMAP_KEY=" in content and len(content.split("NEXT_PUBLIC_AMAP_KEY=")[1].split("\n")[0].strip()) > 0
    
    if has_amap:
        print(f"✓ 前端环境变量已配置")
        return True
    else:
        print(f"✗ 前端环境变量未配置")
        print(f"  请编辑 {env_file}，填入 NEXT_PUBLIC_AMAP_KEY")
        return False

def check_backend_deps():
    """检查后端依赖"""
    try:
        import fastapi
        import uvicorn
        import pydantic
        import httpx
        print("✓ 后端依赖已安装")
        return True
    except ImportError as e:
        print(f"✗ 后端依赖未安装: {e}")
        print("  运行: cd backend && pip install -r requirements.txt")
        return False

def main():
    print("=" * 50)
    print("DollyNav 环境检查")
    print("=" * 50)
    print()
    
    results = []
    
    print("[1/4] 检查 Python 版本...")
    results.append(check_python_version())
    print()
    
    print("[2/4] 检查后端环境变量...")
    results.append(check_backend_env())
    print()
    
    print("[3/4] 检查前端环境变量...")
    results.append(check_frontend_env())
    print()
    
    print("[4/4] 检查后端依赖...")
    results.append(check_backend_deps())
    print()
    
    print("=" * 50)
    if all(results):
        print("✓ 所有检查通过！可以启动服务")
        print()
        print("启动方式：")
        print("  1. 双击 start.bat（一键启动）")
        print("  2. 或分别运行：")
        print("     - 后端: cd backend && python -m app.main")
        print("     - 前端: cd frontend && npm run dev")
    else:
        print("✗ 部分检查未通过，请按照提示修复")
    print("=" * 50)

if __name__ == "__main__":
    main()

