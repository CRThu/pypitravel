# pypitravel (智能旅行规划工具)

本项目旨在构建一个交互式旅行规划与数据可视化工具，主要用于解决“圆周旅迹”缺乏电脑端行程规划能力的问题。

## 软件运行流程与技术架构

本项目 `pypitravel` 采用 **FastAPI (后端) + 静态前端** 的架构，旨在实现数据处理与可视化。

### 数据交互流程

1.  **用户输入**: 用户在前端页面粘贴行程链接（例如: `https://www.pitravel.cn/web/journey/detail/{journey_id}?lang=zh_cn&source=copyLink`）。
2.  **前端解析**: 前端通过正则表达式提取 `journey_id`。
3.  **请求转发**: 前端通过 `fetch` 请求本地后端接口：
    *   **接口**: `GET /api/journey?journey_id={journey_id}`
4.  **后端代理**: FastAPI 后端 (`src/pypitravel/cli.py`) 接收请求，调用 `httpx` 发起真正的 API 请求：
    *   **目标地址**: `https://www.pitravel.cn/api/slytherin/v1/web/journey/detail?journey_id={journey_id}`
    *   **请求头**: 伪装 `User-Agent` 与 `Referer` 以绕过服务器安全检查。
5.  **数据响应**: 目标服务器返回 JSON 数据，后端原样透传回前端。
6.  **可视化处理**: 前端接收到数据后，进行解析并在地图上绘制（计划中）。

---

## 任务清单

### 1. 后端 (FastAPI 代理)
*   [x] 建立标准包结构 `src/pypitravel/`。
*   [x] 配置 `pyproject.toml` 支持 CLI 脚本入口 `pypitravel`。
*   [x] 编写 `cli.py`，实现 API 代理及静态文件映射。
*   [ ] 优化数据处理逻辑（引入 CSV 导出、圆周旅迹分析）。

### 2. 前端 (交互式地图)
*   [x] 建立基础静态页面架构。
*   [ ] 集成 Leaflet.js，完成路径可视化开发。
*   [ ] 优化前端构建流程（整合 `Bun` 构建资源）。

### 3. 打包与发布
*   [ ] 配置 `Nuitka` 打包脚本，确保包含所有依赖、静态文件（`static/`）并优化体积。
*   [ ] 测试全流程构建，验证最终 `.exe` 的可执行性。

---

## 使用指南

*   **同步环境**: `uv sync`
*   **开发运行**: `uv run pypitravel`
*   **CLI 安装**: `uv pip install -e .` (随后直接执行 `pypitravel`)
