import xml.dom.minidom
try:
    import xml.etree.CElementTree as ET
except:
    import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
# import xml.etree.ElementTree as ET
import re
import csv
import os
from multiprocessing import Pool
import aiohttp
import asyncio
import time

dir=os.getcwd()

def tocsv(fileNmae,rows):
    with open(fileNmae,'a+', newline='',encoding="utf-8") as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)

def par_xml(file_name,cnt):
    print('第%d个html-----------date:%s'% (cnt,file_name))
    data = ''
    i = 0
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            i += 1
            if i != 3:
                data = data + line.replace('\n', '')
    root = ET.fromstring(data)
    if root.tag=='Fault':
        return
    cid = root.find('RecordNumber').text
    # 获取图谱url
    urls = root.findall('./Section/Section/Section/Information/URL')
    rows = []
    for url in urls:
        if re.match('https://spectrabase.com/spectrum/', url.text):
            rows.append([cid, url.text])
    if len(rows)>1:
        tocsv('spectra_100w.csv', rows)


def multi_parse_html(html,cnt):
    #print('第%d个html-----------date:%s'% (cnt,time.time()))
    pass

#多进程解析xml
def main_parse_html():
    paths = 'C:\\Users\\PharmaOryx-YJ\\Desktop\\pubchemdata\\XML'
    p = Pool(12)
    i = 0
    g=os.walk(paths)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            i+=1
            p.apply_async(par_xml,args=(paths+'\\'+file_name,i))
    p.close()
    p.join()

if __name__ == '__main__':
    main_parse_html()
