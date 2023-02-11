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

int visited[CityNum];     //�������飬����ͼʱʹ��

typedef struct {
	bool pass = false;
	string Country;      //������
	string city;         //������
	float latitude;      //����
	float longtitude;    //γ��
}City;

typedef struct {
	string origin_city;      //������
	string destination_city; //�յ����
	string transport;        //��ͨ��ʽ
	string other_information;//������Ϣ

	float time;              //ʱ��
	float cost;              //����
}Route;

typedef  struct
{
	City *vertex;
	Route arcs[CityNum][CityNum];  //ͼ���ڽӾ���
	int vexnum;                    //ͼ�Ľڵ�����Ҳ���ǳ�����
	int arcnum;                    //�����Ԫ������
}Graph;

typedef struct
{
	vector<int> path;//����������vector����·���Ĵ���
}Way;


Graph g;                  //����ͼ�Ķ���g
Way way[CityNum][CityNum];//��Ϊȫ�ֱ�����Ŀ�ľ���Ϊ�˱���ջ���


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
//��ȡ���к���

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
//��ȡ·�ߺ���

int Locate(string CityName, City ct[CityNum])
{
	int i = 0;
	while (CityName != ct[i].city)//�������ĳ������������ĳ����У��򷵻ظó����������е����λ��
	{
		i++;
	}
	return i;
}
//���ݳ��������ҵ����е�˳��

void CreateGraphforFlight(Way way[CityNum][CityNum], Route route[RouteNum], City *ct)
{
	g.arcnum = CityNum*CityNum;
	g.vexnum = CityNum;
	g.vertex = ct;

	int i = 0, j = 0;

	for (i = 0; i<CityNum; i++)            //��ʼ���ڽӾ��󣬲�δ�����κ�����
		for (j = 0; j < CityNum; j++)
		{
			if (i == j)                    //��ͬ����֮�䵱Ȼ������·��
			{
				g.arcs[i][j].cost = 0;
				g.arcs[i][j].time = 0;
			}
			else                           //�ڴ����ڽӾ���ʱ�������нڵ���·��������Ϊ�����ΪN1000000
			{
				g.arcs[i][j].cost = N;
				g.arcs[i][j].time = N;
			}
		}

	for (i = 0; i < RouteNum; i++)         //��һ�����Ǵ��ڵ�·���������ڽӾ���
	{
		int or , de;
		or = Locate(route[i].origin_city, ct);
		de = Locate(route[i].destination_city, ct);
		g.arcs[or ][de].cost = route[i].cost;
		g.arcs[or ][de].time = route[i].time;
	}
}
//����ͼ

void shortestPath_DIJ(const Graph& g, int depart, int dest, Way way[][CityNum], float dist[][CityNum])
{
	//departָ����ѡ���ĵ�һ��������� 
	//destָ����ѡ���ĵڶ����������
	//way[][CityNum]ָ����·��
	//dist[][CityNum]ָ����������·��������ʱ��
	for (int v = 0; v < g.vexnum; ++v)
	{
		g.vertex[v].pass = false;                //��v������δ�����ʣ��ڳ�ʼ�����¾������еĳ��ж�δ�����ʡ�
		dist[depart][v] = g.arcs[depart][v].time;//��ʼѡ���ĳ��е���v�����е�ʱ��
	}
	dist[depart][depart] = 0;                    //���������ʱ��Ϊ0��
	g.vertex[depart].pass = true;                //��ʼѡ���ĳ����Ѿ�������

	for (int i = 0; i < CityNum; i++) 
	{   
 		way[depart][i].path.push_back(depart);   //Ϊdepart�����಻ͬ�Ķ���֮�䴴��·��
		way[depart][i].path.push_back(i);
	}
	way[depart][depart].path.pop_back();         //��������յ���ͬ�Ļ�����Ҫɾ����ӵĵ�
	 
	for (int i = 0; i < g.vexnum; ++i)           //vexnum - i��Ϊδ�����ʵ�ʣ��Ķ���
	{
		int v = 0;    double minTime = N;

		for (int w = 0; w < g.vexnum; ++w)
		{
			if (g.vertex[w].pass == false)       //�����w�����㻹δ������
				if (dist[depart][w] < minTime)
				{
					v = w;
					minTime = dist[depart][w];
				}                                //�ҵ���Сʱ��
		}
		g.vertex[v].pass = true;                 //�ҵ���depart�������ʱ����̵ĳ���v��������Ϊ�ѷ��ʡ�
		
		for (int w = 0; w < g.vexnum; ++w)       //�ҵ���depart����������·��
		{
			if (g.vertex[w].pass == false && (minTime + g.arcs[v][w].time < dist[depart][w]))
				                                 //����ÿ�ʼ�����ʱ����ϳ���v������w��ʱ�仹С��depart��w���е�ʱ�䣬������ʱ���Ϊ
			{
				dist[depart][w] = minTime + g.arcs[v][w].time;  //depart��w���е����ʱ��

				way[depart][w].path.clear();     //��depart��wԭ����·�����������������һ����ʵ�ʲ����зǳ����ã����û��clear�Ļ�������������
				way[depart][w].path = way[depart][v].path;//ԭ��depart��v��·���Ҷ�Ҫ
				way[depart][w].path.push_back(w);//�ټ���v��w��·����Ҳ�����൱����way�����һ����w
			}
		}
	}
}
//�Ͻ�˹�����㷨�����·��
 
void dfs(int i, Graph *g)
{
	int j;
	cout << g->vertex[i].city << "��>";      //��������ĳ���

	visited[i] = 1;                          //���������Ķ�����ж����Ϊ1
	for (j = 0; j<g->vexnum; j++)
	{  
		if (visited[j] == 0)                 //�����j���㻹û�б��������������������ȱ�������
		{
			dfs(j, g);                       //�ݹ��������ֱ����ö������������ж��㶼��������
		}
	}
}
//�ӵ�i���������������ȱ���

void tdfs(Graph *g) 
{
	int i;
	for (i = 0; i<g->vexnum; i++)
	{
		if (visited[i] != 1)      //�������δ������
		{
			dfs(i, g);            //����dfs����     
		} 
	}
}
//������ȱ�������ͼ

void string_replace(string &strBig, const string &strsrc, const string &strdst)
{
	string::size_type pos = 0;                                    //pos�Ǳ��滻�ַ�����λ��
	string::size_type srclen = strsrc.size();                     //srclen�Ǳ��滻�ַ����ĳ���
	string::size_type dstlen = strdst.size();                     //dstlen���滻�ַ����ĳ���

	while ((pos = strBig.find(strsrc, pos)) != string::npos)      //find�������ҵ�pos��λ��		                                            
	{
		strBig.replace(pos, srclen, strdst);                      //replace������string�����Դ����滻����
		pos += dstlen;
	}
}
//�����ַ�����ĳ���ַ����滻


int main()
{
	const char *FileName1 = "D://cities.csv";
	const char *FileName2 = "D://routes.csv";
	City ct[CityNum];
	Route route[RouteNum];


	Timer timer;
	timer.Start();//��ʱ��ʼ

	GetPointsFromFile(FileName1, ct);
	GetRoutesFromFile(FileName2, route);

	float dist[CityNum][CityNum];                 //����������ʱ��

	string CityName1;
	string CityName2;
	cout << "��ʼ����" << endl;
	getline(cin, CityName1);
	cout << "�յ����" << endl;
	getline(cin, CityName2);


	int depart = Locate(CityName1, ct);           //��ʼ����ȷ��
	int dest = Locate(CityName2, ct);             //�յ����ȷ��

	CreateGraphforFlight(way, route, ct);         //����ͼ�������ڽӾ���

	shortestPath_DIJ(g, depart, dest, way, dist); //�����·��


	//��Щ������������·����
	int i = 0;
	int n = 0;
	int citynum = way[depart][dest].path.size();  //�ҵ����·���ϵĳ�����
	int *count = new int[citynum];
	cout << "���·��Ϊ��";

	while (i < citynum - 1)                       //���ÿһ��������
	{
		n = way[depart][dest].path[i];
		count[i] = n;
		cout << g.vertex[n].city << "����>";
		i++;
	}n = way[depart][dest].path[i];
	count[i] = n;
	cout << g.vertex[n].city;


	//��һ����������ʱ���
	cout << "���·�����ѵ���ʱ��Ϊ��" << dist[depart][dest] << endl;

	//��ʼ���������飬Ȼ����б���
	for (int i = 0; i < CityNum; i++)
	{
		visited[i] = 0;                            //��ʼ����������;
	}
	cout << "�Ӷ��㿪ʼ���б���";
	tdfs(&g);


	//��ͼ��
	ofstream ofs;
	int m_makers = citynum;                        //��Ҫ�ڵ�ͼ�ϻ��Ƶĵ���
	i = 0;
	string file =  "D://ShortPath.html";          //���ӻ��ļ������·��
	ofs.open(file);
	ofs << "<!DOCTYPE html><html><head><style type='text/css'>body, html{width: 100%;height: 100%;margin:0;font-family:'΢���ź�';}#allmap{height:100%;width:100%;}#r-result{width:100%;}</style><script type='text/javascript' src='http://api.map.baidu.com/api?v=2.0&ak=nSxiPohfziUaCuONe4ViUP2N'></script><title>Shortest path from Beijing to London</title></head>";
	ofs << "<body><div id='allmap'></div></div></body>";
	ofs << "</html>";
	ofs << "<script type='text/javascript'>var map = new BMap.Map('allmap');var point = new BMap.Point(0, 0);map.centerAndZoom(point, 2);map.enableScrollWheelZoom(true);";
	
	//�����ر�ע���һ������еĳ������ĸ�ʽ���ܻ��ڿ��ӻ������в���bug�����Թ�����һ���ַ�ת���ĺ���
	//��Ϊ������л��߹���������Ӣ�ı�㵥����' ' ',���ܿ��ӻ�����Ҫ����ת��Ϊ���ı�㵥����' �� '
	string_replace(g.vertex[count[i]].Country, "'", "��");
	string_replace(g.vertex[count[i]].city, "'", "��");

	ofs << "var marker" << i << "= new BMap.Marker(new BMap.Point(" << g.vertex[count[i]].longtitude << "," << g.vertex[count[i]].latitude << " )); map.addOverlay(marker" << i << ");";
	ofs << "var infoWindow" << i << " = new BMap.InfoWindow(\"<p style = 'font-size:14px;'>country:" << g.vertex[count[i]].Country << "<br/>city : " << g.vertex[count[i]].city << "</p>\");";
	ofs << "marker" << i << ".addEventListener(\"click\", function(){this.openInfoWindow(infoWindow" << i << "); });";

	for (i = 1; i < m_makers; i++)//��ͼ����Ҫ�����ٵ�
	{
		string_replace(g.vertex[count[i]].Country, "'", "��");
		string_replace(g.vertex[count[i]].city, "'", "��");

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


	delete[]count;//�ͷ��ڴ�ռ�
	for (int w = 0; w < CityNum; w++)
	{
		way[depart][w].path.clear();
	}


	timer.Stop(); //��ʱֹͣ
	printf("\nElapsed time is: <%4.2lf> ms\n", timer.ElapsedTime());
	char c = getchar();
	return 0;
}

