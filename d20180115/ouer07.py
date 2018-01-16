#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
E文件源文件（100000087010000_E2017121210332925_20171212000000_gbk.txt）
100000087010000|20171212|2017121210332925|15|2
100000087010000|HT20171212103329128|20171212094256|71208252424BBO117167|20171212|FB20171208252424BBO117167|5|HQB|7|03040000|6230209874563882|1|441402199202245603|201711221725306040|78110000|||||
100000087010000|HT20171212103329126|20171212092638|01712102535BBO117271|20171212|FB201712102535BBO117271|5|HQB|8|03040000|6230200840165260|1|450226198809198811|201710111209142934|78110000|||||

E文件目标文件（100000087010000_E2017121210332925_20171212000000_back.txt）
HT20180105163604316|2018010511051612|171124171831|32000.0|2|0|0
HT20180105163604316|20180104124322|80104124322BBO119191|20180105|5|HQB|19000|03040000|6230209832543178|201712111842501559|78110000|20171127104500|1|
HT20180105163604318|20180105154050|80204124322BBO119193|20180105|5|HQB|13000|03040000|6230209832543178|201712111842501559|78110000|20171127104500|4|

代码运行结果
HT20180105163604316|2018010516360415|171124171831|0.00|0.|0|0
HT20180105163604316|20180104124322|80104124322BBO119191|20180105|5|HQB|19000|03040000|6230209832543178|201712111842501559|78110000|20171127104500|1
HT20180105163604318|20180105154050|80204124322BBO119193|20180105|5|HQB|13000|03040000|6230209832543178|201712111842501559|78110000|20171127104500|1

c)  交易请求文件
文件头：基金销售机构号|发起日期|批次号|总额|总笔数
交易数据：基金机构号|交易流水号|发起日期时间|原合作商户交易流水号|原合作商户交易日期|原赎回交易流水号|支付模式|基金代码|交易金额|银行编码|卡号|证件类型|证件号|通联会员号|合作商户编码|联合商户编码|现金账户标识|||
d)  交易结果文件
文件头：基金销售机构号|发起日期|批次号|转换成功总金额|转换成功总笔数|转换失败总金额|转换失败总笔数
交易数据：基金销售机构交易流水号|交易发起日期时间|原合作商户交易流水号|支付模式|基金代码|交易金额|银行代码|银行卡号|通联交易流水号|合作商户编码|交易执行时间|交易执行状态
5）  文件内容格式说明
所有字段均不能为空。
a)  交易发起日期时间：YYYYMMDDHHMMSS
b)  原合作商户交易流水号：客户在合作商户，原货基购买理财交易的流水号
c)  原赎回交易流水号：赎回文件中需转换交易的流水号
d)  支付类型：默认填“5”
e)  基金代码：和赎回交易中的货基一致
f)  银行卡号：和赎回交易一致
g)  证件类型：和赎回交易一致
h)  证件号码：和赎回交易一致
i)  通联会员号：和赎回交易一致
j)  合作商户编码：通联分配的合作商户对应编码
k)  交易执行状态：1-成功、2-失败



"""
import re


def read_file_E(upload_file_E, is_log=True):
    """ 读文件， 返回title和lines  这个方法只用于处理D文件"""

    ouput_title = [] #用文本数组，最后用|合并
    ouput_lines = []

    with open('inpute.txt', 'r') as f: 

        title_segments = []
        jijinxiaoshoujigou = ''

        while True:
            line = f.readline()
            if not line:
                break
            if 'HT' in line:
                # 详细条目
                # 100000087010000|HT20180105163604318|20180105154050|80204124322BBO119193|20180105|FB20280204124322BBO119193|5|HQB|13000|03040000|6230209832543178|1|211401198512085584|201712111842501559|78110000|||||
                # 需要的几个字段是
                segs = line.strip().split('|')
                # 这是需要的几个字段，我不单独取名字了，直接append
                result_line_list = []
                result_line_list.append(segs[1])  # HT20180105163604318
                if not jijinxiaoshoujigou:  #初始值为''，把第一个机构号赋给它
                    jijinxiaoshoujigou = segs[1]
                result_line_list.append(segs[2])  # 20180105154050
                result_line_list.append(segs[3])  # 80204124322BBO119193
                result_line_list.append(segs[4])  # 20180105
                result_line_list.append(segs[6])  # 5
                result_line_list.append(segs[7])  # HQB
                result_line_list.append(segs[8])  # 13000
                result_line_list.append(segs[9])  # 03040000
                result_line_list.append(segs[10]) # 6230209832543178
                result_line_list.append(segs[13]) # 201712111842501559
                result_line_list.append(segs[14]) # 78110000
                result_line_list.append('20171127104500')  # 目标文件的这个字段，源文件没有 我这边就写了个固定的值 20171127104500
                result_line_list.append('1')  # 交易执行状态 1 2 4 9 应该是根据源文件的某些来判断吧，这个规则看你怎么实现

                result_line_str = '|'.join(result_line_list)
                ouput_lines.append(result_line_str)
            else:
                # 标题行
                title_segments = line.split('|')

        # 构造标题行 
        # 文件头：基金销售机构号|发起日期|批次号|转换成功总金额|转换成功总笔数|转换失败总金额|转换失败总笔数
        # HT20180105163604316|2018010511051612|171124171831|32000.0|2|0|0
        ouput_title.append(jijinxiaoshoujigou)
        # 发起日期我从文件标题里面取 100000087010000_E2018010516360415_20180105000000_back.txt
        # E后面那一串，正好长度适合
        datetime_from_filename_re = re.search('E\d+', '100000087010000_E2018010516360415_20180105000000_back.txt')
        if datetime_from_filename_re:
            ouput_title.append(datetime_from_filename_re.group(0)[1:])
        else:
            ouput_title.append("2018010511051612")
        ouput_title.append("171124171831")  # 批次号

        # 后面的4个字段，32000.0|2|0|0
        ouput_title.append('0.00')
        ouput_title.append('0.')
        ouput_title.append('0')
        ouput_title.append('0')

    return ['|'.join(ouput_title)] + ouput_lines


def read_remote_file_E(upload_file_E, is_log=True):
    """ 读文件， 返回title和lines  这个方法只用于处理D文件"""

    ouput_title = [] #用文本数组，最后用|合并
    ouput_lines = []
    return ['|'.join(ouput_title)] + ouput_lines

all_read_lines = read_file_E('inpute.txt')

with open('ouput24.txt', 'w') as f: 
    for line in all_read_lines:
        f.write(line)
        f.write('\n')