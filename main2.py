# -*- coding : utf-8-*-
# coding:utf-8
import requests
import sys
import datetime

from elasticsearch import Elasticsearch, helpers
from utils.GetData2 import getHtml,ggfwUrl,xzqlUrl,tocsv,readurl
from utils.utilMysql import MysqlTool

es = Elasticsearch('http://127.0.0.1:9200/')

#请求url,判断能否正常访问
def existsUrl(url):
    res = requests.get(url)
    if res.status_code!=200:
        return 0

#mysql和es字段映射和转换
def transform_row(row):
    """将 MySQL 字段映射为 Elasticsearch 字段"""
    return {
        "id": row["id"],                # 映射 MySQL 的 `id` 到 Elasticsearch 的 `id`
        "url": row["URL"],
        "title": row["TITLE"],             # 映射 `age` 到 `user_age`
        "name": row["NAME"],      # 映射 `created_at` 到 `timestamp`
        "zdName": row["ZD_NAME"],
        "content": row["CONTENT"],
        "aurhor": row["AURHOR"],
        "classification": row["CLASSIFICATION"]
    }

if __name__ == '__main__':
    orgcode = sys.argv[1]
    print(orgcode)
    #1、获取链接
    rows=[]
    rows = ggfwUrl(orgcode)
    rows.extend(xzqlUrl(orgcode))
    tocsv(f'{orgcode}url-{datetime.date.today()}.csv', rows, 'w+')
    #测试
    #rows=readurl('江北区url.csv')
    with MysqlTool() as db:
        sql = f"DELETE FROM r_know_library WHERE zd_name='渝快办' AND add_time<CURRENT_DATE()"
        db.execute(sql, None, commit=True)  #删除历史渝快办数据
        data=[]
        #2、获取内容、解析页面、插入数据库
        sql = f"INSERT INTO r_know_library(id,add_time,update_time,zt,click_num,zd_name,title,url,name,content,aurhor,org,fw_code,zrr_code,fr_code) " \
              f"VALUES (REPLACE(UUID(),'-',''),CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP(),2,0,'渝快办',%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for url in rows:
            d=getHtml(url)
            if d!=None:
                db.execute(sql, d, commit=True) #插入数据库
                data.append([d,url[2]])
        #记录当前获取的渝快办
        tocsv(f'{orgcode}body-{datetime.date.today()}.csv', data, 'w+')
        # 更新classification
        sql = f"UPDATE r_know_library SET classification=name WHERE zd_name='渝快办'"
        db.execute(sql, None, commit=True)
        #5、推送到es
        sql = "SELECT COUNT(1) AS num FROM r_know_library WHERE zd_name='渝快办'"
        result = db.execute(sql)
        #5.1、删除es渝快办数据
        num = result[0]['num']
        # if num>3000:
        index_name = "know_library"
        query = {
          "query":{
            "match": {
              "zdName.keyword":"渝快办"
            }
          }
        }
        try:
            response = es.delete_by_query(index=index_name, body=query)
            print("删除成功:", response)
        except Exception as e:
            print("删除失败:", str(e))
        #5.2查询mysql数据库，推送到es
        sql = f"SELECT * FROM r_know_library WHERE zd_name='渝快办'"
        rows = db.execute(sql)
        actions = [
            {
                "_index": index_name,
                "_source": transform_row(row)  # 调用转换函数
            }
            for row in rows
        ]
        # 6. 批量插入到 Elasticsearch
        try:
            helpers.bulk(es, actions)
            print(f"成功将 {len(actions)} 条数据插入到索引 {index_name}")
        except Exception as e:
            print("批量插入失败:", str(e))
        #7、更新mysql渝快办状态
        sql = f"UPDATE r_know_library SET zt=1 WHERE zd_name='渝快办'"
        db.execute(sql,None,commit=True)
