from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn
import os
import sys
import json
import socket
import threading
import webbrowser
import argparse
# 导入配置和解析器
from . import paths
from .journey_parser import get_summary, get_map_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确定静态文件路径和缓存目录在 paths.py 中定义

def get_cache_path(journey_id: str) -> str:
    """获取缓存文件路径"""
    return os.path.join(paths.CACHE_DIR, f"{journey_id}.json")

def load_from_cache(journey_id: str) -> dict | None:
    """从缓存读取数据"""
    path = get_cache_path(journey_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_to_cache(journey_id: str, data: dict):
    """保存数据到缓存"""
    with open(get_cache_path(journey_id), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def fetch_journey_from_api(journey_id: str) -> dict:
    """从源 API 获取原始数据"""
    url = f"https://www.pitravel.cn/api/slytherin/v1/web/journey/detail?journey_id={journey_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.pitravel.cn/"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

@app.get("/api/journey")
async def get_journey(journey_id: str, force_refresh: bool = False):
    """API 入口：协调缓存与数据获取"""
    # 校验 journey_id 是否合法
    if not journey_id.isdigit():
        return {"error": f"无效的行程 ID: {journey_id}，请确保输入的是纯数字 ID。"}

    # 1. 尝试从缓存获取 (如果 force_refresh 为 True，跳过缓存)
    raw_data = None
    if not force_refresh:
        raw_data = load_from_cache(journey_id)
    
    # 2. 如果缓存不存在或强制刷新，从 API 获取并写入缓存
    if not raw_data:
        raw_data = await fetch_journey_from_api(journey_id)
        save_to_cache(journey_id, raw_data)
            
    # 3. 直接返回原始数据
    return raw_data

@app.get("/api/cached-journeys")
async def get_cached_journeys():
    """获取所有缓存的行程信息（ID + 名称）"""
    files = os.listdir(paths.CACHE_DIR)
    journeys = []
    for f in files:
        if f.endswith(".json"):
            journey_id = f.replace(".json", "")
            data = load_from_cache(journey_id)
            name = "未命名行程"
            if data and "data" in data and "journey" in data["data"]:
                name = data["data"]["journey"].get("name", "未命名行程")
            journeys.append({"id": journey_id, "name": name})
    return {"journeys": journeys}

@app.get("/api/journey/summary")
async def get_journey_summary(journey_id: str):
    """
    获取行程的精简汇总摘要信息
    """
    # 校验 journey_id 是否合法
    if not journey_id.isdigit():
        return {"error": f"无效的行程 ID: {journey_id}，请确保输入的是纯数字 ID。"}

    raw_data = load_from_cache(journey_id)
    if not raw_data:
        raw_data = await fetch_journey_from_api(journey_id)
        save_to_cache(journey_id, raw_data)
        
    return get_summary(raw_data)

@app.get("/api/journey/map")
async def get_journey_map(journey_id: str):
    """获取行程的地图可视化数据"""
    if not journey_id.isdigit():
        return {"error": f"无效的行程 ID: {journey_id}，请确保输入的是纯数字 ID。"}

    raw_data = load_from_cache(journey_id)
    if not raw_data:
        raw_data = await fetch_journey_from_api(journey_id)
        save_to_cache(journey_id, raw_data)

    return get_map_data(raw_data)

app.mount("/", StaticFiles(directory=paths.STATIC_DIR, html=True), name="static")

def check_port(port: int) -> bool:
    """检查端口是否可用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False

def find_free_port() -> int:
    """随机一个可用的高位端口 (49152-65535)"""
    import random
    for _ in range(50):
        port = random.randint(49152, 65535)
        if check_port(port):
            return port
    # fallback: 让 OS 分配
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

def wait_for_server(host: str, port: int, timeout: float = 5.0):
    """轮询端口直到服务就绪"""
    import time
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.2)
    return False

def open_browser_when_ready(host: str, port: int):
    """服务就绪后打开浏览器"""
    def _open():
        if wait_for_server(host, port):
            webbrowser.open(f"http://{host}:{port}")
    threading.Thread(target=_open, daemon=True).start()

def main():
    parser = argparse.ArgumentParser(description="圆周旅迹行程规划导出与可视化工具")
    parser.add_argument("-p", "--port", type=int, default=None, help="端口号 (默认: 8000, GUI 模式随机高位端口)")
    parser.add_argument("--cache-dir", type=str, default=None, help="缓存目录路径 (默认: ~/.pypitravel/cache)")
    parser.add_argument("--no-browser", action="store_true", help="不自动打开浏览器")
    parser.add_argument("--gui", action="store_true", help="使用桌面窗口启动 (需安装 pywebview)")
    args = parser.parse_args()

    if args.cache_dir:
        paths.set_cache_dir(args.cache_dir)

    # GUI 模式默认随机高位端口，浏览器模式默认 8000
    port = args.port if args.port is not None else (find_free_port() if args.gui else 8000)

    if not check_port(port):
        print(f"❌ 端口 {port} 已被占用，请使用 -p 指定其他端口")
        sys.exit(1)

    host = "127.0.0.1"
    url = f"http://{host}:{port}"
    print(f"🚀 服务启动于 {url}")

    if args.gui:
        from .gui import launch_gui
        threading.Thread(target=uvicorn.run, args=(app,), kwargs={"host": host, "port": port}, daemon=True).start()
        launch_gui(host, port)
    else:
        if not args.no_browser:
            open_browser_when_ready(host, port)
        uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
