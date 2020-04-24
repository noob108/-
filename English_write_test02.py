import matplotlib as plt
import numpy as np
import write_file_pyscript
import 输入去空格
import os
import random
import re

# 只有听写功能 待升级版本 2020/2/21
# *为难度系数
# 1还需自己事先打入单词 *****
# 2无法得知单词出自（第几单元）** finished
# 3不能学习得知哪些单词错误频率高而更高的概率出现（目前只有错误率）******
# 4单词的错误次数还要在另一个文件中存取
# 5无法听写短语  finished
# 6无法显示多个中文意思 * finished
# 7无法选择单元报听写  finished
# 8不能随机英文中文 finished 没有必要
# 9可视化界面 ********
# 10输入的时候光标在最前端 解决了11其实这个似乎无所谓
# 11输入的单词不能自动去掉空格之类的 finished
#            a=a.strip() 可以出去输入的前后空格
# 12布局排版问题*****
# 13倒计时功能**
# 14如果中间有个单词打错只能从后往前删掉在打不能插入 finished 打包后似乎可以

class Vocabulary(object):
    def __init__(self):
        self.Chinese = ''
        self.English = ''
        self.id = ''
        self.belong = ''


def init_vocabulary(vocabulary,sum_of_vocabulary,text,Unit_number):
    reg1 = r'[^\u4e00-\u9fa5()（），.*]+'
    reg2 = r'[\u4e00-\u9fa5()（），.*]+'
    for i in text:
        sum_of_vocabulary+=1
        English_list=re.findall(reg1,i)
        vocabulary[sum_of_vocabulary].Chinese=re.findall(reg2,i)[0]
        vocabulary[sum_of_vocabulary].id=sum_of_vocabulary
        vocabulary[sum_of_vocabulary].belong=Unit_number
        for every_Englishvocabulary in English_list:
            vocabulary[sum_of_vocabulary].English+=every_Englishvocabulary
        vocabulary[sum_of_vocabulary].English=vocabulary[sum_of_vocabulary].English.strip()

        #print(sum_of_vocabulary,vocabulary[sum_of_vocabulary].English,vocabulary[sum_of_vocabulary].Chinese)

    return sum_of_vocabulary

def find():
    if the_number in range(1, sum_of_vocabulary+1):
        print('是该单元第%d个的单词' % (the_number))


def pri():
    with open(os_path + '\\' + 'wrong_data'+Unit_number+'.txt', 'at', encoding='utf8') as f:
        num = -1
        for vo in wrong_tot:
            num += 1
            if vo >0:
                print(vocabulary[num].English)
                f.writelines(vocabulary[num].English +'-----'+vocabulary[num].Chinese+ '\n')
    print('错误词汇详见wrong_data'+Unit_number+'.txt')
    return


def opt():
    global shuru
    shuru =input('请输入：').strip()
    if shuru == 'find':  # 寻找单词的出自
        find()
        shuru = input().strip()
    if shuru == 'exit':  # 退出程序
        np.savetxt(os_path + '\\' + 'wrong_cs'+Unit_number+'.txt', wrong_tot)
        print('是否要将多频错误词汇打印(Y|N 默认N)')
        if input() == 'Y':
            pri()
        print('*********感谢你的使用**********')
        exit()
    if shuru == 'next':  # 目前作用仅仅是跳过单词（没有惩罚）
        return 1
    return 0


if __name__ == '__main__':
    print('输入要报单词的单元')
    Unit_number = input()
    txt_name = '第' + Unit_number + '单元词汇'
    os_path = os.getcwd()
    path=str(os_path) + '\\' + txt_name + '.txt'
    with open(path,'r') as f:
        text=f.readlines()
    alreadywrite_tot = 0  # 已经听写的个数
    writeright_tot = 0  # 听写正确的个数

    # 单词的总数
    sum_of_vocabulary=0
    vocabulary = [Vocabulary() for i in range(10000)]

    sum_of_vocabulary=init_vocabulary(vocabulary,sum_of_vocabulary,text,Unit_number)
    try:
        wrong_tot = np.loadtxt('wrong_cs'+Unit_number+'.txt')  # 读入是数组
    except:
        wrong_tot = np.zeros((sum_of_vocabulary+2, 1))

    print('********英语测试正式开始*********')
    print('********一共有%d个单词***********' % (sum_of_vocabulary))
    print('操作注解:')
    print('exit:退出')
    print('find:寻找当前单词的出自')
    print('*********************************')

    ra_list = random.sample(range(1, sum_of_vocabulary+1),sum_of_vocabulary)

    for the_number in ra_list:
        alreadywrite_tot+= 1
        print('中文', end='')
        print(' ' * 10, end='')
        print(vocabulary[the_number].Chinese)
        if opt():
            continue
        if shuru == vocabulary[the_number].English:  # 拼写正确
            writeright_tot += 1
            print(' ' * 10, end='')
            print('you are right 还有%d个单词' % (sum_of_vocabulary - alreadywrite_tot))
        else:  # 拼写错误
            print(' ' * 10, end='')
            print('you are wrong 还有%d个单词' % (sum_of_vocabulary - alreadywrite_tot))
            print('你的正确率是%.2lf%%' % (writeright_tot *100/alreadywrite_tot ))
            print('正确拼写是', end='')
            print(vocabulary[the_number].English)
            wrong_tot[the_number] += 1
            print('    这个单词你已经错了%d次' % (wrong_tot[the_number]))
    np.savetxt('wrong_cs'+Unit_number+'.txt', wrong_tot)