#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import json
import sys
from pathlib import Path

def log(msg):
    print(msg.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))

log("=== 全站扫描和修复 ===\n")

repo = Path('.')
html_files = list(repo.rglob('*.html'))
log(f"找到 {len(html_files)} 个 HTML 文件\n")

# ============================================================
# 1. 修复首页 index.html
# ============================================================
log("--- [1/5] 修复首页 index.html ---")

p = repo / 'index.html'
if p.exists():
    content = p.read_text(encoding='utf-8')
    
    # 1a. 给文章列表添加 ID
    old = '<h2><i class="fas fa-fire"></i> 最新文章</h2>\n            <ul class="post-list">'
    new = '<h2><i class="fas fa-fire"></i> 最新文章</h2>\n            <ul class="post-list" id="homeArticleList">'
    if old in content:
        content = content.replace(old, new)
        log("[1a] 已给文章列表添加 id=homeArticleList")
    
    # 1b. 删除错误的 pagination div
    ps = content.find('<div class="pagination" id="pagination">')
    if ps != -1:
        temp = content[ps:]
        depth = 0
        in_div = False
        end_pos = 0
        i = 0
        while i < len(temp):
            if i+4 < len(temp) and temp[i:i+4] == '<div' and temp[i+4] in (' ', '>', '\n', '\r', '\t'):
                depth += 1
                in_div = True
            elif i+6 < len(temp) and temp[i:i+6] == '</div>':
                depth -= 1
                if in_div and depth == 0:
                    end_pos = i + 6
                    break
            i += 1
        if end_pos > 0:
            content = content[:ps] + '\n            ' + content[ps + end_pos:]
            log("[1b] 已删除错误的 pagination div")
    
    # 1c. 删除 Category Page Pagination JS
    pat = r'\n<script>\n/\* Category Page Pagination \*/.*?</script>\n'
    m = re.search(pat, content, re.DOTALL)
    if m:
        content = content[:m.start()] + '\n<script>\n/* Pagination removed for homepage */\n</script>\n' + content[m.end():]
        log("[1c] 已删除 Category Page Pagination JS")
    
    # 1d. 修复 CATEGORY_TAGS 脏数据
    old_tags = '{"name": ".", "count": 1, "url": "/./"}, '
    if old_tags in content:
        content = content.replace(old_tags, '')
        log("[1d] 已删除 CATEGORY_TAGS 脏数据")
    
    # 1e. 更新文章统计
    aa_start = content.find('window.ALL_ARTICLES = [')
    if aa_start != -1:
        aa_end = content.find('];', aa_start) + 2
        aa_json_str = content[aa_start + len('window.ALL_ARTICLES = '):aa_end-1]
        try:
            articles = json.loads(aa_json_str)
            actual = len(articles)
            log(f"[1e] 文章总数: {actual}")
            content = content.replace('<span class="stat-value">156</span>', f'<span class="stat-value">{actual}</span>')
            log(f"[1e] 已更新统计: 156 -> {actual}")
        except Exception as e:
            log(f"[1e] 无法解析 ALL_ARTICLES: {e}")
    
    p.write_text(content, encoding='utf-8')
    log("首页修复完成\n")
else:
    log("WARNING: index.html 不存在\n")

# ============================================================
# 2. 检查所有分类页的 pagination JS 是否正确
# ============================================================
log("--- [2/5] 检查分类页 pagination JS ---")
for html_file in html_files:
    if 'index.html' in str(html_file):
        continue
    content = html_file.read_text(encoding='utf-8', errors='ignore')
    if 'Category Page Pagination' in content:
        # 检查是否选中了正确的 .post-list
        if 'querySelector(\'.post-list\')' in content:
            log(f"  [问题] {html_file}: JS 可能选中错误的 .post-list")
log("分类页检查完成\n")

# ============================================================
# 3. 检查所有页面的 CSS 变量语法
# ============================================================
log("--- [3/5] 检查 CSS 变量语法 ---")
for html_file in html_files:
    content = html_file.read_text(encoding='utf-8', errors='ignore')
    # 检查 var() 语法
    vars_found = re.findall(r'var\([^)]*\)', content)
    for v in vars_found:
        if 'var(--' in v and ')' in v:
            pass  # 正确
        elif 'var(' in v and '--' not in v:
            log(f"  [CSS错误] {html_file}: {v}")
log("CSS 检查完成\n")

# ============================================================
# 4. 检查所有页面的 JS 错误（Console 可检测）
# ============================================================
log("--- [4/5] 检查 JS 语法问题 ---")
for html_file in html_files:
    content = html_file.read_text(encoding='utf-8', errors='ignore')
    # 检查未闭合的字符串
    script_start = content.find('<script>')
    while script_start != -1:
        script_end = content.find('</script>', script_start)
        if script_end == -1:
            log(f"  [JS错误] {html_file}: 未闭合的 <script> 标签")
            break
        script_content = content[script_start + 8:script_end]
        # 检查引号不匹配
        single = script_content.count("'")
        double = script_content.count('"')
        # 简单检查（不完美）
        if single % 2 != 0:
            log(f"  [JS警告] {html_file}: 单引号可能不匹配")
        if double % 2 != 0:
            log(f"  [JS警告] {html_file}: 双引号可能不匹配")
        script_start = content.find('<script>', script_end)
log("JS 检查完成\n")

# ============================================================
# 5. 汇总
# ============================================================
log("=== 全站扫描完成 ===")
log("请检查上述输出，然后手动修复或告诉我需要自动修复哪些问题。")
log("\n下一步: git add -A && git commit -m 'fix: 全站修复' && git push")
