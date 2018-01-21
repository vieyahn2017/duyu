#!/usr/bin/python
#encoding: utf-8

import re
import time

new_date = "20180109" # 你要改成的日期

#BusinessCode业务代码
CFM_SG = '122' #申购确认
CFM_RG = '120' #认购确认
CFM_SH = '124' #赎回确认
CFM_SZFHFS = '129' #设置分红方式确认
CFM_TZ = '144' #强行调增确认
CMF_TJ = '145' #强行调减确认
CMF_QS = '142'#强行赎回确认

AppSheetSerialNo = '541801030000000000237992' #申请订单号
TransactionCfmDate = '20180119' #确认日期
ConfirmedVol = '0000000000888000' #确认份额:16位，2位小数
ConfirmedAmount = '0000000000888000' #确认金额：16位，2位小数
FundCode = '021531' #产品编码，与ta对应
TransactionDate = '20180118' #交易发生日期
TransactionTime = time.strftime('%H%M%S') #交易发生时间：时分秒
ReturnCode = '0000' #交易处理返回结果码：0000代表成功
TransactionAccountID = '0106A00000108' #投资人交易基金账号
ApplicationVol = '    0000000000000000' #申请基金份数16位，前面空格不能省略，基金公司给的文件问题：赎回填此处，申购默认为0
ApplicationAmount = '0000000000888000' #申请金额：申购填此处，赎回默认为0
TASerialNO = '3790000000006       ' #TA确认交易流水号:TA交易时用
Charge = '0000000000' #手续费:10(两位小数)
AgencyFee = '0000000000' #代理费:10（两位小数）
NAV = '0010500' #基金单位净值:7（四位小数）
DefDividendMethod = ' ' #默认分红方式
TargetNAV = '0010800' #目标基金的单位净值:7（四位小数）


def _rewrite_order_detail_CFM_SH(order_detail):
    """赎回确认"""
    pass

def _rewrite_order_detail_CFM_RG(order_detail):
    """认购确认"""
    pass

def _rewrite_order_detail_CFM_SG(order_detail):
    """申购确认"""
    order_detail_items = order_detail.strip().split('|')
    order_detail_items[0] = AppSheetSerialNo
    order_detail_items[1] = TransactionCfmDate
    order_detail_items[3] = ConfirmedVol
    order_detail_items[4] = ConfirmedAmount
    order_detail_items[5] = FundCode
    order_detail_items[7] = TransactionDate
    order_detail_items[8] = TransactionTime
    order_detail_items[9] = ReturnCode
    order_detail_items[10] = TransactionAccountID
    order_detail_items[12] = ApplicationVol
    order_detail_items[13] = ApplicationAmount
    order_detail_items[14] = CFM_SG
    order_detail_items[22] = Charge
    order_detail_items[23] = AgencyFee
    order_detail_items[24] = NAV
    order_detail_items[43] = DefDividendMethod
    order_detail_items[52] = TargetNAV

    new_detail = '|'.join(order_detail_items)
    return new_detail


the_file_name = "201801080005.txt"
the_file = open(the_file_name)
content = the_file.read()

content_lines = content.strip().split('\n')
order_counts = len(content_lines) - 128
print "order counts is :", order_counts
# 如果总共是130行，第127行是条数汇总，第130行是结束，实际交易条数是2行


# TODO: 然后主程序中 到底是调用哪个处理方法，要通过某些条件 来判断
for i in range(order_counts):
    content_lines[127+i] = _rewrite_order_detail_CFM_SG(content_lines[127+i])


print content_lines

f = open(the_file_name.replace(".txt", "__marked.txt"), 'w')
f.write('\n'.join(content_lines))
f.close()
