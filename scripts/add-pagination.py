#!/usr/bin/env python3
"""
Add pagination to category pages with many articles.
Uses client-side JavaScript for simple page navigation.
"""

import os
import re

PAGINATION_STYLES = '''
/* Pagination */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    margin: 48px 0 32px 0;
    padding: 24px 0;
    border-top: 1px solid var(--border);
}

.pagination-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 40px;
    height: 40px;
    padding: 0 12px;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text-secondary);
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;
}

.pagination-btn:hover:not(:disabled) {
    background: var(--accent);
    border-color: var(--accent);
    color: white;
}

.pagination-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.pagination-btn.active {
    background: var(--accent);
    border-color: var(--accent);
    color: white;
}

.pagination-btn i {
    font-size: 0.8rem;
}

.pagination-info {
    margin-left: 16px;
    font-size: 0.85rem;
    color: var(--text-muted);
}

.post-list.hidden {
    display: none;
}

@media (max-width: 768px) {
    .pagination {
        flex-wrap: wrap;
    }
    
    .pagination-info {
        width: 100%;
        text-align: center;
        margin: 12px 0 0 0;
    }
}
'''

PAGINATION_HTML = '''
<!-- Pagination -->
<div class="pagination" id="pagination">
    <button class="pagination-btn" id="prevBtn" disabled>
        <i class="fas fa-chevron-left"></i> 上一页
    </button>
    <div id="pageNumbers"></div>
    <button class="pagination-btn" id="nextBtn">
        下一页 <i class="fas fa-chevron-right"></i>
    </button>
    <span class="pagination-info" id="paginationInfo"></span>
</div>
'''

PAGINATION_JS = '''
/* Category Page Pagination */
(function() {
    var ARTICLES_PER_PAGE = 15;
    
    var postList = document.querySelector('.post-list');
    var pagination = document.getElementById('pagination');
    var prevBtn = document.getElementById('prevBtn');
    var nextBtn = document.getElementById('nextBtn');
    var pageNumbers = document.getElementById('pageNumbers');
    var paginationInfo = document.getElementById('paginationInfo');
    
    if (!postList || !pagination) return;
    
    var articles = postList.querySelectorAll('li');
    var totalArticles = articles.length;
    
    // Only paginate if more than ARTICLES_PER_PAGE articles
    if (totalArticles <= ARTICLES_PER_PAGE) return;
    
    var totalPages = Math.ceil(totalArticles / ARTICLES_PER_PAGE);
    
    // Get current page from URL hash or default to 1
    var currentPage = 1;
    var hash = window.location.hash;
    if (hash && hash.indexOf('page-') === 1) {
        var page = parseInt(hash.replace('#page-', ''));
        if (page >= 1 && page <= totalPages) {
            currentPage = page;
        }
    }
    
    function showPage(page) {
        currentPage = page;
        
        // Update URL hash
        if (page === 1) {
            history.replaceState(null, '', window.location.pathname);
        } else {
            history.replaceState(null, '', '#page-' + page);
        }
        
        // Show/hide articles
        var start = (page - 1) * ARTICLES_PER_PAGE;
        var end = start + ARTICLES_PER_PAGE;
        
        articles.forEach(function(article, index) {
            if (index >= start && index < end) {
                article.style.display = '';
            } else {
                article.style.display = 'none';
            }
        });
        
        // Update pagination buttons
        prevBtn.disabled = currentPage === 1;
        nextBtn.disabled = currentPage === totalPages;
        
        // Update page numbers
        updatePageNumbers();
        
        // Update info text
        paginationInfo.textContent = '第 ' + currentPage + ' / ' + totalPages + ' 页，共 ' + totalArticles + ' 篇文章';
        
        // Scroll to top of post list
        var listTop = postList.getBoundingClientRect().top + window.scrollY - 80;
        window.scrollTo({ top: listTop, behavior: 'smooth' });
    }
    
    function updatePageNumbers() {
        pageNumbers.innerHTML = '';
        
        var maxVisible = 5;
        var startPage, endPage;
        
        if (totalPages <= maxVisible) {
            startPage = 1;
            endPage = totalPages;
        } else {
            if (currentPage <= 3) {
                startPage = 1;
                endPage = maxVisible;
            } else if (currentPage >= totalPages - 2) {
                startPage = totalPages - maxVisible + 1;
                endPage = totalPages;
            } else {
                startPage = currentPage - 2;
                endPage = currentPage + 2;
            }
        }
        
        // Add first page + ellipsis if needed
        if (startPage > 1) {
            var firstBtn = document.createElement('button');
            firstBtn.className = 'pagination-btn';
            firstBtn.textContent = '1';
            firstBtn.onclick = function() { showPage(1); };
            pageNumbers.appendChild(firstBtn);
            
            if (startPage > 2) {
                var ellipsis = document.createElement('span');
                ellipsis.style.padding = '0 8px';
                ellipsis.textContent = '...';
                pageNumbers.appendChild(ellipsis);
            }
        }
        
        // Add page buttons
        for (var i = startPage; i <= endPage; i++) {
            var btn = document.createElement('button');
            btn.className = 'pagination-btn' + (i === currentPage ? ' active' : '');
            btn.textContent = i;
            btn.onclick = (function(page) {
                return function() { showPage(page); };
            })(i);
            pageNumbers.appendChild(btn);
        }
        
        // Add last page + ellipsis if needed
        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                var ellipsis = document.createElement('span');
                ellipsis.style.padding = '0 8px';
                ellipsis.textContent = '...';
                pageNumbers.appendChild(ellipsis);
            }
            
            var lastBtn = document.createElement('button');
            lastBtn.className = 'pagination-btn';
            lastBtn.textContent = totalPages;
            lastBtn.onclick = function() { showPage(totalPages); };
            pageNumbers.appendChild(lastBtn);
        }
    }
    
    // Event listeners
    prevBtn.onclick = function() {
        if (currentPage > 1) showPage(currentPage - 1);
    };
    
    nextBtn.onclick = function() {
        if (currentPage < totalPages) showPage(currentPage + 1);
    };
    
    // Handle browser back/forward
    window.addEventListener('hashchange', function() {
        var hash = window.location.hash;
        if (hash && hash.indexOf('page-') === 1) {
            var page = parseInt(hash.replace('#page-', ''));
            if (page >= 1 && page <= totalPages) {
                showPage(page);
            }
        } else {
            showPage(1);
        }
    });
    
    // Initialize
    showPage(currentPage);
})();
'''

def add_pagination(html_content):
    """Add pagination to a category page."""
    # Check if it's a category page (has .post-list)
    if 'class="post-list"' not in html_content:
        return html_content, False
    
    # Check if pagination already exists
    if 'class="pagination"' in html_content:
        return html_content, False
    
    # Count articles
    article_count = html_content.count('<li><a href=')
    if article_count <= 15:
        return html_content, False
    
    # Add pagination styles before </head>
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', '<style>' + PAGINATION_STYLES + '</style>\n</head>')
    
    # Add pagination HTML after </ul> (closing the post-list)
    # Find the closing </ul> of post-list and insert pagination after it
    post_list_match = re.search(r'(<ul class="post-list">.*?</ul>)', html_content, re.DOTALL)
    if post_list_match:
        original_ul = post_list_match.group(1)
        modified_ul = original_ul + '\n' + PAGINATION_HTML
        html_content = html_content.replace(original_ul, modified_ul)
    
    # Add pagination JS before </body>
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', '<script>' + PAGINATION_JS + '</script>\n</body>')
    
    return html_content, True

def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, added = add_pagination(content)
    
    if added:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    base_dir = '/Users/halo/.qclaw/workspace/blog-repo'
    
    # Find all category index files (index.html in subdirectories)
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['scripts', 'images', 'stylesheets', 'javascripts', 'blog']]
        for file in files:
            if file == 'index.html':
                html_files.append(os.path.join(root, file))
    
    print(f"Found {len(html_files)} category/index files")
    
    # Process all files
    updated = 0
    for filepath in html_files:
        try:
            if process_file(filepath):
                rel_path = os.path.relpath(filepath, base_dir)
                print(f"  Added pagination: {rel_path}")
                updated += 1
        except Exception as e:
            print(f"  Error processing {filepath}: {e}")
    
    print(f"\nDone! Updated {updated} files.")

if __name__ == '__main__':
    main()
