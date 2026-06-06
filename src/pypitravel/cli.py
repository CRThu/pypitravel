from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn
import os
import sys
import json
# 导入配置和解析器
from .paths import CACHE_DIR, STATIC_DIR
from .journey_parser import get_summary

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
    return os.path.join(CACHE_DIR, f"{journey_id}.json")

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
    """获取所有缓存的 journey ID"""
    files = os.listdir(CACHE_DIR)
    ids = [f.replace(".json", "") for f in files if f.endswith(".json")]
    return {"ids": ids}

@app.get("/api/journey/summary")
async def get_journey_summary(journey_id: str):
    """
    获取行程的精简汇总摘要信息
    """
    raw_data = load_from_cache(journey_id)
    if not raw_data:
        raw_data = await fetch_journey_from_api(journey_id)
        save_to_cache(journey_id, raw_data)
        
    return get_summary(raw_data)

app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
