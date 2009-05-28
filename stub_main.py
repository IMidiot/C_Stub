#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

import stub_info

#reload(sys)
#sys.setdefaultencoding('utf8')

class gui_window:
    def open_button_clicked(self,widget):
        file_dialog = gtk.FileChooserDialog('Open',
                                None,
                                gtk.FILE_CHOOSER_ACTION_OPEN,
                                (gtk.STOCK_CANCEL,
                                gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN,
                                gtk.RESPONSE_OK))
        filter = gtk.FileFilter()
        filter.set_name('All Files')
        filter.add_pattern('*.c')
        filter.add_pattern('*.h')
        file_dialog.add_filter(filter)
        file_re = file_dialog.run()
        if file_re == gtk.RESPONSE_OK:
            file_path = file_dialog.get_filename()
            file_dialog.destroy()
            text_buf = gtk.TextBuffer()
            stub = stub_info.code_info(file_path)
            text_buf.set_text(stub.text)
            self.wTree.get_widget('textview').set_buffer(text_buf)
        file_dialog.destroy()
    
    def __init__(self):
        self.wTree = gtk.glade.XML('stub_gui.glade') 
        self.window = self.wTree.get_widget('window')
        self.window.connect("destroy", gtk.main_quit)
        dic = { "on_open_button_clicked" : self.open_button_clicked}
        self.wTree.signal_autoconnect(dic)
        self.window.show()
    
    def main(self):
        gtk.main()

if __name__ == "__main__":
    w = gui_window()
    w.main()
#w = stub_info.code_info('/home/yangguang/Code/test_c1.c')