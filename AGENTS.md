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
    *   `GET /api/journey/map?journey_id={journey_id}` (获取地图可视化数据)
    *   `GET /api/cached-journeys` (获取已缓存行程列表)
4.  **后端代理**: FastAPI 后端 (`src/pypitravel/cli.py`) 接收请求：
    *   **缓存逻辑**: 优先读取本地缓存目录（默认为 `~/.pypitravel/cache/`，可通过 `--cache-dir` 参数自定义，由 `paths.py` 统一管理）。
    *   **远程代理**: 若缓存不存在或请求强制刷新，调用 `httpx` 发起 API 请求，伪装 `User-Agent` 与 `Referer`。
5.  **数据响应**: 后端返回 JSON 数据。
6.  **可视化处理**: 前端接收到数据后，通过 MapLibre GL JS 在交互式地图上绘制 POI 标记点和交通路线（飞机弧线/驾车OSRM路由/步行直线）。

## 数据模型定义 (`dev/detail.json` 转换目标)

为了方便前端开发与地图可视化，我们将 API 返回的原始数据转换为以下标准模型结构：

> **注**: `/api/journey/summary` 接口返回的摘要数据会进一步简化，并将满足条件的交通事件中的 `transport_info` 字段平铺到事件对象中，以便前端直接读取。

### `/api/journey/map` 返回格式

```json
{
  "journey_name": "202609欧洲深度游26天",
  "days": [
    {
      "day_plan_name": "09.23 周三",
      "events": [
        {
          "name": "上海虹桥国际机场出发 至 北京首都国际机场",
          "event_type": 201,
          "transport_num": "CA1510",
          "transport_mode": "flight",
          "start": { "lat": 31.196, "lng": 121.340, "coord_type": "GCJ02", "name": "上海虹桥国际机场" },
          "end": { "lat": 40.080, "lng": 116.603, "coord_type": "GCJ02", "name": "北京首都国际机场" }
        }
      ]
    }
  ]
}
```

**`transport_mode` 含义**（表示从当前事件到下一个事件的交通方式）：
- `"flight"` — 飞机（event_type=201 + POI=机场）
- `"train"` — 火车（event_type=201 + POI=火车站）
- `"driving"` — 驾车（rtt=0）
- `"walking"` — 步行（rtt=1）
- `"transfer"` — 跨城转移（rtt=3）

### 原始 API 数据结构

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
*   [x] 实现本地缓存管理 (`~/.pypitravel/cache/`) 与路径模块化 (`paths.py`)。
*   [x] 实现业务解析模块 (`journey_parser.py`)。
*   [x] 优化数据处理逻辑（已实现 XLSX 导出、交通信息平铺解析）。
*   [x] 实现自动寻端口与浏览器唤起（`check_port` + `wait_for_server` + `webbrowser.open`）。
*   [x] 实现 WebView2 桌面窗口启动模式 (`gui.py` + `--gui` 参数)。
*   [ ] 实现圆周旅迹数据深度分析。

### 2. 前端 (交互式地图)
*   [x] 建立基础静态页面架构。
*   [x] 实现缓存列表选择与双模式请求。
*   [x] UI 美化（Tailwind CSS、卡片布局、表格样式）。
*   [x] 行程导出为 XLSX 格式（SheetJS）。
*   [x] 集成 MapLibre GL JS，完成路径可视化开发。

### 3. 打包与发布
*   [x] 配置 GitHub Actions 自动发布到 PyPI（推送 `v*` tag 触发）。
*   [ ] 配置 Nuitka 打包脚本，确保包含所有依赖、静态文件（`static/`）并优化体积。
*   [ ] 测试全流程构建，验证最终 `.exe` 的可执行性。

---

## 开发约定与操作指南

### 工具脚本
*   `tools/list_cache.py` — 缓存解析工具，用于查看和解析本地缓存的行程数据。

### 操作原则
*   **严禁自动提交**: 本项目的所有操作（如文件修改、版本更新等）均**严禁在未经用户明确同意的情况下执行自动 commit/push 操作**。Agent 必须在完成文件变更后停下来等待用户确认。

### 版本管理 (`bump-my-version`)
使用 `bump-my-version` 工具进行版本更新：
```bash
# 执行 patch 版本升级 (例如 1.0.2 -> 1.0.3)
uv run bump-my-version bump patch

# 更新锁文件
uv lock
```
