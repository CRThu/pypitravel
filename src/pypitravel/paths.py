# src/pypitravel/paths.py
import os
import sys

# 确定基础路径 (Nuitka 打包环境 + 开发环境)
if getattr(sys, 'frozen', False):
    # Nuitka 打包后，可执行文件所在目录
    base_path = os.path.dirname(sys.executable)
else:
    # 开发环境 (src/pypitravel/ 目录)
    base_path = os.path.dirname(os.path.abspath(__file__))

# 缓存目录
CACHE_DIR = os.path.join(base_path, "data", "cache")
# 静态文件目录
STATIC_DIR = os.path.join(base_path, "static")

def set_cache_dir(path: str):
    """覆盖缓存目录路径"""
    global CACHE_DIR
    CACHE_DIR = path
    os.makedirs(CACHE_DIR, exist_ok=True)

# 确保必要的目录存在
os.makedirs(CACHE_DIR, exist_ok=True)
