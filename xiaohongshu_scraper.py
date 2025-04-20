from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import random
import os
import requests
from urllib.parse import urlparse
import re

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
    pattern = r'http://xhslink\.com/a/[a-zA-Z0-9]+'
    match = re.search(pattern, input_text)
    
    if match:
        url = match.group(0)
        print(f"已提取URL: {url}")
        return url
        
    # 如果没有找到URL，提示用户
    print("警告：未能从输入文本中提取到有效的小红书链接")
    return None

class XiaohongshuScraper:
    def __init__(self):
        """初始化Selenium WebDriver"""
        self.setup_driver()
        self.is_logged_in = False
        
    def setup_driver(self):
        """设置Chrome浏览器选项"""
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 无头模式，如果不需要看到浏览器界面可以取消注释
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        
        # 添加更真实的浏览器特征
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 设置中文语言
        chrome_options.add_argument('--lang=zh-CN')
        
        # 初始化WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 设置等待时间
        self.wait = WebDriverWait(self.driver, 20)  # 增加等待时间到20秒
        
    def create_output_directory(self, title):
        """创建输出目录"""
        # 清理标题，移除非法字符
        clean_title = re.sub(r'[<>:"/\\|?*]', '_', title)
        # 限制标题长度
        clean_title = clean_title[:50]
        
        # 创建输出目录
        output_dir = os.path.join('xiaohongshu_posts', clean_title)
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
        
    def download_image(self, url, output_dir, index):
        """下载单张图片"""
        try:
            # 获取文件扩展名
            parsed_url = urlparse(url)
            path = parsed_url.path
            ext = os.path.splitext(path)[1]
            if not ext:
                ext = '.jpg'  # 默认扩展名
                
            # 构建文件名
            filename = f"{index:03d}{ext}"
            filepath = os.path.join(output_dir, filename)
            
            # 下载图片
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        
            print(f"已下载图片: {filename}")
            return filepath
            
        except Exception as e:
            print(f"下载图片失败: {url}, 错误: {str(e)}")
            return None
            
    def download_images(self, image_urls, output_dir):
        """下载所有图片"""
        downloaded_files = []
        for i, url in enumerate(image_urls, 1):
            filepath = self.download_image(url, output_dir, i)
            if filepath:
                downloaded_files.append(filepath)
        return downloaded_files
        
    def login(self):
        """登录小红书"""
        if self.is_logged_in:
            return True
            
        try:
            print("\n请登录小红书...")
            self.driver.get('https://www.xiaohongshu.com')
            
            # 等待用户手动登录 - 在API中这需要用户通过浏览器手动登录
            print("等待小红书网站加载，请稍后...")
            time.sleep(5)
            
            # 检查是否有登录按钮
            try:
                # 判断是否已经登录
                if "用户登录" in self.driver.page_source or "登录" in self.driver.page_source:
                    print("请在浏览器中手动登录，此处API需要单独处理登录流程")
                    return False
                else:
                    # 已经登录成功
                    self.is_logged_in = True
                    print("登录成功！")
                    
                    # 保存cookies
                    cookies = self.driver.get_cookies()
                    with open('xiaohongshu_cookies.json', 'w') as f:
                        json.dump(cookies, f)
                    
                    return True
            except Exception as e:
                print(f"检查登录状态时出错: {str(e)}")
                return False
            
        except Exception as e:
            print(f"登录过程中出错: {str(e)}")
            return False
            
    def load_cookies(self):
        """加载已保存的cookies"""
        try:
            if os.path.exists('xiaohongshu_cookies.json'):
                with open('xiaohongshu_cookies.json', 'r') as f:
                    cookies = json.load(f)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                return True
        except Exception as e:
            print(f"加载cookies时出错: {str(e)}")
        return False
        
    def scrape_post(self, url):
        """
        抓取小红书帖子内容
        
        Args:
            url (str): 小红书帖子URL
            
        Returns:
            dict: 包含标题、内容和图片URL的字典
        """
        try:
            if not self.is_logged_in:
                # 尝试加载已保存的cookies
                if not self.load_cookies():
                    if not self.login():
                        return None
            
            print("正在加载页面...")
            self.driver.get(url)
            
            # 等待页面加载
            time.sleep(random.uniform(3, 5))
            
            # 等待内容加载完成
            print("等待内容加载...")
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # 滚动页面以加载更多内容
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # 获取页面内容
            print("提取内容...")
            
            try:
                # 尝试获取标题
                title_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.title, .title")))
                title = title_element.text
            except:
                title = "未找到标题"
                print("警告：未找到标题")
            
            try:
                # 尝试获取正文内容
                content_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".content, .desc")))
                content = content_element.text
            except:
                content = "未找到内容"
                print("警告：未找到正文内容")
            
            # 获取图片URL
            image_urls = []
            try:
                # 等待图片元素加载
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[src*='http']")))
                images = self.driver.find_elements(By.CSS_SELECTOR, "img[src*='http']")
                for img in images:
                    src = img.get_attribute('src')
                    if src and not src.startswith('data:'):
                        image_urls.append(src)
            except:
                print("警告：提取图片URL时出错")
            
            # 创建输出目录并下载图片
            output_dir = self.create_output_directory(title)
            downloaded_files = self.download_images(image_urls, output_dir)
            
            return {
                'title': title,
                'content': content,
                'image_urls': image_urls,
                'downloaded_files': downloaded_files,
                'output_dir': output_dir
            }
            
        except TimeoutException:
            print("错误：页面加载超时")
            return None
        except Exception as e:
            print(f"错误：抓取过程中出现异常: {str(e)}")
            return None
            
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()

def save_to_file(data, filename='xiaohongshu_content.json'):
    """将抓取的数据保存到JSON文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"数据已保存到 {filename}")
    except Exception as e:
        print(f"保存文件时出错: {e}") 