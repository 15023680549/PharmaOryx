#-*- coding : utf-8-*-
# coding:utf-8
import os
from csv import reader
from multiprocessing import Pool, Manager
from selenium import webdriver
import requests
import csv
import json
import time

import scripts.utilMysql as MysqlTool
import aiohttp
import asyncio

urls=[]
htmls=[]


sem=asyncio.Semaphore(0) #信号量，控制协程数量，防止爬的过快

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

#获取返回json list
async def get_html(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    async with sem: #
        async with aiohttp.ClientSession(headers=headers) as session:  #获取session
            async with session.get(url[2]) as resp:  # 提出请求
                # html = await resp.text()  # 直接获取到bytes
                if(resp.status!=200):
                    htmls.append(url)
                    print('异步获取%s.'% url[2])

#协程调用，请求网页
def main_get_html():
    loop=asyncio.get_event_loop()   #获取事件循环
    tasks=[get_html(url) for url in urls]   #把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))    #激活协程

def parse(html):
    url = html[1]
    html = json.loads(html[0])
    return

#使用多进程解析html
def multi_parse_html(html,cnt,rows):
    try:
        list = parse(html)
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

#list存入csv文件
def detilList(filename,list):
    title = list['name']
    id = list['id']
    implementCode = list['implementCode']
    href = 'https://zwykb.cq.gov.cn/qxzz/psx/bszn/?id=' + id + '&parentPage=7'
    zxbl = 'https://zwfw.cq.gov.cn/psx/icity/submitsp/baseinfo?itemCode='+implementCode
    row = [title, id, href,zxbl]
    tocsv(filename, [row])


if __name__ == '__main__':
    #1、获取mysql数据库数据
    with MysqlTool.MysqlTool() as db:
        #2、把所有数据zt字段改为5
        sql ="UPDATE r_know_library set zt=5"
        # db.execute(sql,None,commit=True)
        while(True):
            sql = "SELECT id,title,url FROM r_know_library WHERE zt = %s LIMIT 100"
            args = (5,)
            urls = db.execute(sql, args)
            corre_urls=[]
            if(len(urls) > 0):
                for url in urls:
                    res = requests.get(url[2])
                    if(res.status_code==404):
                        htmls.append([url[0],url[1],url[2],res.status_code])
                        sql = "UPDATE r_know_library SET zt=3 WHERE id=%s"
                        args = (url[0],)
                        db.execute(sql, args, commit=True)
                    #
                    else:
                        corre_urls.append(url[0])
                sql = "UPDATE r_know_library SET zt=%s WHERE id in %s"
                args = (2, corre_urls)
                db.execute(sql, args, commit=True)
            else:
                break
    # 定义多进程共享变量
    # manager = Manager()
    # rows = manager.list()
    # main_get_html()
    # for html in htmls:
    #     print(html)
    # main_parse_html(rows)
    # tocsv('渝快办彭水body.csv', rows)
