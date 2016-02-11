'''
Created on Feb 11, 2016

@author: ravith
'''
import re
import io
import base64
from PIL import Image
import os
import json
import http.server
from net.bottronix.print_manager import PrintManager
from http.server import SimpleHTTPRequestHandler
from net.bottronix.print_exception import PrintException


def get_print_job_hander(prnt_manager):
    
    class PrintJobHandler(http.server.SimpleHTTPRequestHandler):
        '''
        classdocs
        '''
        
        def __init__(self, *args, **kwargs):
            self.print_manager = prnt_manager
            super().__init__(*args, **kwargs)
    
    #     def do_HEAD(self):
    #         self.send_response(200)
    #         self.send_header("Content-type", "text/html")
    #         self.end_headers()
    #         
        def do_POST(self):
    
            print("got post!!")
            content_len = int(self.headers['Content-Length'])
            
            body = self.rfile.read(content_len).decode('UTF-8')
    
            data = json.loads(body)
            image_data = base64.b64decode(re.sub('^data:image/.+;base64,', '', data['labelData']))
            lbl_image = Image.open(io.BytesIO(image_data))
            
            result = ""
            http_result_code = 200
            try:
                self.print_manager.set_label_img(lbl_image)
                self.print_manager.set_label_size(int(data['labelWidth']),int(data['labelHeight']))
                self.print_manager.set_label_count(int(data['labelCount']))
                
                self.print_manager.init()
                self.print_manager.print_labels()
                
                result = "{status:'"+str(http_result_code)+"',msg='success'}"
            except PrintException as e:
                http_result_code = 500
                print("Error occured : "+ e.value)
                result = "{status:'"+str(http_result_code)+"',msg='"+e.value+"'}"
            finally:
                self.print_manager.close_printer()
                
            response = bytes(result,'UTF-8')
            self.send_response(http_result_code)
            self.send_header("Content-type", "application/json")
            self.send_header("Content-length", len(response))
            self.end_headers()
            self.wfile.write(response)
             
    #     def do_GET(self):     
    # 
    #         try:
    #             uiFile = open(os.path.join(os.path.dirname(os.path.realpath('__file__')), "../../resources/ui-file.html"),"r")
    #             if(uiFile):
    #                 data=uiFile.read()
    #                 self.respond(data)
    #         except:
    #             self.respond("File not found",404)
    #         
    #     def respond(self, response, status=200):
    #         self.send_response(status)
    #         self.send_header("Content-type", "text/html")
    #         self.send_header("Content-length", len(response))
    #         self.end_headers()
    #         self.wfile.write(response)
            
    return PrintJobHandler
        
        
# if __name__ == '__main__':    
#             
#     print_mgr = PrintManager()
#     print_mgr.set_label_gaps(args.horizontal_gap_mm, args.vertical_gap_mm)
#     print_mgr.set_print_options(args.labels_per_row, args.paper_width_mm,args.label_x_offset_mm,args.label_y_offset_mm)
#     print_mgr.set_label_count(data['labelCount'])
#     
#     
#     os.chdir(os.path.join(os.path.dirname(os.path.realpath('__file__')), "../../htdocs"))
#     
#     print_job_handler_class = get_print_job_hander(print_mgr)
#     httpd = socketserver.TCPServer(("", 31173), print_job_handler_class)
# 
#     print("daemon started on port : ", 31173, ", docroot : ", os.getcwd())
#     try:
#         httpd.serve_forever()
#     except KeyboardInterrupt:
#         pass
#         print("Stopping....")
#         httpd.server_close()
#     
# #     server_class = BaseHTTPServer.HTTPServer
# #     httpd = server_class(("localhost", 31173),PrintDaemon)
# #     print("****** Open Labels Daemon ******")
# #     print("Starting....")
#     
