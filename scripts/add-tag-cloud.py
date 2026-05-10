#!/usr/bin/env python3
"""
Add category tag cloud to homepage and article sidebars.
Tags are based on existing categories with varying sizes based on article count.
"""

import os
import re
import json
from collections import defaultdict

TAG_CLOUD_STYLES = '''
/* Tag Cloud */
.tag-cloud {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    padding: 16px 0;
}

.tag-cloud a {
    display: inline-block;
    padding: 6px 14px;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 20px;
    color: var(--text-secondary);
    font-size: 0.85rem;
    text-decoration: none;
    transition: all 0.2s;
    white-space: nowrap;
}

.tag-cloud a:hover {
    background: var(--accent);
    border-color: var(--accent);
    color: white;
    transform: translateY(-2px);
}

.tag-cloud .tag-size-1 { font-size: 0.75rem; padding: 4px 10px; }
.tag-cloud .tag-size-2 { font-size: 0.85rem; }
.tag-cloud .tag-size-3 { font-size: 0.95rem; padding: 8px 16px; }
.tag-cloud .tag-size-4 { font-size: 1.05rem; padding: 8px 18px; }
.tag-cloud .tag-size-5 { font-size: 1.15rem; padding: 10px 20px; font-weight: 600; }

.sidebar-section .tag-cloud {
    padding: 8px 0;
}

.sidebar-section .tag-cloud a {
    font-size: 0.8rem;
    padding: 4px 10px;
}

.sidebar-section .tag-cloud .tag-size-3,
.sidebar-section .tag-cloud .tag-size-4,
.sidebar-section .tag-cloud .tag-size-5 {
    font-size: 0.85rem;
    padding: 6px 12px;
}

/* Homepage Tag Cloud Section */
.tag-cloud-section {
    margin: 32px 0;
    padding: 24px;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 12px;
}

.tag-cloud-section h3 {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 16px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.tag-cloud-section h3 i {
    color: var(--accent);
}
'''

TAG_CLOUD_DATA = '''
<script>
// Category tag cloud data - auto-generated
window.CATEGORY_TAGS = %CATEGORIES_JSON%;
</script>
'''

TAG_CLOUD_HTML_HOME = '''
<!-- Tag Cloud Section -->
<section class="tag-cloud-section">
    <h3><i class="fas fa-tags"></i> 探索主题</h3>
    <div class="tag-cloud" id="homeTagCloud"></div>
</section>
'''

TAG_CLOUD_HTML_SIDEBAR = '''
<!-- Category Tags -->
<div class="sidebar-section tags-section">
    <h3 class="sidebar-title"><i class="fas fa-tags"></i> 主题标签</h3>
    <div class="tag-cloud" id="sidebarTagCloud"></div>
</div>
'''

TAG_CLOUD_JS = '''
/* Tag Cloud Initialization */
(function() {
    var tags = window.CATEGORY_TAGS || [];
    if (tags.length === 0) return;
    
    // Sort by article count
    tags.sort(function(a, b) { return b.count - a.count; });
    
    var maxCount = tags[0] ? tags[0].count : 1;
    var minCount = tags[tags.length - 1] ? tags[tags.length - 1].count : 1;
    
    function getTagSize(count) {
        if (maxCount === minCount) return 3;
        var ratio = (count - minCount) / (maxCount - minCount);
        if (ratio < 0.25) return 1;
        if (ratio < 0.5) return 2;
        if (ratio < 0.75) return 3;
        if (ratio < 0.9) return 4;
        return 5;
    }
    
    function renderCloud(containerId) {
        var container = document.getElementById(containerId);
        if (!container) return;
        
        tags.forEach(function(tag) {
            var a = document.createElement('a');
            a.href = tag.url;
            a.textContent = tag.name + ' (' + tag.count + ')';
            a.className = 'tag-size-' + getTagSize(tag.count);
            container.appendChild(a);
        });
    }
    
    renderCloud('homeTagCloud');
    renderCloud('sidebarTagCloud');
})();
'''

def scan_categories(base_dir):
    """Scan all categories and count articles."""
    categories = defaultdict(lambda: {'count': 0, 'url': '', 'name': ''})
    
    # Map of category paths to display names
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
    
    # Scan directories for index.html files
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['scripts', 'images', 'stylesheets', 'javascripts', 'blog']]
        
        if 'index.html' in files:
            # Count HTML files in this directory (articles)
            html_files = [f for f in files if f.endswith('.html') and f != 'index.html']
            article_count = len(html_files)
            
            if article_count > 0:
                rel_path = os.path.relpath(root, base_dir)
                
                # Get display name
                name = category_names.get(rel_path, rel_path.replace('posts/', '').replace('/', ' / '))
                
                # Determine URL
                if rel_path == base_dir.replace(base_dir.rsplit('/', 1)[0], '').lstrip('/'):
                    url = '/'
                else:
                    url = '/' + rel_path + '/'
                
                categories[rel_path] = {
                    'name': name,
                    'count': article_count,
                    'url': url
                }
    
    return list(categories.values())

def add_tag_cloud_to_homepage(html_content, categories_json):
    """Add tag cloud to homepage."""
    if 'id="homeTagCloud"' in html_content:
        return html_content, False
    
    # Add styles before </head>
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', '<style>' + TAG_CLOUD_STYLES + '</style>\n</head>')
    
    # Add category data
    if '</body>' in html_content:
        data_script = TAG_CLOUD_DATA.replace('%CATEGORIES_JSON%', categories_json)
        html_content = html_content.replace('</body>', data_script + '\n</body>')
    
    # Add tag cloud HTML after hero section or before categories
    if '<section class="categories-grid">' in html_content:
        html_content = html_content.replace(
            '<section class="categories-grid">',
            TAG_CLOUD_HTML_HOME + '\n<section class="categories-grid">'
        )
    elif '<div class="post-list">' in html_content:
        html_content = html_content.replace(
            '<div class="post-list">',
            TAG_CLOUD_HTML_HOME + '\n<div class="post-list">'
        )
    
    # Add JS before </body>
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', '<script>' + TAG_CLOUD_JS + '</script>\n</body>')
    
    return html_content, True

def add_tag_cloud_to_sidebar(html_content):
    """Add tag cloud to article sidebar."""
    if 'class="sidebar"' not in html_content:
        return html_content, False
    
    if 'id="sidebarTagCloud"' in html_content:
        return html_content, False
    
    # Add tag cloud HTML before </aside>
    if '</aside>' in html_content:
        html_content = html_content.replace('</aside>', TAG_CLOUD_HTML_SIDEBAR + '\n    </aside>')
    
    return html_content, True

def process_homepage(filepath, categories_json):
    """Process homepage."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, added = add_tag_cloud_to_homepage(content, categories_json)
    
    if added:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def process_article(filepath):
    """Process article page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, added = add_tag_cloud_to_sidebar(content)
    
    if added:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    base_dir = '/Users/halo/.qclaw/workspace/blog-repo'
    
    # Scan categories
    print("Scanning categories...")
    categories = scan_categories(base_dir)
    categories_json = json.dumps(categories, ensure_ascii=False)
    print(f"Found {len(categories)} categories")
    for cat in sorted(categories, key=lambda x: x['count'], reverse=True)[:10]:
        print(f"  {cat['name']}: {cat['count']} articles")
    
    # Update homepage
    print("\nUpdating homepage...")
    homepage_path = os.path.join(base_dir, 'index.html')
    if process_homepage(homepage_path, categories_json):
        print("  Added tag cloud to homepage")
    
    # Update article pages (sample - only update a few for sidebar)
    print("\nUpdating article sidebars...")
    updated = 0
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['scripts', 'images', 'stylesheets', 'javascripts', 'blog']]
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                filepath = os.path.join(root, file)
                try:
                    if process_article(filepath):
                        updated += 1
                except Exception as e:
                    pass
        # Only process first level articles to avoid too many updates
        break
    
    print(f"  Added tag cloud to {updated} article sidebars")

if __name__ == '__main__':
    main()
