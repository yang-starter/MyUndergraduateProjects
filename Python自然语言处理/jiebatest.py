import jieba
from string import punctuation
from zhon.hanzi import punctuation

# 去除中文符号
def hanzi(string):
    for i in punctuation:
        string = string.replace(i,'')
    return string
#去除英文符号
def english(string):
    for i in punctuation:
        string = str.replace(i, '')
    return string

# 结巴分词分割
def jiebaword():
    f = open('trails.txt', encoding='utf8')
    text = []
    for line in f:
        if line.isspace():
            pass
        else:
            line1 = hanzi(line)
            line2 = english(line1)
            text.append(line2.strip())
    f.close()
    jiebaword = []
    length = len(text)
    for i in range(0, length):
        seg_list = jieba.cut(text[i], cut_all=False)
        result = "/ ".join(seg_list) + "\n"
        jiebaword.append(result)
    return jiebaword


def stopword():
    stopword = []
    try:
        with open('stopword.txt', "r", encoding='utf-8') as fr:
            lines = fr.readlines()
    except FileNotFoundError:
        print("no file like this")
    for line in lines:
        line = line.strip('\n')
        stopword.append(line)
    return stopword


def clean_stopword(jiebaword,stopword):
    fw = open('CleanWords.txt', 'a+', encoding='utf-8')
    fw.truncate(0)
    for words in jiebaword:
        words = words.split('/ ')
        for word in words:
            print(word)
            if word in stopword:
                pass
            else:
                fw.write(word+'\t')
        fw.write('\n')
    fw.close()
    try:
        with open('CleanWords.txt', "r", encoding='utf-8') as fr:
            lines = fr.readlines()
    except FileNotFoundError:
        print("no file like this")
    fw = open('CleanWords2.txt','w',encoding='utf-8')
    for line in lines:
        if len(line)<=3:
            line = ''
        fw.write(line)
        fw.write('\n')
    fr.close()
    fw.close()
    with open('CleanWords2.txt', 'r', encoding='utf-8') as fr2, open('CleanWords4.txt', 'w', encoding='utf-8') as fd2:
        for text in fr2.readlines():
            if text.split():
                fd2.write(text)
    fr2.close()
    fd2.close()


if __name__ == '__main__':
    jiebaword1 = jiebaword()
    stopword1 = stopword()
    i = 0
    for i in range(99):
        stopword1.append(str(i))
    # print(stopword1)
    # print(stopword.count(','))
    # print(jiebaword)
    clean_stopword(jiebaword1, stopword1)
