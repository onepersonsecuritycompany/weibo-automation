# Weibo Automation Skill

A powerful skill for automating Weibo (微博) operations, including posting tweets and retrieving hot search trends.

[中文文档](./README_CN.md)

## Features

- **Post Weibo**: Post text and images to Weibo automatically
- **Hot Search**: Retrieve real-time trending topics from Weibo
- **Trend Analysis**: Analyze hot search data with intelligent insights
- **Auto Comment**: Generate and post comments based on trending topics

## Installation

### Quick Install (One-Line Command)

**macOS / Linux (Bash):**
```bash
# Auto-detect agent and install
curl -fsSL https://raw.githubusercontent.com/onepersonsecuritycompany/weibo-automation/main/install.sh | bash

# Or specify agent: claude, openclaw, codex, opencode, trae, qoder
curl -fsSL https://raw.githubusercontent.com/onepersonsecuritycompany/weibo-automation/main/install.sh | bash -s -- claude
```

**Windows (PowerShell):**
```powershell
# Run installer (auto-detect agent)
Invoke-Expression (Invoke-WebRequest -Uri "https://raw.githubusercontent.com/onepersonsecuritycompany/weibo-automation/main/install.ps1" -UseBasicParsing).Content
```

### Manual Install

**Step 1:** Clone the repository
```bash
git clone https://github.com/onepersonsecuritycompany/weibo-automation.git
```

**Step 2:** Copy skill folder to your agent's config directory

| Agent | Config Directory |
|-------|------------------|
| Claude Code | `~/.claude/skills/weibo-automation/` |
| OpenClaw | `~/.openclaw/skills/weibo-automation/` |
| Codex | `~/.codex/skills/weibo-automation/` |
| OpenCode | `~/.opencode/skills/weibo-automation/` |
| Trae | `~/.trae/skills/weibo-automation/` |
| Qoder | `~/.qoder/skills/weibo-automation/` |

```bash
# macOS / Linux example
cp -r weibo-automation/skills/weibo-automation ~/.claude/skills/
```

```powershell
# Windows example
Copy-Item -Recurse -Path ".\weibo-automation\skills\weibo-automation" -Destination "$env:USERPROFILE\.claude\skills\weibo-automation"
```

### Requirements

- Python 3.8+
- `requests` library: `pip install requests`

## Authentication Setup

### Method 1: Environment Variables (Recommended)

**macOS / Linux:**
```bash
export WEIBO_SUBP="your_subp_cookie_value"
export WEIBO_SUB="your_sub_cookie_value"
```

**Windows (PowerShell):**
```powershell
$env:WEIBO_SUBP="your_subp_cookie_value"
$env:WEIBO_SUB="your_sub_cookie_value"
```

### Method 2: Cookie File

Create `~/.weibo_cookies.json`:

```json
{
  "SUBP": "your_subp_cookie_value",
  "SUB": "your_sub_cookie_value"
}
```

### How to Get Cookies

1. Log into [weibo.com](https://weibo.com) in Chrome
2. Open DevTools (F12) → Application → Cookies
3. Find `weibo.com` domain
4. Copy `SUBP` and `SUB` values

## Usage

After installation, simply use natural language with your agent. The skill will be triggered automatically.

### Trigger Keywords

| Action | Trigger Phrases |
|--------|-----------------|
| Post Weibo | "post to Weibo", "发微博", "publish a Weibo" |
| Get Hot Search | "get hot search", "热搜", "trending topics", "微博热搜" |
| Analyze Trends | "analyze Weibo trends", "analyze hot search" |

### Examples

**Post a Weibo:**
```
"Post 'Hello, Weibo!' to Weibo"
"发一条微博：今天天气真好"
"帮我发微博，内容是：新功能上线啦 #科技#"
```

**Get Hot Search:**
```
"What's trending on Weibo?"
"查看微博热搜"
"Get the top 10 hot search topics"
"热搜榜前20"
```

**Analyze & Comment:**
```
"Analyze today's Weibo hot search trends"
"分析微博热搜趋势"
"Generate a comment based on hot search and post it"
```

### Comment Styles

When generating comments, you can specify a style:
- `neutral` - Balanced, informative style (default)
- `humorous` - Fun, casual style
- `professional` - Data-focused, formal style
- `simple` - Minimal, clean format

Example: "Generate a humorous comment based on hot search"

## API Reference

See [skills/weibo-automation/references/api-reference.md](./skills/weibo-automation/references/api-reference.md) for complete API documentation.

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 100001 | Login required | Refresh cookies |
| 100002 | Session expired | Re-login to Weibo |
| 100003 | Rate limited | Wait and retry |

## Rate Limits

| Operation | Limit | Window |
|-----------|-------|--------|
| Post tweet | 30 | 1 hour |
| Hot search | 60 | 1 minute |

## Security Notes

- Never share your cookies publicly
- Cookies expire periodically - refresh when needed
- Use environment variables for sensitive data in CI/CD

## License

MIT License
