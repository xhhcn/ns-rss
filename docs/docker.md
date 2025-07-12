# 🐳 Docker 部署

> 📦 **支持多平台架构，一键部署**

## 🏷️ 支持的架构

| 架构 | 说明 | 适用设备 |
|------|------|----------|
| `linux/amd64` | x86_64 架构 | 大多数服务器、PC |
| `linux/arm64` | ARM64 架构 | 树莓派、ARM 服务器 |

## 🚀 部署方式

### 方式一：Docker Run

#### 基础部署

```bash
# 创建数据目录
mkdir -p ./data

# 启动容器
docker run -d \
  --name ns-rss-monitor \
  -e TG_BOT_TOKEN="your_bot_token_here" \
  -e TG_CHAT_ID='["your_chat_id_here"]' \
  -v ./data:/app/data \
  --restart unless-stopped \
  xhh1128/ns-rss:latest
```

#### 完整配置

```bash
docker run -d \
  --name ns-rss-monitor \
  -e TG_BOT_TOKEN="your_bot_token_here" \
  -e TG_CHAT_ID='["your_chat_id_here"]' \
  -e CATEGORIES='["daily","review","tech"]' \
  -e KEYWORDS='["VPS","优惠","测评"]' \
  -e WAIT_TIME=10 \
  -e CLEANUP_DAYS=7 \
  -v ./data:/app/data \
  --restart unless-stopped \
  xhh1128/ns-rss:latest
```

### 方式二：Docker Compose

#### 创建配置文件

```yaml
# docker-compose.yml
version: '3.8'

services:
  ns-rss:
    image: xhh1128/ns-rss:latest
    container_name: ns-rss-monitor
    environment:
      # 必填配置
      - TG_BOT_TOKEN=your_bot_token_here
      - TG_CHAT_ID=["your_chat_id_here"]
      
      # 可选配置
      - CATEGORIES=["daily","review","tech"]
      - KEYWORDS=["VPS","优惠","测评"]
      - WAIT_TIME=10
      - CLEANUP_DAYS=7
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    
    # 可选：资源限制
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          cpus: '0.1'
          memory: 64M
```

#### 启动服务

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f ns-rss

# 重启服务
docker-compose restart ns-rss

# 停止服务
docker-compose stop ns-rss

# 更新镜像
docker-compose pull && docker-compose up -d
```

## 📊 容器管理

### 查看状态

```bash
# 查看运行的容器
docker ps | grep ns-rss

# 查看所有容器（包括停止的）
docker ps -a | grep ns-rss

# 查看容器详情
docker inspect ns-rss-monitor
```

### 日志管理

```bash
# 查看实时日志
docker logs -f ns-rss-monitor

# 查看最近100行日志
docker logs --tail 100 ns-rss-monitor

# 查看指定时间的日志
docker logs --since="2025-01-13T14:00:00" ns-rss-monitor

# 导出日志到文件
docker logs ns-rss-monitor > ns-rss.log
```

### 容器操作

```bash
# 重启容器
docker restart ns-rss-monitor

# 停止容器
docker stop ns-rss-monitor

# 删除容器
docker rm ns-rss-monitor

# 强制删除运行中的容器
docker rm -f ns-rss-monitor
```

## 🔧 高级配置

### 环境变量文件

创建 `.env` 文件：

```bash
# .env
TG_BOT_TOKEN=your_bot_token_here
TG_CHAT_ID=["your_chat_id_here"]
CATEGORIES=["daily","review","tech"]
KEYWORDS=["VPS","优惠","测评"]
WAIT_TIME=10
CLEANUP_DAYS=7
```

然后在 docker-compose.yml 中使用：

```yaml
version: '3.8'

services:
  ns-rss:
    image: xhh1128/ns-rss:latest
    container_name: ns-rss-monitor
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

### 网络配置

```yaml
version: '3.8'

networks:
  ns-rss-network:
    driver: bridge

services:
  ns-rss:
    image: xhh1128/ns-rss:latest
    container_name: ns-rss-monitor
    environment:
      - TG_BOT_TOKEN=your_bot_token_here
      - TG_CHAT_ID=["your_chat_id_here"]
    volumes:
      - ./data:/app/data
    networks:
      - ns-rss-network
    restart: unless-stopped
```

### 资源限制

```yaml
services:
  ns-rss:
    image: xhh1128/ns-rss:latest
    container_name: ns-rss-monitor
    environment:
      - TG_BOT_TOKEN=your_bot_token_here
      - TG_CHAT_ID=["your_chat_id_here"]
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    
    # 资源限制
    deploy:
      resources:
        limits:
          cpus: '0.5'      # 最大 0.5 CPU
          memory: 256M     # 最大 256MB 内存
        reservations:
          cpus: '0.1'      # 保留 0.1 CPU
          memory: 64M      # 保留 64MB 内存
    
    # 健康检查
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('https://rss.nodeseek.com/', timeout=5)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

## 🗂️ 数据管理

### 数据持久化

```bash
# 创建专用数据卷
docker volume create ns-rss-data

# 使用数据卷
docker run -d \
  --name ns-rss-monitor \
  -e TG_BOT_TOKEN="your_bot_token_here" \
  -e TG_CHAT_ID='["your_chat_id_here"]' \
  -v ns-rss-data:/app/data \
  --restart unless-stopped \
  xhh1128/ns-rss:latest
```

### 数据备份

```bash
# 备份数据
docker run --rm \
  -v ns-rss-data:/source \
  -v $(pwd):/backup \
  alpine tar czf /backup/ns-rss-backup.tar.gz -C /source .

# 恢复数据
docker run --rm \
  -v ns-rss-data:/target \
  -v $(pwd):/backup \
  alpine tar xzf /backup/ns-rss-backup.tar.gz -C /target
```

### 数据清理

```bash
# 查看数据使用情况
docker system df

# 清理无用的镜像
docker image prune -a

# 清理无用的容器
docker container prune

# 清理无用的数据卷
docker volume prune
```

## 🔍 故障排除

### 常见问题

#### 1. 容器无法启动

```bash
# 检查容器状态
docker ps -a | grep ns-rss

# 查看错误日志
docker logs ns-rss-monitor

# 检查配置
docker inspect ns-rss-monitor
```

#### 2. 消息发送失败

```bash
# 检查网络连接
docker exec ns-rss-monitor ping -c 3 api.telegram.org

# 检查环境变量
docker exec ns-rss-monitor env | grep TG_
```

#### 3. RSS 获取失败

```bash
# 检查 RSS 源连接
docker exec ns-rss-monitor curl -I https://rss.nodeseek.com/

# 检查 DNS 解析
docker exec ns-rss-monitor nslookup rss.nodeseek.com
```

### 调试模式

```bash
# 以交互模式运行
docker run -it --rm \
  -e TG_BOT_TOKEN="your_bot_token_here" \
  -e TG_CHAT_ID='["your_chat_id_here"]' \
  xhh1128/ns-rss:latest

# 进入运行中的容器
docker exec -it ns-rss-monitor /bin/bash

# 查看Python进程
docker exec ns-rss-monitor ps aux | grep python
```

## 📈 性能优化

### 监控指标

```bash
# 查看资源使用情况
docker stats ns-rss-monitor

# 查看容器进程
docker exec ns-rss-monitor ps aux

# 查看内存使用
docker exec ns-rss-monitor free -h

# 查看磁盘使用
docker exec ns-rss-monitor df -h
```

### 优化建议

1. **合理设置检查间隔**：
   ```bash
   WAIT_TIME=30  # 30秒检查一次，减少资源消耗
   ```

2. **控制历史记录**：
   ```bash
   CLEANUP_DAYS=3  # 只保留3天记录，减少存储占用
   ```

3. **资源限制**：
   ```yaml
   deploy:
     resources:
       limits:
         memory: 128M  # 限制内存使用
   ```

## 🔄 更新升级

### 升级到最新版本

```bash
# 停止当前容器
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

### 使用 Docker Compose 升级

```bash
# 拉取最新镜像
docker-compose pull

# 重新创建容器
docker-compose up -d

# 清理旧镜像
docker image prune -a
```

## 🎯 最佳实践

1. **使用 Docker Compose**：便于管理和维护
2. **设置资源限制**：防止容器消耗过多资源
3. **定期备份数据**：防止数据丢失
4. **监控日志**：及时发现问题
5. **定期更新镜像**：获得最新功能和安全修复

---

?> 💡 **提示**：如果您在使用过程中遇到问题，请查看 [故障排除](troubleshooting.md) 或提交 [Issues](https://github.com/xhhcn/ns-rss/issues)。 