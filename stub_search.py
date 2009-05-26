#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os,sys

def is_keyword(string):
    '''判断是否为不该在函数定义中出现的关键词'''
    keyword=['auto',    'struct',
            'break',    'else',
            'switch',   'case',
            'enum',     'register',
            'typedef',  'return',
            'union',    'const',
            'unsigned', 'continue',
            'for',      'signed',
            'default',  'goto',
            'sizeof',   'do',
            'if',       'while']
    m=re.findall(r'[a-zA-Z_]+', string)
    for x in m:
        if x in keyword:
            return True
        else:
            return False

def search_fun(text):
    '''返回:[函数名,函数起点,左括号起点,右括号终点]'''
    m=re.findall(r'[a-zA-Z0-9_* ()]+\s*\(.*\).*\s*\{',text)
    fun_list=[]
    for x in m:
        fun_temp=[]
        fun_name=re.match(r'[a-zA-Z0-9_* ()]+',x).group()
        fun_name_re=re.match(r'[a-zA-Z0-9_* ()]+\s*\(.*\)',x).group()
        if is_keyword(fun_name)==False:
            side=text.find(x)
            fun_temp.append(fun_name_re)
            fun_temp.append(side)
            fun_temp.append(side + len(x)-1)
            fun_list.append(fun_temp)
    for x in fun_list:
        lift=0
        right=0
        end=0
        for i in range(x[2],len(text)-1):
            if text[i]=='{':
                lift+=1
            elif text[i]=='}':
                right+=1
                end=i
            if lift!=0 and right!=0:
                if lift==right:
                    x.append(end)
                    break
    return tuple(fun_list)
    
def search_return(text):
    '''返回:[[起点,终点],return or exit]'''
    re=[]
    return_begin = 0
    return_end = 0
    while 1:
        temp = []
        return_begin = text.find('return' , return_end)
        return_end=text.find(';',return_begin+6)
        if return_begin == -1:
            break
        if ((text[return_begin-1] == '\n' or
        text[return_begin-1] == '	' or
        text[return_begin-1] == ' ' or
        text[return_begin-1] == '}' or
        text[return_begin-1] == ';' or
        text[return_begin-1] == ')') and
        (text[return_begin+6] == '    ' or
        text[return_begin+6] == '(' or
        text[return_begin+6] == ' ')):
            temp.append(return_begin-1)
            temp.append(return_end)
            temp.append('return')
            re.append(tuple(temp))
                
    exit_begin = 0
    exit_end = 0
    while 1:
        temp=[]
        exit_begin = text.find('exit' , exit_end)
        exit_end = text.find(';',exit_begin+4)
        if exit_begin == -1:
            break
        if ((text[exit_begin-1] == '\n' or
        text[exit_begin-1] ==  '	' or
        text[exit_begin-1] == ' ' or
        text[exit_begin-1] == '}' or
        text[exit_begin-1] == ';' or
        text[exit_begin-1] == ')') and
        (text[exit_begin+4] == '    ' or
        text[exit_begin+4] == '(' or
        text[exit_begin+4] == ' ')):
            temp.append(exit_begin-1)
            temp.append(exit_end)
            temp.append('exit')
            re.append(temp)
    return tuple(re)

def search_if(text):
    re=[]
    if_begin=0
    if_end=0
    while 1:
        temp = []
        if_begin = text.find('if' , if_end)
        if_end = text.find('(' , if_begin+2)
        if if_begin==-1:
            break
        if ((text[if_begin-1] == '\n' or
        text[if_begin-1] ==  '	' or
        text[if_begin-1] == ' ' or
        text[if_begin-1] == ';' or
        text[if_begin-1] == '}' or
        text[if_begin-1] == ')') and
        (text[if_begin+2] == '  ' or
        text[if_begin+2] == ' ' or
        text[if_begin+2] == '(')):
            if_begin = if_end
            lift = 0
            right = 0
            end = 0
            for i in range(if_begin , len(text)-1):
                if text[i] == '(':
                    lift += 1
                elif text[i] == ')':
                    right += 1
                    end = i
                if lift != 0 and right != 0:
                    if lift == right:
                        temp.append(if_begin-1)
                        temp.append(end)
                        temp.append('if')
                        re.append(temp)
                        break
    return tuple(re)

def search_for(text):
    re = []
    for_begin = 0
    for_end = 0
    while 1:
        temp=[]
        for_begin = text.find('for' , for_end)
        for_end = text.find('(' , for_begin+3)
        if for_begin == -1:
            break
        if ((text[for_begin-1] == '\n' or
        text[for_begin-1] == '	' or
        text[for_begin-1] == ' ' or
        text[for_begin-1] == ';' or
        text[for_begin-1] == '}' or
        text[for_begin-1] == ')') and
        (text[for_begin+3] ==  '	' or
        text[for_begin+3] == ' ' or
        text[for_begin+3] == '(')):
            #ifBegin=ifEnd
            lift = 0
            right = 0
            end = 0
            for i in range(for_begin , len(text)-1):
                if text[i] == '(':
                    lift += 1
                elif text[i] == ')':
                    right += 1
                    end = i
                if lift != 0 and right != 0:
                    if lift == right:
                        temp.append(for_begin-1)
                        temp.append(end)
                        temp.append('for')
                        re.append(temp)
                        break
    return tuple(re)

def search_while(text):
    re = []
    while_begin = 0
    while_end = 0
    while 1:
        temp = []
        while_begin = text.find('while' , while_end)
        while_end = text.find('(' , while_begin+5)
        if while_begin == -1:
            break
        if ((text[while_begin-1] == '\n' or
        text[while_begin-1] == '	' or
        text[while_begin-1] == ' ' or
        text[while_begin-1] == ';' or
        text[while_begin-1] == '}' or
        text[while_begin-1] == ')') and
        (text[while_begin+5] == '	' or
        text[while_begin+5] == ' ' or
        text[while_begin+5] == '(')):
            while_begin = while_end
            lift = 0
            right = 0
            end = 0
            for i in range(while_begin , len(text)-1):
                if text[i] == '(':
                    lift += 1
                elif text[i] == ')':
                    right += 1
                    end = i
                if lift != 0 and right != 0:
                    if lift == right:
                        temp.append(while_begin-1)
                        temp.append(end)
                        re.append(temp)
                        break
    for x in re:
        temp = text[x[1]+1:].lstrip()
        if temp.startswith(';'):
            x.append('do')
        else:
            x.append('while')
    return tuple(re)

def search_switch(text):
    re = []
    switch_begin = 0
    switch_end = 0
    while 1:
        temp = []
        switch_begin = text.find('switch' , switch_end)
        switch_end = text.find('{' , switch_begin+6)
        if switch_begin == -1:
            break
        if ((text[switch_begin-1] == '\n' or
        text[switch_begin-1] == '	' or
        text[switch_begin-1] == ' ' or
        text[switch_begin-1] == ';' or
        text[switch_begin-1] == '}' or
        text[switch_begin-1] == ';' or
        text[switch_begin-1] == ')') and
        (text[switch_begin+6] == '	' or
        text[switch_begin+6] == ' ' or
        text[switch_begin+6] == '(')):
            temp.append(switch_end)
            lift = 0
            right = 0
            isBegin = False
            end = 0
            for i in range(switch_end , len(text)-1):
                if text[i] == '{':
                    lift += 1
                elif text[i] == '}':
                    right += 1
                    end = i
                if lift != 0 and right != 0:
                    if lift == right:
                        temp.append(end)
                        re.append([text[temp[0]:temp[1]+1],temp[0],temp[1]])
                        break
    return tuple(re)

def search_case(switch_list):
    re = []
    for i in switch_list:
        case_begin = 0
        case_end = 0
        case_side = 0
        while 1:
            case_begin = i[0].find('case' , case_end)
            case_end = i[0].find(':' , case_begin+4)
            if case_begin == -1:
                break
            if ((i[0][case_begin-1] == '\n' or
            i[0][case_begin-1] ==  '	' or
            i[0][case_begin-1] == ' ' or
            i[0][case_begin-1] == '}' or
            i[0][case_begin-1] == ';' or
            i[0][case_begin-1] == ')') and
            (i[0][case_begin+4] == '	' or
            i[0][case_begin+4] == ' ' or
            i[0][case_begin+4] == '\n' or
            i[0][case_begin+4] == '{' or
            i[0][case_begin+4] == '(')):
                re.append([case_begin-1+i[1] , case_end+i[1] , 'case' , case_side])
                case_side += 1
        default_begin = i[0].find('default')
        default_end = i[0].find(':' , default_begin+7)
        if default_begin != -1:
            if ((i[0][default_begin-1] == '\n' or
                i[0][default_begin-1] == '	' or
                i[0][default_begin-1] == ' ' or
                i[0][default_begin-1] == '}' or
                i[0][default_begin-1] == ';' or
                i[0][default_begin-1] == ')') and
                (i[0][default_begin+7] ==  '	' or
                i[0][default_begin+7] == ' ' or
                i[0][default_begin+7] == '\n' or
                i[0][default_begin+7] == ':')):
                    re.append([default_begin-1+i[1] , default_end+i[1] , 'default' , case_side])
        if len(re) != 0:
            for j in range(0 , len(re)):
                if j != len(re)-1:
                    if i[0].find('break' , re[j][1] , re[j+1][0])!=-1:
                        re[j].append('y')
                    else:
                        re[j].append('n')
                if j == len(re)-1:
                    if i[0].find('break' , re[j][1])!=-1:
                        re[j].append('y')
                    else:
                        re[j].append('n')
    return tuple(re)