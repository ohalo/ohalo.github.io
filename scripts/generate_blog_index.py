#!/usr/bin/env python3
"""
Blog Index Generator
Scans all article HTML files, extracts metadata, and generates:
1. ALL_ARTICLES JavaScript array for homepage search
2. Latest articles section for homepage
3. Featured articles section for homepage

Usage:
    python3 generate_blog_index.py

Cron job setup (daily at 6 AM):
    crontab -e
    0 6 * * * cd /path/to/blog-repo && /usr/bin/python3 generate_blog_index.py >> /path/to/blog-repo/logs/generate_index.log 2>&1
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
import sys

# Ensure UTF-8 output (Python 3.7+)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass  # Older Python version, assume UTF-8 is default

# Configuration
BLOG_REPO = Path(__file__).parent.parent
POSTS_DIR = BLOG_REPO / "posts"
INDEX_HTML = BLOG_REPO / "index.html"
FEATURED_CONFIG = BLOG_REPO / "scripts" / "featured_articles.json"
OUTPUT_LOG = BLOG_REPO / "logs" / "generate_index.log"

# Category mapping (folder name -> display name)
CATEGORY_MAP = {
    "ai-tools": "AI工具",
    "ai-observation": "AI观察",
    "hardware": "硬件数码",
    "career": "职业成长",
    "life": "生活方式",
    "investment": "投资理财",
    "reading": "阅读思考",
    "tech-tips": "效率技巧",
}

# Number of articles to show in each section
LATEST_COUNT = 10
FEATURED_COUNT = 6


def extract_date_from_filename(filename):
    """Extract date from filename like '2026-05-10-article-title.html'"""
    match = re.match(r'^(\d{4}-\d{2}-\d{2})-.+\.html$', filename)
    if match:
        return match.group(1)
    return None


def extract_category_from_path(file_path):
    """Extract category from file path like 'posts/career/2026-05-10-xxx.html'"""
    parts = file_path.parts
    if len(parts) >= 2:
        folder = parts[1]
        return CATEGORY_MAP.get(folder, folder)
    return "未分类"


def extract_title_from_html(html_content):
    """Extract title from <title> tag"""
    match = re.search(r'<title>([^<]+)</title>', html_content)
    if match:
        title = match.group(1)
        # Remove site name suffix like " - halo的技术博客"
        title = re.sub(r'\s*-\s*[^_]*的技术博客\s*$', '', title)
        # Fix malformed titles with literal \" (backslash + quote) by replacing with proper escaped quote
        # This handles cases where HTML was written with unescaped quotes in <title>
        title = title.replace('\\"', '\\\\"')  # \" -> \\"
        return title.strip()
    return ""


def extract_description_from_html(html_content):
    """Extract meta description"""
    # Try og:description first
    match = re.search(r'<meta property="og:description" content="([^"]+)"', html_content)
    if match:
        desc = match.group(1)
        # Fix malformed descriptions with literal \" (backslash + quote)
        desc = desc.replace('\\"', '\\\\"')  # \" -> \\"
        return desc
    # Try generic description
    match = re.search(r'<meta name="description" content="([^"]+)"', html_content)
    if match:
        desc = match.group(1)
        desc = desc.replace('\\"', '\\\\"')
        return desc
    return ""


def extract_description_from_html(html_content):
    """Extract meta description"""
    # Try og:description first
    match = re.search(r'<meta property="og:description" content="([^"]+)"', html_content)
    if match:
        return match.group(1)
    # Try generic description
    match = re.search(r'<meta name="description" content="([^"]+)"', html_content)
    if match:
        return match.group(1)
    return ""


def extract_read_time_from_html(html_content):
    """Extract read time from meta or content"""
    # Try meta tag
    match = re.search(r'<meta name="readTime" content="([^"]+)"', html_content)
    if match:
        return match.group(1)
    # Try to find "X分钟" pattern in content
    match = re.search(r'(\d+)\s*分钟', html_content)
    if match:
        return match.group(1) + "分钟"
    return ""


def scan_articles():
    """Scan all article HTML files and extract metadata"""
    articles = []
    
    for html_file in POSTS_DIR.rglob("*.html"):
        # Skip index pages and archive pages
        if "index.html" in str(html_file):
            continue
        
        # Skip files in root posts directory (those are category pages)
        if html_file.parent == POSTS_DIR:
            continue
        
        try:
            content = html_file.read_text(encoding='utf-8')
            
            # Extract date from filename
            date = extract_date_from_filename(html_file.name)
            if not date:
                continue  # Skip files without proper date in filename
            
            # Extract category from path
            category = extract_category_from_path(html_file)
            
            # Extract other metadata
            title = extract_title_from_html(content)
            description = extract_description_from_html(content)
            read_time = extract_read_time_from_html(content)
            
            # Generate URL (keep .html extension)
            url = str(html_file.relative_to(BLOG_REPO)).replace('\\', '/')
            url = "/" + url
            
            article = {
                "title": title,
                "url": url,
                "date": date,
                "category": category,
                "desc": description,
                "readTime": read_time,
            }
            articles.append(article)
            
        except Exception as e:
            print(f"Error processing {html_file}: {e}", file=sys.stderr)
    
    # Sort by date descending (newest first)
    articles.sort(key=lambda x: x["date"], reverse=True)
    
    return articles


def load_featured_articles():
    """Load manually curated featured articles list"""
    if FEATURED_CONFIG.exists():
        try:
            with open(FEATURED_CONFIG, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("featured_urls", [])
        except Exception as e:
            print(f"Error loading featured config: {e}", file=sys.stderr)
    return []


def generate_all_articles_js(articles):
    """Generate ALL_ARTICLES JavaScript array.
    
    json.dumps with ensure_ascii=False handles:
    - Chinese characters: preserved as-is (valid in UTF-8 JS)
    - Chinese quotes " ": preserved as-is (U+201C/U+201D, NOT string delimiters)
    - ASCII backslash-n \\: becomes \\n (escape sequence)
    - ASCII quotes \": already escaped by json.dumps
    
    Result is a valid JS string literal with proper escaping.
    """
    js_lines = ["window.ALL_ARTICLES = ["]
    for article in articles:
        # json.dumps already produces valid JS: "content with proper escapes"
        # For ASCII " inside content, json.dumps escapes as \"
        # For Chinese " or " (U+201C/U+201D), they remain as-is (valid in JS)
        row = {k: article.get(k, "") for k in ['title', 'url', 'date', 'category', 'desc', 'readTime']}
        js_lines.append(f'    {json.dumps(row, ensure_ascii=False)},')
    js_lines.append("];")
    return "\n".join(js_lines)
    js_lines.append("];")
    return "\n".join(js_lines)


def generate_latest_articles_html(articles, count=LATEST_COUNT):
    """Generate HTML for latest articles section"""
    latest = articles[:count]
    
    html_lines = [
        '',
        '            <h2><i class="fas fa-fire"></i> 最新文章</h2>',
        '            <ul class="post-list" id="homeArticleList">',
    ]
    
    for article in latest:
        date_obj = datetime.strptime(article["date"], "%Y-%m-%d")
        date_str = date_obj.strftime("%Y-%m-%d")
        
        read_time_html = ""
        if article["readTime"]:
            read_time_html = f'<span class="reading-time">📖 {article["readTime"]}</span>'
        
        li = f'                <li><a href="{article["url"]}">{article["title"]}</a> <span class="date">{date_str}</span> {read_time_html}</li>'
        html_lines.append(li)
    
    html_lines.append('            </ul>')
    return '\n'.join(html_lines)


def generate_featured_articles_html(articles, featured_urls, count=FEATURED_COUNT):
    """Generate HTML for featured articles section"""
    # Filter to only featured articles that exist in our article list
    url_to_article = {a["url"]: a for a in articles}
    featured = []
    for url in featured_urls:
        if url in url_to_article:
            featured.append(url_to_article[url])
    
    # Limit to count
    featured = featured[:count]
    
    if not featured:
        return ""
    
    html_lines = [
        '',
        '        <!-- Featured Section -->',
        '        <section class="featured-section">',
        '            <h2><i class="fas fa-star" style="color: #f59e0b;"></i> 精选文章</h2>',
        '            <div class="featured-grid">',
    ]
    
    for article in featured:
        date_obj = datetime.strptime(article["date"], "%Y-%m-%d")
        date_str = date_obj.strftime("%Y-%m-%d")
        
        # Truncate description for display
        desc = article["desc"]
        if len(desc) > 80:
            desc = desc[:80] + "..."
        
        read_time_html = ""
        if article["readTime"]:
            read_time_html = f'<span><i class="far fa-clock"></i> {article["readTime"]}</span>'
        
        card = f'''                <a href="{article["url"]}" class="featured-card">
                    <span class="featured-card-category">{article["category"]}</span>
                    <h3 class="featured-card-title">{article["title"]}</h3>
                    <p class="featured-card-desc">{desc}</p>
                    <div class="featured-card-meta">
                        <span><i class="far fa-calendar"></i> {date_str}</span>
                        {read_time_html}
                    </div>
                </a>'''
        html_lines.append(card)
    
    html_lines.append('            </div>')
    html_lines.append('        </section>')
    return '\n'.join(html_lines)


def update_homepage(articles, all_articles_js, latest_html, featured_html):
    """Update the homepage HTML with new article data"""
    if not INDEX_HTML.exists():
        print(f"Error: {INDEX_HTML} not found", file=sys.stderr)
        return False
    
    try:
        content = INDEX_HTML.read_text(encoding='utf-8')
        
        # Update category counts
        category_counts = {}
        for article in articles:
            cat = article.get('category', '')
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Update category count in HTML
        # Pattern: <li><a href="/posts/CATEGORY/">...</a> <span class="date">NUM篇</span></li>
        for cat_name, count in category_counts.items():
            # Find the category link and update the count
            pattern_cat = rf'(<li><a href="/posts/[^"]+/"><i class="fas [^"]+"></i> {re.escape(cat_name)}</a>\s*<span class="date">)\d+篇(</span></li>)'
            replacement = f'\g<1>{count}篇\g<2>'
            content = re.sub(pattern_cat, replacement, content)
        
        # Find and replace ALL_ARTICLES
        # Pattern: window.ALL_ARTICLES = [...];
        pattern_all = r'window\.ALL_ARTICLES\s*=\s*\[[\s\S]*?\];'
        if re.search(pattern_all, content):
            content = re.sub(pattern_all, all_articles_js, content)
        else:
            print("Warning: ALL_ARTICLES not found in homepage, inserting before </script>", file=sys.stderr)
            # Try to insert before closing </script> tag or </body>
            if '</script>' in content:
                # Find the last </script> tag and insert before it
                last_script_end = content.rfind('</script>')
                if last_script_end > 0:
                    content = content[:last_script_end] + '\n' + all_articles_js + '\n' + content[last_script_end:]
            elif '</body>' in content:
                content = content.replace('</body>', '<script>\n' + all_articles_js + '\n</script>\n</body>')
        
        # Find and replace latest articles section
        # Match from <h2> through </ul> (the article list)
        pattern_latest = r'(<h2><i class="fas fa-fire"></i>\s*最新文章</h2>[\s\S]*?</ul>)'
        if re.search(pattern_latest, content):
            content = re.sub(pattern_latest, latest_html, content)
        else:
            print("Warning: Latest articles section not found", file=sys.stderr)
        
        # Find and replace featured articles section
        # Match from <!-- Featured Section --> through </section>
        pattern_featured = r'(<!-- Featured Section -->[\s\S]*?</section>)'
        if re.search(pattern_featured, content):
            content = re.sub(pattern_featured, '\n' + featured_html.strip() + '\n', content)
        
        INDEX_HTML.write_text(content, encoding='utf-8')
        return True
        
    except Exception as e:
        print(f"Error updating homepage: {e}", file=sys.stderr)
        return False


def ensure_logs_dir():
    """Ensure logs directory exists"""
    logs_dir = BLOG_REPO / "logs"
    if not logs_dir.exists():
        logs_dir.mkdir(exist_ok=True)


def main():
    """Main function"""
    print(f"Starting blog index generation at {datetime.now()}")
    ensure_logs_dir()
    
    # Scan all articles
    print("Scanning articles...")
    articles = scan_articles()
    print(f"Found {len(articles)} articles")
    
    if not articles:
        print("No articles found, exiting")
        return
    
    # Load featured articles
    print("Loading featured articles config...")
    featured_urls = load_featured_articles()
    print(f"Featured articles: {len(featured_urls)}")
    
    # Generate JavaScript for ALL_ARTICLES
    print("Generating ALL_ARTICLES JavaScript...")
    all_articles_js = generate_all_articles_js(articles)
    
    # Generate HTML for sections
    print("Generating latest articles HTML...")
    latest_html = generate_latest_articles_html(articles, LATEST_COUNT)
    
    print("Generating featured articles HTML...")
    featured_html = generate_featured_articles_html(articles, featured_urls, FEATURED_COUNT)
    
    # Update homepage
    print("Updating homepage...")
    if update_homepage(articles, all_articles_js, latest_html, featured_html):
        print("Homepage updated successfully!")
    else:
        print("Failed to update homepage", file=sys.stderr)
    
    # Log completion
    print(f"Blog index generation completed at {datetime.now()}")


if __name__ == "__main__":
    main()
