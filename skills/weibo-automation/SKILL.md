---
name: weibo-automation
description: This skill should be used when the user asks to "post to Weibo", "发微博", "get hot search", "热搜", "analyze Weibo trends", "微博热搜", or automate Weibo interactions without manual login.
---

# Weibo Automation

Automate Weibo (Chinese social media platform) operations using cookie-based authentication with SUBP and SUB cookies.

## Prerequisites

Authentication requires two cookies obtained from browser DevTools after logging into weibo.com:
- `SUBP`: Weibo subscription cookie
- `SUB`: Weibo session cookie

## Quick Start

### Authentication Setup

```bash
# Environment variables (recommended)
export WEIBO_SUBP="your_subp_value"
export WEIBO_SUB="your_sub_value"

# Or create ~/.weibo_cookies.json
echo '{"SUBP": "value", "SUB": "value"}' > ~/.weibo_cookies.json
```

### Common Operations

```bash
# Post a tweet
python scripts/post_weibo.py "Your content here"

# Post with image
python scripts/post_weibo.py "Content" --image /path/to/image.jpg

# Get hot search list (no auth required)
python scripts/hot_search.py --limit 50

# Analyze and generate comment
python scripts/hot_search.py --comment --style neutral

# Auto-post hot search comment
python scripts/hot_search.py --comment --post
```

## Core Concepts

### Cookie Resolution Priority

Scripts resolve cookies in this order:
1. Command-line arguments (`--subp`, `--sub`)
2. Environment variables (`WEIBO_SUBP`, `WEIBO_SUB`)
3. Cookie file (`~/.weibo_cookies.json`)

### XSRF Token Flow

POST operations require XSRF token:
1. GET `https://weibo.com/` with auth cookies
2. Extract `XSRF-TOKEN` from response cookies
3. Include `X-XSRF-TOKEN` header in POST requests

### Hashtag Formatting

The `post_weibo.py` script auto-formats hashtags for proper display:
- Input: `测试#标签1##标签2#`
- Output: `测试#标签1# #标签2#`

## Available Scripts

| Script | Purpose | Auth Required |
|--------|---------|---------------|
| `scripts/post_weibo.py` | Post tweets with optional images | Yes |
| `scripts/hot_search.py` | Get/analyze hot search trends | No (Yes for posting) |

## Error Handling

| Code | Meaning | Solution |
|------|---------|----------|
| 100001 | Login required | Refresh cookies |
| 100002 | Session expired | Re-login |
| 100003 | Rate limited | Wait and retry |

## Rate Limits

- Post: 30/hour | Hot search: 60/min

## Additional Resources

### Reference Files

- **`references/api-reference.md`** - Complete API documentation, endpoints, parameters, and error codes
