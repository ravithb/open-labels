#!/usr/bin/python3

"""
Created on Feb 7, 2016.

@author: ravith.

"""
from net.bottronix.print_manager import PrintManager
import sys

if __name__ == '__main__':

    if(len(sys.argv)<8):
        print("Usage is : python main.py <label-file> <width-mm> <height-mm> <horizontal-gap-mm> <vertical-gap-mm> <labels-per-row> <paper-width-mm> <lable-count> [<printer-port>]")
        print("\n")
        print("1) label-file         : Path to the label file. Must be a black and white 8-bit per pixel BMP file")
        print("2) width-mm           : Width of the label in mm")
        print("3) height-mm          : Height of the label in mm")
        print("4) horizontal-gap-mm  : Horizontal gap between two adjacent labels in mm")
        print("5) vertical-gap-mm    : Vertical gap between two adjacent labels in mm")
        print("6) labels-per-row     : Number of labels per row on the paper.")
        print("7) paper-width-mm     : Width of the label paper in mm")
        print("8) label-x-offset-mm  : Horizontal offset in mm")
        print("9) layel-y-offset-mm  : Vertical offset in mm")
        print("10) label-count       : Number of lables to print")
        print("11) printer-port      : [Optional] printer device path [eg: /dev/usb/lp0]")
        sys.exit()
        
    print_mgr = PrintManager()
    print_mgr.set_label_file(sys.argv[1])
    print_mgr.set_label_size(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    print_mgr.set_print_options(sys.argv[6], sys.argv[7],sys.argv[9],sys.argv[10])
    print_mgr.set_label_count(sys.argv[8])
    
    if(len(sys.argv)==12):
        print_mgr.set_printer_port(sys.argv[11])

    print_mgr.init()
    print_mgr.print_labels()