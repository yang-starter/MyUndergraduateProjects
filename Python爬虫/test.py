import urllib.request
from bs4 import BeautifulSoup
import re
import xlwt

findlink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'img.*src="(.*?)"', re.S)  # re.S让换行符包含在字符中
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*) </p>', re.S)


def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"}
    request = urllib.request.Request(url, headers=head)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except Exception as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = askURL(url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_="item"):
            data = []
            # print(item)
            item = str(item)
            link = re.findall(findlink, item)[0]
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle, item)
            if len(titles) == 2:
                ctitle = titles[0]
                data.append(ctitle)
                etitle = titles[1].replace("/", "")  # 去掉无关符号
                data.append(etitle)
            else:
                data.append(titles[0])
                data.append(" ")  # 留空
            rating = re.findall(findRating, item)[0]
            data.append(rating)
            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)
            bd = re.sub("/", " ", bd)
            data.append(bd.strip())  # 去掉前后空格

            datalist.append(data)

    # print(datalist)

    # print(link)
    return datalist


def saveData(datalist, savepath):
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    worksheet = workbook.add_sheet('movies', cell_overwrite_ok=True)
    col = ('电影链接', '图片链接', '影片中文名', '影片外文名', '评分', '评价数', '概况', '相关信息')
    for i in range(0, 8):
        worksheet.write(0, i, col[i])
    for i in range(0, 250):
        print("number %d" % i)
        data = datalist[i]
        for j in range(0, 8):
            worksheet.write(i+1, j, data[j])
    workbook.save(savepath)



baseurl = "https://movie.douban.com/top250?start="
#   savepath=".\\doubanmovie.xls"
getData(baseurl)
saveData(datalist=getData(baseurl), savepath='DoubanMovies.xls')