#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
--upLoadfileD 输入文件  我本地测试名字input.txt
--upLoadfileD = sftp_client.open("/opt/file/fund-gw/share-dir/export/settle/fundout/generate/20180108/100000087010000_D2018010817532924_20180107000000_gbk.txt")#文件路径
100000087010000|20171226|2017122611453810|8031.76|6
TX41|20171226093224|FB20171220213224BBO118514|BANK|50|03040000|6230209874563882|1|441402199202245603|201711221725306040
TX41|20171225162900|FB20171225162900BBO119003|BANK|1970.44|03040000|6230209874563882|1|441402199202245603|201711221725306040
TX41|20171225164412|FB20171225164412BBO119004|BANK|1970.44|03040000|6230209874563882|1|441402199202245603|201711221725306040
TX41|20171226103846|FB20171225173836BBO119017|BANK|100|03040000|6230209874563882|1|441402199202245603|201711221725306040
TX41|20171225185646|FB20171225185646BBO119023|BANK|1970.44|03040000|6230209874563882|1|441402199202245603|201711221725306040
TX41|20171225190536|FB20171225190536BBO119024|BANK|1970.44|03040000|6230209874563882|1|441402199202245603|201711221725306040

-- downLoadfileD 输出文件  我本地测试名字ouput.txt
--downLoadfileD = sftp_client.open("/opt/file/fund-gw/share-dir/export/settle/fundout/generate/20180108/100000087010000_D2018010817532924_20180107000000_back.txt")
基金销售机构号，发起日期，批次号，成功总金额
100000087010000|20171226000000|100000087010000_D2017122611453810_20171226000000|0.00|0|0.00|0|0.00|0
TX41|FB20171220213224BBO118514|50.00|03040000|6230209874563882|201711221725306040|null|9
TX41|FB20171225162900BBO119003|1970.44|03040000|6230209874563882|201711221725306040|null|9
TX41|FB20171225164412BBO119004|1970.44|03040000|6230209874563882|201711221725306040|null|9
TX41|FB20171225173836BBO119017|100.00|03040000|6230209874563882|201711221725306040|null|9
TX41|FB20171225185646BBO119023|1970.44|03040000|6230209874563882|201711221725306040|null|9
TX41|FB20171225190536BBO119024|1970.44|03040000|6230209874563882|201711221725306040|null|9
交易类型，基金销售机构交易流水号，交易金额，银行代码，银行卡号，银行交易流水号，交易执行时间，交易执行状态
"""
import re

ouput_title = [] #用文本数组，最后用|合并
ouput_lines = []

with open('input.txt', 'r') as f: 

    title_segments = []

    while True:
        line = f.readline()
        if not line:
            break
        if line.startswith('TX'):
            # 详细条目
            # TX41|20171226093224|FB20171220213224BBO118514|BANK|50|03040000|6230209874563882|1|441402199202245603|201711221725306040
            # 交易类型，基金销售机构交易流水号，通联交易流水号
            # 需要的几个字段是
            segs = line.strip().split('|')
            # 这是需要的几个字段
            seg0_tx41, seg2_fb, seg4_money, seg5_bank, seg6_bankcard, seg9 = segs[0], segs[2], segs[4], segs[5], segs[6], segs[9]
            # 构造目标文件的行
            result_line_list = []
            result_line_list.append(seg0_tx41) 
            result_line_list.append(seg2_fb) 
            result_line_list.append(seg4_money) 
            result_line_list.append(seg5_bank) 
            result_line_list.append(seg6_bankcard) 
            result_line_list.append(seg9) 
            result_line_list.append('null') # 交易执行时间 设为null
            result_line_list.append('9') # 交易执行状态 1 2 4 9 应该是根据源文件的某些来判断吧，这个规则看你怎么实现

            result_line_str = '|'.join(result_line_list)
            ouput_lines.append(result_line_str)
        else:
            # 标题行
            title_segments = line.split('|')

    # 构造标题行 
    # 100000087010000|20171226000000|100000087010000_D2017122611453810_20171226000000|0.00|0|0.00|0|0.00|0
    ouput_title.append(title_segments[0]) # 基金销售机构
    ouput_title.append(title_segments[1] + '000000')  # 20171226000000
    ouput_title.append('{0}_D{1}_{2}000000'.format(title_segments[0], title_segments[2], title_segments[1])) 

    # 后面的6个字段，你怎么处理 0.00|0|0.00|0|0.00|0
    ouput_title.append('0.00')
    ouput_title.append('0.')
    ouput_title.append('0.00')
    ouput_title.append('0.')
    ouput_title.append('0.00')
    ouput_title.append('0')


with open('ouput.txt', 'w') as f: 
    f.write('|'.join(ouput_title))
    f.write('\n')
    for line in ouput_lines:
        f.write(line)
        f.write('\n')