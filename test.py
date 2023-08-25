import csv
from csv import reader

urls=[]
def get_url():
    with open('E:\\work\\djrm\\ykb\\body.csv','r',encoding='utf-8_sig') as f:
        csv_reader=reader(f)
        list_of_rows=list(csv_reader)
        for i in range(0,len(list_of_rows)):
            if(len(list_of_rows[i])>1):
                urls.append(list_of_rows[i])

def tocsv(fileNmae,rows):
    with open('E:\\work\\djrm\\ykb\\'+fileNmae,'a+', newline='',encoding="utf-8-sig") as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)

if __name__ == '__main__':
    get_url()
    new_url=[]
    for url in urls:
        if url not in new_url:
            new_url.append(url)
        #去重

    tocsv('test.csv',new_url)