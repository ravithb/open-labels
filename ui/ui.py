#!/usr/bin/env python3

'''
Created on Feb 28, 2016

@author: ravith
'''


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class OpenLabelsUi:


    def on_main_window_destroy(self, object, data=None):
        print("quit with cancel")
        Gtk.main_quit()

    def on_quit_activate(self, menuitem, data=None):
        print("quit from menu")
        Gtk.main_quit()
    
    def on_about_activate(self, menuitem, data=None):
        print("help about selected")
        #self.response = self.aboutdialog.run()
        #self.aboutdialog.hide()

    def on_click_server_start(self,object):
        validation = self.validate_inputs()
        if(validation ==0 ) :
            self.get_input_values()
        
    def on_warning_box_close(self,object):
        self.warning_msg.hide()
    
    def on_click_print_label(self,object):
        pass
    
    def on_click_browse(self,object):
        self.filechooser.show()
        
    def get_input_values(self):
        self.width = int(self.txt_width.get_text())
        self.height = int(self.txt_height.get_text())        
        self.paper_width = int(self.txt_paper_width.get_text())
        
        if(self.txt_x_gap.get_text()!=''):
            self.x_gap = int(self.txt_x_gap.get_text())
        else:
            self.x_gap = 0
            
        if(self.txt_y_gap.get_text()!=''):
            self.y_gap = int(self.txt_y_gap.get_text())
        else:
            self.y_gap = 0
            
        if(self.txt_x_offset.get_text()!=''):
            self.x_offset = int(self.txt_x_offset.get_text())
        else:
            self.x_offset = 0
            
        if(self.txt_y_offset.get_text()!=''):
            self.y_offset = int(self.txt_y_offset.get_text())
        else:
            self.y_offset = 0
        
    def validate_inputs(self):
        error_count = 0;
        if(self.txt_width.get_text()=='' or int(self.txt_width.get_text()) <= 0):
            self.warning_msg.set_markup("Invalid width.")
            error_count += 1
        if(self.txt_height.get_text()=='' or int(self.txt_height.get_text()) <=0):
            self.warning_msg.set_markup("Invalid height")
            error_count += 1
        if(self.txt_paper_width.get_text()=='' or int(self.txt_paper_width.get_text())<=0):
            self.warning_msg.set_markup("Invalid paper width")
            error_count += 1
        if(self.txt_x_gap.get_text()!='' and int(self.txt_x_gap.get_text())<0):
            self.warning_msg.set_markup("Invalid x gap")
            error_count += 1
        if(self.txt_y_gap.get_text()!='' and int(self.txt_y_gap.get_text())<0):
            self.warning_msg.set_markup("Invalid y gap")
            error_count += 1
        if(self.txt_x_offset.get_text()!='' and int(self.txt_x_offset.get_text())<0):
            self.warning_msg.set_markup("Invalid x offset")
            error_count += 1
        if(self.txt_y_offset.get_text()!='' and int(self.txt_y_offset.get_text())<0):
            self.warning_msg.set_markup("Invalid y offset")
            error_count += 1
        if(error_count>0):
            self.warning_msg.show()
            return 1;
        return 0

    def __init__(self):
        self.gladefile = "ui.glade" 
        self.builder = Gtk.Builder() 
        self.builder.add_from_file(self.gladefile)

        self.builder.connect_signals(self)

        self.window = self.builder.get_object("main_window")
        self.filechooser = self.builder.get_object("filechooser")
        self.warning_msg = self.builder.get_object("warning_box")
        self.statusbar = self.builder.get_object("staturbar")
        
        self.txt_width = self.builder.get_object("txt_width")
        self.txt_height = self.builder.get_object("txt_height")
        self.txt_x_gap = self.builder.get_object("txt_x_gap")
        self.txt_y_gap = self.builder.get_object("txt_y_gap")
        self.txt_paper_width = self.builder.get_object("txt_pap_width")
        self.txt_x_offset = self.builder.get_object("txt_x_offset")
        self.txt_y_offset = self.builder.get_object("txt_y_offset")
        
        self.window.show()


if __name__ == "__main__":
    main = OpenLabelsUi()
    Gtk.main() 


