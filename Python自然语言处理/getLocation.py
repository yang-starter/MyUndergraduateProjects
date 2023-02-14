import json
import requests


def get_location_x_y(place):
    url = 'https://restapi.amap.com/v3/geocode/geo?parameters'
    parameters = {
        'key': '5e351e900ed432f6e6ad161b0645e6c9',
        'address': '%s' % place
    }
    page_resource = requests.get(url, params=parameters)
    text = page_resource.text  # 获得数据是json格式
    data = json.loads(text)  # 把数据变成字典格式
    location = data["geocodes"][0]['location']
    # print(location)
    return location


if __name__ == '__main__':
    addresslist = []
    locationlist = []
    fw = open('locations.txt', 'w', encoding='utf-8')
    with open('address.txt', "r", encoding='utf-8') as fr:
        lines = fr.readlines()
    for line in lines:
        line = line.strip('\n')
        addresslist.append(line)
    length = len(addresslist)
    for i in range(0, length):
        locations = get_location_x_y(addresslist[i])
        content = '南京市' + addresslist[i] + ',' + '南京市' + ',' + '"' + locations +'"'
        fw.write(content)
        fw.write('\n')
        locationlist.append(locations)
    fw.close()
    fr.close()
    print(locationlist)
    # print(addresslist)



    # get_location_x_y()
