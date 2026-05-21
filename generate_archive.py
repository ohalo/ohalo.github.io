#!/usr/bin/env python3
"""
生成博客归档页（posts/archive/index.html）
扫描posts/目录下所有HTML文件，按年月分组，生成归档列表
"""

import os
import re
from datetime import datetime
from collections import defaultdict

BLOG_ROOT = "/Users/halo/workspace/blog-repo"
POSTS_DIR = os.path.join(BLOG_ROOT, "posts")
ARCHIVE_DIR = os.path.join(POSTS_DIR, "archive")
OUTPUT_FILE = os.path.join(ARCHIVE_DIR, "index.html")

def extract_metadata(html_file):
    """从HTML文件中提取标题和日期"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题
        title_match = re.search(r'<h1[^>]*class="post-title"[^>]*>(.*?)</h1>', content, re.DOTALL)
        if not title_match:
            title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        title = title_match.group(1).strip() if title_match else "无标题"
        
        # 提取日期
        date_match = re.search(r'<div[^>]*class="post-date"[^>]*>.*?(\d{4}-\d{2}-\d{2})', content, re.DOTALL)
        if not date_match:
            # 从文件名提取日期
            filename = os.path.basename(html_file)
            date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
        date = date_match.group(1) if date_match else "1970-01-01"
        
        return title, date
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
        return None, None

def scan_posts():
    """扫描所有文章"""
    posts = []
    
    for root, dirs, files in os.walk(POSTS_DIR):
        # 跳过archive目录
        if 'archive' in root:
            continue
        
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                filepath = os.path.join(root, file)
                title, date = extract_metadata(filepath)
                
                if title and date:
                    # 计算相对路径
                    rel_path = os.path.relpath(filepath, POSTS_DIR)
                    rel_path = '/' + os.path.join('posts', rel_path).replace('\\', '/')
                    
                    posts.append({
                        'title': title,
                        'date': date,
                        'path': rel_path,
                        'year': date[:4],
                        'month': date[5:7]
                    })
    
    return posts

def generate_archive_html(posts):
    """生成归档页HTML"""
    # 按年月分组
    grouped = defaultdict(list)
    for post in posts:
        key = f"{post['year']}-{post['month']}"
        grouped[key].append(post)
    
    # 按日期倒序排序
    for key in grouped:
        grouped[key].sort(key=lambda x: x['date'], reverse=True)
    
    # 按年月倒序排序
    sorted_keys = sorted(grouped.keys(), reverse=True)
    
    # 统计总文章数
    total_posts = len(posts)
    
    # 生成HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="halo的技术博客文章归档，共{total_posts}篇">
    
    <link rel="stylesheet" type="text/css" href="/stylesheets/modern-theme.css" media="screen">
    <link rel="stylesheet" href="/stylesheets/article.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <script src="/javascripts/google-analytics.js"></script>
    <title>文章归档 - halo的技术博客</title>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    
    <meta property="og:type" content="website">
    <meta property="og:title" content="文章归档 - halo的技术博客">
    <meta property="og:description" content="halo的技术博客文章归档，共{total_posts}篇">
    <meta property="og:image" content="https://blog.halo26812.eu.org/images/social-preview.jpg">
    <meta property="og:url" content="https://blog.halo26812.eu.org/posts/archive/">
    
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:title" content="文章归档 - halo的技术博客">
    <meta property="twitter:description" content="halo的技术博客文章归档，共{total_posts}篇">
    <meta property="twitter:image" content="https://blog.halo26812.eu.org/images/social-preview.jpg">
    </head>
<body>
    <div id="header-placeholder"></div>
    <main class="container">
        <h1>文章归档</h1>
        <p>共 {total_posts} 篇文章</p>
'''
    
    current_year = None
    current_month_posts = []
    
    for key in sorted_keys:
        year, month = key.split('-')
        month_name = f"{int(month)}月"
        
        # 年中分组
        if year != current_year:
            if current_year:
                html += f'            </ul>\n'
            html += f'            <h3 class="archive-year">{year}年</h3>\n'
            current_year = year
        
        # 月分组
        month_posts = grouped[key]
        html += f'            <h4 class="archive-month">{month_name}（{len(month_posts)}篇）</h4>\n'
        html += '            <ul class="post-list">\n'
        
        for post in month_posts:
            html += f'              <li><a href="{post["path"]}">{post["title"]}</a> <span class="date">{post["date"]}</span></li>\n'
        
        html += '            </ul>\n'
    
    html += '''    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 halo.</p>
        </div>
    </footer>

    <script src="/javascripts/header.js"></script>
    <script src="/javascripts/sidebar.js"></script>
</body>
</html>'''
    
    return html

def main():
    print("开始扫描文章...")
    posts = scan_posts()
    print(f"共找到 {len(posts)} 篇文章")
    
    print("生成归档页...")
    html = generate_archive_html(posts)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"归档页已生成: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
