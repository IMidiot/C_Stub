#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os,sys

def fun_main(file):
    '''读取文件内容'''
    file_path=os.path.abspath(file)
    handle = open(file_path, 'r')
    text = handle.read()
    handle.close()
    handle = open(file_path, 'r')
    text_lines = tuple(handle.readlines())
    handle.close()
    
    line = line_num(text_lines)
    print pre_and_commond(text,line)

def line_num(text_lines):
    ''''每行的开始位置及结束位置'''
    re=[]
    text_num=0
    for line in text_lines:
        temp=[text_num , text_num+len(line)-1]
        text_num+=len(line)
        re.append(temp)
    return tuple(re)
    
def pre_and_commond(text,line):
    '''返回:预处理位置(list) 入口:由源文件读取的str、每行起始位置'''
    rtn_list=[]
    pre_begin=False
    for myline in line:
        if pre_begin==False:
            if re.search(r'^\s*#.*\\$',text[myline[0]:myline[1]])==None:
                if re.search(r'^\s*#.*',text[myline[0]:myline[1]]):
                    rtn_list.append(myline)
            else:
                pre_begin=True
                rtn_list.append(myline)
        else:
            if re.search(r'.*\\$',text[myline[0]:myline[1]])==None:
                pre_begin=False
                rtn_list.append(myline)
            else:
                pre_begin=True
                rtn_list.append(myline)
    return tuple(rtn_list)

def fun_block():
    pass
