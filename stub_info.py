#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import codecs
import stub_fun
import stub_search

class code_info:
    def __init__(self , code_file):
        self.file_path = code_file
        handle = open(self.file_path, 'r',)
        self.text = handle.read()
        handle.seek(0)
        self.text_lines = handle.readlines()
        handle.close()
    
    def stub_run(self):
        self.line_side = stub_fun.line_num(self.text_lines)
        self.p_and_c = stub_fun.search_pre_and_comment(self.text , self.line_side)
        self.empty_text = stub_fun.remove_pre_and_comment(self.text , self.p_and_c)
        
        self.fun_side = stub_search.search_fun(self.text)
        self.fun_block =  stub_fun.fun_block_list(self.text , self.empty_text , self.fun_side , self.line_side)
        self.ds_list,self.new_text = stub_fun.fun_stub(self.fun_block , self.file_path)
    
    def get_text(self):
        try:
            return self.text.decode('utf-8').encode('utf-8')
        except:
            return self.text.decode('gbk').encode('utf-8')
    
    def get_new_text(self):
        try:
            return self.new_text.decode('utf-8').encode('utf-8')
        except:
            return self.new_text.decode('gbk').encode('utf-8')
    
    def get_ds_text(self):
        return ('\n'.join(self.ds_list))
