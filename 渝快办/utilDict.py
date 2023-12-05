#-*- coding : utf-8-*-
# coding:utf-8

sfdict = {
    '0': '否',
    '1': '是'
}

# 办理形式
blxsdict = {
    '1': '窗口办理',
    '2': '网上办理',
    '3': '快递申请'
}

serviceObjectName = {
    '1': '自然人',
    '2': '企业法人',
    '3': '事业法人',
    '4': '社会组织法人',
    '5': '非法人企业',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '其他组织'
}

# 层级
cjdictName = {
    '4': '县级'
}
# 事项类型字典
sxdictName = {
    '20': '公共服务',
    '10': '其他行政权力',
    '09': '行政裁决',
    '08': '行政奖励',
    '07': '行政确认',
    '06': '行政检查',
    '05': '行政给付',
    '04': '行政征收',
    '03': '行政强制',
    '02': '行政处罚',
    '01': '行政许可'
}

@staticmethod
def getSxlxName(sxlx):
    return utilDict.sxdictName[sxlx]

@staticmethod
def getCjName(cj):
    return utilDict.cjdictName[cj]

@staticmethod
def getServiceObjectName(object):
    return utilDict.serviceObjectName[object]

@staticmethod
def getBlxsName(blxs):
    return utilDict.blxsdict[blxs]


@classmethod
def getSxlxName(sxlx):
    return utilDict.sxdictName[sxlx]


