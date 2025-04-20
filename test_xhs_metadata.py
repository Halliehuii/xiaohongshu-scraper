import requests
import json

def test_extract_metadata(debug=True):
    """测试小红书元数据提取API"""
    
    # 测试输入文本
    input_text = "34 拓麻慧子发布了一篇小红书笔记，快来看吧！ 😆 tnk9IKuwcqYQnJK 😆 http://xhslink.com/a/IGTNc5Db7WEab，复制本条信息，打开【小红书】App查看精彩内容！"
    
    # 发送请求到API
    print("发送请求到API...")
    try:
        response = requests.post(
            "http://localhost:8080/extract/",
            json={"input_text": input_text, "debug": debug}
        )
        
        # 检查响应状态
        if response.status_code == 200:
            result = response.json()
            print("\n提取成功！结果如下:\n")
            print(f"标题: {result['title']}")
            print(f"描述: {result['description']}")
            print(f"图片URL数量: {len(result['image_urls'])}")
            
            print("\n图片URL列表:")
            for i, url in enumerate(result['image_urls'], 1):
                print(f"{i}. {url}")
                
            print(f"\n原始URL: {result['original_url']}")
            print(f"最终URL: {result['extracted_url']}")
            
            # 如果调试模式开启，展示部分HTML源码
            if debug and 'html_source' in result:
                html_preview = result['html_source'][:1000] + "..." if len(result['html_source']) > 1000 else result['html_source']
                print("\n部分HTML源码预览:")
                print("-" * 80)
                print(html_preview)
                print("-" * 80)
                
                # 尝试从源码中查找元数据标签
                print("\n直接从HTML源码查找元数据标签:")
                html = result['html_source']
                
                # 查找og:title
                import re
                og_title_tags = re.findall(r'<meta[^>]*?property="og:title"[^>]*?>', html)
                if og_title_tags:
                    print("\nog:title标签:")
                    for tag in og_title_tags:
                        print(tag)
                
                # 查找描述
                desc_tags = re.findall(r'<meta[^>]*?name="description"[^>]*?>', html)
                if desc_tags:
                    print("\ndescription标签:")
                    for tag in desc_tags:
                        print(tag)
                
                # 查找og:image
                og_image_tags = re.findall(r'<meta[^>]*?property="og:image"[^>]*?>', html)
                if og_image_tags:
                    print("\nog:image标签:")
                    for tag in og_image_tags:
                        print(tag)
                
        else:
            print(f"错误: {response.status_code}")
            print(response.json())
    
    except Exception as e:
        print(f"测试过程中出错: {str(e)}")

if __name__ == "__main__":
    test_extract_metadata(debug=True) 