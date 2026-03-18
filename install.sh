#!/bin/bash
# Weibo Automation Skill Installer
# Cross-platform installation script for Claude Code, OpenClaw, Codex, OpenCode, Trae, Qoder

#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/onepersonsecuritycompany/weibo-automation/main/install.sh | bash
#   curl -fsSL ... | bash -s -- claude  # Specify agent
#
# Or run directly:
#   ./install.sh --agent claude

set -e

REPO_URL="https://github.com/onepersonsecuritycompany/weibo-automation"
REPO_RAW="https://raw.githubusercontent.com/onepersonsecuritycompany/weibo-automation/main"

# Agent config directories
declare -A AGENT_DIRS=(
    ["claude"]="$HOME/.claude/skills"
    ["openclaw"]="$HOME/.openclaw/skills"
    ["codex"]="$HOME/.codex/skills"
    ["opencode"]="$HOME/.opencode/skills"
    ["trae"]="$HOME/.trae/skills"
    ["qoder"]="$HOME/.qoder/skills"
)

# Colors
RED='\033[0m'
GREEN='\033[0m'
YELLOW='\033[1m'
BLUE='\033[0m'
NC='\033[0m'

# Parse arguments
AGENT=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        -s|--agent)
            shift
            AGENT="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 --agent <agent_name>"
            echo ""
            echo "Available agents: ${!AGENT_DIRS[@]}"
            echo "  - ${AGENT_DIRS[@]}"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

# Detect agent if not specified
if [ -z "$AGENT" ]; then
    echo -e "${YELLOW}No agent specified, auto-detecting...${NC}"
    for agent in "${!AGENT_DIRS[@]}"; do
        if [ -d "${AGENT_DIRS[$agent]}" ]; then
            AGENT="$agent"
            echo -e "${GREEN}Detected: $agent${NC}"
            break
        fi
    done
fi

# Validate agent
if [ -z "$AGENT" ] || [ -z "${AGENT_DIRS[$AGENT]}" ]; then
    echo -e "${RED}Error: Unknown or unspecified agent.${NC}"
    echo -e "Available agents: ${!AGENT_DIRS[@]}"
    exit 1
fi

SKILL_DIR="${AGENT_DIRS[$AGENT]}/weibo-automation"

echo -e "${BLUE}Installing Weibo Automation Skill for $AGENT...${NC}"
echo ""

# Check if already installed
if [ -d "$SKILL_DIR" ]; then
    echo -e "${YELLOW}Warning: Skill already installed at $SKILL_DIR${NC}"
    read -p "Overwrite? (y/N) " -n 1 < /dev/tty
    if [[ "$REPLY" =~ ^[Yy]$ ]]; then
        rm -rf "$SKILL_DIR"
    else
        echo -e "${RED}Installation cancelled.${NC}"
        exit 1
    fi
fi

# Create directories
mkdir -p "$SKILL_DIR"
mkdir -p "$SKILL_DIR/scripts"
mkdir -p "$SKILL_DIR/references"

# Download files
echo -e "${BLUE}Downloading files...${NC}"

# Download SKILL.md
curl -fsSL "$REPO_RAW/skills/weibo-automation/SKILL.md" -o "$SKILL_DIR/SKILL.md" 2>/dev/null

# Download scripts
curl -fsSL "$REPO_RAW/skills/weibo-automation/scripts/post_weibo.py" -o "$SKILL_DIR/scripts/post_weibo.py" 2>/dev/null
curl -fsSL "$REPO_RAW/skills/weibo-automation/scripts/hot_search.py" -o "$SKILL_DIR/scripts/hot_search.py" 2>/dev/null

# Download references
curl -fsSL "$REPO_RAW/skills/weibo-automation/references/api-reference.md" -o "$SKILL_DIR/references/api-reference.md" 2>/dev/null

# Verify installation
if [ -f "$SKILL_DIR/SKILL.md" ] && [ -f "$SKILL_DIR/scripts/post_weibo.py" ]; then
    echo ""
    echo -e "${GREEN}✓ Successfully installed!${NC}"
    echo ""
    echo "  Location: $SKILL_DIR"
    echo ""
    echo "Next steps:"
    echo "  1. Set up cookies:"
    echo "     export WEIBO_SUBP='your_cookie'"
    echo "     export WEIBO_SUB='your_cookie'"
    echo ""
    echo "  2. Test installation:"
    echo "     python $SKILL_DIR/scripts/hot_search.py --limit 5"
    echo ""
else
    echo -e "${RED}✗ Installation failed. Please try manual install.${NC}"
    exit 1
fi
