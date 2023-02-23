import csv
import random
import pandas as pd

census = []
countyBlock = ['Bronx', 'Kings', 'New York', 'Queens', 'Richmond']

with open('census_block.csv', "r", encoding='utf-8') as fC:
    reader = csv.DictReader(fC)
    for row in reader:
        census.append(row)
# print(dictionary)
fC.close()

# with open('census_block.csv', 'w', encoding='utf-8') as fv:
#     for item in census:
#         for county in countyBlock:
#             if item['County'] == county:
#                 fv.write(item['County'] + ',' + item['Latitude'] + ',' + item['Longitude'])
#                 fv.write('\n')
# fv.close()

# shootingData = []
# with open('E://NYPD Shooting Incident Data (Historic).csv', "r", encoding='utf-8') as fn:
#     reader = csv.DictReader(fn)
#     for row in reader:
#         shootingData.append(row)
# fn.close()
#
censusLen = len(census)

indexlist11 = []
indexlist12 = []
indexlist13 = []
indexlist14 = []
indexlist15 = []
indexlist16 = []
indexlist17 = []
indexlist18 = []
indexlist19 = []
indexlist20 = []
dangerIndex = []
dangerWeight = []
difference = []
INTindexlist20 = []
for i in range(0, censusLen):
    dangerIndex.append(0)
    dangerWeight.append(0)
    difference.append(0)
    INTindexlist20.append(0)
#     indexlist20.append(0)
#     indexlist11.append(0)
#     indexlist12.append(0)
#     indexlist13.append(0)
#     indexlist14.append(0)
#     indexlist15.append(0)
#     indexlist16.append(0)
#     indexlist17.append(0)
#     indexlist18.append(0)
#     indexlist19.append(0)
with open('2011.csv', "r", encoding='utf-8') as f1:
    for row in f1:
        indexlist11.append(row)
f1.close()
with open('2012.csv', "r", encoding='utf-8') as f2:
    for row in f2:
        indexlist12.append(row)
f2.close()
with open('2013.csv', "r", encoding='utf-8') as f3:
    for row in f3:
        indexlist13.append(row)
f3.close()
with open('2014.csv', "r", encoding='utf-8') as f4:
    for row in f4:
        indexlist14.append(row)
f4.close()
with open('2015.csv', "r", encoding='utf-8') as f5:
    for row in f5:
        indexlist15.append(row)
f5.close()
with open('2016.csv', "r", encoding='utf-8') as f6:
    for row in f6:
        indexlist16.append(row)
f6.close()
with open('2017.csv', "r", encoding='utf-8') as f7:
    for row in f7:
        indexlist17.append(row)
f7.close()
with open('2018.csv', "r", encoding='utf-8') as f8:
    for row in f8:
        indexlist18.append(row)
f8.close()
with open('2019.csv', "r", encoding='utf-8') as f9:
    for row in f9:
        indexlist19.append(row)
f9.close()
with open('2020.csv', "r", encoding='utf-8') as f10:
    for row in f10:
        indexlist20.append(row)
f10.close()

# print(indexlist11[0])

p = 0.07929140462645867
for i in range(0, len(dangerIndex)):
    sumave = int(indexlist12[i]) + int(indexlist13[i]) \
             + int(indexlist14[i]) + int(indexlist15[i]) + int(indexlist16[i]) + int(indexlist17[i]) \
             + int(indexlist18[i]) + int(indexlist19[i]) + int(indexlist20[i])
    dangerIndex[i] = sumave / 9
    sumWeight = int(indexlist12[i]) * p * ((1 - p) ** 8) + int(indexlist13[i]) * p * ((1 - p) ** 7) + int(
        indexlist14[i]) * p * ((1 - p) ** 6) + int(indexlist15[i]) * p * ((1 - p) ** 5) + int(indexlist16[i]) * p * (
                            (1 - p) ** 4) + int(indexlist17[i]) * p * ((1 - p) ** 3) + int(indexlist18[i]) * p * (
                            (1 - p) ** 2) + int(indexlist19[i]) * p * (1 - p) + int(indexlist20[i]) * p

    dangerWeight[i] = sumWeight / (
                p * ((1 - p) ** 8) + p * ((1 - p) ** 7) + p * ((1 - p) ** 6) + p * ((1 - p) ** 5) + p * (
                    (1 - p) ** 4) + p * ((1 - p) ** 3) + p * ((1 - p) ** 2) + p * ((1 - p)) + p)

# ----------------------------------------------------------

# 下面生成的是生成最适合p值

# ----------------------------------------------------------

# for i in range(0, len(dangerIndex)):
#     sumave = int(indexlist11[i]) + int(indexlist12[i]) + int(indexlist13[i]) \
#              + int(indexlist14[i]) + int(indexlist15[i]) + int(indexlist16[i]) + int(indexlist17[i]) \
#              + int(indexlist18[i]) + int(indexlist19[i])
#     dangerIndex[i] = sumave / 9
#
#
# for i in range(0, len(indexlist20)):
#     INTindexlist20[i] = int(indexlist20[i])
# predictData = pd.Series(INTindexlist20)
#
# maxcorr = 0
# valueP = 0
# for j in range(0, 100):
#     p = random.random()
#     for i in range(0, len(dangerIndex)):
#         dangerWeight = int(indexlist11[i])*p*((1-p)**8) + int(indexlist12[i])*p*((1-p)**7) + int(indexlist13[i])*p*((1-p)**6) + int(indexlist14[i])*p*((1-p)**5) + int(indexlist15[i])*p*((1-p)**4) + int(indexlist16[i])*p*((1-p)**3) + int(indexlist17[i])*p*((1-p)**2) + int(indexlist18[i])*p*(1-p) + int(indexlist19[i])*p
#         dangerIndex[i] = dangerWeight / (p*((1-p)**8)+p*((1-p)**7)+p*((1-p)**6)+p*((1-p)**5)+p*((1-p)**4)+p*((1-p)**3)+p*((1-p)**2)+p*((1-p))+p)
#     testData = pd.Series(dangerIndex)
#     corr = round(predictData.corr(testData), 4)
#     if corr > maxcorr:
#         maxcorr = corr
#         valueP = p
# print(valueP)

for i in range(0, len(dangerIndex)):
    if dangerWeight[i] - dangerIndex[i] < 0:
        difference[i] = - 1000 * (dangerWeight[i] - dangerIndex[i])
        if difference[i] > 150:
            difference[i] = 200
    else:
        difference[i] = 0


# for i in range(0, len(dangerIndex)):
#     if dangerWeight[i] > 2:
#         dangerWeight[i] = 100



posi = 0
with open('prediction.csv', 'w', encoding='utf-8') as fp:
    fp.write('County,Latitude,Longitude,Average,Weight,Difference')
    fp.write('\n')
    for item in census:
        print(posi)
        string = item['County'] + ',' + item['Latitude'] + ',' + item['Longitude'] + ','
        fp.write(string)
        fp.write('%s' % dangerIndex[posi])
        fp.write(',')
        fp.write('%s' % dangerWeight[posi])
        fp.write(',')
        fp.write('%s' % difference[posi])
        fp.write('\n')
        posi += 1
fp.close()

# ----------------------------------------------------------

# 下面生成的是街区数据

# ----------------------------------------------------------
# for shot in shootingData:
#     dist = 0
#     mindist = 100
#     numindex = -1
#     if shot['OCCUR_DATE'][8] == '2' and shot['OCCUR_DATE'][9] == '0':
#         for item in census:
#             dist = abs((float(shot['Latitude']) - float(item['Latitude']))) + abs(
#                 (float(shot['Longitude']) - float(item['Longitude'])))
#             if dist < mindist:
#                 mindist = dist
#                 numindex = census.index(item)
#     if numindex > -1:
#         indexlist20[numindex] += 1
#
# with open('2020.csv', 'w', encoding='utf-8') as ff:
#     for item in indexlist20:
#         ff.write(str(item))
#         ff.write('\n')

# for shot in shootingData:
#     dist = 0
#     mindist = 100
#     numindex = -1
#     if shot['OCCUR_DATE'][8] == '1' and shot['OCCUR_DATE'][9] == '9':
#         for item in census:
#             dist = abs((float(shot['Latitude']) - float(item['Latitude']))) + abs(
#                 (float(shot['Longitude']) - float(item['Longitude'])))
#             if dist < mindist:
#                 mindist = dist
#                 numindex = census.index(item)
#     if numindex > -1:
#         indexlist19[numindex] += 1
#
# with open('2019.csv', 'w', encoding='utf-8') as ff3:
#     for item in indexlist19:
#         ff3.write(str(item))
#         ff3.write('\n')
