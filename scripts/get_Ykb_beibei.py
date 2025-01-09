#-*- coding : utf-8-*-
# coding:utf-8
import os
from csv import reader
from selenium import webdriver
from multiprocessing import Pool, Manager
import scripts.utilParseHtml as utilParseHtml
import requests
import csv
import json
import time

import aiohttp
import asyncio

#重庆市 500000
#南川 500119
#江北 500105
#江津 500116
#酉阳 500242
#北碚 500109
#区县编码
orgcode='500109'
urls=[]
htmls=[]

sem=asyncio.Semaphore(10) #信号量，控制协程数量，防止爬的过快
#
dir=os.getcwd()

prefixUrl=''
if orgcode=='500105':
    prefixUrl='https://zwykb.cq.gov.cn/qxzz/jbq/bszn/?id='
elif orgcode=='500116':
    prefixUrl='https://zwykb.cq.gov.cn/qxzz/ncq/bszn/?id='
elif orgcode=='500242':
    prefixUrl='https://zwykb.cq.gov.cn/qxzz/yyxxx/bszn/?id='
elif orgcode=='500109':
    prefixUrl='https://zwykb.cq.gov.cn/qxzz/bbq/bszn/?id='
elif orgcode == '500000':
    prefixUrl = 'https://zwykb.cq.gov.cn/sxqd/bsznq/?id='

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

def getXzqlqdUrl(filename,pageNo):
    print('第' + str(pageNo) + '页')
    # 获取市级行政权力清单
    data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101","tRecInPage":10,"tPageJump":' + str(
        pageNo) + '},"txnBodyCom":{"name":"","strLevel":1,"minnum":"","regnCode":"'+orgcode+'","addrLvlCd":"3","type":"XZSP","fwlb":""}}'
    res = requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10017', headers=headers, data=data).json()
    list2 = json.loads(res['C-Response-Body'])['lIST2']
    for list in list2:
        groupId = list['groupId']
        # 查看是否有下级目录
        data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101","tRecInPage":100,"tPageJump":1},"txnBodyCom":{"matterId":"' + groupId + '","strLevel":2,"regnCode":"'+orgcode+'","addrLvlCd":"3","exeLevel":"4"}}'
        res2 = requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10017', headers=headers, data=data).json()[
            'C-Response-Body']
        listz = json.loads(res2)['lIST2']
        if len(listz) >= 1:
            for l2 in listz:
                rows = []
                title = l2['name']
                id = l2['id']
                href = prefixUrl + id + '&parentPage=7'
                row2 = [title, id, href]
                rows.append(row2)
                sonList = l2['sonList']
                for son in sonList:
                    title3 = son['name']
                    id3 = son['id']
                    href3 = prefixUrl + id3 + '&parentPage=7'
                    if title == title3:
                        rows.remove(row2)
                    rows.append([title3, id3, href3])
                print(rows)
                tocsv(filename, rows)

def getGgfwUrl(filename,pageNo):
    # 获取公共服务清单
    print('第' + str(pageNo) + '页')
    data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101","tRecInPage":10,"tPageJump":' + str(pageNo) + '},"txnBodyCom":{"name":"","strLevel":1,"minnum":"","regnCode":"'+orgcode+'","addrLvlCd":"3","type":"20","fwlb":""}}'
    res = requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10022', headers=headers, data=data).json()
    list2 = json.loads(res['C-Response-Body'])['lIST2']
    for list in list2:
        matterId = list['matterId']
        # 查看是否有下级目录
        data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101","tRecInPage":100,"tPageJump":1},"txnBodyCom":{"matterId":"' + matterId + '","strLevel":2,"regnCode":"'+orgcode+'","addrLvlCd":"3"}}'
        res2 = requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10022', headers=headers, data=data).json()[
            'C-Response-Body']
        listz = json.loads(res2)['lIST2']
        if len(listz) >= 1:
            for l2 in listz:
                rows = []
                title = l2['name']
                id = l2['id']
                href = prefixUrl + id + '&parentPage=7'
                row2 = [title, id, href]
                rows.append(row2)
                sonList = l2['sonList']
                for son in sonList:
                    title3 = son['name']
                    id3 = son['id']
                    href3 = prefixUrl + id3 + '&parentPage=7'
                    if title == title3:
                        rows.remove(row2)
                    rows.append([title3, id3, href3])
                print(rows)
                tocsv(filename, rows)

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

#多进程调用总函数，解析html
def main_parse_html(rows):
    p=Pool(2)
    i=0
    for html in htmls:
        i+=1
        p.apply_async(multi_parse_html,args=(html,i,rows))
    p.close()
    p.join()

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

if __name__ == '__main__':
    #直接爬取链接
    for i in range(1,419+1):#438
        getXzqlqdUrl(orgcode+'url.csv', i)
    for i in range(1, 28 + 1):#27
        getGgfwUrl(orgcode+'url.csv', i)
    # 读取存储url csv到数组中
    readurl(orgcode+'url.csv')
    # 定义多进程共享变量
    manager = Manager()
    rows = manager.list()
    main_get_html()
    main_parse_html(rows)
    tocsv('渝快办body20240701.csv', rows)
