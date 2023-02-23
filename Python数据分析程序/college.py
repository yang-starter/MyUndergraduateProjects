import csv
import re

dictionary = []  # 存储csv文件数据

def csvRead(filepath):
    # 读取csv文件
    with open(filepath, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dictionary.append(row)
    # print(dictionary)
    f.close()
    return dictionary


if __name__ == '__main__':
    dictUniversity = csvRead("E://COLLEGE_UNIVERSITY.csv")
    with open('universities.csv', 'w', encoding='utf-8') as fw:
        info = 'NAME' + ',' + 'county' + ',' + 'longitude' + ',' + 'latitude'
        fw.write(info)
        fw.write('\n')
        for item in dictUniversity:
            point = item['the_geom']
            name = item['NAME']
            name = name.replace(',', '-')
            fw.write(name + ',')
            fw.write(item['CITY'])
            fw.write(',')
            extr = re.findall(r"\d+\.?\d*", point)
            numberlon = extr[0]
            number1 = float(numberlon[0:])
            number1 = 0 - number1
            numberlat = extr[1]
            number2 = float(numberlat[0:])
            number2 = number2
            lon_lat = str(number1) + ',' + str(number2)
            fw.write(lon_lat)
            print(lon_lat)
            fw.write('\n')
    fw.close()




