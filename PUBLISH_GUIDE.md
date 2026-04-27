# 博客发布规范 (PUBLISH_GUIDE)

每次发布文章到 GitHub Pages 前，**必须**执行以下自检。

---

## 一、Frontmatter 格式（最高优先级）

| 字段 | 正确写法 | ❌ 错误写法 |
|------|----------|------------|
| `date` | `date: 2026-04-28` | `date: 2026-04-28 09:30:00 +0800` |
| `layout` | `layout: post` | 其他值 |
| `permalink` | `/posts/{category}/{slug}.html` | 其他格式 |
| `category` | 路径格式，如 `tech-tips/security` | `/posts/tech-tips/security/` |

**⚠️ 教训：date 字段绝对不能带时间和时区，否则 GitHub Pages 的 Jekyll 构建会静默跳过该文件，导致 404！**

---

## 二、分类索引（每次必检）

发布前必须确认以下索引页面存在并已更新：

| 索引页 | 检查命令 |
|--------|----------|
| `posts/{category}/index.html` | 文件存在 + 列表含新文章链接 |
| `posts/{category}/{subcategory}/index.html` | 同上 |
| `posts/index.html` | 同上 |
| `posts/tech-tips/index.html` | 若有新子分类，必须加入链接 |

**⚠️ 教训：新增文章对应的分类目录若无 index.html，导航链接会 404！**

---

## 三、配图要求

- 每篇文章至少 2 张图
- 图片保存到 `blog-repo/images/{slug}/`
- HTML 中用 `<img src="/images/{slug}/xxx.jpg">` 引用

---

## 四、Git 提交流程

1. `git add -A`
2. `git diff --cached --stat` ← **必须看这一眼，确认改动范围**
3. `git commit -m "feat: {一句话描述}"`
4. `git push`
5. **等待 2 分钟后验证文章 URL 返回 200**

---

## 五、常见 404 排查路径

```
1. 文章 404 → 检查 frontmatter date 格式
2. 分类索引 404 → 检查 posts/{category}/index.html 是否存在
3. 导航链接 404 → 检查父级 index.html 是否更新
4. 全部 404 → 检查 _config.yml 是否含 future: true + timezone: Asia/Shanghai
```

---

*本文档由 AI 自动维护，发现问题后更新本文件并同步更新 cron 任务 prompt。*
