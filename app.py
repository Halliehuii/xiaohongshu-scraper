from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import json
from typing import List, Optional
from xiaohongshu_scraper import XiaohongshuScraper, extract_xiaohongshu_url

app = FastAPI(title="小红书内容抓取API", description="抓取小红书帖子内容的API")

# 创建主输出目录
os.makedirs('xiaohongshu_posts', exist_ok=True)

# 全局变量存储scraper实例
scraper = None

class ScrapeRequest(BaseModel):
    url: str
    save_metadata: bool = False

class ScrapeResponse(BaseModel):
    title: str
    content: str
    image_urls: List[str]
    downloaded_files: List[str]
    output_dir: str
    saved_metadata_path: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    global scraper
    scraper = XiaohongshuScraper()
    print("启动浏览器...")

@app.on_event("shutdown")
async def shutdown_event():
    global scraper
    if scraper:
        scraper.close()
        print("浏览器已关闭")

def save_to_file(data, filename='xiaohongshu_content.json'):
    """将抓取的数据保存到JSON文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return filename
    except Exception as e:
        print(f"保存文件时出错: {e}")
        return None

@app.post("/scrape/", response_model=ScrapeResponse)
async def scrape_post(request: ScrapeRequest, background_tasks: BackgroundTasks):
    global scraper
    
    if not scraper:
        raise HTTPException(status_code=500, detail="Scraper未初始化")
    
    # 尝试提取URL
    url = request.url
    extracted_url = extract_xiaohongshu_url(url)
    if extracted_url:
        url = extracted_url
    elif not url.startswith('http'):
        url = 'https://' + url
    
    print(f"开始抓取内容: {url}")
    result = scraper.scrape_post(url)
    
    if not result:
        raise HTTPException(status_code=404, detail="无法抓取内容，请检查URL是否正确")
    
    response = ScrapeResponse(
        title=result['title'],
        content=result['content'],
        image_urls=result['image_urls'],
        downloaded_files=result['downloaded_files'],
        output_dir=result['output_dir']
    )
    
    if request.save_metadata:
        metadata_path = save_to_file(result)
        if metadata_path:
            response.saved_metadata_path = metadata_path
    
    return response

@app.post("/login/")
async def login():
    global scraper
    
    if not scraper:
        raise HTTPException(status_code=500, detail="Scraper未初始化")
    
    success = scraper.login()
    if not success:
        raise HTTPException(status_code=401, detail="登录失败")
    
    return {"message": "登录成功"}

@app.get("/")
async def read_root():
    return {"message": "小红书内容抓取API", "version": "1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 