#-*- coding:utf-8 -*-
# @Author : Dummerfu
# @Time : 2020/4/26 18:17
import requests
import json
import time
from pyecharts.charts import Bar,Timeline
from matplotlib import pyplot as plt
import pandas
from matplotlib.animation import FuncAnimation
plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
class Timeinfo(object):
    def __init__(self):
        self.name = []  # 所有省份名称
        # 与省份一一对应
        self.confirm = []  # 所有省份确诊人数
        self.heal = []  # 所有省份治愈人数
        self.dead = []  # 所有省份死亡人数
class Province(object):
    def __init__(self):
        self.name=''
        self.confirm=[]
        self.heal=[]
        self.dead=[]
        self.confirmadd=[]
def output_to_excel(all_province_name):
    '''
        因为pandas 按列操作比较容易所以列为省份名称，行为时间数据
    :return:
    '''
    alllist=[]
    timelist=[]
    flag=0
    for pr in all_province_name:
        # 自动是key值
        url='https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province='+str(pr)
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
        res = requests.get(url,headers = header)
        res.encoding = 'utf-8'
        res = json.loads(res.text)
        confirm=[]
        for j,daydata in enumerate(res['data']):
            confirm.append(daydata['confirm'])
            if flag == 0:
                timelist.append(daydata['date'])
        flag=1
        alllist.append(confirm)
    print(alllist)
    dataframe=pandas.DataFrame(alllist,index=all_province_name)
    # 加下面这一句会输出一个excel文件
    # 文件名 dummer.xls 编码形式 utf-8 缺失值补为 0
    dataframe.to_excel('dummer.xls',encoding='utf-8',na_rep=0)
if __name__=='__main__':
    all_province_name=['湖北','安徽']
    province=[Province() for i in range(len(all_province_name))]
    output_to_excel(all_province_name)