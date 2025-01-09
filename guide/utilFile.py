#-*- coding : utf-8-*-
# coding:utf-8

import csv
import os
from csv import reader
import requests
import json
import re
from urllib.parse import unquote
from urllib import parse
import itertools
import traceback
import time

dir=os.getcwd()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
           'zwzt-app-proxy':'cqzwzt',
           }

#a 、a+追加,w 、w+覆盖
#存储数据之csv
def tocsv(fileNmae,rows,type):
    with open(dir+'\\'+fileNmae,type, newline='',encoding="utf-8-sig") as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)

def readurl(fileNmae):
    urls=[]
    with open(dir+'\\'+fileNmae,'r',encoding='utf-8') as f:
        csv_reader=reader(f)
        list_of_rows=list(csv_reader)
        for i in range(0,len(list_of_rows)):
            urls.append(list_of_rows[i])
        return urls

#写入text文件
def toText(save_dir,fileNmae,text,type):
    with open(dir+'\\'+save_dir+'\\'+fileNmae,type,encoding='utf-8-sig') as f:
        f.write(text)

def get_unique_filename(directory, filename):
    """
    检查文件名是否存在，若存在则自动重命名，添加编号后缀。
    """
    base_name, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base_name}_{counter}{extension}"
        counter += 1
    return new_filename

class UtilFile:
    def DownloadFile(self,save_dir,url):
        # save_dir = 'images'
        # 创建目录（如果不存在）
        if not os.path.exists(dir+'\\'+save_dir):
            os.makedirs(dir+'\\'+save_dir)
        try:
            print("开始下载文件...")
            time.sleep(0.2)
            response = requests.get(url, stream=True,headers=headers)
            response.raise_for_status()  # 检查请求是否成功

            # 获取文件名：尝试从 Content-Disposition 头中提取
            content_disposition = response.headers.get("Content-Disposition", "")
            file_name = None
            if content_disposition:
                match = re.search(r'fileName\*?=["\']?(?:UTF-8\'\')?([^"\';]+)', content_disposition)
                if match:
                    file_name = match.group(1)
                    file_name = unquote(file_name.encode('latin1').decode('utf-8'))  # 处理文件名编码

            # 方法 2: 如果没有 Content-Disposition，从 URL 提取文件名
            if not file_name:
                file_name = os.path.basename(url.split("?")[0])

            # 方法 3: 设置兜底默认文件名
            if not file_name:
                file_name = "default_file"

            # 检查文件是否存在并生成唯一文件名
            file_name = get_unique_filename(save_dir, file_name)

            # 设置保存路径
            save_path = os.path.join(dir+'\\'+save_dir, file_name)

            # 将内容写入文件
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):  # 分块下载
                    file.write(chunk)

            return file_name
        except requests.exceptions.RequestException as e:
            print(f"下载失败: {e}")

    #取材料清单getMatterId
    def getMatterId(self,onlineUrl,materialUrl):
        if onlineUrl!=None:
            result = parse.urlparse(onlineUrl.replace('#',''))
            query_dict = parse.parse_qs(result.query)
        else:
            response = requests.get(materialUrl,headers=headers)
            result = parse.urlparse(response.url.replace('#',''))
            query_dict = parse.parse_qs(result.query)
        return query_dict['matterId'][0]

    #通过matterId获取到问题
    def getQuestByMatterId(self,matterId):
        ans = ''
        # x=0
        try:
            data = {"matterId":matterId,"matterType":"single","preview":'false'}
            questRes = requests.post('https://cqzwfw.cqdcg.com/form/api/nologin/guidance/render',json=data,headers=headers,timeout=2)
            questDict = questRes.json()
            if 'data' in questDict:
                rootList = questDict['data']['rootList']

                # 根据 optionType 处理 children 的取值逻辑
                processed_children = []

                for item in rootList:
                    bizcode = item['bizCode']
                    questName = item['name']+':'
                    if item['optionType'] == '2':
                        # 多选：生成非空子集
                        children = item['children']
                        subsets = []
                        for i in range(1, len(children) + 1):  # 从1到len(children)生成所有非空子集
                            subsets.extend(itertools.combinations(children, i))
                        # 保存为 {'bizcode': ..., 'quest': ...} 格式
                        processed_children.append([{'Q':questName+subset['name'],'bizcode': bizcode, 'quest': list(subset['bizCode'])} for subset in subsets])
                    elif item['optionType'] == '1':
                        # 单选：每次只能取一个值
                        processed_children.append([{'Q':questName+child['name'],'questionCode': bizcode, 'optionList': [child['bizCode']]} for child in item['children']])
                # 生成所有组合
                combinations = list(itertools.product(*processed_children))

                # 格式化结果
                result = []
                for combo in combinations:
                    result.append(list(combo))  # 每个组合是一个列表，其中每项是一个字典

                # 打印结果
                for idx, combination in enumerate(result, start=1):
                    for condition in combination:
                        ans += condition['Q']+' '
                        # condition.pop('Q')
                    #从问题去请求答案
                    data = {"matterId":matterId,"matterType":"single","preview":'false',"selectedList":combination,"fieldValues":{},"questionFieldValue":{}}
                    anRes = requests.post('https://cqzwfw.cqdcg.com/form/api/nologin/guidance/submit', json=data,headers=headers,timeout=3)
                    # while x<3:
                    #     anRes = requests.post('https://cqzwfw.cqdcg.com/form/api/nologin/guidance/submit', json=data,headers=headers)
                    #     if 'data' not in anRes.json():
                    #         time.sleep(1)
                    #         x+=1
                    #         continue
                    #     else:
                    #         break
                    if 'data' not in anRes.json():
                        return ans
                    anDict = anRes.json()['data']['materialAndGroup']
                    ans +='\n'
                    for group in anDict['materialGroups']:
                        ans +=group['groupTitle']+'('+group['groupTip']+'):\n'
                    if len(anDict['materials'])!=0:
                        for i,material in enumerate(anDict['materials'],start=1):
                            requireType = ''
                            materialTypeDes = ''
                            source = ''
                            sourceDesc = ''
                            if 'materialGuide' in material:
                                if 'materialTypeDes' in material["materialGuide"]:
                                    materialTypeDes = material["materialGuide"]["materialTypeDes"]
                            if 'extend' in material:
                                if 'requireType' in material["extend"]:
                                    requireType = material["extend"]["requireType"]
                            if 'materialFormDesc' in material:
                                materialFormDesc = material["materialFormDesc"]
                            if 'source' in material:
                                source=material["source"]
                            if 'sourceDesc' in material:
                                sourceDesc = material["sourceDesc"]
                            ans += f'序号:{i},材料名称:{material["materialName"]},材料类型:{materialTypeDes},来源及渠道说明:{source}({sourceDesc}),材料形式:{materialFormDesc},材料必要性:{requireType}\n'
                    else:
                        ans +='当前办理情况，无需准备任何材料\n'
            else:
                data = {"guidanceId": "SG20241218161222962539", "matterId": matterId, "matterType": "single","preview": 'false', "selectedList": []}
                anRes = requests.post('https://cqzwfw.cqdcg.com/form/api/nologin/guidance/submit', json=data,
                                      headers=headers,timeout=3)
                anResJson = anRes.json()
                # while x<3:
                #     anRes = requests.post('https://cqzwfw.cqdcg.com/form/api/nologin/guidance/submit',json=data,headers=headers)
                #     anResJson = anRes.json()
                #     if 'data' not in anResJson:
                #         time.sleep(1)
                #         x+=1
                #         print("无data："+anRes.text)
                #         continue
                #     else:
                #         break
                if 'data' not in anResJson:
                    return ans
                anDict = anRes.json()['data']['materialAndGroup']
                if 'materialAndGroup' not in anRes.json()['data']:
                    print("无materialAndGroup："+anRes.text)
                for group in anDict['materialGroups']:
                    ans += group['groupTitle'] + '(' + group['groupTip'] + '):\n'
                for i,material in enumerate(anDict['materials'],start=1):
                    requireType=''
                    materialTypeDes=''
                    source=''
                    sourceDesc=''
                    if 'materialGuide' in material:
                        if 'materialTypeDes' in material["materialGuide"]:
                            materialTypeDes=material["materialGuide"]["materialTypeDes"]
                    if 'extend' in material:
                        if 'requireType' in material["extend"]:
                            requireType=material["extend"]["requireType"]
                    if 'materialFormDesc' in material:
                        materialTypeDes=material["materialFormDesc"]
                    if 'source' in material:
                        source = material["source"]
                    if 'sourceDesc' in material:
                        sourceDesc = material["sourceDesc"]
                    ans += f'序号:{i},材料名称:{material["materialName"]},材料类型:{materialTypeDes},来源及渠道说明:{source}({sourceDesc}),材料形式:{material["materialFormDesc"]},材料必要性:{requireType}\n'
                    # ans += f'序号:{i},材料名称:{material["materialName"]},材料类型:{material["materialFormDesc"]},来源及渠道说明:{source}({sourceDesc}),材料形式:{material["materialFormDesc"]},材料必要性:{requireType}\n'
        except Exception as ex:
            traceback.print_exc()
            print(ex)
        return ans

if __name__ == '__main__':
    # imgUrl = 'https://cqykb.cq.gov.cn/pc/xindian/item_guid/get_attach_info?cliengguid=d731dcd9-cd8d-4c43-85bb-ffddedf633a7&isOnline=false'
    # UtilFile.DownloadFile('',imgUrl)

    #matterId = getMatterId('https://cqzwfw.cqdcg.com/cqzwzt/online/accept#/accept/entry?matterType=single&matterId=1116464156627&hasLayout=true','https://cqzwfw.cqdcg.com/cqzwzt/ykb-spcx/ykb-spcx/matter/matterCodeExchange/redirect?type=onlyMatter&sourceReferNo=11500109552015745B4502014001000')
    # matterId = getMatterId(None,'https://cqzwfw.cqdcg.com/cqzwzt/ykb-spcx/ykb-spcx/matter/matterCodeExchange/redirect?type=onlyMatter&sourceReferNo=11500000009277567B400010914000916')
    #getQuestByMatterId(matterId)
    # getQuestByMatterId('1116464156627')
    # getQuestByMatterId('1116517490335')
    str = UtilFile.getQuestByMatterId('','1114587430918')
    print(str)