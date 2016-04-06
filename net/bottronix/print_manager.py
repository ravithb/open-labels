'''
Created on Feb 10, 2016

@author: ravith
'''
from net.bottronix.printer_util import PrinterUtil
from PIL import Image
from PIL import ImageFile
from net.bottronix.label_grid import LabelGrid
from net.bottronix.bit_img import BitImg
from net.bottronix.num_util import NumUtil
import constants
from constants import DOTS_PER_MM
from net.bottronix.print_exception import PrintException
from _io import StringIO

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
        
    def set_label_gaps(self,x_gap,y_gap):
        self.label_x_gap_mm=x_gap
        self.label_y_gap_mm=y_gap
    
    def set_label_size(self,width,height):
        self.label_width_mm=width
        self.label_height_mm=height
        
        
    def set_printer_port(self,port):
        self.printer_port = port  
        
    def init(self):
        printer_util = PrinterUtil()
        if(self.printer_port is None):
            port = printer_util.get_printer_port()
            if(port is None or port == ''):
                print("No printer found !")
                raise PrintException("No Printer Found")
            self.set_printer_port(port)    
        
    def set_label_count(self,lcount):
        self.label_count = lcount
        
    def set_label_img(self,l_img):
        if(isinstance(l_img, ImageFile.ImageFile)):
            self.label_img = l_img
    
    def set_label_file(self,l_file):
        self.label_file = l_file
        self.label_img = Image.open(self.label_file,"r")
        
    def get_config(self):
        outstr = StringIO()
        outstr.write("======================================\n")
        outstr.write("       Print Configuration  \n")
        outstr.write("======================================\n")
        if(hasattr(self, 'labels_per_row')):
            outstr.write(" Labels per row : ")
            outstr.write(str(self.labels_per_row))
            outstr.write("\n")
        if(hasattr(self, 'paper_width_mm')):
            outstr.write(" Paper width mm : ")
            outstr.write(str(self.paper_width_mm))
            outstr.write("\n")
        if(hasattr(self, 'label_x_offset_mm')):
            outstr.write(" x offset : ")
            outstr.write(str(self.label_x_offset_mm))
            outstr.write("\n")
        if(hasattr(self, 'label_y_offset_mm')):
            outstr.write(" y offset : ")
            outstr.write(str(self.label_y_offset_mm))
            outstr.write("\n")
        if(hasattr(self, 'label_width_mm') and hasattr(self, 'label_width_mm')):
            outstr.write(" Labels size mm : ")
            outstr.write(str(self.label_width_mm))
            outstr.write(" x ")
            outstr.write(str(self.label_height_mm))
            outstr.write("\n")
        if(hasattr(self, 'label_x_gap_mm')):
            outstr.write(" x gap mm : ")
            outstr.write(str(self.label_x_gap_mm))
            outstr.write("\n")
        if(hasattr(self, 'label_y_gap_mm')):
            outstr.write(" y gap mm : ")
            outstr.write(str(self.label_y_gap_mm))
            outstr.write("\n")
        outstr.write("======================================\n")
        return outstr.getvalue()       
        
    def print_labels(self):
        if(self.label_count<=0 or self.labels_per_row<=0):
            print("Label count and Labels per row fields are mandatory")
            raise PrintException("Label count and labels per row fields are not set")
        if(hasattr(self,'label_img') == False or self.label_img=='' or self.label_img == None):
            print("Label image is required.")
            raise PrintException("Label image is not set")
            
        self.labels_per_row = int(self.labels_per_row)
        self.label_count = int(self.label_count)
        
        print_count = (self.label_count//self.labels_per_row)
        print_count_remainder = self.label_count % self.labels_per_row
        
        label_grid = LabelGrid()
        if(print_count > 0):
            grid_img = label_grid.create_grid_img(self.label_img, self.labels_per_row, self.label_x_gap_mm)
        if(print_count_remainder > 0):
            grid_img_remainder = label_grid.create_grid_img(self.label_img, print_count_remainder, self.label_x_gap_mm)
#         print((print_count,print_count_remainder))
        
        self.open_printer()
                
        if(print_count > 0):
            self.send_init_commands()
            self.print_img(grid_img,print_count)
        if(print_count_remainder > 0):
            self.send_init_commands()
            self.print_img(grid_img_remainder,1)
        self.close_printer()

    def open_printer(self):
        try:            
            self.printer = open(self.printer_port,"wb")
            print("Printer opened.")
        except:
            if(self.printer_port!=None):
                print("Couldnt open printer at "+self.printer_port)
                raise PrintException("Couldn't open printer at "+self.printer_port)
            else:
                print("Printer not connected")
                raise PrintException("Printer not connected")
        
    def send_init_commands(self):
        if(self.printer is None):
            print("Printer port not open yet.")
            raise PrintException("Printer port not yet open")
        print("Sending init commands.")
        # Set Margin 
        self.printer.write(bytes("SM0,0\r\n",'ascii', 'ignore'))
        # Set printer type thermal transfer
        self.printer.write(bytes("STt\r\n",'ascii', 'ignore'))
        # Set speed 5
        self.printer.write(bytes("SS3\r\n",'ascii', 'ignore'))
        # Disable double buffering
        self.printer.write(bytes("SB0\r\n",'ascii', 'ignore'))
        # Set density 14
        self.printer.write(bytes("SD14\r\n",'ascii', 'ignore'))
        # Set gap offset 0 
        self.printer.write(bytes("SA0\r\n",'ascii', 'ignore'))
        # Set Tearoff Postion 0
        self.printer.write(bytes("TA0\r\n",'ascii', 'ignore'))
        # Set label options width, gap and gap detection
        self.printer.write(bytes("SL"+str(int(float(self.label_width_mm)*constants.DOTS_PER_MM))+ \
                                 ","+str(int(float(self.label_x_gap_mm)*constants.DOTS_PER_MM))+",G\r\n",'ascii', 'ignore'))
        # Set print from top to bottom
        self.printer.write(bytes("SOT\r\n",'ascii', 'ignore'))
        # Set Label Width dots
        self.printer.write(bytes("SW"+str(int(float(self.paper_width_mm)*constants.DOTS_PER_MM))+"\r\n",'ascii', 'ignore'))
        # Disable cutting
        self.printer.write(bytes("CUTn\r\n",'ascii', 'ignore'))
        # Clear image buffer
        self.printer.write(bytes("CB\r\n",'ascii', 'ignore'))
        
    def print_img(self,img,print_count):
        if(self.printer is None):
            print("Printer port not open yet.")
            raise PrintException("Printer port not open")
        if(int(print_count)<=0):
            print("Invalid print count "+str(print_count))
            raise PrintException("Invalid print count "+str(print_count))
        
        print("Printing image.")
        w,h= img.size
#         print((w,h))
        bi = BitImg()
        im_data = bi.get_bit_bytes(bytearray(img.getdata()))
        hx,lx = NumUtil.to_lh_int(self.label_x_offset_mm*DOTS_PER_MM)
        hy,ly = NumUtil.to_lh_int(self.label_y_offset_mm*DOTS_PER_MM)
        hw,lw = NumUtil.to_lh_int(PrintManager.img_byte_width(w))
        hlines,llines = NumUtil.to_lh_int(h)
 
        cmd = bytearray([0x4C,0x44,lx,hx,ly,hy,lw,hw,llines,hlines])
        cmd.extend(im_data)
#         print(''.join(format(x, '02x') for x in cmd)) 
        self.printer.write(cmd)        
        self.printer.write(bytes("P"+str(int(print_count))+"\r\n",'ascii', 'ignore'))
        
    def close_printer(self):
        if(hasattr(self, 'printer') == False):
            print("Printer port not open yet.")
            return
        self.printer.close()
        print("Printer closed")
        
    @staticmethod
    def img_byte_width(width):
        return width/8 + (1 if(width%8 != 0) else 0)
    
    
