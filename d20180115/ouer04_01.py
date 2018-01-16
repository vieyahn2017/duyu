#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from config import config
import paramiko
import re
import os
import sys


def get_remote_sftp_client(hostname, port, username, password)
    #服务器信息，主机名（IP地址）、端口号、用户名及密码
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, password, compress=True)
    sftp_client = client.open_sftp()
    return sftp_client


def read_remote_file_D(upLoadfileD, is_log=True):
    """ 远程读文件， 返回title和lines  这个方法只用于处理D文件"""

    ouput_title = [] #用文本数组，最后用|合并
    ouput_lines = []
    title_segments = []
    # 这三个存目标值的，要放在for循环之前

    for line in upLoadfileD:
        if line.startswith('TX'):
            # 详细条目
            # TX41|20171226093224|FB20171220213224BBO118514|BANK|50|03040000|6230209874563882|1|441402199202245603|201711221725306040
            # 交易类型，基金销售机构交易流水号，通联交易流水号
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
    # 其中{0} {1} {2}的三个参数占位符号，用后面format方法的三个参数生成一个字符串
    # 最后生成100000087010000_D2017122611453810_20171226000000

    # 后面的6个字段，你怎么处理 0.00|0|0.00|0|0.00|0
    ouput_title.append('0.00')
    ouput_title.append('0.')
    ouput_title.append('0.00')
    ouput_title.append('0.')
    ouput_title.append('0.00')
    ouput_title.append('0')

    if is_log:
        print ouput_title
        print ouput_lines

    return ouput_title, ouput_lines


def read_remote_file_E(upLoadfileD, is_log=True):
    """ 远程读文件， 返回title和lines  这个方法只用于处理E文件"""
    pass
    # todo


def write_remote_file(filename, title, lines):
    # 这个方法DE都是用这个，O未知，估计也可以用，看你那边的情况
    filename.write('|'.join(title))
    filename.write('\n')
    for line in lines:
        filename.write(line)
        filename.write('\n')



#########
# 把功能全部写成def方法，放到之前。  这下面是具体调用
#########



sftp_client = get_remote_sftp_client(hostname=config.file_interfaceHost, 
                                     port=config.file_interfacePort, 
                                     username=config.file_userName, 
                                     password=config.file_pwd)

remote_path = "/opt/file/fund-gw/share-dir/export/settle/fundout/generate/"

the_day = '20180108' # 每次手动改这里吧

today_remote_dirs = sftp_client.listdir(remote_path + the_day)

for one_file in today_remote_dirs:
    
    if one_file.endswith('gbk.txt'):
        print "========begin========="
        print one_file, "is in process..."
        upload_file = sftp_client.open(remote_path + the_day + '/' + one_file, 'r')

        ouput_title, ouput_lines = '', []
        # 按 DE文件的不同，选择不同的执行方法
        if 'D' in one_file:
            ouput_title, ouput_lines = read_remote_file_D(upload_file)
        elif 'E' in one_file:  # E文件的处理方法还没写，可以先把这两行注释了
            ouput_title, ouput_lines = read_remote_file_E(upload_file)
        else:
            # O文件怎么弄，这边待完成
            pass
        download_file = sftp_client.open(remote_path + the_day + '/' + one_file.replace('gbk', 'back'), 'w')
        write_remote_file(download_file, ouput_title, ouput_lines)
        print "========end========="
    else:
        print one_file, "skipped"
