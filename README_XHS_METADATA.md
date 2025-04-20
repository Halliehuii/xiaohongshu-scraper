# 小红书元数据抓取API

这是一个简单的FastAPI应用，用于从小红书分享链接中提取元数据，包括标题、描述和图片URL。

## 功能特点

- 从分享文本中自动提取小红书短链接
- 自动跟踪短链接重定向获取最终URL
- 使用BeautifulSoup提取页面元数据
- 返回标题、描述和图片URL
- 提供简洁的REST API接口
- 支持直接从HTML样例中提取元数据
- 支持调试模式查看源HTML

## 安装要求

- Python 3.8+
- FastAPI
- Uvicorn
- Requests
- BeautifulSoup4

## 安装方法

1. 克隆仓库或下载代码

2. 安装依赖包：
   ```
   pip install -r requirements.txt
   ```

## 使用方法

1. 启动API服务器：
   ```
   python xhs_metadata_api.py
   ```
   
   或者使用uvicorn：
   ```
   uvicorn xhs_metadata_api:app --reload
   ```

2. API服务器将在 `http://localhost:8080` 上运行

3. 访问API文档：
   打开浏览器访问 `http://localhost:8080/docs` 查看交互式API文档

## API接口

### POST /extract/

从分享文本中提取小红书链接，然后获取元数据

**请求体：**
```json
{
  "input_text": "34 拓麻慧子发布了一篇小红书笔记，快来看吧！ 😆 tnk9IKuwcqYQnJK 😆 http://xhslink.com/a/IGTNc5Db7WEab，复制本条信息，打开【小红书】App查看精彩内容！",
  "debug": false
}
```

**响应：**
```json
{
  "title": "在东京随地大小NewJeans - 小红书",
  "description": "走到哪里看到哪里拍到哪里🫰🏻 还买到我们海粼宝宝的口香糖 幸福🫰🏻🫰🏻 \t #newjeans #东京 #haerin",
  "image_urls": [
    "http://sns-webpic-qc.xhscdn.com/202504201457/09df8e8378a94bc6b0800fde25b62991/1040g2sg314m097hp6g705p9j9o7aj4jb75acl70!nd_dft_wlteh_webp_3",
    "http://sns-webpic-qc.xhscdn.com/202504201457/411d38c203c5ae564fde9471ac425e58/1040g2sg314m097hp6g7g5p9j9o7aj4jbicutmn0!nd_dft_wlteh_webp_3",
    "http://sns-webpic-qc.xhscdn.com/202504201457/cecc0f0755aa1bbc51bdf1dea0d0d51d/1040g2sg314m097hp6g805p9j9o7aj4jbd08bsvg!nd_dft_wlteh_webp_3"
  ],
  "original_url": "http://xhslink.com/a/IGTNc5Db7WEab",
  "extracted_url": "https://www.xiaohongshu.com/explore/66815879000000001c02a2d7",
  "html_source": "..." // 仅在debug=true时返回
}
```

### POST /extract_from_html/

直接从HTML样例中提取元数据

**请求体：**
```json
{
  "html_sample": "<meta name=\"description\" content=\"走到哪里看到哪里拍到哪里🫰🏻 还买到我们海粼宝宝的口香糖 幸福🫰🏻🫰🏻 \t #newjeans #东京 #haerin\">\n<meta name=\"og:type\" content=\"article\">\n<meta name=\"og:site_name\" content=\"小红书\">\n<meta name=\"og:title\" content=\"在东京随地大小NewJeans - 小红书\">\n<meta name=\"og:image\" content=\"http://sns-webpic-qc.xhscdn.com/202504201457/09df8e8378a94bc6b0800fde25b62991/1040g2sg314m097hp6g705p9j9o7aj4jb75acl70!nd_dft_wlteh_webp_3\">\n<meta name=\"og:image\" content=\"http://sns-webpic-qc.xhscdn.com/202504201457/411d38c203c5ae564fde9471ac425e58/1040g2sg314m097hp6g7g5p9j9o7aj4jbicutmn0!nd_dft_wlteh_webp_3\">\n<meta name=\"og:image\" content=\"http://sns-webpic-qc.xhscdn.com/202504201457/cecc0f0755aa1bbc51bdf1dea0d0d51d/1040g2sg314m097hp6g805p9j9o7aj4jbd08bsvg!nd_dft_wlteh_webp_3\">\n<meta name=\"og:url\" content=\"https://www.xiaohongshu.com/explore/66815879000000001c02a2d7\">"
}
```

**响应：**
```json
{
  "title": "在东京随地大小NewJeans - 小红书",
  "description": "走到哪里看到哪里拍到哪里🫰🏻 还买到我们海粼宝宝的口香糖 幸福🫰🏻🫰🏻 \t #newjeans #东京 #haerin",
  "image_urls": [
    "http://sns-webpic-qc.xhscdn.com/202504201457/09df8e8378a94bc6b0800fde25b62991/1040g2sg314m097hp6g705p9j9o7aj4jb75acl70!nd_dft_wlteh_webp_3",
    "http://sns-webpic-qc.xhscdn.com/202504201457/411d38c203c5ae564fde9471ac425e58/1040g2sg314m097hp6g7g5p9j9o7aj4jbicutmn0!nd_dft_wlteh_webp_3",
    "http://sns-webpic-qc.xhscdn.com/202504201457/cecc0f0755aa1bbc51bdf1dea0d0d51d/1040g2sg314m097hp6g805p9j9o7aj4jbd08bsvg!nd_dft_wlteh_webp_3"
  ],
  "original_url": "",
  "extracted_url": ""
}
```

## 测试

使用提供的测试脚本测试API：
```
python test_xhs_metadata.py    # 测试链接提取
python test_html_api.py        # 测试HTML样例提取
python test_html_sample.py     # 测试直接从HTML提取 (不使用API)
```

## 调试模式

启用调试模式可以在响应中获取HTML源码：
```json
{
  "input_text": "...",
  "debug": true
}
```

## 注意事项

- 该API需要网络连接才能访问小红书网站
- 小红书可能会有反爬虫措施，频繁使用可能导致IP被临时限制
- 请遵守小红书的使用条款和服务协议
- 仅用于学习和研究目的，请勿用于商业用途

## 许可证

MIT 