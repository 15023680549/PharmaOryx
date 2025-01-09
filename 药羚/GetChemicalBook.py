import csv

from bs4 import BeautifulSoup
import requests
import aiohttp
import asyncio
from multiprocessing import Pool
import os
import urllib.request
import re


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

urls=[]
htmls=[]
sem=asyncio.Semaphore(2) #信号量，控制协程数量，防止爬的过快



def get_url(url):
    response=requests.get(url,headers=headers)#有机
    html=response.text
    #1、取所有物质url
    soup = BeautifulSoup(html, 'lxml')
    lx=soup.title.string
    #id='Productleft'
    Productleft = soup.find_all(id='Productleft')
    i=1
    for div in Productleft[0].contents:
        dl=''
        xl=''
        if i!=1:
            dl=div.h2.a.string      #大类
            if div.dt:
                xl=div.dt.string    #小类
            #print(div.prettify())
            for em in div.findAll('em'):
                urls.append([dl,xl,em.a.string,'https://www.chemicalbook.com'+em.a.attrs['href'],lx])
        i+=1

    #id='Productright'
    Productright = soup.find_all(id='Productright')
    i = 1
    for div in Productright[0].contents:
        dl = ''
        xl = ''
        if i != 1:
            dl = div.h2.a.string  # 大类
            if div.dt:
                xl = div.dt.string  # 小类
            # print(div.prettify())
            for em in div.findAll('em'):
                url='https://www.chemicalbook.com'+em.a.attrs['href']
                urls.append([dl, xl, em.a.string, url])
        i += 1

#保存为csv文件
def save_csv(name,rows):
    with open('C:\\Users\\PharmaOryx-YJ\\Desktop\\data\\chemicalbook\\' + name+'.csv', 'a+', encoding='utf-8_sig',newline='') as f:
        f_output=csv.writer(f)
        f_output.writerows(rows)

async def get_html(url):
    async with sem:
        async with aiohttp.ClientSession(trust_env = True,headers=headers,cookies=cookies) as session:  #获取session
            async with session.request('GET',url[3]) as resp:  # 提出请求
                html=await resp.text()
                htmls.append([html,url])
                print('异步获取%s下的html.'% url[3])

#协程调用，请求网页
def main_get_html():
    loop = asyncio.get_event_loop()  # 获取事件循环
    tasks = [get_html(url) for url in urls]  # 把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))    #激活协程

#使用多进程解析html
def multi_parse_html(html,url,cnt):
    print(url)
    rows = []
    soup = BeautifulSoup(html, 'lxml')
    if soup.find('table') is not None:
        tables=soup.find('table').contents[1].contents[3].findAll('table')
        print(len(tables))

        for i in range(0,len(tables)):
            try:
                req=tables[i].findAll('tr')[1].td.text
                if re.search('性质', tables[i].findAll('tr')[1].td.text, re.M | re.I):
                    print('----------性质')
                    for tr in tables[i+1].findAll('tr'):
                        tds = tr.findAll('td')
                        if tds[1].font:
                            str=tds[1].font.text
                        else:
                            str=tds[1].string
                        rows.append([url[2], '性质', tds[0].string, str])

                elif re.search('用途与合成方法', tables[i].findAll('tr')[1].td.text, re.M | re.I):
                    print('----------用途与合成方法')
                    for tr in tables[i+1].findAll('tr'):
                        tds = tr.findAll('td')
                        if tds[1].font:
                            str=tds[1].font
                        #print(tds[0].string+':', tds[1].text)
                        rows.append([url[2], '用途与合成方法', tds[0].string, str])
                elif re.search('价格', tables[i].findAll('tr')[1].td.text, re.M | re.I):
                    print('--------------价格')
                    for tr in tables[11].findAll('tr'):
                        tds = tr.findAll('td')
                        #print(tds[0].text,tds[1].text,tds[2].text,tds[3].text,tds[4].text)
                        save_csv('价格',[[url[2],tds[0].text,tds[1].text,tds[2].text,tds[3].text,tds[4].text]])

                elif re.search('上下游产品信息', tables[i].findAll('tr')[1].td.text, re.M | re.I):
                    print('--------------上下游信息')
                    for tr in tables[i+1].findAll('tr'):
                        tds = tr.findAll('td')
                        str=tds[1].text
                        #print(tds[0].string,tds[1].text)
                        rows.append([url[2], '上下游产品信息', tds[0].string, str])

                elif i == 1:
                #elif url[2]==tables[i].findAll('tr')[1].td.text:
                    print('--------基本信息')
                    for tr in tables[1].findAll('tr'):   #商品基础信息
                        tds=tr.findAll('td')
                        str=''
                        if tds[0].string=='Mol文件:':
                            str=tds[1].string
                            #print(tds[0].string,tds[1].string)
                            urllib.request.urlretrieve('https://www.chemicalbook.com/'+tds[1].a.attrs['href'], 'C:\\Users\\PharmaOryx-YJ\\Desktop\\data\\chemicalbook\\mol\\'+tds[1].string)
                        elif len(tds)==1 and 'src' in tds[0].img.attrs:
                            if tds[0].img.attrs['src']:
                                str=tds[0].img.attrs['src'].split('/')[-1]
                                urllib.request.urlretrieve('https://www.chemicalbook.com/' + tds[0].img.attrs['src'],
                                                           'C:\\Users\\PharmaOryx-YJ\\Desktop\\data\\chemicalbook\\structure\\' + str)
                            else:
                                str='无图片'
                        elif tds[1].font:
                            for f in tds[1].findAll('font'):
                                str+=f.string+';'
                            #print(tds[0].string,str)
                        elif tds[1].a:
                            for a in tds[1].findAll('a'):
                                str+=a.string+';'
                            #print(tds[0].string,str)
                        else:
                            str=tds[1].string
                            #print(tds[0].string,tds[1].string)
                        rows.append([url[2],'基本信息',tds[0].string,str])


                elif re.search('安全信息', tables[i].findAll('tr')[1].td.text, re.M | re.I):
                    print('-----------安全信息')
                    for tr in tables[i+1].findAll('tr'):
                        tds = tr.findAll('td')
                        str=''
                        if tds[1].font:
                            for f in tds[1].findAll('font'):
                                str += f.string + ';'
                            #print(tds[0].string+':', str)
                        elif tds[1].a:
                            for a in tds[1].findAll('a'):
                                str += a.string + ';'
                        rows.append([url[2], '安全信息', tds[0].string, str])

                elif re.search('MSDS信息', tables[i].findAll('tr')[1].td.text, re.M | re.I):
                    print('--------------MSDS信息')
                    for tr in tables[i+1].findAll('tr'):
                        tds = tr.findAll('td')
                        if len(tds)>1:
                            str=tds[1].string
                            #print(tds[0].a.string+':',tds[1].string)
                            rows.append([url[2], 'MSDS信息', tds[0].a.string, str])
            except:
                print('无记录')
        save_csv('baseinfo',rows)

#多进程调用总函数，解析html
def main_parse_html():
    p=Pool(2)
    i=0
    for html,url in htmls:
        i+=1
        print(html)
        p.apply_async(multi_parse_html,args=(html,url,i))
    p.close()
    p.join()

if __name__ == '__main__':
    for url2 in ['https://www.chemicalbook.com/ChemicalProductsList_69.htm']:
        urls=[]
        htmls=[]
        get_url(url2)
        #urls=[['醚类化合物及其衍生物', '醚、醚醇', '2-硝基苯甲醚', 'https://www.chemicalbook.com/ProductChemicalPropertiesCB1101492.htm']
        # ,['氨基化合物','含氧基氨基化合物','对氨基苯磺酸','https://www.chemicalbook.com/ProductChemicalPropertiesCB2181554.htm']
        #]
        save_csv('names',urls)
        #main_get_html()
        print('---------开始执行main_parse_html')
        #main_parse_html()
        j=1
        # for html,url in htmls:
        #     multi_parse_html(html,url,j)
        #     j+=1
        print('---------完成main_parse_html')