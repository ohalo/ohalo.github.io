---
layout: post
title: "我用AI助手三件套，把一天的网页操作压缩到了3分钟"
date: 2026-04-07
category: ai-tools
category_name: "AI工具"
---

<p><em>一个能搜索、能抓取、能替你点鼠标的AI，到底有多爽？</em></p>

<hr>

<h2>前言：你还在手动操作网页吗？</h2>

<p>我见过太多人每天重复这样的操作——</p>

<p>打开百度搜个关键词，点开5个链接找信息，复制粘贴到文档里整理，然后再打开另一个网站继续搜……</p>

<p><strong>一个简单的信息收集任务，手动操作至少30分钟。</strong></p>

<p>但如果你的AI助手能自己做这些事呢？</p>

<p>不是那种"我帮你搜一下然后给你链接"的半成品，而是<strong>真的能搜索、真的能抓内容、真的能操作浏览器</strong>的完整能力。</p>

<p>OpenClaw 就给了你这样三件套：</p>

<ul>
<li><strong>web_search</strong> → 搜索（像你用百度一样，但更快更准）</li>
<li><strong>web_fetch</strong> → 抓取（一键提取网页正文，过滤广告和废话）</li>
<li><strong>browser</strong> → 自动化（替你点按钮、填表单、截图、处理弹窗）</li>
</ul>

<p>今天我把自己踩过的坑和摸索出来的最佳实践，整理成这篇保姆级指南。</p>

<hr>

<h2>一、web_search：让AI替你搜</h2>

<h3>1.1 它和普通搜索有什么区别？</h3>

<p>你用百度搜"AI工具推荐"，得到的是一堆广告和SEO内容。</p>

<p>你让 web_search 搜同样的东西，它基于 Brave Search API 返回的，是<strong>标题 + 链接 + 摘要</strong>的精简结果，没有广告，没有废话，直接给你有用的信息。</p>

<h3>1.2 核心参数（记住这几个就够了）</h3>

<table>
<thead><tr><th>参数</th><th>作用</th><th>举例</th></tr></thead>
<tbody>
<tr><td><code>query</code></td><td>搜索关键词</td><td><code>"OpenClaw 教程"</code></td></tr>
<tr><td><code>count</code></td><td>返回几条结果</td><td><code>5</code>（默认10条）</td></tr>
<tr><td><code>country</code></td><td>搜索哪个地区</td><td><code>CN</code>中国、<code>US</code>美国</td></tr>
<tr><td><code>search_lang</code></td><td>搜索结果语言</td><td><code>zh</code>中文、<code>en</code>英文</td></tr>
<tr><td><code>freshness</code></td><td>时间范围</td><td><code>pd</code>今天、<code>pw</code>本周、<code>pm</code>本月、<code>py</code>今年</td></tr>
</tbody>
</table>

<p><strong>实战技巧</strong>：搜索中文内容一定要加 <code>country=CN</code> + <code>search_lang=zh</code>，不然结果可能完全不相关（别问我怎么知道的）。</p>

<h3>1.3 一个小场景</h3>

<p>你想了解"2026年AI Agent最新进展"——</p>

<pre><code>web_search({
  "query": "AI Agent 最新进展 2026",
  "count": 5,
  "country": "CN",
  "search_lang": "zh",
  "freshness": "pm"  // 只看最近一个月的
})</code></pre>

<p>5秒内，5条最新、最相关的结果就摆在你面前了。</p>

<hr>

<h2>二、web_fetch：一键提取网页正文</h2>

<h3>2.1 解决什么问题？</h3>

<p>你找到一篇好文章，但里面有：导航栏、侧边栏广告、"猜你喜欢"推荐、评论区、弹窗……</p>

<p>你只想看<strong>正文内容</strong>。</p>

<p>web_fetch 内置了智能内容提取算法，自动过滤掉所有噪音，只给你文章本身。</p>

<h3>2.2 两种模式</h3>

<table>
<thead><tr><th>模式</th><th>输出格式</th><th>适用场景</th></tr></thead>
<tbody>
<tr><td><code>markdown</code></td><td>保留标题层级、列表、链接</td><td>需要格式化内容的场景</td></tr>
<tr><td><code>text</code></td><td>纯文本</td><td>只需要文字信息的场景</td></tr>
</tbody>
</table>

<p><strong>我的经验</strong>：90%的情况用 <code>markdown</code> 就对了，它保留了文章结构，后续处理更方便。</p>

<h3>2.3 实用技巧</h3>

<pre><code>// 抓取一篇文章，限制5000字符（省钱）
web_fetch({
  "url": "https://example.com/long-article",
  "extractMode": "markdown",
  "maxChars": 5000
})</code></pre>

<p><code>maxChars</code> 是个被低估的参数。很多长文章你根本不需要全部内容，限制字符数可以节省 token 消耗，提高处理速度。</p>

<h3>2.4 web_fetch 的局限性</h3>

<p><strong>它不能做的事</strong>：</p>

<ul>
<li>❌ 处理需要登录的页面（Cookie、Token）</li>
<li>❌ 渲染 JavaScript 动态内容</li>
<li>❌ 处理验证码</li>
</ul>

<p>这些场景就需要用到第三件套了。</p>

<hr>

<h2>三、browser：让AI替你操作浏览器</h2>

<h3>3.1 这是什么级别的武器？</h3>

<p>如果说 web_search 是"帮你搜"，web_fetch 是"帮你读"，那 browser 就是<strong>"帮你做"</strong>。</p>

<p>基于 Playwright 框架，它能：</p>

<ul>
<li>✅ 打开网页、导航跳转</li>
<li>✅ 点击按钮、填写表单</li>
<li>✅ 处理弹窗、下拉选择</li>
<li>✅ 截图保存、页面快照分析</li>
<li>✅ 执行 JavaScript</li>
<li>✅ 管理 Cookie 和登录状态</li>
</ul>

<h3>3.2 支持的操作类型</h3>

<table>
<thead><tr><th>操作</th><th>说明</th><th>实际用途</th></tr></thead>
<tbody>
<tr><td><code>click</code></td><td>点击元素</td><td>点"同意Cookie"、点"下一页"</td></tr>
<tr><td><code>type</code></td><td>输入文本</td><td>填搜索框、填表单</td></tr>
<tr><td><code>press</code></td><td>按键盘</td><td>回车提交、Ctrl+C复制</td></tr>
<tr><td><code>hover</code></td><td>鼠标悬停</td><td>触发下拉菜单</td></tr>
<tr><td><code>drag</code></td><td>拖拽</td><td>调整滑块、拖拽排序</td></tr>
<tr><td><code>select</code></td><td>下拉选择</td><td>选择省份、选择分类</td></tr>
<tr><td><code>fill</code></td><td>填充表单</td><td>一键填写整个表单</td></tr>
<tr><td><code>resize</code></td><td>调整窗口</td><td>测试响应式布局</td></tr>
<tr><td><code>wait</code></td><td>等待加载</td><td>等待AJAX请求完成</td></tr>
</tbody>
</table>

<h3>3.3 两种运行模式</h3>

<table>
<thead><tr><th>模式</th><th>特点</th><th>适用场景</th></tr></thead>
<tbody>
<tr><td><strong>沙箱模式</strong></td><td>隔离环境，安全性高</td><td>处理不可信网页</td></tr>
<tr><td><strong>主机模式</strong></td><td>直接运行，性能更好</td><td>需要访问本地资源</td></tr>
</tbody>
</table>

<h3>3.4 一个真实案例：自动化登录 + 数据采集</h3>

<p>假设你需要每天从某个需要登录的网站采集数据：</p>

<pre><code>Step 1: browser.open("https://target-site.com/login")
Step 2: browser.act(type="fill", 目标="用户名输入框", text="your_username")
Step 3: browser.act(type="fill", 目标="密码输入框", text="your_password")
Step 4: browser.act(type="click", 目标="登录按钮")
Step 5: browser.act(type="wait", 目标="页面加载完成")
Step 6: browser.navigate("https://target-site.com/data-page")
Step 7: browser.snapshot() → 获取页面结构
Step 8: browser.act(type="click", 目标="导出按钮")</code></pre>

<p><strong>整个过程不需要你碰一下鼠标。</strong></p>

<hr>

<h2>四、三件套的配合使用</h2>

<p>这三件套的真正威力，在于<strong>组合使用</strong>。</p>

<h3>典型工作流</h3>

<pre><code>1. web_search("关键词") → 搜索到10个相关链接
2. web_fetch(最相关的3个URL) → 提取正文内容
3. AI 整理分析 → 生成报告
4. browser(填表单/发邮件) → 自动发布或发送</code></pre>

<h3>实际例子：竞品分析报告</h3>

<pre><code>1. web_search("竞品A 功能对比", count=5)
2. web_search("竞品B 功能对比", count=5)
3. web_fetch(3篇深度评测文章)
4. AI 生成对比表格 + 分析报告
5. 保存为 Markdown 文件</code></pre>

<p><strong>过去需要半天的工作，现在10分钟搞定。</strong></p>

<hr>

<h2>五、那些文档里不会告诉你的坑</h2>

<p><strong>坑1：搜索结果质量参差不齐</strong><br>
中文搜索用百度经常触发安全验证，用 Bing CN 有时不相关。<br>
<em>解决方案</em>：多引擎轮询，Bing CN + Bing INT + DuckDuckGo 三个一起用，取最好的结果。</p>

<p><strong>坑2：web_fetch 抓不到动态页面</strong><br>
很多现代网站用 JavaScript 渲染内容（比如 SPA），web_fetch 只能拿到一个空壳。<br>
<em>解决方案</em>：检测到空内容时自动降级到 browser 工具。</p>

<p><strong>坑3：浏览器自动化不稳定</strong><br>
网络延迟、页面加载顺序变化、弹窗随机出现……这些都会导致自动化脚本中断。<br>
<em>解决方案</em>：善用 <code>wait</code> 操作等待特定元素出现，而不是硬编码等待时间。</p>

<p><strong>坑4：Google 搜索被屏蔽</strong><br>
直接 fetch Google 搜索在国内可能被屏蔽。<br>
<em>解决方案</em>：用 Google HK (<code>google.com.hk</code>) 或 Bing INT 替代。</p>

<hr>

<h2>六、总结</h2>

<table>
<thead><tr><th>工具</th><th>一句话定位</th><th>你该用它来</th></tr></thead>
<tbody>
<tr><td>web_search</td><td><strong>帮你搜</strong></td><td>快速获取搜索结果</td></tr>
<tr><td>web_fetch</td><td><strong>帮你读</strong></td><td>提取网页正文内容</td></tr>
<tr><td>browser</td><td><strong>帮你做</strong></td><td>操作浏览器、处理复杂交互</td></tr>
</tbody>
</table>

<p><strong>我的建议</strong>：</p>

<ul>
<li>90%的信息获取任务，web_search + web_fetch 就够了</li>
<li>需要登录、动态渲染、复杂交互时，才动用 browser</li>
<li>永远先用 web_search 搜一圈，再用 web_fetch 深入抓取——别上来就开浏览器</li>
</ul>

<p>OpenClaw 目前 GitHub 310k+ Star，开源免费，支持 Claude、GPT、本地模型。如果你还没有体验过"让AI帮你上网"的感觉，强烈建议试试。</p>

<hr>

<h2>写在最后</h2>

<p>AI 助手的核心价值不在于"能和你聊天"，而在于<strong>能帮你做事</strong>。</p>

<p>搜索、抓取、自动化——这三件套覆盖了你日常90%的网页操作需求。</p>

<p><strong>省下来的时间，才是真正的生产力。</strong></p>

<hr>

<p><em>觉得有用的话，点个赞，关注我，后续会分享更多 OpenClaw 实战技巧 👍</em></p>

    </section>
    
<div class="giscus-comments">
    <h3>💬 评论区</h3>