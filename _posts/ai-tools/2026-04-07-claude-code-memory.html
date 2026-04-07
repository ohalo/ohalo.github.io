---
layout: post
title: "Claude Code 记忆机制：六层体系实操指南"
date: 2026-04-07
category: ai-tools
category_name: "AI工具"
---

<blockquote>看完这篇，你会彻底搞懂 Claude Code 的记忆分层，不再被"明明告诉过它"的问题困扰。</blockquote>

    <h2>先说痛点</h2>
    <p>用 Claude Code 的人大概都遇到过：</p>
    <blockquote>关掉会话，第二天回来，它什么都不记得了。项目用什么包管理器？代码风格怎么约定？上次调试到哪里？全要重新解释一遍。</blockquote>
    <p>Anthropic 推出了 <strong>Auto Memory</strong> 功能，让 Claude Code 自己记笔记。听起来很美好，但如果你不理解它的记忆体系是怎么分层的，很容易搞出一堆互相矛盾的指令。</p>

    <h2>一、两套记忆系统</h2>
    <p>Claude Code 有两套互补的记忆系统：</p>
    <table>
        <thead><tr><th></th><th>CLAUDE.md</th><th>Auto Memory</th></tr></thead>
        <tbody>
            <tr><td><strong>谁写的</strong></td><td>你</td><td>Claude 自己</td></tr>
            <tr><td><strong>里面是什么</strong></td><td>指令、规则</td><td>学到的模式、踩过的坑</td></tr>
            <tr><td><strong>作用范围</strong></td><td>项目/用户/组织</td><td>单个项目</td></tr>
            <tr><td><strong>什么时候加载</strong></td><td>每次会话</td><td>每次会话（前200行）</td></tr>
            <tr><td><strong>用来干嘛</strong></td><td>编码规范、工作流、架构决策</td><td>构建命令、调试经验、偏好</td></tr>
        </tbody>
    </table>
    <p>简单说：<strong>CLAUDE.md 是你在管它，Auto Memory 是它自己在总结经验。</strong></p>

    <h2>二、六层记忆结构</h2>
    <p>CLAUDE.md 不是一个文件，而是一个层级体系。从全局到局部：</p>
    <table>
        <thead><tr><th>层级</th><th>位置</th><th>谁维护</th><th>共享范围</th></tr></thead>
        <tbody>
            <tr><td>组织策略</td><td><code>/Library/Application Support/ClaudeCode/CLAUDE.md</code></td><td>IT/DevOps</td><td>组织内所有人</td></tr>
            <tr><td>项目记忆</td><td><code>./CLAUDE.md</code> 或 <code>./.claude/CLAUDE.md</code></td><td>团队</td><td>通过 Git 共享</td></tr>
            <tr><td>项目规则</td><td><code>./.claude/rules/*.md</code></td><td>团队</td><td>通过 Git 共享</td></tr>
            <tr><td>用户记忆</td><td><code>~/.claude/CLAUDE.md</code></td><td>个人</td><td>所有项目</td></tr>
            <tr><td>项目本地</td><td><code>./CLAUDE.local.md</code></td><td>个人</td><td>仅当前项目</td></tr>
            <tr><td>Auto Memory</td><td><code>~/.claude/projects/&lt;project&gt;/memory/</code></td><td>Claude</td><td>仅你自己</td></tr>
        </tbody>
    </table>
    <p><strong>越具体的层级优先级越高。</strong> 项目规则覆盖用户偏好，本地配置覆盖项目配置。这个设计很像 Git 的配置层级：<code>--system</code>、<code>--global</code>、<code>--local</code>。</p>

    <h2>三、CLAUDE.md 怎么写</h2>
    <p>CLAUDE.md 本质就是 Markdown，用自然语言写指令。</p>
    <h3>一个例子</h3>
    <pre><code># 项目约定
- 使用 pnpm，不要用 npm
- 测试命令：pnpm test
- 提交前必须跑 lint

# 代码风格
- TypeScript 严格模式
- 组件用 PascalCase，工具函数用 camelCase</code></pre>
    <h3>三条实用建议</h3>
    <ol>
        <li><strong>把常用命令写进去</strong> - Claude Code 每次都要翻 package.json 找构建命令，不如直接告诉它。</li>
        <li><strong>写具体的约定，不写模糊的要求</strong> - ❌ "代码要简洁" → ✅ "函数不超过 30 行"</li>
        <li><strong>用 /init 自动生成</strong> - Claude Code 会扫描项目结构，生成一份基础的 CLAUDE.md。</li>
    </ol>

    <h2>四、模块化规则：.claude/rules/</h2>
    <p>当项目变大，一个 CLAUDE.md 会变得又长又杂。<code>.claude/rules/</code> 目录解决这个问题——按主题拆分。</p>
    <h3>条件规则：只在特定文件时生效</h3>
    <pre><code>---
paths:
- "src/api/**/*.ts"
---
# API 开发规则
- 所有端点必须做输入校验
- 使用标准错误响应格式</code></pre>
    <p>带 paths 的规则只在 Claude 实际读写匹配文件时才生效。处理前端代码时这条规则不起作用，只有碰到 <code>src/api/</code> 下的 TypeScript 文件时才会生效。</p>

    <h2>五、Auto Memory：让它自己记</h2>
    <p>这是新功能。Claude Code 会在工作过程中自己记笔记。</p>
    <h3>它记什么</h3>
    <ul>
        <li><strong>项目模式</strong>：构建命令、测试约定、代码风格</li>
        <li><strong>调试经验</strong>：遇到过的坑、解决方案</li>
        <li><strong>架构笔记</strong>：关键文件、模块关系</li>
        <li><strong>你的偏好</strong>：沟通风格、工作习惯、工具选择</li>
    </ul>
    <h3>存在哪里</h3>
    <pre><code>~/.claude/projects/&lt;project&gt;/memory/
├── MEMORY.md      # 索引文件，每次启动加载前 200 行
├── debugging.md   # 调试相关笔记
├── api-conventions.md  # API 设计决策
└── ...</code></pre>
    <h3>怎么控制</h3>
    <p>Auto Memory 默认开启。如果不想用：对话里跑 <code>/memory</code> 关闭，或设置环境变量 <code>CLAUDE_CODE_DISABLE_AUTO_MEMORY=1</code>。</p>
    <p>你也可以主动让它记住东西：</p>
    <blockquote>"记住我们用 pnpm 不用 npm"<br>"保存到记忆：API 测试需要本地 Redis"</blockquote>
    <p>反过来也行：</p>
    <blockquote>"忘掉之前关于 Redis 的记忆"</blockquote>

    <h2>六、导入机制：@path/to/file</h2>
    <p>CLAUDE.md 支持 <code>@path/to/file</code> 语法导入其他文件：</p>
    <pre><code>参考 @README 了解项目概况，@package.json 查看可用命令。

# 额外指令
- Git 工作流 @docs/git-instructions.md</code></pre>
    <p>相对路径基于当前文件所在目录解析，支持递归导入，最深 5 层。</p>
    <h3>一个实用场景</h3>
    <p>如果你用 Git worktree，<code>CLAUDE.local.md</code> 只存在于一个 worktree 里。把个人配置放到 home 目录，然后导入：</p>
    <pre><code># 个人偏好
- @~/.claude/my-project-instructions.md</code></pre>

    <h2>七、加载时机：为什么没生效？</h2>
    <table>
        <thead><tr><th>加载类型</th><th>说明</th></tr></thead>
        <tbody>
            <tr><td><strong>启动时全量加载</strong></td><td>工作目录往上的所有 CLAUDE.md、CLAUDE.local.md、~/.claude/rules/*.md、Auto Memory 的 MEMORY.md 前 200 行</td></tr>
            <tr><td><strong>按需加载</strong></td><td>子目录下的 CLAUDE.md 只在 Claude 读取那个目录的文件时才加载；Auto Memory 的主题文件在需要时读取</td></tr>
            <tr><td><strong>条件加载</strong></td><td>.claude/rules/ 里有 paths 字段的规则只在匹配文件时生效</td></tr>
        </tbody>
    </table>
    <p>这意味着你可以在 monorepo 的每个子包里放自己的 CLAUDE.md，不会一开始就把所有指令都塞进上下文。</p>

    <h2>八、最佳实践</h2>
    <ol>
        <li><strong>项目 CLAUDE.md 写团队共识，提交到 Git</strong> - 构建命令、代码规范、架构决策</li>
        <li><strong>CLAUDE.local.md 写个人偏好，自动 .gitignore</strong> - 你的测试数据路径、沙箱 URL</li>
        <li><strong>Auto Memory 让它自己跑，定期检查</strong> - 检查 MEMORY.md 有没有记错的</li>
        <li><strong>不要重复</strong> - 如果 CLAUDE.md 里已经写了"用 pnpm"，Auto Memory 再记一遍就是噪音</li>
        <li><strong>保持精简</strong> - MEMORY.md 超过 200 行就会被截断，把细节移到独立文件</li>
    </ol>

    <h2>最后说一句</h2>
    <p>记忆越多不代表越好。</p>
    <p>Claude Code 每次启动都会把这些内容塞进 system prompt，占的是上下文窗口。<strong>写得精准、组织得清楚，比写得多更重要。</strong></p>

    <hr>

    <p><em>数据来源：Claude Code 官方文档、掘金、知乎问答</em></p>