from time import sleep
class Bilt(object):

    def __init__(self,inst):
        self.inst = inst
        
        self.param_dict = {}
        
        #self.id = id
        #self.channel = channel
        #self.Vmemory = self.DataQueryCheck()
    





    def data_info(self,devicenumber):#returns the data keys of the device
        self.data_keys = []
        for k in range(1,6):
            self.inst.write('i' + str(k))
            q = self.inst.query('*IDN?')
            if 'No instrument' not in q:
                modulename = q.split(',')[0]
                if modulename == '586':
                    self.data_keys.append(str(devicenumber) + '_Bilt_' + modulename + '_i' + str(k) + '_c1' + '_voltage')
                    self.data_keys.append(str(devicenumber) + '_Bilt_' + modulename + '_i' + str(k) + '_c2' + '_voltage')
                    self.data_keys.append(str(devicenumber) + '_Bilt_' + modulename + '_i' + str(k) + '_c3' + '_voltage')
                    self.data_keys.append(str(devicenumber) + '_Bilt_' + modulename + '_i' + str(k) + '_c1' + '_current')
                    self.data_keys.append(str(devicenumber) + '_Bilt_' + modulename + '_i' + str(k) + '_c2' + '_current')
                    self.data_keys.append(str(devicenumber) + '_Bilt_' + modulename + '_i' + str(k) + '_c3' + '_current')
                elif modulename == '2102' or modulename == '2231':
                    self.data_keys.append(str(devicenumber) + '_Bilt_' + modulename + '_i' + str(k) + '_voltage')
        return(self.data_keys)

    def read_info(self,devicenumber):
        self.read_keys = []
        for key in self.data_keys:
            self.read_keys.append(key)
        return(self.read_keys)
    
    def write_info(self,devicenumber):
        self.write_keys = []
        for key in self.data_keys:
            self.write_keys.append(key)
            if 'voltage' in key:
                self.write_keys.append(key.replace('_voltage','_parameters'))
        return(self.write_keys)
    
    def write_pattern(self,devicenumber,write_key):
        if 'voltage' in write_key:
            return([('voltage','text',None)])
        elif 'current' in write_key:
            return([('current','text',None)])
        elif 'parameters' in write_key:
            if '2231' in write_key:
                return([('autorange','choice',['None','on','off']),('range','choice',['None','5','50']),('output','choice',['None','on','off'])])
            elif '2102' in write_key:
                return([('autorange','choice',['None','on','off']),('range','choice',['None','1.2','12']),('output','choice',['None','on','off'])])
            elif '586' in write_key:
                return([('Volt autorange','choice',['None','on','off']),('Current autorange','choice',['None','on','off']),('Volt range(V)','choice',['None','-120','120']),('Current range(A)','choice',['None','0.002','0.2']),('output','choice',['None','on','off'])])


    def floatHandling(self,text):
        try:
            f = str(float(text))
        except:
            try:
                f = str(float(text.replace(',','.')))
            except:
                f = False
        return(f)



    def init_v(self,Vmin,Vmax):
        #self.Vmemory = self.DataQueryCheck()
        None


    def Write(self,Key,L):#L -> data with variable length
        #print 'iX' , X=1,2,3,4 or 5
        if '586' in Key:
            self.WriteBE586(Key,L)
        else:
            self.inst.write(Key.split('_')[3])
            if 'voltage' in Key:
                v = self.floatHandling(L[0])
                if type(v) == type('1'):
                    self.inst.write('volt ' + v)
                    self.inst.write('outp on')
                # else:
                #     print('erreur valeur tension')
            elif 'parameters' in Key:
                if L[0] != 'None':
                    self.inst.write('outp off')
                    self.inst.write('volt:rang:auto ' + L[0])
                v = self.floatHandling(L[1])
                if type(v) == type('1'):
                    self.inst.write('outp off')
                    self.inst.write('volt:rang ' + v)
                # else:
                #     print('erreur valeur tension')
    
                if L[2] != 'None':
                    self.inst.write('outp ' + L[2])
        return(True)#each write function returns True when done

   

    def Read(self,Key):
        if '586' in Key:
            return(self.ReadBE586(Key))
        else:
            self.inst.write(Key.split('_')[3])#print 'iX' , X=1,2,3,4 or 5
            v = float(self.inst.query('MEAS:VOLT ?').replace('\n',''))
            return ([(Key,v),])





    def WriteBE586(self,Key,L):
        self.inst.write(Key.split('_')[3])
        self.inst.write(Key.split('_')[4])
        if 'voltage' in Key:
            v = self.floatHandling(L[0])
            if type(v) == type('1'):
                Vrange = float(self.floatHandling(self.inst.query('VOLT:RANG?')))
                V = float(v)
                if Vrange > 0 and V < 0:
                    self.inst.write('outp off')
                    self.inst.write('VOLT:RANG -120')
                elif V >= 0 and Vrange < 0:
                    self.inst.write('outp off')
                    self.inst.write('VOLT:RANG 120')
                if V >-0.25 and V < 0:
                    v = str(-0.25)
                elif V < 0.25 and V >= 0:
                    v = str(0.25)
                self.inst.write('volt ' + v)
                self.inst.write('outp on')
        elif 'current' in Key:
            None
        elif 'parameters' in Key:
            if L[0] != 'None':
                self.inst.write('outp off')
                self.inst.write('volt:rang:auto ' + L[0])
            if L[1] != 'None':
                self.inst.write('outp off')
                self.inst.write('curr:rang:auto ' + L[0])
            v = self.floatHandling(L[2])
            if type(v) == type('1'):
                self.inst.write('outp off')
                self.inst.write('volt:rang ' + v)
            c = self.floatHandling(L[3])
            if type(c) == type('1'):
                self.inst.write('outp off')
                self.inst.write('curr:rang ' + c)
                # else:
                #     print('erreur valeur tension')
            if L[4] != 'None':
                self.inst.write('outp ' + L[4])



    def ReadBE586(self,Key):
        self.inst.write(Key.split('_')[3])#print 'iX' , X=1,2,3,4 or 5
        self.inst.write(Key.split('_')[4])
        if 'voltage' in Key:
            v = float(self.inst.query('MEAS:VOLT ?').replace('\n',''))
            return ([(Key,v),])
        elif 'current' in Key:
            v = float(self.inst.query('MEAS:CURR ?').replace('\n',''))
            return ([(Key,v),])
