import re
import json
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# 创建FastAPI实例
app = FastAPI(title="小红书元数据抓取API", description="从小红书链接中提取标题、描述和图片URL的API")

# 定义请求模型
class XHSLinkRequest(BaseModel):
    input_text: str

# 定义响应模型
class XHSMetadataResponse(BaseModel):
    title: str
    description: str
    image_urls: List[str]
    original_url: str
    extracted_url: str

# 定义HTML样例请求模型
class HTMLSampleRequest(BaseModel):
    html_sample: str

def extract_xiaohongshu_url(input_text):
    """
    从手机端复制的文本中提取小红书URL
    
    Args:
        input_text (str): 用户输入的文本，例如：
        "34 拓麻慧子发布了一篇小红书笔记，快来看吧！😆 tnk9IKuwcqYQnJK 😆 http://xhslink.com/a/IGTNc5Db7WEab"
        
    Returns:
        str: 提取出的URL，如果未找到则返回None
    """
    # 匹配 http://xhslink.com/a/ 开头的完整URL
    pattern = r'http://xhslink\.com/[a-zA-Z0-9/]+'
    match = re.search(pattern, input_text)
    
    if match:
        url = match.group(0)
        return url
        
    return None

def follow_redirect(short_url):
    """
    跟踪短链接的重定向，获取最终URL
    
    Args:
        short_url (str): 短链接URL
        
    Returns:
        str: 重定向后的最终URL
    """
    try:
        response = requests.head(short_url, allow_redirects=True)
        return response.url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"跟踪链接重定向失败: {str(e)}")

def extract_metadata(url, debug=False):
    """
    从小红书页面中提取元数据
    
    Args:
        url (str): 小红书帖子URL
        debug (bool): 是否返回HTML源码
        
    Returns:
        dict: 包含标题、描述和图片URL的字典
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # 保存HTML内容以便调试
        html_content = response.text
        print(f"获取到HTML内容，长度: {len(html_content)} 字节")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取标题 - 使用属性选择器
        title = ""
        # 尝试多种可能的选择器方式
        title_meta = soup.find('meta', attrs={'property': 'og:title'})
        if title_meta and title_meta.get('content'):
            title = title_meta.get('content')
            print(f"从BeautifulSoup提取到标题: {title}")
        
        # 提取描述
        description = ""
        desc_meta = soup.find('meta', attrs={'name': 'description'})
        if desc_meta and desc_meta.get('content'):
            description = desc_meta.get('content')
            print(f"从BeautifulSoup提取到描述: {description}")
        
        # 提取图片URL - 使用属性选择器
        image_urls = []
        image_metas = soup.find_all('meta', attrs={'property': 'og:image'})
        for img_meta in image_metas:
            if img_meta.get('content'):
                image_url = img_meta.get('content')
                if image_url not in image_urls:  # 避免重复
                    image_urls.append(image_url)
        
        if image_urls:
            print(f"从BeautifulSoup提取到图片URL数量: {len(image_urls)}")
        
        # 如果通过BeautifulSoup无法提取到元数据，尝试使用正则表达式直接从HTML内容提取
        if not title or not description or not image_urls:
            print("使用正则表达式从HTML中提取元数据...")
            
            # 提取标题
            title_match = re.search(r'<meta\s+(?:[^>]*?\s+)?property="og:title"(?:\s+[^>]*?)?content="([^"]*)"', html_content, re.IGNORECASE)
            if title_match and not title:
                title = title_match.group(1)
                print(f"通过正则表达式提取到标题: {title}")
            
            # 提取描述
            desc_match = re.search(r'<meta\s+(?:[^>]*?\s+)?name="description"(?:\s+[^>]*?)?content="([^"]*)"', html_content, re.IGNORECASE)
            if desc_match and not description:
                description = desc_match.group(1)
                print(f"通过正则表达式提取到描述: {description}")
            
            # 提取所有og:image标签
            image_matches = re.findall(r'<meta\s+(?:[^>]*?\s+)?property="og:image"(?:\s+[^>]*?)?content="([^"]*)"', html_content, re.IGNORECASE)
            if image_matches:
                for img_url in image_matches:
                    if img_url not in image_urls:
                        image_urls.append(img_url)
                print(f"通过正则表达式提取到图片URL数量: {len(image_urls)}")
        
        # 如果仍然无法提取到足够的元数据，尝试直接处理示例中的HTML代码
        if not title and "<meta name=\"og:title\"" in html_content or "<meta property=\"og:title\"" in html_content:
            print("尝试直接从HTML代码片段提取...")
            # 这种情况可能是用户直接提供了HTML代码片段而不是URL
            
            # 提取标题 - 直接字符串处理
            title_pattern = r'<meta (?:name|property)="og:title" content="([^"]*)">'
            title_match = re.search(title_pattern, html_content)
            if title_match:
                title = title_match.group(1)
                print(f"直接从HTML代码提取到标题: {title}")
            
            # 提取描述 - 直接字符串处理
            desc_pattern = r'<meta name="description" content="([^"]*)">'
            desc_match = re.search(desc_pattern, html_content)
            if desc_match:
                description = desc_match.group(1)
                print(f"直接从HTML代码提取到描述: {description}")
            
            # 提取图片 - 直接字符串处理
            image_pattern = r'<meta (?:name|property)="og:image" content="([^"]*)">'
            image_matches = re.findall(image_pattern, html_content)
            if image_matches:
                for img_url in image_matches:
                    if img_url not in image_urls:
                        image_urls.append(img_url)
                print(f"直接从HTML代码提取到图片URL数量: {len(image_urls)}")
        
        result = {
            'title': title,
            'description': description,
            'image_urls': image_urls
        }
        
        # 如果是调试模式，返回HTML源码
        if debug:
            result['html_source'] = html_content
            
        return result
        
    except Exception as e:
        print(f"提取元数据失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"提取元数据失败: {str(e)}")

@app.post("/extract/", response_model=XHSMetadataResponse)
async def extract_xiaohongshu_metadata(request: XHSLinkRequest):
    """
    从小红书链接中提取元数据
    
    从用户输入的文本中提取小红书链接，然后获取该链接的标题、描述和图片URL
    
    - **input_text**: 用户输入的文本，包含小红书分享链接
    
    返回:
    - **title**: 帖子标题
    - **description**: 帖子描述
    - **image_urls**: 图片URL列表
    - **original_url**: 原始短链接
    - **extracted_url**: 最终的链接
    """
    # 从输入文本中提取URL
    short_url = extract_xiaohongshu_url(request.input_text)
    if not short_url:
        raise HTTPException(status_code=400, detail="未能从输入文本中提取到有效的小红书链接")
    
    # 跟踪重定向获取最终URL
    final_url = follow_redirect(short_url)
    
    # 提取元数据
    metadata = extract_metadata(final_url)
    
    return XHSMetadataResponse(
        title=metadata['title'],
        description=metadata['description'],
        image_urls=metadata['image_urls'],
        original_url=short_url,
        extracted_url=final_url
    )

@app.post("/extract_from_html/", response_model=XHSMetadataResponse)
async def extract_from_html_sample(request: HTMLSampleRequest):
    """
    直接从HTML样例中提取元数据
    
    从用户提供的HTML代码样例中提取标题、描述和图片URL
    
    - **html_sample**: HTML代码样例，包含meta标签
    
    返回:
    - **title**: 帖子标题
    - **description**: 帖子描述
    - **image_urls**: 图片URL列表
    - **original_url**: 样例URL (空字符串)
    - **extracted_url**: 样例URL (空字符串)
    """
    html_content = request.html_sample
    
    print("从HTML样例中提取元数据...")
    
    # 提取标题
    title = ""
    title_pattern = r'<meta\s+[^>]*?(?:name|property)="og:title"[^>]*?content="([^"]+)"'
    title_match = re.search(title_pattern, html_content)
    if title_match:
        title = title_match.group(1)
        print(f"提取到标题: {title}")
    
    # 提取描述
    description = ""
    desc_pattern = r'<meta\s+[^>]*?name="description"[^>]*?content="([^"]+)"'
    desc_match = re.search(desc_pattern, html_content)
    if desc_match:
        description = desc_match.group(1)
        print(f"提取到描述: {description}")
    
    # 提取图片URL
    image_urls = []
    image_pattern = r'<meta\s+[^>]*?(?:name|property)="og:image"[^>]*?content="([^"]+)"'
    image_matches = re.findall(image_pattern, html_content)
    if image_matches:
        for img_url in image_matches:
            if img_url not in image_urls:
                image_urls.append(img_url)
        print(f"提取到图片URL数量: {len(image_urls)}")
    
    # 如果未能提取到信息，返回错误
    if not title and not description and not image_urls:
        raise HTTPException(status_code=400, detail="未能从HTML样例中提取到任何元数据")
    
    return XHSMetadataResponse(
        title=title,
        description=description,
        image_urls=image_urls,
        original_url="",
        extracted_url=""
    )

@app.get("/")
async def read_root():
    return {"message": "小红书元数据抓取API", "version": "1.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080) 