from math import *
import numpy
import numpy as np
# import相关库进行数学和矩阵计算

# 数据准备部分---------------------------------------------------------------------------------
# 以列表形式存储已知数据
x = [-86.15e-3, -53.40e-3, -14.78e-3, 10.46e-3]
y = [-68.99e-3, 82.21e-3, -76.63e-3, 64.43e-3]
X = [36589.41, 37631.08, 39100.97, 40426.54]
Y = [25273.32, 31324.51, 24934.98, 30319.81]
Z = [2195.17, 728.69, 2386.50, 757.31]
# n表示点的数量，在运算中起作用
n = 4
# trans用来进行角度的转换和精度评定
trans = 180 / pi * 3600
# 给定初值
phi = 0
omega = 0
kappa = 0
m = 50000
f = 153.24e-3
Z0 = m * f
X0 = sum(X) / len(X)
Y0 = sum(Y) / len(Y)
# times统计迭代次数
times = 0

# 对计算用到的矩阵提前进行处理
x_ = np.mat(numpy.zeros(shape=(len(x), 1)))
y_ = np.mat(numpy.zeros(shape=(len(x), 1)))
ll = np.mat(numpy.zeros(shape=(len(x) * 2, 1)))
A = np.mat(numpy.zeros(shape=(len(x) * 2, 6)))
XX = np.mat(numpy.ones(shape=(6, 1)))
XYZ = np.mat(np.zeros((len(x), 3)))
R = np.mat(numpy.zeros(shape=(3, 3)))


# 主要计算部分--------------------------------------------------------------------------------------------
# 设定精度评定标准下的循环
while abs(XX[0, 0]) >= 1e-3 or abs(XX[1, 0]) >= 1e-3 or abs(XX[2, 0]) >= 1e-3 or abs(XX[3, 0] * trans) >= 6 or abs(
        XX[4, 0] * trans) >= 6 or abs(XX[5, 0] * trans) >= 6:
    # 旋转矩阵
    R = np.mat([[cos(phi) * cos(kappa) - sin(phi) * sin(omega) * sin(kappa),
                 -cos(phi) * sin(kappa) - sin(phi) * sin(omega) * cos(kappa), -sin(phi) * cos(omega)],
                [cos(omega) * sin(kappa), cos(omega) * cos(kappa), -sin(omega)],
                [sin(phi) * cos(kappa) + cos(phi) * sin(omega) * sin(kappa),
                 -sin(phi) * sin(kappa) + cos(phi) * sin(omega) * cos(kappa), cos(phi) * cos(omega)]])
    for i in range(0, len(x)):
        XYZ[i, 0] = X[i] - X0
        XYZ[i, 1] = Y[i] - Y0
        XYZ[i, 2] = Z[i] - Z0
    XYZ_ = R.T * XYZ.T
    for i in range(0, len(x)):
        # 系数阵
        ll[i * 2, 0] = x[i] + f * XYZ_[0, i] / XYZ_[2, i]
        ll[i * 2 + 1, 0] = y[i] + f * XYZ_[1, i] / XYZ_[2, i]
        H = Z0 - Z[i]
        A[i * 2, 0] = -f / H
        A[i * 2 + 1, 0] = 0
        A[i * 2, 1] = 0
        A[i * 2 + 1, 1] = -f / H
        A[i * 2, 2] = -x[i] / H
        A[i * 2 + 1, 2] = -y[i] / H
        A[i * 2, 3] = -f * (1 + pow(x[i], 2) / pow(f, 2))
        A[i * 2 + 1, 3] = -x[i] * y[i] / f
        A[i * 2, 4] = -x[i] * y[i] / f
        A[i * 2 + 1, 4] = -f * (1 + pow(y[i], 2) / pow(f, 2))
        A[i * 2, 5] = y[i]
        A[i * 2 + 1, 5] = -x[i]
    # 关键公式计算外方位元素
    XX = (A.T * A).I * A.T * ll
    # 循环相加得到所求值
    X0 += XX[0, 0]
    Y0 += XX[1, 0]
    Z0 += XX[2, 0]
    phi += XX[3, 0]
    omega += XX[4, 0]
    kappa += XX[5, 0]
    times += 1

# 计算误差矩阵和单位权中误差
V = A * XX - ll
VV = abs(V.T * V)
m0 = sqrt(VV / (2 * n - 6))

# 输出结果---------------------------------------------------------------------------------------------
print("迭代次数为：", times)
print("外方位元素Xs为：", X0)
print("外方位元素Ys为：", Y0)
print("外方位元素Zs为：", Z0)
print("外方位元素phi为：", phi)
print("外方位元素omega为：", omega)
print("外方位元素kappa为：", kappa)
print("旋转矩阵：\n", R)
print("单位权中误差为：+-", m0)
