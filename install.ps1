# Weibo Automation Skill Installer for Windows
# Cross-platform installation script for Claude Code, OpenClaw, Codex, OpenCode, Trae, Qoder
#
# Usage:
#   Invoke-Expression (Invoke-WebRequest -Uri "https://raw.githubusercontent.com/onepersonsecuritycompany/weibo-automation/main/install.ps1" -UseBasicParsing).Content
#
# Or run directly:
#   .\install.ps1 -Agent claude

param(
    [string]$Agent = "",
    [switch]$Help
)

$RepoRaw = "https://raw.githubusercontent.com/onepersonsecuritycompany/weibo-automation/main"

# Agent config directories
$AgentDirs = @{
    "claude"    = "$env:USERPROFILE\.claude\skills"
    "openclaw"  = "$env:USERPROFILE\.openclaw\skills"
    "codex"     = "$env:USERPROFILE\.codex\skills"
    "opencode"  = "$env:USERPROFILE\.opencode\skills"
    "trae"      = "$env:USERPROFILE\.trae\skills"
    "qoder"     = "$env:USERPROFILE\.qoder\skills"
}

function Write-Info { Write-Host "[INFO] $args" -ForegroundColor Green }
function Write-Warn { Write-Host "[WARN] $args" -ForegroundColor Yellow }
function Write-Err  { Write-Host "[ERROR] $args" -ForegroundColor Red; exit 1 }

if ($Help) {
    Write-Host "Usage: .\install.ps1 -Agent <agent_name>"
    Write-Host ""
    Write-Host "Available agents: $($AgentDirs.Keys -join ', ')"
    exit 0
}

# Auto-detect agent if not specified
if ($Agent -eq "") {
    Write-Host "No agent specified, auto-detecting..." -ForegroundColor Yellow
    foreach ($key in $AgentDirs.Keys) {
        if (Test-Path (Split-Path $AgentDirs[$key] -Parent)) {
            $Agent = $key
            Write-Host "Detected: $Agent" -ForegroundColor Green
            break
        }
    }
}

# Validate agent
if ($Agent -eq "" -or -not $AgentDirs.ContainsKey($Agent)) {
    Write-Err "Unknown agent. Available: $($AgentDirs.Keys -join ', ')"
}

$SkillDir = "$($AgentDirs[$Agent])\weibo-automation"

Write-Host "Installing Weibo Automation Skill for $Agent..." -ForegroundColor Cyan
Write-Host ""

# Check if already installed
if (Test-Path $SkillDir) {
    Write-Warn "Skill already installed at $SkillDir"
    $confirm = Read-Host "Overwrite? (y/N)"
    if ($confirm -ne "y" -and $confirm -ne "Y") {
        Write-Err "Installation cancelled."
    }
    Remove-Item -Recurse -Force $SkillDir
}

# Create directories
New-Item -ItemType Directory -Force -Path "$SkillDir\scripts" | Out-Null
New-Item -ItemType Directory -Force -Path "$SkillDir\references" | Out-Null

# Download files
Write-Info "Downloading files..."

function Download-File {
    param($Url, $Output)
    try {
        Invoke-WebRequest -Uri $Url -OutFile $Output -UseBasicParsing
    } catch {
        Write-Err "Failed to download: $Url"
    }
}

Download-File "$RepoRaw/skills/weibo-automation/SKILL.md" "$SkillDir\SKILL.md"
Download-File "$RepoRaw/skills/weibo-automation/scripts/post_weibo.py" "$SkillDir\scripts\post_weibo.py"
Download-File "$RepoRaw/skills/weibo-automation/scripts/hot_search.py" "$SkillDir\scripts\hot_search.py"
Download-File "$RepoRaw/skills/weibo-automation/references/api-reference.md" "$SkillDir\references\api-reference.md"

# Verify installation
if ((Test-Path "$SkillDir\SKILL.md") -and (Test-Path "$SkillDir\scripts\post_weibo.py")) {
    Write-Host ""
    Write-Info "Successfully installed!"
    Write-Host ""
    Write-Host "  Location: $SkillDir"
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. Set up cookies:"
    Write-Host "     `$env:WEIBO_SUBP='your_cookie'"
    Write-Host "     `$env:WEIBO_SUB='your_cookie'"
    Write-Host ""
    Write-Host "  2. Test installation:"
    Write-Host "     python $SkillDir\scripts\hot_search.py --limit 5"
    Write-Host ""
} else {
    Write-Err "Installation failed. Please try manual install."
}
