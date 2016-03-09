'''
Created on Mar 1, 2016

@author: ravith
'''
import os
import json
from os.path import expanduser
from collections import OrderedDict

class Preset(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.home_dir = expanduser("~")
        self.config_dir_path = os.path.abspath(os.path.join(str(self.home_dir),".open-labels"))
        self.presets_file_path = os.path.abspath(os.path.join(str(self.config_dir_path),"presets.json"))
        self.preset_data = {}
        
        if(os.path.exists(self.config_dir_path)==False):
            os.makedirs(self.config_dir_path)
        
    
    def write_default_preset(self):
        presets = {"30x20 label":{"name":"30x20 label","width":30,"height":20}, \
                    "40x20 label":{"name":"40x20 label","width":40,"height":20}}
        self.save_preset(presets)
        self.preset_data = presets
        
    def get_preset(self,name):
        return self.preset_data.get(name);
        
    def save_preset(self, ps):
        self.preset_data.update(ps)
        with open(self.presets_file_path, 'w') as tfile:
            json.dump(self.preset_data, tfile)

    
    def read_presets(self):
        if(os.path.exists(self.presets_file_path) and os.path.isfile(self.presets_file_path)):
            with open(self.presets_file_path,'r') as data_file:    
                file_content = data_file.read()
                self.preset_data = json.loads(file_content)
        else:
            self.write_default_preset()
            
        self.preset_data = OrderedDict(sorted(self.preset_data.items(), key=lambda t: t[0]))


    def delete_preset(self,name):
        self.preset_data.pop(name)            
        self.save_preset(self.preset_data)