# NodeSeek RSS 监控工具

<div align="center">

![Docker Pulls](https://img.shields.io/docker/pulls/xhh1128/ns-rss?style=flat-square&logo=docker&logoColor=white)
![Image Size](https://img.shields.io/docker/image-size/xhh1128/ns-rss?style=flat-square&logo=docker&logoColor=white)
![License](https://img.shields.io/github/license/xhhcn/ns-rss?style=flat-square)
![Stars](https://img.shields.io/github/stars/xhhcn/ns-rss?style=flat-square)

**🚀 高效、智能的 NodeSeek RSS 监控与 Telegram 推送工具**

[快速开始](#快速开始) • [Docker 部署](#docker-部署) • [配置说明](#配置说明)

</div>

## ✨ 功能特性

- 🔍 **智能筛选**: 支持按类别和关键词筛选 RSS 内容
- 📱 **多群推送**: 支持同时推送到多个 Telegram 群组/频道
- 🚀 **Docker 部署**: 完整的 Docker 支持，一键部署
- ⚡ **实时监控**: 可配置的检查间隔，实时获取最新内容
- 🎯 **去重机制**: 智能去重，避免重复推送
- 🗂️ **存储优化**: 自动清理历史记录，防止存储空间无限增长

## 🏷️ 支持的类别

| 类别 | 标题 |
|------|------|
| `daily` | 🔔 **NodeSeek日常帖子** |
| `tech` | 🔔 **NodeSeek技术帖子** |
| `info` | 🔔 **NodeSeek情报帖子** |
| `review` | 🔔 **NodeSeek测评帖子** |
| `trade` | 🔔 **NodeSeek交易帖子** |
| `carpool` | 🔔 **NodeSeek拼车帖子** |
| `dev` | 🔔 **NodeSeek dev帖子** |
| `photo-share` | 🔔 **NodeSeek贴图帖子** |
| `expose` | 🔔 **NodeSeek曝光帖子** |
| `promotion` | 🔔 **NodeSeek商家信息** |

## 🚀 快速开始

### 环境变量配置

| 变量名 | 说明 | 必填 | 示例 |
|--------|------|------|------|
| `TG_BOT_TOKEN` | Telegram Bot Token | ✅ | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `TG_CHAT_ID` | Telegram 聊天 ID | ✅ | `["123456789","987654321"]` |
| `CATEGORIES` | RSS 类别筛选 | ❌ | `["promotion","tech","info"]` |
| `KEYWORDS` | 关键词筛选 | ❌ | `["优惠","活动","促销"]` |
| `WAIT_TIME` | 检查间隔（秒） | ❌ | `5` |
| `CLEANUP_DAYS` | 历史记录保留天数 | ❌ | `7` |

## 🐳 Docker 部署

### 方式一：Docker Run

```bash
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

1. **下载 docker-compose.yml**
   ```bash
   curl -O https://raw.githubusercontent.com/xhhcn/ns-rss/main/docker-compose.yml
   ```

2. **修改环境变量**
   ```yaml
   services:
     ns-rss:
       image: xhh1128/ns-rss:latest
       container_name: ns-rss-monitor
       environment:
         - TG_BOT_TOKEN=your_bot_token_here
         - 'TG_CHAT_ID=["your_chat_id_here"]'
         - 'CATEGORIES=["daily","review"]'
         - 'KEYWORDS=["关键词1","关键词2"]'
         - WAIT_TIME=5
         - CLEANUP_DAYS=7
       volumes:
         - ./data:/app/data
       restart: unless-stopped
   ```

3. **启动服务**
   ```bash
   docker-compose up -d
   ```

## ⚙️ 配置说明

### 格式支持

支持 **JSON 数组格式**（推荐）和**逗号分隔格式**：

```env
# JSON 数组格式 (推荐)
TG_CHAT_ID=["123456789","987654321"]
CATEGORIES=["promotion","tech"]
KEYWORDS=["优惠","活动"]

# 逗号分隔格式 (兼容)
TG_CHAT_ID=123456789,987654321
CATEGORIES=promotion,tech
KEYWORDS=优惠,活动
```

### 配置示例

<details>
<summary>点击查看更多配置示例</summary>

#### 只监控商家信息
```env
CATEGORIES=["promotion"]
KEYWORDS=
```

#### 监控特定关键词
```env
CATEGORIES=
KEYWORDS=["优惠","促销","活动","黑五"]
```

#### 多群组推送
```env
TG_CHAT_ID=["-1001234567890","-1001234567891","@channel_username"]
```

</details>

## 📊 管理命令

```bash
# 查看日志
docker-compose logs -f ns-rss

# 重启服务
docker-compose restart ns-rss

# 停止服务
docker-compose stop ns-rss

# 更新镜像
docker-compose pull && docker-compose up -d
```

## 🔧 故障排除

| 问题 | 解决方案 |
|------|----------|
| 消息发送失败 | 检查 Bot Token 和 Chat ID 是否正确 |
| 无法获取 RSS | 检查网络连接和 RSS 源地址 |
| Docker 启动失败 | 检查环境变量配置，查看日志 |

## 📄 许可证

MIT License

---

<div align="center">
⭐ 如果这个项目对您有帮助，请给个 Star 支持一下！
</div> 