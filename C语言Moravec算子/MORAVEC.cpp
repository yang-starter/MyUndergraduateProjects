// MORAVEC.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。

#include <iostream>   
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>   
#include <opencv2/highgui/highgui.hpp>   
#include <opencv2/imgproc/types_c.h>
#include "math.h"
#include<time.h>
using namespace std;  //省去屏幕输出函数cout前的std::
using namespace cv;   // 省去函数前面加cv::的必要性

#include"stdlib.h"
#include "stdio.h"
#include <string>
#include <algorithm>
#ifndef FALSE
#define FALSE   (0)
#endif
#ifndef TRUE
#define TRUE    (1)
#endif

void Moravec(Mat img, char* OutputPath);
void ImageMatch(char* Path, Mat Img_left, Mat Img_right);

int main()
{

	Mat ImgLeft = imread("Left.tif", 0);
	if (ImgLeft.empty())
	{
		printf("fail!\n");
		return -1;
	}

	Mat ImgRight = imread("Right.tif", 0);
	if (ImgRight.empty())
	{
		printf("fail!\n");
		return -1;
	}

	char Path[] = "MoravecPoint.bmp";
	Moravec(ImgLeft, Path);
	ImageMatch(Path, ImgLeft, ImgRight);
	system("pause");
	return 0;
}

void Moravec(Mat img, char* OutputPath) {
	unsigned char* pImg = img.data;

	int col = img.cols;
	int row = img.rows;

	//定义遍历窗口的大小
	int w1 = 5;

	//兴趣值阈值
	int threshold = 6000;

	//记录兴趣值，四个方向相邻像素灰度差平方和
	float V0, V45, V90, V135;

	float MinIV = 0;

	//数组IV存放每个像元的兴趣值
	float* IV = new float[row * col];
	float* IV1 = new float[row * col];
	for (int i = 0; i < row; i++) {
		for (int j = 0; j < col; j++) {
			IV[i * col + j] = img.at<uchar>(i, j);
		}
	}
	for (int i = 0; i < row; i++) {
		for (int j = 0; j < col; j++) {
			IV1[i * col + j] = 0;
		}
	}

	//遍历图像
	for (int i = int(w1 / 2); i < row - int(w1 / 2); i++) {
		for (int j = int(w1 / 2); j < col - int(w1 / 2); j++) {
			V0 = 0;
			V45 = 0;
			V90 = 0;
			V135 = 0;
			//min = 0;
			for (int k = -int(w1 / 2); k < int(w1 / 2); k++) {
				V0 += (pImg[(i + k) * col + j] - pImg[(i + k + 1) * col + j]) * (pImg[(i + k) * col + j] - pImg[(i + k + 1) * col + j]);
				V45 += (pImg[(i + k) * col + j + k] - pImg[(i + k + 1) * col + j + k + 1]) * (pImg[(i + k) * col + j + k] - pImg[(i + k + 1) * col + j + k + 1]);
				V90 += (pImg[i * col + j + k] - pImg[i * col + j + k + 1]) * (pImg[i * col + j + k] - pImg[i * col + j + k + 1]);
				V135 += (pImg[(i + k) * col + j - k] - pImg[(i + k + 1) * col + j - k - 1]) * (pImg[(i + k) * col + j - k] - pImg[(i + k + 1) * col + j - k - 1]);
			}
			MinIV = min(min(V0, V45), min(V90, V135));
			IV1[i * col + j] = MinIV;
		}
	}

	for (int i = 0; i < row; i++) {
		for (int j = 0; j < col; j++) {
			if (IV1[i * col + j] < threshold)
				IV1[i * col + j] = 0;
		}
	}

	int w2 = 15; 
	int Xm, Ym;
	float max_v;

	Mat img_fp = Mat::zeros(row, col, 0);

	
	for (int i = int(w2 / 2); i < row - int(w2 / 2); i += w2) {
		for (int j = int(w2 / 2); j < col - int(w2 / 2); j++) {
			max_v = 0;
			Xm = -1;
			Ym = -1;
			for (int m = -int(w2 / 2); m<int(w2 / 2) + 1; m++) {
				for (int n = -int(w2 / 2); n<int(w2 / 2) + 1; n++) {
					if (max_v < IV1[(i + m) * col + j + n]) {
						max_v = IV1[(i + m) * col + j + n];
						Xm = i + m;
						Ym = j + n;
					}
				}
				if (Xm >= 0 && Ym >= 0) {
					img_fp.at<uchar>(Xm, Ym) = 255;
					Point2i p1(Ym - 7, Xm - 7), p2(Ym + 7, Xm + 7);
					Point2i p3(Ym - 7, Xm + 7), p4(Ym + 7, Xm - 7);
					line(img, p1, p2, Scalar(255, 255, 255));
					line(img, p3, p4, Scalar(255, 255, 255));
				}
			}
		}

	}
	imwrite(OutputPath, img_fp);
	imwrite("Moravec.bmp", img);
	waitKey();
}

void ImageMatch(char* Path, Mat Img_left, Mat Img_right)
{
	Mat img_fp = imread(Path, 0);
	int row = Img_right.rows;
	int col = Img_right.cols;

	int fp_x = 0;
	int fp_y = 0;
	int W_tar = 9;//目标窗口大小

	float temp1, temp2, temp3, temp4, temp5, temp6, temp7;
	float temp;
	int M1, M2;

	//CCoe存放待匹配影像各个像元与某一特征点的相关系数
	float CCoe;

	for (int i = 30; i < 900; i++) {
		for (int j = 30; j < 900; j++) {
			if (img_fp.at<uchar>(i, j) == 255) {
				temp = 0;
				for (int a = int(W_tar / 2); a < row - int(W_tar / 2); a++) {
					for (int b = int(W_tar / 2); b < col - int(W_tar / 2); b++) {
						temp1 = 0;
						temp2 = 0;
						temp3 = 0;
						temp4 = 0;
						temp5 = 0;
						temp6 = 0;
						temp7 = 0;
						//在窗口上进行遍历搜寻匹配点
						for (int m = -int(W_tar / 2); m<int(W_tar / 2); m++) {
							for (int n = -int(W_tar / 2); n<int(W_tar / 2); n++) {
								M1 = Img_left.at<uchar>(i + m, j + n);
								M2 = Img_right.at<uchar>(a + m, b + n);
								temp1 += M1 * M2;
								temp2 += M1;
								temp3 += M2;
								temp4 += M1 * M1;
								temp5 += M2 * M2;
							}
						}
						temp6 = temp4 - (1 / W_tar * W_tar) * temp2 * temp2;
						temp7 = temp5 - (1 / W_tar * W_tar) * temp3 * temp3;

						CCoe = (temp1 - (1 / W_tar * W_tar) * temp2 * temp3) / sqrt(temp6 * temp7);
						if (temp < CCoe) {
							temp = CCoe;
							fp_x = a;
							fp_y = b;
						}
					}
				}

				Point2i p1(fp_y - 7, fp_x - 7), p2(fp_y + 7, fp_x + 7);
				Point2i p3(fp_y - 7, fp_x + 7), p4(fp_y + 7, fp_x - 7);
				line(Img_right, p1, p2, Scalar(255, 0, 0));
				line(Img_right, p3, p4, Scalar(255, 0, 0));
			}
		}
	}
	imwrite("Result.bmp", Img_right);
}
