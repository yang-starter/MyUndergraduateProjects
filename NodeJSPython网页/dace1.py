# -*- coding: utf-8 -*-
import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS

# 数据库连接
db = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="dace01")
cursor = db.cursor()

# 后端服务启动
app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/table/list', methods=['POST'])
def table_list():
    if request.method == "POST":
        cursor.execute("select username,usernumber,userphone,usermail,userhobby from new_table01")
        data = cursor.fetchall()
        temp = {}
        result = []
        if (data != None):
            for i in data:
                temp["username"] = i[0]
                temp["usernumber"] = i[1]
                temp["userphone"] = i[2]
                temp["usermail"] = i[3]
                temp["userhobby"] = i[4]
                result.append(temp.copy())  # 特别注意要用copy，否则只是内存的引用
            print("result:", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])


@app.route('/table/add', methods=['POST'])
def table_add():
    if request.method == "POST":
        username = request.form.get("username")
        usernumber = request.form.get("usernumber")
        userphone = request.form.get("userphone")
        usermail = request.form.get("usermail")
        userhobby = request.form.get("userhobby")
        try:
            cursor.execute("insert into new_table01(username,usernumber,userphone,usermail,userhobby) values (\""
                           + str(username) + "\",\"" + str(usernumber) + "\",\"" +
                           str(userphone) + "\",\"" + str(usermail) + "\",\"" + str(userhobby) + "\")")
            db.commit()  # 提交，使操作生效
            print("add a new user successfully!")
            return "1"
        except Exception as e:
            print("add a new user failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/table/update', methods=['POST'])
def table_update():
    if request.method == "POST":
        username = request.form.get("username")
        usermail = request.form.get("usermail")
        userphone = request.form.get("userphone")
        try:
            cursor.execute("update new_table01 set usermail=\"" + str(usermail)
                           + "\" where username=" + "'%s'" % str(username))
            db.commit()
            cursor.execute("update new_table01 set userphone=\"" + str(userphone)
                           + "\" where username=" + "'%s'" % str(username))
            db.commit()
            print("update successfully!")
            return "1"
        except Exception as e:
            print("update password failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/table/del', methods=['POST'])
def table_del():
    if request.method == "POST":
        username = request.form.get("username")
        try:
            cursor.execute("delete from new_table01 where username=" + "'%s'" % str(username))
            db.commit()
            print("delete user" + str(username) + " successfully!")
            return "1"
        except Exception as e:
            print("delete the user failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090)
    db.close()
    print("Good bye!")
