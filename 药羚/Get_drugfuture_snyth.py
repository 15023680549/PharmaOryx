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

sem=asyncio.Semaphore(10)
headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/102.0.5005.63 Safari/537.36'
}

dir=os.getcwd()

#存储数据之csv
def tocsv(rows):
    with open('snyth.csv','a+', newline='',encoding="utf-8") as f_output:
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
                if resp.status==200 and resp.content_length>161:
                    print(url+'访问成功')
                    htmls.append([await resp.text(),url.split('=')[-1]])
                elif resp.status==200 and resp.content_length==161:
                    # print(url+'无此ID')
                    pass
                else:
                    print('访问失败+'+resp.status)

def main_get_htm():
    loop = asyncio.get_event_loop()  # 获取事件循环
    tasks = [get_html(url) for url in urls]  # 把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))  # 激活协程

def multi_parse_html(html,ID,cnt):
    soup = BeautifulSoup(html, 'lxml')
    #print(soup.prettify())  #格式化输出
    #tables = soup.findAll('table')
    tables=soup.form.findAll('table')
    rows=[]
    for i in range(len(tables)):
        tab = tables[i]
        if i==0:
            k=1
            for tr in tab.findAll('tr'):#取第一个表格数据
                if k == 1:
                    mc=tr.getText().split('【药物名称】')[-1]
                elif k==3:
                    img_src = "https://www.drugfuture.com/synth/" + tr.img.attrs['src'].replace('.\\', '/').replace(
                        '\\', '/')
                    filename=re.findall("\d+\.?.*", img_src)[0].replace('/','_')
                    urllib.request.urlretrieve(img_src,dir+'\\snyth\\'+filename) #复制内容到本地
                    # print('化学结构式(Chemical Structure):'+filename)
                k+=1
            rows.append([ID, i, mc, filename])
        else:
            j=1
            for td in tab.findAll('td'):  # 取第一个表格数据
                if j==2:
                    ckwx=td.getText()
                elif j==4:
                    bt = td.getText()
                elif j==6:
                    zz=td.getText()
                elif j==8:
                    ly=td.getText()
                elif j==9:
                    # print('合成过程:')
                    img_src = "https://www.drugfuture.com/synth/" + td.img.attrs['src'].replace('.\\', '/').replace(
                        '\\', '/')
                    filename = re.findall("\d+\.?.*", img_src)[0].replace('/', '_')
                    urllib.request.urlretrieve(img_src, dir + '\\snyth\\' + filename)  # 复制内容到本地
                    # print(filename)
                elif j==10:
                    hclx=td.getText().split('合成路线图解说明:')[-1]
                j+=1
            rows.append([ID, i, ckwx, bt, zz, ly, filename,hclx])
    tocsv(rows)
    print('第%d个html-----------date:%s'% (cnt,time.time()))

#多进程调用总函数，解析html
def main_parse_html():
    p=Pool(8)
    i=0
    for html,ID in htmls:
        i+=1
        p.apply_async(multi_parse_html,args=(html,ID,i))
    p.close()
    p.join()

if __name__ == '__main__':
    i=356000
    for j in range(100000):
        urls=[]
        htmls=[]
        for i in range(i,i+1001):
            urls.append('https://www.drugfuture.com/synth/syndata.aspx?ID='+str(i))
        main_get_htm()
        main_parse_html()
        print(i)
