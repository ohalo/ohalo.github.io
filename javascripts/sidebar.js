// Sidebar Component Generator
// Replaces static sidebar with floating TOC button + panel

(function() {
    'use strict';

    // Generate TOC from article headings
    function generateTocFromHeadings() {
        var article = document.querySelector('article');
        if (!article) return '';
        
        var headings = article.querySelectorAll('h2, h3');
        if (headings.length === 0) return '';
        
        var tocHtml = '';
        headings.forEach(function(heading, index) {
            // Create anchor if not exists
            if (!heading.id) {
                heading.id = 'section-' + index;
            }
            var level = heading.tagName === 'H2' ? '' : ' class="toc-h3"';
            tocHtml += '<li' + level + '><a href="#' + heading.id + '">' + heading.textContent + '</a></li>';
        });
        return tocHtml;
    }

    // Generate the full floating TOC HTML
    function generateFloatingToc() {
        var tocContent = generateTocFromHeadings();
        if (!tocContent) return ''; // Don't show if no headings

        return '<div id="floating-toc-btn" class="floating-toc-btn" title="文章目录">\n' +
               '    <i class="fas fa-list-ul"></i>\n' +
               '</div>\n' +
               '\n' +
               '<div id="floating-toc-panel" class="floating-toc-panel">\n' +
               '    <div class="floating-toc-header">\n' +
               '        <h4>文章目录</h4>\n' +
               '        <button id="floating-toc-close" class="floating-toc-close" title="关闭">\n' +
               '            <i class="fas fa-times"></i>\n' +
               '        </button>\n' +
               '    </div>\n' +
               '    <div class="floating-toc-content">\n' +
               '        <ul class="toc-list">' + tocContent + '</ul>\n' +
               '    </div>\n' +
               '</div>';
    }

    // Toggle floating TOC panel
    function setupFloatingToc() {
        var btn = document.getElementById('floating-toc-btn');
        var panel = document.getElementById('floating-toc-panel');
        var closeBtn = document.getElementById('floating-toc-close');

        if (!btn || !panel) return;

        // Click button to toggle
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            panel.classList.toggle('open');
            btn.classList.toggle('active');
        });

        // Click close button
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                panel.classList.remove('open');
                btn.classList.remove('active');
            });
        }

        // Click outside to close
        document.addEventListener('click', function(e) {
            if (!panel.contains(e.target) && !btn.contains(e.target)) {
                panel.classList.remove('open');
                btn.classList.remove('active');
            }
        });

        // Active link highlighting on scroll
        var tocLinks = panel.querySelectorAll('a');
        var headings = document.querySelectorAll('article h2, article h3');
        
        function updateActiveLink() {
            var scrollY = window.scrollY;
            var current = '';
            
            headings.forEach(function(heading) {
                if (heading.offsetTop - 100 <= scrollY) {
                    current = heading.id;
                }
            });
            
            tocLinks.forEach(function(link) {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {
                    link.classList.add('active');
                }
            });
        }

        window.addEventListener('scroll', updateActiveLink, { passive: true });
        updateActiveLink();
    }

    // Inject floating TOC when DOM is ready
    function init() {
        var floatingToc = generateFloatingToc();
        if (!floatingToc) return; // No TOC to show

        var placeholder = document.getElementById('sidebar-placeholder');
        if (placeholder) {
            placeholder.innerHTML = floatingToc;
        } else {
            // Fallback: append to body
            document.body.insertAdjacentHTML('beforeend', floatingToc);
        }

        setupFloatingToc();
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
