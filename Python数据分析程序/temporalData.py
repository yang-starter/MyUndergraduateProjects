import matplotlib.pyplot as plt
import csv
import college
import numpy as np

nycCounty = ['Bronx', 'Brooklyn', 'New York', 'Queens', 'Staten Island']
nycCounty2 = ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']
nycCountyB = ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']

numShootingCounty = [0, 0, 0, 0, 0]
shootingData = college.csvRead('E://NYPD Shooting Incident Data (Historic).csv')

# numShootingCountyper = [0, 0, 0, 0, 0]
# for item in shootingData:
#     for i in range(0, 5):
#         if item['BORO'] == nycCountyB[i]:
#             numShootingCounty[i] += 1
# for i in range(0, 5):
#     numShootingCountyper[i] = 100 * numShootingCounty[i] / sum(numShootingCounty)
# print(numShootingCountyper)

# -------------------------------------------------------------------------------

# 以下是年龄百分比

# -------------------------------------------------------------------------------
# agelist = ['<18', '18-24', '25-44', '45-64', '65+']
# numage = [0, 0, 0, 0, 0]
# numageper = [0, 0, 0, 0, 0]
# for item in shootingData:
#     for i in range(0, 5):
#         if item['PERP_AGE_GROUP'] == agelist[i]:
#             numage[i] += 1
# for i in range(0, 5):
#     numageper[i] = 100 * numage[i] / sum(numage)
#
# print(agelist)
# print(numageper)


# -------------------------------------------------------------------------------

# 以下是种族百分比

# -------------------------------------------------------------------------------

# racelist = ['BLACK', 'WHITE HISPANIC', 'BLACK HISPANIC', 'WHITE', 'ASIAN / PACIFIC ISLANDER',
#             'AMERICAN INDIAN/ALASKAN NATIVE']
# racenum = [0, 0, 0, 0, 0, 0]
# raceRate = [0, 0, 0, 0, 0, 0]
# # 获取种族列表
# # for item in shootingData:
# #     if item['PERP_RACE'] != '':
# #         if item['PERP_RACE'] not in racelist:
# #             racelist.append(item['PERP_RACE'])
# # print(racelist)
# for item in shootingData:
#     for i in range(0, 6):
#         if item['PERP_RACE'] == racelist[i]:
#             racenum[i] += 1
# for i in range(0, 6):
#     raceRate[i] = 100 * racenum[i] / sum(racenum)
#
# X = np.arange(6)
# plt.bar(X, raceRate,tick_label=racelist, fc='b', width=0.3, label='age')
# plt.title('percent of race')
# plt.legend()
# plt.plot(X, raceRate, color='b', linestyle='--')
# plt.show()


# -------------------------------------------------------------------------------

# 以下是生成高德可视化文件

# -------------------------------------------------------------------------------
# with open('NYPD.csv', 'w', encoding='utf-8') as fw:
#     fw.write('BORO' + ',' + '经纬度' + '\n')
#     for item in shootingData:
#         if item['OCCUR_DATE'][8] == '2' and item['OCCUR_DATE'][9] == '0':
#             string = item['BORO'] + ',' + '"' + item['Longitude'] + ',' + item['Latitude'] + '"'
#             fw.write(string)
#             fw.write('\n')

# -------------------------------------------------------------------------------

# 绘制区位案件按照年份的变化图

# -------------------------------------------------------------------------------

change = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# bronx = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# brooklyn = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# manhattan = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# queens = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# statenisland = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# for i in range(0, 9):
#     for item in shootingData:
#         for j in range(0, 5):
#             if item['OCCUR_DATE'][8] == '1' and item['OCCUR_DATE'][9] == str(i + 1):
#                 if item['BORO'] == nycCountyB[j]:
#                     change[j][i] += 1
# for item in shootingData:
#     for j in range(0, 5):
#         if item['OCCUR_DATE'][8] == '2' and item['OCCUR_DATE'][9] == '0':
#             if item['BORO'] == nycCountyB[j]:
#                 change[j][9] += 1
#
# print(change)
# yearlist = []
# for i in range(2011, 2021):
#     yearlist.append(i)
#
# X = np.arange(10)
# bronx = change[0]
# brooklyn = change[1]
# manhatten = change[2]
# queens = change[3]
# statenisland = change[4]
#
#
# plt.figure(figsize=[10, 5])
# plt.title('Numbers Changing')

# -----------------------------------
# 以下是生成一幅图中的五条曲线
# -----------------------------------
# plt.plot(yearlist, bronx)
# plt.plot(yearlist, brooklyn)
# plt.plot(yearlist, manhatten)
# plt.plot(yearlist, queens)
# plt.plot(yearlist, statenisland)

# -----------------------------------
# 以下是生成五幅图五条曲线，在此处更加清晰
# 12至13、15至16枪击案显著下降，19至20枪击案数量显著上升
# -----------------------------------
# plt.subplot(231);
# plt.plot(yearlist, bronx)
# plt.title('BRONX')
# plt.xlabel('Year')
# plt.ylabel('number')
# plt.subplot(232);
# plt.plot(yearlist, brooklyn)
# plt.title('BROOKLYN')
# plt.xlabel('Year')
# plt.ylabel('number')
# plt.subplot(233);
# plt.plot(yearlist, manhatten)
# plt.title('MANHATTEN')
# plt.xlabel('Year')
# plt.ylabel('number')
# plt.subplot(234);
# plt.plot(yearlist, queens)
# plt.title('QUEENS')
# plt.xlabel('Year')
# plt.ylabel('number')
# plt.subplot(235);
# plt.plot(yearlist, statenisland)
# plt.title('STATEN ISLAND')
# plt.xlabel('Year')
# plt.ylabel('number')
# plt.show()
# X = np.arange(5)
# # X2 = [i + 0.3 for i in X]
# #
# plt.bar(X, numageper, tick_label=agelist, fc='b', width=0.3, label='age')
# # plt.bar(X2, collegeper, fc='r', width=0.3, label='college')
# plt.title('percent of age')
# plt.xlabel('age')
# plt.ylabel('percent')
# plt.legend()
# # plt.text(X, numageper,numageper,ha='left')
# plt.plot(X, numageper, color='b', linestyle='--')
# # plt.plot(X2, collegeper,color='r',linestyle='--')
# plt.show()
