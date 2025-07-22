---
title: "Hello World - 我的第一篇博客"
date: "2023-10-20"
author: "肖麒"
excerpt: "这是我的第一篇博客文章，介绍了如何使用这个简洁的静态博客系统。"
---

# Hello World!

## 欢迎来到我的个人网站

这是我使用**肖麒简洁静态博客系统**发布的第一篇文章。这个博客系统具有以下特点：

- ✅ 完全静态，无需后端数据库
- ✅ 支持Markdown格式文章
- ✅ 简洁大气的设计风格
- ✅ 响应式布局，适配各种设备

## 如何发布新文章

1. 使用Markdown编辑器编写文章
2. 添加必要的元数据（标题、日期等）
3. 将文件保存到`articles/`目录
4. 刷新博客页面即可看到新文章

## 代码示例

以下是一个简单的JavaScript代码示例：

```javascript
// 加载Markdown文章
function loadArticle(filename) {
  fetch(`articles/${filename}`)
    .then(response => response.text())
    .then(text => {
      // 解析Markdown内容
      const html = marked.parse(text);
      document.getElementById('article-content').innerHTML = html;
    });
}
```

希望这个博客系统能帮助我更好地分享技术心得和学习笔记！
