from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox
from PySide2.QtWidgets import QSpinBox, QLabel, QFileDialog, QComboBox
from PySide2.QtCore import Qt, QDir, QTimer
import shapefile
from PIL import Image
from PIL import ImageDraw
import csv
import sys
from osgeo import ogr
import cv2

list = []
a = []
b = []


def handleCalc():
    info = textEdit1.toPlainText()
    boxtext = types.currentText()
    positiontext = textEdit4.toPlainText()
    error = '(' + positiontext + ')' + boxtext + '--' + info
    # f = open("errorRecords.csv", "a", encoding='utf-8')
    if len(info) > 1:
        if error in list:
            QMessageBox.about(window, '错误提示', '请勿重复提交')
        else:
            list.append(error)
            # order = list.index(error) + 1
            # write = csv.writer(f)
            # write.writerow(['%d' % order, '%s' % error])

            # f.write('%d、%s' % (list.index(error) + 1, error))
            textEdit.appendPlainText('%d、' % (list.index(error) + 1))
            #    textEdit.insertPlainText('(%s)--' % boxtext)
            textEdit.insertPlainText(error)
    else:
        QMessageBox.about(window, '错误提示', '请至少输入两个字符')
    textEdit1.clear()
    textEdit4.clear()


def handleCalc1():
    info1 = textEdit2.toPlainText()
    # f = open("errorRecords.csv", "r", encoding='utf-8')

    if len(info1) < 2:
        QMessageBox.about(window, '错误提示', '请至少输入两个字符')
    else:
        for item in list:
            if info1[0] in item:
                count = item.index(info1[0])
                if count < len(item) - 1 and item[count + 1] == info1[1]:
                    position = list.index(item) + 1
                    QMessageBox.about(window, '查找结果', '%d--' % position + item)
                else:
                    QMessageBox.about(window, '错误提示', '查找不存在')

    textEdit2.clear()


def handleCalc2():
    textEdit4.clear()
    textEdit1.clear()


def handleCalc3():
    num = number1.value()
    if num < 1 or num > len(list):
        QMessageBox.about(window, '错误提示', '记录不存在')
    else:
        del list[num - 1]
        textEdit.clear()
        for item in list:
            textEdit.appendPlainText('%d、' % (list.index(item) + 1))
            textEdit.insertPlainText(item)


def filechoice():
    FileDialog = QFileDialog(button4)
    # 设置可以打开任何文件
    FileDialog.setFileMode(QFileDialog.AnyFile)
    # 文件过滤
    Filter = "(*.jpg,*.png,*.jpeg,*.bmp,*.gif)|*.jgp;*.png;*.jpeg;*.bmp;*.gif|All files(*.*)|*.*"
    image_file, _ = FileDialog.getOpenFileName(button4, 'open file', './',
                                               'Image files (*.jpg *.gif *.png *.jpeg)')  # 选择目录，返回选中的路径 'Image files (*.jpg *.gif *.png *.jpeg)'
    # 判断是否正确打开文件
    if not image_file:
        QMessageBox.warning(button4, "警告", "文件错误或打开文件失败！", QMessageBox.Yes)
        return
    textEdit10.appendPlainText(image_file)
    image1.setPixmap(image_file)  ##输入为图片路径，比如当前文件内的logo.png图片
    # self.label.setFixedSize(600, 400)  # 设置显示固定尺寸，可以根据图片的像素长宽来设置
    image1.setScaledContents(True)  # 让图片自适应 label 大小
    img = cv2.imread(image_file)
    cv2.imwrite('trans.png', img)


def show1():
    choice = QMessageBox.question(button2, "NOTICE", "确认要清除吗？", QMessageBox.Yes | QMessageBox.No)
    if choice == QMessageBox.Yes:
        handleCalc2()


def show2():
    choice = choice = QMessageBox.question(button2, "NOTICE", "确认要删除该条记录吗？", QMessageBox.Yes | QMessageBox.No)
    if choice == QMessageBox.Yes:
        handleCalc3()


def typechoice():
    if types1.currentText() == '其他图片文件':
        filechoice()
    if types1.currentText() == 'shp文件':
        shpfile()


def shpfile():
    FileDialog = QFileDialog(button4)
    # 设置可以打开任何文件
    FileDialog.setFileMode(QFileDialog.AnyFile)
    # 文件过滤
    # Filter = "(*.shp)|*.shp|All files(*.*)|*.*"
    image_file, _ = FileDialog.getOpenFileName(button4)  # 选择目录，返回选中的路径 'Image files (*.jpg *.gif *.png *.jpeg)'
    # 判断是否正确打开文件
    if not image_file:
        QMessageBox.warning(button4, "警告", "文件错误或打开文件失败！", QMessageBox.Yes)
        return
    if '.shp' not in image_file:
        QMessageBox.about(window, '错误提示', '请选择shp文件！')
    else:
        textEdit10.appendPlainText(image_file)
        r = shapefile.Reader(image_file)
        #   textEdit5.appendPlainText(r.shapes())
        #  f=open("test.txt", "w")
        # f.write(str(r.shapes()))
        # print(r.fields)
        num = len(r.shapes())
        xdist = r.bbox[2] - r.bbox[0]
        ydist = r.bbox[3] - r.bbox[1]
        iwidth = 1000
        ratio = ydist / xdist
        iheight = int(1000 * ratio)
        xratio = iwidth / xdist
        yratio = iheight / ydist
        i = 0
        img = Image.new("RGB", (iwidth, iheight), "white")
        draw = ImageDraw.Draw(img)
        for i in range(0, num):
            pixels = []
            for x, y in r.shapes()[i].points:
                px = int(iwidth - ((r.bbox[2] - x) * xratio))
                py = int((r.bbox[3] - y) * yratio)
                pixels.append((px, py))

            i += 1
            draw.polygon(pixels, outline="rgb(203, 196, 190)", fill=(255, 255, 240))
        img.save("trans.png")
        path = 'trans.png'
        image1.setPixmap(path)  # 输入为图片路径，比如当前文件内的logo.png图片
        # self.label.setFixedSize(600, 400)  # 设置显示固定尺寸，可以根据图片的像素长宽来设置
        image1.setScaledContents(True)  # 让图片自适应 label 大小
        # for j in range(0, len(r.fields)):
        #     textEdit5.appendPlainText(str(r.fields[j]))

        fn = image_file
        ds = ogr.Open(fn, 0)  # ds = data source，0：表示以只读模式打开文件，1或True：表示以编辑模式打开
        if ds is None:  # 确保shapefile文件不为空，可正常打开
            sys.exit('Could not open {0}.'.format(fn))
        lyr = ds.GetLayer()  # 获取图层索引，从0开始，不提供参数时，默认返回第1个图层
        # feature = lyr.GetNextFeature()
        # while feature:
        #     geom = feature.GetGeometryRef()
        #     X = geom.GetX()  # 读取xy坐标,转为字符串，方便TXT写入
        #     Y = geom.GetY()
        #     print(X, Y)
        #     feature.Destroy()
        #     feature = lyr.GetNextFeature()
        for feat in lyr:
            # pt = feat.geometry()  # 获得几何对象
            # 获得属性值
            name = feat.GetField('NAME')
            # geom = feature.GetGeometryRef()
            # X = str(geom.GetX())  # 读取xy坐标,转为字符串，方便TXT写入
            # Y = str(geom.GetY())
            # pop = feat.GetField('POP_MAX')
            # pop = feat.GetFieldAsString('POP_MAX')  #  数据转换
            # pop = feat.GetFieldAsInteger('POP_MAX')
            # print(name, pt, x, y)
            textEdit5.appendPlainText(name)
            # textEdit5.insertPlainText(X+',')
            # textEdit5.insertPlainText(Y)

            # i += 1
            # if i == 5:
            #     break


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    img = cv2.imread('trans.png')
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        a.append(x)
        b.append(y)
        cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("image", img)


def position():
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    try:
        img = cv2.imread('trans.png')
        cv2.imshow("image", img)
        cv2.waitKey(0)
        # for i in range(0, len(a)):
        #     # print(a[i], b[i])
        if len(a) == 0:
            QMessageBox.about(window, '提示', '未选点')
        else:
            poss = str(a[len(a) - 1]) + ',' + str(b[len(b) - 1])
            textEdit4.appendPlainText(poss)
    except:
        QMessageBox.about(window, '提示', '未选择图片')


def file():
    f = open("errorRecords.csv", "a", encoding='utf-8')
    # write = csv.writer(f)
    user = textEdit6.toPlainText()
    filefile = textEdit10.toPlainText()
    if len(user) > 0 and len(filefile) > 0:
        f.write('----------%s的单次操作----------\n' % user)
        f.write('操作文件为：%s\n' % filefile)
        j = 1
        if len(list) > 0:
            for error in list:
                # write.writerow(['%d' % j, '%s' % error])
                f.write('%d,' % j)
                f.write(error)
                f.write('\n')
                j += 1
            f.write('\n')


def login():
    username = textEdit6.toPlainText()
    password = textEdit7.toPlainText()
    with open('b.csv', 'r', encoding='utf-8') as g:
        length1 = len(username)
        length2 = len(password)
        m = 0
        for item in g:

            j = 0
            k = 0
            for i in range(0, length1):
                if username[i] == item[i]:
                    i += 1
                    j += 1
                else:
                    break

            if j == length1:
                for ii in range(length1 + 1, length1 + length2 + 1):
                    if password[ii - length1 - 1] == item[ii]:
                        ii += 1
                        k += 1
                    else:
                        break
                if k == length2 and length1 + length2 + 2 == len(item):
                    QMessageBox.about(window, '操作提示', '登陆成功')
                    button.setEnabled(True)
                    button1.setEnabled(True)
                    button2.setEnabled(True)
                    button3.setEnabled(True)
                    button4.setEnabled(True)
                    button5.setEnabled(True)
                    m += 1
        if m == 0:
            QMessageBox.about(window, '操作提示', '登陆失败')


def register():
    user = textEdit8.toPlainText()
    pwd = textEdit9.toPlainText()
    if len(user)>0 and len(pwd)>0:
        with open('b.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            column1 = [row[0] for row in reader]
            if user in column1:
                QMessageBox.about(window, '操作提示', '用户已存在')
            else:
                with open('b.csv', 'a', encoding='utf-8') as f:
                    QMessageBox.about(window, '操作提示', '注册成功')
                    f.write('\n')
                    f.write(user)
                    f.write(',')
                    f.write(pwd)
                    f.write('\n')
                    f.close()
                textEdit8.clear()
                textEdit9.clear()
    else:
        QMessageBox.about(window, '操作提示', '请输入有效用户名和密码')

app = QApplication([])

window = QMainWindow()
window.resize(1300, 800)
window.move(300, 100)
window.setWindowTitle('地图数据检查工具')

textEdit4 = QPlainTextEdit(window)
textEdit4.setPlaceholderText("坐标")
textEdit4.move(580, 75)
textEdit4.resize(200, 50)
textEdit4.setEnabled(False)
# textEdit3 = QPlainTextEdit(window)
# textEdit3.setPlaceholderText("请输入错误类型")
# textEdit3.move(580, 150)
# textEdit3.resize(200, 50)

textEdit10 = QPlainTextEdit(window)
textEdit10.setPlaceholderText("文件路径")
textEdit10.move(80, 600)
textEdit10.resize(300, 50)
textEdit10.setEnabled(False)

hint = QLabel('请选择错误类型', window)
hint.resize(200, 15)
hint.move(580, 140)

types = QComboBox(window)
types.move(580, 170)
types.resize(200, 30)
types.addItems(['边界错误', '位置偏移', '名称错误', '漏标关键地物', '地物实际不存在'])

types1 = QComboBox(window)
types1.move(115, 520)
types1.resize(130, 30)
types1.addItems((['shp文件', '其他图片文件']))

textEdit1 = QPlainTextEdit(window)
textEdit1.setPlaceholderText("请输入错误描述")
textEdit1.move(580, 225)
textEdit1.resize(200, 50)

textEdit2 = QPlainTextEdit(window)
textEdit2.setPlaceholderText("搜索")
textEdit2.move(580, 430)
textEdit2.resize(200, 50)

button1 = QPushButton('搜索', window)
button1.move(630, 520)
button1.clicked.connect(handleCalc1)

button = QPushButton('保存', window)
button.move(630, 340)
button.clicked.connect(handleCalc)

button2 = QPushButton('清除', window)
button2.move(630, 300)
button2.clicked.connect(show1)

button3 = QPushButton('删除该条记录', window)
button3.move(840, 520)
button3.clicked.connect(show2)

textEdit = QPlainTextEdit(window)
textEdit.setPlaceholderText("本次记录")
textEdit.move(820, 30)
textEdit.resize(150, 400)
textEdit.setEnabled(False)

textEdit5 = QPlainTextEdit(window)
textEdit5.setPlaceholderText("shp地图字段信息")
textEdit5.move(400, 600)
textEdit5.resize(800, 140)
# textEdit5.setEnabled(False)

image1 = QLabel(window)
image1.move(40, 30)
image1.resize(450, 450)
image1.setStyleSheet('background-color: rgb(240, 255, 255)')
image1.setMouseTracking(True)

# image2 = QLabel(window)
# image2.move(580, 80)
# image2.resize(200, 50)
# image2.setText('x,y')

button5 = QPushButton('点击选取坐标', window)
button5.move(385, 520)
button5.clicked.connect(position)

image3 = QLabel(window)
image3.move(580, 30)
image3.resize(200, 50)
image3.setText('选中的坐标')

button4 = QPushButton('选择文件', window)
button4.move(270, 520)
button4.clicked.connect(typechoice)

number1 = QSpinBox(window)
number1.move(840, 460)

button.setEnabled(False)
button1.setEnabled(False)
button2.setEnabled(False)
button3.setEnabled(False)
button4.setEnabled(False)
button5.setEnabled(False)

# 用户登录与注册部分

image4 = QLabel(window)
image4.move(1100, 20)
image4.resize(200, 50)
image4.setText('用户登录')

textEdit6 = QPlainTextEdit(window)
textEdit6.setPlaceholderText("用户名")
textEdit6.move(1070, 80)
textEdit6.resize(150, 35)

textEdit7 = QPlainTextEdit(window)
textEdit7.setPlaceholderText("密码")
textEdit7.move(1070, 140)
textEdit7.resize(150, 35)

button6 = QPushButton('登录', window)
button6.move(1100, 200)
button6.clicked.connect(login)

image5 = QLabel(window)
image5.move(1100, 280)
image5.resize(200, 50)
image5.setText('用户注册')

textEdit8 = QPlainTextEdit(window)
textEdit8.setPlaceholderText("输入用户名")
textEdit8.move(1070, 340)
textEdit8.resize(150, 35)

textEdit9 = QPlainTextEdit(window)
textEdit9.setPlaceholderText("输入密码")
textEdit9.move(1070, 400)
textEdit9.resize(150, 35)

button7 = QPushButton('注册', window)
button7.move(1100, 460)
button7.clicked.connect(register)

window.show()

app.exec_()

file()
