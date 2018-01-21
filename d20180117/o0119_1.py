#!user/bin/env Python
# -*- coding: utf-8 -*-
import re
import time
import linecache

#BusinessCode业务代码
CFM_SG = '122' #申购确认
CFM_RG = '120' #认购确认
CFM_SH = '124' #赎回确认
CFM_SZFHFS = '129' #设置分红方式确认
CFM_TZ = '144' #强行调增确认
CMF_TJ = '145' #强行调减确认
CMF_QS = '142'#强行赎回确认

# cfm_Order = 'C:/Users/likun/Desktop/autotest_file/OFD_02_379_20180104_04.TXT'
# the_file = open(cfm_Order)
# content = the_file.read()
# order_detail = linecache.getline(cfm_Order, 128)

order_detail = '201711280000000002937922|20171220|156|0000000000100000|0000000000100000|180004|0|20171128|141233|0000|0106A00000055|    379  |    0000000000000000|0000000000100000|122|181010000001|3790000000006       |1|10000|                   |    |20171220|0000000000|0000000000|0010000|379      |                        |        |0000000000|1|        |0000000000000000|00|000000000|0000000000000000|                    |                                                            |20171128|         |         |                 |    | | |0000000000000000|0000000000|0000000000000000|0000000000000000|0010000|        | |0000000000000000|0000000|0000000|0000000000000000|0000000000|0000000000000000|        |0000000000|0|0|0| | |        | |      |0000000000|     |     | |            |  |0106     |            | |                    |        |        |00|            |   | | |        | |                                        |00000| |0000000000000000|  |  |00000|      |0000000000000000|00000000|0010000|0000000000000000|0000000000000000|0000000000000000|0000000000000000| |3790000000006       |0000000000000000|0|0000000000000000|0000000000000000|0000000000000000|        |0000000000000000|0000000000000000|0000                                                        | |0000000000000000| |20171220'
"""
#方便数，每5个一行
order_detail     = '201711280000000002937922|20171220|156|0000000000100000|0000000000100000|
                    180004|0|20171128|141233|0000|
                    0106A00000055|    379  |    0000000000000000|0000000000100000|122|
                    181010000001|3790000000006       |1|10000|                   |
                        |20171220|0000000000|0000000000|0010000|379      |                        |        |0000000000|1|        |0000000000000000|00|000000000|0000000000000000|                    |                                                            |20171128|         |         |                 |    | | |0000000000000000|0000000000|0000000000000000|0000000000000000|0010000|        | |0000000000000000|0000000|0000000|0000000000000000|0000000000|0000000000000000|        |0000000000|0|0|0| | |        | |      |0000000000|     |     | |            |  |0106     |            | |                    |        |        |00|            |   | | |        | |                                        |00000| |0000000000000000|  |  |00000|      |0000000000000000|00000000|0010000|0000000000000000|0000000000000000|0000000000000000|0000000000000000| |3790000000006       |0000000000000000|0|0000000000000000|0000000000000000|0000000000000000|        |0000000000000000|0000000000000000|0000                                                        | |0000000000000000| |20171220'
"""

order_detail_items = order_detail.strip().split('|')

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
BusinessCode = '122'
TASerialNO = '3790000000006       ' #TA确认交易流水号:TA交易时用

# []里的下标，我是凭感觉改的，你自己核对
order_detail_items[0] = AppSheetSerialNo
order_detail_items[1] = TransactionCfmDate
#new_detail.append(list[2]) #CurrencyType结算币种
order_detail_items[3] = ConfirmedVol
order_detail_items[4] = ConfirmedAmount
order_detail_items[5] = FundCode
#new_detail.append(list[6]) #LargeRedemptionFlag巨额赎回标志
order_detail_items[7] = TransactionDate
order_detail_items[8] = TransactionTime
order_detail_items[9] = ReturnCode
order_detail_items[10] = TransactionAccountID
# new_detail.append(list[11]) #DistributorCode销售人代码,379
order_detail_items[12] = ApplicationVol
order_detail_items[13] = ApplicationAmount
order_detail_items[14] = CFM_SG


new_detail = '|'.join(order_detail_items)

print order_detail
print new_detail


'''
f = open(the_file_name.replace(".txt", "__marked.txt"), 'w')
f.write(content)
f.close()
'''  