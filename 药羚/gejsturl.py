"""
作用：提取js中的url，http开头
用法：python index.py /js
需要输入一个参数，/js是js所在的路径
"""
import os, sys
import re


# 定义查找方法
def Find(string):
    #  查找匹配正则表达式的字符串
    url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url


# 读取js方法
def read_js(path):
    print("当前文件是:" + path)
    da = open(path, 'rb').read()
    # print(da)
    try:
        # print(Find(str(da, encoding="utf-8")))
        if len(Find(str(da, encoding="utf-8"))) > 0:
            print(path + ":", Find(str(da, encoding="utf-8")))
            return Find(str(da, encoding="utf-8"))
    except UnicodeDecodeError:
        # print(Find(str(da, encoding="gbk")))
        if len(Find(str(da, encoding="gbk"))) > 0:
            print(path + ":", Find(str(da, encoding="gbk")))
            return Find(str(da, encoding="gbk"))

    except:
        return "请尝试其他编码格式"


# 文件递归查询方法
def read_file(path):
    # print(os.listdir(path))
    allarr = []
    for i in os.listdir(path):
        fi_d = os.path.join(path, i)
        if os.path.isdir(fi_d):
            read_file(fi_d)
        else:
            if os.path.splitext(i)[1] == '.js':
                baby = read_js(os.path.join(fi_d))
                if not baby is None and len(baby) > 0:
                    allarr.append(baby)

    print(sum(allarr, []))
    exit()


if __name__ == '__main__':
    # 接收路径
    path = sys.argv[1]

    read_file(path)
