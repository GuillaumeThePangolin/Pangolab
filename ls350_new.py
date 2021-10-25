



class Ls350(object):
    
    def __init__(self,inst):
        self.inst = inst
    
    def data_info(self,devicenumber):
        self.data_keys = [str(devicenumber) + '_LS350_A',str(devicenumber) + '_LS350_B',str(devicenumber) + '_LS350_C',str(devicenumber) + '_LS350_D']
        return(self.data_keys)
    
    def read_info(self,devicenumber):
        self.read_keys = [str(devicenumber) + '_LS350_A',str(devicenumber) + '_LS350_B',str(devicenumber) + '_LS350_C',str(devicenumber) + '_LS350_D']
        return(self.read_keys)
    
    def write_info(self,devicenumber):
        self.write_keys = [str(devicenumber) + '_LS350_A',str(devicenumber) + '_LS350_C',str(devicenumber) + '_LS350_range']
        return(self.write_keys)
    
    def write_pattern(self,devicenumber,write_key):
        if write_key == self.write_keys[0]:
            return([('Setpoint T(K)','text',None)])
        elif write_key == self.write_keys[1]:
            return([('Setpoint T(K)','text',None)])
        elif write_key == self.write_keys[2]:
            return([('Output','choice',['A','C']),('Range','choice',['Off','1','2','3','4','5'])])
    
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
        # print(Key)
        # print(L)
        if Key == self.write_keys[0]:
            T = self.floatHandling(L[0])
            if type(T) == type(''): #checking if it is a string?
                self.inst.write('SETP ' + '1' + ',' + T)#default control loop is 1 for input A
            #self.setp(Key,L)
        elif Key == self.write_keys[1]:
            T = self.floatHandling(L[0])
            if type(T) == type(''):
                self.inst.write('SETP ' + '2' + ',' + T)#default control loop is 2 for input B
        elif Key == self.write_keys[2]:
            rDict = {'Off':0,'1':1,'2':2,'3':3,'4':4,'5':5}
            rDict2 = {'A':1,'C':2}
 
            if L[0] in rDict2 and L[1] in rDict:
                self.inst.write('RANGE ' + str(rDict2[L[0]])+','+str(rDict[L[1]]))
        return()
    
    
    def Read(self,Key):
        ABinput = Key[-1]#A,B,C or D
        T = float(self.inst.query('KRDG? '+ABinput))
        return([(Key,T),])
    
    
    
    
    
    
    
    