#!/usr/bin/env python3

'''
Created on Feb 28, 2016

@author: ravith
'''


import gi
import os
import sys
import time
from net.bottronix.print_server import PrintServer
from net.bottronix.ui.preset import Preset
from DistUpgrade import sourceslist
from net.bottronix.print_manager import PrintManager
from net.bottronix.print_exception import PrintException
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class OpenLabelsUi:

    def resource_path(self):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(os.path.realpath(__file__))
    
        print(base_path)
        return base_path

    def on_main_window_destroy(self, object, data=None):
        print("quit with cancel")
        Gtk.main_quit()

    def on_quit_activate(self, menuitem, data=None):
        print("quit from menu")
        self.stop_server()
        Gtk.main_quit()
    
    def on_about_activate(self, menuitem, data=None):
        self.about_dialog.show()  
        
    def on_about_dlg_close(self,object):
        self.about_dialog.hide() 

    def on_click_server_start_stop(self,object):
        if(self.server_running):            
            self.stop_server()
        else:
            validation = self.validate_inputs()
            if(validation ==0 ) :
                port = 31173
                self.get_input_values()
                self.statusbar.push(self.statusbar_context_id,"Starting server...")
                self.start_server(port)
            
            else:
                self.statusbar.push(self.statusbar_context_id,"Invalid configuraiton")
                
    def start_server(self,port):
        self.print_server = PrintServer(port,\
                    os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),"../../"))))
        self.print_server.set_configuration(self.width, self.height, self.x_gap, \
            self.y_gap, self.paper_width, self.labels_per_row, self.x_offset, self.y_offset)
        try:
            self.print_server.start_server()
        except OSError as e:
            self.statusbar.push(self.statusbar_context_id,"Server start failed. "+e.strerror)
            self.server_running = False
            return
        self.statusbar.push(self.statusbar_context_id,"Server started on port "+str(port))
        self.server_running = True
        self.btn_start_server.set_label("Stop Server")

    def stop_server(self):
        if(self.print_server != None):
            self.print_server.stop_server()
            self.server_running = False
            self.btn_start_server.set_label("Start Server")
            self.statusbar.push(self.statusbar_context_id, "Server stopped.")

    def on_warning_dialog_close(self,object, object2):
        self.warning_dialog.hide()
    
    def on_click_print_label(self,object):        
        if(self.bmp_filepath == '' or os.path.exists(self.bmp_filepath)==False):
            self.warning_dialog.set_markup("Please select a label image")
            self.warning_dialog.show()
            self.statusbar.push(self.statusbar_context_id,"Label image not found")
            return
        validation = self.validate_inputs()
        if(validation ==0 ):
            self.print_count_dialog.show()            
        else:
            self.warning_dialog.set_markup("Invalid configuration.")
            self.warning_dialog.show()
            self.statusbar.push(self.statusbar_context_id,"Invalid configuraiton")
        
    
    def on_click_browse(self,object):
        self.filechooser_dialog.show()
        
    def on_save_name_dialog_close(self,object):
        self.save_name_dialog.hide()
    
    def on_save_dialog_cancel_btn_clicked(self,object):
        self.save_name_dialog.hide()

    def on_save_dialog_ok_button_clicked(self,object):
        if(self.txt_save_name.get_text()==""):
            self.warning_dialog.set_markup("Please enter a name")
            self.warning_dialog.show()
            return
        self.save_name_dialog.hide()
        ui_data = self.get_preset_from_ui(self.txt_save_name.get_text())
        self.save_preset(ui_data)
    
    def on_btn_save_preset_clicked(self, source):
        (model, iter) = self.preset_listbox.get_selection().get_selected()
        selected_row = model.get_value(iter, 0)
        if(selected_row!=''):
            self.txt_save_name.set_text(selected_row)
        else:
            self.txt_save_name.set_text("")
        self.save_name_dialog.show()
        
    def on_btn_del_preset_clicked(self,source):
        (model, iter) = self.preset_listbox.get_selection().get_selected()
        selected_row = model.get_value(iter, 0)
        if(selected_row!=''):
            self.delete_preset_dialog.set_markup("Are you sure you need to delete "+selected_row+" ?")
            self.delete_preset_dialog.target_row_id=selected_row
            self.delete_preset_dialog.show()
        
    def btn_del_preset_dlg_cancel_clicked(self,source):
        self.delete_preset_dialog.hide();
    
    def btn_del_preset_dlg_del_clicked(self,source):
        self.delete_preset(self.delete_preset_dialog.target_row_id)
        self.delete_preset_dialog.hide();
    
    def on_preset_select(self,source,index,col_object):
        (model, iter) = source.get_selection().get_selected()
        selected_row = model.get_value(iter, 0)
        data = self.preset.get_preset(selected_row) 
        self.set_preset_to_ui(data)
        
    def on_btn_filechooser_dlg_cancel_clicked(self,source):
        self.filechooser_dialog.hide()
        
    def on_btn_filechooser_dlg_select_clicked(self,source):
        self.bmp_filepath = self.filechooser_dialog.get_filename()
        self.preview_img.set_from_file(self.bmp_filepath)
        self.filechooser_dialog.hide()
        
    def on_btn_prnt_count_dlg_cancel_clicked(self,source):
        self.print_count_dialog.hide()
        
    def on_btn_prnt_count_dlg_print_clicked(self,source):
        if(self.bmp_filepath == '' or os.path.exists(self.bmp_filepath)==False):
            self.statusbar.push(self.statusbar_context_id,"Label not found")
            return
        
        if(self.txt_print_count.get_text()==''):
            self.statusbar.push(self.statusbar_context_id,"Invalid number of labels to print")
            return
        
        validation = self.validate_inputs()
        if(validation ==0 ):
            self.get_input_values()            
            self.print_mgr = PrintManager()
            self.print_mgr.set_label_count(int(self.txt_print_count.get_text()))
            self.print_mgr.set_label_size(self.width,self.height)
            self.print_mgr.set_label_gaps(self.x_gap, self.y_gap)
            self.print_mgr.set_print_options(self.labels_per_row, self.paper_width,self.x_offset,self.y_offset)
            self.print_mgr.set_label_file(self.bmp_filepath)
            try:
                self.print_mgr.print_labels()
            except PrintException as e:
                self.statusbar.push(self.statusbar_context_id,"Print failed : "+e.value)
                self.warning_dialog.set_markup("Print failed. "+e.value)
                self.warning_dialog.show()
        else:
            self.statusbar.push(self.statusbar_context_id,"Invalid configuraiton")
        
        self.print_count_dialog.hide() 
        
    def set_preset_to_ui(self,data):
        if('width' in data):
            self.txt_width.set_text(str(data['width']))
        if('height' in data):
            self.txt_height.set_text(str(data['height']))
        if('x_gap' in data):
            self.txt_x_gap.set_text(str(data['x_gap']))
        if('y_gap' in data):
            self.txt_y_gap.set_text(str(data['y_gap']))
        if('paper_width' in data):
            self.txt_paper_width.set_text(str(data['paper_width']))
        if('labels_per_row' in data):
            self.txt_labels_per_row.set_text(str(data['labels_per_row']))
        if('x_offset' in data):
            self.txt_y_offset.set_text(str(data['x_offset']))
        if('y_offset' in data):
            self.txt_x_offset.set_text(str(data['y_offset']))
        
    def get_preset_from_ui(self,name):
        data = {name: {"width":self.txt_width.get_text(),\
                       "height":self.txt_height.get_text(),\
                       "x_gap":self.txt_x_gap.get_text(),\
                       "y_gap":self.txt_y_gap.get_text(),\
                       "paper_width":self.txt_paper_width.get_text(),\
                       "labels_per_row":self.txt_labels_per_row.get_text(),\
                       "y_offset":self.txt_y_offset.get_text(),\
                       "x_offset":self.txt_x_offset.get_text()}}
        return data
        

    def get_input_values(self):
        self.width = int(self.txt_width.get_text())
        self.height = int(self.txt_height.get_text())        
        self.paper_width = int(self.txt_paper_width.get_text())
        self.labels_per_row = int(self.txt_labels_per_row.get_text())
        
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
            self.warning_dialog.set_markup("Invalid width.")
            error_count += 1
        if(self.txt_height.get_text()=='' or int(self.txt_height.get_text()) <=0):
            self.warning_dialog.set_markup("Invalid height")
            error_count += 1
        if(self.txt_paper_width.get_text()=='' or int(self.txt_paper_width.get_text())<=0):
            self.warning_dialog.set_markup("Invalid paper width")
            error_count += 1
        if(self.txt_labels_per_row.get_text()=='' or int(self.txt_labels_per_row.get_text())<=1):
            self.warning_dialog.set_markup("Labels per row must be greater than or equal to 1")
            error_count += 1
        if(self.txt_x_gap.get_text()!='' and int(self.txt_x_gap.get_text())<0):
            self.warning_dialog.set_markup("Invalid x gap")
            error_count += 1
        if(self.txt_y_gap.get_text()!='' and int(self.txt_y_gap.get_text())<0):
            self.warning_dialog.set_markup("Invalid y gap")
            error_count += 1
        if(self.txt_x_offset.get_text()!='' and int(self.txt_x_offset.get_text())<0):
            self.warning_dialog.set_markup("Invalid x offset")
            error_count += 1
        if(self.txt_y_offset.get_text()!='' and int(self.txt_y_offset.get_text())<0):
            self.warning_dialog.set_markup("Invalid y offset")
            error_count += 1
        if(error_count>0):
            self.warning_dialog.show()
            return 1;
        return 0
    
    def save_preset(self,ps):
        self.preset.save_preset(ps)
        self.update_preset_list()
        
    def delete_preset(self,ps):
        self.preset.delete_preset(ps)
        self.update_preset_list()
        
    def update_preset_list(self):
        self.preset_liststore.clear()
        if(self.preset.preset_data != None):
            for name,pdata in self.preset.preset_data.items():
                plist = list([name, \
                             int(pdata["width"]), \
                             int(pdata["height"])])
                self.preset_liststore.append(plist)     
        
        self.preset_listbox.set_model(self.preset_liststore)
        
    def __init__(self):
        self.print_server = None
        self.bmp_filepath = ''
        self.gladefile = os.path.abspath(os.path.join(self.resource_path(), "ui.glade" ))
        self.builder = Gtk.Builder() 
        self.builder.add_from_file(self.gladefile)

        self.builder.connect_signals(self)

        self.window = self.builder.get_object("main_window")
        self.filechooser_dialog = self.builder.get_object("filechooser_dialog")
        self.warning_dialog = self.builder.get_object("warning_dialog")
        self.save_name_dialog = self.builder.get_object("save_name_dialog")
        self.delete_preset_dialog = self.builder.get_object("delete_preset_dialog")
        self.print_count_dialog = self.builder.get_object("print_count_dialog")
        self.about_dialog = self.builder.get_object("about_dialog")
        self.statusbar = self.builder.get_object("statusbar")
        self.btn_start_server = self.builder.get_object("btn_server")
        self.preset_listbox = self.builder.get_object("preset_listbox")
        self.btn_save_preset = self.builder.get_object("btn_save_preset")
        self.btn_del_preset = self.builder.get_object("btn_del_preset")
        self.preset_liststore = self.builder.get_object("preset_liststore")  
        self.preview_img = self.builder.get_object("preview_img")   
        
        self.txt_width = self.builder.get_object("txt_width")
        self.txt_height = self.builder.get_object("txt_height")
        self.txt_x_gap = self.builder.get_object("txt_x_gap")
        self.txt_y_gap = self.builder.get_object("txt_y_gap")
        self.txt_paper_width = self.builder.get_object("txt_pap_width")
        self.txt_labels_per_row = self.builder.get_object("txt_labels_per_row")
        self.txt_x_offset = self.builder.get_object("txt_x_offset")
        self.txt_y_offset = self.builder.get_object("txt_y_offset")   
        
        self.filechooser_dialog.set_transient_for(self.window)
        self.warning_dialog.set_transient_for(self.window)
        self.save_name_dialog.set_transient_for(self.window)
        self.delete_preset_dialog.set_transient_for(self.window)
        self.print_count_dialog.set_transient_for(self.window)
        self.about_dialog.set_transient_for(self.window)
        self.txt_width = self.builder.get_object("txt_width")
        self.txt_height = self.builder.get_object("txt_height")
        self.txt_x_gap = self.builder.get_object("txt_x_gap")
        self.txt_y_gap = self.builder.get_object("txt_y_gap")
        self.txt_paper_width = self.builder.get_object("txt_pap_width")
        self.txt_x_offset = self.builder.get_object("txt_x_offset")
        self.txt_y_offset = self.builder.get_object("txt_y_offset")
        self.txt_labels_per_row = self.builder.get_object("txt_labels_per_row")
        self.txt_print_count = self.builder.get_object("txt_print_count")
        
        self.txt_save_name = self.builder.get_object("txt_save_name")
        
        self.statusbar_context_id = self.statusbar.get_context_id("statusbar")
        
        file_filter = Gtk.FileFilter()
        file_filter.set_name("BMP Files")
        file_filter.add_pattern("*.bmp")
        file_filter.add_pattern("*.BMP")
        self.filechooser_dialog.add_filter(file_filter)
        
        self.preset = Preset()
        
        self.preset.read_presets()
        
        self.update_preset_list()
        
        columns = ["Name","Width","Height"]
        for i in range(len(columns)):
            cell = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(columns[i], cell, text=i)
            self.preset_listbox.append_column(col)

        
        
        self.window.show()

        self.server_running = False
        
    @staticmethod
    def run_ui():
        main = OpenLabelsUi()
        Gtk.main()
    
if __name__ == "__main__":
        OpenLabelsUi.run_ui()


