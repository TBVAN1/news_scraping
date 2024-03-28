import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

departments = ["基础学部", "未来技术学院", "计算学部", "团委", "本科生院", "国际合作部", "图书馆", "物理学院"]

current_time = datetime.now()
#默认保存到.py同目录
output_file = "news_output.txt"

# 定义一个函数来将时间差转换成易读格式
def format_timedelta(td):
    seconds = td.seconds
    days = td.days
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 0:
        return f"{days}天前"
    elif hours > 0:
        return f"{hours}小时前"
    elif minutes > 0:
        return f"{minutes}分钟前"
    else:
        return "刚刚"

with open(output_file, "w", encoding="utf-8") as file:
    for page_number in range(3):  # 执行3次翻页操作

        #这里更改自己学校的新闻发布页url
        url = f'http://today.hit.edu.cn/category/10?page={page_number}'
        
        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')

        # 选择所有的<li>标签 这里需要根据自己的页面结构更改选择的标签
        news_items = soup.find_all('li')

        for item in news_items:
            department_element = item.select_one('.pull-right a[hreflang="zh-hans"]')
            if department_element is not None:
                department = department_element.text.strip()
                if department in departments:
                    time_element = item.select_one('.date')
                    time_str = time_element.text.strip()
                    time_since_published = time_str

                    # 只保留发布时间在一天内的内容
                    if '天前' not in time_since_published:
                        title_element = item.select_one('.title a')
                        title = title_element.text.strip()
                        article_url = 'http://today.hit.edu.cn' + title_element['href']

                        file.write("部门: {}\n".format(department))
                        file.write("标题: {}\n".format(title))
                        file.write("发布时间: {}\n".format(time_since_published))
                        file.write("网址: {}\n".format(article_url))
                        file.write("\n")

print("输出结果已保存到文件:", output_file)
