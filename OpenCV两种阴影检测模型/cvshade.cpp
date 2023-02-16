// cvshade.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
//C1C2C3
#include <iostream>   
#include <opencv2/core/core.hpp>   
#include <opencv2/highgui/highgui.hpp>   
#include <algorithm>
#include <cmath>
using namespace std;  
using namespace cv;   

int mini(int b, int g, int r)
{
	if((b<=g)&&(b<=r))
	{
		return b;
	}
	else if (g <= r) { return g;}
	else { return r; }
};

int main()
{

	Mat zy3, result;
	zy3 = imread("F:/zy3.jpg");
	result = zy3.clone();
	double h, s, v, cal, cal1, theta, m, gray,c3 = 0.0;
	int max = 0;
	double pi = 3.14159;
	int rowNumber = result.rows;
	int colNumber = result.cols;
	int rr[][10000] = {0};
	for (int row = 0; row < rowNumber; row++)
		for (int col = 0; col < colNumber; col++) {
				int	b = zy3.at<Vec3b>(row, col)[0];  //读取通道值
				int	g = zy3.at<Vec3b>(row, col)[1];
				int	r = zy3.at<Vec3b>(row, col)[2];
				if (r > g) { max = r; }
				else { max = g; }    //取更大的值为max
				c3 = atan(b / max); // C3的赋值
				if (c3 > -0.0000000001 && b < 127) {    // 选择阈值，二值化
					result.at<Vec3b>(row, col)[0] = 0;
					result.at<Vec3b>(row, col)[1] = 0;
					result.at<Vec3b>(row, col)[2] = 0;
				}
				else
				{
					result.at<Vec3b>(row, col)[0] = 255;
					result.at<Vec3b>(row, col)[1] = 255;
					result.at<Vec3b>(row, col)[2] = 255;
				}
		}
//	imshow("src", zy3);
	imshow("pic", result);
	waitKey();
	imwrite("F:/zzzzc1c2c3.jpg", result);
	return 0;

}

				
/*
//HSV
#include <iostream>
#include <opencv2/opencv.hpp>
#include <math.h>
using namespace std;
using namespace cv;

double varOf3(double x1, double x2, double x3) {
	double mean = (x1 + x2 + x3) / 3;
	return (pow((x1 - mean), 2) + pow((x2 - mean), 2) + pow((x3 - mean), 2));
}
Mat ShadowExtraction(Mat src, int type = 1);

int main()
{
	//读取图片
	char filename[] = "F:/Color.bmp";
	Mat src = imread(filename);
	imshow("Previous", src);
	
	ShadowExtraction(src);
	return 0;
}

Mat ShadowExtraction(Mat src, int type) {
	int rows = src.rows, cols = src.cols;
	Mat M(rows, cols, CV_8UC1);
	double* var = new double[rows * cols];
	int i = 0;
	for (int x = 0; x < cols; x++) {
		for (int y = 0; y < rows; y++) {
			if (((double)src.at<Vec3b>(y, x)[0] + (double)src.at<Vec3b>(y, x)[1] + (double)src.at<Vec3b>(y, x)[2]) < 250) {
				var[i] = sqrt(varOf3((double)src.at<Vec3b>(y, x)[0], (double)src.at<Vec3b>(y, x)[1], (double)src.at<Vec3b>(y, x)[2]));
			}
			else {
				var[i] = 255;
			}
			i++;
		}
	}
	int j = 0;
	for (int x = 0; x < cols; x++) {
		for (int y = 0; y < rows; y++) {
			M.at<uchar>(y, x) = (uchar)(var[j]);//把方差作为亮度进行赋值
			j++;
		}
	}
	threshold(M, M, 70, 255, THRESH_BINARY_INV);//把图像二值化
	imshow("Shadow", M);
	Mat M3 = src.clone();//M3是最后阴影提取后的结果
	double count = 0.0;
	for (int x = 0; x < cols; x++) {//给识别出来的阴影上色
		for (int y = 0; y < rows; y++) {
			if (M.at<uchar>(y, x) == 255) {
				M3.at<Vec3b>(y, x)[0] = 0;
				M3.at<Vec3b>(y, x)[1] = 0;
				M3.at<Vec3b>(y, x)[2] = 0;
				count++;
			}
			else {
				M3.at<Vec3b>(y, x)[0] = 255;
				M3.at<Vec3b>(y, x)[1] = 255;
				M3.at<Vec3b>(y, x)[2] = 255;
				count++;
			}
		}
	}

	//waitKey(0);
	//imwrite("F:/color627.jpg", M3);
	delete[] var;
	return M3;
}*/

