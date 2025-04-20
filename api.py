from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import os
import threading
from typing import List, Optional
import time
import json
import re

# 导入原脚本中的爬虫类
from xiaohongshu_scraper import XiaohongshuScraper, extract_xiaohongshu_url

app = FastAPI(
    title="小红书内容抓取API",
    description="基于Selenium的小红书内容抓取API，支持抓取帖子内容和图片",
    version="1.0.0"
)

# 创建一个全局的爬虫实例和锁，确保多个请求之间不会冲突
scraper = None
scraper_lock = threading.Lock()

# 定义请求模型
class ScrapeRequest(BaseModel):
    url: str = Field(..., description="小红书帖子URL或分享文本")
    save_to_json: bool = Field(False, description="是否保存元数据到JSON文件")

# 定义响应模型
class ImageInfo(BaseModel):
    url: str
    local_path: Optional[str] = None

class ScrapeResponse(BaseModel):
    title: str
    content: str
    image_count: int
    image_info: List[ImageInfo]
    output_directory: Optional[str] = None
    success: bool
    message: str

# 初始化爬虫
def init_scraper():
    global scraper
    if scraper is None:
        with scraper_lock:
            if scraper is None:  # 双重检查锁定
                scraper = XiaohongshuScraper()
                # 创建主输出目录
                os.makedirs('xiaohongshu_posts', exist_ok=True)

# 启动时初始化
@app.on_event("startup")
def startup_event():
    init_scraper()

# 关闭时清理资源
@app.on_event("shutdown")
def shutdown_event():
    global scraper
    if scraper:
        scraper.close()

# 健康检查端点
@app.get("/health")
def health_check():
    return {"status": "ok"}

# 提取URL的辅助函数
def process_url(url_text):
    # 如果是分享文本，提取URL
    extracted_url = extract_xiaohongshu_url(url_text)
    if extracted_url:
        return extracted_url
    # 如果是直接URL，检查并格式化
    if not url_text.startswith('http'):
        return 'https://' + url_text
    return url_text

# 抓取内容端点
@app.post("/scrape", response_model=ScrapeResponse)
async def scrape_post(request: ScrapeRequest, background_tasks: BackgroundTasks):
    init_scraper()  # 确保爬虫已初始化
    
    try:
        # 处理URL
        url = process_url(request.url)
        if not url:
            raise HTTPException(status_code=400, detail="无效的URL或分享文本")
        
        # 获取锁以确保同一时间只有一个请求在使用爬虫
        with scraper_lock:
            # 执行抓取
            result = scraper.scrape_post(url)
            
            if not result:
                return ScrapeResponse(
                    title="",
                    content="",
                    image_count=0,
                    image_info=[],
                    success=False,
                    message="抓取失败，请检查URL是否有效或尝试重新登录"
                )
            
            # 构建图片信息
            image_info = []
            for i, (img_url, local_path) in enumerate(zip(result['image_urls'], result.get('downloaded_files', []))):
                image_info.append(ImageInfo(url=img_url, local_path=local_path))
            
            # 如果请求中指定了保存JSON，则在后台保存
            if request.save_to_json:
                background_tasks.add_task(save_to_json, result)
            
            return ScrapeResponse(
                title=result['title'],
                content=result['content'],
                image_count=len(result['image_urls']),
                image_info=image_info,
                output_directory=result.get('output_dir', ''),
                success=True,
                message="抓取成功"
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"抓取过程中出错: {str(e)}")

# 后台保存JSON文件
def save_to_json(data, filename='xiaohongshu_content.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"保存文件时出错: {e}")

# 登录端点
@app.post("/login")
async def login():
    init_scraper()  # 确保爬虫已初始化
    
    try:
        with scraper_lock:
            success = scraper.login()
            if success:
                return {"success": True, "message": "登录成功"}
            else:
                return {"success": False, "message": "登录失败，请重试"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"登录过程中出错: {str(e)}")

# 主程序入口
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True) 