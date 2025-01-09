import re
import os
import openpyxl
import time

# 获取当前文件夹路径


# paths = os.getcwd()
paths = 'C:\\Users\\PharmaOryx-YJ\\Desktop\\pubchemdata\\pubchem1~100w\\XML'
lists = os.listdir(f'{paths}/XML')
REGEX_NUMBER = re.compile("<RecordNumber>([^<]+)<\/RecordNumber>")
#REGEX_Wikipedia = re.compile("<TOCHeading>Wikipedia</TOCHeading>.*?<URL>([^<]+)<\/URL>")
#REGEX_Wikipedia = re.compile(r"<TOCHeading>Wikidata</TOCHeading>.*?<URL>([^<]+)<\/URL>", re.MULTILINE | re.DOTALL)

asdf = [
'30',
'31',
'32',
'33',
'34',
'35',
'36',
'37',
'38',
'39',
'40',
'41',
'42',
'43',
'44',
'45',
'46',
'47',
'48',
'49',
'50',
'51',
'52',
'53',
'54',
'55',
'56',
'57',
'58',
'59',
'60',
'61',
'62',
'63',
'64',
'65',
'66',
'67',
'68',
'69',
'70']

lieming = ['CID','30',
'31',
'32',
'33',
'34',
'35',
'36',
'37',
'38',
'39',
'40',
'41',
'42',
'43',
'44',
'45',
'46',
'47',
'48',
'49',
'50',
'51',
'52',
'53',
'54',
'55',
'56',
'57',
'58',
'59',
'60',
'61',
'62',
'63',
'64',
'65',
'66',
'67',
'68',
'69',
'70']

asdf_regex_dict = {}
for item in asdf:
    asdf_regex_dict[item] = re.compile(
        "<ReferenceNumber>{}</ReferenceNumber>.*?<URL>([^<]+)<\/URL>".format(item),
        re.MULTILINE | re.DOTALL)
    #print(asdf_regex_dict[item])


def tbsd(tst, rename):
    if rename == "Wikidata":
        REGEX = REGEX_Wikipedia
    elif rename == "Molecular Weight_value":
        REGEX = REGEX_Molecular
    else:
        REGEX = asdf_regex_dict.get(rename)
        #print(REGEX)
    stk = REGEX.findall(tst)
    if stk:
        return stk[0]
    else:
        return ''


def rsss(files):
    with open(f'{paths}/XML/{files}', encoding="utf-8") as f:
        ppp = f.read()

    smart = []
    cid = REGEX_NUMBER.findall(ppp)
    if cid:
        smart.append(cid[0])
    else:
        smart.append('')
    for gelas in asdf:
        kuba = tbsd(ppp, gelas)
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
# time.sleep(50)