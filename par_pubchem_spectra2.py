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

dir=os.getcwd()

def tocsv(fileNmae,rows):
    with open(fileNmae,'a+', newline='',encoding="utf-8") as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)

def par_xml(file_name,cnt):
    print('第%d个html-----------date:%s'% (cnt))
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
            #print(url.text)
            rows.append([cid, url.text])
        tocsv('1~100w.csv', rows)

def main_parse_xml(path):
    p=Pool(8)
    i=0
    g=os.walk(path)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            i+=1
            p.apply_async(par_xml,args=(file_name,i))
    p.close()
    p.join()
#os.path.exists() 判断文件是否存在
#os.path.getsize() 判断文件大小

if __name__ == '__main__':
    g = os.walk(r"C:\Users\PharmaOryx-YJ\Desktop\pubchemdata\pubchem1~100w\XML\XML")
    main_parse_xml('C:\Users\PharmaOryx-YJ\Desktop\pubchemdata\pubchem1~100w\XML\XML')
    for path, dir_list, file_list in g:
        for file_name in file_list:
            file_name = 'C:\\Users\\PharmaOryx-YJ\\Desktop\\pubchemdata\\pubchem1~100w\\XML\\XML\\'+file_name
            par_xml(file_name)
        print(file_name)
