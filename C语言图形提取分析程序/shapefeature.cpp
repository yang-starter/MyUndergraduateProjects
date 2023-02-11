// shapefeature.cpp : �������̨Ӧ�ó������ڵ㡣
//

#include "stdafx.h"
#include "feature_extract.h"

int _tmain(int argc, _TCHAR* argv[])
{
	Mat img;
	img = imread("ik_beijing_c.bmp");
	if (img.empty())
		return -1;

	Mat imgGray = Img2gray(img); //ͼ��ҶȻ�
	Average(imgGray); //��ֵ�˲�
	OTSU(imgGray); // �����䷽���ֵ��
	namedWindow("binGray");
	imshow("binGray", imgGray); //��ʾ�Ҷȶ�ֵ�����ͼ��

	Mat imgLabel; //��Ǳ�
	int shapesSum; //ͼ������
	Label_2steps(imgGray, imgLabel, shapesSum); //��ͨ�ɷֱ��-������
	//Label_seed(imgGray, imgLabel, shapesSum); //��ͨ�ɷֱ��-������䷨

	vector<Shape> shapes(shapesSum); //ͼ�μ�
	ImgCompute(shapes, imgLabel); //��״��������
	Mat display = Display(shapes, imgLabel); //��״������ʾ

	namedWindow("display");
	imshow("display", display); //��ʾ��״������ȡ�ɹ�
	imwrite("display.bmp", display);
	waitKey(0);
	return 0;
}
