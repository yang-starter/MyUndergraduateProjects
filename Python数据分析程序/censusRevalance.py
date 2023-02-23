import pandas as pd
import numpy as np
import scipy as sc
import matplotlib as mt
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as mpl_pp

nyc_census = pd.read_csv("E://nyc_census_tracts.csv")
census_block = pd.read_csv('E://census_block_loc.csv')
print(census_block.head())

# nyc_census.plot(kind = 'scatter',x='Income',y='Poverty')
# mpl_pp.show()

# ----------------------------------------------------------

# 下面三行绘制了多种相关图

# ----------------------------------------------------------
# nyc_census_new = nyc_census.fillna(nyc_census.mean())
# sns.pairplot(nyc_census_new[['Poverty','Income','Professional','Black','White']])
# plt.show()

# ----------------------------------------------------------

# 下面绘制了相关因素的相关数据

# ----------------------------------------------------------

nyc_census_new = nyc_census.fillna(nyc_census.mean())
corr = nyc_census_new[
    ['Poverty', 'Income', 'CensusTract', 'Professional', 'Unemployment','Hispanic',  'White', 'Black']].corr()
corr.head()
f, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(corr, annot=True, fmt='g', cmap='viridis', square=True, ax=ax, xticklabels=1, yticklabels=1)
plt.show()
