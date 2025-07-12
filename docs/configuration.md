# ⚙️ 配置说明

> 🔧 **详细的环境变量配置指南**

## 📋 完整配置列表

### 必填配置

| 变量名 | 类型 | 描述 | 示例 |
|--------|------|------|------|
| `TG_BOT_TOKEN` | String | Telegram Bot Token | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `TG_CHAT_ID` | JSON Array | Telegram 聊天 ID 列表 | `["123456789","-1001234567890"]` |

### 可选配置

| 变量名 | 类型 | 默认值 | 描述 | 示例 |
|--------|------|--------|------|------|
| `CATEGORIES` | JSON Array | 全部 | RSS 类别筛选 | `["daily","review","tech"]` |
| `KEYWORDS` | JSON Array | 无 | 关键词筛选 | `["VPS","优惠","测评"]` |
| `WAIT_TIME` | Integer | 5 | 检查间隔（秒） | `10` |
| `CLEANUP_DAYS` | Integer | 7 | 历史记录保留天数 | `14` |

## 🔧 配置详解

### TG_BOT_TOKEN

Telegram 机器人的访问令牌，用于发送消息。

**获取方式：**
1. 在 Telegram 中搜索 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 创建机器人
3. 按提示设置名称和用户名
4. 获取返回的 Token

**格式：**
```bash
TG_BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
```

### TG_CHAT_ID

接收消息的 Telegram 聊天 ID，支持多个目标。

**支持的类型：**
- 私聊：正数 ID
- 群组：负数 ID
- 频道：以 `-100` 开头的 ID

**获取方式：**
1. 将机器人添加到目标群组
2. 发送一条消息
3. 访问 `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. 在响应中找到 `chat.id`

**格式：**
```bash
# 单个聊天
TG_CHAT_ID='["123456789"]'

# 多个聊天
TG_CHAT_ID='["123456789","987654321","-1001234567890"]'
```

### CATEGORIES

筛选特定类别的 RSS 内容。

**支持的类别：**
- `daily` - 日常讨论
- `tech` - 技术分享
- `info` - 情报信息
- `review` - 测评报告
- `trade` - 交易信息
- `carpool` - 拼车信息
- `dev` - 开发相关
- `photo-share` - 图片分享
- `expose` - 曝光举报
- `promotion` - 商家推广

**格式：**
```bash
# 监控所有类别（默认）
CATEGORIES=''

# 监控特定类别
CATEGORIES='["daily","review","tech"]'

# 只监控商家推广
CATEGORIES='["promotion"]'
```

### KEYWORDS

按关键词筛选内容，支持多个关键词。

**匹配规则：**
- 不区分大小写
- 包含匹配（部分匹配）
- 任意关键词匹配即推送

**格式：**
```bash
# 无关键词筛选（默认）
KEYWORDS=''

# 单个关键词
KEYWORDS='["VPS"]'

# 多个关键词
KEYWORDS='["VPS","优惠","测评","限时"]'
```

### WAIT_TIME

两次检查之间的等待时间（秒）。

**建议值：**
- 测试环境：`5-10` 秒
- 生产环境：`30-60` 秒
- 低频监控：`300-600` 秒

**格式：**
```bash
WAIT_TIME=10
```

### CLEANUP_DAYS

历史记录保留天数，超过此时间的记录将被自动清理。

**建议值：**
- 高频使用：`3-7` 天
- 中频使用：`7-14` 天
- 低频使用：`14-30` 天

**格式：**
```bash
CLEANUP_DAYS=7
```

## 🎯 配置示例

### 商家监控配置

适用于关注优惠活动和商家推广的用户。

```bash
TG_BOT_TOKEN="your_bot_token_here"
TG_CHAT_ID='["your_chat_id_here"]'
CATEGORIES='["promotion"]'
KEYWORDS='["优惠","折扣","促销","限时","特价","黑五"]'
WAIT_TIME=30
CLEANUP_DAYS=7
```

### 技术学习配置

适用于关注技术分享和开发相关内容的用户。

```bash
TG_BOT_TOKEN="your_bot_token_here"
TG_CHAT_ID='["your_chat_id_here"]'
CATEGORIES='["tech","dev"]'
KEYWORDS='["Docker","Kubernetes","Python","云原生","开源"]'
WAIT_TIME=60
CLEANUP_DAYS=14
```

### 全面监控配置

适用于想要全面了解社区动态的用户。

```bash
TG_BOT_TOKEN="your_bot_token_here"
TG_CHAT_ID='["your_chat_id_here"]'
CATEGORIES='["daily","tech","info","review"]'
KEYWORDS=''
WAIT_TIME=30
CLEANUP_DAYS=10
```

### 多群推送配置

适用于需要将不同内容推送到不同群组的用户。

```bash
TG_BOT_TOKEN="your_bot_token_here"
# 推送到多个群组：技术群、优惠群、个人频道
TG_CHAT_ID='["-1001234567890","-1001234567891","@personal_channel"]'
CATEGORIES='["tech","promotion","review"]'
KEYWORDS='["VPS","服务器","优惠","测评"]'
WAIT_TIME=30
CLEANUP_DAYS=7
```

## 🔄 动态配置

### 使用环境变量文件

创建 `.env` 文件：

```bash
# .env
TG_BOT_TOKEN=your_bot_token_here
TG_CHAT_ID=["your_chat_id_here"]
CATEGORIES=["daily","review"]
KEYWORDS=["VPS","测评"]
WAIT_TIME=10
CLEANUP_DAYS=7
```

### 配置验证

部署前验证配置：

```bash
# 检查环境变量
echo $TG_BOT_TOKEN
echo $TG_CHAT_ID

# 测试 Bot Token
curl -s "https://api.telegram.org/bot$TG_BOT_TOKEN/getMe"

# 测试发送消息
curl -s -X POST "https://api.telegram.org/bot$TG_BOT_TOKEN/sendMessage" \
  -d chat_id="$TG_CHAT_ID" \
  -d text="测试消息"
```

## 🚨 安全建议

1. **保护 Token**：
   - 不要在公共代码库中硬编码 Token
   - 使用环境变量或配置文件
   - 定期更换 Token

2. **Chat ID 管理**：
   - 定期检查群组权限
   - 移除不再需要的聊天 ID
   - 使用私有群组接收敏感信息

3. **配置备份**：
   - 备份重要的配置文件
   - 记录配置变更历史
   - 测试配置恢复流程

## 🔧 高级配置技巧

### 条件筛选

```bash
# 只关注包含特定关键词的测评内容
CATEGORIES='["review"]'
KEYWORDS='["VPS","云服务器","性能测试"]'

# 关注技术讨论，但排除新手问题
CATEGORIES='["tech"]'
KEYWORDS='["Docker","Kubernetes","高级","架构"]'
```

### 时间优化

```bash
# 白天频繁检查，夜间减少频率
# 可以通过脚本动态调整 WAIT_TIME
```

### 多实例部署

```bash
# 不同配置的多个实例
# 实例1：商家监控
# 实例2：技术学习
# 实例3：全面监控
```

---

?> 💡 **提示**：配置修改后需要重启容器才能生效。建议在测试环境中验证配置后再应用到生产环境。 