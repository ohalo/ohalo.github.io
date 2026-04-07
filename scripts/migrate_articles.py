#!/usr/bin/env python3
"""
批量迁移 HTML 文章到 Jekyll Markdown 格式 - 修复版
使用文件修改时间作为文章日期
"""
import os
import re
from pathlib import Path
from datetime import datetime

BLOG_ROOT = Path.home() / ".qclaw/workspace/blog-repo"

# 分类映射
CATEGORY_MAP = {
    "ai-tools": "AI工具",
    "society-observation": "社会观察", 
    "entrepreneurship": "创业思考",
    "tech-tips": "技术技巧"
}

def get_file_date(file_path):
    """获取文件修改日期"""
    mtime = os.path.getmtime(file_path)
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

def extract_article(html_path):
    """提取文章元数据和内容"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题
    h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    title = h1_match.group(1) if h1_match else html_path.stem
    
    # 从路径提取分类
    rel_path = html_path.relative_to(BLOG_ROOT / "posts")
    category = rel_path.parts[0] if len(rel_path.parts) > 1 else "uncategorized"
    category_name = CATEGORY_MAP.get(category, category)
    
    # 使用文件修改时间作为日期
    date = get_file_date(html_path)
    
    # 提取数据来源 - 格式: 数据来源：xxx
    source = "原创"
    source_match = re.search(r'<em>数据来源[：:]\s*([^<]+)</em>', content)
    if source_match:
        source = source_match.group(1).strip()
    
    # 提取标签 - 格式: 🔖 标签1, 标签2, 标签3
    tags = []
    tags_match = re.search(r'🔖\s*([^<]+)</div>', content)
    if tags_match:
        tags_str = tags_match.group(1).strip()
        tags = [t.strip() for t in tags_str.split(',') if t.strip()]
    
    # 提取正文内容 - 找到第一个 <p> 或 <hr> 开始
    # 跳过 header/nav 部分
    body_start = content.find('<body')
    body_start = content.find('>', body_start) + 1 if body_start != -1 else 0
    
    # 找到 giscus 或 </body> 作为结束
    giscus_pos = content.find('<script src="https://giscus.app', body_start)
    if giscus_pos == -1:
        giscus_pos = content.find('<div class="giscus"', body_start)
    body_end = content.find('</body>')
    end_pos = min(p for p in [giscus_pos, body_end] if p > body_start) if any(p > body_start for p in [giscus_pos, body_end]) else len(content)
    
    body = content[body_start:end_pos]
    
    # 清理内容
    # 去掉 style 标签
    body = re.sub(r'<style>.*?</style>', '', body, flags=re.DOTALL)
    # 去掉 script 标签
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    # 去掉 header 部分
    body = re.sub(r'<header>.*?</header>', '', body, flags=re.DOTALL)
    # 去掉 nav 部分
    body = re.sub(r'<nav>.*?</nav>', '', body, flags=re.DOTALL)
    # 去掉 div class="nav" 部分
    body = re.sub(r'<div class="nav">.*?</div>', '', body, flags=re.DOTALL)
    # 去掉 div class="meta" 部分（模板会自动加）
    body = re.sub(r'<div class="meta">.*?</div>', '', body, flags=re.DOTALL)
    # 去掉数据来源行（模板会自动加）
    body = re.sub(r'<p><em>数据来源[：:][^<]*</em></p>', '', body)
    # 去掉第一个 h1（模板会自动加）
    body = re.sub(r'<h1[^>]*>[^<]*</h1>', '', body, count=1)
    # 去掉多余的 div 包裹
    body = re.sub(r'<div class="container">.*?<section id="main_content">', '', body, flags=re.DOTALL)
    body = re.sub(r'</section>.*?</div>\s*</div>', '', body, flags=re.DOTALL)
    # 清理多余空白
    body = body.strip()
    
    return {
        'title': title,
        'date': date,
        'category': category,
        'category_name': category_name,
        'tags': tags,
        'source': source,
        'content': body
    }

def create_markdown(article, output_path):
    """生成 HTML 文件（不是 .md，因为 GitHub Pages 不支持 kramdown HTML 渲染）"""
    # 转义标题中的引号
    title = article['title'].replace('"', '\\"')
    
    # 构建标签 YAML
    tags_yaml = ""
    if article.get('tags'):
        tags_str = ", ".join([f'"{t}"' for t in article['tags']])
        tags_yaml = f"\ntags: [{tags_str}]"
    
    # 构建来源 YAML
    source_yaml = ""
    if article.get('source') and article['source'] != "原创":
        source_escaped = article['source'].replace('"', '\\"')
        source_yaml = f'\nsource: "{source_escaped}"'
    
    front_matter = f"""---
layout: post
title: "{title}"
date: {article['date']}
category: {article['category']}
category_name: "{article['category_name']}"{tags_yaml}{source_yaml}
---

"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(article['content'])
    
    return True

def main():
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    posts_dir = BLOG_ROOT / "posts"
    output_dir = BLOG_ROOT / "_posts"
    
    # 清理并重建输出目录
    for cat in CATEGORY_MAP.keys():
        cat_dir = output_dir / cat
        cat_dir.mkdir(parents=True, exist_ok=True)
        # 清理旧文件（.md 和 .html）
        for f in cat_dir.glob("*.md"):
            f.unlink()
        for f in cat_dir.glob("*.html"):
            f.unlink()
    
    count = 0
    errors = []
    
    for html_file in sorted(posts_dir.rglob("*.html")):
        if html_file.name == "index.html":
            continue
        
        try:
            article = extract_article(html_file)
            
            # 生成文件名 - 使用 .html 扩展名
            output_name = f"{article['date']}-{html_file.stem}.html"
            output_path = output_dir / article['category'] / output_name
            
            create_markdown(article, output_path)
            print(f"OK: {article['date']} - {article['title'][:30]}...")
            count += 1
        except Exception as e:
            errors.append(f"{html_file.name}: {e}")
            print(f"FAIL: {html_file.name}")
    
    print(f"\n{'='*50}")
    print(f"Done! Converted {count} articles")
    if errors:
        print(f"Failed: {len(errors)}")
        for e in errors:
            print(f"  - {e}")

if __name__ == "__main__":
    main()
