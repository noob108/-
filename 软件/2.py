#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import json
import time
from pyecharts.charts.basic_charts import bar
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
def func(frame):
    ax.cla()
    print(frame,':')
    for pr in all_prov:
        num=all_prov[pr]
        print(num)
        ax.barh(pr,province[num].confirm[frame],label='date:%s'%date[frame],height=0.5)
        ax.legend()
    return ax,
def init():
    ax.set_xlim(0,100000)
    return ax,
class Province(object):
    def __init__(self):
        self.name=''
        self.confirm=[]
        self.heal=[]
        self.dead=[]
if __name__=='__main__':
    all_prov={'湖北': 0,'安徽': 1 }
    province=[Province() for i in range(len(all_prov))]
    date=[]
    flag=0
    print(len(province))
    for pr in all_prov:
        # 自动是key值
        url='https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province='+pr
        print(url)
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
        res = requests.get(url,headers = header)
        res.encoding = 'utf-8'
        res = json.loads(res.text)
        num=all_prov[pr]
        province[num].name=pr
        for daydata in res['data']:
            size=len(province[num].confirm)
            if not daydata['confirm']:
                daydata['confrim']=province[num].confirm[size-1]
            province[num].confirm.append(daydata['confirm'])
            if daydata['heal']:
                daydata['heal'] = province[num].confirm[size - 1]
            province[num].heal.append(daydata['heal'])
            if daydata['dead']:
                daydata['dead'] = province[num].confirm[size - 1]
            province[num].dead.append(daydata['dead'])
            if flag == 0:
                date.append(daydata['date'])
        flag=1
    print(province[1].confirm)
    fig,ax=plt.subplots()
    ani=FuncAnimation(fig=fig,func=func,init_func=init,frames=len(date)-1,interval=100,blit=False)
    plt.show()