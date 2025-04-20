import re

def test_html_sample():
    """测试从HTML样例中直接提取元数据"""
    
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
    
    print("开始测试HTML样例提取...")
    
    # 提取标题
    title = ""
    title_pattern = r'<meta\s+name="og:title"\s+content="([^"]+)"'
    title_match = re.search(title_pattern, html_sample)
    if title_match:
        title = title_match.group(1)
        print(f"提取到标题: {title}")
    else:
        print("未能提取到标题")
    
    # 提取描述
    description = ""
    desc_pattern = r'<meta\s+name="description"\s+content="([^"]+)"'
    desc_match = re.search(desc_pattern, html_sample)
    if desc_match:
        description = desc_match.group(1)
        print(f"提取到描述: {description}")
    else:
        print("未能提取到描述")
    
    # 提取图片URL
    image_urls = []
    image_pattern = r'<meta\s+name="og:image"\s+content="([^"]+)"'
    image_matches = re.findall(image_pattern, html_sample)
    if image_matches:
        for img_url in image_matches:
            image_urls.append(img_url)
        print(f"提取到图片URL数量: {len(image_urls)}")
        for i, url in enumerate(image_urls, 1):
            print(f"{i}. {url}")
    else:
        print("未能提取到图片URL")
    
    # 测试不同的正则表达式
    print("\n尝试更灵活的正则表达式模式...")
    
    # 更灵活的标题提取 (name或property属性)
    flexible_title_pattern = r'<meta\s+(?:name|property)="og:title"\s+content="([^"]+)"'
    flexible_title_match = re.search(flexible_title_pattern, html_sample)
    if flexible_title_match:
        print(f"灵活模式提取到标题: {flexible_title_match.group(1)}")
    
    # 更灵活的图片URL提取 (name或property属性)
    flexible_image_pattern = r'<meta\s+(?:name|property)="og:image"\s+content="([^"]+)"'
    flexible_image_matches = re.findall(flexible_image_pattern, html_sample)
    if flexible_image_matches:
        print(f"灵活模式提取到图片URL数量: {len(flexible_image_matches)}")
    
    # 顺序无关的属性匹配模式
    print("\n尝试顺序无关的属性匹配模式...")
    order_insensitive_title = r'<meta\s+[^>]*?(?:name|property)="og:title"[^>]*?content="([^"]+)"'
    order_match = re.search(order_insensitive_title, html_sample)
    if order_match:
        print(f"顺序无关模式提取到标题: {order_match.group(1)}")
    
    order_insensitive_image = r'<meta\s+[^>]*?(?:name|property)="og:image"[^>]*?content="([^"]+)"'
    order_image_matches = re.findall(order_insensitive_image, html_sample)
    if order_image_matches:
        print(f"顺序无关模式提取到图片URL数量: {len(order_image_matches)}")

if __name__ == "__main__":
    test_html_sample() 