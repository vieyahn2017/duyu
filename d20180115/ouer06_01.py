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

def read_remote_file_O(upLoadfileD, is_log=True):
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



#################################################################
##    把功能全部写成def方法，放到之前。  这下面是具体调用      ##
#################################################################



sftp_client = get_remote_sftp_client(hostname=config.file_interfaceHost, 
                                     port=config.file_interfacePort, 
                                     username=config.file_userName, 
                                     password=config.file_pwd)

remote_path = "/opt/file/fund-gw/share-dir/export/settle/fundout/generate/"

the_day = '20180108' # 每次手动改这里吧


def _choose_file_func(one_file_with_path, file_tpye, func):
    """按照给定的文件类型，选择相应的处理方法；会询问一次，可以输入其他处理类型
    （也就是说，先默认按文件里的OED自动识别一个文件类型，但是也许不一定对，会询问一次"""
    print "the file type is maybe: ", file_tpye
    print "handle it with this type (press any key to continue), or choose the other type: {'D': D, 'O': O, 'E': E}"
    choose = raw_input()
    # 按 DE文件的不同，选择不同的执行方法
    if choose == 'D':
        print "you choose the D type."
        file_tpye = 'D'
        func = read_remote_file_D
    elif choose == 'E':
        print "you choose the E type."
        file_tpye = 'E'
        func = read_remote_file_O
    elif choose == 'O':
        print "you choose the O type."
        file_tpye = 'O'
        func = read_remote_file_O
    else:
        print "handle it with this type of parameter: %s " % file_tpye

    ouput_title, ouput_lines = '', []
    print one_file_with_path, "is in process..."
    try:
        ouput_title, ouput_lines = func(one_file_with_path)
    except Exception as e:
        print e
        # 处理文件可能出错，这边把错误 原样打出来。
    finally:
        return ouput_title, ouput_lines


def main(sftp_client, remote_path_add_the_day):
    """ the main function """

    # sftp_client.chdir(remote_path_add_the_day)
    # the_day_remote_dirs = sftp_client.listdir()
    the_day_remote_dirs = sftp_client.listdir(remote_path_add_the_day)

    dirs_dicts = {}
    # 列出该目录下所有gbk文件，并生成一个以序号为主键的dict
    for no, one_file in enumerate(the_day_remote_dirs):
        if one_file.endswith('gbk.txt'):
            print no, one_file
            dirs_dicts[str(no)] = one_file

    print "please choose your file: "
    file_no = raw_input()
    one_file = dirs_dicts[file_no]
    upload_file = sftp_client.open(remote_path_add_the_day + '/' + one_file, 'r')

    ouput_title, ouput_lines = '', []
    # 按 ODE文件的不同，选择不同的执行方法
    if 'O' in one_file:
        ouput_title, ouput_lines = _choose_file_func(upload_file, 'O', read_remote_file_O)
    elif 'D' in one_file:
        ouput_title, ouput_lines = _choose_file_func(upload_file, 'D', read_remote_file_D)
    elif 'E' in one_file:  # E文件的处理方法还没写，可以先把这两行注释了
        ouput_title, ouput_lines = _choose_file_func(upload_file, 'E', read_remote_file_E)
    else:
        print "can not recognize your file"
    
    download_file = sftp_client.open(remote_path_add_the_day + '/' + one_file.replace('gbk', 'back'), 'w')
    write_remote_file(download_file, ouput_title, ouput_lines)



main(sftp_client, remote_path + the_day)