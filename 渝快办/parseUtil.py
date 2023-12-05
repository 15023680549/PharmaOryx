import os
import csv
from csv import reader



dir=os.getcwd()
urls=[]
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

if __name__ == '__main__':
    readurl('渝快办body.csv')
    for url in urls:
        href=url[3]+'<span style="float: right;background: #1b6ecc" class="ayui-btn layui-btn-xs layui-btn-normal"><a href="'+url[1]+'" target="_blank" style="color: white;">查看网页</a></span>'
        tocsv('渝快办body精准问答.csv',[[url[0],href]])