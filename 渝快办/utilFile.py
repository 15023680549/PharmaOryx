#-*- coding : utf-8-*-
# coding:utf-8

import csv
import os
from csv import reader

dir=os.getcwd()
#存储数据之csv
def tocsv(fileNmae,rows):
    with open(dir+'\\'+fileNmae,'a+', newline='',encoding="utf-8-sig") as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)

def readurl(fileNmae):
    urls=[]
    with open(dir+'\\'+fileNmae,'r',encoding='utf-8-sig') as f:
        csv_reader=reader(f)
        list_of_rows=list(csv_reader)
        for i in range(0,len(list_of_rows)):
            urls.append(list_of_rows[i])
        return urls