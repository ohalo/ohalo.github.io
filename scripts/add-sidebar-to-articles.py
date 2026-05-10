#!/usr/bin/env python3
"""
Add sidebar to article pages.
Sidebar includes: Author card, Table of Contents (auto-gen via JS), Related articles (auto-gen via JS)
"""

import os
import re

SIDEBAR_HTML = '''
        <!-- Sidebar -->
        <aside class="sidebar">
            <!-- Author Card -->
            <div class="sidebar-section author-card">
                <img src="https://avatars.githubusercontent.com/u/2868547?v=4" alt="halo" class="author-avatar">
                <h3 class="author-name">halo</h3>
                <p class="author-bio">40岁创业者，探索AI时代的工作方式</p>
                <div class="author-social">
                    <a href="https://github.com/ohalo" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
                    <a href="https://www.zhihu.com/" target="_blank" title="知乎"><i class="fab fa-zhihu"></i></a>
                </div>
            </div>
            
            <!-- Table of Contents -->
            <div class="sidebar-section toc-section">
                <h3 class="sidebar-title"><i class="fas fa-list-ul"></i> 目录</h3>
                <nav id="toc-nav" class="toc-nav"></nav>
            </div>
            
            <!-- Related Articles -->
            <div class="sidebar-section related-section">
                <h3 class="sidebar-title"><i class="fas fa-bookmark"></i> 相关文章</h3>
                <ul class="related-list" id="related-list"></ul>
            </div>
        </aside>
'''

SIDEBAR_STYLES = '''
/* Sidebar Layout */
.post-layout {
    display: flex;
    gap: 48px;
    align-items: flex-start;
}

.post-layout .post-content-wrapper {
    flex: 1;
    min-width: 0;
}

.post-layout .sidebar {
    width: 280px;
    flex-shrink: 0;
    position: sticky;
    top: 32px;
    max-height: calc(100vh - 64px);
    overflow-y: auto;
}

/* Sidebar Sections */
.sidebar-section {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}

.sidebar-section:last-child {
    margin-bottom: 0;
}

/* Author Card */
.author-card {
    text-align: center;
}

.author-avatar {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    border: 3px solid var(--accent);
    margin-bottom: 12px;
}

.author-name {
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 8px 0;
    color: var(--text-primary);
}

.author-bio {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin: 0 0 16px 0;
    line-height: 1.5;
}

.author-social {
    display: flex;
    justify-content: center;
    gap: 16px;
}

.author-social a {
    color: var(--text-secondary);
    font-size: 1.2rem;
    transition: color 0.2s, transform 0.2s;
    border: none;
}

.author-social a:hover {
    color: var(--accent);
    transform: translateY(-2px);
}

/* Table of Contents */
.sidebar-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 16px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.sidebar-title i {
    color: var(--accent);
}

.toc-nav {
    max-height: 300px;
    overflow-y: auto;
}

.toc-nav ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.toc-nav li {
    margin: 0;
    padding: 6px 0;
    border-bottom: 1px solid var(--border);
}

.toc-nav li:last-child {
    border-bottom: none;
}

.toc-nav a {
    color: var(--text-secondary);
    font-size: 0.85rem;
    text-decoration: none;
    border: none;
    display: block;
    padding: 4px 0;
    transition: color 0.2s, padding-left 0.2s;
    line-height: 1.4;
}

.toc-nav a:hover,
.toc-nav a.active {
    color: var(--accent);
    padding-left: 8px;
}

/* Related Articles */
.related-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.related-list li {
    margin: 0;
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
}

.related-list li:last-child {
    border-bottom: none;
}

.related-list a {
    color: var(--text-secondary);
    font-size: 0.85rem;
    text-decoration: none;
    border: none;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    transition: color 0.2s;
}

.related-list a:hover {
    color: var(--accent);
}

/* Sidebar JS functionality */
.sidebar-toc-item {
    cursor: pointer;
}

.sidebar-toc-item::before {
    content: '• ';
    color: var(--text-muted);
}

.sidebar-toc-item.active::before {
    color: var(--accent);
}

/* Responsive */
@media (max-width: 1024px) {
    .post-layout {
        flex-direction: column;
        gap: 32px;
    }
    
    .post-layout .sidebar {
        width: 100%;
        position: static;
        max-height: none;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 20px;
    }
    
    .sidebar-section {
        margin-bottom: 0;
    }
}

@media (max-width: 768px) {
    .post-layout .sidebar {
        grid-template-columns: 1fr;
    }
}
'''

SIDEBAR_JS = '''
/* Sidebar: Table of Contents & Related Articles */
(function() {
    function initSidebar() {
        // Get current article's category from breadcrumb
        var breadcrumb = document.querySelector('.breadcrumb');
        if (!breadcrumb) return;
        
        var categoryLink = breadcrumb.querySelector('a[href^="/posts/"]');
        if (!categoryLink) return;
        
        var categoryHref = categoryLink.getAttribute('href');
        var categoryName = categoryLink.textContent.trim();
        
        // Generate Table of Contents
        generateTOC();
        
        // Find related articles from same category
        findRelatedArticles(categoryHref);
    }
    
    function generateTOC() {
        var content = document.querySelector('.post-content');
        if (!content) return;
        
        var tocNav = document.getElementById('toc-nav');
        if (!tocNav) return;
        
        // Find all h2 headings
        var headings = content.querySelectorAll('h2');
        if (headings.length === 0) {
            // Hide TOC section if no headings
            var tocSection = document.querySelector('.toc-section');
            if (tocSection) tocSection.style.display = 'none';
            return;
        }
        
        var ul = document.createElement('ul');
        
        headings.forEach(function(heading, index) {
            // Generate ID if not exists
            if (!heading.id) {
                heading.id = 'heading-' + index;
            }
            
            var li = document.createElement('li');
            var a = document.createElement('a');
            a.href = '#' + heading.id;
            a.textContent = heading.textContent;
            a.className = 'sidebar-toc-item';
            
            li.appendChild(a);
            ul.appendChild(li);
        });
        
        tocNav.appendChild(ul);
        
        // Highlight current section on scroll
        setupTOCScrollSpy(headings);
    }
    
    function setupTOCScrollSpy(headings) {
        var tocLinks = document.querySelectorAll('.toc-nav a');
        
        function updateActiveLink() {
            var scrollY = window.scrollY;
            var offset = 120; // Header height + some margin
            
            headings.forEach(function(heading, index) {
                var rect = heading.getBoundingClientRect();
                var top = rect.top + scrollY - offset;
                
                if (scrollY >= top && scrollY < top + rect.height) {
                    tocLinks.forEach(function(link) { link.classList.remove('active'); });
                    if (tocLinks[index]) tocLinks[index].classList.add('active');
                }
            });
        }
        
        window.addEventListener('scroll', updateActiveLink);
        updateActiveLink();
    }
    
    function findRelatedArticles(categoryHref) {
        var relatedList = document.getElementById('related-list');
        if (!relatedList) return;
        
        // Fetch category page to get article links
        fetch(categoryHref)
            .then(function(response) { return response.text(); })
            .then(function(html) {
                var parser = new DOMParser();
                var doc = parser.parseFromString(html, 'text/html');
                
                // Get article links from the category page
                var links = doc.querySelectorAll('.post-list a[href$=".html"]');
                var currentPath = window.location.pathname;
                var relatedArticles = [];
                
                links.forEach(function(link) {
                    var href = link.getAttribute('href');
                    // Skip if it's the current article or not in same category
                    if (href === currentPath || href.indexOf('/posts/ai-tools/claude-code') !== -1) return;
                    if (href.indexOf('/posts/') === -1) return;
                    
                    // Get the article title
                    var title = link.textContent.trim();
                    if (title && relatedArticles.length < 4) {
                        // Normalize href to absolute URL
                        var absoluteHref = new URL(href, window.location.origin).pathname;
                        relatedArticles.push({
                            title: title,
                            href: absoluteHref
                        });
                    }
                });
                
                // Display related articles
                if (relatedArticles.length > 0) {
                    relatedArticles.forEach(function(article) {
                        var li = document.createElement('li');
                        var a = document.createElement('a');
                        a.href = article.href;
                        a.textContent = article.title;
                        li.appendChild(a);
                        relatedList.appendChild(li);
                    });
                } else {
                    // Hide related section if no articles found
                    var relatedSection = document.querySelector('.related-section');
                    if (relatedSection) relatedSection.style.display = 'none';
                }
            })
            .catch(function() {
                // Hide related section on error
                var relatedSection = document.querySelector('.related-section');
                if (relatedSection) relatedSection.style.display = 'none';
            });
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSidebar);
    } else {
        initSidebar();
    }
})();
'''

def add_sidebar_to_article(html_content):
    """Add sidebar to an article page."""
    # Check if it's an article page (has .post-content)
    if 'class="post-content"' not in html_content and 'class=\'post-content\'' not in html_content:
        return html_content, False
    
    # Check if sidebar already exists
    if 'class="sidebar"' in html_content:
        return html_content, False
    
    # Add sidebar styles before </head>
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', '<style>' + SIDEBAR_STYLES + '</style>\n</head>')
    
    # Wrap article content in post-layout div
    # Find the article element and wrap it
    if '<article class="post">' in html_content:
        # Replace <article class="post"> with <div class="post-layout"><article class="post">
        html_content = html_content.replace('<article class="post">', '<div class="post-layout"><article class="post">')
        # Add sidebar and close div before </article> closing
        # Find the </article> tag and add sidebar before it
        html_content = html_content.replace('</article>', SIDEBAR_HTML + '\n        </article>\n    </div>')
    elif "<article class='post'>" in html_content:
        html_content = html_content.replace("<article class='post'>", "<article class='post'>")
        html_content = html_content.replace('</article>', SIDEBAR_HTML + '\n        </article>\n    </div>')
    
    # Add sidebar JS before </body>
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', '<script>' + SIDEBAR_JS + '</script>\n</body>')
    
    return html_content, True

def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, added = add_sidebar_to_article(content)
    
    if added:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    base_dir = '/Users/halo/.qclaw/workspace/blog-repo'
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['scripts', 'images', 'stylesheets', 'javascripts', 'blog']]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Found {len(html_files)} HTML files")
    
    # Process all files
    updated = 0
    for filepath in html_files:
        try:
            if process_file(filepath):
                rel_path = os.path.relpath(filepath, base_dir)
                print(f"  Added sidebar: {rel_path}")
                updated += 1
        except Exception as e:
            print(f"  Error processing {filepath}: {e}")
    
    print(f"\nDone! Updated {updated} files.")

if __name__ == '__main__':
    main()
