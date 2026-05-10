#!/usr/bin/env python3
"""
HTML to Jekyll Markdown Converter
Converts static HTML blog posts to Jekyll Markdown format with frontmatter
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

# HTML to Markdown conversion rules
def html_to_markdown(html_content):
    """Convert basic HTML to Markdown"""
    
    # Remove scripts and styles
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)
    
    # Convert headings
    html_content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n\n', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n\n', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n\n', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1\n\n', html_content, flags=re.DOTALL)
    
    # Convert paragraph and line breaks
    html_content = re.sub(r'<p[^>]*>', '', html_content)
    html_content = re.sub(r'</p>', '\n\n', html_content)
    html_content = re.sub(r'<br\s*/?>', '\n', html_content)
    
    # Convert strong and bold
    html_content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', html_content, flags=re.DOTALL)
    
    # Convert emphasis
    html_content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', html_content, flags=re.DOTALL)
    
    # Convert links
    html_content = re.sub(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)', html_content, flags=re.DOTALL)
    
    # Convert blockquotes
    html_content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1\n\n', html_content, flags=re.DOTALL)
    
    # Convert pre and code
    html_content = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', r'```\n\1\n```\n\n', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', html_content, flags=re.DOTALL)
    
    # Convert unordered lists
    html_content = re.sub(r'<ul[^>]*>', '', html_content)
    html_content = re.sub(r'</ul>', '\n', html_content)
    html_content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', html_content, flags=re.DOTALL)
    
    # Convert ordered lists
    html_content = re.sub(r'<ol[^>]*>', '', html_content)
    html_content = re.sub(r'</ol>', '\n', html_content)
    html_content = re.sub(r'<li[^>]*>(.*?)</li>', r'1. \1\n', html_content, flags=re.DOTALL)
    
    # Convert horizontal rule
    html_content = re.sub(r'<hr\s*/?>', '\n---\n\n', html_content)
    
    # Convert div to paragraphs
    html_content = re.sub(r'<div[^>]*>', '\n', html_content)
    html_content = re.sub(r'</div>', '\n', html_content)
    
    # Remove remaining HTML tags
    html_content = re.sub(r'<[^>]+>', '', html_content)
    
    # Clean up whitespace
    html_content = re.sub(r'\n\s*\n', '\n\n', html_content)
    html_content = re.sub(r' +', ' ', html_content)
    html_content = html_content.strip()
    
    return html_content


def extract_title_from_html(html_content):
    """Extract title from HTML content"""
    # Try h1 first
    match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Try title tag
    match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    return "Untitled"


def extract_date_from_filename(filepath):
    """Extract date from filename like 2026-05-10-article-title.html"""
    filename = os.path.basename(filepath)
    match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return match.group(1)
    return datetime.now().strftime('%Y-%m-%d')


def extract_category_from_path(filepath):
    """Extract category from file path"""
    # Path format: posts/category/article.html
    parts = Path(filepath).parts
    if len(parts) >= 2 and parts[0] == 'posts':
        return parts[1]
    return 'uncategorized'


def extract_content_from_html(html_content):
    """Extract main content from HTML (between body tags or main_content section)"""
    # Try to find main content section
    match = re.search(r'<section[^>]*id=["\']main_content["\'][^>]*>(.*?)</section>', html_content, re.DOTALL)
    if match:
        return match.group(1)
    
    # Try body tag
    match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL)
    if match:
        return match.group(1)
    
    return html_content


def convert_html_to_markdown(filepath):
    """Convert an HTML file to Jekyll Markdown format"""
    
    # Skip index files
    if filepath.endswith('index.html'):
        return None
    
    # Read HTML file
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extract metadata
    title = extract_title_from_html(html_content)
    date = extract_date_from_filename(filepath)
    category = extract_category_from_path(filepath)
    content = extract_content_from_html(html_content)
    
    # Convert to Markdown
    markdown_content = html_to_markdown(content)
    
    # Create frontmatter
    frontmatter = f"""---
layout: single
title: "{title}"
date: {date}
categories: [{category}]
permalink: /posts/{category}/:title.html
author_profile: false
show_date: true
toc: true
---

"""
    
    # Combine frontmatter and content
    final_content = frontmatter + markdown_content
    
    return final_content


def main():
    """Main conversion function"""
    posts_dir = Path('posts')
    output_dir = Path('_posts')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    converted_count = 0
    error_count = 0
    
    # Walk through all HTML files
    for html_file in posts_dir.rglob('*.html'):
        # Skip index files
        if html_file.name == 'index.html':
            continue
        
        try:
            # Convert to Markdown
            markdown_content = convert_html_to_markdown(str(html_file))
            
            if markdown_content:
                # Generate output filename
                filename = html_file.stem + '.md'
                
                # Create category subdirectory in _posts
                category = html_file.parts[1] if len(html_file.parts) > 1 else 'uncategorized'
                category_dir = output_dir / category
                category_dir.mkdir(exist_ok=True)
                
                output_path = category_dir / filename
                
                # Write Markdown file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                converted_count += 1
                print(f"[OK] Converted: {html_file} -> {output_path}")
        
        except Exception as e:
            error_count += 1
            print(f"[ERROR] Error converting {html_file}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Conversion complete!")
    print(f"Converted: {converted_count} files")
    print(f"Errors: {error_count} files")
    print(f"Output directory: {output_dir}")


if __name__ == '__main__':
    main()