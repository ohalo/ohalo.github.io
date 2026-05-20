#!/usr/bin/env python3
"""
Fix article template for new articles.
Adds missing components: article.css, post-layout structure, sidebar, TOC, giscus comments.
"""

import os
import re
from pathlib import Path

# Article template components
ARTICLE_CSS_LINK = '    <link rel="stylesheet" href="/stylesheets/article.css">'

GISCUS_SCRIPT = '''<script src="https://giscus.app/client.js"
        data-repo="ohalo/ohalo.github.io"
        data-repo-id="R_kgDOOG0HsQ"
        data-category="Comments"
        data-category-id="DIC_kwDOOG0Hsc4Ckvhg"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="preferred_color_scheme"
        data-lang="zh-CN"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>'''

SIDEBAR_JS_LINK = '    <script src="/javascripts/sidebar.js"></script>'

def fix_article(filepath):
    """Fix a single article file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already fixed
    if 'article.css' in content and 'sidebar.js' in content:
        return False, "Already fixed"
    
    # Fix 1: Add article.css after modern-theme.css
    if 'modern-theme.css' in content and 'article.css' not in content:
        content = content.replace(
            '<link rel="stylesheet" type="text/css" href="/stylesheets/modern-theme.css" media="screen">',
            '<link rel="stylesheet" type="text/css" href="/stylesheets/modern-theme.css" media="screen">\n' + ARTICLE_CSS_LINK
        )
    
    # Fix 2: Add post-layout wrapper and sidebar placeholder
    # Check if article has proper structure
    if '<article>' in content and 'post-layout' not in content:
        # Wrap article in post-layout
        content = content.replace('<article>', '<div class="post-layout"><article class="post">')
        # Add sidebar placeholder before closing article
        if '</article>' in content:
            content = content.replace('</article>', '</article>\n    <div id="sidebar-placeholder"></div>\n    </div>')
    
    # Fix 3: Add giscus before </main> or </body>
    if 'giscus.app' not in content:
        if '</main>' in content:
            content = content.replace('</main>', GISCUS_SCRIPT + '\n</main>')
        elif '</body>' in content:
            content = content.replace('</body>', GISCUS_SCRIPT + '\n</body>')
    
    # Fix 4: Add sidebar.js before </body>
    if 'sidebar.js' not in content:
        if '</body>' in content:
            content = content.replace('</body>', SIDEBAR_JS_LINK + '\n</body>')
    
    # Fix 5: Add header placeholder if missing
    if 'header-placeholder' not in content and '<header>' in content:
        # Already has inline header, skip
        pass
    elif 'header-placeholder' not in content:
        # Add header placeholder after <body>
        content = content.replace('<body>', '<body>\n    <div id="header-placeholder"></div>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True, "Fixed"


def main():
    posts_dir = Path('posts')
    fixed_count = 0
    error_count = 0
    
    for html_file in posts_dir.rglob('*.html'):
        # Skip index files
        if html_file.name == 'index.html':
            continue
        
        try:
            fixed, msg = fix_article(html_file)
            if fixed:
                print(f"[FIXED] {html_file}")
                fixed_count += 1
        except Exception as e:
            print(f"[ERROR] {html_file}: {e}")
            error_count += 1
    
    print(f"\n{'='*50}")
    print(f"Fixed: {fixed_count} files")
    print(f"Errors: {error_count} files")


if __name__ == '__main__':
    main()
