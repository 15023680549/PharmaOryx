# -*- coding : utf-8-*-
# coding:utf-8

from multiprocessing import Pool, Manager
from guide.guideUrl import GuideUrl
from scripts.utilMysql import MysqlTool
# from guide.guideHtml import MyGetHtmlTool
import guide.utilFile as MyFileTool
from guide.GetHtml import MyGetHtmlTool

if __name__ == '__main__':
    #用于接收返回的url
    qdRows = []
    #
    guide = GuideUrl()
    qdRows = guide.ggfwUrl(500105) #获取渝快公共服务办链接
    # print(len(ggfwRows))
    qdRows = guide.xzqlUrl(500105) #获取渝快行政权力办链接
    # print(len(xzqlRows))
    # ggfwRows.extend(xzqlRows) #合并列表 将xzqlRows合并到ggfwRows,经过检查后发现不需要合并，同一个实例在GuideUrl()类里面已经追加了
    MyFileTool.tocsv('江北区url.csv',qdRows,'w+') #把url链接保存到csv文件,a 、a+追加,w 、w+覆盖
    # 使用 Manager 来管理进程间共享的列表
    with Manager() as manager:
        # 请求url中的连接
        qdRows = MyFileTool.readurl('江北区url.csv')
        htmlTool = MyGetHtmlTool(qdRows)
        rows = manager.list()
        htmlTool.main_get_html()  # 获取 HTML
        htmlTool.main_parse_html(rows)  # 解析 HTML
        MyFileTool.tocsv('江北区body.csv', rows,'w+')

        # htmlTool.whilePauseToText() #北碚渝快办数据导出到文本
    # #     #写入csv文件
    #     # with MysqlTool as db:
    #     #     sql = "INSERT INTO r_know_library(ID, sort,orgcode,short_name,name,class_type) VALUES (replace(UUID(),'-',''),%s,%s,%s,%s,%s)"
    #     #     db.execute("DELETE FROM r_know_library WHERE zd_name='渝快办'")
    #     #     for args in rows:
    #     #         db.execute(sql, args, commit=True)