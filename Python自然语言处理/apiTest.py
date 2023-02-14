import jieba
from string import punctuation
from zhon.hanzi import punctuation


def geoword():
    f = open('trails.txt', 'r', encoding='utf8')
    address = []
    for line in f:
        for letter in line:
            if letter == '到' or letter == '往' or letter == '至' or letter == '在':
                pos = line.index(letter)

                add = line[pos + 1] + line[pos + 2] + line[pos + 3] + line[pos + 4] + line[pos + 5] + line[pos + 6] + \
                      line[pos + 7] + line[pos + 8]
                address.append(add)

    for item in address:
        if '禄口' in item:
            address.remove(item)

    address = list(set(address))
    # if not '\u4e00' <= item <= '\u9fa5':
    #     address.remove(item)

    length = len(address)
    for i in range(0, length):
        print('%s:' % i + address[i])
    # while 1:
    return address

    #     # print(line)
    #     seg_list = jieba.cut(line, cut_all=False)
    #     result = "/ ".join(seg_list) + "\n"
    #     # print("__" + "Default Mode: " + "/ ".join(seg_list) + "\n")  # 精确模式
    #     jiebaword.append(result)
    # # print(jiebaword)
    # return jiebaword


if __name__ == '__main__':
    address = geoword()
    fw = open('address.txt', 'a+', encoding='utf-8')
    while 1:
        addr = input('input address:')
        if addr == '!':
            break
        else:
            fw.write(addr)
            fw.write('\n')
    fw.close()
