# -*- coding: utf-8 -*-
class Cryomag4G(object):
    def __init__(self,inst):
        self.inst = inst
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\n'
    
    
    def data_info(self,devicenumber):#returns the data keys of the device
        self.data_keys = [str(devicenumber) + '_CRYO4G_Current']
        return(self.data_keys)

    def read_info(self,devicenumber):
        self.read_keys = [str(devicenumber) + '_CRYO4G_Current']
        return(self.read_keys)
    
    def write_info(self,devicenumber):
        self.write_keys = [str(devicenumber) + '_CRYO4G_Current']
        return(self.write_keys)
    
    def write_pattern(self,devicenumber,write_key):
        if write_key == self.write_keys[0]:
            return([('Setpoint (A)','text',None)])


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
            C = self.floatHandling(L[0])
            if type(C) == str:
                Cfloat = float(C)
                if Cfloat > 97.58 :
                    Cfloat = 97.58
                    C = str(97.58)
                elif Cfloat < -97.58 :
                    Cfloat = -97.58
                    C = str(-97.58)
                INOW=float(self.inst.query('IMAG?').replace('\n','').replace('A',''))
                if Cfloat > INOW:
                    self.inst.write('ULIM ' + str(Cfloat))
                    self.inst.write('SWEEP UP')
                elif Cfloat < INOW: 
                    self.inst.write('LLIM ' +str(Cfloat))
                    self.inst.write('SWEEP DOWN')     
        return()
    
    def Read(self,Key):
        if Key == self.read_keys[0]:
            INOW=float(self.inst.query('IMAG?').replace('\n','').replace('A',''))
            return([(Key,INOW),])
            
            