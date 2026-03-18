#!/usr/bin/env python3
"""
Weibo Hot Search Analyzer
获取微博热搜榜并进行智能分析
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import requests

# API Endpoints
HOT_SEARCH_URL = "https://weibo.com/ajax/side/hotSearch"

# Headers template
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://weibo.com/",
}


def get_cookies():
    """Get cookies from environment or file"""
    cookies = {}
    
    # Priority 1: Environment variables
    subp = os.environ.get("WEIBO_SUBP")
    sub = os.environ.get("WEIBO_SUB")
    if subp and sub:
        cookies["SUBP"] = subp
        cookies["SUB"] = sub
        return cookies
    
    # Priority 2: Cookie file
    cookie_file = Path.home() / ".weibo_cookies.json"
    if cookie_file.exists():
        with open(cookie_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "SUBP" in data and "SUB" in data:
                cookies["SUBP"] = data["SUBP"]
                cookies["SUB"] = data["SUB"]
                return cookies
    
    # Hot search doesn't require login
    return {}


def get_xsrf_token(cookies):
    """Get XSRF-TOKEN from Weibo homepage"""
    headers = HEADERS.copy()
    
    response = requests.get(
        "https://weibo.com/",
        headers=headers,
        cookies=cookies,
        timeout=30,
        allow_redirects=True
    )
    response.raise_for_status()
    
    xsrf_token = response.cookies.get('XSRF-TOKEN')
    if xsrf_token:
        return xsrf_token
    
    return None


def get_hot_search(cookies, limit=50):
    """获取微博热搜榜"""
    headers = HEADERS.copy()
    
    # Get XSRF-TOKEN if we have cookies
    if cookies:
        xsrf = get_xsrf_token(cookies)
        if xsrf:
            cookies = cookies.copy()
            cookies['XSRF-TOKEN'] = xsrf
            headers['X-XSRF-TOKEN'] = xsrf
    
    response = requests.get(
        HOT_SEARCH_URL,
        headers=headers,
        cookies=cookies,
        timeout=30
    )
    response.raise_for_status()
    
    result = response.json()
    if result.get("ok") != 1:
        raise Exception(f"Failed to get hot search: {result}")
    
    data = result.get("data", {})
    realtime = data.get("realtime", [])
    
    # Filter and format
    hot_list = []
    for item in realtime[:limit]:
        hot_list.append({
            "rank": item.get("rank", 0),
            "title": item.get("note", ""),
            "category": item.get("category", ""),
            "hot_value": item.get("raw_hot", 0),
            "label": item.get("label", ""),  # 爆、热、新、荐
            "url": f"https://s.weibo.com/weibo?q={requests.utils.quote(item.get('note', ''))}",
        })
    
    return hot_list


def analyze_trend(hot_list: List[Dict]) -> Dict[str, Any]:
    """分析热搜趋势"""
    analysis = {
        "total": len(hot_list),
        "categories": {},
        "labels": {},
        "top_10": hot_list[:10],
        "hot_topics": [],  # 爆
        "rising_topics": [],  # 新
        "recommend_topics": [],  # 荐
    }
    
    for item in hot_list:
        # Category stats
        cat = item.get("category", "其他")
        analysis["categories"][cat] = analysis["categories"].get(cat, 0) + 1
        
        # Label stats
        label = item.get("label", "")
        if label:
            analysis["labels"][label] = analysis["labels"].get(label, 0) + 1
        
        # Special labels
        if label == "爆":
            analysis["hot_topics"].append(item)
        elif label == "新":
            analysis["rising_topics"].append(item)
        elif label == "荐":
            analysis["recommend_topics"].append(item)
    
    return analysis


def generate_comment(analysis: Dict, style="neutral") -> str:
    """生成热搜评论"""
    hot_list = analysis.get("top_10", [])
    
    if not hot_list:
        return "暂无热搜数据"
    
    # Get top topics
    top_3 = [t["title"] for t in hot_list[:3]]
    hot_topics = analysis.get("hot_topics", [])
    rising_topics = analysis.get("rising_topics", [])
    
    # Generate comment based on style
    if style == "neutral":
        comment = f"📊 今日热搜观察（共{analysis['total']}条）：\n\n"
        comment += "🔥 热度前三：\n"
        for i, title in enumerate(top_3, 1):
            comment += f"  {i}. {title}\n"
        
        if hot_topics:
            comment += f"\n💥 爆点话题：{hot_topics[0]['title']}"
        
        if rising_topics:
            comment += f"\n🆕 新晋热点：{rising_topics[0]['title']}"
    
    elif style == "humorous":
        comment = "🍉 今日吃瓜指南：\n\n"
        comment += f"热搜榜比我家冰箱还热闹！\n"
        comment += f"C位出道的是：{top_3[0]}\n"
        if len(top_3) > 1:
            comment += f"紧追其后的是：{top_3[1]}\n"
        if hot_topics:
            comment += f"\n这瓜保熟：{hot_topics[0]['title']} 🔥"
    
    elif style == "professional":
        comment = "【热搜数据分析】\n\n"
        comment += f"监测时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        comment += f"样本数量：{analysis['total']}条\n"
        comment += f"热度峰值：{hot_list[0]['hot_value']:,}\n"
        comment += "\nTop 3 话题：\n"
        for i, item in enumerate(hot_list[:3], 1):
            comment += f"  {i}. {item['title']} ({item['hot_value']:,})\n"
        
        # Category distribution
        if analysis["categories"]:
            comment += "\n领域分布：\n"
            for cat, count in sorted(analysis["categories"].items(), key=lambda x: -x[1])[:3]:
                comment += f"  {cat}: {count}条\n"
    
    else:
        comment = "今日热搜速览\n\n"
        for i, item in enumerate(hot_list[:5], 1):
            label = f"[{item['label']}]" if item['label'] else ""
            comment += f"{i}. {label}{item['title']}\n"
    
    return comment


def display_hot_search(hot_list, format_type="text"):
    """显示热搜榜"""
    if format_type == "json":
        print(json.dumps(hot_list, ensure_ascii=False, indent=2))
        return
    
    if format_type == "raw":
        for item in hot_list:
            print(json.dumps(item, ensure_ascii=False))
        return
    
    # Text format
    print(f"\n{'='*70}")
    print(f"📈 微博热搜榜 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*70}")
    
    for item in hot_list:
        rank = item["rank"]
        title = item["title"]
        label = item["label"]
        hot_value = item["hot_value"]
        category = item["category"]
        
        # Format label
        label_str = ""
        if label == "爆":
            label_str = "🔥"
        elif label == "热":
            label_str = "🌡️"
        elif label == "新":
            label_str = "🆕"
        elif label == "荐":
            label_str = "⭐"
        elif label == "商":
            label_str = "💰"
        
        # Format hot value
        if hot_value >= 1000000:
            hot_str = f"{hot_value/10000:.0f}万"
        else:
            hot_str = f"{hot_value:,}"
        
        cat_str = f"[{category}]" if category else ""
        
        print(f"\n[{rank:2d}] {label_str} {title}")
        print(f"      热度: {hot_str} {cat_str}")


def main():
    parser = argparse.ArgumentParser(description="Weibo Hot Search Analyzer")
    parser.add_argument("--limit", "-l", type=int, default=50, help="Number of hot search items (default: 50)")
    parser.add_argument("--format", "-f", choices=["text", "json", "raw"], default="text", help="Output format")
    parser.add_argument("--analyze", "-a", action="store_true", help="Analyze trends")
    parser.add_argument("--comment", "-c", action="store_true", help="Generate comment")
    parser.add_argument("--style", "-s", choices=["neutral", "humorous", "professional", "simple"], 
                       default="neutral", help="Comment style")
    parser.add_argument("--post", "-p", action="store_true", help="Post comment to Weibo")
    
    args = parser.parse_args()
    
    try:
        # Get cookies (optional for hot search)
        cookies = get_cookies()
        
        # Get hot search
        hot_list = get_hot_search(cookies, args.limit)
        
        # Display
        display_hot_search(hot_list, args.format)
        
        # Analyze
        if args.analyze or args.comment or args.post:
            analysis = analyze_trend(hot_list)
            
            if args.analyze:
                print(f"\n{'='*70}")
                print("📊 数据分析")
                print(f"{'='*70}")
                print(f"总话题数: {analysis['total']}")
                print(f"\n领域分布:")
                for cat, count in sorted(analysis['categories'].items(), key=lambda x: -x[1]):
                    print(f"  {cat}: {count}条")
                print(f"\n标签分布:")
                for label, count in analysis['labels'].items():
                    label_name = {"爆": "爆点", "热": "热门", "新": "新晋", "荐": "推荐", "商": "商业"}.get(label, label)
                    print(f"  {label_name}: {count}条")
            
            # Generate comment
            if args.comment or args.post:
                comment = generate_comment(analysis, args.style)
                print(f"\n{'='*70}")
                print("💬 智能评论")
                print(f"{'='*70}")
                print(comment)
                
                # Post to Weibo
                if args.post:
                    print(f"\n{'='*70}")
                    print("📤 发布到微博")
                    print(f"{'='*70}")
                    
                    # Import post_weibo module
                    sys.path.insert(0, str(Path(__file__).parent))
                    from post_weibo import post_weibo, get_xsrf_token
                    
                    # 添加话题标签，确保标签之间有空格
                    hashtags = "#微博热搜 #热点观察 #智能助手整理"
                    full_content = comment + "\n\n" + hashtags
                    result = post_weibo(full_content, cookies)
                    
                    if result.get("ok") == 1:
                        data = result.get("data", {})
                        print(f"✓ 发布成功!")
                        print(f"  ID: {data.get('id')}")
                        print(f"  URL: https://weibo.com/{data.get('id')}")
                    else:
                        print(f"✗ 发布失败: {result.get('msg', 'Unknown error')}")
                        return 1
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
