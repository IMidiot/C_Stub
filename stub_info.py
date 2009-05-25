#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys

import stub_fun
import stub_search

class code_info:
    def __init__(self , code_file):
        self.file_path = os.path.abspath(code_file)
        handle = open(self.file_path, 'r')
        self.text = handle.read()
        handle.seek(0)
        self.text_lines = tuple(handle.readlines())
        handle.close()
        
        self.line_side = stub_fun.line_num(self.text_lines)
        self.p_and_c = stub_fun.search_pre_and_comment(self.text , self.line_side)
        self.empty_text = stub_fun.remove_pre_and_comment(self.text , self.p_and_c)
        
        self.fun_side = stub_search.search_fun(self.text)
        self.fun_block =  stub_fun.fun_block_list(self.text , self.empty_text , self.fun_side , self.line_side)
        stub_fun.fun_stub(self.fun_block , self.file_path)
