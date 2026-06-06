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
        simplified_events = [
            {
                "name": event.get("name", "未命名事件"),
                "note": event.get("note", "")
            }
            for event in raw_events
        ]
        
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
