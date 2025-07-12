# ❓ 常见问题

> 🔧 **常见问题解答与故障排除**

## 🚀 部署相关

### Q: 如何获取 Telegram Bot Token？

**A:** 
1. 在 Telegram 中搜索 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 命令创建机器人
3. 按提示设置机器人名称和用户名
4. 获取返回的 Token（格式：`123456:ABC-DEF1234ghIkl`）

### Q: 如何获取 Chat ID？

**A:**
1. 将机器人添加到目标群组或频道
2. 在群组中发送一条消息（任意内容）
3. 访问：`https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. 在返回的JSON中找到 `"chat":{"id":123456789}`

?> 💡 **提示**：群组 ID 通常是负数，私聊 ID 是正数，频道 ID 以 `-100` 开头。

### Q: 容器启动失败怎么办？

**A:**
```bash
# 查看容器状态
docker ps -a | grep ns-rss

# 查看错误日志
docker logs ns-rss-monitor

# 检查配置
docker inspect ns-rss-monitor
```

常见原因：
- 环境变量格式错误
- Bot Token 无效
- Chat ID 格式错误
- 网络连接问题

## 📱 功能使用

### Q: 如何只监控特定类别？

**A:**
```bash
# 只监控商家推广
CATEGORIES='["promotion"]'

# 监控多个类别
CATEGORIES='["daily","review","tech"]'

# 监控所有类别（默认）
CATEGORIES=''
```

### Q: 如何设置关键词筛选？

**A:**
```bash
# 单个关键词
KEYWORDS='["VPS"]'

# 多个关键词（任意匹配）
KEYWORDS='["VPS","优惠","测评","限时"]'

# 无关键词筛选（默认）
KEYWORDS=''
```

### Q: 如何推送到多个群组？

**A:**
```bash
# 推送到多个群组
TG_CHAT_ID='["123456789","987654321","-1001234567890"]'

# 支持的格式
TG_CHAT_ID='["私聊ID","群组ID","频道ID","@频道用户名"]'
```

### Q: 如何调整检查频率？

**A:**
```bash
# 设置检查间隔（秒）
WAIT_TIME=30  # 30秒检查一次

# 建议值
WAIT_TIME=5   # 测试环境
WAIT_TIME=30  # 生产环境
WAIT_TIME=300 # 低频监控
```

## 🔧 配置问题

### Q: 环境变量格式错误？

**A:**
JSON 数组格式必须使用双引号和方括号：

```bash
# ✅ 正确格式
TG_CHAT_ID='["123456789","987654321"]'
CATEGORIES='["daily","review"]'
KEYWORDS='["VPS","测评"]'

# ❌ 错误格式
TG_CHAT_ID=[123456789,987654321]
CATEGORIES=["daily","review"]
KEYWORDS=VPS,测评
```

### Q: 如何在 Docker Compose 中使用单引号？

**A:**
```yaml
# docker-compose.yml
environment:
  - TG_BOT_TOKEN=your_bot_token_here
  - 'TG_CHAT_ID=["123456789","987654321"]'
  - 'CATEGORIES=["daily","review"]'
  - 'KEYWORDS=["VPS","测评"]'
```

### Q: 配置修改后不生效？

**A:**
配置修改后需要重启容器：

```bash
# Docker Run
docker restart ns-rss-monitor

# Docker Compose
docker-compose restart ns-rss
```

## 🌐 网络问题

### Q: 无法连接到 Telegram API？

**A:**
检查网络连接：

```bash
# 测试 Telegram API 连接
curl -I https://api.telegram.org

# 测试 RSS 源连接
curl -I https://rss.nodeseek.com/

# 检查 DNS 解析
nslookup api.telegram.org
nslookup rss.nodeseek.com
```

### Q: 在国内服务器上使用？

**A:**
可能需要配置代理：

```bash
# 设置代理（如果需要）
docker run -d \
  --name ns-rss-monitor \
  -e TG_BOT_TOKEN="your_bot_token_here" \
  -e TG_CHAT_ID='["your_chat_id_here"]' \
  -e HTTP_PROXY="http://proxy:port" \
  -e HTTPS_PROXY="http://proxy:port" \
  xhh1128/ns-rss:latest
```

## 🗂️ 数据相关

### Q: 历史记录文件在哪里？

**A:**
```bash
# 在容器内
/app/data/last_sent.json

# 在宿主机（如果挂载了卷）
./data/last_sent.json
```

### Q: 如何清理历史记录？

**A:**
```bash
# 手动清理
docker exec ns-rss-monitor rm -f /app/data/last_sent.json

# 自动清理（配置保留天数）
CLEANUP_DAYS=7  # 保留7天记录
```

### Q: 数据备份和恢复？

**A:**
```bash
# 备份数据
docker cp ns-rss-monitor:/app/data/last_sent.json ./backup/

# 恢复数据
docker cp ./backup/last_sent.json ns-rss-monitor:/app/data/
```

## 📊 性能优化

### Q: 内存使用过高？

**A:**
```bash
# 查看内存使用
docker stats ns-rss-monitor

# 设置内存限制
docker run -d \
  --name ns-rss-monitor \
  --memory="128m" \
  -e TG_BOT_TOKEN="your_bot_token_here" \
  -e TG_CHAT_ID='["your_chat_id_here"]' \
  xhh1128/ns-rss:latest
```

### Q: 如何减少资源消耗？

**A:**
```bash
# 增加检查间隔
WAIT_TIME=60  # 60秒检查一次

# 减少历史记录保留时间
CLEANUP_DAYS=3  # 只保留3天

# 精确筛选，减少处理量
CATEGORIES='["promotion"]'
KEYWORDS='["VPS"]'
```

## 🔍 调试相关

### Q: 如何查看详细日志？

**A:**
```bash
# 查看实时日志
docker logs -f ns-rss-monitor

# 查看最近日志
docker logs --tail 100 ns-rss-monitor

# 查看指定时间日志
docker logs --since="2025-01-13T14:00:00" ns-rss-monitor
```

### Q: 如何进入容器调试？

**A:**
```bash
# 进入运行中的容器
docker exec -it ns-rss-monitor /bin/bash

# 以交互模式启动新容器
docker run -it --rm \
  -e TG_BOT_TOKEN="your_bot_token_here" \
  -e TG_CHAT_ID='["your_chat_id_here"]' \
  xhh1128/ns-rss:latest /bin/bash
```

### Q: 如何测试配置？

**A:**
```bash
# 测试 Bot Token
curl -s "https://api.telegram.org/bot$TG_BOT_TOKEN/getMe"

# 测试发送消息
curl -s -X POST "https://api.telegram.org/bot$TG_BOT_TOKEN/sendMessage" \
  -d chat_id="$TG_CHAT_ID" \
  -d text="测试消息"

# 测试 RSS 源
curl -s "https://rss.nodeseek.com/" | head -20
```

## 🔄 更新升级

### Q: 如何更新到最新版本？

**A:**
```bash
# 停止容器
docker stop ns-rss-monitor

# 删除旧容器
docker rm ns-rss-monitor

# 拉取最新镜像
docker pull xhh1128/ns-rss:latest

# 启动新容器
docker run -d \
  --name ns-rss-monitor \
  -e TG_BOT_TOKEN="your_bot_token_here" \
  -e TG_CHAT_ID='["your_chat_id_here"]' \
  -v ./data:/app/data \
  --restart unless-stopped \
  xhh1128/ns-rss:latest
```

### Q: 如何回滚到旧版本？

**A:**
```bash
# 使用特定版本
docker run -d \
  --name ns-rss-monitor \
  -e TG_BOT_TOKEN="your_bot_token_here" \
  -e TG_CHAT_ID='["your_chat_id_here"]' \
  xhh1128/ns-rss:v1.0  # 指定版本
```

## 🚨 错误处理

### Q: "TG_BOT_TOKEN 环境变量不能为空" 错误？

**A:**
检查环境变量设置：

```bash
# 检查变量是否设置
echo $TG_BOT_TOKEN

# 确保格式正确
TG_BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
```

### Q: "TG_CHAT_ID 环境变量不能为空" 错误？

**A:**
检查 Chat ID 设置：

```bash
# 检查变量是否设置
echo $TG_CHAT_ID

# 确保格式正确
TG_CHAT_ID='["123456789"]'
```

### Q: "消息发送失败" 错误？

**A:**
可能的原因：
1. Bot Token 无效
2. Chat ID 错误
3. 机器人未被添加到群组
4. 网络连接问题

```bash
# 检查 Bot 权限
curl -s "https://api.telegram.org/bot$TG_BOT_TOKEN/getMe"

# 检查 Chat 权限
curl -s "https://api.telegram.org/bot$TG_BOT_TOKEN/getChat" \
  -d chat_id="$TG_CHAT_ID"
```

## 📞 获取帮助

如果以上解答没有解决您的问题，您可以：

1. 📖 查看 [完整文档](guide.md)
2. 🔧 查看 [故障排除](troubleshooting.md)
3. 💬 在 [GitHub Discussions](https://github.com/xhhcn/ns-rss/discussions) 提问
4. 🐛 在 [GitHub Issues](https://github.com/xhhcn/ns-rss/issues) 报告问题

---

?> 💡 **提示**：请在提问时提供详细的错误信息和配置，这样我们能更好地帮助您解决问题。 