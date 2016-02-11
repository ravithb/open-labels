"""
Created on Feb 7, 2016.

@author: ravith.

"""
import pyudev
"""

"""

class PrinterUtil:
    """

    """
    
    def __init__(self):
        pass
        
    def get_printer_port(self):
        context = pyudev.Context()
        for device in context.list_devices(ID_BUS='usb', ID_VENDOR_ID='1504'):
            vendor_id = device.get('ID_VENDOR_ID', '')
            device_id = device.get('ID_MODEL_ID', '')
            driver = device.get('ID_USB_DRIVER', '')
            dev_node = ''

            if (vendor_id == '1504' and device_id == '0008'
                and driver == 'usblp'):
                    dev_node = device.get('DEVNAME', '')
                    if (dev_node != ''):
                        break
        if(dev_node != ''):
            print('Found dev_node '+dev_node)
            return dev_node
        else:
            return None
