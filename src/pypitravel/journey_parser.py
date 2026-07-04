# src/pypitravel/journey_parser.py
import math


def _category_level2(poi: dict) -> str:
    cats = poi.get("category", [])
    return cats[0].get("level2", "") if cats else ""


def _infer_transport_event_mode(event: dict) -> str:
    """event_type=201 的交通事件：从 POI category 推断 flight/train/car"""
    sp = event.get("start_poi_info") or {}
    ep = event.get("end_poi_info") or {}
    sc = _category_level2(sp)
    ec = _category_level2(ep)
    if sc == "机场" or ec == "机场":
        return "flight"
    if sc == "火车站" or ec == "火车站":
        return "train"
    return "car"


def _rtt_to_mode(rtt) -> str:
    """route_transportation_type → 从当前事件到下一个事件的交通方式"""
    if rtt == 0:
        return "driving"
    if rtt == 1:
        return "walking"
    if rtt == 3:
        return "transfer"
    return "walking"


def _extract_poi(poi: dict) -> dict | None:
    if not poi:
        return None
    loc = poi.get("location", {})
    lat = loc.get("latitude")
    lng = loc.get("longitude")
    if not lat or not lng:
        return None
    return {
        "lat": float(lat),
        "lng": float(lng),
        "coord_type": poi.get("coordinate_type", "WGS84"),
        "name": poi.get("name", ""),
    }


def get_map_data(data: dict) -> dict:
    """解析行程数据，返回地图可视化所需的结构化数据。"""
    journey = data.get("data", {}).get("journey", {})
    if not journey:
        return {"error": "Invalid data format"}

    days = []
    for day_plan in journey.get("day_plans", []):
        raw_events = day_plan.get("events", [])
        events = []
        for event in raw_events:
            event_type = event.get("event_type")
            rtt = event.get("route_transportation_type")
            start = _extract_poi(event.get("start_poi_info"))
            end = _extract_poi(event.get("end_poi_info"))

            if event_type == 201:
                mode = _infer_transport_event_mode(event)
                tnum = (event.get("transport_info") or {}).get("transport_num", "")
            else:
                mode = _rtt_to_mode(rtt)
                tnum = ""

            events.append({
                "name": event.get("name", ""),
                "event_type": event_type,
                "transport_mode": mode,
                "transport_num": tnum,
                "start": start,
                "end": end,
            })

        days.append({
            "day_plan_name": day_plan.get("day_plan_name", ""),
            "events": events,
        })

    return {
        "journey_name": journey.get("name", ""),
        "days": days,
    }


def get_summary(data: dict) -> dict:
    """
    解析旅行行程数据，提取精简后的汇总信息。
    """
    journey = data.get("data", {}).get("journey", {})
    if not journey:
        return {"error": "Invalid data format"}

    day_plans = journey.get("day_plans", [])
    
    daily_summaries = []
    total_events = 0
    
    for day_plan in day_plans:
        raw_events = day_plan.get("events", [])
        
        # 精简事件：只保留 name 和 note
        simplified_events = []
        for event in raw_events:
            simplified_event = {
                "name": event.get("name", "未命名事件"),
                "note": event.get("note", "")
            }
            
            # 如果是交通，平铺提取 transport_info
            event_type = event.get("event_type")
            event_type_v2 = event.get("event_type_v2")
            if event_type == 201 or event_type_v2 == 201:
                transport_info = event.get("transport_info")
                if transport_info and isinstance(transport_info, dict):
                    simplified_event.update(transport_info)
            
            simplified_events.append(simplified_event)
        
        event_count = len(simplified_events)
        
        daily_summaries.append({
            "day_plan_name": day_plan.get("day_plan_name"),
            "event_count": event_count,
            "events": simplified_events
        })
        total_events += event_count
    
    return {
        "journey_name": journey.get("name"),
        "total_days": journey.get("days", 0),
        "total_events": total_events,
        "daily_summaries": daily_summaries
    }
