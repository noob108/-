#-*- coding:utf-8 -*-
# @Author : Dummerfu
# @Time : 2020/4/26 18:17
import requests
import json
import time
import os
from pyecharts.charts import Bar,Timeline
from pyecharts import options as opts
from matplotlib import pyplot as plt
import pandas as pd
from 疫情动态柱状图.nameMap import city_name_map

plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
class Province(object):
    def __init__(self):
        self.num=''
        self.name=''
        self.confirm=[]
        self.confirmadd=[]
        self.heal=[]
        self.dead=[]
        self.timedata=[]
    def get_data(self,num,name):
        self.num=num
        url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province=' + name
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
        res = requests.get(url, headers=header)
        res.encoding = 'utf-8'
        res = json.loads(res.text)
        for daydata in res['data']:
            self.confirmadd.append(daydata['confirm_add'])
            self.confirm.append(daydata['confirm'])
            self.heal.append(daydata['heal'])
            self.dead.append(daydata['dead'])
            self.timedata.append(daydata['date'])
def handle_confirm(data_frame,tot):
    i = tot-80
    while 1:
        try:
            data_frame.loc[:][i] = data_frame.loc[:][i] + data_frame.loc[:][i - 1]
            i += 1
        except:
            return data_frame
def find(a,b):
    for i,j  in enumerate(a):
        if i ==b:
            return j
def crop(data_frame,path,tot):
    data_frame.to_excel(path,encoding='utf-8',na_rep=0,header=None,index=None)
    data_frame = pd.read_excel(path,header=None)
    data_frame.drop(data_frame.columns[0:tot - 80], axis=1, inplace=True)
    data_frame=handle_confirm(data_frame,tot)
    return data_frame
def output_to_data_frame(all_province_name):
    '''
        因为pandas 按列操作比较容易所以列为省份名称，行为时间数据
    :return:
    '''
    confirm_alllist=[]
    heal_alllist=[]
    dead_alllist=[]
    timelist=[]
    for i,pr in enumerate(all_province_name):
        # 自动是key值
        time.sleep(0.01)
        province[i].get_data(i,pr)
        # 找共同的时间序列 所以不需要再转excel自动补全了 缺点就是数据量减少了
        if len(timelist)>len(province[i].timedata) or len(timelist)==0:
            timelist=province[i].timedata
    l=len(timelist)
    for i,pr in enumerate(all_province_name):
        confirm_alllist.append(province[i].confirm[-l:])

    #print(confirm_alllist)

    confirm_frame = pd.DataFrame(confirm_alllist)
    dead_frame = pd.DataFrame(dead_alllist)
    heal_frame = pd.DataFrame(heal_alllist)

    return confirm_frame,dead_frame,heal_frame,timelist
def get_province():
    '''
        得到每个省的名字
    :return:
    '''
    all_province=[]
    for i in city_name_map:
        all_province.append(i)
    return all_province
def get_Top10info():
    pass
def print_bar(confirm_frame,dead_frame,heal_frame,timelist):
    '''
        暂时只有confrimadd 数据
        横坐标就是时间，纵坐标是确诊人数，
    :return:
    '''
    #excel=pd.read_excel('dummer.xls')
    tl=Timeline(init_opts=opts.InitOpts(page_title='疫情可视化'))
    # 调节播放速率 ,是否自动播放，是否循环播放，是否显示时间轴
    tl.add_schema(play_interval=300,is_auto_play=True,is_loop_play=False,is_timeline_show=True)
    l=len(timelist)
    #print('len timelist:',l)

    for i in range(0,l):
        # 将每天的数据单独拿出来进行排序
        s = {'province': all_province_name, 'confirm': confirm_frame.loc[:][i]}
        s = pd.DataFrame(s)

        # 翻转是镜像翻转所以 这里要从大到小排序
        s = s.sort_values(by='confirm', ascending=1)
        province_name=s[-10:]['province']
        confirm=s[-10:]['confirm']
        heal_list=get_Top10info()
        bar = Bar()
        bar.add_xaxis(province_name .to_list())
        # 名字，数据，柱状图间距， label标签显示在右侧|这样翻转的时候就在右侧
        bar.add_yaxis('确诊人数',confirm.to_list(),category_gap=0.5,label_opts=opts.LabelOpts(position='right'))
        #bar.add_yaxis('',heal_list.to_list())
        # 设置全局变量：x轴标签倾斜度，html主标题
        bar.set_global_opts(xaxis_opts=opts.AxisOpts(name_rotate=-15),title_opts=opts.TitleOpts('当前日期：%s'%timelist[i],subtitle='数据来自inews'))
        bar.reversal_axis()
        tl.add(bar,timelist[i])
    tl.render('my1.html')
if __name__=='__main__':
    all_province_name=get_province()
    province=[Province() for i in range(100)]
    confirm_frame,dead_frame,heal_frame,timelist=output_to_data_frame(all_province_name)
    #data_frame = pd.read_excel('E:\py_exercise\疫情动态柱状图\dummer.xls')
    print_bar(confirm_frame,dead_frame,heal_frame,timelist)
