'''
Created on Feb 29, 2016

@author: ravith
'''

from net.bottronix.print_manager import PrintManager
import os
import socketserver
import threading
from net.bottronix.print_daemon import get_print_job_hander
from net.bottronix.print_exception import PrintException

class PrintServer(object):
    '''
    classdocs
    '''


    def __init__(self, port, webroot):
        self.port = port
        self.webroot = webroot
        
    
    def set_configuration(self,width,height,x_gap,y_gap, paper_width,labels_per_row,x_offset,y_offset):
        self.print_mgr = PrintManager()
        self.print_mgr.set_label_gaps(x_gap, y_gap)
        self.print_mgr.set_print_options(labels_per_row, paper_width,x_offset,y_offset)
        
    def run_server(self):
        self.httpd.serve_forever(poll_interval=0.5)
    
    def start_server(self):
        os.chdir(os.path.join(self.webroot, "htdocs"))
     
        print_job_handler_class = get_print_job_hander(self.print_mgr)
        self.httpd = socketserver.TCPServer(("", self.port), print_job_handler_class)
     
        print("Daemon started on port : ", self.port)
        
        try:
            threading.Thread(target=self.run_server,args=()).start()
        except KeyboardInterrupt:
            print("Stopping....")
            self.httpd.server_close()
        finally:
            self.print_mgr.close_printer()

        
    def stop_server(self):
        self.print_mgr.close_printer()
        self.httpd.server_close()
        self.httpd.shutdown()
        
        
    
    