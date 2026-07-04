# src/pypitravel/paths.py
import os
import sys

# 用户主目录下的 .pypitravel 文件夹
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".pypitravel", "cache")

# 静态文件目录（打包后或开发环境）
if getattr(sys, 'frozen', False):
    STATIC_DIR = os.path.join(os.path.dirname(sys.executable), "static")
else:
    STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

def set_cache_dir(path: str):
    """覆盖缓存目录路径"""
    global CACHE_DIR
    CACHE_DIR = path
    os.makedirs(CACHE_DIR, exist_ok=True)

# 确保必要的目录存在
os.makedirs(CACHE_DIR, exist_ok=True)
