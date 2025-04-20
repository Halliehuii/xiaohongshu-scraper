import requests
import json

def test_html_api():
    """测试从HTML样例中提取元数据的API"""
    
    # 用户提供的HTML样例
    html_sample = """
    <meta name="description" content="走到哪里看到哪里拍到哪里🫰🏻 还买到我们海粼宝宝的口香糖 幸福🫰🏻🫰🏻 	 #newjeans #东京 #haerin">
    <meta name="og:type" content="article">
    <meta name="og:site_name" content="小红书">
    <meta name="og:title" content="在东京随地大小NewJeans - 小红书">
    <meta name="og:image" content="http://sns-webpic-qc.xhscdn.com/202504201457/09df8e8378a94bc6b0800fde25b62991/1040g2sg314m097hp6g705p9j9o7aj4jb75acl70!nd_dft_wlteh_webp_3">
    <meta name="og:image" content="http://sns-webpic-qc.xhscdn.com/202504201457/411d38c203c5ae564fde9471ac425e58/1040g2sg314m097hp6g7g5p9j9o7aj4jbicutmn0!nd_dft_wlteh_webp_3">
    <meta name="og:image" content="http://sns-webpic-qc.xhscdn.com/202504201457/cecc0f0755aa1bbc51bdf1dea0d0d51d/1040g2sg314m097hp6g805p9j9o7aj4jbd08bsvg!nd_dft_wlteh_webp_3">
    <meta name="og:url" content="https://www.xiaohongshu.com/explore/66815879000000001c02a2d7">
    """
    
    # 发送请求到API
    print("发送请求到HTML提取API...")
    try:
        response = requests.post(
            "http://localhost:8080/extract_from_html/",
            json={"html_sample": html_sample}
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
        else:
            print(f"错误: {response.status_code}")
            print(response.json())
    
    except Exception as e:
        print(f"测试过程中出错: {str(e)}")

if __name__ == "__main__":
    test_html_api() 