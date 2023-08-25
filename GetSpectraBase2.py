import csv
from csv import reader
import json

#from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import lxml
import requests
import aiohttp
import asyncio
from multiprocessing import Pool
import re
import os
import time
import base64
import base64
import urllib.request
from urllib import parse

import requests

#1、判断目录是否存在
dir=os.getcwd()
if not os.path.exists(dir+"\\Spectra\\JSON"):
    os.mkdir(dir + "\\Spectra")
    os.mkdir(dir + "\\Spectra\\JSON")
    os.mkdir(dir+"\\Spectra\\txt")
    os.mkdir(dir + "\\Spectra\\spectrum")
    os.mkdir(dir + "\\Spectra\\destxt")
    os.mkdir(dir + "\\Spectra\\STRUCTURE")
    print("----------------目录已创建----------------")

cookies={
    'cookie':'osano_consentmanager_uuid=2c7ff550-84f1-44b0-8fd2-71c083df0b2d; osano_consentmanager=LACoDQXFiWJ5d88SbSJkt4S_KAdD_iNA-oKIjmaHPtxjcdjgmH-hsNmDBsr3GIJkk_Wm2ytpX9KBAmytZOl7HtjSaKk5jyZbNyBkyGOLMhkQGnz5BbZhNxvpPbtaZoGqBkYax19GKMiAV4dS9tb0LyBFv1L0dQ71B8XCHAWIWK4Jth8hrCTGJEyy84dJ2Om57cDUonThquvBi9yQ8AVuAlc-vGJSaihoN8LhrNg2td2QlyHR1nRPoB4_oHmY4GG0QR6mCu7YvW5KvgPqfj8RH2djGFelORmidKlHRA==; s_fid=058AAB48EA171EC1-3E2EC97AEED6650A; s_cc=true; _fbp=fb.1.1653383212785.1617112061; __gads=ID=51efcc02d38ba074:T=1653383206:S=ALNI_MaXwtiV-7K4pHn0b6q4cdHw6p7FXw; __gpi=UID=000005b267fa2c76:T=1653383206:RT=1653442009:S=ALNI_MaJjxQ_WM2m8X0jZOEMMPyABDcD5w; auth_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik4wRkdRemhHUkRoQk56TkROa0l3TmpjMVJUSTFOelpHTlRrNE1EZzBOMFZCUlRVME1USXdOQSJ9.eyJodHRwczovL3NwZWN0cmFiYXNlLmNvbS9uYW1lIjoiWW9uZyBKaWFuZyIsImdpdmVuX25hbWUiOiJZb25nIiwiZmFtaWx5X25hbWUiOiJKaWFuZyIsIm5pY2tuYW1lIjoiankxNTAyMzY4MDU0OSIsIm5hbWUiOiJZb25nIEppYW5nIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdqOE9BWVdPMVZTNjdDTk1FOTJOcnlpNzlwOVMtb2lvOVNPN0VtbD1zOTYtYyIsImxvY2FsZSI6InpoLUNOIiwidXBkYXRlZF9hdCI6IjIwMjItMDUtMjVUMDI6NDQ6NTUuNzAwWiIsImlzcyI6Imh0dHBzOi8vc3BlY3RyYWJhc2UuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE1MTM3MTUxMjU1NjIyNjM1MDk5IiwiYXVkIjoiZ25CZzU1MDNzbnlOZm9DbUx0aTZkdXM3WEhneWVubTAiLCJpYXQiOjE2NTM0NDY2OTYsImV4cCI6MTY1MzQ4MjY5NiwiYXRfaGFzaCI6IkVWY0N0bTdoYkFWVGpqMnljeUtDd2ciLCJub25jZSI6IlNqUG9MTlVvbFNSSC1kc2ljOVU1fnJMWEVKUzh6WVBsIn0.BGKFW122_-nmcP1xMC-tb4-kZX2hdReLQL8LFfGQJkUY5Souwp5zMxY2IMx1PacS5KPId9ZMuEtfwosJA6dZCyNCT9-lXweND1DjoZcGk_Buor4ZS8gp7VJddQzogzrEbuGchLni8URrhp843msVoj9Snax5o5EIEVbfHq8cAQDnvC0P4jIBd6WG2O0Uh_3L7PgZ0fP3I039Nq-8C3fur6HfK8tTz6tbAMMBYMhKAkHPa1EH6h33FAoFSIqWL6NThvJE2jQFXPZYKo6MLkgE1ZNNSYlba7SyAMvcwUE4ojZdAfyuvgqDFxvZBsSxoHTG0JG402cS7ShJELlJzkRwDQ; access_token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9zcGVjdHJhYmFzZS5hdXRoMC5jb20vIn0..IQsc8ZNHsiET29cV.cU1zkn3hUelR58up5mV5y_NYpzrho_Czs3C7isQ6MST9Q7oQ5cEm3cd8AEyov3EdRpJsjS0d4aqpqv4Jnnq3kkYZj08o_nGdGtCGnLN2y27mrp0fEVdSwyjHe0gf3v4dteMifNzkxnHzgoGSNDwblXlmOck_rUo0Bw1lz8Bxbn8KozQdQxEqwJ0kZrCDaGObxK6GEPChemgjJWKu4bdJ93a9f-qQPhjqSb9iaMgvubsTIBWgqjlC4m0CwiDoLG_rzGMRNq3tkcxdetpL9NdkOC7v3nHwpokq43wUerTvl6Ci-UTI-MGR048.ozjp1-H9wSLmKrhJhXeXgQ; s_sq=[[B]]',
}

headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/102.0.5005.63 Safari/537.36'
}
url_home='https://spectrabase.com'
urls2=['https://spectrabase.com/api/spectrum/VEyU80HVqz',
'https://spectrabase.com/api/spectrum/2kIORiNyKde.png?h=516.9375&ph=true&w=919',
'https://spectrabase.com/api/spectrum/9mGilsloX8e.png?h=516.9375&ph=true&w=919',
'https://spectrabase.com/api/spectrum/7ZdLb5TGbEA.png?h=516.9375&ph=true&w=919',
'https://spectrabase.com/api/spectrum/ArwxdIQlxna.png?h=516.9375&ph=true&w=919',
'https://spectrabase.com/api/spectrum/3NSEwPcJJKK.png?h=516.9375&w=919']

htmls=[]
sem=asyncio.Semaphore(10) #信号量，控制协程数量，防止爬的过快

def base64toimg(str):
    str = 'iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAIAAAB7QOjdAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAOSURBVBhXY/gPBP//AwAU8gX7YtukPQAAAABJRU5ErkJggg=='
    imgdata = base64.b64decode(str)
    file = open('1.png', 'wb')
    file.write(imgdata)
    file.close()

#取物质主页json数据
def get_json(soup):
    # 1、取物质主页中json数据
    scripts = soup.findAll('script', attrs={'type': 'text/javascript'})
    for sc in scripts:
        if re.search(r'{"_id":.*}', sc.get_text(), re.M | re.I):
            json = re.search(r'{"_id":.*}', sc.get_text(), re.M | re.I).group()

#保存明细json
def save_descjson(html):
    with open(dir + '\\Spectra\\JSON\\descjson.json', 'a+', encoding='utf-8_sig') as f:
        f.write(html + '\n')

#获取结构式图片
def save_Img_Structure(url):
        resp=requests.get(url,headers=headers)
        if resp.status_code == 200:
            html=resp.text()
            # 取sbCompound
            sbCompound = re.findall("/compound/.*.png", url)[0].replace('.png', '').replace('/compound/', '')
            img_src=dir + '\\Spectra\\STRUCTURE\\' + sbCompound + '.png'
            print('--------------------------------')
            urllib.request.urlretrieve(html, img_src)
            #save_Img(html,img_src)
            print('保存'+sbCompound+'化学式结构完成！')

#获取光谱图
def save_Img(html,img_src):
    bytes_stream = BytesIO(html)
    # 读取到图片
    # roiimg = Image.open(bytes_stream)
    roiimg=''
    imgByteArr = BytesIO()  # 初始化一个空字节流
    roiimg.save(imgByteArr, format('PNG'))  # 把我们得图片以‘PNG'保存到空字节流
    imgByteArr = imgByteArr.getvalue()  # 无视指针，获取全部内容，类型由io流变成bytes。
    with open(img_src, 'wb') as f:
        f.write(imgByteArr)

#通过CAS号获取主页信息
def search_CAS(cas):
        resp=requests.get('https://spectrabase.com/search?q=CAS+'+cas,headers=headers)
        assert resp.status_code == 200
        html=resp.text
        htmls.append(html)


#保存结构式图片和urls中新增光谱明细数据
def get_tab(html):
    soup = BeautifulSoup(html,'lxml')
    #print(soup.prettify())
    print(soup.title.string)
    if soup.h4 is None:

        #1、取物质主页中json数据
        scripts=soup.findAll('script',attrs={'type':'text/javascript'})
        for sc in scripts:
            if re.search(r'{"_id":.*}',sc.get_text(), re.M|re.I):
                json=re.search(r'{"_id":.*}',sc.get_text(), re.M|re.I).group()

        #2、获取物质结构式
        url_structure=url_home+soup.img['src']
        print("STRUCTURE URL:"+url_structure)

        #取sbCompound
        sbCompound=re.findall("/compound/.*.png",url_structure)[0].replace('.png','').replace('/compound/','')
        print(sbCompound)
        tables=soup.findAll('table')
        tab=tables[0]
        tds=[]
        str=''
        for td in tab.findAll('td'):
            str=str+td.getText().replace('Google Search','').replace('\n','').strip()+"^|"
            save_text(str,sbCompound)
            tds.append(str)
        #print(soup.table.contents)      #table标签的子节点列表
        #for children in soup.table.children:
        #    print(children)
        #print(soup.img.attrs['src'])    #标签属性
        urls=[]
        for a in soup.findAll('a'):
            if 'alt' in a.attrs and a.attrs['alt']!='WSS Home' and a.attrs['alt']!='Home':
                urls.append(url_home+'/api'+a.attrs['href'])
                print(url_home+'/api'+a.attrs['href'])
                #print(a.get('href')+"------"+a.get('alt'))
            #print(a.attrs['href'])
        #for img in soup.findAll('img'):
            #if img.attrs['alt']=='Acetylsalicylic acid':
            #    url_structure = 'https://spectrabase.com' + img.attrs['src']
            #    print('url_structure:'+url_structure)
            #elif img.attrs['alt']=='Raman Spectrum':
            #    print(img.attrs['lazy-load'])
            #else:
            #    pass
            #     url_spectra='https://spectrabase.com'+img.attrs['lazy-load']
            #     print(img.attrs['lazy-load'])
        #print(soup.img.next_sibling)
        #平行遍历
        #for sibling in soup.img.next_siblings:
        #    print(sibling.name)

#保存html内容到文件
def save_text(str,specid):
    # 保存json文件
    file_name =specid+ '.txt'
    with open(dir+'\\Spectra\\txt\\' + file_name, 'w', encoding='utf-8_sig') as f:
        f.write(str+'\n')

#保存光普和明细数据
async def get_html(url):
    async with sem:
        async with aiohttp.ClientSession(trust_env = True,headers=headers,cookies=cookies) as session:  #获取session
            async with session.request('GET', url) as resp:  # 提出请求
                if resp.status==200:
                    if resp.content_type=='image/png':
                        img_src=dir + '\\Spectra\\spectrum\\'+re.findall("/spectrum/.*.png",url)[0].replace('.png','').replace('/spectrum/','')+'.png'
                        html=await resp.read()
                        urllib.request.urlretrieve(html, img_src)
                    elif resp.content_type=='application/json':
                        save_descjson(await resp.text())
                #print('异步获取%s下的html.'% url)

def get_html2(url):
            resp=requests.get(url,headers=headers)
            print(url)
            if url.split('.')[-2].split('?')[0]=='png':
                html = resp.content
                img_src=dir + '\\Spectra\\spectrum\\'+re.findall("/spectrum/.*.png",url)[0].replace('.png','').replace('/spectrum/','')+'.png'
                with open(img_src, 'wb') as outfile:
                    outfile.write(html)
                #urllib.request.urlretrieve(html, img_src)
            else:
                html = resp.text
                with open(dir + '\\Spectra\\JSON\\descjson.json', 'a+', encoding='utf-8_sig') as f:
                    f.write(html + '\n')

#协程调用，请求网页
def main_get_html():
    loop = asyncio.get_event_loop()  # 获取事件循环
    tasks = [get_html(url) for url in urls]  # 把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))    #激活协程

#使用多进程解析主页html，把光谱明细url添加到urls中，执行 get_html
def multi_parse_html(html,cnt):
    soup = BeautifulSoup(html, 'lxml')
    print(soup.title.string)
    if soup.h4 is None:
        # 2、获取物质结构式
        url_structure = url_home + soup.img['src']
        print("STRUCTURE URL:" + url_structure)
        #save_Img_Structure(url_structure)
        #https://spectrabase.com:/api/compound/3EvKR6yOXcn.png?ph=true&h=300&w=328
        img_src = dir + '\\Spectra\\STRUCTURE\\' + url_structure.split('/')[-1].split('?')[0]
        print(img_src)
        #urllib.request.urlretrieve(url_structure,img_src)
        r = requests.get(url_structure,headers=headers)
        with open(img_src, 'wb') as outfile:
            outfile.write(r.content)

        print('----------------------')
        tables = soup.findAll('table')
        tab = tables[0]
        tds = []
        str = ''
        #表格1内容
        sbCompound = re.findall("/compound/.*.png", url_structure)[0].replace('.png', '').replace('/compound/', '')
        for td in tab.findAll('td'):
            str = str + td.getText().replace('Google Search', '').replace('\n', '').strip() + "^|"
        save_text(str, sbCompound)
        global urls
        for a in soup.findAll('a'):
            if 'alt' in a.attrs and a.attrs['alt'] != 'WSS Home' and a.attrs['alt'] != 'Home':
                urls.append(url_home + '/api' + a.attrs['href'])
                urls.append(url_home + '/api' + a.attrs['href']+'.png?h=516.9375&w=919')
    print('第%d个html-----------date:%s'% (cnt,time.time()))

#多进程调用总函数，解析html
def main_parse_html():
    p=Pool(2)
    i=0
    for html in htmls:
        i+=1
        p.apply_async(multi_parse_html,args=(html,i))
    p.close()
    p.join()


urls=[]
def get_url():
    with open('C:\\Uers\\PharmaOryx-YJ\\PycharmProjects\\PharmaOryx\\psectra_1~100w.csv','r',encoding='utf-8') as f:
        csv_reader=reader(f)
        list_of_rows=list(csv_reader)
        for i in range(0,len(list_of_rows)):
            urls.append(list_of_rows[i][1])

if __name__ == '__main__':
    get_url()

    for url in urls:
        print('CAS:', url)
        htmls=[]
        i=0
        for html in htmls:
            multi_parse_html(html, i)
            i+=1
        for url in urls:
            get_html2(url)

        # i = 0
        # for html in htmls:
        #     i += 1
        #     multi_parse_html(html,i)
