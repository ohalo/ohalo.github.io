#!/usr/bin/env python3
"""
批量修复博客HTML文件：将独立HTML骨架转换为Jekyll模板格式
"""
import os
import re
from pathlib import Path

BLOG_REPO = Path("/Users/halo/.qclaw/workspace/blog-repo")

def extract_title_from_html(content):
    """从HTML中提取标题"""
    # 尝试从<title>标签提取
    match = re.search(r'<title>([^<]+)</title>', content)
    if match:
        title = match.group(1)
        # 去掉常见的后缀
        title = re.sub(r'\s*[-|·]\s*halo的技术博客\s*$', '', title)
        title = re.sub(r'\s*[-|·]\s*Halo Blog\s*$', '', title)
        return title.strip()
    
    # 尝试从<h1>标签提取
    match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    if match:
        return match.group(1).strip()
    
    return "未命名文章"

def extract_date_from_path(filepath):
    """从文件路径提取日期"""
    match = re.search(r'/(\d{4}-\d{2}-\d{2})-', str(filepath))
    if match:
        return match.group(1)
    return "2026-04-07"

def extract_category_from_path(filepath):
    """从文件路径提取分类"""
    rel_path = filepath.relative_to(BLOG_REPO / "posts")
    parts = list(rel_path.parts[:-1])  # 去掉文件名
    if parts:
        return "/".join(parts)
    return "uncategorized"

def generate_category_name(category):
    """生成中文分类名"""
    category_map = {
        "hardware/nas": "数码硬件/NAS存储",
        "hardware/others": "数码硬件/其他硬件",
        "hardware/gpu-5070-9070-comparison": "数码硬件/显卡对比",
        "ai-observation/career": "AI观察/职业思考",
        "ai-observation/society": "AI观察/社会现象",
        "ai-tools/openclaw": "AI工具/OpenClaw",
        "ai-tools/hafw": "AI工具/HAFW",
        "reading/book-review": "阅读/书评",
        "reading/reading-notes": "阅读/读书笔记",
        "career": "职业成长",
    }
    return category_map.get(category, category)

def extract_tags_from_content(content):
    """从内容提取标签"""
    tags = []
    # 从meta keywords提取
    match = re.search(r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']+)["\']', content)
    if match:
        tags = [t.strip() for t in match.group(1).split(',') if t.strip()]
    
    # 如果没有keywords，从h2标题提取关键词
    if not tags:
        h2_titles = re.findall(r'<h2[^>]*>([^<]+)</h2>', content)
        keywords = []
        for title in h2_titles[:3]:
            # 提取核心词
            if 'NAS' in title:
                keywords.append('NAS')
            if 'RAID' in title:
                keywords.append('RAID')
            if '安全' in title or '备份' in title:
                keywords.append('数据安全')
        tags = list(set(keywords))[:5]
    
    return tags if tags else ["随笔"]

def extract_body_content(content):
    """提取正文内容（去除HTML骨架）"""
    # 移除frontmatter（如果有）
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # 尝试多种模式提取正文
    
    # 模式1: <article>标签内的内容
    match = re.search(r'<article[^>]*>(.*?)</article>', content, flags=re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # 模式2: <section id="main_content">内的内容
    match = re.search(r'<section[^>]*id=["\']main_content["\'][^>]*>(.*?)</section>', content, flags=re.DOTALL)
    if match:
        body = match.group(1)
        # 移除<article>包装
        body = re.sub(r'</?article[^>]*>', '', body)
        return body.strip()
    
    # 模式3: <div class="container">后的主要内容
    match = re.search(r'<div[^>]*class=["\']container["\'][^>]*>(.*?)</div>\s*</body>', content, flags=re.DOTALL)
    if match:
        body = match.group(1)
        # 移除section包装
        body = re.sub(r'</?section[^>]*>', '', body)
        return body.strip()
    
    # 模式4: body内的所有内容，移除header/nav
    match = re.search(r'<body[^>]*>(.*?)</body>', content, flags=re.DOTALL)
    if match:
        body = match.group(1)
        # 移除header
        body = re.sub(r'<header[^>]*>.*?</header>', '', body, flags=re.DOTALL)
        # 移除nav
        body = re.sub(r'<nav[^>]*>.*?</nav>', '', body, flags=re.DOTALL)
        # 移除div.nav
        body = re.sub(r'<div[^>]*class=["\']nav["\'][^>]*>.*?</div>', '', body, flags=re.DOTALL)
        # 移除div.container包装
        body = re.sub(r'<div[^>]*class=["\']container["\'][^>]*>', '', body)
        body = re.sub(r'</div>\s*$', '', body.strip())
        return body.strip()
    
    return content

def extract_existing_frontmatter(content):
    """提取现有的frontmatter"""
    match = re.match(r'^---\n(.*?)\n---\n', content, flags=re.DOTALL)
    if match:
        fm_text = match.group(1)
        fm = {}
        for line in fm_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                fm[key.strip()] = value.strip().strip('"').strip("'")
        return fm
    return None

def create_jekyll_content(filepath, content):
    """创建Jekyll格式的文章内容"""
    # 提取现有frontmatter
    existing_fm = extract_existing_frontmatter(content)
    
    # 提取正文
    body = extract_body_content(content)
    
    # 确定文章元数据
    if existing_fm:
        title = existing_fm.get('title', extract_title_from_html(content))
        date = existing_fm.get('date', extract_date_from_path(filepath))
        category = existing_fm.get('category', extract_category_from_path(filepath))
        tags = existing_fm.get('tags', [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.strip('[]').split(',')]
    else:
        title = extract_title_from_html(content)
        date = extract_date_from_path(filepath)
        category = extract_category_from_path(filepath)
        tags = extract_tags_from_content(content)
    
    category_name = generate_category_name(category)
    
    # 计算permalink
    rel_path = filepath.relative_to(BLOG_REPO / "posts")
    permalink = f"/posts/{rel_path}"
    
    # 格式化tags
    if tags:
        tags_str = ", ".join([f'"{t}"' if ' ' in t or '/' in t else t for t in tags])
        tags_str = f"[{tags_str}]"
    else:
        tags_str = "[]"
    
    # 构建新的frontmatter
    frontmatter = f'''---
permalink: {permalink}
layout: post
title: "{title}"
date: {date}
category: {category}
category_name: "{category_name}"
tags: {tags_str}
---

'''
    
    return frontmatter + body

def process_file(filepath):
    """处理单个文件"""
    print(f"处理: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否需要处理（包含<!DOCTYPE html>）
        if '<!DOCTYPE html>' not in content:
            print(f"  跳过: 已是Jekyll格式")
            return False
        
        # 转换内容
        new_content = create_jekyll_content(filepath, content)
        
        # 写回文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✓ 转换完成")
        return True
    
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return False

def main():
    """主函数"""
    posts_dir = BLOG_REPO / "posts"
    
    # 找到所有需要修复的文件
    files_to_fix = []
    for html_file in posts_dir.rglob("*.html"):
        if html_file.name == "index.html":
            continue
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if '<!DOCTYPE html>' in content:
                files_to_fix.append(html_file)
        except:
            pass
    
    print(f"找到 {len(files_to_fix)} 个需要修复的文件\n")
    
    # 处理每个文件
    success_count = 0
    for filepath in files_to_fix:
        if process_file(filepath):
            success_count += 1
    
    print(f"\n完成! 成功转换 {success_count}/{len(files_to_fix)} 个文件")

if __name__ == "__main__":
    main()
