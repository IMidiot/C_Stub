#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os,sys
import stub_search

def line_num(text_lines):
    ''''每行的开始位置及结束位置'''
    re=[]
    text_num = 0
    for line in text_lines:
        temp=[text_num , text_num+len(line)-1]
        text_num += len(line)
        re.append(temp)
    return tuple(re)
    
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

def fun_block_list(text , empty_text , fun_side , line_side):
    new_fun_block=[]
    old_fun_block=[]
    for x in fun_side:
        new_fun_block.append([empty_text[x[2]:x[3]+1],x[0]])
        old_fun_block.append([text[x[2]:x[3]+1],x[0]])
    free_block=[]
    free_block.append(text[0:(fun_side[0])[2]] )
    for i in range(1,len(fun_side)):
        free_block.append(text[fun_side[i-1][3]+1:fun_side[i][2]])
    free_block.append(text[fun_side[len(fun_side)-1][3]+1:])
    for i in range(0,len(fun_side)):
        for j in range(0,len(line_side)):
            if (fun_side[i][1] in range(line_side[j][0],line_side[j][1]+1)):
                new_fun_block[i].append(j)
            else:
                pass
            if (fun_side[i][3] in range(line_side[j][0],line_side[j][1]+1)):
                new_fun_block[i].append(j)
            else:
                pass
    return (tuple(new_fun_block) , (old_fun_block) , (free_block))

def fun_stub(fun_block , file_path):
    ds_list=[]
    num_fun = 0x10000000
    num_return = 0x20000000
    num_branch = 0x30000000
    
    for fun_id , fun in enumerate(fun_block[0]):
        tmp = ''
        num_fun+=1
        stub_list=[]
        stub_list.append([0,'ctTag(0x%X);{' % num_fun])
        tmp += '%X;%s;%s;%d;%d;start;' % (num_fun,fun[1] , file_path,fun[2] , fun[3])
        #-----return and exit-----
        num_return += 1
        stub_list.append([len(fun[0])-2,'ctTag(0x%X);}' % num_return])
        return_list = stub_search.search_return(fun[0])
        for i in return_list:
            num_return+=1
            stub_list.append([i[0],'{ctTag(0x%X);' % num_return])
            tmp+=';%X' % num_return
            stub_list.append([i[1],'}'])
        ds_list.append(tmp)
        print ds_list
    print stub_list
