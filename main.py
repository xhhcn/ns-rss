#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 feedparser 获取 NodeSeek RSS 内容的脚本
筛选指定类别且标题包含特定关键词的项目并推送到Telegram
支持环境变量配置
"""

import requests
import time
import random
import feedparser
from email.utils import parsedate_to_datetime
from datetime import datetime
import asyncio
from telegram import Bot
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量获取配置
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')
CATEGORIES = os.getenv('CATEGORIES', '').strip()
KEYWORDS = os.getenv('KEYWORDS', '').strip()
WAIT_TIME = int(os.getenv('WAIT_TIME', '5'))
CLEANUP_DAYS = int(os.getenv('CLEANUP_DAYS', '7'))

# 验证必填环境变量
if not TG_BOT_TOKEN:
    raise ValueError("TG_BOT_TOKEN 环境变量不能为空")
if not TG_CHAT_ID:
    raise ValueError("TG_CHAT_ID 环境变量不能为空")

# 解析环境变量列表的函数
def parse_list_env(env_value):
    """解析环境变量列表，支持JSON数组格式和逗号分隔格式"""
    if not env_value:
        return []
    
    # 尝试解析为JSON数组
    try:
        parsed = json.loads(env_value)
        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed if str(item).strip()]
    except (json.JSONDecodeError, TypeError):
        pass
    
    # 如果不是有效的JSON，则按逗号分隔解析
    return [item.strip() for item in env_value.split(',') if item.strip()]

# 解析多个 CHAT_ID（支持JSON数组格式和逗号分隔）
CHAT_IDS = parse_list_env(TG_CHAT_ID)

# 解析多个 CATEGORIES（支持JSON数组格式和逗号分隔）
CATEGORY_LIST = parse_list_env(CATEGORIES)
KEYWORD_LIST = parse_list_env(KEYWORDS)

# 支持的类别及其对应的消息标题
CATEGORY_TITLES = {
    'daily': '🔔 <b>NodeSeek日常帖子</b>',
    'tech': '🔔 <b>NodeSeek技术帖子</b>',
    'info': '🔔 <b>NodeSeek情报帖子</b>',
    'review': '🔔 <b>NodeSeek测评帖子</b>',
    'trade': '🔔 <b>NodeSeek交易帖子</b>',
    'carpool': '🔔 <b>NodeSeek拼车帖子</b>',
    'dev': '🔔 <b>NodeSeek dev帖子</b>',
    'photo-share': '🔔 <b>NodeSeek贴图帖子</b>',
    'expose': '🔔 <b>NodeSeek曝光帖子</b>',
    'promotion': '🔔 <b>NodeSeek商家信息</b>'
}

# 存储上次发送的内容，避免重复发送
# 在 Docker 环境中使用 /app/data 目录，本地环境使用当前目录
LAST_SENT_FILE = "/app/data/last_sent.json" if os.path.exists("/app/data") else "last_sent.json"

def load_last_sent():
    """加载上次发送的内容"""
    try:
        if os.path.exists(LAST_SENT_FILE):
            with open(LAST_SENT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_last_sent(data):
    """保存本次发送的内容，并清理过期记录"""
    try:
        # 清理过期记录（保留最近N天的记录）
        cleaned_data = cleanup_old_records(data, CLEANUP_DAYS)
        
        with open(LAST_SENT_FILE, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
        
        # 打印清理统计
        removed_count = len(data) - len(cleaned_data)
        if removed_count > 0:
            print(f"  🧹 清理了 {removed_count} 条过期记录，当前保留 {len(cleaned_data)} 条记录")
            
    except Exception as e:
        print(f"保存历史记录失败: {e}")

def cleanup_old_records(data, days_to_keep=7):
    """清理过期记录，只保留指定天数内的记录"""
    from datetime import timedelta
    
    if not data:
        return data
    
    # 计算过期时间（7天前）
    cutoff_time = datetime.now() - timedelta(days=days_to_keep)
    
    cleaned_data = {}
    
    for item_id, item_info in data.items():
        try:
            # 获取发送时间
            sent_time_str = item_info.get('sent_time')
            if not sent_time_str:
                # 如果没有sent_time，保留这条记录（向后兼容）
                cleaned_data[item_id] = item_info
                continue
            
            # 解析发送时间
            sent_time = datetime.fromisoformat(sent_time_str)
            
            # 如果记录在保留期内，则保留
            if sent_time >= cutoff_time:
                cleaned_data[item_id] = item_info
                
        except (ValueError, TypeError) as e:
            # 如果时间解析失败，保留这条记录（向后兼容）
            print(f"  ⚠️ 解析记录时间失败，保留记录: {item_id}")
            cleaned_data[item_id] = item_info
    
    return cleaned_data

async def send_to_telegram(message, chat_id):
    """发送消息到指定的Telegram聊天"""
    try:
        bot = Bot(token=TG_BOT_TOKEN)
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='HTML',
            disable_web_page_preview=False
        )
        print(f"  ✓ 消息已发送到Telegram (Chat ID: {chat_id})")
        return True
    except Exception as e:
        print(f"  ✗ 发送Telegram消息失败 (Chat ID: {chat_id}): {e}")
        return False

async def send_to_all_chats(message):
    """发送消息到所有配置的聊天"""
    success_count = 0
    for chat_id in CHAT_IDS:
        if await send_to_telegram(message, chat_id):
            success_count += 1
        # 添加发送间隔，避免频率限制
        if len(CHAT_IDS) > 1:
            await asyncio.sleep(0.5)
    
    print(f"  ✓ 消息发送完成: {success_count}/{len(CHAT_IDS)} 个聊天")
    return success_count > 0

def escape_html(text):
    """转义HTML特殊字符"""
    # HTML需要转义的特殊字符
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def format_time(time_str):
    """格式化时间为简洁格式，转换为GMT+8"""
    try:
        from datetime import timezone, timedelta
        
        # 跳过无效时间
        if time_str in ["N/A", "", None]:
            return "N/A"
        
        dt = None
        
        # 首先尝试解析RFC 2822格式 (如: "Fri, 11 Jul 2025 10:33:33 GMT")
        try:
            dt = parsedate_to_datetime(time_str)
            # parsedate_to_datetime已经处理了时区信息
        except Exception:
            # 如果RFC 2822格式解析失败，尝试ISO格式
            try:
                if 'T' in time_str:  # ISO格式
                    if time_str.endswith('Z'):
                        # UTC时间
                        dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                    elif '+' in time_str or '-' in time_str[-6:]:
                        # 带时区的时间
                        dt = datetime.fromisoformat(time_str)
                    else:
                        # 没有时区信息，假设为UTC
                        dt = datetime.fromisoformat(time_str)
                        dt = dt.replace(tzinfo=timezone.utc)
            except Exception:
                # 都解析失败，返回原字符串
                return time_str
        
        # 如果成功解析时间，转换为GMT+8
        if dt:
            gmt8 = timezone(timedelta(hours=8))
            dt_gmt8 = dt.astimezone(gmt8)
            
            # 格式化为 年-月-日 时:分
            return dt_gmt8.strftime("%Y-%m-%d %H:%M")
        
        # 如果解析失败，返回原字符串
        return time_str
        
    except Exception as e:
        # 如果解析失败，返回原字符串
        print(f"  ⚠️ 时间解析失败: {time_str} - {e}")
        return time_str

def format_message(item):
    """格式化消息内容 - 根据category使用不同的标题"""
    # 获取category对应的标题
    category = item.get('category', '').lower()
    title = CATEGORY_TITLES.get(category, '🔔 <b>NodeSeek帖子</b>')
    
    # 格式化时间
    formatted_time = format_time(item['pub_date'])
    
    # 转义HTML特殊字符
    escaped_title = escape_html(item['title'])
    escaped_time = escape_html(formatted_time)
    escaped_link = escape_html(item['link'])
    
    creator = item.get('creator', 'N/A')
    escaped_creator = escape_html(creator)
    
    message = f"""{title}

<b>【账号】 </b>{escaped_creator}
<b>【主题】 <a href="{escaped_link}">{escaped_title}</a></b>"""
    
    return message

def get_nodeseek_rss(url):
    """
    使用 feedparser 获取 NodeSeek RSS 内容
    每次调用都会创建新的 requests 会话
    """
    session = None
    try:
        # 每次都创建新的 session
        session = requests.Session()
        
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        session.headers.update(headers)
        
        # 添加随机延迟
        time.sleep(random.uniform(1, 3))
        
        print(f"  正在使用 feedparser 获取 NodeSeek RSS 内容: {url}")
        
        # 发送请求
        response = session.get(url, timeout=10)
        
        # 检查响应状态码
        if response.status_code == 200:
            print(f"  ✓ 成功获取内容 (状态码: {response.status_code})")
            
            # 使用 feedparser 解析 RSS
            feed = feedparser.parse(response.text)
            
            if not feed.entries:
                print("  ✗ Feed 里暂时没有条目")
                return None
            
            # 转换为统一格式
            items = []
            for entry in feed.entries:
                # 获取发布时间
                published = "N/A"
                if hasattr(entry, "published"):
                    published = entry.published
                elif hasattr(entry, "updated"):
                    published = entry.updated
                
                # 保持原始时间格式，让format_time函数处理转换
                
                # 获取描述
                description = "N/A"
                if hasattr(entry, "summary"):
                    description = entry.summary
                elif hasattr(entry, "description"):
                    description = entry.description
                
                # 获取作者信息 (NodeSeek 使用 dc:creator)
                creator = "N/A"
                if hasattr(entry, "authors") and entry.authors:
                    creator = entry.authors[0].get('name', 'N/A')
                elif hasattr(entry, "author"):
                    creator = entry.author
                elif hasattr(entry, "dc_creator"):
                    creator = entry.dc_creator
                # 尝试从tags中获取dc:creator
                if creator == "N/A" and hasattr(entry, "tags"):
                    for tag in entry.tags:
                        if tag.get('term') and 'creator' in tag.get('label', '').lower():
                            creator = tag.get('term')
                            break
                
                # 获取分类信息
                category = "N/A"
                if hasattr(entry, "category"):
                    category = entry.category
                elif hasattr(entry, "tags") and entry.tags:
                    # 查找category标签
                    for tag in entry.tags:
                        if tag.get('term'):
                            category = tag.get('term')
                            break
                
                rss_item = {
                    'title': entry.title if hasattr(entry, 'title') else 'N/A',
                    'link': entry.link if hasattr(entry, 'link') else 'N/A',
                    'description': description,
                    'pub_date': published,
                    'creator': creator,
                    'category': category
                }
                items.append(rss_item)
            
            return items
            
        else:
            print(f"  ✗ 请求失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ✗ feedparser 请求异常: {e}")
        return None
    finally:
        # 确保 session 被关闭
        if session:
            try:
                session.close()
                print(f"  ✓ requests 会话已关闭")
            except:
                pass

def print_rss_item(item):
    """
    打印 RSS 项目信息 - 简约风格
    """
    # 格式化时间
    formatted_time = format_time(item['pub_date'])
    
    print(f"\n{'-'*60}")
    print(f"【NodeSeek】最新项目")
    print(f"{'-'*60}")
    print(f"标题: {item['title']}")
    print(f"分类: {item.get('category', 'N/A')}")
    print(f"作者: {item.get('creator', 'N/A')}")
    print(f"时间: {formatted_time}")
    print(f"链接: {item['link']}")
    print(f"{'-'*60}")

async def process_rss_feed(rss_url, last_sent):
    """
    处理NodeSeek RSS源
    """
    print(f"\n{'='*80}")
    print(f"正在处理 NodeSeek")
    print(f"目标 URL: {rss_url}")
    print("-" * 80)
    
    # 获取RSS内容
    items = get_nodeseek_rss(rss_url)
    
    if items is None:
        print(f"✗ 无法获取 NodeSeek RSS 内容")
        return False, None
        
    if not items:
        print(f"✗ NodeSeek 没有找到 RSS 项目")
        return False, None
    
    print(f"✓ 成功解析 NodeSeek RSS，共找到 {len(items)} 个项目")
    
    # 第一步：筛选指定类别的项目
    category_filtered = []
    if CATEGORY_LIST:
        for item in items:
            if item.get('category', '').lower() in [cat.lower() for cat in CATEGORY_LIST]:
                category_filtered.append(item)
        print(f"  ✓ 筛选指定类别 {CATEGORY_LIST}，从 {len(items)} 个项目中筛选出 {len(category_filtered)} 个")
    else:
        category_filtered = items
        print(f"  ✓ 未指定类别筛选，处理所有 {len(items)} 个项目")
    
    if not category_filtered:
        print(f"  ℹ️ 没有找到指定类别的项目")
        return True, None
    
    # 第二步：如果有关键词，筛选标题包含指定关键词的项目
    if KEYWORD_LIST:
        filtered_items = []
        for item in category_filtered:
            title = item.get('title', '').lower()  # 转为小写进行匹配
            
            # 检查标题是否包含任意一个关键词
            found_keyword = None
            for keyword in KEYWORD_LIST:
                if keyword.lower() in title:  # 关键词也转小写匹配
                    found_keyword = keyword
                    break
            
            if found_keyword:
                item['matched_keyword'] = found_keyword  # 记录匹配的关键词
                filtered_items.append(item)
        
        if not filtered_items:
            print(f"  ℹ️ 没有找到包含指定关键词的项目")
            print(f"  📝 关键词列表: {', '.join(KEYWORD_LIST)}")
            return True, None
        
        print(f"  ✓ 关键词筛选，从 {len(category_filtered)} 个项目中筛选出 {len(filtered_items)} 个")
        print(f"  📝 关键词列表: {', '.join(KEYWORD_LIST)}")
    else:
        filtered_items = category_filtered
        print(f"  ✓ 未指定关键词筛选，处理所有 {len(category_filtered)} 个项目")
    
    # 处理所有符合条件的项目
    latest_items = filtered_items
    print(f"  ✓ 准备处理所有 {len(latest_items)} 个符合条件的项目")
    
    new_items = []
    all_updates = {}
    
    # 检查每个项目是否为新内容
    for item in latest_items:
        # 使用作者+发布时间作为唯一标识符
        creator = item.get('creator', 'N/A')
        pub_date = item.get('pub_date', 'N/A')
        item_id = f"NodeSeek_{creator}_{pub_date}"
        
        # 检查是否已存在相同的作者+时间组合
        if item_id not in last_sent:
            # 这是新内容
            new_items.append(item)
            all_updates[item_id] = {
                'creator': creator,
                'pub_date': pub_date,
                'title': item.get('title', ''),
                'category': item.get('category', ''),
                'sent_time': datetime.now().isoformat()
            }
            matched_keyword = item.get('matched_keyword', '无关键词匹配')
            print(f"  🆕 发现新内容 [类别: {item.get('category', 'N/A')}] [关键词: {matched_keyword}]: {item.get('title', '')[:50]}...")
        else:
            print(f"  ℹ️ 已存在内容: {item.get('title', '')[:50]}...")
    
    if not new_items:
        print(f"  ℹ️ 没有发现新内容，跳过发送")
        return True, None
    
    print(f"  ✓ 发现 {len(new_items)} 个新内容，准备发送到Telegram")
    
    # 发送所有新内容到Telegram
    success_count = 0
    for i, item in enumerate(new_items, 1):
        print(f"  📤 正在发送第 {i}/{len(new_items)} 个新内容...")
        
        # 打印项目信息
        print_rss_item(item)
        
        # 格式化消息
        message = format_message(item)
        
        # 发送到所有聊天
        if await send_to_all_chats(message):
            success_count += 1
            # 添加发送间隔，避免频率限制
            if i < len(new_items):  # 不是最后一个
                await asyncio.sleep(1)  # 等待1秒
        else:
            print(f"  ✗ 第 {i} 个内容发送失败")
    
    print(f"  ✅ 成功发送 {success_count}/{len(new_items)} 个新内容")
    
    if success_count > 0:
        return True, all_updates
    else:
        return False, None

async def fetch_rss_once():
    """
    执行一次RSS获取操作
    """
    rss_url = 'https://rss.nodeseek.com/'
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*80}")
    print(f"开始新一轮RSS获取 - {current_time}")
    print(f"将获取 NodeSeek RSS 最新项目")
    print("配置信息：")
    print(f"  - 类别筛选: {CATEGORY_LIST if CATEGORY_LIST else '全部'}")
    print(f"  - 关键词筛选: {KEYWORD_LIST if KEYWORD_LIST else '无'}")
    print(f"  - 发送目标: {len(CHAT_IDS)} 个聊天")
    print(f"  - 等待时间: {WAIT_TIME} 秒")
    print("=" * 80)
    
    # 加载上次发送的记录
    last_sent = load_last_sent()
    
    # 处理RSS源
    success, updates = await process_rss_feed(rss_url, last_sent)
    
    # 保存更新的记录
    if updates:
        last_sent.update(updates)
        save_last_sent(last_sent)
        print(f"  💾 已保存 {len(updates)} 条新记录")
    
    print(f"\n{'='*80}")
    print(f"本轮处理完成！{'成功' if success else '失败'} - {current_time}")
    print("=" * 80)
    
    return success

async def main():
    """
    主函数 - 循环获取RSS源并发送到Telegram
    """
    print("NodeSeek RSS 循环获取工具 + Telegram推送")
    print(f"每{WAIT_TIME}秒自动获取最新RSS项目")
    print("配置信息：")
    print(f"  - 类别筛选: {CATEGORY_LIST if CATEGORY_LIST else '全部'}")
    print(f"  - 关键词筛选: {KEYWORD_LIST if KEYWORD_LIST else '无'}")
    print(f"  - 发送目标: {len(CHAT_IDS)} 个聊天")
    print("符合条件的新内容将自动推送到Telegram")
    print("按 Ctrl+C 退出程序")
    print("=" * 80)
    
    # 清空历史记录，确保重新启动时发送当前最新内容
    if os.path.exists(LAST_SENT_FILE):
        os.remove(LAST_SENT_FILE)
        print("🗑️ 已清空历史记录，重新开始监控")
        print("=" * 80)
    
    try:
        while True:
            # 执行一次RSS获取
            await fetch_rss_once()
            
            # 等待指定时间，显示倒计时
            print(f"\n等待{WAIT_TIME}秒后进行下一轮获取...")
            for i in range(WAIT_TIME, 0, -1):
                print(f"倒计时: {i}秒", end="\r")
                await asyncio.sleep(1)
            print(" " * 20, end="\r")  # 清除倒计时显示
            
    except KeyboardInterrupt:
        print(f"\n\n{'='*80}")
        print("用户中断程序，正在退出...")
        print("感谢使用RSS获取工具！")
        print("=" * 80)
    except Exception as e:
        print(f"\n程序发生异常: {e}")
        print("程序将退出")

def run_main():
    """运行主程序"""
    asyncio.run(main())

if __name__ == "__main__":
    run_main()