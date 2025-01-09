import re
import os
import openpyxl
import time
#获取当前文件夹路径



paths = os.getcwd()
paths='C:\\Users\\PharmaOryx-YJ\\Desktop\\pubchemdata'
lists = os.listdir(f'{paths}//XML3')

# def lista(shu):
#     d = []
#     for bb in range(shu+1):
#         d.append("")
#     return d

def tbsd(tst,rename):
    regex = f"<TOCHeading>{rename}</TOCHeading>.*?<Number>([^<]+)<\/Number>"
    if rename =="Topological Polar Surface Area_value":
        regex = f"<TOCHeading>Topological Polar Surface Area</TOCHeading>.*?<Unit>([^<]+)<\/Unit>"

    stk = re.findall(regex,tst,re.MULTILINE | re.DOTALL)
    if stk:
        return stk[0]
    else:
        return ''



def rsss(files):
    with open(f'{paths}/XML3/{files}',encoding="utf-8") as sldfj:
        ppp = sldfj.read()
    # regex = r"</Section>\s+<Section>\s+<TOCHeading>([^<]+)<\/TOCHeading>.*?<(?:String|DateISO8601)>([^<]+)<\/(?:String|DateISO8601)>"
    regex = r" <RecordNumber>([^<]+)<\/RecordNumber>"
    smart = []
    cid = re.findall(regex,ppp)
    if cid:
        smart.append(cid[0])
    else:
        smart.append('')
    asdf = [
                'XLogP3',
                'Hydrogen Bond Donor Count',
                'Hydrogen Bond Acceptor Count',
                'Rotatable Bond Count',
                'Topological Polar Surface Area',
                'Topological Polar Surface Area_value',
                'Heavy Atom Count',
                'Formal Charge',
                'Complexity',
                'Isotope Atom Count',
                'Defined Atom Stereocenter Count',
                'Undefined Atom Stereocenter Count',
                'Defined Bond Stereocenter Count',
                'Undefined Bond Stereocenter Count',
                'Covalently-Bonded Unit Count'
            ]
    for gelas in asdf:
        # print(gelas,tbsd(ppp,gelas))
        kuba = tbsd(ppp,gelas)
        if kuba:
            smart.append(kuba)
        else:
            smart.append("")
    return smart



zonglists = []
for bbb in lists:
    if bbb.endswith(".xml"):
        kd = rsss(bbb)
        if kd:
            zonglists.append(kd)
lieming = ['CID', 'XLogP3',
                'Hydrogen Bond Donor Count',
                'Hydrogen Bond Acceptor Count',
                'Rotatable Bond Count',
                'Topological Polar Surface Area',
                'Topological Polar Surface Area_value',
                'Heavy Atom Count',
                'Formal Charge',
                'Complexity',
                'Isotope Atom Count',
                'Defined Atom Stereocenter Count',
                'Undefined Atom Stereocenter Count',
                'Defined Bond Stereocenter Count',
                'Undefined Bond Stereocenter Count',
                'Covalently-Bonded Unit Count']



wb = openpyxl.Workbook()
# 获取活跃的工作表，ws代表wb(工作簿)的一个工作表
ws = wb.active
# 更改工作表ws的title
ws.title = 'test_sheet1'

ws.append(lieming)



for kjid in zonglists:

    ws.append(kjid)
wb.save(f'{time.time()}.csv')
print("全部任务执行完毕，程序在50秒后自动退出！")
time.sleep(50)