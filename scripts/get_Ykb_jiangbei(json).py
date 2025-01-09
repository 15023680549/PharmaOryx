#-*- coding : utf-8-*-
# coding:utf-8
import os
import sys
sys.path.append(os.getcwd())
from csv import reader
from multiprocessing import Pool, Manager
from selenium import webdriver
import scripts.utilParseHtml as utilParseHtml
import requests
import csv
import json
import time

import aiohttp
import asyncio

urls=[]
htmls=[]

#是否在线办理 isOnline   0否 1是
#在线办理地址 https://zwfw.cq.gov.cn/psx/icity/submitsp/baseinfo?itemCode=implementCode
#是否收费
sfdict = {
    '0':'否',
    '1':'是'
}

#办理形式
blxsdict = {
    '1':'窗口办理',
    '2':'网上办理',
    '3':'快递申请'
}


serviceOpbjectName = {
    '1':'自然人',
    '2':'企业法人',
    '3':'事业法人',
    '4':'社会组织法人',
    '5':'非法人企业',
    '6':'行政机关',
    '7':'7',
    '8':'8',
    '9':'其他组织'
}

#层级
cjdictName = {
    '4':'县级'
}
#事项类型字典
sxdictName = {
'20':'公共服务',
'10':'其他行政权力',
'09':'行政裁决',
'08':'行政奖励',
'07':'行政确认',
'06':'行政检查',
'05':'行政给付',
'04':'行政征收',
'03':'行政强制',
'02':'行政处罚',
'01':'行政许可'
}

sem=asyncio.Semaphore(10) #信号量，控制协程数量，防止爬的过快

#
dir=os.getcwd()


#存储数据之csv
def tocsv(fileNmae,rows):
    with open(dir+'\\'+fileNmae,'a+', newline='',encoding="utf-8-sig") as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)

def readurl(fileNmae):
    with open(dir+'\\'+fileNmae,'r',encoding='utf-8-sig') as f:
        csv_reader=reader(f)
        list_of_rows=list(csv_reader)
        for i in range(0,len(list_of_rows)):
            urls.append(list_of_rows[i])

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
#获取返回json list
async def get_html(url):
    async with sem: #
        async with aiohttp.ClientSession(headers=headers) as session:  #获取session
            data = {"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101"},"txnBodyCom":{"id":url[1],"basicCode":"","orgCode":"","isQueryCons":1,"matterId":""}}
            data = json.dumps(data)
            async with session.post('https://ykbapp.cq.gov.cn:8082/gml/web10002',data=data) as resp:  # 提出请求
                html=await resp.json() #直接获取到bytes
                htmls.append([html['C-Response-Body'],url[2]])
                name=json.loads(html['C-Response-Body'])
                print('异步获取%s.'% name['name'],url[2])

#协程调用，请求网页
def main_get_html():
    loop=asyncio.get_event_loop()   #获取事件循环
    tasks=[get_html(url) for url in urls]   #把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))    #激活协程

#使用多进程解析html
def multi_parse_html(html,cnt,rows):
    try:
        list = utilParseHtml.parse(html)
    except Exception as ex:
        print(ex,html[0])
    rows.append(list)
    print('第%d个html-----------date:%s'% (cnt,time.time()))

#多进程调用总函数，解析html
def main_parse_html(rows):
    p=Pool(2)
    i=0
    for html in htmls:
        i+=1
        p.apply_async(multi_parse_html,args=(html,i,rows))
    p.close()
    p.join()

def getXzqlqdUrl(filename,pageNo):
    print('第' + str(pageNo) + '页')
    # 获取市级行政权力清单
    data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101","tRecInPage":10,"tPageJump":'+str(pageNo)+'},"txnBodyCom":{"name":"","strLevel":1,"minnum":"","regnCode":"500105","addrLvlCd":"3","type":"XZSP","fwlb":""}}'
    #测试南川公安局行政确认
    # data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101","tRecInPage":10,"tPageJump":2},"txnBodyCom":{"name":"","strLevel":1,"minnum":"","orgCode":"500119208","regnCode":"500119","addrLvlCd":"3","type":"07","fwlb":""}}'
    res = requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10017', headers=headers, data=data).json()
    list2 = json.loads(res['C-Response-Body'])['lIST2']
    for list in list2:
        groupId = list['groupId']
        #查看是否有下级目录
        data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101","tRecInPage":100,"tPageJump":1},"txnBodyCom":{"matterId":"'+groupId+'","strLevel":2,"regnCode":"500105","addrLvlCd":"3","exeLevel":"4"}}'
        res2= requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10017', headers=headers, data=data).json()['C-Response-Body']
        listz=json.loads(res2)['lIST2']
        if len(listz)>=1:
            for l2 in listz:
                rows = []
                title = l2['name']
                id = l2['id']
                href = 'https://zwykb.cq.gov.cn/qxzz/jbq/bszn/?id=' + id + '&parentPage=7'
                row2 = [title, id, href]
                rows.append(row2)
                sonList = l2['sonList']
                for son in sonList:
                    title3=son['name']
                    id3=son['id']
                    href3='https://zwykb.cq.gov.cn/qxzz/jbq/bszn/?id='+id3+'&parentPage=7'
                    if title==title3:
                        rows.remove(row2)
                    rows.append([title3,id3,href3])
                print(rows)
                tocsv(filename, rows)



def getGgfwUrl(filename,pageNo):
    print('第' + str(pageNo) + '页')
    # 获取公共服务清单
    data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101","tRecInPage":10,"tPageJump":'+str(pageNo)+'},"txnBodyCom":{"name":"","strLevel":1,"minnum":"","regnCode":"500105","addrLvlCd":"3","type":"20","fwlb":""}}'
    res = requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10022', headers=headers, data=data).json()
    list2 = json.loads(res['C-Response-Body'])['lIST2']
    for list in list2:
        matterId = list['matterId']
        #查看是否有下级目录
        data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101","tRecInPage":100,"tPageJump":1},"txnBodyCom":{"matterId":"'+matterId+'","strLevel":2,"regnCode":"500105","addrLvlCd":"3"}}'
        res2= requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10022', headers=headers, data=data).json()['C-Response-Body']
        listz=json.loads(res2)['lIST2']
        if len(listz)>=1:
            for l2 in listz:
                rows=[]
                title = l2['name']
                id = l2['id']
                href = 'https://zwykb.cq.gov.cn/qxzz/jbq/bszn/?id=' + id + '&parentPage=7'
                row2 = [title, id, href]
                rows.append(row2)
                sonList = l2['sonList']
                for son in sonList:
                    title3 = son['name']
                    id3 = son['id']
                    href3 = 'https://zwykb.cq.gov.cn/qxzz/jbq/bszn/?id=' + id3 + '&parentPage=7'
                    if title == title3:
                        rows.remove(row2)
                    rows.append([title3, id3, href3])
                print(rows)
                tocsv(filename, rows)


#获取url
def geturl(filename):
    #市级行政权力清单，市级公共服务清单
    bszn=['https://zwykb.cq.gov.cn/qxzz/jbq/fwqd/xzqlqd/','https://zwykb.cq.gov.cn/qxzz/jbq/fwqd/ggfwqd/']
    for url in bszn:
        driver.get(url);
        time.sleep(1)
        # 获取总页面
        print(url)
        total = int(driver.find_element_by_xpath('/html/body/div[4]/div[5]/div[6]/a[6]').text)
        #退出并关闭浏览器
        j = 0
        while (True):
            j += 1
            # 获取页面title,url及id
            getXzqlqdUrl(filename,j)
            if (j == 1):
                break
    driver.quit();

if __name__ == '__main__':
    # driver = webdriver.Chrome()
    #获取页面总页数再爬取链接
    # geturl('渝快办酉阳url.csv')
    #直接爬取链接
    for i in range(1,415+1):#435页
        getXzqlqdUrl('渝快办江北url.csv', i)
    for i in range(1, 28 + 1):#32页
        getGgfwUrl('渝快办江北url.csv', i)

    # 读取存储url csv到数组中
    readurl('渝快办江北url.csv')
    # 定义多进程共享变量
    manager = Manager()
    rows = manager.list()
    main_get_html()
    main_parse_html(rows)
    tocsv('渝快办江北body.csv', rows)
