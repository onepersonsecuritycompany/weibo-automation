#!/usr/bin/env python3
"""
Weibo Post Automation Script
Post tweets to Weibo using cookie-based authentication
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests

# API Endpoints
POST_URL = "https://weibo.com/ajax/statuses/update"
UPLOAD_URL = "https://picupload.weibo.com/interface/pic_upload.php"

# Headers template
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://weibo.com",
    "Referer": "https://weibo.com/",
}


def get_cookies(args):
    """Get cookies from various sources"""
    cookies = {}
    
    # Priority 1: Command line arguments
    if args.subp and args.sub:
        cookies["SUBP"] = args.subp
        cookies["SUB"] = args.sub
        return cookies
    
    # Priority 2: Environment variables
    subp = os.environ.get("WEIBO_SUBP")
    sub = os.environ.get("WEIBO_SUB")
    if subp and sub:
        cookies["SUBP"] = subp
        cookies["SUB"] = sub
        return cookies
    
    # Priority 3: Cookie file
    cookie_file = Path.home() / ".weibo_cookies.json"
    if cookie_file.exists():
        with open(cookie_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "SUBP" in data and "SUB" in data:
                cookies["SUBP"] = data["SUBP"]
                cookies["SUB"] = data["SUB"]
                return cookies
    
    raise ValueError(
        "Cookies not found. Please provide via:\n"
        "1. Command line: --subp and --sub\n"
        "2. Environment: WEIBO_SUBP and WEIBO_SUB\n"
        "3. File: ~/.weibo_cookies.json"
    )


def upload_image(image_path, cookies):
    """Upload image to Weibo and return pic_id"""
    headers = HEADERS.copy()
    headers["Referer"] = "https://weibo.com/"
    
    with open(image_path, "rb") as f:
        files = {"pic1": f}
        data = {"p": "1", "upload_source": "PC"}
        
        response = requests.post(
            UPLOAD_URL,
            headers=headers,
            cookies=cookies,
            files=files,
            data=data,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        if result.get("code") == "A00006":
            pic_data = result.get("data", {}).get("pics", {}).get("pic_1", {})
            return pic_data.get("pid")
        else:
            raise Exception(f"Upload failed: {result}")


def get_xsrf_token(cookies):
    """Get XSRF-TOKEN from Weibo homepage"""
    headers = HEADERS.copy()
    headers["Referer"] = "https://weibo.com/"
    
    response = requests.get(
        "https://weibo.com/",
        headers=headers,
        cookies=cookies,
        timeout=30,
        allow_redirects=True
    )
    response.raise_for_status()
    
    # Get XSRF-TOKEN from response cookies
    xsrf_token = response.cookies.get('XSRF-TOKEN')
    if xsrf_token:
        return xsrf_token
    
    raise Exception("Failed to get XSRF-TOKEN from Weibo")


def post_weibo(content, cookies, image_path=None):
    """Post a tweet to Weibo"""
    # Get XSRF-TOKEN first
    xsrf_token = get_xsrf_token(cookies)
    cookies['XSRF-TOKEN'] = xsrf_token
    
    headers = HEADERS.copy()
    headers["Referer"] = "https://weibo.com/"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["X-XSRF-TOKEN"] = xsrf_token
    
    # Prepare data
    data = {
        "content": content,
        "visible": "0",  # Public
        "share_id": "",
    }
    
    # Upload image if provided
    if image_path:
        pic_id = upload_image(image_path, cookies)
        data["pic_id"] = pic_id
    
    # Post the tweet
    response = requests.post(
        POST_URL,
        headers=headers,
        cookies=cookies,
        data=data,
        timeout=30
    )
    response.raise_for_status()
    
    result = response.json()
    return result


def format_hashtags(content):
    """
    格式化微博话题标签
    确保标签之间有空格分隔，以便正确显示为话题
    """
    import re
    
    # 查找所有话题标签 #话题#
    hashtags = re.findall(r'#([^#]+)#', content)
    
    # 如果没有标签，直接返回
    if not hashtags:
        return content
    
    # 确保标签之间有空格
    formatted = content
    for tag in hashtags:
        # 替换连续的标签，确保有空格
        pattern = f'#{tag}#(?=#)'
        replacement = f'#{tag}# '
        formatted = re.sub(pattern, replacement, formatted)
    
    return formatted


def main():
    parser = argparse.ArgumentParser(description="Post to Weibo")
    parser.add_argument("content", nargs="?", help="Tweet content")
    parser.add_argument("--file", "-f", help="Read content from file")
    parser.add_argument("--image", "-i", help="Attach image file")
    parser.add_argument("--subp", help="SUBP cookie value")
    parser.add_argument("--sub", help="SUB cookie value")
    parser.add_argument("--raw", "-r", action="store_true", help="Output raw JSON")
    parser.add_argument("--no-format", action="store_true", help="Disable hashtag formatting")
    
    args = parser.parse_args()
    
    # Get content
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read().strip()
    elif args.content:
        content = args.content
    else:
        # Read from stdin
        content = sys.stdin.read().strip()
    
    if not content:
        print("Error: No content provided", file=sys.stderr)
        sys.exit(1)
    
    # Format hashtags
    if not args.no_format:
        content = format_hashtags(content)
    
    # Validate content length
    if len(content) > 5000:
        print("Error: Content exceeds 5000 characters", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Get cookies
        cookies = get_cookies(args)
        
        # Post
        result = post_weibo(content, cookies, args.image)
        
        if args.raw:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            if result.get("ok") == 1:
                data = result.get("data", {})
                print(f"✓ Posted successfully!")
                print(f"  ID: {data.get('id')}")
                print(f"  URL: https://weibo.com/{data.get('id')}")
                print(f"  Time: {data.get('created_at')}")
            else:
                print(f"✗ Post failed: {result.get('msg', 'Unknown error')}", file=sys.stderr)
                sys.exit(1)
                
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
