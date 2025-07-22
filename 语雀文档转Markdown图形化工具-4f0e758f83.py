import re
import os
import requests
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
import time

class YuqueToMdConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("语雀文档转Markdown工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 创建界面组件
        self.create_widgets()
        
        # 设置请求头，模拟浏览器访问
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Referer": "https://www.yuque.com/"
        }
        
        # 初始化变量
        self.output_dir = os.getcwd()
        self.image_dir = "images"

    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL输入区域
        url_frame = ttk.LabelFrame(main_frame, text="语雀文档链接", padding="10")
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(url_frame, text="文档URL:").pack(anchor=tk.W)
        self.url_entry = ttk.Entry(url_frame, width=80)
        self.url_entry.pack(fill=tk.X, pady=(5, 10))
        self.url_entry.insert(0, "https://www.yuque.com/xiaoqi-pcrpa/wftdwe/zdkgst2xlbsat02b?singleDoc")
        
        # 输出目录选择
        dir_frame = ttk.LabelFrame(main_frame, text="输出设置", padding="10")
        dir_frame.pack(fill=tk.X, pady=(0, 15))
        
        dir_row = ttk.Frame(dir_frame)
        dir_row.pack(fill=tk.X)
        
        ttk.Label(dir_row, text="输出目录:").pack(side=tk.LEFT)
        self.dir_entry = ttk.Entry(dir_row, width=60)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        self.dir_entry.insert(0, os.getcwd())
        
        ttk.Button(dir_row, text="浏览...", command=self.browse_dir).pack(side=tk.RIGHT)
        
        # 按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.convert_btn = ttk.Button(btn_frame, text="开始转换", command=self.start_conversion)
        self.convert_btn.pack(side=tk.RIGHT)
        
        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="转换日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_dir(self):
        dir_path = filedialog.askdirectory(initialdir=self.output_dir)
        if dir_path:
            self.output_dir = dir_path
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, dir_path)

    def log(self, message):
        """在日志区域显示消息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.status_var.set(message)
        self.root.update_idletasks()

    def get_yuque_doc(self, url):
        """从语雀URL获取文档内容"""
        try:
            self.log("正在获取语雀文档...")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 提取标题
            title_tag = soup.find("h1", class_="DocTitle-title")
            title = title_tag.get_text(strip=True) if title_tag else "语雀文档"
            self.log(f"获取文档成功: {title}")
            
            # 提取Markdown内容
            # 语雀文档内容在pre标签内，class包含"language-markdown"
            markdown_tag = soup.find("pre", class_=re.compile(r"language-markdown"))
            if not markdown_tag:
                # 如果找不到pre标签，尝试提取article内容
                self.log("未找到Markdown源代码，尝试提取HTML内容...")
                article_tag = soup.find("article", class_="DocArticle-content")
                if not article_tag:
                    raise Exception("无法提取文档内容，请检查URL是否正确")
                
                # 这里简化处理，实际可能需要更复杂的HTML转Markdown
                markdown_content = f"# {title}\n\n文档内容需要手动转换，请检查原始HTML。"
            else:
                markdown_content = markdown_tag.get_text()
            
            return title, markdown_content
            
        except Exception as e:
            self.log(f"获取文档失败: {str(e)}")
            raise

    def download_images(self, markdown_content):
        """下载Markdown中的图片并替换路径"""
        # 创建图片目录
        image_path = Path(self.output_dir) / self.image_dir
        image_path.mkdir(exist_ok=True)
        
        # 查找所有图片链接
        pattern = r"!\[([^\]]*)\]\((https://cdn\.nlark\.com/[^\)]+)\)"
        matches = re.findall(pattern, markdown_content)
        
        if not matches:
            self.log("未找到图片链接")
            return markdown_content
        
        self.log(f"找到{len(matches)}张图片，开始下载...")
        
        # 下载并替换图片链接
        for i, (alt_text, url) in enumerate(matches, 1):
            try:
                # 提取文件名
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                # 添加前缀，避免文件名冲突
                local_filename = f"yuque_img_{i}_{filename}"
                local_path = str(image_path / local_filename)
                
                # 下载图片
                self.log(f"下载图片 {i}/{len(matches)}: {filename}")
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                # 保存图片
                with open(local_path, "wb") as img_file:
                    img_file.write(response.content)
                
                # 替换链接
                relative_path = os.path.join(self.image_dir, local_filename).replace("\\", "/")
                markdown_content = markdown_content.replace(url, relative_path)
                
            except Exception as e:
                self.log(f"下载图片失败 {i}: {str(e)}")
                # 保留原链接
                continue
        
        self.log(f"图片处理完成，保存到: {str(image_path)}")
        return markdown_content

    def save_markdown(self, title, content):
        """保存处理后的Markdown内容"""
        # 清理标题中的特殊字符，用于文件名
        safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)
        filename = f"{safe_title}.md"
        file_path = Path(self.output_dir) / filename
        
        # 添加标题（如果不存在）
        if not content.startswith("#"):
            content = f"# {title}\n\n{content}"
        
        # 保存文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return str(file_path)

    def start_conversion(self):
        """开始转换流程"""
        self.convert_btn.config(state=tk.DISABLED)
        self.log("="*50)
        self.log(f"转换开始于 {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            url = self.url_entry.get().strip()
            self.output_dir = self.dir_entry.get().strip()
            
            # 1. 获取语雀文档
            title, markdown_content = self.get_yuque_doc(url)
            
            # 2. 下载并替换图片
            processed_content = self.download_images(markdown_content)
            
            # 3. 保存Markdown文件
            file_path = self.save_markdown(title, processed_content)
            
            self.log(f"转换完成！文件已保存至:\n{file_path}")
            self.log("="*50)
            
        except Exception as e:
            self.log(f"转换失败: {str(e)}")
        finally:
            self.convert_btn.config(state=tk.NORMAL)
            self.status_var.set("转换完成" if "转换完成" in self.status_var.get() else "转换失败")

if __name__ == "__main__":
    root = tk.Tk()
    app = YuqueToMdConverter(root)
    root.mainloop()