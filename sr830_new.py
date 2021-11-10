from time import sleep
from PyQt5 import QtTest
import variables

# sens_dic = {'0': "2 nV/fA",'1': "5 nV/fA",'2': "10 nV/fA",'3': "20 nV/fA",'4': "50 nV/fA",'5': "100 nV/fA",'6': "200 nV/fA",'7': "500 nV/fA",'8': "1 μV/pA",'9': "2 μV/pA",'10': "5 μV/pA",'11': "10 μV/pA",'12': "20 μV/pA",'13': "50 μV/pA",'14': "100 μV/pA",'15': "200 μV/pA",'16': "500 μV/pA",'17': "1 mV/nA",'18': "2 mV/nA",'19': "5 mV/nA",'20': "10 mV/nA",'21': "20 mV/nA",'22': "50 mV/nA",'23': "100 mV/nA",'24': "200 mV/nA",'25': "500 mV/nA",'26': "1 V/μA"}
#
# time_dic = {'0': "10 μs",'1': "30 μs",'2': "100 μs",'3': "300 μs",'4': "1 ms",'5': "3 ms",'6': "10 ms",'7': "30 ms",'8': "100 ms",'9': "300 ms",'10': "1 s",'11': "3 s",'12': "10 s",'13': "30 s",'14': "100 s",'15': "300 s",'16': "1 ks",'17': "3 ks",'18': "10 ks",'19': "30 ks"}
# ref_dic = {'0':'External','1':'Internal'}


class Sr830(object):

    def __init__(self,inst):
        self.sens_dict = {"2 nV/fA":'0',"5 nV/fA":'1',"10 nV/fA":'2',"20 nV/fA":'3',"50 nV/fA":'4',"100 nV/fA":'5',"200 nV/fA":'6',"500 nV/fA":'7',"1 μV/pA":'8',"2 μV/pA":'9',"5 μV/pA":'10',"10 μV/pA":'11',"20 μV/pA":'12',"50 μV/pA":'13',"100 μV/pA":'14',"200 μV/pA":'15',"500 μV/pA":'16',"1 mV/nA":'17',"2 mV/nA":'18',"5 mV/nA":'19',"10 mV/nA":'20',"20 mV/nA":'21',"50 mV/nA":'22',"100 mV/nA":'23',"200 mV/nA":'24',"500 mV/nA":'25',"1 V/μA":'26'}
        self.sens_dict_inverted = {0:2e-9,1:5e-9,2:10e-9,3:20e-9,4:50e-9,5:1e-7,6:2e-9,7:5e-7,8:1e-6,9:2e-6,10:5e-6,11:1e-5,12:2e-5,13:5e-5,14:1e-4,15:2e-4,16:5e-4,17:1e-3,18:2e-3,19:5e-3,20:1e-2,21:2e-2,22:5e-2,23:1e-1,24:2e-1,25:5e-1,26:1}
        self.time_dict = {"10 μs":'0',"30 μs":'1',"100 μs":'2',"300 μs":'3',"1 ms":'4',"3 ms":'5',"10 ms":'6',"30 ms":'7',"100 ms":'8',"300 ms":'9',"1 s":'10',"3 s":'11',"10 s":'12',"30 s":'13',"100 s":'14',"300 s":'15',"1 ks":'16',"3 ks":'17',"10 ks":'18',"30 ks":'19'}
        self.time_dict_inverted = {'0':10e-6,'1':30e-6,'2':100e-6,'3':300e-6,'4':1e-3,'5':3e-3,'6':10e-3,'7':30e-3,'8':100e-3,'9':300e-3,'10':1,'11':3,'12':10,'13':30,'14':100,'15':300,'16':1e3,'17':3e3,'18':1e4,'19':3e4}
        self.inst = inst
        self.isenss = None
        self.autogain = True
        self.uponly = False
        # self.inst.query_delay = 2
        self.inst.clear()
        self.inst.timeout = None #timeout infinite bc of overload
        self.inst.write('REST')
        
        InputConfig = int(self.inst.query('ISRC?'))
        if InputConfig == 2 or InputConfig == 3:
            self.multiplier = 1e-6
        else:
            self.multiplier = 1
    
    def data_info(self,devicenumber):#returns the data keys of the device
        self.devicenumber = devicenumber
        self.data_keys = [str(devicenumber) + '_SR830_X',str(devicenumber) + '_SR830_Y']
        return(self.data_keys)

    def read_info(self,devicenumber):
        self.read_keys = [str(devicenumber) + '_SR830_XY']
        return(self.read_keys)
    
    def write_info(self,devicenumber):
        self.write_keys = [str(devicenumber) + '_SR830_' + 'Parameters']
        return(self.write_keys)
    
    def write_pattern(self,devicenumber,write_key):
        if write_key == self.write_keys[0]:
            return([('Reference','choice',['None','Internal','External']),('Sensitivity','choice',['None','Auto'] + list(self.sens_dict)),('Time Constant','choice',['None'] + list(self.time_dict)),('Amplitude(V)','text',None),('Phase(°) (type auto for autophase)','text',None),('Frequency(Hz)','text',None),('Autogain','choice',['None','on','off', 'up only'])])

    
    
    
    
    def floatHandling(self,text):
        try:
            f = str(float(text))
        except:
            try:
                f = str(float(text.replace(',','.')))
            except:
                f = False
        return(f)
    
    
    
    


    # def OverloadHandling(self):
    #     Status = self.inst.query('LIAS? 2')[0]# query : 1\n of ovld or 0\n
    #     if Status == '1':
    #         i = self.inst.query('OFLT?').replace('\n','')
    #         T = self.time_dict_inverted[i]
    #         self.inst.write('AGAN')
    #         running = self.inst.query('*STB? 1')[0]
    #         while running == '1':
    #             sleep(T)
    #             running = self.inst.query('*STB? 1')[0]
    #         f = self.inst.query('SNAP? 1,2') #blank measurement after autogain (bad point)
    #         sleep(10*T)#seconds
    #         f = self.inst.query('SNAP? 1,2') #blank measurement after autogain (bad point)
    #         self.inst.write('REST')#just in case
    #         self.inst.write('*CLS')#reset status buffer
    
    def OverloadHandling(self):
        X,Y,R = self.inst.query('SNAP? 1,2,3').split(',') #querying X,Y and R
        X,Y,R = float(X),float(Y),float(R)
        if self.autogain:
            isens = int(self.inst.query('SENS?').replace('\n','')) #querying sensistivity
            i = self.inst.query('OFLT?').replace('\n','') #querying time constant
            T = self.time_dict_inverted[i]
            variables.sharedbuffer[self.devicenumber-1] = self.sens_dict_inverted[isens]
            while isens <26 and R > 0.95*self.sens_dict_inverted[isens]*self.multiplier:
                isens += 1
                self.inst.write('SENS ' + str(isens))
                self.isenss = isens #saving the sensitivity in the variable self.isenss 
                sleep(10*T)#seconds
                self.inst.write('REST') #Reset the scan. All stored data is lost
                self.inst.write('*CLS') #Clear all status bytes
                X,Y,R = self.inst.query('SNAP? 1,2,3').split(',')
                X,Y,R = float(X),float(Y),float(R)
                variables.sharedbuffer[self.devicenumber-1] = self.sens_dict_inverted[isens]*self.multiplier
            while isens>0 and R < 0.7*self.sens_dict_inverted[isens-1]*self.multiplier:
                isens-=1
                self.inst.write('SENS ' + str(isens))
                self.isenss = isens
                sleep(10*T)#seconds
                self.inst.write('REST')
                self.inst.write('*CLS')
                X,Y,R = self.inst.query('SNAP? 1,2,3').split(',')
                X,Y,R = float(X),float(Y),float(R)
                variables.sharedbuffer[self.devicenumber-1] = self.sens_dict_inverted[isens]*self.multiplier
                
        if self.uponly:
            if self.isenss == None:
                isens = int(self.inst.query('SENS?').replace('\n',''))
            else: 
                isens = self.isenss
                
            variables.sharedbuffer[self.devicenumber-1] = self.sens_dict_inverted[isens]
            while  R > 0.90*self.sens_dict_inverted[isens]*self.multiplier:
                isens += 1
                self.inst.write('SENS ' + str(isens))
                self.isenss = isens
            
        return(X,Y)
    
    def Read(self,Key):
        X,Y = self.OverloadHandling()
        if Key == self.read_keys[0]:
            return ([(self.data_keys[0],X),(self.data_keys[1],Y)])
        return()
    
    def Write(self,Key,L):#L = ['Internal', '50 nV/fA', '300 μs', '1', '2', '3']
        if Key == self.write_keys[0]:
            if L[0] == 'Internal':
                self.inst.write('FMOD 1')
            elif L[0] == 'External':
                self.inst.write('FMOD 0')
            if L[1] != 'None':
                if L[1] == 'Auto':
                    i = self.inst.query('OFLT?').replace('\n','')
                    T = self.time_dict_inverted[i]
                    self.inst.write('AGAN')
                    running = self.inst.query('*STB? 1')[0]
                    while running == '1':
                        sleep(T)
                        running = self.inst.query('*STB? 1')[0]
                    f = self.inst.query('SNAP? 1,2') #blank measurement after autogain (bad point)
                    sleep(10*T)#seconds
                    f = self.inst.query('SNAP? 1,2') #blank measurement after autogain (bad point)
                    self.inst.write('REST')#just in case
                    self.inst.write('*CLS')#reset status buffer
                else:
                    self.inst.write('SENS ' + self.sens_dict[L[1]])
                    self.isenss = self.sens_dict[L[1]]
            if L[2] != 'None':
                self.inst.write('OFLT' + self.time_dict[L[2]])
            
            f = self.floatHandling(L[5])
            if type(f) == type('42.0'):
                self.inst.write('FREQ ' + str(f))
            if L[4].lower() == 'auto':
                self.inst.write('APHS')
            else:
                phi = self.floatHandling(L[4])
                if type(phi) == type('42.0'):
                    if float(phi) >= -360 and float(phi) <= 729.99:
                        self.inst.write('PHAS ' + phi)
            
            V = self.floatHandling(L[3])
            if type(V) == type('42.0'):
                if float(V) >= 0.04 and float(V) <= 5:
                        self.inst.write('SLVL ' + V)
            if L[6] == 'on':
                self.autogain = True
                self.uponly = False
            elif L[6] == 'off':
                self.autogain = False
                self.uponly = False
            elif L[6] == 'up only':
                self.uponly = True
                self.autogain = False
            
            return(True)
            
                
    