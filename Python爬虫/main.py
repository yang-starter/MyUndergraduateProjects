import urllib.request
# # 向指定的url发送请求，并返回服务器响应的类文件对象
# response = urllib.request.urlopen("http://www.baidu.com")
# # 类文件对象支持 文件对象的操作方法，如read()方法读取文件全部内容，返回字符串
# html = response.read().decode("utf-8")
# # 打印字符串
# print(html)
import urllib.parse
# data=bytes(urllib.parse.urlencode({}),encoding="utf-8")
# response=urllib.request.urlopen("http://httpbin.org/post",data=data)
# print(response.read().decode("utf-8"))

# try:
#     response=urllib.request.urlopen("http://httpbin.org/get",timeout=0.01)
#     print(response.read().decode("utf-8"))
# except Exception as e:
#     print("time out!")

# response=urllib.request.urlopen("http://httpbin.org/get",timeout=1)
# print(response.status)

# response=urllib.request.urlopen("http://www.baidu.com")
# print(response.getheader("Server"))

# url="http://httpbin.org/post"
# headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"}
# data=bytes(urllib.parse.urlencode({}),encoding="utf-8")
# req=urllib.request.Request(url=url,data=data,headers=headers,method="POST")
# response=urllib.request.urlopen(req)
# print(response.read().decode("utf-8"))

# url="http://www.douban.com"
# headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"}
# req=urllib.request.Request(url=url,headers=headers)
# response=urllib.request.urlopen(req)
# print(response.read().decode("utf-8"))

# --------------------------------------------------------------------------
# def askURL(url):
#     head={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"}
#     request=urllib.request.Request(url,headers=head)
#     try:
#         response=urllib.request.urlopen(request)
#         html=response.read().decode("utf-8")
#         print(html)
#     except Exception as e:
#         if hasattr(e,"code"):
#             print(e.code)
#         if hasattr(e,"reason"):
#             print(e.reason)
#     return html
# baseurl="https://movie.douban.com/top250?start="
# askURL("https://movie.douban.com/top250?start=0")
# def getData(baseurl):
#     datalist=[]
#     for i in range(0,10):
#         url=baseurl+str(i*25)
#         html=askURL(url)

# --------------------------beautifulsoup-------------------------
# -Tag
# -NavigableString
# -BeautifulSoup
# -Comment

from bs4 import BeautifulSoup
import re

file = open("./bd.html", "rb")
html = file.read().decode("utf-8")
bs = BeautifulSoup(html, "html.parser")

# print(bs.a.attrs)
# print(bs.title.string)
# print(type(bs))
# print(bs.name)
# print(bs)
# print(bs.attrs)
# print(bs.a.string)

# ----------------------------------------------------------------------

# 文档遍历
# print(bs.head.contents)
# print(bs.head.contents[1])

# 文档搜索
# t_list=bs.find_all("a")
# print(t_list)
# t_list = bs.find_all(re.compile("a"))

# def is_name_exist(tag):
#     return tag.has_attr("name")
# t_list = bs.find_all(is_name_exist)
# for item in t_list:
#     print(item)

# t_list=bs.find_all(id="head")
# t_list=bs.find_all(class_=True)
#
# for item in t_list:
#     print(item)

# t_list = bs.find_all(text=re.compile("\d"))
# for item in t_list:
#     print(item)

# t_list = bs.find_all("a", limit=3)
# for item in t_list:
#     print(item)

# css选择器
# t_list=bs.select("title")   #标签
# t_list=bs.select(".mnav")    #类名
# t_list=bs.select("#u1")      #id
# t_list = bs.select("a[class]")  # 属性

# t_list = bs.select("head > title")  # 通过子标签查找
# for item in t_list:
#     print(item)
t_list = bs.select(".mnav ~ .bri")      # 兄弟标签
print(t_list[0].get_text())

# ----------------------------------xpath---------------------------------
# 实例化一个etree的对象，将被解析的页面源码数据加载到该对象中
# etree.parse(filepath)
# etree.HTML('page_text')
# 调用etree对象中的xpath方法结合xpath表达式实现标签的定位和内容的捕获
