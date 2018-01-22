#!user/bin/env Python
# -*- coding: utf-8 -*-

import re
import time

# work_date，在文件中多处使用
TransactionCfmDate = '20180100' #确认日期

#BusinessCode业务代码
CFM_SG = '122' #申购确认
CFM_RG = '120' #认购确认
CFM_SH = '124' #赎回确认
CFM_SZFHFS = '129' #设置分红方式确认
CFM_TZ = '144' #强行调增确认
CMF_TJ = '145' #强行调减确认
CMF_QS = '142'#强行赎回确认


with open('E:/testfile/OFD_02_379_20180104_04.TXT') as f:
    lines = f.readlines()
    lines[4] = TransactionCfmDate + '\n'#修改交易确认日期

#AppSheetSerialNo申请订单号不能重复，多次生成时使用循环
i = 0
for i in range(10):
    print '循环第几次:', i
    i = i + 1
    counts_10_bits = str(i).zfill(10)
    print counts_10_bits
    AppSheetSerialNo = TransactionCfmDate + counts_10_bits + '237992'  #申请订单号:交易确认日+10位不重复的值+237992
    print AppSheetSerialNo
    #其他参数
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

    order_detail = '201711280000000002937922|20171220|156|0000000000100000|0000000000100000|180004|0|20171128|141233|0000|0106A00000055|    379  |    0000000000000000|0000000000100000|122|181010000001|3790000000006       |1|10000|                   |    |20171220|0000000000|0000000000|0010000|379      |                        |        |0000000000|1|        |0000000000000000|00|000000000|0000000000000000|                    |                                                            |20171128|         |         |                 |    | | |0000000000000000|0000000000|0000000000000000|0000000000000000|0010000|        | |0000000000000000|0000000|0000000|0000000000000000|0000000000|0000000000000000|        |0000000000|0|0|0| | |        | |      |0000000000|     |     | |            |  |0106     |            | |                    |        |        |00|            |   | | |        | |                                        |00000| |0000000000000000|  |  |00000|      |0000000000000000|00000000|0010000|0000000000000000|0000000000000000|0000000000000000|0000000000000000| |3790000000006       |0000000000000000|0|0000000000000000|0000000000000000|0000000000000000|        |0000000000000000|0000000000000000|0000                                                        | |0000000000000000| |20171220'

    # def _rewrite_order_detail_SG(order_detail):
    """按行处理"""
    print order_detail
    order_detail_items = order_detail.strip().split('|')
    # []里的下标，代表每个字段，参考文件《中登2.0开放式基金业务数据交换协议0902》7.66.4　交易确认（04文件）
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

    new_detail = ''.join(order_detail_items)
    print new_detail
    #从[127]之后，循环写入交易数据
    lines[127:127] = [new_detail + '\n']
    open('E:/testfile/OFD_02_379_20180104_04.txt', 'w').writelines(lines)
    #[126]行，统计出所有交易数据的条数
    total_count = str(len(lines) - 127).zfill(8)
    print total_count
    lines[126] = total_count + '\n'
    print lines[126]
