#!/usr/bin/env python3
"""
Add floating TOC feature to article pages.
This creates a floating button that reveals a mini TOC when clicked.
"""

import os
import re

# Floating TOC HTML and styles
FLOATING_TOC_STYLES = '''
/* Floating TOC */
.floating-toc-btn {
    position: fixed;
    bottom: 32px;
    right: 32px;
    width: 48px;
    height: 48px;
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    z-index: 1000;
    transition: transform 0.2s, box-shadow 0.2s;
    opacity: 0;
    pointer-events: none;
}

.floating-toc-btn.visible {
    opacity: 1;
    pointer-events: auto;
}

.floating-toc-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

.floating-toc-btn i {
    transition: transform 0.2s;
}

.floating-toc-btn.active i {
    transform: rotate(45deg);
}

.floating-toc-panel {
    position: fixed;
    bottom: 90px;
    right: 32px;
    width: 300px;
    max-height: 400px;
    background: var(--bg-primary);
    border: 1px solid var(--border);
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    z-index: 1000;
    display: none;
    flex-direction: column;
    overflow: hidden;
}

.floating-toc-panel.open {
    display: flex;
}

.floating-toc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    border-bottom: 1px solid var(--border);
    background: var(--bg-secondary);
}

.floating-toc-header h4 {
    margin: 0;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
}

.floating-toc-close {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px;
    font-size: 1rem;
    line-height: 1;
    transition: color 0.2s;
}

.floating-toc-close:hover {
    color: var(--text-primary);
}

.floating-toc-content {
    flex: 1;
    overflow-y: auto;
    padding: 12px 16px;
}

.floating-toc-content ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.floating-toc-content li {
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
}

.floating-toc-content li:last-child {
    border-bottom: none;
}

.floating-toc-content a {
    color: var(--text-secondary);
    font-size: 0.85rem;
    text-decoration: none;
    border: none;
    line-height: 1.4;
    display: block;
    transition: color 0.2s, padding-left 0.2s;
}

.floating-toc-content a:hover,
.floating-toc-content a.active {
    color: var(--accent);
    padding-left: 8px;
}

@media (max-width: 768px) {
    .floating-toc-btn {
        bottom: 20px;
        right: 20px;
        width: 44px;
        height: 44px;
    }
    
    .floating-toc-panel {
        bottom: 76px;
        right: 12px;
        left: 12px;
        width: auto;
    }
}
'''

FLOATING_TOC_HTML = '''
<!-- Floating TOC Button -->
<button class="floating-toc-btn" id="floatingTocBtn" title="目录导航">
    <i class="fas fa-list-ul"></i>
</button>

<!-- Floating TOC Panel -->
<div class="floating-toc-panel" id="floatingTocPanel">
    <div class="floating-toc-header">
        <h4><i class="fas fa-list-ul"></i> 目录</h4>
        <button class="floating-toc-close" id="floatingTocClose">&times;</button>
    </div>
    <div class="floating-toc-content" id="floatingTocContent">
        <!-- TOC will be populated by JS -->
    </div>
</div>
'''

FLOATING_TOC_JS = '''
/* Floating TOC Feature */
(function() {
    var floatingBtn = document.getElementById('floatingTocBtn');
    var floatingPanel = document.getElementById('floatingTocPanel');
    var floatingClose = document.getElementById('floatingTocClose');
    var floatingContent = document.getElementById('floatingTocContent');
    var tocNav = document.getElementById('toc-nav');
    var sidebar = document.querySelector('.sidebar');
    
    if (!floatingBtn || !floatingPanel || !floatingContent) return;
    
    // Only show if there's a TOC in the sidebar
    var sidebarToc = document.querySelector('.toc-section');
    if (!sidebarToc) return;
    
    // Copy TOC content to floating panel
    function syncTocToFloating() {
        if (tocNav && tocNav.innerHTML) {
            floatingContent.innerHTML = tocNav.innerHTML;
            
            // Add click handlers to floating TOC links
            floatingContent.querySelectorAll('a').forEach(function(link) {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    var targetId = link.getAttribute('href').substring(1);
                    var target = document.getElementById(targetId);
                    if (target) {
                        var headerOffset = 100;
                        var elementPosition = target.getBoundingClientRect().top;
                        var offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                        window.scrollTo({
                            top: offsetPosition,
                            behavior: 'smooth'
                        });
                        // Close panel after click
                        floatingPanel.classList.remove('open');
                        floatingBtn.classList.remove('active');
                    }
                });
            });
        }
    }
    
    syncTocToFloating();
    
    // Toggle floating panel
    floatingBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        floatingPanel.classList.toggle('open');
        floatingBtn.classList.toggle('active');
    });
    
    // Close button
    floatingClose.addEventListener('click', function(e) {
        e.stopPropagation();
        floatingPanel.classList.remove('open');
        floatingBtn.classList.remove('active');
    });
    
    // Click outside to close
    document.addEventListener('click', function(e) {
        if (!floatingPanel.contains(e.target) && !floatingBtn.contains(e.target)) {
            floatingPanel.classList.remove('open');
            floatingBtn.classList.remove('active');
        }
    });
    
    // Show/hide floating button based on scroll and sidebar visibility
    var tocSection = document.querySelector('.toc-section');
    var floatingBtnShown = false;
    
    function updateFloatingBtnVisibility() {
        if (!tocSection) return;
        
        var tocRect = tocSection.getBoundingClientRect();
        var windowHeight = window.innerHeight;
        
        // Show floating button when TOC section is out of viewport (scrolled past)
        if (tocRect.bottom < 0 || tocRect.top > windowHeight) {
            floatingBtn.classList.add('visible');
            floatingBtnShown = true;
        } else {
            // Hide when sidebar TOC is visible
            if (floatingBtnShown) {
                floatingBtn.classList.remove('visible');
                floatingBtnShown = false;
            }
        }
    }
    
    window.addEventListener('scroll', updateFloatingBtnVisibility);
    updateFloatingBtnVisibility();
    
    // Highlight current section in floating TOC
    function highlightCurrentInFloating() {
        var headings = document.querySelectorAll('.post-content h2');
        var floatingLinks = floatingContent.querySelectorAll('a');
        
        if (headings.length === 0 || floatingLinks.length === 0) return;
        
        var scrollY = window.scrollY;
        var offset = 120;
        
        headings.forEach(function(heading, index) {
            var rect = heading.getBoundingClientRect();
            var top = rect.top + scrollY - offset;
            
            if (scrollY >= top && scrollY < top + rect.height) {
                floatingLinks.forEach(function(link) { link.classList.remove('active'); });
                if (floatingLinks[index]) floatingLinks[index].classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', highlightCurrentInFloating);
    highlightCurrentInFloating();
})();
'''

def add_floating_toc(html_content):
    """Add floating TOC feature to an article page."""
    # Check if it's an article page (has sidebar)
    if 'class="sidebar"' not in html_content:
        return html_content, False
    
    # Check if floating TOC already exists
    if 'class="floating-toc-btn"' in html_content:
        return html_content, False
    
    # Add floating TOC styles before </head>
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', '<style>' + FLOATING_TOC_STYLES + '</style>\n</head>')
    
    # Add floating TOC HTML before the sidebar
    # Find the sidebar and insert before it
    if '<aside class="sidebar">' in html_content:
        html_content = html_content.replace('<aside class="sidebar">', FLOATING_TOC_HTML + '\n        <aside class="sidebar">')
    
    # Add floating TOC JS before </body>
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', '<script>' + FLOATING_TOC_JS + '</script>\n</body>')
    
    return html_content, True

def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, added = add_floating_toc(content)
    
    if added:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    base_dir = '/Users/halo/.qclaw/workspace/blog-repo'
    
    # Find all HTML files with sidebar
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
                print(f"  Added floating TOC: {rel_path}")
                updated += 1
        except Exception as e:
            print(f"  Error processing {filepath}: {e}")
    
    print(f"\nDone! Updated {updated} files.")

if __name__ == '__main__':
    main()
