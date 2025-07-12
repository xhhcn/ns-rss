# Docker Run 使用示例

## 基本用法

### 单个聊天ID
```bash
docker run -d --name nodeseek-rss-monitor \
  -e TG_BOT_TOKEN='你的机器人token' \
  -e TG_CHAT_ID='聊天ID' \
  -e 'CATEGORIES=["daily","review"]' \
  -e 'KEYWORDS=["关键词1","关键词2"]' \
  -e WAIT_TIME=5 \
  -v "$(pwd)/data:/app/data" \
  nodeseek-rss
```

### 多个聊天ID（JSON数组格式）
```bash
docker run -d --name nodeseek-rss-monitor \
  -e TG_BOT_TOKEN='7729781072:AAFwddTv27lCDblU06wVmOryEh05vY5-BRA' \
  -e 'TG_CHAT_ID=["35873777","396733329"]' \
  -e 'CATEGORIES=["daily","review"]' \
  -e 'KEYWORDS=["只测不评","没有"]' \
  -e WAIT_TIME=5 \
  -v "$(pwd)/data:/app/data" \
  nodeseek-rss
```

### 兼容旧格式（逗号分隔）
```bash
docker run -d --name nodeseek-rss-monitor \
  -e TG_BOT_TOKEN='7729781072:AAFwddTv27lCDblU06wVmOryEh05vY5-BRA' \
  -e TG_CHAT_ID='35873777,396733329' \
  -e CATEGORIES='daily,review' \
  -e KEYWORDS='只测不评,没有' \
  -e WAIT_TIME=5 \
  -v "$(pwd)/data:/app/data" \
  nodeseek-rss
```

## 查看日志
```bash
docker logs -f nodeseek-rss-monitor
```

## 停止容器
```bash
docker stop nodeseek-rss-monitor
docker rm nodeseek-rss-monitor
```

## 注意事项

1. **JSON数组格式**：在Shell中使用JSON数组时，需要用单引号包围整个环境变量值
2. **路径映射**：使用 `-v "$(pwd)/data:/app/data"` 来持久化历史记录
3. **容器名称**：使用 `--name` 指定容器名称，方便后续管理
4. **后台运行**：使用 `-d` 参数让容器在后台运行 