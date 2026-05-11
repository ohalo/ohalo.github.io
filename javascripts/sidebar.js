// TOC Component Generator
// Generates sticky TOC panel on the right side of article

(function() {
    'use strict';

    // Generate TOC from article headings
    function generateToc() {
        var article = document.querySelector('article');
        if (!article) return '';

        var headings = article.querySelectorAll('h2, h3, h4');
        if (headings.length === 0) return '';

        var tocHtml = '';
        headings.forEach(function(heading, index) {
            // Create anchor ID if not exists
            if (!heading.id) {
                heading.id = 'section-' + index;
            }

            var level = parseInt(heading.tagName.substring(1));
            var levelClass = 'toc-h' + level;

            tocHtml += '<li class="' + levelClass + '"><a href="#' + heading.id + '">' + heading.textContent + '</a></li>';
        });

        return '<div class="toc-sticky-wrapper">' +
               '<div class="toc-panel">' +
               '<h4 class="toc-title">文章目录</h4>' +
               '<ul class="toc-list">' + tocHtml + '</ul>' +
               '</div>' +
               '</div>';
    }

    // Setup scroll spy for active link highlighting
    function setupScrollSpy() {
        var tocLinks = document.querySelectorAll('.toc-list a');
        var headings = document.querySelectorAll('article h2, article h3, article h4');

        if (tocLinks.length === 0 || headings.length === 0) return;

        function updateActiveLink() {
            var scrollY = window.scrollY;
            var current = '';

            headings.forEach(function(heading) {
                if (heading.offsetTop - 120 <= scrollY) {
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

    // Inject TOC into article page - after post-content-wrapper (sibling)
    function init() {
        var tocHtml = generateToc();
        if (!tocHtml) return;

        var postContentWrapper = document.querySelector('.post-content-wrapper');
        if (postContentWrapper) {
            // Insert TOC after post-content-wrapper (as sibling, inside post-layout)
            postContentWrapper.insertAdjacentHTML('afterend', tocHtml);
            setupScrollSpy();
        }
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
