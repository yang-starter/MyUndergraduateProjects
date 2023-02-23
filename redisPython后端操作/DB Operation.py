from setting import data, photo, host, port
import redis
import xlrd
import os

book = xlrd.open_workbook(data)
redis_conn = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True, charset='UTF-8',
                         encoding='UTF-8')
sheet = book.sheet_by_index(0)  # 打开第1个sheet

file = os.listdir(photo)


# 查找操作：根据地名查询是否含有图片信息
def find_files(find_file):
    end_file = "jpg"
    for f in file:
        if find_file in f and f.endswith(end_file):
            if f:
                return f
            else:
                f = "none"
            return f


# 入库操作，并根据查找操作生成相关图片的链接
for i in range(1, sheet.nrows):
    keys = find_files(str(sheet.cell(i, 1).value))
    if str(keys) == "None":
        imgLink = "none"
    else:
        imgLink = host + ":" + port + "/photo/" + str(keys)

    redis_conn.lpush(sheet.cell(i, 0).value, sheet.cell(i, 1).value, sheet.cell(i, 2).value,
                     sheet.cell(i, 3).value,
                     sheet.cell(i, 4).value, sheet.cell(i, 5).value,
                     sheet.cell(i, 6).value, sheet.cell(i, 7).value, sheet.cell(i, 8).value,
                     sheet.cell(i, 9).value, sheet.cell(i, 10).value, imgLink)
