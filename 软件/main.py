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
timelist=[]
def output_to_data_frame(all_province_name):
    '''

        因为pandas 按列操作比较容易所以列为省份名称，行为时间数据
    :return:
    '''
    confirmadd_alllist=[]
    heal_alllist=[]
    dead_alllist=[]
    # emmm 这个flag 防止timelist多次更新 可以不要
    flag=0
    for pr in all_province_name:
        # 自动是key值
        time.sleep(0.01)
        url='https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province='+str(pr)
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
        res = requests.get(url,headers = header)
        res.encoding = 'utf-8'
        res = json.loads(res.text)
        confirmadd=[]
        heal=[]
        dead=[]
        for j,daydata in enumerate(res['data']):
            confirmadd.append(daydata['confirm_add'])
            heal.append(daydata['heal'])
            dead.append(daydata['dead'])
            if flag == 0:
                timelist.append(daydata['date'])
        flag=1
        confirmadd_alllist.append(confirmadd)
        heal_alllist.append(heal)
        dead_alllist.append(dead)


    confirmadd_frame = pd.DataFrame(confirmadd_alllist)
    dead_frame = pd.DataFrame(dead_alllist)
    heal_frame = pd.DataFrame(heal_alllist)
    # 下面这一句会输出一个excel文件
    # 文件名 dummer.xls 编码形式 utf-8 缺失值补为 0
    path=os.getcwd()
    path1=path+'\confirmadd.xls'
    path2=path+'\dead.xls'
    path3=path+'\heal.xls'
    try:
        os.remove(path)
    except:
        pass
    # 将confirmadd，heal，dead 三个数据分别保存到三个excel文件里
    # 因为excel可以自动补缺失值 以后再想想怎么样优化这一步
    confirmadd_frame.to_excel(path1,encoding='utf-8',na_rep=0)
    dead_frame.to_excel(path2, encoding='utf-8', na_rep=0)
    heal_frame.to_excel(path3, encoding='utf-8', na_rep=0)
    confirmadd_frame=pd.read_excel(path1)
    dead_frame=pd.read_excel(path2)
    heal_frame=pd.read_excel(path3)
    return confirmadd_frame,dead_frame,heal_frame
def get_province():
    '''
        得到每个省的名字
    :return:
    '''
    all_province=[]
    for i in city_name_map:
        all_province.append(i)
    return all_province
def print_bar(confirmadd_frame,dead_frame,heal_frame):
    '''
        暂时只有confrimadd 数据
        横坐标就是时间，纵坐标是确诊人数，
    :return:
    '''
    #excel=pd.read_excel('dummer.xls')
    tl=Timeline()
    # 调节播放速率 ,是否自动播放，是否循环播放，是否显示时间轴
    tl.add_schema(play_interval=300,is_auto_play=True,is_loop_play=False,is_timeline_show=True)

    for i,time in enumerate(timelist):

        # 将每天的数据单独拿出来进行排序
        s = {'province': all_province_name, 'confirmadd': confirmadd_frame.loc[:][i]}
        s = pd.DataFrame(s)

        # 翻转是镜像翻转所以 这里要从大到小排序
        s = s.sort_values(by='confirmadd', ascending=1)
        province=s[-10:]['province']
        confirmadd=s[-10:]['confirmadd']

        bar=Bar()
        bar.add_xaxis(province.to_list())
        # 名字，数据，柱状图间距， label标签显示在右侧|这样翻转的时候就在右侧
        bar.add_yaxis('',confirmadd.to_list(),category_gap=0.5,label_opts=opts.LabelOpts(position='right'))

        # 设置全局变量：x轴标签倾斜度，html主标题
        bar.set_global_opts(xaxis_opts=opts.AxisOpts(name_rotate=-15),title_opts=opts.TitleOpts('当前日期：%s'%time))
        bar.reversal_axis()
        if i%3==0:
            tl.add(bar,time)
    tl.render('my1.html')
def remove_file():
    '''
        移除产生的excel 文件
    :return:
    '''
    pass
if __name__=='__main__':
    all_province_name=get_province()
    confirmadd_frame,dead_frame,heal_frame=output_to_data_frame(all_province_name)
    #data_frame = pd.read_excel('E:\py_exercise\疫情动态柱状图\dummer.xls')
    print_bar(confirmadd_frame,dead_frame,heal_frame)
    remove_file()
