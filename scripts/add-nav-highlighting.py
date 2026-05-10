#!/usr/bin/env python3
"""
Batch add navigation highlighting script to HTML pages.
"""

import os
import re

NAV_SCRIPT = '''
    <!-- Navigation Active State -->
    <script>
    (function() {
        var path = window.location.pathname;
        var navLinks = document.querySelectorAll('nav ul li a');
        navLinks.forEach(function(link) {
            var href = link.getAttribute('href');
            if (href === '/' && (path === '/' || path === '/index.html')) {
                link.classList.add('active');
            } else if (href !== '/' && href !== '/posts/archive/' && href !== '/about/' && path.startsWith(href)) {
                link.classList.add('active');
            } else if ((href === '/posts/archive/' && path === '/posts/archive/') || (href === '/about/' && path === '/about/')) {
                link.classList.add('active');
            }
        });
    })();
    </script>
'''

def add_nav_script(html_content, filepath):
    """Add navigation highlighting script before </body> if not already present."""
    # Skip if already has nav script
    if 'Navigation Active State' in html_content or 'navLinks.forEach' in html_content:
        return html_content, False  # Already has a similar script
    
    # Insert before </body>
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', NAV_SCRIPT + '\n</body>')
        return html_content, True
    return html_content, False

def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, added = add_nav_script(content, filepath)
    
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
        # Skip .git and other hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Found {len(html_files)} HTML files")
    
    # Process all files
    updated = 0
    for filepath in html_files:
        if process_file(filepath):
            rel_path = os.path.relpath(filepath, base_dir)
            print(f"  Added nav script: {rel_path}")
            updated += 1
    
    print(f"\nDone! Updated {updated} files.")

if __name__ == '__main__':
    main()
