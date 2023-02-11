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

struct Shape //ͼ������
{
	vector<Point> points; //�㼯
	int circumference; //�ܳ�
	int area; //���
	double R; //Բ�ζ�
	Point center; //����
	double M[2]; //Hu��
};

Mat Img2gray(const Mat &src) //ͼ��ҶȻ�
{ 
	unsigned char *pImg = src.data;
	Mat imgGray;
	imgGray.create(src.rows, src.cols, CV_8UC1);
	unsigned char *pGray = imgGray.data;

	for (int i = 0; i < src.rows; i++) 
	{
		for (int j = 0; j < src.cols; j++) 
		{
			if (src.channels()>1) //��ɫͼ��
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

void Average(Mat &imgGray) // ��ֵ�˲�
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
			for (int y = 0; y < size; y++) //���
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

void OTSU(Mat &imgGray) // �����䷽���ֵ��
{ 
	unsigned char *pGray = imgGray.data;
	int Cnt[256] = { 0 }, Sum = imgGray.rows*imgGray.cols, threshold; //Cnt�洢��Ӧ�Ҷ����ظ�����SumΪ����������thresholdΪ��ֵ
	double Pro[256] = { 0 }; //Ƶ��
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
				w0 += Pro[j]; //����Ƶ��
				u0t += j * Pro[j];
			}
			else 
			{
				w1 += Pro[j]; //ǰ��Ƶ��
				u1t += j * Pro[j];
			}
		}
		u0 = u0t / w0; //������ֵ
		u1 = u1t / w1; //ǰ����ֵ
		u = u0t + u1t; //�ܾ�ֵ
		variance = w0 * (u0 - u)*(u0 - u) + w1 * (u1 - u)*(u1 - u); //��䷽��
		if (variance > varianceMax)
		{
			varianceMax = variance;
			threshold = i; //iΪʹĿǰ��䷽������ֵ
		}
	}
	for (int i = 0; i<imgGray.rows; i++)
		for (int j = 0; j<imgGray.cols; j++) {
			if (pGray[i*imgGray.cols + j] >= threshold)
				pGray[i*imgGray.cols + j] = 255; //ǰ��
			else
				pGray[i*imgGray.cols + j] = 0; //����
		}
}

void Label_2steps(const Mat &src, Mat &dst, int &shapesSum) //��ͨ�ɷֱ��-������|�����ֵͼ��src,dst�洢��Ǳ�,shapesSum�洢��ͨ������
{
	// ��һ�α���
	unsigned char *pSrc = src.data;
	int label = 0; //labelΪ�������
	vector<int> parent(1); //parent�洢���֮������ͽṹ��ϵ,parent[i]��ʾ���i��˫�׽��,parent[i]=0ʱiΪ�����,0�ŵ�Ԫ����
	int *labelMtrix = new int[src.rows*src.cols](); //��ʱ��Ǿ���
	dst = Mat::zeros(src.size(), src.type());
	unsigned char *pDst = dst.data;
	for (int i = 0; i < src.rows; i++) 
	{
		for (int j = 0; j < src.cols; j++) 
		{
			if (pSrc[i*src.cols + j] == 255) //ǰ����������
			{ 
				int left = j - 1 < 0 ? 0 : labelMtrix[i*src.cols + j - 1]; //������ֵ
				int up = i - 1 < 0 ? 0 : labelMtrix[(i - 1)*src.cols + j]; //������ֵ
				if (left == 0 && up == 0) //�������
				{
					labelMtrix[i*src.cols + j] = ++label;
					parent.push_back(0);
				}
				else 
				{
					if (left != 0 && up != 0) //��left��up����ͬһ����
					{ 
						labelMtrix[i*src.cols + j] = min(left, up); //���ȡ��Сֵ
						int pmin = min(left, up), pmax = max(left, up);
						while (parent[pmin] != 0)
							pmin = parent[pmin];
						while (parent[pmax] != 0)
							pmax = parent[pmax];
						if (pmin != pmax) //�����߸���㲻ͬ������Сֵ��Ϊ�ϴ�ֵ��˫�׽��
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
	// �ڶ��α���
	map<int, int> label2idx; //�洢���������ŵĶ�Ӧ��ϵ
	for (int i = 0; i < src.rows; i++) 
	{
		for (int j = 0; j < src.cols; j++) 
		{
			if (pSrc[i*src.cols + j] == 255) //���±��
			{ 
				int p = labelMtrix[i*src.cols + j];
				while (parent[p] != 0)
					p = parent[p]; //�ҵ���Ӧ�ĸ����
				map<int, int>::iterator itr;
				itr = label2idx.find(p);
				if (itr == label2idx.end())
					label2idx[p] = (int)label2idx.size() + 1; //�������������ŵĶ�Ӧ��ϵ
				pDst[i*dst.cols + j] = label2idx[p]; //���ձ��Ϊ������Ӧ���
			}
		}
	}
	shapesSum = (int)label2idx.size();
	delete[] labelMtrix;
}

void Label_seed(const Mat &src, Mat &dst, int &shapesSum) //��ͨ�ɷֱ��-������䷨|�����ֵͼ��src,dst�洢��Ǳ�,shapesSum�洢��ͨ������
{
	int label = 0;//��ͨ���������
	unsigned char *pSrc = src.data;
	int height = src.rows, width = src.cols;
	dst = Mat::zeros(src.size(), src.type());
	unsigned char *pDst = dst.data;
	stack<Point> neighbors; //ջ
	for (int i = 0; i < height; i++) 
	{
		for (int j = 0; j < width; j++) 
		{
			if ((pSrc[i * width + j] == 255) && (pDst[i * width + j] == 0)) //������δ���
			{ 
				label++;
				neighbors.push(Point(j, i)); //��ջ
				while (neighbors.size() != 0) 
				{
					int temi = neighbors.top().y;
					int temj = neighbors.top().x;
					pDst[temi * width + temj] = label;
					neighbors.pop(); //��ջ
					if ((temi>0) && (pSrc[(temi - 1) * width + temj] == 255) && (pDst[(temi - 1) * width + temj] == 0)) //����������Ϊǰ��������������ջ
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

void ImgCompute(vector<Shape> &shapes, const Mat &imgLabel) //��״��������|shapesΪͼ�μ���imgLabelΪ��Ǳ�|��ȡ�㼯
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
	// ��ȡ��������1��ʾ
	Mat Edge(imgLabel.size(), imgLabel.type());
	unsigned char *pEdge = Edge.data;
	for (int i = 0; i<imgLabel.rows; i++)
		for (int j = 0; j < imgLabel.cols; j++)
		{
			if (pLabel[i*imgLabel.cols + j] > 0) 
			{
				if (i == 0 || j == 0 || i == imgLabel.rows - 1 || j == imgLabel.cols - 1) //ͼ��߽�
					pEdge[i*imgLabel.cols + j] = 1;
				else if (pLabel[i*imgLabel.cols + j + 1] == 0 || pLabel[i*imgLabel.cols + j - 1] == 0 ||pLabel[(i + 1)*imgLabel.cols + j] == 0 || pLabel[(i - 1)*imgLabel.cols + j] == 0) // �������д��ڱ���ֵ
					pEdge[i*imgLabel.cols + j] = 1;
				else
					pEdge[i*imgLabel.cols + j] = 0;
			}
			else
				pEdge[i*imgLabel.cols + j] = 0;
		}

	for (size_t i = 0; i < shapes.size(); i++)  //����ͼ��
	{
		shapes[i].circumference = 0; //��ʼ���ܳ�
		int x_sum = 0, y_sum = 0;
		double m11 = 0, m20 = 0, m02 = 0;
		//double tmp = 0;
		for (size_t j = 0; j < shapes[i].points.size(); j++) //�����㼯
		{ 
			int x = shapes[i].points[j].x;
			int y = shapes[i].points[j].y;
			x_sum += x;
			y_sum += y;
			if (pEdge[y*imgLabel.cols + x] == 1) //Ϊ����
				shapes[i].circumference++; //�����ܳ�
			/* �����ܳ�-������
			tmp += (y == 0 ? 0 : pEdge[(y - 1)*imgLabel.cols + x]) + (y == 255 ? 0 : pEdge[(y + 1)*imgLabel.cols + x]) + (x == 0 ? 0 : pEdge[y*imgLabel.cols + x - 1]) + (x == 255 ? 0 : pEdge[y*imgLabel.cols + x + 1]) +
			sqrt(2)*(((y == 0 || x == 0) ? 0 : pEdge[(y - 1)*imgLabel.cols + x - 1]) + ((y == 0 || x == 255) ? 0 : pEdge[(y - 1)*imgLabel.cols + x + 1]) + ((y == 255 || x == 0) ? 0 : pEdge[(y + 1)*imgLabel.cols + x - 1]) + ((y == 255 || x == 255) ? 0 : pEdge[(y + 1)*imgLabel.cols + x + 1]));
			*/
		}
		//shapes[i].circumference = cvRound(tmp / 2); //�����ܳ�-����
		shapes[i].area = (int)shapes[i].points.size(); //�������
		shapes[i].R = 4 * PI*shapes[i].area / (double)(shapes[i].circumference*shapes[i].circumference); //����Բ�ζ�|����һ�׾ؼ�������

		int x_ave = cvRound((double)x_sum / shapes[i].points.size());
		int y_ave = cvRound((double)y_sum / shapes[i].points.size());
		shapes[i].center = Point(x_ave, y_ave);//��������

		// ����ͼ�ε�Hu��(ǰ����)
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

Mat Display(const vector<Shape> &shapes, const Mat &imgLabel) //��״������ʾ|shapesΪͼ�μ���imgLabelΪ��Ǳ�������ʾͼ|���Ⱦɫ
{ 
	unsigned char* pLabel = imgLabel.data;
	Scalar *colors = new Scalar[shapes.size() + 1];
	srand((unsigned)time(NULL)); //��ʱ����Ϊ���������
	colors[0] = Scalar(0, 0, 0); //����

	for (size_t i = 1; i <= shapes.size(); i++) //��ȡ�����ɫ
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

	//ͼ����Ϣ��ʾ
	for (size_t i = 0; i < shapes.size(); i++) 
	{
		stringstream sarea, scir, scenter;
		sarea << "a:" << shapes[i].area; //����ַ���
		int baseline;
		Size text_size = getTextSize(sarea.str(), FONT_HERSHEY_PLAIN, 0.8, 1, &baseline); //��ȡ�ı���ĳ���
		Point pos; //�ı������½�λ��
		pos.x = shapes[i].center.x - text_size.width / 2;
		pos.y = shapes[i].center.y + text_size.height / 2;
		putText(display, sarea.str(), pos, FONT_HERSHEY_PLAIN, 0.8, Scalar(255, 255, 255)); //�ı�����ͼ�����Ĵ���ʾ
		scir << "c:" << shapes[i].circumference; //�ܳ��ַ���
		pos.y -= (text_size.height + 1);
		putText(display, scir.str(), pos, FONT_HERSHEY_PLAIN, 0.8, Scalar(255, 255, 255));
		scenter << "(" << shapes[i].center.x << "," << shapes[i].center.y << ")"; //�����ַ���
		pos.y += 2 * (text_size.height + 1);
		putText(display, scenter.str(), pos, FONT_HERSHEY_PLAIN, 0.8, Scalar(255, 255, 255));
	}

	cout << "���" << "\t" << "���" << "\t" << "�ܳ�" << "\t" << "����" << "\t\t" << "Hu��" << "\t\t" << "Բ�ζ�" << endl;
	for (size_t i = 0; i < shapes.size(); i++)
	{
		cout << i+1 << "\t" << shapes[i].area << "\t" << shapes[i].circumference << "\t" << shapes[i].center << "\t" << shapes[i].M << "\t" << shapes[i].R << endl;
	}

	return display;
}