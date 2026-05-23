#!/usr/bin/env python3
"""
HTML 转 Astro 博客格式工具
将 blog-repo 的 HTML 文章转换为 astro-blog 的 Markdown 格式
"""

import os
import re
import html
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

# 配置
BLOG_REPO = "/Users/halo/workspace/blog-repo"
ASTRO_BLOG = "/Users/halo/workspace/astro-blog"

def extract_metadata(html_file):
    """从 HTML 文件中提取元数据"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 提取 title
    title_tag = soup.find('title')
    title = title_tag.text.strip() if title_tag else ''
    
    # 提取 description
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    description = desc_tag['content'] if desc_tag else ''
    
    # 提取日期（从文件名）
    filename = os.path.basename(html_file)
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    date = date_match.group(1) if date_match else ''
    
    # 提取分类（从路径）
    rel_path = os.path.relpath(html_file, BLOG_REPO)
    parts = rel_path.split(os.sep)
    category = parts[1] if len(parts) > 1 else 'uncategorized'
    
    # 提取 slug（文件名去掉日期）
    slug = filename.replace(date + '-', '').replace('.html', '')
    
    # 提取正文内容（<article> 标签内）
    article = soup.find('article')
    if article:
        # 去掉 breadcrumb 和 post-title
        breadcrumb = article.find(class_='breadcrumb')
        if breadcrumb:
            breadcrumb.decompose()
        
        post_title = article.find(class_='post-title')
        if post_title:
            post_title.decompose()
        
        post_date = article.find(class_='post-date')
        if post_date:
            post_date.decompose()
        
        # 获取 HTML 内容
        content_html = str(article)
    else:
        content_html = ''
    
    return {
        'title': title,
        'description': description,
        'date': date,
        'category': category,
        'slug': slug,
        'content_html': content_html
    }

def html_to_markdown(html_content):
    """将 HTML 转换为 Markdown（简单版本）"""
    # 这里使用简单的正则替换，复杂场景可能需要 html2text 或类似库
    # 为简化，我们直接保留 HTML（Astro 支持在 Markdown 中混写 HTML）
    return html_content

def create_astro_post(metadata):
    """创建 Astro 格式的博客文章"""
    title = metadata['title']
    description = metadata['description']
    date = metadata['date']
    category = metadata['category']
    slug = metadata['slug']
    content_html = metadata['content_html']
    
    # 创建目录
    post_dir = os.path.join(ASTRO_BLOG, 'src', 'content', 'blog', category, f"{date}-{slug}")
    os.makedirs(post_dir, exist_ok=True)
    
    # 生成 frontmatter
    frontmatter = f"""---
title: "{title}"
description: "{description}"
date: {date}
category: "{category}"
tags: []
heroImage: ""
draft: false
---

{content_html}
"""
    
    # 写入 index.md
    output_file = os.path.join(post_dir, 'index.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
    
    print(f"✅ 已创建：{output_file}")
    return output_file

def copy_images(html_file, metadata):
    """复制图片到 astro-blog"""
    filename = os.path.basename(html_file)
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    if not date_match:
        return
    
    date = date_match.group(1)
    slug = metadata['slug']
    
    # 源图片目录
    src_img_dir = os.path.join(BLOG_REPO, 'images', slug)
    if not os.path.exists(src_img_dir):
        print(f"⚠️  图片目录不存在：{src_img_dir}")
        return
    
    # 目标图片目录
    dst_img_dir = os.path.join(ASTRO_BLOG, 'public', 'images', slug)
    os.makedirs(dst_img_dir, exist_ok=True)
    
    # 复制图片
    for img_file in os.listdir(src_img_dir):
        src_path = os.path.join(src_img_dir, img_file)
        dst_path = os.path.join(dst_img_dir, img_file)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"  📷 已复制图片：{img_file}")

def convert_html_to_astro(html_file):
    """转换单个 HTML 文件为 Astro 格式"""
    print(f"\n🔄 处理：{html_file}")
    
    # 提取元数据
    metadata = extract_metadata(html_file)
    
    if not metadata['title']:
        print(f"❌ 无法提取标题：{html_file}")
        return None
    
    print(f"  标题：{metadata['title']}")
    print(f"  日期：{metadata['date']}")
    print(f"  分类：{metadata['category']}")
    
    # 创建 Astro 文章
    output_file = create_astro_post(metadata)
    
    # 复制图片
    copy_images(html_file, metadata)
    
    return output_file

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python3 html-to-astro.py <html_file1> [html_file2] ...")
        print("\n示例：")
        print("  python3 html-to-astro.py /Users/halo/workspace/blog-repo/posts/life/2026-05-21-digital-minimalism-2026.html")
        print("  python3 html-to-astro.py /Users/halo/workspace/blog-repo/posts/investment/2026-05-21-*.html")
        sys.exit(1)
    
    html_files = sys.argv[1:]
    
    print(f"📦 HTML → Astro 转换工具")
    print(f"================================")
    print(f"源目录：{BLOG_REPO}")
    print(f"目标目录：{ASTRO_BLOG}")
    print(f"================================\n")
    
    converted = []
    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"❌ 文件不存在：{html_file}")
            continue
        
        result = convert_html_to_astro(html_file)
        if result:
            converted.append(result)
    
    print(f"\n✅ 转换完成！共 {len(converted)} 篇文章")
    print(f"\n📝 下一步：")
    print(f"  1. cd {ASTRO_BLOG}")
    print(f"  2. npm run build")
    print(f"  3. git add . && git commit -m 'feat: 添加新文章'")
    print(f"  4. git push origin main")

if __name__ == '__main__':
    main()
