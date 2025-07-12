# NodeSeek RSS 监控工具

<div align="center">

[![Docker Pulls](https://img.shields.io/docker/pulls/xhh1128/ns-rss?style=for-the-badge&logo=docker)](https://hub.docker.com/r/xhh1128/ns-rss)
[![Docker Image Size](https://img.shields.io/docker/image-size/xhh1128/ns-rss/latest?style=for-the-badge&logo=docker)](https://hub.docker.com/r/xhh1128/ns-rss)
[![GitHub](https://img.shields.io/github/license/xhhcn/ns-rss?style=for-the-badge)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/xhhcn/ns-rss?style=for-the-badge)](https://github.com/xhhcn/ns-rss/stargazers)

**🚀 高效、智能的 NodeSeek RSS 监控与 Telegram 推送工具**

[快速开始](#-快速开始) • [Docker 部署](#-docker-部署) • [配置说明](#-配置说明)

</div>

## ✨ 功能特性

- 🔍 **智能筛选**: 支持按类别和关键词筛选 RSS 内容
- 📱 **多群推送**: 支持同时推送到多个 Telegram 群组/频道
- 🚀 **Docker 部署**: 完整的 Docker 支持，一键部署
- ⚡ **实时监控**: 可配置的检查间隔，实时获取最新内容
- 🎯 **去重机制**: 智能去重，避免重复推送
- 🗂️ **存储优化**: 自动清理历史记录，防止存储空间无限增长

## 🏷️ 支持的类别

<div align="center">

| 类别 | 标题 | 类别 | 标题 |
|------|------|------|------|
| **`daily`** | 🔔 **NodeSeek日常帖子** | **`tech`** | 🔔 **NodeSeek技术帖子** |
| **`info`** | 🔔 **NodeSeek情报帖子** | **`review`** | 🔔 **NodeSeek测评帖子** |
| **`trade`** | 🔔 **NodeSeek交易帖子** | **`carpool`** | 🔔 **NodeSeek拼车帖子** |
| **`dev`** | 🔔 **NodeSeek dev帖子** | **`photo-share`** | 🔔 **NodeSeek贴图帖子** |
| **`expose`** | 🔔 **NodeSeek曝光帖子** | **`promotion`** | 🔔 **NodeSeek商家信息** |

</div>

## 🚀 快速开始

[![Deploy on Docker](https://img.shields.io/badge/Deploy%20on-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/xhh1128/ns-rss)

### 1. 获取 Telegram Bot Token

1. 在 Telegram 中找到 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 创建新机器人
3. 按提示设置机器人名称和用户名
4. 获取 Bot Token

### 2. 获取 Chat ID

1. 将机器人添加到目标群组或频道
2. 发送一条消息 `/start`
3. 访问 `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. 在返回的JSON中找到 `chat` → `id`

## 🐳 Docker 部署

### 方式一：Docker Run

```bash
# 创建数据目录
mkdir -p ./data

# 运行容器
docker run -d \
  --name ns-rss \
  -e TG_BOT_TOKEN="your_bot_token_here" \
  -e TG_CHAT_ID='["your_chat_id_here"]' \
  -e CATEGORIES='["daily","review"]' \
  -e KEYWORDS='["关键词1","关键词2"]' \
  -e WAIT_TIME=5 \
  -e CLEANUP_DAYS=7 \
  -v ./data:/app/data \
  --restart unless-stopped \
  xhh1128/ns-rss:latest
```

### 方式二：Docker Compose

1. 创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  ns-rss:
    image: xhh1128/ns-rss:latest
    container_name: ns-rss-monitor
    environment:
      # 必填：Telegram Bot Token
      - TG_BOT_TOKEN=your_bot_token_here
      # 必填：Telegram Chat ID (JSON数组格式)
      - TG_CHAT_ID=["your_chat_id_here"]
      # 可选：RSS 类别筛选 (JSON数组格式)
      - CATEGORIES=["daily","review"]
      # 可选：关键词筛选 (JSON数组格式)
      - KEYWORDS=["关键词1","关键词2"]
      # 可选：等待时间（秒），默认5秒
      - WAIT_TIME=5
      # 可选：历史记录保留天数，默认7天
      - CLEANUP_DAYS=7
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

2. 启动服务：

```bash
docker-compose up -d
```

## ⚙️ 配置说明

<div align="center">

| 环境变量 | 类型 | 必填 | 默认值 | 说明 |
|----------|------|------|--------|------|
| **`TG_BOT_TOKEN`** | `String` | ✅ | - | Telegram Bot Token |
| **`TG_CHAT_ID`** | `JSON Array` | ✅ | - | 聊天ID列表，如 `["123","456"]` |
| **`CATEGORIES`** | `JSON Array` | ❌ | 全部 | 类别筛选，如 `["daily","review"]` |
| **`KEYWORDS`** | `JSON Array` | ❌ | 无 | 关键词筛选，如 `["关键词1","关键词2"]` |
| **`WAIT_TIME`** | `Integer` | ❌ | `5` | 检查间隔（秒） |
| **`CLEANUP_DAYS`** | `Integer` | ❌ | `7` | 历史记录保留天数 |

</div>

<details>
<summary>📋 配置示例</summary>

### 基础配置
```bash
TG_BOT_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
TG_CHAT_ID=["123456789"]
```

### 完整配置
```bash
TG_BOT_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
TG_CHAT_ID=["123456789", "987654321"]
CATEGORIES=["daily","tech","review"]
KEYWORDS=["VPS","服务器","测评"]
WAIT_TIME=10
CLEANUP_DAYS=14
```

### 监控特定内容
```bash
# 只监控日常和测评帖子
CATEGORIES=["daily","review"]

# 只推送包含特定关键词的内容
KEYWORDS=["只测不评","性能测试"]

# 组合使用：监控测评帖子中包含"VPS"的内容
CATEGORIES=["review"]
KEYWORDS=["VPS"]
```

</details>

## 📊 使用统计

- 🐳 **Docker 镜像**: 多平台支持 (linux/amd64, linux/arm64)
- 💾 **存储优化**: 自动清理历史记录，防止无限增长
- 🔄 **实时监控**: 可配置检查间隔，实时获取最新内容
- 📱 **多群推送**: 支持同时推送到多个 Telegram 群组

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目使用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🔗 相关链接

- [NodeSeek 官网](https://nodeseek.com)
- [Docker Hub](https://hub.docker.com/r/xhh1128/ns-rss)
- [GitHub Repository](https://github.com/xhhcn/ns-rss) 