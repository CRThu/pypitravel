# pypitravel (智能旅行规划工具)

本项目旨在构建一个交互式旅行规划与数据可视化工具，主要用于解决“圆周旅迹”缺乏电脑端行程规划能力的问题。

## 软件运行流程与技术架构

本项目 `pypitravel` 采用 **FastAPI (后端) + 静态前端** 的架构，旨在实现数据处理与可视化。

### 数据交互流程

1.  **用户输入**: 用户在前端页面粘贴行程链接（例如: `https://www.pitravel.cn/web/journey/detail/{journey_id}?lang=zh_cn&source=copyLink`），或通过下拉框选择已缓存的行程。
2.  **前端解析**: 前端通过正则表达式提取 `journey_id`。
3.  **请求转发**: 前端通过 `fetch` 请求本地后端接口：
    *   `GET /api/journey?journey_id={journey_id}` (获取原始数据，支持缓存)
    *   `GET /api/journey/summary?journey_id={journey_id}` (获取精简摘要)
    *   `GET /api/cached-journeys` (获取已缓存行程列表)
4.  **后端代理**: FastAPI 后端 (`src/pypitravel/cli.py`) 接收请求：
    *   **缓存逻辑**: 优先读取本地 `src/pypitravel/data/cache/` 目录。
    *   **远程代理**: 若缓存不存在或请求强制刷新，调用 `httpx` 发起 API 请求，伪装 `User-Agent` 与 `Referer`。
5.  **数据响应**: 后端返回 JSON 数据。
6.  **可视化处理**: 前端接收到数据后，进行解析并在地图上绘制（计划中）。

## 数据模型定义 (`dev/detail.json` 转换目标)

为了方便前端开发与地图可视化，我们将 API 返回的原始数据转换为以下标准模型结构：

```json
{
  "code": 0,                // 接口状态码
  "success": true,          // 请求是否成功
  "msg": "成功",            // 状态描述
  "data": {
    "user_profile": {       // 用户信息
      "user_id": "...",
      "nickname": "...",
      "gender": 2,
      "avatar": "..."
    },
    "journey": {            // 核心行程数据
      "id": 0,              // 行程 ID
      "name": "...",        // 行程标题
      "days": 0,            // 总天数
      "start_time": 0,      // 行程起始时间戳 (毫秒)
      "time_description": "...", // 行程日期范围说明
      "poi_count": 0,       // POI 总数
      "bind_political_info": [ // 地理位置列表
        {
          "political_id": "...",
          "name": "...",
          "political_level": 3,
          "location": { "latitude": "...", "longitude": "..." }
        }
      ],
      "day_plans": [        // 每日计划数组 (按天组织)
        {
          "day_index": 1,
          "day_plan_name": "...",
          "remark": "...",
          "events": [       // 具体事件数组
            {
              "id": 0,
              "name": "...",
              "note": "...",
              "event_type": 0,
              "start_time": "HH:MM",
              "end_time": "HH:MM",
              "transport_info": { "transport_num": "...", "transport_start_time": 0 },
              "start_poi_info": { 
                "name": "...",
                "location": { "latitude": 0, "longitude": 0 },
                "coordinate_type": "...",
                "address": "...",
                "category": [{ "level1": "...", "level2": "..." }]
              },
              "end_poi_info": { ... }
            }
          ]
        }
      ]
    }
  }
}
```

## 任务清单

### 1. 后端 (FastAPI 代理)
*   [x] 建立标准包结构 `src/pypitravel/`。
*   [x] 配置 `pyproject.toml` 支持 CLI 脚本入口 `pypitravel`。
*   [x] 编写 `cli.py`，实现 API 代理及静态文件映射。
*   [x] 实现本地缓存管理 (`data/cache/`) 与路径模块化 (`paths.py`)。
*   [x] 实现业务解析模块 (`journey_parser.py`)。
*   [ ] 优化数据处理逻辑（引入 CSV 导出、圆周旅迹分析）。

### 2. 前端 (交互式地图)
*   [x] 建立基础静态页面架构。
*   [x] 实现缓存列表选择与双模式请求。
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
