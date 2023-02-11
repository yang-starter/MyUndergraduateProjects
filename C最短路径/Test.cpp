#include<fstream>
#include<iostream>
#include<string>
#include<vector>
#include"Timer.h"
using namespace std;
#define CityNum 199
#define RouteNum 1975
#define N 1000000
#define TRUE 1
#define FALSE 0

int visited[CityNum];     //遍历数组，遍历图时使用

typedef struct {
	bool pass = false;
	string Country;      //国家名
	string city;         //城市名
	float latitude;      //经度
	float longtitude;    //纬度
}City;

typedef struct {
	string origin_city;      //起点城市
	string destination_city; //终点城市
	string transport;        //交通方式
	string other_information;//其他信息

	float time;              //时间
	float cost;              //花费
}Route;

typedef  struct
{
	City *vertex;
	Route arcs[CityNum][CityNum];  //图的邻接矩阵
	int vexnum;                    //图的节点数，也就是城市数
	int arcnum;                    //矩阵的元素总数
}Graph;

typedef struct
{
	vector<int> path;//这里我运用vector进行路径的储存
}Way;


Graph g;                  //建立图的对象g
Way way[CityNum][CityNum];//设为全局变量的目的就是为了避免栈溢出


bool GetPointsFromFile(const char *FileName, City ct[CityNum])
{
	FILE *fp = fopen(FileName, "r");
	if (!fp) { return false; }

	char ch;   float f;  int i = 0;

	while (!feof(fp))
	{
		ch = fgetc(fp);
		for (; ch != ','; ch = fgetc(fp))
		{
			ct[i].Country += ch;
		}
		ch = fgetc(fp);
		for (; ch != ','; ch = fgetc(fp))
		{
			ct[i].city += ch;
		}
		fscanf(fp, "%f,", &f);
		ct[i].latitude = f;
		fscanf(fp, "%f\n,", &f);
		ct[i].longtitude = f;
		i++;
	}
	fclose(fp);
	return true;
}
//读取城市函数

bool GetRoutesFromFile(const char *FileName, Route route[RouteNum])
{
	FILE *fp2 = fopen(FileName, "r");
	if (!fp2) { cout << "error2!"; return false; }
	char ch; int i = 0; int j = 0;

	ch = fgetc(fp2);
	while (!feof(fp2))
	{
		while (ch != ',')
		{
			route[i].origin_city += ch;
			ch = fgetc(fp2);
		}
		ch = fgetc(fp2);
		while (ch != ',')
		{
			route[i].destination_city += ch;
			ch = fgetc(fp2);
		}
		ch = fgetc(fp2);
		while (ch != ',')
		{
			route[i].transport += ch;
			ch = fgetc(fp2);
		}
		fscanf(fp2, "%f,", &route[i].time);
		fscanf(fp2, "%f,", &route[i].cost);
		ch = fgetc(fp2);
		while (ch != '\n')
		{
			route[i].other_information += ch;
			ch = fgetc(fp2);
		}
		ch = fgetc(fp2);
		i++;
	}
	fclose(fp2);
	return true;
}
//读取路线函数

int Locate(string CityName, City ct[CityNum])
{
	int i = 0;
	while (CityName != ct[i].city)//如果输入的城市名在所给的城市中，则返回该城市在排列中的序号位置
	{
		i++;
	}
	return i;
}
//根据城市名来找到城市的顺序

void CreateGraphforFlight(Way way[CityNum][CityNum], Route route[RouteNum], City *ct)
{
	g.arcnum = CityNum*CityNum;
	g.vexnum = CityNum;
	g.vertex = ct;

	int i = 0, j = 0;

	for (i = 0; i<CityNum; i++)            //初始化邻接矩阵，并未存入任何数据
		for (j = 0; j < CityNum; j++)
		{
			if (i == j)                    //相同两点之间当然不存在路径
			{
				g.arcs[i][j].cost = 0;
				g.arcs[i][j].time = 0;
			}
			else                           //在创建邻接矩阵时，将所有节点间的路径都设置为无穷大为N1000000
			{
				g.arcs[i][j].cost = N;
				g.arcs[i][j].time = N;
			}
		}

	for (i = 0; i < RouteNum; i++)         //这一步就是存在的路径，建立邻接矩阵
	{
		int or , de;
		or = Locate(route[i].origin_city, ct);
		de = Locate(route[i].destination_city, ct);
		g.arcs[or ][de].cost = route[i].cost;
		g.arcs[or ][de].time = route[i].time;
	}
}
//构建图

void shortestPath_DIJ(const Graph& g, int depart, int dest, Way way[][CityNum], float dist[][CityNum])
{
	//depart指的是选定的第一个城市序号 
	//dest指的是选定的第二个城市序号
	//way[][CityNum]指的是路径
	//dist[][CityNum]指的是两城市路径的最少时间
	for (int v = 0; v < g.vexnum; ++v)
	{
		g.vertex[v].pass = false;                //第v个城市未被访问，在初始条件下就是所有的城市都未被访问。
		dist[depart][v] = g.arcs[depart][v].time;//初始选定的城市到第v个城市的时间
	}
	dist[depart][depart] = 0;                    //自身到自身的时间为0；
	g.vertex[depart].pass = true;                //初始选定的城市已经被访问

	for (int i = 0; i < CityNum; i++) 
	{   
 		way[depart][i].path.push_back(depart);   //为depart到其余不同的顶点之间创建路径
		way[depart][i].path.push_back(i);
	}
	way[depart][depart].path.pop_back();         //如果起点和终点相同的话，就要删除添加的点
	 
	for (int i = 0; i < g.vexnum; ++i)           //vexnum - i即为未被访问的剩余的顶点
	{
		int v = 0;    double minTime = N;

		for (int w = 0; w < g.vexnum; ++w)
		{
			if (g.vertex[w].pass == false)       //如果第w个顶点还未被访问
				if (dist[depart][w] < minTime)
				{
					v = w;
					minTime = dist[depart][w];
				}                                //找到最小时间
		}
		g.vertex[v].pass = true;                 //找到与depart城市相距时间最短的城市v，将其标记为已访问。
		
		for (int w = 0; w < g.vexnum; ++w)       //找到从depart点出发的最短路径
		{
			if (g.vertex[w].pass == false && (minTime + g.arcs[v][w].time < dist[depart][w]))
				                                 //如果该开始的最短时间加上城市v到城市w的时间还小于depart到w城市的时间，则最少时间就为
			{
				dist[depart][w] = minTime + g.arcs[v][w].time;  //depart到w城市的最短时间

				way[depart][w].path.clear();     //把depart到w原来的路径都清掉————这一步在实际操作中非常有用，如果没有clear的话，容易造成溢出
				way[depart][w].path = way[depart][v].path;//原来depart到v的路径我都要
				way[depart][w].path.push_back(w);//再加上v到w的路径，也就是相当于在way中添加一个点w
			}
		}
	}
}
//迪杰斯特拉算法求最短路径
 
void dfs(int i, Graph *g)
{
	int j;
	cout << g->vertex[i].city << "—>";      //输出遍历的城市

	visited[i] = 1;                          //将遍历过的顶点城市都标记为1
	for (j = 0; j<g->vexnum; j++)
	{  
		if (visited[j] == 0)                 //如果第j个点还没有被遍历过，则调用深度优先遍历函数
		{
			dfs(j, g);                       //递归调用自身，直到与该顶点相连的所有顶点都被遍历到
		}
	}
}
//从第i个顶点出发深度优先遍历

void tdfs(Graph *g) 
{
	int i;
	for (i = 0; i<g->vexnum; i++)
	{
		if (visited[i] != 1)      //如果顶点未被遍历
		{
			dfs(i, g);            //调用dfs函数     
		} 
	}
}
//深度优先遍历整个图

void string_replace(string &strBig, const string &strsrc, const string &strdst)
{
	string::size_type pos = 0;                                    //pos是被替换字符串的位置
	string::size_type srclen = strsrc.size();                     //srclen是被替换字符串的长度
	string::size_type dstlen = strdst.size();                     //dstlen是替换字符串的长度

	while ((pos = strBig.find(strsrc, pos)) != string::npos)      //find函数是找到pos的位置		                                            
	{
		strBig.replace(pos, srclen, strdst);                      //replace函数是string类型自带的替换函数
		pos += dstlen;
	}
}
//进行字符串字某个字符的替换


int main()
{
	const char *FileName1 = "D://cities.csv";
	const char *FileName2 = "D://routes.csv";
	City ct[CityNum];
	Route route[RouteNum];


	Timer timer;
	timer.Start();//计时开始

	GetPointsFromFile(FileName1, ct);
	GetRoutesFromFile(FileName2, route);

	float dist[CityNum][CityNum];                 //用来存放最短时间

	string CityName1;
	string CityName2;
	cout << "起始城市" << endl;
	getline(cin, CityName1);
	cout << "终点城市" << endl;
	getline(cin, CityName2);


	int depart = Locate(CityName1, ct);           //起始城市确定
	int dest = Locate(CityName2, ct);             //终点城市确定

	CreateGraphforFlight(way, route, ct);         //创建图，包括邻接矩阵

	shortestPath_DIJ(g, depart, dest, way, dist); //求最短路径


	//这些步骤是输出最短路径的
	int i = 0;
	int n = 0;
	int citynum = way[depart][dest].path.size();  //找到最短路径上的成熟数
	int *count = new int[citynum];
	cout << "最短路径为：";

	while (i < citynum - 1)                       //输出每一个城市名
	{
		n = way[depart][dest].path[i];
		count[i] = n;
		cout << g.vertex[n].city << "——>";
		i++;
	}n = way[depart][dest].path[i];
	count[i] = n;
	cout << g.vertex[n].city;


	//这一步是输出最短时间的
	cout << "最短路径花费的总时间为：" << dist[depart][dest] << endl;

	//初始化访问数组，然后进行遍历
	for (int i = 0; i < CityNum; i++)
	{
		visited[i] = 0;                            //初始化访问数组;
	}
	cout << "从顶点开始进行遍历";
	tdfs(&g);


	//绘图：
	ofstream ofs;
	int m_makers = citynum;                        //需要在地图上绘制的点数
	i = 0;
	string file =  "D://ShortPath.html";          //可视化文件储存的路径
	ofs.open(file);
	ofs << "<!DOCTYPE html><html><head><style type='text/css'>body, html{width: 100%;height: 100%;margin:0;font-family:'微软雅黑';}#allmap{height:100%;width:100%;}#r-result{width:100%;}</style><script type='text/javascript' src='http://api.map.baidu.com/api?v=2.0&ak=nSxiPohfziUaCuONe4ViUP2N'></script><title>Shortest path from Beijing to London</title></head>";
	ofs << "<body><div id='allmap'></div></div></body>";
	ofs << "</html>";
	ofs << "<script type='text/javascript'>var map = new BMap.Map('allmap');var point = new BMap.Point(0, 0);map.centerAndZoom(point, 2);map.enableScrollWheelZoom(true);";
	
	//这里特别注意的一点就是有的城市名的格式可能会在可视化过程中产生bug，所以构造了一个字符转换的函数
	//因为如果城市或者国家名中有英文标点单引号' ' ',则不能可视化；需要将其转化为中文标点单引号' ’ '
	string_replace(g.vertex[count[i]].Country, "'", "‘");
	string_replace(g.vertex[count[i]].city, "'", "‘");

	ofs << "var marker" << i << "= new BMap.Marker(new BMap.Point(" << g.vertex[count[i]].longtitude << "," << g.vertex[count[i]].latitude << " )); map.addOverlay(marker" << i << ");";
	ofs << "var infoWindow" << i << " = new BMap.InfoWindow(\"<p style = 'font-size:14px;'>country:" << g.vertex[count[i]].Country << "<br/>city : " << g.vertex[count[i]].city << "</p>\");";
	ofs << "marker" << i << ".addEventListener(\"click\", function(){this.openInfoWindow(infoWindow" << i << "); });";

	for (i = 1; i < m_makers; i++)//地图上需要画多少点
	{
		string_replace(g.vertex[count[i]].Country, "'", "‘");
		string_replace(g.vertex[count[i]].city, "'", "‘");

		ofs << "var marker" << i << "= new BMap.Marker(new BMap.Point(" << g.vertex[count[i]].longtitude << "," << g.vertex[count[i]].latitude << " )); map.addOverlay(marker" << i << ");";
		ofs << "var infoWindow" << i <<" = new BMap.InfoWindow(\"<p style = 'font-size:14px;'>country:" << g.vertex[count[i]].Country << "<br/>city : " << g.vertex[count[i]].city << "</p>\");";
		ofs << "marker" << i << ".addEventListener(\"click\", function(){this.openInfoWindow(infoWindow" << i << "); });";

		ofs << "var contentString0" << i << "= '" << g.vertex[count[i - 1]].city << "," << g.vertex[count[i - 1]].Country << "-->" << g.vertex[count[i]].city << "," << g.vertex[count[i]].Country << "(" << g.arcs[count[i-1]][count[i]].transport << "-" << g.arcs[count[i - 1]][count[i]].time << "hours - $ - " << g.arcs[count[i - 1]][count[i]].cost <<")';";
		                                                                                                                                                                                             

		ofs << "var path" << i << " = new BMap.Polyline([new BMap.Point(" << g.vertex[count[i - 1]].longtitude << "," << g.vertex[count[i - 1]].latitude << "), new BMap.Point(" << g.vertex[count[i]].longtitude << "," << g.vertex[count[i]].latitude << ")], { strokeColor:'#18a45b', strokeWeight : 8, strokeOpacity : 0.8 });";
		ofs << "map.addOverlay(path" << i << ");";
		ofs << "path" << i << ".addEventListener(\"click\", function(){alert(contentString0" << i << ");});";
	}

	ofs << "</script>";
	ofs.close();


	delete[]count;//释放内存空间
	for (int w = 0; w < CityNum; w++)
	{
		way[depart][w].path.clear();
	}


	timer.Stop(); //计时停止
	printf("\nElapsed time is: <%4.2lf> ms\n", timer.ElapsedTime());
	char c = getchar();
	return 0;
}

