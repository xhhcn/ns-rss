# 🚀 快速开始

> 🎉 **一分钟即可完成部署！**

## 📋 准备工作

### 1. 创建 Telegram 机器人

1. **找到 BotFather**：在 Telegram 中搜索 [@BotFather](https://t.me/BotFather)
2. **创建机器人**：发送 `/newbot` 命令
3. **设置名称**：按提示设置机器人名称和用户名
4. **获取 Token**：记录返回的 Bot Token

### 2. 获取 Chat ID

1. **添加机器人**：将机器人添加到目标群组或频道
2. **发送消息**：在群组中发送 `/start` 或任意消息
3. **获取 ID**：访问以下链接获取 Chat ID
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
4. **提取 ID**：在返回的 JSON 中找到 `"chat":{"id":123456789}`

?> 💡 **提示**：Chat ID 可能是负数（群组）或正数（私聊），都是正常的。

## 🚀 部署方式

### 方式一：Docker Run（推荐）

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

### 方式二：Docker Compose

1. **创建配置文件**：
   ```yaml
   # docker-compose.yml
   version: '3.8'
   services:
     ns-rss:
       image: xhh1128/ns-rss:latest
       container_name: ns-rss-monitor
       environment:
         - TG_BOT_TOKEN=your_bot_token_here
         - TG_CHAT_ID=["your_chat_id_here"]
         - CATEGORIES=["daily","review"]
         - KEYWORDS=["VPS","测评"]
         - WAIT_TIME=10
         - CLEANUP_DAYS=7
       volumes:
         - ./data:/app/data
       restart: unless-stopped
   ```

2. **启动服务**：
   ```bash
   docker-compose up -d
   ```

## ✅ 验证部署

### 检查运行状态

```bash
# 查看容器状态
docker ps | grep ns-rss

# 查看详细信息
docker inspect ns-rss-monitor
```

### 查看日志

```bash
# 查看实时日志
docker logs -f ns-rss-monitor

# 查看最近100行日志
docker logs --tail 100 ns-rss-monitor
```

### 正常运行的日志示例

```
================================================================================
开始新一轮RSS获取 - 2025-01-13 14:30:00
将获取 NodeSeek RSS 最新项目
配置信息：
  - 类别筛选: ['daily', 'review']
  - 关键词筛选: ['VPS', '测评']
  - 发送目标: 1 个聊天
  - 等待时间: 10 秒
================================================================================

正在处理 NodeSeek
目标 URL: https://rss.nodeseek.com/
--------------------------------------------------------------------------------
  正在使用 feedparser 获取 NodeSeek RSS 内容: https://rss.nodeseek.com/
  ✓ 成功获取内容 (状态码: 200)
  ✓ requests 会话已关闭
✓ 成功解析 NodeSeek RSS，共找到 20 个项目
  ✓ 筛选指定类别 ['daily', 'review']，从 20 个项目中筛选出 8 个
  ✓ 关键词筛选，从 8 个项目中筛选出 3 个
  📝 关键词列表: VPS, 测评
  ✓ 准备处理所有 3 个符合条件的项目
  🆕 发现新内容 [类别: review] [关键词: VPS]: 【测评】某某VPS性能测试报告...
  📤 正在发送第 1/3 个新内容...
  ✓ 消息已发送到Telegram (Chat ID: 123456789)
  ✓ 消息发送完成: 1/1 个聊天
  ✅ 成功发送 3/3 个新内容
  💾 已保存 3 条新记录

================================================================================
本轮处理完成！成功 - 2025-01-13 14:30:05
================================================================================

等待10秒后进行下一轮获取...
```

## 🎯 基础配置说明

### 必填参数

| 参数 | 描述 | 示例 |
|------|------|------|
| `TG_BOT_TOKEN` | Telegram 机器人 Token | `123456:ABC-DEF1234ghIkl` |
| `TG_CHAT_ID` | 聊天 ID（JSON 数组格式） | `["123456789"]` |

### 可选参数

| 参数 | 描述 | 默认值 | 示例 |
|------|------|--------|------|
| `CATEGORIES` | 类别筛选 | 全部 | `["daily","review"]` |
| `KEYWORDS` | 关键词筛选 | 无 | `["VPS","测评"]` |
| `WAIT_TIME` | 检查间隔（秒） | 5 | `10` |
| `CLEANUP_DAYS` | 历史记录保留天数 | 7 | `14` |

## 🔧 常见问题

### Q: 如何监控多个群组？

A: 在 `TG_CHAT_ID` 中添加多个 Chat ID：
```bash
TG_CHAT_ID='["123456789","987654321","-1001234567890"]'
```

### Q: 如何只监控特定类别？

A: 设置 `CATEGORIES` 参数：
```bash
CATEGORIES='["promotion","review"]'
```

### Q: 如何添加关键词筛选？

A: 设置 `KEYWORDS` 参数：
```bash
KEYWORDS='["VPS","优惠","测评"]'
```

### Q: 如何调整检查频率？

A: 设置 `WAIT_TIME` 参数（单位：秒）：
```bash
WAIT_TIME=30  # 30秒检查一次
```

## 🎉 部署成功！

如果看到类似上述的日志输出，说明部署成功！现在您可以：

1. 🔍 在 Telegram 中查看推送的消息
2. 🔧 根据需要调整配置参数
3. 📊 监控日志确保正常运行
4. 🎯 根据实际需求优化筛选条件

## 📈 下一步

- 📖 查看 [完整文档](guide.md) 了解更多功能
- 🔧 查看 [配置说明](configuration.md) 进行高级配置
- 🐳 查看 [Docker 部署](docker.md) 了解更多部署选项
- ❓ 查看 [常见问题](faq.md) 解决使用中的问题

---

?> 🎉 **恭喜！** 您已成功部署 NodeSeek RSS 监控工具！如有问题，请查看 [故障排除](troubleshooting.md) 或提交 [Issues](https://github.com/xhhcn/ns-rss/issues)。 