# 微博自动化技能

一个强大的微博自动化操作技能，支持发微博和获取热搜趋势。

[English](./README.md)

## 功能特性

- **发布微博**：自动发布文字和图片微博
- **热搜获取**：实时获取微博热搜榜单
- **趋势分析**：智能分析热搜数据
- **自动评论**：基于热搜生成并发布评论

## 安装方法

### 快速安装（一键命令）

**macOS / Linux (Bash):**
```bash
# 自动检测 Agent 并安装
curl -fsSL https://raw.githubusercontent.com/onepersonsecuritycompany/weibo-automation/main/install.sh | bash

# 或指定 Agent: claude, openclaw, codex, opencode, trae, qoder
curl -fsSL https://raw.githubusercontent.com/onepersonsecuritycompany/weibo-automation/main/install.sh | bash -s -- claude
```

**Windows (PowerShell):**
```powershell
# 运行安装脚本（自动检测 Agent）
Invoke-Expression (Invoke-WebRequest -Uri "https://raw.githubusercontent.com/onepersonsecuritycompany/weibo-automation/main/install.ps1" -UseBasicParsing).Content
```

### 手动安装

**步骤 1:** 克隆仓库
```bash
git clone https://github.com/onepersonsecuritycompany/weibo-automation.git
```

**步骤 2:** 复制 skill 文件夹到 Agent 配置目录

| Agent | 配置目录 |
|-------|----------|
| Claude Code | `~/.claude/skills/weibo-automation/` |
| OpenClaw | `~/.openclaw/skills/weibo-automation/` |
| Codex | `~/.codex/skills/weibo-automation/` |
| OpenCode | `~/.opencode/skills/weibo-automation/` |
| Trae | `~/.trae/skills/weibo-automation/` |
| Qoder | `~/.qoder/skills/weibo-automation/` |

```bash
# macOS / Linux 示例
cp -r weibo-automation/skills/weibo-automation ~/.claude/skills/
```

```powershell
# Windows 示例
Copy-Item -Recurse -Path ".\weibo-automation\skills\weibo-automation" -Destination "$env:USERPROFILE\.claude\skills\weibo-automation"
```

### 依赖要求

- Python 3.8+
- `requests` 库： `pip install requests`

## 认证配置

### 方法一：环境变量（推荐）

**macOS / Linux:**
```bash
export WEIBO_SUBP="你的SUBP值"
export WEIBO_SUB="你的SUB值"
```

**Windows (PowerShell):**
```powershell
$env:WEIBO_SUBP="你的SUBP值"
$env:WEIBO_SUB="你的SUB值"
```

### 方法二：配置文件

创建 `~/.weibo_cookies.json` 文件：

```json
{
  "SUBP": "你的SUBP值",
  "SUB": "你的SUB值"
}
```

### 如何获取 Cookie

1. 在 Chrome 浏览器登录 [weibo.com](https://weibo.com)
2. 打开开发者工具 (F12) → Application → Cookies
3. 找到 `weibo.com` 域名。
4. 复制 `SUBP` 和 `SUB` 的值。

## 使用方法

安装完成后，直接用自然语言与 Agent 对话即可，技能会自动触发。

### 触发关键词

| 操作 | 触发短语 |
|------|----------|
| 发布微博 | "发微博"、"post to Weibo"、"发布一条微博" |
| 获取热搜 | "热搜"、"微博热搜"、"get hot search"、"trending topics" |
| 分析趋势 | "分析热搜"、"analyze hot search"、"热搜趋势分析" |

### 使用示例

**发布微博：**
```
"发微博：今天天气真好"
"帮我发一条微博，内容是：新功能上线啦 #科技#"
"Post 'Hello, Weibo!' to Weibo"
```

**获取热搜：**
```
"查看微博热搜"
"热搜榜前10条"
"微博上有什么热点？"
"What's trending on Weibo?"
```

**分析与评论：**
```
"分析今天的微博热搜趋势"
"根据热搜生成一条评论并发布"
"用幽默风格分析热搜"
```

### 评论风格

生成评论时可以指定风格：
- `neutral` - 中性、信息丰富风格（默认）
- `humorous` - 幽默、轻松风格
- `professional` - 专业、数据导向风格
- `simple` - 简洁、清爽风格

示例: "用幽默风格根据热搜生成一条评论"

## API 参考

完整 API 文档请参阅 [skills/weibo-automation/references/api-reference.md](./skills/weibo-automation/references/api-reference.md)

## 错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 100001 | 需要登录 | 刷新 Cookie |
| 100002 | 登录超时 | 重新登录微博 |
| 100003 | 操作频繁 | 稍后重试 |

## 频率限制

| 操作 | 限制 | 时间窗口 |
|------|------|----------|
| 发微博 | 30 次 | 1 小时 |
| 热搜获取 | 60 次 | 1 分钟 |

## 安全提示

- 切勿公开分享你的 Cookie
- Cookie 会定期过期，需要及时刷新
- 在 CI/CD 环境中使用环境变量存储敏感信息

## 许可证

MIT License
