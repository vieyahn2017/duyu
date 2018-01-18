#!/usr/bin/python
#encoding: utf-8

import re

the_file_name = "201801080001.txt"
the_file = open(the_file_name)
content = the_file.read()


# try:
#     search_date_lines = re.search(r"379\n\d+\n999", content).group()
#     ### 正则搜索379\n20180108\n999 这三行
# except AttributeEror:
#     pass


new_date = "20180109" # 你要改成的日期


# 正则替换379\n20180108\n999 这三行 直接替换，不用先搜索
content = re.sub(r"379\s+\d+\s+999",  "379\n" + new_date + "\n999", content)
# 搜索最后交易记录的那几行
detail_order_lines_se = re.search(r"SHAREREGISTERDATE\n[\s\S]*\nOFDCFEND", content)

if detail_order_lines_se is not None:
    detail_order_lines = detail_order_lines_se.group().split('\n')
    order_counts = len(detail_order_lines) - 3 
    #去掉首行SHAREREGISTERDATE  第二行（记录条数） 尾行OFDCFEND
    order_counts_8_bits = str(order_counts).zfill(8) 
    content = re.sub(r"SHAREREGISTERDATE\n\d+\n", "SHAREREGISTERDATE\n%s\n" % order_counts_8_bits, content)

print content

f = open(the_file_name.replace(".txt", "__marked.txt"), 'w')
f.write(content)
f.close()

