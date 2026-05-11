// Sidebar Component Generator
// Generates the sidebar with author card, TOC, related articles, and tags sections

(function() {
    'use strict';

    // Author configuration - change here to update all pages
    var AUTHOR_CONFIG = {
        name: 'halo',
        avatar: 'https://avatars.githubusercontent.com/u/2868547?v=4',
        bio: '40岁创业者，探索AI时代的工作方式',
        github: 'https://github.com/ohalo',
        zhihu: 'https://www.zhihu.com/'
    };

    // Category tags configuration - change here to update all pages
    var CATEGORY_TAGS = [
        { name: '读书', count: 1, url: '/posts/reading/' },
        { name: '书评', count: 4, url: '/posts/reading/book-review/' },
        { name: '职业发展', count: 8, url: '/posts/career/' },
        { name: '硬件数码', count: 5, url: '/posts/hardware/' },
        { name: 'NAS', count: 41, url: '/posts/hardware/nas/' },
        { name: '其他硬件', count: 12, url: '/posts/hardware/others/' },
        { name: 'GPU对比', count: 1, url: '/posts/hardware/gpu-5070-9070-comparison/' },
        { name: '投资理财', count: 1, url: '/posts/investment/' },
        { name: '股票分析', count: 2, url: '/posts/investment/stock-analysis/' },
        { name: '独立开发飞轮', count: 1, url: '/posts/ai-observation/indie-app-flywheel/' },
        { name: 'AI与职业', count: 7, url: '/posts/ai-observation/career/' },
        { name: 'AI社会观察', count: 12, url: '/posts/ai-observation/society/' },
        { name: 'AI行业观察', count: 4, url: '/posts/ai-observation/industry/' },
        { name: '技术技巧', count: 4, url: '/posts/tech-tips/' },
        { name: '安全技巧', count: 1, url: '/posts/tech-tips/security/' },
        { name: '软件使用', count: 2, url: '/posts/tech-tips/software/' },
        { name: '生活方式', count: 5, url: '/posts/life/' },
        { name: 'AI工具', count: 3, url: '/posts/ai-tools/' },
        { name: 'Claude Code', count: 12, url: '/posts/ai-tools/claude-code/' },
        { name: 'OpenClaw', count: 19, url: '/posts/ai-tools/openclaw/' },
        { name: 'AI技能训练', count: 1, url: '/posts/ai-tools/skill-training/' },
        { name: 'AI工具其他', count: 9, url: '/posts/ai-tools/others/' },
        { name: 'AI工作流', count: 1, url: '/posts/ai-tools/workflow/' },
        { name: 'Spec Kit', count: 1, url: '/posts/ai-tools/spec-kit/' },
        { name: 'HAFW', count: 2, url: '/posts/ai-tools/hafw/' },
        { name: 'ai-tools / openspec', count: 1, url: '/posts/ai-tools/openspec/' }
    ];

    // Generate author card HTML
    function generateAuthorCard() {
        return '<div class="sidebar-section author-card">\n' +
               '    <img src="' + AUTHOR_CONFIG.avatar + '" alt="' + AUTHOR_CONFIG.name + '" class="author-avatar">\n' +
               '    <h3 class="author-name">' + AUTHOR_CONFIG.name + '</h3>\n' +
               '    <p class="author-bio">' + AUTHOR_CONFIG.bio + '</p>\n' +
               '    <div class="author-social">\n' +
               '        <a href="' + AUTHOR_CONFIG.github + '" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>\n' +
               '        <a href="' + AUTHOR_CONFIG.zhihu + '" target="_blank" title="知乎"><i class="fab fa-zhihu"></i></a>\n' +
               '    </div>\n' +
               '</div>';
    }

    // Generate TOC from article headings
    function generateTocFromHeadings() {
        var article = document.querySelector('article');
        if (!article) return '';
        
        var headings = article.querySelectorAll('h2, h3');
        if (headings.length === 0) return '';
        
        var tocHtml = '<ul class="toc-list">';
        headings.forEach(function(heading, index) {
            // Create anchor if not exists
            if (!heading.id) {
                heading.id = 'section-' + index;
            }
            var level = heading.tagName === 'H2' ? 'toc-h2' : 'toc-h3';
            tocHtml += '<li class="' + level + '"><a href="#' + heading.id + '">' + heading.textContent + '</a></li>';
        });
        tocHtml += '</ul>';
        return tocHtml;
    }

    // Generate TOC section HTML
    function generateTocSection() {
        var tocContent = generateTocFromHeadings();
        if (!tocContent) {
            return ''; // Don't show TOC if no headings
        }
        return '<div class="sidebar-section toc-section">\n' +
               '    <h3 class="sidebar-title"><i class="fas fa-list-ul"></i> 目录</h3>\n' +
               '    <nav id="toc-nav" class="toc-nav">' + tocContent + '</nav>\n' +
               '</div>';
    }

    // Get current page category from URL
    function getCurrentCategory() {
        var path = window.location.pathname;
        // Extract category from /posts/category/subcategory/article.html
        var match = path.match(/\/posts\/([^\/]+)(?:\/([^\/]+))?\//);
        if (match) {
            return {
                main: match[1],
                sub: match[2] || null
            };
        }
        return null;
    }

    // Find related articles from ALL_ARTICLES if available
    function findRelatedArticles() {
        if (typeof ALL_ARTICLES === 'undefined' || !Array.isArray(ALL_ARTICLES)) {
            return [];
        }
        
        var currentPath = window.location.pathname;
        var category = getCurrentCategory();
        if (!category) return [];
        
        // Filter articles in same category, exclude current
        var related = ALL_ARTICLES.filter(function(article) {
            if (article.url === currentPath) return false;
            
            // Check if same category
            var articleMatch = article.url.match(/\/posts\/([^\/]+)(?:\/([^\/]+))?\//);
            if (!articleMatch) return false;
            
            var articleMain = articleMatch[1];
            var articleSub = articleMatch[2] || null;
            
            // Match main category, prefer subcategory match
            if (articleMain === category.main) {
                if (category.sub && articleSub) {
                    return articleSub === category.sub;
                }
                return true;
            }
            return false;
        });
        
        // Sort by date (newest first) and take top 5
        return related.sort(function(a, b) {
            return (b.date || '').localeCompare(a.date || '');
        }).slice(0, 5);
    }

    // Generate related articles HTML
    function generateRelatedArticlesHtml() {
        var related = findRelatedArticles();
        if (related.length === 0) {
            // Fallback: show random articles from ALL_ARTICLES
            if (typeof ALL_ARTICLES !== 'undefined' && ALL_ARTICLES.length > 0) {
                var currentPath = window.location.pathname;
                var others = ALL_ARTICLES.filter(function(a) { return a.url !== currentPath; });
                related = others.sort(function() { return 0.5 - Math.random(); }).slice(0, 5);
            }
        }
        
        if (related.length === 0) return '';
        
        var html = '';
        related.forEach(function(article) {
            html += '<li><a href="' + article.url + '">' + (article.title || '相关文章') + '</a></li>';
        });
        return html;
    }

    // Generate related articles section HTML
    function generateRelatedSection() {
        var relatedHtml = generateRelatedArticlesHtml();
        if (!relatedHtml) {
            return ''; // Don't show section if no related articles
        }
        return '<div class="sidebar-section related-section">\n' +
               '    <h3 class="sidebar-title"><i class="fas fa-bookmark"></i> 相关文章</h3>\n' +
               '    <ul class="related-list">' + relatedHtml + '</ul>\n' +
               '</div>';
    }

    // Generate tags section HTML
    function generateTagsSection() {
        var tagsHtml = CATEGORY_TAGS.map(function(tag) {
            return '<a href="' + tag.url + '" class="tag">' + tag.name + ' (' + tag.count + ')</a>';
        }).join('\n        ');

        return '<div class="sidebar-section tags-section">\n' +
               '    <h3 class="sidebar-title"><i class="fas fa-tags"></i> 主题标签</h3>\n' +
               '    <div class="tag-cloud" id="sidebarTagCloud">\n' +
               '        ' + tagsHtml + '\n' +
               '    </div>\n' +
               '</div>';
    }

    // Generate full sidebar HTML
    function generateSidebar() {
        return '<aside class="sidebar">\n' +
               '    ' + generateAuthorCard() + '\n' +
               '    \n' +
               '    ' + generateTocSection() + '\n' +
               '    \n' +
               '    ' + generateRelatedSection() + '\n' +
               '    \n' +
               '    ' + generateTagsSection() + '\n' +
               '</aside>';
    }

    // Inject sidebar when DOM is ready
    function init() {
        var placeholder = document.getElementById('sidebar-placeholder');
        if (placeholder) {
            placeholder.outerHTML = generateSidebar();
        }
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
