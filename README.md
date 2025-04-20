# 小红书内容抓取API

这是一个基于FastAPI构建的小红书内容抓取API，可以抓取小红书帖子的标题、内容和图片。

## 功能特点

- 支持抓取小红书帖子内容
- 自动下载帖子中的图片
- 提供RESTful API接口
- 支持手机分享格式的链接提取

## 安装

1. 克隆仓库：

```bash
git clone <仓库地址>
cd <仓库目录>
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 确保已安装Chrome浏览器。

## 使用方法

1. 启动API服务器：

```bash
uvicorn app:app --reload
```

2. 服务器将在 http://127.0.0.1:8000 上运行

3. 访问API文档：http://127.0.0.1:8000/docs

## API端点

### 1. 抓取帖子内容

**请求**：

```
POST /scrape/
```

**参数**：

```json
{
  "url": "http://xhslink.com/a/IGTNc5Db7WEab",  // 小红书分享链接或直接URL
  "save_metadata": true  // 是否保存元数据到JSON文件
}
```

**响应**：

```json
{
  "title": "帖子标题",
  "content": "帖子内容",
  "image_urls": ["图片URL1", "图片URL2", ...],
  "downloaded_files": ["本地文件路径1", "本地文件路径2", ...],
  "output_dir": "输出目录路径",
  "saved_metadata_path": "元数据JSON文件路径"
}
```

### 2. 登录小红书

**请求**：

```
POST /login/
```

**响应**：

```json
{
  "message": "登录成功"
}
```

## 注意事项

1. 首次使用时需要手动登录小红书，登录成功后会保存cookies以便后续使用。
2. 如遇到登录问题，请在浏览器中手动登录。
3. 抓取结果会保存在`xiaohongshu_posts`目录下。

## 技术栈

- FastAPI
- Selenium
- Chrome WebDriver
- Pydantic
- Requests

## 许可证

[MIT License](LICENSE) 