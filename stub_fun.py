#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os,sys

class code_info:
    def __init__(self , code_file):
        self.file_path = os.path.abspath(code_file)
        handle = open(self.file_path, 'r')
        self.text = handle.read()
        handle.seek(0)
        self.text_lines = tuple(handle.readlines())
        handle.close()
        
        self.line_side = line_num(self.text_lines)
        self.p_and_c = search_pre_and_comment(self.text , self.line_side)
        self.empty_text = remove_pre_and_comment(self.text,self.p_and_c)
        

def fun_main(c_file):
    w = code_info(c_file)
    print w.empty_text

def line_num(text_lines):
    ''''每行的开始位置及结束位置'''
    re=[]
    text_num = 0
    for line in text_lines:
        temp=[text_num , text_num+len(line)-1]
        text_num += len(line)
        re.append(temp)
    return tuple(re)

def remove_pre_and_comment(text,p_and_c):
    '''去除预处理、注释、字符串'''
    no_p_and_c_text = ''
    ch_side_list = []
    for x in p_and_c:
        for i in range(x[0] , x[1]+1):
            ch_side_list.append(i)
    for i in range(0 , len(text)):
        if i in ch_side_list:
            no_p_and_c_text += ' '
        else:
            no_p_and_c_text += text[i]
    return no_p_and_c_text
    
def search_pre_and_comment(text,line):
    '''返回:预处理、注释、字符串位置 入口:由源文件读取的str、每行起始位置'''
    rtn_list=[]
    #----------pre----------
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
    #----------comment----------
    temp=[]

    comment_begin_1=False
    comment_begin_2=False
    string_begin=False

    comment_ready_1=False
    comment_ready_2=False

    comment_begin_side_1=-1
    comment_end_side_1=-1
    comment_begin_side_2=-1
    comment_end_side_2=-1
    string_begin_side=-1
    string_end_side=-1
    n=0
    while n<len(text)-1:
        if (text[n]=='/' and text[n+1]=='*' and comment_begin_1==False and comment_begin_2==False and string_begin==False):
            comment_begin_1=True
            comment_begin_side_1=n
            temp.append(n)
            n+=1
        elif ((text[n]=='/' and text[n+1]=='/') and comment_begin_1==False and comment_begin_2==False and string_begin==False):
            comment_begin_2=True;
            comment_begin_side_2=n;
            temp.append(n)
            n+=1
        elif (text[n]=='"' and comment_begin_1==False and comment_begin_2==False and string_begin==False):
            string_begin=True
            string_begin_side=n
            temp.append(n)
        #End
        elif (text[n]=='*' and text[n+1]=='/' and comment_begin_1==True and comment_begin_2==False and string_begin==False):
            comment_begin_1=False
            comment_ready_1=True
            n+=1
            comment_end_side_1=n
            temp.append(n)
            rtn_list.append(temp)
            temp=[]
        elif ((text[n]=='\n' or n==len(text)-2) and comment_begin_1==False and comment_begin_2==True and string_begin==False):
            comment_begin_2=False
            comment_ready_2=True
            if text[n]=='\n':
                n-=1
            comment_end_side_2=n;
            temp.append(n)
            rtn_list.append(temp)
            temp=[]
            n+=1
        elif (text[n]=='"' and comment_begin_1==False and comment_begin_2==False and string_begin==True):
            string_begin=False
            string_begin_side=n
            temp.append(n)
            rtn_list.append(temp)
            temp=[]
        n+=1
    rtn_list.sort()
    for x in rtn_list:
        x.append(text[x[0]:x[1]+1])
    return tuple(rtn_list)


def fun_block():
    pass
