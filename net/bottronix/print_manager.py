'''
Created on Feb 10, 2016

@author: ravith
'''
from net.bottronix.printerutil import PrinterUtil
import sys
import os.path
from net.bottronix.label_grid import LabelGrid
from net.bottronix.bit_img import BitImg
from net.bottronix.num_util import NumUtil
import constants
from constants import DOTS_PER_MM

class PrintManager():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.printer_port = None
        
    def set_print_options(self,lper_row,p_width,lx_offset,ly_offset):
        self.labels_per_row = int(lper_row)
        self.paper_width_mm = int(p_width)
        self.label_x_offset_mm = int(lx_offset)
        self.label_y_offset_mm = int(ly_offset)
    
    def set_label_size(self,width,height,x_gap,y_gap):
        self.label_width_mm=width
        self.label_height_mm=height
        self.label_x_gap_mm=x_gap
        self.label_y_gap_mm=y_gap
        
    def set_printer_port(self,port):
        self.printer_port = port  
        
    def init(self):
        printer_util = PrinterUtil()
        if(self.printer_port is None):
            port = printer_util.get_printer_port()
            if(port is None or port == ''):
                print("No printer found !")
                sys.exit()
            self.set_printer_port(port)    
        
    def set_label_count(self,lcount):
        self.label_count = lcount
    
    def set_label_file(self,l_file):
        self.label_file = l_file        
        
    def print_labels(self):
        if(self.label_count<=0 or self.labels_per_row<=0):
            print("Label count and Labels per row fields are mandatory")
            sys.exit()
        if(self.label_file=='' or os.path.isfile(self.label_file) == False):
            print("Label image file is required.")
            sys.exit()
            
        self.labels_per_row = int(self.labels_per_row)
        self.label_count = int(self.label_count)
        
        print_count = (self.label_count//self.labels_per_row)
        print_count_remainder = self.label_count % self.labels_per_row
        
        label_grid = LabelGrid()
        if(print_count > 0):
            grid_img = label_grid.create_grid_img(self.label_file, self.labels_per_row, self.label_x_gap_mm)
        if(print_count_remainder > 0):
            grid_img_remainder = label_grid.create_grid_img(self.label_file, print_count_remainder, self.label_x_gap_mm)
        print((print_count,print_count_remainder))
        
        self.open_printer()
                
        if(print_count > 0):
            self.send_init_commands()
            self.print_img(grid_img,print_count)
        if(print_count_remainder > 0):
            self.send_init_commands()
            self.print_img(grid_img_remainder,print_count_remainder)
        self.close_printer()

    def open_printer(self):
        try:
            self.printer = open(self.printer_port,"wb")
            print("Printer opened.")
        except:
            print("Couldnt open printer at "+self.printer_port)
            sys.exit()
        
    def send_init_commands(self):
        if(self.printer is None):
            print("Printer port not open yet.")
            sys.exit()
        print("Sending init commands.")
        # Set Margin 
        self.printer.write("SM0,0\r\n")
        # Set printer type thermal transfer
        self.printer.write("STt\r\n")
        # Set speed 5
        self.printer.write("SS3\r\n")
        # Disable double buffering
        self.printer.write("SB0\r\n")
        # Set density 14
        self.printer.write("SD14\r\n")
        # Set gap offset 0 
        self.printer.write("SA0\r\n")
        # Set Tearoff Postion 0
        self.printer.write("TA0\r\n")
        # Set label options width, gap and gap detection
        self.printer.write("SL"+str(int(float(self.label_width_mm)*constants.DOTS_PER_MM))+","+str(int(float(self.label_x_gap_mm)*constants.DOTS_PER_MM))+",G\r\n")
        # Set print from top to bottom
        self.printer.write("SOT\r\n")
        # Set Label Width dots
        self.printer.write("SW"+str(int(float(self.paper_width_mm)*constants.DOTS_PER_MM))+"\r\n")
        # Disable cutting
        self.printer.write("CUTn\r\n")
        # Clear image buffer
        self.printer.write("CB\r\n")
        
    def print_img(self,img,print_count):
        if(self.printer is None):
            print("Printer port not open yet.")
            sys.exit()
        if(int(print_count)<=0):
            print("Invalid print count "+str(print_count))
            sys.exit()
        
        print("Printing image.")
        w,h= img.size
#         img.save('/tmp/grid3.bmp')
        print((w,h))
        bi = BitImg()
        im_data = bi.get_bit_bytes(bytearray(img.getdata()))
        hx,lx = NumUtil.to_lh_int(self.label_x_offset_mm*DOTS_PER_MM)
        hy,ly = NumUtil.to_lh_int(self.label_y_offset_mm*DOTS_PER_MM)
        hw,lw = NumUtil.to_lh_int(PrintManager.img_byte_width(w))
        hlines,llines = NumUtil.to_lh_int(h)
 
        cmd = bytearray([0x4C,0x44,lx,hx,ly,hy,lw,hw,llines,hlines])
        cmd.extend(im_data)
        print(''.join(format(x, '02x') for x in cmd)) 
        self.printer.write(cmd)        
        self.printer.write("P"+str(int(print_count))+"\r\n")
        
    def close_printer(self):
        if(self.printer is None):
            print("Printer port not open yet.")
            sys.exit()
        self.printer.close()
        print("Printer closed")
        
    @staticmethod
    def img_byte_width(width):
        return width/8 + (1 if(width%8 != 0) else 0)
    
    