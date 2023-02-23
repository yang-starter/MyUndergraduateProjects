# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from setting import data, photo, host, port
import redis
import json
import numpy as np
import xlrd


def listToJson(lst):
    keys = [str(x) for x in np.arange(len(lst))]
    keys[0] = '相关图片链接'
    keys[1] = '纬度'
    keys[2] = '经度'
    keys[3] = '所属部门'
    keys[4] = '首次设立时间'
    keys[5] = '级别'
    keys[6] = '类型'
    keys[7] = '保护对象'
    keys[8] = '面积（ha）'
    keys[9] = '所在地'
    keys[10] = '名称'

    list_json = dict(zip(keys, lst))
    str_json = json.dumps(list_json, indent=2, ensure_ascii=False)  # json转为string
    return str_json


# 后端服务启动
app = Flask(__name__)
CORS(app, resources=r'/*')


# 查看图片
@app.route("/photo/<imageId>.jpg")
def get_image(imageId):
    if request.method == 'GET':
        filepath = (photo + r'\{}.jpg').format(imageId)
        with open(filepath, 'rb') as f:
            try:
                image = f.read()
                resp = Response(image, mimetype="image/jpg")
                return resp
            except:
                error_info = '您没有权限访问或图片链接错误'
                return error_info


# 根据id查询
@app.route('/table/list', methods=['POST'])
def QueryById():
    if request.method == 'POST':
        try:
            idname = request.form.get('idname')
            v = redis_conn.lrange(idname, 0, 10)
            # print(v)
            js = listToJson(v)
            return js
        except:
            error_info = '您输入的id不正确，请重新尝试！'
            return error_info


# 根据省份查询
@app.route('/table/province', methods=['POST'])
def QueryByProvince():
    jslist = []
    if request.method == "POST":
        cityname = request.form.get('provincename')
        try:
            a = redis_conn.keys()
            s = [s for s in a if cityname in s]
            for item in s:
                v = redis_conn.lrange(item, 0, 10)
                js = listToJson(v)
                jslist.append(js)
            if len(jslist) > 0:
                return jsonify(jslist)
            else:
                error_info = '您输入的地名不符合要求，请输入省份缩写重新尝试！'
                return error_info
        except:
            error_info = '您输入的地名不符合要求，请重新尝试！'
            return error_info


# 根据城市查询
@app.route('/table/city', methods=['POST'])
def QueryByCity():
    jslist = []
    s = []
    if request.method == "POST":
        cityname = request.form.get('cityname')
        try:
            keys = redis_conn.keys()
            keyNum = len(keys)
            for i in range(1, keyNum):
                l = redis_conn.lrange(keys[i], 9, 9)
                if cityname in l[0]:
                    s.append(keys[i])
            for item in s:
                v = redis_conn.lrange(item, 0, 10)
                js = listToJson(v)
                jslist.append(js)
            if len(jslist) > 0:
                return jsonify(jslist)
            else:
                error_info = '您输入的地名不符合要求，请重新尝试！'
                return error_info
        except:
            error_info = '您输入的地名不符合要求，请重新尝试！'
            return error_info


# 根据空间范围查询
@app.route('/table/range', methods=['POST'])
def QueryByRange():
    jslist = []
    keys = redis_conn.keys()
    keyNum = len(keys)
    if request.method == "POST":
        lat_max = float(request.form.get("lat_max"))
        lat_min = float(request.form.get("lat_min"))
        long_max = float(request.form.get("long_max"))
        long_min = float(request.form.get("long_min"))
        try:
            for i in range(1, keyNum):
                l = redis_conn.lrange(keys[i], 1, 2)
                if lat_min <= float(l[0]) <= lat_max and float(l[1]) >= long_min and float(
                        l[1]) <= long_max:
                    v = redis_conn.lrange(keys[i], 0, 10)
                    js = listToJson(v)
                    jslist.append(js)
            if len(jslist) > 0:
                return jsonify(jslist)
            else:
                error_info = '您输入的选址范围不符合要求，请重新尝试！'
                return error_info
        except:
            error_info = '您输入的选址范围不符合要求，请重新尝试！'
            return error_info


if __name__ == "__main__":
    redis_conn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True,
                             charset='UTF-8', encoding='UTF-8')

    app.run(host=host, port=port)
    # db.close()
    print("Good bye!")
