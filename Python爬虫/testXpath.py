import requests
from lxml import etree

# 爬取页面源码数据
url = 'https://liyang.58.com/ershoufang/'
head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}
page_text = requests.get(url=url, headers=head).text

tree = etree.HTML(page_text)
li_list = tree.xpath('//ul[@class="house-list-wrap"]/li')
fp = open('58.txt', 'w', encoding='utf-8')
for li in li_list:
    title = li.xpath('./div[2]/h2/a/text()')[0]
    print(title)
    fp.write(title+'\n')
