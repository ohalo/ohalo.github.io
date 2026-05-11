#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from pathlib import Path

p = Path('index.html')
content = p.read_text(encoding='utf-8')

print("=== Fixing index.html ===")

# 1. Give the articles <ul> an ID so JS can target it correctly
# Find: <h2><i class="fas fa-fire"></i> 最新文章</h2> followed by <ul class="post-list">
old = '<h2><i class="fas fa-fire"></i> 最新文章</h2>\n            <ul class="post-list">'
new = '<h2><i class="fas fa-fire"></i> 最新文章</h2>\n            <ul class="post-list" id="homeArticleList">'
if old in content:
    content = content.replace(old, new)
    print("[1] Added id=homeArticleList to articles list")
else:
    print("[1] WARNING: Could not find articles list to add ID")

# 2. Remove the OLD pagination div that's between the two post-lists
# The pagination div should only appear on category pages, not homepage
# Find and remove: <!-- Pagination --> ... </div> (the one inside <section id="main_content">)
# Actually, let's just disable the pagination on homepage by removing the pagination HTML
pagination_start = content.find('<div class="pagination" id="pagination">')
if pagination_start != -1:
    # Find the matching end </div> by counting depth
    temp = content[pagination_start:]
    depth = 0
    in_div = False
    end_pos = 0
    i = 0
    while i < len(temp):
        if temp[i:i+4] == '<div':
            # Check it's actually a <div> tag
            j = i + 4
            while j < len(temp) and temp[j] not in (' ', '>', '\n', '\r', '\t'):
                j += 1
            if j < len(temp) and temp[j] in (' ', '>'):
                depth += 1
                in_div = True
        elif temp[i:i+6] == '</div>':
            depth -= 1
            if in_div and depth == 0:
                end_pos = i + 6
                break
        i += 1
    
    if end_pos > 0:
        old_pagination = temp[:end_pos]
        content = content[:pagination_start] + '\n            ' + content[pagination_start + end_pos:]
        print(f"[2] Removed old pagination div (was at position {pagination_start})")
    else:
        print("[2] WARNING: Could not find end of pagination div")
else:
    print("[2] No pagination div found (might already be removed)")

# 3. Remove the "Category Page Pagination" JavaScript that doesn't work on homepage
# This JS tries to paginate .post-list which is wrong on homepage
pattern = r'\n<script>\n/\* Category Page Pagination \*/.*?</script>\n'
match = re.search(pattern, content, re.DOTALL)
if match:
    content = content[:match.start()] + '\n<script>\n/* Pagination removed: homepage has < 15 articles */\n</script>\n' + content[match.end():]
    print("[3] Removed Category Page Pagination JS")
else:
    print("[3] WARNING: Could not find Category Page Pagination JS")

# 4. Fix CATEGORY_TAGS dirty data: {"name": ".", "count": 1, "url": "/./"}
# Remove this entry
old_tags = '{"name": ".", "count": 1, "url": "/./"}, '
if old_tags in content:
    content = content.replace(old_tags, '')
    print("[4] Removed dirty tag: {name: \".\", url: \"/./\"}")

# Also check for other suspicious tags
ct_start = content.find('window.CATEGORY_TAGS = [')
if ct_start != -1:
    ct_end = content.find('];', ct_start) + 2
    tags_str = content[ct_start:ct_end]
    # Check for URLs starting with "/." (suspicious)
    if '"/.' in tags_str or ', {' in tags_str:
        print("[4] WARNING: CATEGORY_TAGS may still have issues, check manually")

# 5. Stats bar: update article count (156 -> actual count)
# Count articles in ALL_ARTICLES
aa_start = content.find('window.ALL_ARTICLES = [')
if aa_start != -1:
    aa_end = content.find('];', aa_start) + 2
    aa_json_str = content[aa_start:aa_end]
    # Count entries
    import json
    try:
        # Fix trailing commas for JSON parsing
        aa_json_str_fixed = re.sub(r',\s*]', ']', aa_json_str[aa_json_str.find('['):])
        articles = json.loads(aa_json_str_fixed)
        actual_count = len(articles)
        print(f"[5] Article count: {actual_count}")
        
        # Update stats bar
        old_stats = f'<span class="stat-value">156</span>'
        new_stats = f'<span class="stat-value">{actual_count}</span>'
        content = content.replace(old_stats, new_stats)
        print(f"[5] Updated stats bar: 156 -> {actual_count}")
    except Exception as e:
        print(f"[5] Could not parse ALL_ARTICLES: {e}")

# Write back
p.write_text(content, encoding='utf-8')
print("\n=== Done! index.html fixed ===")
