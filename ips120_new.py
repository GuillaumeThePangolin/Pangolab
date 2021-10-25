# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 10:58:53 2021

@author: Experiment4K
"""

from time import sleep,time
import variables

class Ips120(object):
    def __init__(self,inst):
        self.inst = inst
        self.inst.read_termination = '\r'
    
    
    def data_info(self,devicenumber):#returns the data keys of the device
        self.devicenumber = devicenumber
        self.data_keys = [str(devicenumber) + '_IPS120_Current']
        return(self.data_keys)

    def read_info(self,devicenumber):
        self.read_keys = [str(devicenumber) + '_IPS120_Current']
        return(self.read_keys)
    
    def write_info(self,devicenumber):
        self.write_keys = [str(devicenumber) + '_IPS120_Current',str(devicenumber) + '_IPS120_Parameters']
        return(self.write_keys)
    
    def write_pattern(self,devicenumber,write_key):
        if write_key == self.write_keys[0]:
            return([('Current (A)','text',None)])
        elif write_key == self.write_keys[1]:
            return([('Current SweepRate (A/min)','text',None),('Output','choice',['None','Hold','To Set Point','To Zero'])])
    
    
    
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
        if Key == self.write_keys[0]:
            I = self.floatHandling(L[0])
            self.inst.write('$I' + I)
        elif Key == self.write_keys[1]:
            Irate = self.floatHandling(L[0])
            if type(Irate) == str:
                self.inst.write('$S' + Irate)
            if L[1] != 'None':
                if L[1] == 'Hold':
                    self.inst.write('$A0')
                elif L[1] == 'To Set Point':
                    self.inst.write('$A1')
                elif L[1] == 'To Zero':
                    self.inst.write('$A2')
    
    def Read(self,Key):
        I = float(self.inst.query('R0')[1:])
        return([(Key,I),])
                    

