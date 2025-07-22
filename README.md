# 肖麒简洁静态博客 - 目录结构与使用说明

## 网站地址
 ```
 https://blog.yybf1.cn
 ```
 

## 一、目录结构

```
blog/
├── index.html           # 博客首页
├── articles/            # 存放Markdown文章的目录
│   ├── hello-world.md   # 示例文章1
│   └── getting-started.md # 示例文章2
├── images/            # 存放图片的目录
├── css/                 # 样式表目录
├── js/                  # JavaScript脚本目录
└── README.md            # 使用说明文档
```

## 二、Markdown文章格式要求

1. **文件命名**：
   - 使用英文或拼音命名，避免中文和特殊字符
   - 扩展名为`.md`
   - 示例：`vue-composition-api.md`

2. **文章元数据**（必须放在文章开头）：
   ```
   ---
   title: "文章标题"
   date: "2023-10-15"
   author: "肖麒"
   excerpt: "文章简短摘要，将显示在文章列表页"
   ---
   ```

3. **内容格式**：
   - 使用标准Markdown语法
   - 支持标题、段落、列表、代码块、链接、图片等

## 三、添加新文章步骤

1. 使用任意Markdown编辑器编写文章
2. 按照上述格式要求添加元数据
3. 将文件保存为`.md`格式
4. 上传到服务器的`articles/`目录
5. 刷新博客页面即可看到新文章## 四、宝塔面板部署教程

### 1. 准备工作
- 已安装宝塔面板的服务器
- 已备案的域名（可选）

### 2. 创建网站
1. 登录宝塔面板
2. 点击左侧菜单「网站」→「添加站点」
3. 填写域名信息（如无域名可填写IP地址）
4. 选择PHP版本：纯静态（无需PHP）
5. 点击「提交」

### 3. 上传文件
1. 进入网站根目录（通常为`/www/wwwroot/你的域名/`）
2. 上传以下文件和目录：
   - `index.html`（博客主页）
   - `articles/`目录（包含所有Markdown文章）
   - `博客目录结构与使用说明.md`（使用教程）

### 4. Nginx配置
1. 在宝塔面板中，点击网站对应的「设置」
2. 选择「配置文件」标签
3. 在`server`块中添加以下配置：

```nginx
location /articles/ {
    autoindex on;
    add_header Cache-Control "no-cache, no-store, must-revalidate";
}

location ~* \.md$ {
    default_type text/plain;
    add_header Cache-Control "no-cache, no-store, must-revalidate";
}
```

4. 点击「保存」并重启Nginx

### 5. 设置文件权限
1. 右键点击网站根目录
2. 选择「权限」
3. 将目录权限设置为755，文件权限设置为644
4. 所有者设置为www:www

## 五、常见问题解决

### 1. 新文章不显示
- 确保MD文件已正确上传到`articles/`目录
- 检查文件名是否符合规范（英文或拼音，无特殊字符）
- 清除浏览器缓存或按Ctrl+F5强制刷新

### 2. Markdown格式显示异常
- 检查文章是否使用标准Markdown语法
- 确保文章元数据格式正确
- 确认marked.js库已正确加载

### 3. 网站访问速度慢
- 优化图片大小
- 启用宝塔面板的「CDN加速」功能
- 开启Nginx缓存
