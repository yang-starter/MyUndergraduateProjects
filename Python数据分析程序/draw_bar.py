import matplotlib.pyplot as plt
import college
import numpy as np

numCollege = [0, 0, 0, 0, 0]
dictCollege = college.csvRead('universities.csv')
nycCounty = ['Bronx', 'Brooklyn', 'New York', 'Queens', 'Staten Island']

for item in dictCollege:
    for i in range(0, 5):
        if item['county'] == nycCounty[i]:
            numCollege[i] += 1

print(numCollege)

X = np.arange(5)

plt.bar(X, numCollege, tick_label=nycCounty, width=0.3)
plt.title('numbers of universities and schools in 5 main counties')
plt.show()
