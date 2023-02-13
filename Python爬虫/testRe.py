import re

# pat = re.compile("AA")  # AA是正则表达式，去验证其他字符串
# m = pat.search("ABCAA")
# m = pat.search("CBA")   # search字符串被校验
# m = pat.search("AABAAAADDDTDYCAA")
# m = re.search("aa", "asdrdsaadd")
# print(m)

print(re.findall("a", "arva gasdfadfgDDDFFFBSggg"))

print(re.findall("[A-Z]", "arva gasADdfadfgDDDFFFBSggg"))

print(re.findall("[A-Z]+", "arva gasAAdfadfgDDDFFFBSggg"))

print(re.sub("a", "A", "abcdcasd"))

# 在正则表达式被转义的字符串前加上r，防止转义字符生效

