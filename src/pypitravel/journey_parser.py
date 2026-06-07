# src/pypitravel/journey_parser.py

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
