---
layout: post
title: "我给 OpenClaw 装了个浏览器，现在它能自己上网了"
date: 2026-04-07
category: ai-tools
category_name: "AI工具"
---

<p>用 AI agent 最大的痛点是什么？
</p>

<strong>它看不到你的屏幕，打不开你的网页，填不了你的表单。</strong>

<p>你想让它帮你在知乎搜个话题、截个图、抓个数据，它只能告诉你"我打不开这个链接，你把内容发给我"。
</p>

<p>直到我给 OpenClaw 装了 <strong>playwright-mcp</strong>，情况才彻底改变。
</p>

<hr>

<h2>什么是 playwright-mcp？</h2>

<p>简单说：<strong>给 AI agent 装一双眼睛和一双手。</strong>
</p>

<ul>
<li><strong>Playwright</strong>：微软开源的浏览器自动化框架，能控制 Chrome、Firefox、WebKit</li>
<li><strong>MCP</strong>（Model Context Protocol）：Anthropic 推出的 AI 工具调用协议</li>
<li><strong>playwright-mcp</strong>：把 Playwright 包装成 MCP 服务器，AI 可以直接调用</li>
</ul>

<p>装上之后，AI 能做的事：
</p>
<ul>
<li>打开网页、点击按钮、填写表单</li>
<li>提取页面内容、抓取数据</li>
<li>截图、生成 PDF</li>
<li>自动化重复操作（抢票、签到、数据采集）</li>
</ul>

<hr>

<h2>安装过程（踩坑实录）</h2>

<h3>第一步：安装 npm 包</h3>

<pre><code class="language-bash">npm install -g @playwright/mcp
</code></pre>

<blockquote>⚠️ 如果报 <code>command not found: npm</code>，先装 Node.js。</blockquote>

<p>装完后验证：
</p>
<pre><code class="language-bash">playwright-mcp --version
</code></pre>

<h3>第二步：安装浏览器内核</h3>

<pre><code class="language-bash">npx playwright install chromium
</code></pre>

<p>这步会下载 Chromium 浏览器，大概 150MB。如果你网络不好，可以设镜像：
</p>

<pre><code class="language-bash">PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright npx playwright install chromium
</code></pre>

<h3>第三步：在 OpenClaw 中启用</h3>

<p>如果你已经用 skillhub 安装过 playwright-mcp 技能，只需要在配置中启用：
</p>

<pre><code class="language-json">{
<p>  "skills": {
    "entries": {
      "playwright-mcp": {
        "enabled": true
      }
    }
  }
}
</p>
</code></pre>

<p>如果还没安装，一条命令搞定：
</p>

<pre><code class="language-bash">skillhub install playwright-mcp
</code></pre>

<h3>第四步：重启 Gateway</h3>

<p>改完配置后重启 OpenClaw Gateway，新技能就会加载。
</p>

<hr>

<h2>装好了怎么用？</h2>

<p>直接用自然语言告诉 AI 就行：
</p>

<table>
<tr><td>你说的话</td><td>AI 实际做的事</td></tr>
<tr><td>"打开知乎搜索今日热榜"</td><td>启动浏览器 → 导航到知乎 → 搜索 → 提取结果</td></tr>
<tr><td>"帮我把这个网页截图"</td><td>打开页面 → 截图 → 返回图片</td></tr>
<tr><td>"登录这个网站，填一下表单"</td><td>打开登录页 → 填账号密码 → 点击登录</td></tr>
<tr><td>"抓取这个表格的数据"</td><td>打开页面 → 定位表格 → 提取数据 → 返回 JSON</td></tr>
</table>

<p>不需要写代码，不需要配置，<strong>用嘴就行</strong>。
</p>

<hr>

<h2>我踩过的坑</h2>

<h3>坑1：安装后还是不能用</h3>

<strong>原因</strong>：技能安装了但没有在配置中 <code>enabled: true</code>。

<strong>解决</strong>：检查 <code>openclaw.json</code>，确保 <code>skills.entries.playwright-mcp.enabled</code> 为 <code>true</code>。

<h3>坑2：浏览器打不开页面</h3>

<strong>原因</strong>：Chromium 没装或者版本不对。

<strong>解决</strong>：重新运行 <code>npx playwright install chromium</code>。

<h3>坑3：打开知乎/微信等网站被拦截</h3>

<strong>原因</strong>：OpenClaw 有 SSRF 安全策略，默认不允许访问内网地址。

<strong>解决</strong>：大部分公网网站不受影响。如果需要访问特定站点，可以在 <code>browser.ssrfPolicy</code> 中配置白名单。

<h3>坑4：中文网页乱码</h3>

<strong>原因</strong>：Playwright 默认系统编码不是 UTF-8。

<strong>解决</strong>：启动时加 <code>--lang zh-CN</code> 参数。

<hr>

<h2>更进一步：高级玩法</h2>

<h3>1. 自动化数据采集</h3>

<p>让 AI 每天定时打开某个网页，抓取数据保存到本地：
</p>

<pre><code class="language-">每天早上 9 点，打开 XX 网站的热榜页面，
<p>提取前 20 条数据，保存到 CSV 文件。
</p>
</code></pre>

<h3>2. 自动化表单填写</h3>

<p>重复性的表单操作，教 AI 一次，以后自动执行：
</p>

<pre><code class="language-">帮我登录 XX 网站，进入设置页面，
<p>把以下信息填进去：...
</p>
</code></pre>

<h3>3. 网页截图和对比</h3>

<p>监控网页变化：
</p>

<pre><code class="language-">打开 XX 页面截图，和昨天的截图对比，
<p>看看有什么不同。
</p>
</code></pre>

<h3>4. 无障碍测试</h3>

<p>Playwright 有无障碍快照功能，AI 能"看到"页面的结构化信息：
</p>

<pre><code class="language-">打开 XX 页面，用无障碍快照分析页面结构，
<p>告诉我这个页面的布局是否合理。
</p>
</code></pre>

<hr>

<h2>MCP 协议是什么？为什么重要？</h2>

<p>MCP（Model Context Protocol）是 Anthropic 在 2024 年底推出的开放协议，定义了 AI 模型和外部工具之间的通信标准。
</p>

<strong>之前</strong>：每个 AI 平台都要自己写插件（OpenAI 写 Function Calling，Claude 写 Tool Use，各自一套）。

<strong>有了 MCP</strong>：工具开发者只需要写一个 MCP 服务器，所有支持 MCP 的 AI 平台都能用。

<p>这意味着：
</p>
<ul>
<li><strong>playwright-mcp</strong> 不只能用在 OpenClaw，也能用在 Claude Desktop、Cursor 等任何支持 MCP 的平台</li>
<li>以后会有越来越多 MCP 工具（数据库、文件系统、API 调用），即插即用</li>
</ul>

<hr>

<h2>最后</h2>

<p>playwright-mcp 只是一个开始。MCP 生态正在快速爆发，未来 AI agent 的能力边界会越来越模糊。
</p>

<p>给 AI 装上浏览器的那一刻，它就不再是一个"只能聊天的工具"了——它变成了一个<strong>能看、能点、能操作的数字助手</strong>。
</p>

<p>如果你也在用 OpenClaw 或类似的 AI agent 工具，强烈建议装一下。体验完全不一样。
</p>

<hr>

<em>本文基于实际安装操作整理，所有步骤均经过验证。如果你在安装过程中遇到问题，欢迎在评论区交流。</em>

    </section>
    
<div class="giscus-comments">
    <h3>💬 评论区</h3>