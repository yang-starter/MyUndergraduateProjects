import requests
import json
# 指定url
post_url = 'https://fanyi.baidu.com/sug'

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}
# post请求参数处理
word = input('enter a word')
data = {'kw': word}

# 请求发送
response = requests.post(url=post_url, data=data, headers=head)
dic_obj = response.json()

fileName = word + '.js'
fp = open(fileName, 'w', encoding='utf-8')
json.dump(dic_obj, fp=fp, ensure_ascii=False)

print('over!')
