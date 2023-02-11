#pragma once
#include "stdafx.h"
#include "opencv2/opencv.hpp"
#include "opencv2/opencv_modules.hpp"
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <iostream>
#include <sstream>
#include <map>
#include <vector>
#include <stack>

#define PI 3.1415926

using namespace std;
using namespace cv;

struct Shape //图形类型
{
	vector<Point> points; //点集
	int circumference; //周长
	int area; //面积
	double R; //圆形度
	Point center; //重心
	double M[2]; //Hu矩
};

Mat Img2gray(const Mat &src) //图像灰度化
{ 
	unsigned char *pImg = src.data;
	Mat imgGray;
	imgGray.create(src.rows, src.cols, CV_8UC1);
	unsigned char *pGray = imgGray.data;

	for (int i = 0; i < src.rows; i++) 
	{
		for (int j = 0; j < src.cols; j++) 
		{
			if (src.channels()>1) //彩色图像
			{ 
				int b, g, r;
				b = pImg[(i *src.cols + j) * 3 + 0];
				g = pImg[(i *src.cols + j) * 3 + 1];
				r = pImg[(i *src.cols + j) * 3 + 2];
				pGray[i*src.cols + j] = (r + g + b) / 3;
			}
			else
			{
				pGray[i*src.cols + j] = pImg[i*src.cols + j];
			}
		}
	}
	return imgGray;
}

void Average(Mat &imgGray) // 均值滤波
{ 
	unsigned char *pGray = imgGray.data;
	Mat imgTemp;
	imgTemp.create(imgGray.rows, imgGray.cols, CV_8UC1);
	unsigned char *pImgTemp = imgTemp.data;
	int size = 3;
	int average[] = { 1,1,1,1,1,1,1,1,1 };

	for (int i = size / 2; i < imgGray.rows - size / 2; i++) 
	{
		for (int j = size / 2; j < imgGray.rows - size / 2; j++) 
		{
			int tmp = 0;
			for (int y = 0; y < size; y++) //卷积
			{ 
				for (int x = 0; x < size; x++) 
				{
					tmp += average[y*size + x] * (int)pGray[(i - size / 2 + y)*imgGray.cols + (j - size / 2 + x)];
				}
			}
			pImgTemp[i*imgGray.cols + j] = cvRound((double)tmp / 9);
		}
	}
	for (int i = size / 2; i < imgGray.rows - size / 2; i++) 
	{
		for (int j = size / 2; j < imgGray.rows - size / 2; j++) 
		{
			pGray[i*imgGray.cols + j] = pImgTemp[i*imgGray.cols + j];
		}
	}
}

void OTSU(Mat &imgGray) // 最大类间方差法二值化
{ 
	unsigned char *pGray = imgGray.data;
	int Cnt[256] = { 0 }, Sum = imgGray.rows*imgGray.cols, threshold; //Cnt存储对应灰度像素个数，Sum为像素总数，threshold为阈值
	double Pro[256] = { 0 }; //频率
	for (int i = 0; i<imgGray.rows; i++)
		for (int j = 0; j<imgGray.cols; j++)
			Cnt[pGray[i*imgGray.cols + j]]++;
	for (int i = 0; i<256; i++)
		Pro[i] = (double)Cnt[i] / Sum;
	double w0, w1, u0, u1, u0t, u1t, u, variance, varianceMax = 0;

	for (int i = 0; i<256; i++) 
	{
		w0 = w1 = u0 = u1 = u0t = u1t = u = variance = 0;
		for (int j = 0; j<256; j++) 
		{
			if (j <= i) 
			{
				w0 += Pro[j]; //背景频率
				u0t += j * Pro[j];
			}
			else 
			{
				w1 += Pro[j]; //前景频率
				u1t += j * Pro[j];
			}
		}
		u0 = u0t / w0; //背景均值
		u1 = u1t / w1; //前景均值
		u = u0t + u1t; //总均值
		variance = w0 * (u0 - u)*(u0 - u) + w1 * (u1 - u)*(u1 - u); //类间方差
		if (variance > varianceMax)
		{
			varianceMax = variance;
			threshold = i; //i为使目前类间方差最大的值
		}
	}
	for (int i = 0; i<imgGray.rows; i++)
		for (int j = 0; j<imgGray.cols; j++) {
			if (pGray[i*imgGray.cols + j] >= threshold)
				pGray[i*imgGray.cols + j] = 255; //前景
			else
				pGray[i*imgGray.cols + j] = 0; //背景
		}
}

void Label_2steps(const Mat &src, Mat &dst, int &shapesSum) //连通成分标记-两步法|输入二值图像src,dst存储标记表,shapesSum存储连通域数量
{
	// 第一次遍历
	unsigned char *pSrc = src.data;
	int label = 0; //label为标记数字
	vector<int> parent(1); //parent存储标记之间的树型结构关系,parent[i]表示标记i的双亲结点,parent[i]=0时i为根结点,0号单元弃用
	int *labelMtrix = new int[src.rows*src.cols](); //临时标记矩阵
	dst = Mat::zeros(src.size(), src.type());
	unsigned char *pDst = dst.data;
	for (int i = 0; i < src.rows; i++) 
	{
		for (int j = 0; j < src.cols; j++) 
		{
			if (pSrc[i*src.cols + j] == 255) //前景区域，需标记
			{ 
				int left = j - 1 < 0 ? 0 : labelMtrix[i*src.cols + j - 1]; //左像素值
				int up = i - 1 < 0 ? 0 : labelMtrix[(i - 1)*src.cols + j]; //上像素值
				if (left == 0 && up == 0) //新增标记
				{
					labelMtrix[i*src.cols + j] = ++label;
					parent.push_back(0);
				}
				else 
				{
					if (left != 0 && up != 0) //将left与up归于同一树中
					{ 
						labelMtrix[i*src.cols + j] = min(left, up); //标记取较小值
						int pmin = min(left, up), pmax = max(left, up);
						while (parent[pmin] != 0)
							pmin = parent[pmin];
						while (parent[pmax] != 0)
							pmax = parent[pmax];
						if (pmin != pmax) //若二者根结点不同，将较小值设为较大值的双亲结点
							parent[pmax] = pmin;
					}
					else
					{
						labelMtrix[i*src.cols + j] = max(left, up);
					}
				}
			}
		}
	}
	// 第二次遍历
	map<int, int> label2idx; //存储根结点与序号的对应关系
	for (int i = 0; i < src.rows; i++) 
	{
		for (int j = 0; j < src.cols; j++) 
		{
			if (pSrc[i*src.cols + j] == 255) //更新标记
			{ 
				int p = labelMtrix[i*src.cols + j];
				while (parent[p] != 0)
					p = parent[p]; //找到对应的根结点
				map<int, int>::iterator itr;
				itr = label2idx.find(p);
				if (itr == label2idx.end())
					label2idx[p] = (int)label2idx.size() + 1; //建立根结点与序号的对应关系
				pDst[i*dst.cols + j] = label2idx[p]; //最终标记为根结点对应序号
			}
		}
	}
	shapesSum = (int)label2idx.size();
	delete[] labelMtrix;
}

void Label_seed(const Mat &src, Mat &dst, int &shapesSum) //连通成分标记-种子填充法|输入二值图像src,dst存储标记表,shapesSum存储连通域数量
{
	int label = 0;//连通区域的数量
	unsigned char *pSrc = src.data;
	int height = src.rows, width = src.cols;
	dst = Mat::zeros(src.size(), src.type());
	unsigned char *pDst = dst.data;
	stack<Point> neighbors; //栈
	for (int i = 0; i < height; i++) 
	{
		for (int j = 0; j < width; j++) 
		{
			if ((pSrc[i * width + j] == 255) && (pDst[i * width + j] == 0)) //需标记且未标记
			{ 
				label++;
				neighbors.push(Point(j, i)); //入栈
				while (neighbors.size() != 0) 
				{
					int temi = neighbors.top().y;
					int temj = neighbors.top().x;
					pDst[temi * width + temj] = label;
					neighbors.pop(); //出栈
					if ((temi>0) && (pSrc[(temi - 1) * width + temj] == 255) && (pDst[(temi - 1) * width + temj] == 0)) //若领域像素为前景，将其坐标入栈
					{ 
						neighbors.push(Point(temj, temi - 1));
					}
					if ((temj>0) && (pSrc[temi * width + (temj - 1)] == 255) && (pDst[temi * width + (temj - 1)] == 0)) 
					{
						neighbors.push(Point(temj - 1, temi));
					}
					if ((temj<width - 1) && (pSrc[temi * width + (temj + 1)] == 255) && (pDst[temi * width + (temj + 1)] == 0))
					{
						neighbors.push(Point(temj + 1, temi));
					}
					if ((temi<height - 1) && (pSrc[(temi + 1) * width + temj] == 255) && (pDst[(temi + 1) * width + temj] == 0)) 
					{
						neighbors.push(Point(temj, temi + 1));
					}
				}
			}
		}
	}
	shapesSum = label;
}

void ImgCompute(vector<Shape> &shapes, const Mat &imgLabel) //形状特征计算|shapes为图形集，imgLabel为标记表|读取点集
{ 
	unsigned char *pLabel = imgLabel.data;
	for (int i = 0; i < imgLabel.rows; i++)
		for (int j = 0; j < imgLabel.cols; j++)
		{
			if (pLabel[i*imgLabel.cols + j] > 0)
			{
				Point tmp(j, i);
				shapes[pLabel[i*imgLabel.cols + j] - 1].points.push_back(tmp);
			}
		}
	// 提取轮廓，以1表示
	Mat Edge(imgLabel.size(), imgLabel.type());
	unsigned char *pEdge = Edge.data;
	for (int i = 0; i<imgLabel.rows; i++)
		for (int j = 0; j < imgLabel.cols; j++)
		{
			if (pLabel[i*imgLabel.cols + j] > 0) 
			{
				if (i == 0 || j == 0 || i == imgLabel.rows - 1 || j == imgLabel.cols - 1) //图像边界
					pEdge[i*imgLabel.cols + j] = 1;
				else if (pLabel[i*imgLabel.cols + j + 1] == 0 || pLabel[i*imgLabel.cols + j - 1] == 0 ||pLabel[(i + 1)*imgLabel.cols + j] == 0 || pLabel[(i - 1)*imgLabel.cols + j] == 0) // 四领域中存在背景值
					pEdge[i*imgLabel.cols + j] = 1;
				else
					pEdge[i*imgLabel.cols + j] = 0;
			}
			else
				pEdge[i*imgLabel.cols + j] = 0;
		}

	for (size_t i = 0; i < shapes.size(); i++)  //遍历图形
	{
		shapes[i].circumference = 0; //初始化周长
		int x_sum = 0, y_sum = 0;
		double m11 = 0, m20 = 0, m02 = 0;
		//double tmp = 0;
		for (size_t j = 0; j < shapes[i].points.size(); j++) //遍历点集
		{ 
			int x = shapes[i].points[j].x;
			int y = shapes[i].points[j].y;
			x_sum += x;
			y_sum += y;
			if (pEdge[y*imgLabel.cols + x] == 1) //为轮廓
				shapes[i].circumference++; //计算周长
			/* 计算周长-方法二
			tmp += (y == 0 ? 0 : pEdge[(y - 1)*imgLabel.cols + x]) + (y == 255 ? 0 : pEdge[(y + 1)*imgLabel.cols + x]) + (x == 0 ? 0 : pEdge[y*imgLabel.cols + x - 1]) + (x == 255 ? 0 : pEdge[y*imgLabel.cols + x + 1]) +
			sqrt(2)*(((y == 0 || x == 0) ? 0 : pEdge[(y - 1)*imgLabel.cols + x - 1]) + ((y == 0 || x == 255) ? 0 : pEdge[(y - 1)*imgLabel.cols + x + 1]) + ((y == 255 || x == 0) ? 0 : pEdge[(y + 1)*imgLabel.cols + x - 1]) + ((y == 255 || x == 255) ? 0 : pEdge[(y + 1)*imgLabel.cols + x + 1]));
			*/
		}
		//shapes[i].circumference = cvRound(tmp / 2); //计算周长-法二
		shapes[i].area = (int)shapes[i].points.size(); //计算面积
		shapes[i].R = 4 * PI*shapes[i].area / (double)(shapes[i].circumference*shapes[i].circumference); //计算圆形度|利用一阶矩计算重心

		int x_ave = cvRound((double)x_sum / shapes[i].points.size());
		int y_ave = cvRound((double)y_sum / shapes[i].points.size());
		shapes[i].center = Point(x_ave, y_ave);//计算重心

		// 计算图形的Hu矩(前两个)
		double m00 = shapes[i].area;
		for (size_t j = 0; j < shapes[i].points.size(); j++) 
		{
			int x = shapes[i].points[j].x;
			int y = shapes[i].points[j].y;
			m11 += 255 * (x - x_ave)*(y - y_ave);
			m20 += 255 * (y - y_ave)*(y - y_ave);
			m02 += 255 * (x - x_ave)*(x - x_ave);
		}
		double u20 = m20 / (m00 * m00), u02 = m02 / (m00 * m00), u11 = m11 / (m00 * m00);
		shapes[i].M[0] = u20 + u02;
		shapes[i].M[1] = (u20 - u02)*(u20 - u02) + 4 * u11*u11;
	}
}

Mat Display(const vector<Shape> &shapes, const Mat &imgLabel) //形状特征显示|shapes为图形集，imgLabel为标记表，返回显示图|随机染色
{ 
	unsigned char* pLabel = imgLabel.data;
	Scalar *colors = new Scalar[shapes.size() + 1];
	srand((unsigned)time(NULL)); //以时间作为随机数种子
	colors[0] = Scalar(0, 0, 0); //背景

	for (size_t i = 1; i <= shapes.size(); i++) //获取随机颜色
	{ 
		unsigned char b = rand() % 256, g = rand() % 256, r = rand() % 256;
		colors[i] = Scalar(b, g, r);
	}
	Mat display(imgLabel.rows, imgLabel.cols, CV_8UC3);
	unsigned char* pDisplay = display.data;
	for (int i = 0; i<display.rows; i++)
		for (int j = 0; j<display.cols; j++)
			for (int k = 0; k<3; k++)
				pDisplay[(i *imgLabel.cols + j) * 3 + k] = (unsigned char)colors[pLabel[i*imgLabel.cols + j]][k];
	delete[] colors;

	//图形信息显示
	for (size_t i = 0; i < shapes.size(); i++) 
	{
		stringstream sarea, scir, scenter;
		sarea << "a:" << shapes[i].area; //面积字符串
		int baseline;
		Size text_size = getTextSize(sarea.str(), FONT_HERSHEY_PLAIN, 0.8, 1, &baseline); //获取文本框的长宽
		Point pos; //文本框左下角位置
		pos.x = shapes[i].center.x - text_size.width / 2;
		pos.y = shapes[i].center.y + text_size.height / 2;
		putText(display, sarea.str(), pos, FONT_HERSHEY_PLAIN, 0.8, Scalar(255, 255, 255)); //文本框在图形重心处显示
		scir << "c:" << shapes[i].circumference; //周长字符串
		pos.y -= (text_size.height + 1);
		putText(display, scir.str(), pos, FONT_HERSHEY_PLAIN, 0.8, Scalar(255, 255, 255));
		scenter << "(" << shapes[i].center.x << "," << shapes[i].center.y << ")"; //重心字符串
		pos.y += 2 * (text_size.height + 1);
		putText(display, scenter.str(), pos, FONT_HERSHEY_PLAIN, 0.8, Scalar(255, 255, 255));
	}

	cout << "标号" << "\t" << "面积" << "\t" << "周长" << "\t" << "重心" << "\t\t" << "Hu矩" << "\t\t" << "圆形度" << endl;
	for (size_t i = 0; i < shapes.size(); i++)
	{
		cout << i+1 << "\t" << shapes[i].area << "\t" << shapes[i].circumference << "\t" << shapes[i].center << "\t" << shapes[i].M << "\t" << shapes[i].R << endl;
	}

	return display;
}