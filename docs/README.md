# NodeSeek RSS 监控工具

[![Docker Pulls](https://img.shields.io/docker/pulls/xhh1128/ns-rss?style=for-the-badge&logo=docker)](https://hub.docker.com/r/xhh1128/ns-rss)
[![Docker Image Size](https://img.shields.io/docker/image-size/xhh1128/ns-rss/latest?style=for-the-badge&logo=docker)](https://hub.docker.com/r/xhh1128/ns-rss)
[![GitHub](https://img.shields.io/github/license/xhhcn/ns-rss?style=for-the-badge)](https://github.com/xhhcn/ns-rss/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/xhhcn/ns-rss?style=for-the-badge)](https://github.com/xhhcn/ns-rss/stargazers)

> 🚀 强大的 RSS 监控解决方案，支持多种筛选条件和 Telegram 推送

## ✨ 功能特性

<div class="feature-grid">

### 🔍 智能筛选
支持按类别和关键词精确筛选 RSS 内容，避免无用信息干扰。

### 📱 多群推送
支持同时推送到多个 Telegram 群组/频道，一次配置，多处接收。

### 🚀 Docker 部署
完整的 Docker 支持，一键部署，支持 linux/amd64 和 linux/arm64 架构。

### ⚡ 实时监控
可配置的检查间隔，实时获取最新内容，第一时间掌握动态。

### 🎯 智能去重
智能去重机制，避免重复推送，节省资源和通知频次。

### 🗂️ 自动清理
定时清理历史记录，防止存储空间无限增长，保持系统轻量。

</div>

## 🎯 使用场景

<div class="use-cases">

### 📊 服务器监控
- 实时监控 NodeSeek 的服务器优惠信息
- 筛选特定关键词的促销活动
- 第一时间获取黑五、双十一等活动信息

### 💡 技术学习
- 关注最新的技术分享和教程
- 筛选感兴趣的技术讨论
- 跟踪特定技术领域的动态

### 🤝 社区参与
- 监控感兴趣的讨论话题
- 及时参与热门话题讨论
- 关注社区重要公告

</div>

## 🚀 快速开始

?> 🎉 **一分钟即可完成部署！**

### 1️⃣ 获取 Telegram 配置

首先需要创建 Telegram 机器人并获取必要的配置信息：

1. **创建机器人**：在 Telegram 中找到 [@BotFather](https://t.me/BotFather)，发送 `/newbot` 创建机器人
2. **获取 Token**：按提示完成创建，记录 Bot Token
3. **获取 Chat ID**：将机器人添加到目标群组，发送 `/start`，然后访问 `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates` 获取 Chat ID

### 2️⃣ 一键部署

```bash
# 创建数据目录
mkdir -p ./data

# 启动容器
docker run -d \
  --name ns-rss-monitor \
  -e TG_BOT_TOKEN="your_bot_token_here" \
  -e TG_CHAT_ID='["your_chat_id_here"]' \
  -e CATEGORIES='["daily","review"]' \
  -e KEYWORDS='["VPS","测评"]' \
  -e WAIT_TIME=10 \
  -e CLEANUP_DAYS=7 \
  -v ./data:/app/data \
  --restart unless-stopped \
  xhh1128/ns-rss:latest
```

### 3️⃣ 验证部署

```bash
# 查看运行状态
docker ps | grep ns-rss

# 查看日志
docker logs -f ns-rss-monitor
```

## 🎨 配置示例

<div class="config-examples">

### 基础配置
```bash
# 最简配置，监控所有内容
TG_BOT_TOKEN="your_bot_token_here"
TG_CHAT_ID='["your_chat_id_here"]'
```

### 商家监控
```bash
# 专注商家促销信息
TG_BOT_TOKEN="your_bot_token_here"
TG_CHAT_ID='["your_chat_id_here"]'
CATEGORIES='["promotion"]'
KEYWORDS='["优惠","折扣","促销","黑五"]'
```

### 技术交流
```bash
# 关注技术讨论
TG_BOT_TOKEN="your_bot_token_here"
TG_CHAT_ID='["your_chat_id_here"]'
CATEGORIES='["tech","dev"]'
KEYWORDS='["Docker","Kubernetes","云原生"]'
```

### 多群推送
```bash
# 同时推送到多个群组
TG_BOT_TOKEN="your_bot_token_here"
TG_CHAT_ID='["group_1_id","group_2_id","channel_id"]'
CATEGORIES='["daily","review","tech"]'
```

</div>

## 📊 支持的内容类别

<div class="categories-grid">

| 类别 | 描述 | 示例用途 |
|------|------|----------|
| **daily** | 日常讨论 | 社区日常话题、生活分享 |
| **tech** | 技术分享 | 技术教程、开发经验 |
| **info** | 情报信息 | 行业动态、新闻资讯 |
| **review** | 测评报告 | 产品测评、服务评价 |
| **trade** | 交易信息 | 买卖交易、二手市场 |
| **carpool** | 拼车信息 | 出行拼车、费用分摊 |
| **dev** | 开发相关 | 开源项目、代码分享 |
| **photo-share** | 图片分享 | 摄影作品、图片展示 |
| **expose** | 曝光举报 | 问题曝光、维权举报 |
| **promotion** | 商家推广 | 优惠活动、产品推广 |

</div>

## 🔧 高级功能

### 🎯 精确筛选

支持多种筛选方式组合使用：

```bash
# 组合筛选：只关注测评类目中包含"VPS"的内容
CATEGORIES='["review"]'
KEYWORDS='["VPS","云服务器"]'

# 多关键词：任意关键词匹配即推送
KEYWORDS='["优惠","折扣","促销","限时"]'
```

### 🔄 自动清理

智能清理历史记录，防止存储膨胀：

```bash
# 保留最近 14 天的记录
CLEANUP_DAYS=14

# 每次启动时自动清理过期记录
# 系统会自动报告清理统计
```

### 📱 多平台支持

Docker 镜像支持多种架构：

- **linux/amd64**：适用于 x86_64 服务器
- **linux/arm64**：适用于 ARM64 服务器（如树莓派）

## 💡 使用技巧

### 🎯 关键词策略

1. **精确匹配**：使用具体的产品名称或技术术语
2. **组合筛选**：结合类别和关键词，提高精准度
3. **动态调整**：根据需求定期调整筛选条件

### 📊 监控优化

1. **合理间隔**：根据需求设置检查间隔，避免过于频繁
2. **多群管理**：不同内容推送到不同群组，便于管理
3. **定期清理**：设置合适的清理周期，保持系统性能

## 🤝 社区支持

<div class="community-links">

### 💬 交流讨论
- [GitHub Discussions](https://github.com/xhhcn/ns-rss/discussions) - 提问讨论
- [GitHub Issues](https://github.com/xhhcn/ns-rss/issues) - 问题反馈

### 📖 资源链接
- [Docker Hub](https://hub.docker.com/r/xhh1128/ns-rss) - 镜像仓库
- [GitHub Repository](https://github.com/xhhcn/ns-rss) - 源代码
- [NodeSeek 官网](https://nodeseek.com) - 内容源

### 🔧 贡献参与
- [贡献指南](contributing.md) - 参与项目开发
- [问题反馈](https://github.com/xhhcn/ns-rss/issues) - 提交 Bug
- [功能建议](https://github.com/xhhcn/ns-rss/discussions) - 提出新功能

</div>

---

<div align="center">
  <p>⭐ 如果这个项目对您有帮助，请给个 Star 支持一下！</p>
  <p>📧 问题反馈：<a href="https://github.com/xhhcn/ns-rss/issues">GitHub Issues</a></p>
  <p>🔗 项目地址：<a href="https://github.com/xhhcn/ns-rss">GitHub Repository</a></p>
</div>

<style>
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

.feature-grid > div {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid var(--theme-color);
}

.feature-grid h3 {
  margin-top: 0;
  color: var(--theme-color);
}

.use-cases {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.use-cases > div {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.use-cases h3 {
  margin-top: 0;
  color: white;
}

.config-examples {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

.config-examples > div {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.categories-grid {
  overflow-x: auto;
  margin: 2rem 0;
}

.categories-grid table {
  width: 100%;
  min-width: 600px;
}

.community-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.community-links > div {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
}

.community-links h3 {
  margin-top: 0;
  color: var(--theme-color);
}

@media (max-width: 768px) {
  .feature-grid,
  .use-cases,
  .config-examples,
  .community-links {
    grid-template-columns: 1fr;
  }
}
</style> 