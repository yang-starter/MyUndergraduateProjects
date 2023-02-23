import csv
import numpy as np
import matplotlib.pyplot as plt

timescan = ['18-21', '21-24', '0-3', '3-6']

shooting12 = []
with open('shooting12.csv', "r", encoding='utf-8') as f12:
    reader = csv.DictReader(f12)
    for row in reader:
        shooting12.append(row)
# print(dictionary)
f12.close()

shooting13 = []
with open('shooting13.csv', "r", encoding='utf-8') as f13:
    reader = csv.DictReader(f13)
    for row in reader:
        shooting13.append(row)
# print(dictionary)
f13.close()

numtime12 = [0, 0, 0, 0]
numtime13 = [0, 0, 0, 0]
time = 0
for item in shooting12:
    # 0:00:00的格式
    if item['时刻'][0] == '0' and item['时刻'][1] == ':':
        time = 0
    elif item['时刻'][0] != '0' and item['时刻'][1] == ':':
        time = item['时刻'][0]
    # 00:00:00的格式
    elif item['时刻'][0] == '0' and item['时刻'][1] == '0':
        time = 0
    elif item['时刻'][0] == '0' and item['时刻'][1] != '0':
        time = item['时刻'][1]
    elif item['时刻'][0] != '0' and item['时刻'][1] != ':':
        time = int(item['时刻'][0] + item['时刻'][1])
    # print(time)
    #     elif item['时刻'][0] != 0 and item['时刻'][1] != 0:
    #         time = item['时刻'][0] + item['时刻'][1]
    #     else:
    # #         time = 0

    if 18 <= int(time) < 21:
        numtime12[0] += 1
    if 21 <= int(time) < 24:
        numtime12[1] += 1
    if 0 <= int(time) < 3:
        numtime12[2] += 1
    if 3 <= int(time) < 6:
        numtime12[3] += 1
#
for item in shooting13:
    # 0:00:00的格式
    if item['时刻'][0] == '0' and item['时刻'][1] == ':':
        time = 0
    elif item['时刻'][0] != '0' and item['时刻'][1] == ':':
        time = item['时刻'][0]
    # 00:00:00的格式
    elif item['时刻'][0] == '0' and item['时刻'][1] == '0':
        time = 0
    elif item['时刻'][0] == '0' and item['时刻'][1] != '0':
        time = item['时刻'][1]
    elif item['时刻'][0] != '0' and item['时刻'][1] != ':':
        time = int(item['时刻'][0] + item['时刻'][1])

    if 18 <= int(time) < 21:
        numtime13[0] += 1
    if 21 <= int(time) < 24:
        numtime13[1] += 1
    if 0 <= int(time) < 3:
        numtime13[2] += 1
    if 3 <= int(time) < 6:
        numtime13[3] += 1
# #
X = np.arange(4)
X2 = [i + 0.3 for i in X]

plt.bar(X, numtime12, tick_label=timescan, fc='b', width=0.3, label='2012')
plt.bar(X2, numtime13, fc='r', width=0.3, label='2013')
plt.title('cases of 2012 and 2013')
plt.xlabel('time')
plt.ylabel('number')
plt.legend()
plt.plot(X, numtime12, color='b', linestyle='--')
plt.plot(X2, numtime13, color='r', linestyle='--')
plt.show()
#
