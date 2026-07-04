# tools/list_cache.py
import json
import os
import sys

# 动态获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将 src 目录添加到 Python 搜索路径，确保能导入 pypitravel
sys.path.append(os.path.join(project_root, 'src'))

from pypitravel.journey_parser import get_summary

def list_and_parse_cache():
    # 缓存目录路径 (使用 paths.py 中的定义)
    cache_dir = os.path.join(os.path.expanduser("~"), ".pypitravel", "cache")
    
    if not os.path.exists(cache_dir):
        print(f"[-] 错误: 缓存目录不存在: {cache_dir}")
        return

    files = [f for f in os.listdir(cache_dir) if f.endswith('.json')]
    
    if not files:
        print("[-] 提示: 缓存目录中没有 JSON 文件")
        return

    print(f"[*] 发现 {len(files)} 个缓存文件，开始解析...\n")

    for file in files:
        file_path = os.path.join(cache_dir, file)
        print(f"--- 正在解析: {file} ---")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 使用解析器处理
            result = get_summary(data)
            
            # 简单验证输出结构
            if "error" in result:
                print(f"  [x] 解析出错: {result['error']}")
            else:
                print(f"  [OK] 解析成功")
                print(f"      行程名称: {result.get('journey_name')}")
                print(f"      总天数: {result.get('total_days')}")
                print(f"      总事件数: {result.get('total_events')}")
                
                # 打印所有每日计划的简要信息
                for daily in result.get('daily_summaries', []):
                    print(f"      - {daily['day_plan_name']}: {daily['event_count']} 个事件")
                    for event in daily.get('events', []):
                        info = ""
                        note = event.get('note', '').strip()
                        if note:
                            info += f" (Note: {note})"
                        
                        if 'transport_num' in event:
                            # 格式化时间戳 (假设是毫秒)
                            import datetime
                            def format_ts(ts):
                                try:
                                    dt = datetime.datetime.fromtimestamp(ts / 1000)
                                    return dt.strftime('%H:%M')
                                except:
                                    return str(ts)
                            
                            start_time = format_ts(event.get('transport_start_time'))
                            end_time = format_ts(event.get('transport_end_time'))
                            info += f" [{event['transport_num']} | {start_time} - {end_time}]"
                        print(f"        * {event['name']}{info}")
        except Exception as e:
            print(f"  [!] 文件处理异常: {e}")
        print("\n")

if __name__ == "__main__":
    list_and_parse_cache()
