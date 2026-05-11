// Header Component Generator
// Generates the site header navigation with auto-active link highlighting

(function() {
    'use strict';

    // Site configuration
    var SITE_CONFIG = {
        title: 'halo的技术博客',
        subtitle: 'AI工具 · 行业观察 · 技术实践',
        nav: [
            { href: '/', icon: 'fa-home', label: '主页' },
            { href: '/posts/ai-tools/', icon: 'fa-robot', label: 'AI工具' },
            { href: '/posts/ai-observation/', icon: 'fa-eye', label: 'AI观察' },
            { href: '/posts/hardware/', icon: 'fa-microchip', label: '硬件数码' },
            { href: '/posts/career/', icon: 'fa-briefcase', label: '职业成长' },
            { href: '/posts/investment/', icon: 'fa-chart-line', label: '投资理财' },
            { href: '/posts/reading/', icon: 'fa-book-open', label: '阅读思考' },
            { href: '/posts/tech-tips/', icon: 'fa-wrench', label: '效率技巧' },
            { href: '/posts/life/', icon: 'fa-heart', label: '生活方式' },
            { href: '/posts/archive/', icon: 'fa-archive', label: '归档' },
            { href: '/about/', icon: 'fa-user', label: '关于' }
        ]
    };

    // Get current path
    function getCurrentPath() {
        var path = window.location.pathname;
        // Remove trailing slash for comparison
        if (path.endsWith('/')) {
            path = path.slice(0, -1);
        }
        return path || '/';
    }

    // Check if a link should be active
    function isActive(href, currentPath) {
        if (href === '/') {
            return currentPath === '/' || currentPath === '' || currentPath.endsWith('/index.html');
        }
        return currentPath.startsWith(href);
    }

    // Generate header HTML
    function generateHeader() {
        var currentPath = getCurrentPath();
        var navItems = SITE_CONFIG.nav.map(function(item) {
            var active = isActive(item.href, currentPath) ? ' class="active"' : '';
            return '<li' + active + '><a href="' + item.href + '"><i class="fas ' + item.icon + '"></i> ' + item.label + '</a></li>';
        }).join('\n                    ');

        return '<header>\n' +
               '    <div class="container">\n' +
               '        <h1><a href="/">' + SITE_CONFIG.title + '</a></h1>\n' +
               '        <h2>' + SITE_CONFIG.subtitle + '</h2>\n' +
               '        <nav>\n' +
               '            <ul>\n' +
               '                    ' + navItems + '\n' +
               '            </ul>\n' +
               '        </nav>\n' +
               '    </div>\n' +
               '</header>';
    }

    // Inject header when DOM is ready
    function init() {
        var placeholder = document.getElementById('header-placeholder');
        if (placeholder) {
            placeholder.outerHTML = generateHeader();
        }
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
