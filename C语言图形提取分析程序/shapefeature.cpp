// shapefeature.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "feature_extract.h"

int _tmain(int argc, _TCHAR* argv[])
{
	Mat img;
	img = imread("ik_beijing_c.bmp");
	if (img.empty())
		return -1;

	Mat imgGray = Img2gray(img); //图像灰度化
	Average(imgGray); //均值滤波
	OTSU(imgGray); // 最大类间方差法二值化
	namedWindow("binGray");
	imshow("binGray", imgGray); //显示灰度二值化后的图像

	Mat imgLabel; //标记表
	int shapesSum; //图形数量
	Label_2steps(imgGray, imgLabel, shapesSum); //连通成分标记-两步法
	//Label_seed(imgGray, imgLabel, shapesSum); //连通成分标记-种子填充法

	vector<Shape> shapes(shapesSum); //图形集
	ImgCompute(shapes, imgLabel); //形状特征计算
	Mat display = Display(shapes, imgLabel); //形状特征显示

	namedWindow("display");
	imshow("display", display); //显示形状特征提取成果
	imwrite("display.bmp", display);
	waitKey(0);
	return 0;
}
