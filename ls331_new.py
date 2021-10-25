from time import sleep,time
import variables

class Ls331(object):
    def __init__(self,inst):
        self.inst = inst
    
    
    def data_info(self,devicenumber):#returns the data keys of the device
        self.devicenumber = devicenumber
        self.data_keys = [str(devicenumber) + '_LS331_A',str(devicenumber) + '_LS331_B']
        return(self.data_keys)

    def read_info(self,devicenumber):
        self.read_keys = [str(devicenumber) + '_LS331_A',str(devicenumber) + '_LS331_B']
        return(self.read_keys)
    
    def write_info(self,devicenumber):
        self.write_keys = [str(devicenumber) + '_LS331_' + 'A',str(devicenumber) + '_LS331_' + 'B',str(devicenumber) + '_LS331_' + 'Parameters',str(devicenumber) + '_LS331_' + 'Loop']
        return(self.write_keys)
    
    def write_pattern(self,devicenumber,write_key):
        if write_key == self.write_keys[0]:
            return([('Setpoint','text',None)])
        if write_key == self.write_keys[1]:
            return([('Setpoint','text',None)])
        elif write_key == self.write_keys[2]:
            return([('Range','choice',['None','Off','Low','Medium','High'])])
        elif write_key == self.write_keys[3]:
            return([('Control loop','choice',['1','2']),('Control loop','choice',['A','B']),('Powerup enable','choice',['off','on']),('Heater display','choice',['current','power'])])



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
            T = self.floatHandling(L[0])
            if type(T) == type(''):
                self.inst.write('SETP ' + '1' + ',' + T)#default control loop is 1 for input A
            #self.setp(Key,L)
        if Key == self.write_keys[1]:
            T = self.floatHandling(L[0])
            if type(T) == type(''):
                self.inst.write('SETP ' + '2' + ',' + T)#default control loop is 2 for input B
        elif Key == self.write_keys[2]:
            rDict = {'Off':0,'Low':1,'Medium':2,'High':3}
            if L[0] in rDict:
                self.inst.write('RANGE ' + str(rDict[L[0]]))
        elif Key == self.write_keys[3]:
            string = 'CSET ' + L[0] + ','+ L[1]+',1,'
            if L[2] == 'off':
                string += '0,'
            else:
                string += '1,'
            if L[3] == 'current':
                string += '0'
            else:
                string += '1'
            self.inst.write(string)


    def Read(self,Key):
        ABinput = Key[-1]
        T = float(self.inst.query('KRDG? '+ABinput))
        return([(Key,T),])






