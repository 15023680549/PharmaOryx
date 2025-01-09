import urllib
from csv import reader
from multiprocessing import Pool

import aiohttp
import asyncio
import re
import os
import time
import csv

#1、判断目录是否存在
dir=os.getcwd()
sem=asyncio.Semaphore(10) #信号量，控制协程数量，防止爬的过快
htmls=[]
urls=[]

cookies={
    'cookie':'osano_consentmanager_uuid=2c7ff550-84f1-44b0-8fd2-71c083df0b2d; osano_consentmanager=LACoDQXFiWJ5d88SbSJkt4S_KAdD_iNA-oKIjmaHPtxjcdjgmH-hsNmDBsr3GIJkk_Wm2ytpX9KBAmytZOl7HtjSaKk5jyZbNyBkyGOLMhkQGnz5BbZhNxvpPbtaZoGqBkYax19GKMiAV4dS9tb0LyBFv1L0dQ71B8XCHAWIWK4Jth8hrCTGJEyy84dJ2Om57cDUonThquvBi9yQ8AVuAlc-vGJSaihoN8LhrNg2td2QlyHR1nRPoB4_oHmY4GG0QR6mCu7YvW5KvgPqfj8RH2djGFelORmidKlHRA==; s_fid=058AAB48EA171EC1-3E2EC97AEED6650A; s_cc=true; _fbp=fb.1.1653383212785.1617112061; __gads=ID=51efcc02d38ba074:T=1653383206:S=ALNI_MaXwtiV-7K4pHn0b6q4cdHw6p7FXw; __gpi=UID=000005b267fa2c76:T=1653383206:RT=1653442009:S=ALNI_MaJjxQ_WM2m8X0jZOEMMPyABDcD5w; auth_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik4wRkdRemhHUkRoQk56TkROa0l3TmpjMVJUSTFOelpHTlRrNE1EZzBOMFZCUlRVME1USXdOQSJ9.eyJodHRwczovL3NwZWN0cmFiYXNlLmNvbS9uYW1lIjoiWW9uZyBKaWFuZyIsImdpdmVuX25hbWUiOiJZb25nIiwiZmFtaWx5X25hbWUiOiJKaWFuZyIsIm5pY2tuYW1lIjoiankxNTAyMzY4MDU0OSIsIm5hbWUiOiJZb25nIEppYW5nIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdqOE9BWVdPMVZTNjdDTk1FOTJOcnlpNzlwOVMtb2lvOVNPN0VtbD1zOTYtYyIsImxvY2FsZSI6InpoLUNOIiwidXBkYXRlZF9hdCI6IjIwMjItMDUtMjVUMDI6NDQ6NTUuNzAwWiIsImlzcyI6Imh0dHBzOi8vc3BlY3RyYWJhc2UuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE1MTM3MTUxMjU1NjIyNjM1MDk5IiwiYXVkIjoiZ25CZzU1MDNzbnlOZm9DbUx0aTZkdXM3WEhneWVubTAiLCJpYXQiOjE2NTM0NDY2OTYsImV4cCI6MTY1MzQ4MjY5NiwiYXRfaGFzaCI6IkVWY0N0bTdoYkFWVGpqMnljeUtDd2ciLCJub25jZSI6IlNqUG9MTlVvbFNSSC1kc2ljOVU1fnJMWEVKUzh6WVBsIn0.BGKFW122_-nmcP1xMC-tb4-kZX2hdReLQL8LFfGQJkUY5Souwp5zMxY2IMx1PacS5KPId9ZMuEtfwosJA6dZCyNCT9-lXweND1DjoZcGk_Buor4ZS8gp7VJddQzogzrEbuGchLni8URrhp843msVoj9Snax5o5EIEVbfHq8cAQDnvC0P4jIBd6WG2O0Uh_3L7PgZ0fP3I039Nq-8C3fur6HfK8tTz6tbAMMBYMhKAkHPa1EH6h33FAoFSIqWL6NThvJE2jQFXPZYKo6MLkgE1ZNNSYlba7SyAMvcwUE4ojZdAfyuvgqDFxvZBsSxoHTG0JG402cS7ShJELlJzkRwDQ; access_token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9zcGVjdHJhYmFzZS5hdXRoMC5jb20vIn0..IQsc8ZNHsiET29cV.cU1zkn3hUelR58up5mV5y_NYpzrho_Czs3C7isQ6MST9Q7oQ5cEm3cd8AEyov3EdRpJsjS0d4aqpqv4Jnnq3kkYZj08o_nGdGtCGnLN2y27mrp0fEVdSwyjHe0gf3v4dteMifNzkxnHzgoGSNDwblXlmOck_rUo0Bw1lz8Bxbn8KozQdQxEqwJ0kZrCDaGObxK6GEPChemgjJWKu4bdJ93a9f-qQPhjqSb9iaMgvubsTIBWgqjlC4m0CwiDoLG_rzGMRNq3tkcxdetpL9NdkOC7v3nHwpokq43wUerTvl6Ci-UTI-MGR048.ozjp1-H9wSLmKrhJhXeXgQ; s_sq=[[B]]',
}

headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}

def savetocsv(fileNmae,rows):
    with open(fileNmae, 'a+', newline='', encoding="utf-8") as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)

#协程调用，请求网页
def main_get_html():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # loop = asyncio.get_event_loop()  # 获取事件循环
    tasks = [get_structrue(url) for url in urls]  # 把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))    #激活协程

#保存明细json数据
async def get_detialjson(url):
    async with sem:
        async with aiohttp.ClientSession(trust_env = True,headers=headers,cookies=cookies) as session:  #获取session
            async with session.request('GET',url) as resp:
                json=await resp.text()
                savetocsv('',[json])


#保存光普和明细数据
async def get_structrue(url):
    file_name ='C:\\Users\\PharmaOryx-YJ\\Desktop\\data\\SpectraBase\\spectra1~100w\\' + re.findall("/spectrum/.*.png", url)[0].replace('.png', '').replace(
        '/spectrum/', '') + '.png'
    if(os.path.exists(file_name)):
        return
    async with sem:
        async with aiohttp.ClientSession(trust_env = True,headers=headers,cookies=cookies) as session:  #获取session
            async with session.request('GET',url) as resp:  # 提出请求
                if resp.status==200:
                    html=await resp.read()
                    with open(file_name,'wb') as f:
                        f.write(html)
                    print(file_name)
                    #urllib.request.urlretrieve(html, file_name)


#使用多进程解析主页html，把光谱明细url添加到urls中，执行 get_html
def multi_parse_html(html,cnt):
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
    with open('E:\\work\\djrm\\ykb','r',encoding='utf-8') as f:
        csv_reader=reader(f)
        list_of_rows=list(csv_reader)
        for i in range(0,len(list_of_rows)):
            if(len(list_of_rows[i])>1):
                urls.append(list_of_rows[i][1].replace('/spectrum/','/api/spectrum/')+'.png?h=239.0625&ph=true&w=425')  #图谱url

if __name__ == '__main__':
    get_url()
    main_get_html()
    # for url in urls:
    #     print(file_name)


        #https://spectrabase.com:/api/spectrum/62FpZ54WHqZ.png?h=239.0625&ph=true&w=425
        #https://spectrabase.com/spectrum/6l4U8PvbT8K
        # htmls=[]
        # i=0
        # for html in htmls:
        #     multi_parse_html(html, i)
        #     i+=1
        # for url in urls:
        #     get_html2(url)
