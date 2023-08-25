import aiohttp
import asyncio
import urllib.request
from multiprocessing import Pool
from bs4 import BeautifulSoup
import time
import re
import os
import xlsxwriter as xw
import csv

htmls=[]
urls=[
    'https://www.drugfuture.com/synth/syndata.aspx?ID=90443',
    'https://www.drugfuture.com/synth/syndata.aspx?ID=90444'
]
rows=[]

sem=asyncio.Semaphore(10)
headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/102.0.5005.63 Safari/537.36'
}

dir=os.getcwd()

#存储数据之csv
def tocsv(rows):
    with open(dir+'\\fda_ndc\\fdandc.csv','a+', newline='',encoding="utf-8") as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)

def dataToExcel(data,sheetName):
    workbook=xw.Workbook('aa')
    worksheet1=workbook.add_worksheet(sheetName)
    worksheet1.activate()
    title=['ID','说明','内容']
    worksheet1.write_row('A1',title)
    i=2
    for j in range(len(data)):
        row='A'+1
        worksheet1.write_row(row,data)

async def get_html(url):
    async with sem:
        async with aiohttp.ClientSession(trust_env = True,headers=headers) as session:  #获取session
            async with session.request('GET', url,) as resp:  # 提出请求
                if resp.status==200:
                    print(url+'访问成功')
                    htmls.append(await resp.text())


def main_get_htm():
    loop = asyncio.get_event_loop()  # 获取事件循环
    tasks = [get_html(url) for url in urls]  # 把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))  # 激活协程

def multi_parse_html(html,cnt):
    rows=[]
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('tbody')
    print(table)
    for tr in table.findAll('tr'):
        tds = tr.findAll('td')
        if len(tds) == 0:
            continue
        cpndc = tds[0].getText()
        cplx = tds[1].getText()
        spm = tds[2].getText()
        tym = tds[3].getText()
        jx = tds[4].getText()
        gytj = tds[5].getText()
        ssrq = tds[6].getText()
        jsrq = tds[7].getText()
        scfl = tds[8].getText()
        sqh = tds[9].getText()
        bqcyz = tds[10].getText()
        hxcf = tds[11].getText()
        gg = tds[12].getText()
        rows.append([cpndc, cplx, spm, tym, jx, gytj, ssrq, jsrq, scfl, sqh, bqcyz, hxcf, gg])
    tocsv(rows)
    print('第%d个html-----------date:%s'% (cnt,time.time()))


#多进程调用总函数，解析html
def main_parse_html():
    p=Pool(8)
    i=0
    for html in htmls:
        i+=1
        p.apply_async(multi_parse_html,args=(html,i))
    p.close()
    p.join()

if __name__ == '__main__':
    i=1
    for j in range(58):
        urls=[]
        htmls=[]
        for i in range(i,i+101):
            urls.append('https://www.drugfuture.com/fda-ndc/search.aspx?SearchTerm=%%%&SearchType=BasicSearch&order=0&page='+str(i))
        main_get_htm()
        main_parse_html()
        print(i)
