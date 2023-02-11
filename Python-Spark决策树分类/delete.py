file = open("adult.test", "r")
lines = []  # lines列表存储每一行的内容
for i in file:
    lines.append(i)  # 遍历每一行内容进行存储
file.close()  # 读取完毕

new = []  # 用于存储处理后的每一行内容
for line in lines:
    if line[:-1].endswith("."):  # 若该行以.结尾
        tmp = line[:-1].rstrip(".")  # 去除该.
        new.append(tmp + "\n")  # 结尾加上换行符并存储
    else:
        new.append(line)  # 若不以.结尾，则直接存储

file_write_object = open("adult.txt", "w")  # 写入模式
for var in new:
    file_write_object.writelines(var)
file_write_object.close()

file = open("adult.txt", "r")
lines = []  # lines列表存储每一行的内容
for i in file:
    lines.append(i)  # 遍历每一行内容进行存储
file.close()  # 读取完毕

new = []  # 用于存储处理后的每一行内容
for line in lines:
    if line[9] == 'Female':
        line[9] == '0'
    if line[9] == 'Male':
        var = line[9] == 1
    new.append(line)

    # if line[:-1].endswith("."):  # 若该行以分号结尾
    #     tmp = line[:-1].rstrip(".")  # 去除该分号
    #     new.append(tmp + "\n")  # 结尾加上换行符并存储
    # else:
    #     new.append(line)  # 若不以分号结尾，则直接存储

file_write_object = open("adult1.txt", "w")  # 写入模式
for var in new:
    file_write_object.writelines(var)
file_write_object.close()