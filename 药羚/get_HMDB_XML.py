#-*- coding : utf-8-*-
# coding:utf-8

import time
from lxml import etree
from multiprocessing import Pool
import requests
import aiohttp
import asyncio
import re
import os
try:
    import xml.etree.CElementTree as ET
except:
    import xml.etree.ElementTree as ET


urls=['https://hmdb.ca/metabolites/HMDB0000031.xml']
htmls=[]
sem=asyncio.Semaphore(10) #信号量，控制协程数量，防止爬的过快

dir=os.getcwd()
#获取url中CID
def getFileName(url):
    return url.split('/')[-1]

#保存html内容到文件
def save_xml(html,name):
    # 保存json文件
    with open(dir + "\\HMDB\\" +name, 'w', encoding='utf-8_sig') as f:
        f.write(html)

async def get_html(url):
    #with(await sem):
    async with sem: #
        #async with是异步上下文管理器
        async with aiohttp.ClientSession(trust_env = True) as session:  #获取session
            #async with session.request('GET',url.format(10)) as resp:  #提出请求
            async with session.request('GET', url) as resp:  # 提出请求
                html=await resp.text() #直接获取到bytes
                #htmls.append(html)
                save_xml(html,getFileName(url)) #保存xml
                print('异步获取%s下的html.'% url)
    #await asyncio.sleep(1)

#协程调用，请求网页
def main_get_html():
    loop=asyncio.get_event_loop()   #获取事件循环
    tasks=[get_html(url) for url in urls]   #把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))    #激活协程

#使用多进程解析html
def multi_parse_html(html,cnt):
    print('第%d个html-----------date:%s'% (cnt,time.time()))
    #print(html)

#多进程调用总函数，解析html
def main_parse_html():
    p=Pool(2)
    i=0
    for html in htmls:
        i+=1
        p.apply_async(multi_parse_html,args=(html,i))
    p.close()
    p.join()

if __name__ == '__main__':
    i=340000
    for f in range(1,2):
        urls=[]
        for i in range(340000,340290):
            filename='HMDB'+str(i).zfill(7)+".xml"
            if not os.path.exists(dir+'\HMDB\HMDB'+str(i).zfill(7)+".xml"):
                url = "https://hmdb.ca/metabolites/"+filename
                urls.append(url)
            start=time.time()
        if len(urls)!=0:
            main_get_html()
        #main_parse_html()
        print('总耗时:%0.5f秒'% float(time.time()-start))
        #https://hmdb.ca/metabolites/HMDB0340289xml
