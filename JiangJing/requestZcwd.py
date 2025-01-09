#-*- coding : utf-8-*-
# coding:utf-8
import requests




#检测江津政策问答所有栏目是否更新


if __name__ == '__main__':
    res = requests.get('http://www.jiangjin.gov.cn/zwgk_180/zfxxgkml/zcwd/')
    res.encoding = res.apparent_encoding   #解决中文乱码问题
    print(res.text)
    print('中文乱码')