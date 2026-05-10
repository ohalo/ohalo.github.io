#!/usr/bin/env python3
"""
Add in-site search functionality to the homepage.
Uses client-side JavaScript for real-time search.
"""

import os
import re
import json

SEARCH_STYLES = '''
/* Search */
.search-section {
    margin: 24px 0;
    padding: 24px;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 12px;
}

.search-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}

.search-header h3 {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.search-header h3 i {
    color: var(--accent);
}

.search-input-wrapper {
    position: relative;
}

.search-input {
    width: 100%;
    padding: 12px 16px 12px 44px;
    font-size: 1rem;
    border: 2px solid var(--border);
    border-radius: 8px;
    background: var(--bg-primary);
    color: var(--text-primary);
    transition: border-color 0.2s;
    box-sizing: border-box;
}

.search-input:focus {
    outline: none;
    border-color: var(--accent);
}

.search-input::placeholder {
    color: var(--text-muted);
}

.search-icon {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
    font-size: 1rem;
}

.search-results {
    margin-top: 16px;
    max-height: 400px;
    overflow-y: auto;
}

.search-result-item {
    padding: 12px;
    border-bottom: 1px solid var(--border);
    transition: background 0.2s;
}

.search-result-item:last-child {
    border-bottom: none;
}

.search-result-item:hover {
    background: var(--bg-primary);
}

.search-result-item a {
    color: var(--text-primary);
    text-decoration: none;
    font-weight: 500;
    border: none;
    display: block;
    margin-bottom: 4px;
}

.search-result-item a:hover {
    color: var(--accent);
}

.search-result-meta {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.search-result-desc {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 4px;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.search-no-results {
    text-align: center;
    padding: 32px;
    color: var(--text-muted);
}

.search-no-results i {
    font-size: 2rem;
    margin-bottom: 12px;
    display: block;
}

.search-count {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--border);
}

.search-highlight {
    background: var(--accent);
    color: white;
    padding: 0 2px;
    border-radius: 2px;
}
'''

SEARCH_HTML = '''
<!-- Search Section -->
<section class="search-section">
    <div class="search-header">
        <h3><i class="fas fa-search"></i> 搜索文章</h3>
    </div>
    <div class="search-input-wrapper">
        <i class="fas fa-search search-icon"></i>
        <input type="text" class="search-input" id="searchInput" placeholder="输入关键词搜索文章..." autocomplete="off">
    </div>
    <div class="search-results" id="searchResults"></div>
</section>
'''

# All articles data - will be populated by script
SEARCH_DATA = '''
<script>
// All articles data for search
window.ALL_ARTICLES = %ARTICLES_JSON%;
</script>
'''

SEARCH_JS = '''
/* In-site Search */
(function() {
    var articles = window.ALL_ARTICLES || [];
    var searchInput = document.getElementById('searchInput');
    var searchResults = document.getElementById('searchResults');
    
    if (!searchInput || !searchResults || articles.length === 0) return;
    
    function highlight(text, query) {
        if (!query) return text;
        var regex = new RegExp('(' + query.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&') + ')', 'gi');
        return text.replace(regex, '<span class="search-highlight">$1</span>');
    }
    
    function search(query) {
        query = query.trim().toLowerCase();
        
        if (!query) {
            searchResults.innerHTML = '';
            return;
        }
        
        var results = articles.filter(function(article) {
            return article.title.toLowerCase().indexOf(query) !== -1 ||
                   article.desc.toLowerCase().indexOf(query) !== -1 ||
                   article.category.toLowerCase().indexOf(query) !== -1;
        });
        
        if (results.length === 0) {
            searchResults.innerHTML = '<div class="search-no-results"><i class="far fa-sad-tear"></i>没有找到匹配的文章</div>';
            return;
        }
        
        var html = '';
        results.slice(0, 10).forEach(function(article) {
            html += '<div class="search-result-item">';
            html += '<a href="' + article.url + '">' + highlight(article.title, query) + '</a>';
            html += '<div class="search-result-meta">';
            html += '<span>' + article.category + '</span> · ';
            html += '<span>' + article.date + '</span>';
            if (article.readTime) {
                html += ' · <span>' + article.readTime + '</span>';
            }
            html += '</div>';
            if (article.desc) {
                html += '<div class="search-result-desc">' + highlight(article.desc, query) + '</div>';
            }
            html += '</div>';
        });
        
        var countText = results.length > 10 ? '显示前10条，共 ' + results.length + ' 条' : '共 ' + results.length + ' 条';
        html += '<div class="search-count">' + countText + '</div>';
        
        searchResults.innerHTML = html;
    }
    
    // Debounce
    var debounceTimer;
    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(function() {
            search(searchInput.value);
        }, 200);
    });
})();
'''

def scan_articles(base_dir):
    """Scan all articles to build search index."""
    articles = []
    
    # Category name mapping
    category_names = {
        'posts/ai-tools': 'AI工具',
        'posts/ai-tools/claude-code': 'Claude Code',
        'posts/ai-tools/openclaw': 'OpenClaw',
        'posts/ai-tools/others': 'AI工具其他',
        'posts/ai-tools/hafw': 'HAFW',
        'posts/ai-tools/spec-kit': 'Spec Kit',
        'posts/ai-tools/workflow': 'AI工作流',
        'posts/ai-tools/skill-training': 'AI技能训练',
        'posts/ai-observation': 'AI观察',
        'posts/ai-observation/career': 'AI与职业',
        'posts/ai-observation/industry': 'AI行业观察',
        'posts/ai-observation/society': 'AI社会观察',
        'posts/ai-observation/indie-app-flywheel': '独立开发飞轮',
        'posts/hardware': '硬件数码',
        'posts/hardware/nas': 'NAS',
        'posts/hardware/others': '其他硬件',
        'posts/hardware/gpu-5070-9070-comparison': 'GPU对比',
        'posts/investment': '投资理财',
        'posts/investment/stock-analysis': '股票分析',
        'posts/reading': '读书',
        'posts/reading/book-review': '书评',
        'posts/career': '职业发展',
        'posts/tech-tips': '技术技巧',
        'posts/tech-tips/software': '软件使用',
        'posts/tech-tips/security': '安全技巧',
        'posts/life': '生活方式',
        'posts/archive': '归档',
    }
    
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['scripts', 'images', 'stylesheets', 'javascripts', 'blog']]
        
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, base_dir)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract title
                    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
                    title = title_match.group(1).strip() if title_match else ''
                    
                    # Clean title - remove any HTML tags
                    title = re.sub(r'<[^>]+>', '', title).strip()
                    
                    # Extract date
                    date_match = re.search(r'<span[^>]*class="date"[^>]*>([\d-]+)</span>', content)
                    date = date_match.group(1) if date_match else ''
                    
                    # Extract category from breadcrumb or path
                    category = category_names.get(os.path.dirname(rel_path), os.path.dirname(rel_path))
                    
                    # Extract description from meta or first paragraph
                    desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]+)"', content)
                    if not desc_match:
                        desc_match = re.search(r'<p[^>]*class="post-meta"[^>]*>(.*?)</p>', content, re.DOTALL)
                    desc = desc_match.group(1).strip() if desc_match else ''
                    desc = re.sub(r'<[^>]+>', '', desc).strip()
                    if len(desc) > 100:
                        desc = desc[:100] + '...'
                    
                    # Extract read time
                    read_time = ''
                    time_match = re.search(r'(\d+)\s*分钟', content)
                    if time_match:
                        read_time = time_match.group(1) + '分钟'
                    
                    # Build URL
                    url = '/' + rel_path.replace('.html', '')
                    
                    articles.append({
                        'title': title,
                        'url': url,
                        'date': date,
                        'category': category,
                        'desc': desc,
                        'readTime': read_time
                    })
                except Exception as e:
                    pass
    
    return articles

def add_search_to_homepage(html_content, articles_json):
    """Add search functionality to homepage."""
    if 'id="searchInput"' in html_content:
        return html_content, False
    
    # Add styles before </head>
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', '<style>' + SEARCH_STYLES + '</style>\n</head>')
    
    # Add search HTML - insert after hero section
    hero_end = html_content.find('</section>')
    if hero_end != -1:
        # Find the next </section> after hero
        first_section_end = html_content.find('</section>', hero_end + 10)
        if first_section_end != -1:
            # Insert search after first section
            search_section = SEARCH_HTML
            html_content = html_content[:first_section_end + 11] + search_section + html_content[first_section_end + 11:]
    
    # Add articles data before </body>
    if '</body>' in html_content:
        data_script = SEARCH_DATA.replace('%ARTICLES_JSON%', articles_json)
        html_content = html_content.replace('</body>', data_script + '\n</body>')
    
    # Add search JS before </body>
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', '<script>' + SEARCH_JS + '</script>\n</body>')
    
    return html_content, True

def main():
    base_dir = '/Users/halo/.qclaw/workspace/blog-repo'
    
    # Scan articles
    print("Scanning articles for search index...")
    articles = scan_articles(base_dir)
    print(f"Found {len(articles)} articles")
    
    articles_json = json.dumps(articles, ensure_ascii=False)
    
    # Update homepage
    print("\nUpdating homepage with search...")
    homepage_path = os.path.join(base_dir, 'index.html')
    with open(homepage_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, added = add_search_to_homepage(content, articles_json)
    
    if added:
        with open(homepage_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Added search to homepage")
    else:
        print("Search already exists or failed to add")

if __name__ == '__main__':
    main()
