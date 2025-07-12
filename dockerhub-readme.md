# NodeSeek RSS 监控工具

<div align="center">

**🚀 高效、智能的 NodeSeek RSS 监控与 Telegram 推送工具**

[![GitHub](https://img.shields.io/badge/GitHub-xhhcn/ns--rss-blue?style=flat-square&logo=github)](https://github.com/xhhcn/ns-rss)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](https://github.com/xhhcn/ns-rss/blob/main/LICENSE)

</div>

## 🌟 功能特性

- 🔍 **智能筛选**: 支持按类别和关键词筛选 RSS 内容
- 📱 **多群推送**: 支持同时推送到多个 Telegram 群组/频道
- ⚡ **实时监控**: 可配置的检查间隔，实时获取最新内容
- 🎯 **去重机制**: 智能去重，避免重复推送
- 🗂️ **存储优化**: 自动清理历史记录，防止存储空间无限增长
- 🐳 **多平台支持**: 支持 linux/amd64 和 linux/arm64 架构

## 🚀 快速开始

### 基础运行

```bash
docker run -d \
  --name ns-rss \
  -e TG_BOT_TOKEN="your_bot_token_here" \
  -e TG_CHAT_ID='["your_chat_id_here"]' \
  -v ./data:/app/data \
  --restart unless-stopped \
  xhh1128/ns-rss:latest
```

### 高级配置

```bash
docker run -d \
  --name ns-rss \
  -e TG_BOT_TOKEN="your_bot_token_here" \
  -e TG_CHAT_ID='["123456789","987654321"]' \
  -e CATEGORIES='["daily","review","tech"]' \
  -e KEYWORDS='["VPS","服务器","测评"]' \
  -e WAIT_TIME=10 \
  -e CLEANUP_DAYS=7 \
  -v ./data:/app/data \
  --restart unless-stopped \
  xhh1128/ns-rss:latest
```

## ⚙️ 环境变量

| 变量名 | 说明 | 必填 | 示例 |
|--------|------|------|------|
| `TG_BOT_TOKEN` | Telegram Bot Token | ✅ | `123456:ABC-DEF1234ghIkl` |
| `TG_CHAT_ID` | Telegram 聊天 ID (JSON数组) | ✅ | `["123456789"]` |
| `CATEGORIES` | RSS 类别筛选 (JSON数组) | ❌ | `["daily","review"]` |
| `KEYWORDS` | 关键词筛选 (JSON数组) | ❌ | `["VPS","测评"]` |
| `WAIT_TIME` | 检查间隔（秒） | ❌ | `5` |
| `CLEANUP_DAYS` | 历史记录保留天数 | ❌ | `7` |

## 🏷️ 支持的类别

- **daily**: 日常帖子
- **tech**: 技术帖子  
- **info**: 情报帖子
- **review**: 测评帖子
- **trade**: 交易帖子
- **carpool**: 拼车帖子
- **dev**: 开发帖子
- **photo-share**: 贴图帖子
- **expose**: 曝光帖子
- **promotion**: 商家信息

## 🔧 获取配置信息

### 获取 Telegram Bot Token
1. 在 Telegram 中找到 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 创建新机器人
3. 按提示设置机器人名称和用户名
4. 获取 Bot Token

### 获取 Chat ID
1. 将机器人添加到目标群组或频道
2. 发送一条消息 `/start`
3. 访问 `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. 在返回的JSON中找到 `chat` → `id`

## 📊 数据存储

- 数据文件存储在 `/app/data/last_sent.json`
- 建议挂载 `./data:/app/data` 以持久化数据
- 自动清理过期记录，防止文件无限增长

## 🔗 相关链接

- **GitHub 仓库**: [https://github.com/xhhcn/ns-rss](https://github.com/xhhcn/ns-rss)
- **完整文档**: [README.md](https://github.com/xhhcn/ns-rss/blob/main/README.md)
- **NodeSeek 官网**: [https://nodeseek.com](https://nodeseek.com)
- **许可证**: MIT License

## 🐳 Docker 标签

- `latest`: 最新稳定版本
- `v1.0`: 版本 1.0
- 支持多架构: `linux/amd64`, `linux/arm64`

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给个 Star 支持一下！**

[GitHub Repository](https://github.com/xhhcn/ns-rss) • [Issues](https://github.com/xhhcn/ns-rss/issues) • [Pull Requests](https://github.com/xhhcn/ns-rss/pulls)

</div> 