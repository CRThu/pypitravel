# PyPitravel

[![PyPI version](https://img.shields.io/pypi/v/pypitravel.svg)](https://pypi.org/project/pypitravel/)
[![Python version](https://img.shields.io/badge/python-3.12+-yellow.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache_2.0-green.svg)](LICENSE)

PyPitravel 是一个用于解析旅行规划平台《圆周旅迹》数据、提供行程规划导出与可视化的工具。

## 项目由来
由于“圆周旅迹”仅提供 iOS 客户端，导致在电脑端进行复杂的行程规划与整理非常不便。本项目旨在通过解析其 API 数据，在电脑端实现行程的可视化导出与整理。

## 核心功能

*   **智能解析**: 自动从旅行行程链接中提取行程 ID，并支持航班交通信息的精简备注。
*   **API 代理**: 安全地获取旅行规划平台数据，绕过 CORS 跨域拦截。
*   **本地部署**: 提供轻量级的本地 Web 服务。
*   **可视化分析**: 支持交互式地图轨迹绘制，区分飞机/火车/驾车/步行路线，支持日期筛选。
*   **数据导出**: 支持将行程规划数据导出为 **XLSX** 格式，方便在 Excel 中进行编辑与打印。
*   **双模式启动**: 支持浏览器模式和 WebView2 桌面窗口模式。

## 快速上手

### 安装

**浏览器模式**（默认）：
```bash
pip install pypitravel
```

**桌面窗口模式**（WebView2）：
```bash
pip install pypitravel[gui]
```
> 桌面窗口模式依赖 WebView2 运行时，Windows 10 20H2+ 和 Windows 11 已预装。如未安装，请参考 [Microsoft WebView2 下载](https://developer.microsoft.com/en-us/microsoft-edge/webview2/)。

### 启动

#### 浏览器模式
```bash
pypitravel
```
程序会自动寻找可用端口（默认 8000）并唤起浏览器，无需手动输入地址。

#### 桌面窗口模式
```bash
pypitravel --gui
```
程序会在 WebView2 桌面窗口中启动，无需浏览器，体验接近原生应用。

### 快速执行 (无需安装)
如果你安装了 `uv`，可以使用 `uvx` 直接运行，无需手动安装：
```bash
# 浏览器模式
uvx pypitravel

# 桌面窗口模式
uvx --from 'pypitravel[gui]' pypitravel --gui
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-p, --port` | 服务端口号 | 8000 |
| `--cache-dir` | 自定义缓存目录路径 | `~/.pypitravel/cache/` |
| `--gui` | 使用 WebView2 桌面窗口启动 | - |
| `--no-browser` | 启动时不自动打开浏览器 | - |

示例：
```bash
# 使用 9000 端口
pypitravel -p 9000

# 使用自定义缓存目录
pypitravel --cache-dir /path/to/cache

# 桌面窗口模式
pypitravel --gui

# 桌面窗口模式 + 自定义端口
pypitravel --gui -p 9000
```

### 快速执行 (无需安装)
如果你安装了 `uv`，可以使用 `uvx` 直接运行，无需手动安装：
```bash
uvx pypitravel
```

## 从源码安装 (开发者)
如果你需要进行二次开发或修改源码：
1. 环境要求：Python >= 3.12，安装 [uv](https://github.com/astral-sh/uv)。
2. 克隆项目并安装依赖：
   ```bash
   uv sync
   ```
3. 运行项目：
   ```bash
   uv run pypitravel
   ```

## 应用预览

### 路线地图
![路线地图](img/demo-map.png)

## 技术栈
*   **后端**: FastAPI, httpx
*   **前端**: HTML, JavaScript, Tailwind CSS, SheetJS, MapLibre GL JS
*   **地图**: MapLibre GL JS + OpenFreeMap + OSRM 路由
*   **桌面窗口**: pywebview + WebView2 (可选)
*   **依赖管理**: uv

## 许可证

本项目采用 [Apache License 2.0](LICENSE) 开源。

## 免责声明

PyPitravel 仅供个人学习与研究使用。所调用的 Pitravel 服务为商业软件，其 API 和数据归原平台所有。
*   本项目不承担任何因使用本项目而导致的平台服务条款违反责任。
*   严禁将本项目用于任何商业用途或大规模自动化抓取。
*   使用时请遵守目标平台的相关服务条款与隐私政策。
