# coding=utf-8
# 统计种类数量的函数
import findspark

findspark.init()

from pyspark import SparkContext

logfile = r'adult.data'
sc = SparkContext("local", "first app")
line = sc.textFile(logfile)


line1 = line.map(lambda line: line.split(","))
m = line1.map(lambda r: (r[8], r))
r = m.reduceByKey(lambda x, y: x)
print(r.count())

