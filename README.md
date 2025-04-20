# 小红书内容抓取工具

一个基于 Selenium 的自动化工具，用于抓取小红书帖子内容和图片。

## 主要功能

- 自动登录小红书（首次使用需手动登录，之后自动保存 cookies）
- 抓取帖子标题、正文内容和图片
- 自动下载帖子中的所有图片
- 支持手机分享文本中的链接提取
- 将内容保存为 JSON 格式（可选）

## 使用方法

### 环境准备

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安装依赖
pip install selenium webdriver-manager requests
```

### 运行脚本

```bash
python xiaohongshu_scraper.py
```

### 输入格式

支持以下输入格式：
1. 直接输入小红书URL链接
2. 粘贴手机分享的完整文本，例如：
   "34 某用户发布了一篇小红书笔记，快来看吧！😆 tnk9xxx 😆 http://xhslink.com/a/xxx"

### 图片存储

- 所有图片会自动保存在 `xiaohongshu_posts/帖子标题/` 目录下
- 图片按顺序编号（001.jpg, 002.jpg 等）

## 注意事项

- 首次使用需要手动登录小红书账号
- 脚本会自动保存 cookies 以便后续使用
- 需要稳定的网络连接 