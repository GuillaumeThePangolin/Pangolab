# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 14:04:41 2021

@author: Experiment4K
"""


class Euro2404(object):
    def __init__(self,inst):
        self.inst = inst
        self.inst.serial.timeout = 2
        self.inst.serial.baudrate = 9600
    
    
    def data_info(self,devicenumber):#returns the data keys of the device
        self.devicenumber = devicenumber
        self.data_keys = [str(devicenumber) + '_Euro2404_T']
        return(self.data_keys)

    def read_info(self,devicenumber):
        self.read_keys = [str(devicenumber) + '_Euro2404_T']
        return(self.read_keys)
    
    def write_info(self,devicenumber):
        self.write_keys = []
        return(self.write_keys)
    
    def write_pattern(self,devicenumber,write_key):
        return([])
    
    
    
    def floatHandling(self,text):
        try:
            f = str(float(text))
        except:
            try:
                f = str(float(text.replace(',','.')))
            except:
                f = False
        return(f)
    
    def Write(self,Key,L):
        None
    
    def Read(self,Key):
        T = self.inst.read_register(1)
        return([(Key,T),])
                    