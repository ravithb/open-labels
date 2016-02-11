#!/usr/bin/python3

"""
Created on Feb 7, 2016.

@author: ravith.

"""
from net.bottronix.print_manager import PrintManager
import os
import socketserver
from net.bottronix.print_daemon import get_print_job_hander
from argparse import ArgumentParser
from net.bottronix.print_exception import PrintException


if __name__ == '__main__':
    
    parser = ArgumentParser()
    parser.add_argument("label_file",help="Path to the label file. Must be  black and white 8-bit/pixel BMP file.")
    parser.add_argument("width_mm",help="Width of the label in mm",type=float)
    parser.add_argument("height_mm",help="Height of the label in mm",type=float)
    parser.add_argument("horizontal_gap_mm",help="Horizontal gap between two adjacent labels in mm",type=float)
    parser.add_argument("vertical_gap_mm",help="Vertical gap between two adjacent labels in mm",type=float)
    parser.add_argument("labels_per_row",help="Number of labels per row on the paper.",type=int)
    parser.add_argument("paper_width_mm",help="Width of the label paper in mm",type=float)
    parser.add_argument("label_x_offset_mm",help="Horizontal offset in mm",type=float)
    parser.add_argument("label_y_offset_mm",help="Vertical offset in mm",type=float)
    parser.add_argument("label_count",help="Number of lables to print",type=int)
    parser.add_argument("-p","--printer_port",help="Printer device path [eg: /dev/usb/lp0]")
    parser.add_argument("-d","--run_as_daemon",help="Printer device path [eg: /dev/usb/lp0]")
    parser.add_argument("-l","--listen",help="Daemon listen port. Default 31173",type=int)
    
    args = parser.parse_args()
        
    print_mgr = PrintManager()
    print_mgr.set_label_gaps(args.horizontal_gap_mm, args.vertical_gap_mm)
    print_mgr.set_print_options(args.labels_per_row, args.paper_width_mm,args.label_x_offset_mm,args.label_y_offset_mm)
    print_mgr.set_label_count(args.label_count)
    
    if(args.printer_port):
        print_mgr.set_printer_port(args.printer_port)
        
    print(print_mgr.get_config())

    if(args.run_as_daemon):
#         daemon = PrintDaemon()        
        print("****** Open Labels Daemon ******")        
        print("Starting....")
        
        os.chdir(os.path.join(os.path.dirname(os.path.realpath('__file__')), "htdocs"))
     
        print_job_handler_class = get_print_job_hander(print_mgr)
        httpd = socketserver.TCPServer(("", 31173), print_job_handler_class)
     
        print("Daemon started on port : ", 31173)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
            print("Stopping....")
            httpd.server_close()
        finally:
            print_mgr.close_printer()

    else:
        print_mgr.set_label_file(args.label_file)
        print_mgr.set_label_size(args.width_mm, args.height_mm)
        try:
            print_mgr.init()
            print_mgr.print_labels()
        except PrintException as e:
            print("Error occured : "+e.value)
        finally:
            print_mgr.close_printer()