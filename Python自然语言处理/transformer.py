from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.cluster.kmeans import KMeansClusterer
from nltk.cluster.util import cosine_distance
import pandas as pd
from collections import Counter


# 生成tf-idf矩阵文档
def get_tfidf():
    try:
        with open('CleanWords4.txt', "r", encoding='utf-8') as fr:
            lines = fr.readlines()
    except FileNotFoundError:
        print("no file like this")
    transformer = TfidfVectorizer()
    tfidf = transformer.fit_transform(lines)
    # 转为数组形式
    tfidf_arr = tfidf.toarray()
    return tfidf_arr


# K-means聚类
def get_cluster(tfidf_arr, k):
    kmeans = KMeansClusterer(num_means=k, distance=cosine_distance)  # 分成k类，使用余弦相似分析
    kmeans.cluster(tfidf_arr)
    # 获取分类
    kinds = pd.Series([kmeans.classify(i) for i in tfidf_arr])
    fw = open('ClusterText.txt', 'a+', encoding='utf-8')
    for i, v in kinds.items():
        fw.write(str(i) + '\t' + str(v) + '\n')
    fw.close()


# 获取分类文档
def cluster_text():
    index_cluser = []
    try:
        with open('ClusterText.txt', "r", encoding='utf-8') as fr:
            lines = fr.readlines()
    except FileNotFoundError:
        print("no file like this")
    for line in lines:
        line = line.strip('\n')
        line = line.split('\t')
        index_cluser.append(line)
    # index_cluser[i][j]表示第i行第j列
    try:
        with open('CleanWords4.txt', "r", encoding='utf-8') as fr:
            lines = fr.readlines()
    except FileNotFoundError:
        print("no file like this")
    for index, line in enumerate(lines):
        for i in range(16):
            if str(index) == index_cluser[i][0]:
                fw = open('clusterResult' + index_cluser[i][1] + '.txt', 'a+', encoding='utf-8')
                fw.write(line)
    fw.close()


# 获取主题词
def get_title(cluster):
    for i in range(cluster):
        try:
            with open('clusterResult' + str(i) + '.txt', "r", encoding='utf-8') as fr:
                lines = fr.readlines()
        except FileNotFoundError:
            print("no file like this")
        all_words = []
        for line in lines:
            line = line.strip('\n')
            line = line.split('\t')
            for word in line:
                all_words.append(word)
        c = Counter()
        for x in all_words:
            if len(x) > 1 and x != '\r\n':
                c[x] += 1

        print('主题' + str(i + 1) + '\n词频统计结果：')
        # 输出词频最高的那个词，也可以输出多个高频词
        for (k, v) in c.most_common(20):
            print(k, ':', v, '\n')


if __name__ == '__main__':
    get_tfidf()
    print(get_tfidf())
    print(get_tfidf().shape)
    get_cluster(get_tfidf(), 3)
    cluster_text()
    get_title(3)
