import college
import matplotlib.pyplot as plt
import numpy as np
import csv
import re
import pandas as pd

nycCounty = ['Bronx', 'Brooklyn', 'New York', 'Queens', 'Staten Island']
nycCounty2 = ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']
nycCountyB = ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']

numShootingCounty = [0, 0, 0, 0, 0]
shootingData = college.csvRead('E://NYPD Shooting Incident Data (Historic).csv')

numShootingCountyper = [0, 0, 0, 0, 0]
for item in shootingData:
    for i in range(0, 5):
        if item['BORO'] == nycCountyB[i]:
            numShootingCounty[i] += 1
for i in range(0, 5):
    numShootingCountyper[i] = 100 * numShootingCounty[i] / sum(numShootingCounty)
# print(numShootingCountyper)
#
# print(numShootingCounty)
# with open('shooting20.csv', 'w', encoding='utf-8') as fw:
#     fw.write('BORO' + ',' + '时刻' + ',' + '经纬度' + '\n')
#     for item in shootingData:
#         if item['OCCUR_DATE'][8] == '2' and item['OCCUR_DATE'][9] == '0':
#             string = item['BORO'] + ',' + item['OCCUR_TIME'] + ',' + '"' + item['Longitude'] + ',' + item[
#                 'Latitude'] + '"'
#             fw.write(string)
#             fw.write('\n')
# ---------------------------------------------------------------------------------------

# 以下绘制了大学按区位分布的数量和区位的犯罪数量，并绘制了并列柱状图，结果是几乎无关联

# ---------------------------------------------------------------------------------------
# numCollege = [0, 0, 0, 0, 0]
# dictCollege = []
# collegeper = [0, 0, 0, 0, 0]
# with open('universities.csv', "r", encoding='utf-8') as fc:
#     reader = csv.DictReader(fc)
#     for row in reader:
#         dictCollege.append(row)
# fc.close()
#
# for item in dictCollege:
#     for i in range(0, 5):
#         if item['county'] == nycCounty[i]:
#             numCollege[i] += 1
# for i in range(0, 5):
#     collegeper[i] = 100 * numCollege[i] / sum(numCollege)
# print(collegeper)

#
# X = np.arange(5)
# X2 = [i + 0.3 for i in X]
#
# plt.bar(X, numShootingCountyper, tick_label=nycCounty, fc='b', width=0.3, label='shooting')
# plt.bar(X2, collegeper, fc='r', width=0.3, label='college')
# plt.title('percent of shooting and college')
# plt.xlabel('County')
# plt.ylabel('percent')
# plt.legend()
# plt.plot(X, numShootingCountyper, color='b', linestyle='--')
# plt.plot(X2, collegeper,color='r',linestyle='--')
# plt.show()


# ----------------------------------------------------------------------------------------

# 一下是黑人分布与枪击案的柱状图，有相关性

# ----------------------------------------------------------------------------------------

# dictBlack = []
# numBlack = [0, 0, 0, 0, 0]
# numBlackPer = [0, 0, 0, 0, 0]
# with open('E://nyc_census_tracts.csv', "r", encoding='utf-8') as fc:
#     reader = csv.DictReader(fc)
#     for row in reader:
#         dictBlack.append(row)
# fc.close()
#
# for item in dictBlack:
#     for i in range(0, 5):
#         if item['Borough'] == nycCounty2[i]:
#             num = item['Black']
#             if num != '':
#                 numBlack[i] += float(num)
#             # print(num)
# print(numBlack)
#
# for i in range(0, 5):
#     numBlackPer[i] = 100 * numBlack[i] / sum(numBlack)
#
# print(numBlackPer)
#
# X = np.arange(5)
# X2 = [i + 0.3 for i in X]
#
# plt.bar(X, numShootingCountyper, tick_label=nycCounty, fc='b', width=0.3, label='shooting')
# plt.bar(X2, numBlackPer, fc='r', width=0.3, label='black')
# plt.title('percent of shooting and black')
# plt.xlabel('County')
# plt.ylabel('percent')
# plt.legend()
# plt.plot(X, numShootingCountyper, color='b', linestyle='--')
# plt.plot(X2, numBlackPer,color='r',linestyle='--')
# plt.show()


# ----------------------------------------------------------------------------------------

# 以下是失业率分布与枪击案的柱状图，几乎没有相关性

# ----------------------------------------------------------------------------------------

# dictUnemployment = []
#
# with open('E://nyc_census_tracts.csv', "r", encoding='utf-8') as fc:
#     reader = csv.DictReader(fc)
#     for row in reader:
#         dictUnemployment.append(row)
# fc.close()
#
# numBlock = [0, 0, 0, 0, 0]
# unemploySum = [0, 0, 0, 0, 0]
# unemployAve = [0, 0, 0, 0, 0]
# for item in dictUnemployment:
#     for i in range(0, 5):
#         if item['Borough'] == nycCounty2[i]:
#             if item['Unemployment'] != '':
#                 numBlock[i] += 1
#                 unemploySum[i] += float(item['Unemployment'])
# for i in range(0, 5):
#     unemployAve[i] = unemploySum[i] / numBlock[i]
# print(unemployAve)
#
# mini = min(unemployAve)
# maxi = max(unemployAve)
#
# for i in range(0, 5):
#     unemployAve[i] = 40 * (unemployAve[i] - mini)/(maxi - mini)
#
# print(unemployAve)
#
# X = np.arange(5)
# X2 = [i + 0.3 for i in X]
# plt.bar(X, numShootingCountyper, tick_label=nycCounty, fc='b', width=0.3, label='shooting')
# plt.bar(X2, unemployAve, fc='r', width=0.3, label='min_max unemploy')
# plt.title('percent of shooting and unemployment')
# plt.xlabel('County')
# plt.ylabel('percent')
# plt.legend()
# plt.plot(X, numShootingCountyper, color='b', linestyle='--')
# plt.plot(X2, unemployAve,color='r',linestyle='--')
# plt.show()

haveRace = 0
numPerpblack = 0
numblack_black = 0
support1 = 0
confidence1 = 0

for item in shootingData:
    if item['PERP_RACE'] != '':
        haveRace += 1
    if item['PERP_RACE'] == 'WHITE HISPANIC':
        numPerpblack += 1
        if item['VIC_RACE'] == 'BLACK HISPANIC':
            numblack_black += 1

confidence1 = 100 * numblack_black / numPerpblack
support1 = 100 * numblack_black / haveRace

print('WHITE HISPANIC --> BLACK HISPANIC的支持度为 %s '%support1 + '%')
print('WHITE HISPANIC --> BLACK HISPANIC的置信度为 %s '%confidence1 + '%')




