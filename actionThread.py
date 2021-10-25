# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 10:29:58 2021

@author: Drawings2
"""
from PyQt5 import QtCore,QtTest
import numpy as np
from time import time,sleep
import csv,os
from math import *
import copy

##################### email preparation
import email,smtplib, ssl 
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#####################



import variables


class Action(QtCore.QObject):
    
    def __init__(self,Plot2D):
        super().__init__()
        
        self.Plot2D = Plot2D

    
    def run(self):#function called when pangolab is launched and is running until pamngolab is closed
        while not variables.close:
            if variables.id_in_process != -1:
                self.ActionToFunction()
            sleep(5e-3)

    
    def ActionToFunction(self):#execute the current action
        if type(variables.actionlist[variables.id_in_process][1]) != type(None) or variables.actionlist[variables.id_in_process][0] == 'ClearData' or variables.actionlist[variables.id_in_process][0] == 'Idle':
            if variables.actionlist[variables.id_in_process][0] == 'VRampe':
                self.Vrampe()
            elif variables.actionlist[variables.id_in_process][0] == 'SaveData':
                self.SaveDataFunc()
            elif variables.actionlist[variables.id_in_process][0] == 'ClearData':
                self.ClearDataFunc()
            elif variables.actionlist[variables.id_in_process][0] == 'Write':
                self.WriteFunc()
            elif variables.actionlist[variables.id_in_process][0] == 'Idle':
                self.IdleInit()
            elif variables.actionlist[variables.id_in_process][0] == 'Sweep2D':
                self.Rampe2D_init()
            elif variables.actionlist[variables.id_in_process][0] == 'Read':
                self.ReadFunc()
            elif variables.actionlist[variables.id_in_process][0] == 'Math':
                self.MathFunc()
            elif variables.actionlist[variables.id_in_process][0] == 'JumpIf':
                self.JumpIfFunc()
            elif variables.actionlist[variables.id_in_process][0] == 'CustomSweep':
                self.CustomSweepFunc()
            elif variables.actionlist[variables.id_in_process][0] == 'Irampe':
                self.IrampeFunc()
                
            elif variables.actionlist[variables.id_in_process][0] == 'SetTemp':
                self.setTempFunc()
                
               
        else:
            self.id_temp = variables.id_in_process
            variables.id_in_process += 1
            self.ShouldStop()
    
###############################################################################################################################
    
    #custom functions to be called later on by action function
    
################################################################################################################################

    def isDeviceDone(self):#checks if all the devices are done reading/writing
        isDone = False
        while not isDone:
            #QtTest.QTest.qWait(30)#time signal to be emitted
            isDone = True
            for dev in variables.QueryList:
                if len(dev) > 0:
                    isDone = False
                    break
            QtTest.QTest.qWait(10)
    

    def ReadCustom(self,actions):#reads devices and adds the measurement to Data
        #actions = [['devicex_key','readkey1'],['devicex_key','readkey2']...]
        for request in actions:
            if request[0] == 'Math':
                variables.Data['Math'].append(float(self.VariablesToStr(request[1])))
            else:
                x = int(request[0].split('_')[0])-1
                # print(x)
                # print(request[1])
                variables.QueryList[int(request[0].split('_')[0])-1].append(('Read',request[1]))
        variables.Data['Time'].append(time()-variables.t0)
        isDoneMeasuring = False
        while not isDoneMeasuring:
            QtTest.QTest.qWait(30)#time signal to be emitted
            isDoneMeasuring = True
            for dev in variables.QueryList:
                if len(dev) > 0:
                    isDoneMeasuring = False
                    break
        return()
    
    def WriteCustom(self,actions):
        #actions = [['devicex_key','writekey1',parameter1,...],['devicex_key','writekey2',parameter1,...]...]

        variables.QueryList[int(actions[0].split('_')[0])-1].append(('Write',actions[1:]))
        return()

    def ReadwithoutSaving(self,request):#only for one request/read_key
        #request = ['device_key','readkey']
        dev = int(request[0].split('_')[0])-1
        variables.sharedbuffer[dev] = None
        variables.QueryList[dev].append(('ReadwithoutSaving',request[1]))
        isDoneMeasuring = False
        while not isDoneMeasuring:
            isDoneMeasuring = True
            if len(variables.QueryList[dev]) > 0:
                isDoneMeasuring = False
                break
            QtTest.QTest.qWait(30)#time signal to be emitted
        while type(variables.sharedbuffer[dev]) == type(None):
            QtTest.QTest.qWait(10)
        return(variables.sharedbuffer[dev])

#Action function
    

    def WriteFunc(self):
        self.id_temp = variables.id_in_process
        param = variables.actionlist[variables.id_in_process][1][:]
        for k in range(len(param)):
            param[k] = self.VariablesToStr(param[k])
        # print(int(param[0].split('_')[0])-1)
        # print(param[1:])
        variables.QueryList[int(param[0].split('_')[0])-1].append(('Write',param[1:]))
        self.isDeviceDone()
        if self.ShouldStop():
            return()
        variables.id_in_process += 1
        self.ShouldStop()
        return()
    
    def ReadFunc(self):
        self.id_temp = variables.id_in_process
        param = variables.actionlist[variables.id_in_process][1]
        for request in param:
            if request[0] == 'Math':
                variables.Data['Math'].append(float(self.VariablesToStr(request[1])))
            else:
               
                variables.QueryList[int(request[0].split('_')[0])-1].append(('Read',request[1]))
        variables.Data['Time'].append(time()-variables.t0)
        self.isDeviceDone()
        if self.ShouldStop():
            return()
        variables.id_in_process += 1
        self.ShouldStop()
        return()





    #2 functions, init is called once while run is called by the timer
    def Vrampe(self):
        self.i = 1#index sweep
        self.ReadParam = variables.actionlist[variables.id_in_process][1]
        self.SweepParam = variables.actionlist[variables.id_in_process][2]
        #self.connectedDevicesInst[param[0]].init_v(param[1],param[2])
        self.ReadCustom(self.ReadParam)
        #QtTest.QTest.qWait(50)
        try:
            V = variables.Data[self.SweepParam[1]][-1]
        except:
            V = 0
        pas = self.SweepParam[7]*(2*(V < self.SweepParam[2]) - 1)
        L1 = np.arange(V,self.SweepParam[2],pas)#300 mV step from initial measured value to vstart
        try:
            sweep = int(self.SweepParam[6])
            if sweep == 0:
                self.Lcons = np.concatenate([L1,np.linspace(self.SweepParam[2],self.SweepParam[3],self.SweepParam[4])])
            else:
                Ltemp = np.tile(np.concatenate([np.linspace(self.SweepParam[2],self.SweepParam[3],self.SweepParam[4]),np.linspace(self.SweepParam[3],self.SweepParam[2],self.SweepParam[4])]),sweep)
                self.Lcons = np.concatenate([L1,Ltemp])
        except:
            if self.SweepParam[6] == 'inf':
                Ltemp = np.tile(np.concatenate([np.linspace(self.SweepParam[2],self.SweepParam[3],self.SweepParam[4]),np.linspace(self.SweepParam[3],self.SweepParam[2],self.SweepParam[4])]),2)
                self.Lcons = np.concatenate([L1,Ltemp])
            else:
                return()
        self.id_temp = variables.id_in_process
        # self.Querys() #querys adds in average 100 ms
        
        while True:
            if self.ShouldStop():
                return()
            if self.i >= len(self.Lcons):
                if self.SweepParam[6] == 'inf':    
                    Ltemp = np.concatenate([np.linspace(self.SweepParam[2],self.SweepParam[3],self.SweepParam[4]),np.linspace(self.SweepParam[3],self.SweepParam[2],self.SweepParam[4])])
                    self.Lcons = np.concatenate([self.Lcons,Ltemp])
                else:
                    QtTest.QTest.qWait(1000) #This wait was added to avoid that the save start before acquiring the last data
                    variables.id_in_process += 1
                    self.ShouldStop()
                    return()
            self.WriteCustom([self.SweepParam[0],self.SweepParam[1],self.Lcons[self.i]])
            QtTest.QTest.qWait(self.SweepParam[5])
            self.ReadCustom(self.ReadParam)
            self.i += 1
        return()
        
   #2 functions, init is called once while run is called by the timer
    def IrampeFunc(self):
        self.i = 1#index sweep
        self.ReadParam = variables.actionlist[variables.id_in_process][1]
        self.SweepParam = variables.actionlist[variables.id_in_process][2]
        #self.connectedDevicesInst[param[0]].init_v(param[1],param[2])
        # self.ReadCustom(self.ReadParam) #reading the parameters of the instrument set to be read
        #QtTest.QTest.qWait(50)
        # try:
        #     V = variables.Data[self.SweepParam[1]][-1] #checking if it exist the last read of the sweep instrument
        # except:
        #     V = 0
        self.WriteCustom([self.SweepParam[0],self.SweepParam[1],self.SweepParam[2]])
        
        self.CheckThreshold(self.SweepParam[0:2], 0.0005, 1000, 5, self.SweepParam[2])  #checkin the threshold to be at the initial value
           
        # pas = self.SweepParam[7]*(2*(V < self.SweepParam[2]) - 1)
        # L1 = np.linspace(V,self.SweepParam[2],2)#300 mV step from initial measured value to vstart
        try:
            sweep = int(self.SweepParam[5])
            if sweep == 0:
                self.Lcons = np.linspace(self.SweepParam[2],self.SweepParam[3],2)
            else:
                Ltemp = np.tile(np.concatenate([np.linspace(self.SweepParam[2],self.SweepParam[3],2),np.linspace(self.SweepParam[3],self.SweepParam[2],2)]),sweep)
                self.Lcons = np.concatenate([L1,Ltemp])
        except:
            if self.SweepParam[5] == 'inf':
                Ltemp = np.tile(np.concatenate([np.linspace(self.SweepParam[2],self.SweepParam[3],self.SweepParam[4]),np.linspace(self.SweepParam[3],self.SweepParam[2],self.SweepParam[4])]),2)
                self.Lcons = np.concatenate([L1,Ltemp])
            else:
                return()
        self.id_temp = variables.id_in_process
        # self.Querys() #querys adds in average 100 ms
        
        while True:
            if self.ShouldStop():
                return()
            if self.i >= len(self.Lcons):
                if self.SweepParam[5] == 'inf':    
                    Ltemp = np.concatenate([np.linspace(self.SweepParam[2],self.SweepParam[3],2),np.linspace(self.SweepParam[3],self.SweepParam[2],2)])
                    self.Lcons = np.concatenate([self.Lcons,Ltemp])
                else:
                    QtTest.QTest.qWait(1000) #This wait was added to avoid that the save start before acquiring the last data
                    variables.id_in_process += 1
                    self.ShouldStop()
                    return()
            self.ReadCustom(self.ReadParam)
            
            self.WriteCustom([self.SweepParam[0],self.SweepParam[1],self.Lcons[self.i]])
            
            
            
            
            V = variables.Data[self.SweepParam[1]][-1]

            while abs(V-self.Lcons[self.i])>0.0005:
                
                QtTest.QTest.qWait(self.SweepParam[4])
                self.ReadCustom(self.ReadParam)
                V = variables.Data[self.SweepParam[1]][-1]
                
            self.i += 1
        return()     
        #self.timer.start(self.SweepParam[5])

    def setTempFunc(self):
        self.i = 1#index sweep
        self.ReadParam = [variables.actionlist[variables.id_in_process][1][:2][:]]
        self.SweepParam = variables.actionlist[variables.id_in_process][1][:]
        
        # print(self.SweepParam[1])
        self.WriteCustom([self.SweepParam[0],self.SweepParam[1],self.SweepParam[-1]])    #writting the set temperature
        
        self.devicekeyrange= self.SweepParam[1][:-1]+'range'
        # print(self.SweepParam[0])
        # print(self.devicekeyrange)
        # print(self.SweepParam[3])
        # print(self.SweepParam[2])
        self.WriteCustom([self.SweepParam[0],self.devicekeyrange,self.SweepParam[3],str(self.SweepParam[2])]) #writting the output and the range of the output
        
        initialtime = time()/60 ###### converting time in minutes
        setpointisgood = True   ###### variable used in the while
        
        
        ####defining error scale for different temperature (in Kelvin)
        if abs(self.SweepParam[-1]) <101: #for temperatures smaller than 101 K
            errorscale = 0.005 #error acceptable - 0.5%
        if abs(self.SweepParam[-1]) <51: #for temperatures smaller than 51 K
            errorscale = 0.01  #error acceptable - 1%
        
        elif abs(self.SweepParam[-1]) <21: #for temperatures smaller than 21 K
            errorscale = 0.1    #error acceptable - 10%
        elif abs(self.SweepParam[-1]) < 3: #for temperatures smaller than 4 K
            errorscale = 0.08 #error acceptable - 8%
        
        elif abs(self.SweepParam[-1]) <0.3:
            self.id_in_process += 1
            self.ShouldStop()
            return()
        else:                   #for temperatures bigger than 101 K
            errorscale = 0.003  #error acceptable - 0.3%

        # print(self.ReadParam)
        self.ReadCustom(self.ReadParam)
        
        V = variables.Data[self.SweepParam[1]][-1]
        
        T2 = []
        
        while setpointisgood:   #separation between setpoint and measured temperature
            if self.ShouldStop():
                return()
           
            
            
            
            QtTest.QTest.qWait(1000)  #wait 1s
            
            self.ReadCustom(self.ReadParam)
        
            V = variables.Data[self.SweepParam[1]][-1]
        
            T2.append( V ) #measure the temperature and append to array T2
            if self.SweepParam[-1] != 0: # if set temperature different than 0 
                
                err = (T2[-1] - self.SweepParam[-1])/self.SweepParam[-1] #calculates the error = % of measured Temperature with respect to the set temperature
            else:
                self.SweepParam[-1] = 0.3 #putting set temp as 1 to avoid stupid error of percentage
                err = (T2[-1] - self.SweepParam[-1])/self.SweepParam[-1]
            print("waiting setpoint to be reached T=" )
            print(str(T2[-1]))
            
            if err<errorscale: #if error is smaller than what I set in the beggining, continue the program, otherwise continue on this while
                setpointisgood = False
            getnewtime = time()/60
            
            if abs(getnewtime-initialtime)>30: #if this while goes for longer then 30 minutes
                setpointisgood = False
                print("It could not get temperature stable after 20 minutes")
        
        T2 = []
        trial = 0
        
        # check if temperature stays lower then error for 5 minutes, if it is the case finishs, if not verify for more 2 minutes
     
            
        initialtime = time()/60
        
         ####defining error scale ( in temperature now)
        if abs(self.SweepParam[-1]) <101:
            errorscale = 1
        if abs(self.SweepParam[-1]) <51:
            errorscale = 0.8
        
        elif abs(self.SweepParam[-1]) <21:
            errorscale = 0.6
            
        else: 
            errorscale = 2
            
        while trial < 300:
            
                if self.ShouldStop():
                    return()
                
                QtTest.QTest.qWait(1000) #wait one second
                
                
                self.ReadCustom(self.ReadParam)
        
                V = variables.Data[self.SweepParam[1]][-1]
        
                T2.append( V ) #measure the temperature and append to array T2
               
                err = abs(T2[-1] - self.SweepParam[-1]) #calculate error of the measured temperature with respect to set temperature
                if err<errorscale:
                    trial+=1 #if it is ok, it adds one t trial (it is a counter parameter)
                else:
                    trial = 0 #if larger than the error, sets the counter to zero
                
                expectedtime = (300-trial)/ 60
                print("waiting equilibration")
                print("Expected time to finish - %5.3f minutes"%expectedtime)
                getnewtime = time()/60
                
                if abs(getnewtime-initialtime)>30: #if stays in this while longer then half hour, it stops the counting and continue to the next action of pango
                    trial = 600
                    print("It could not get temperature stable after 30 minutes")
               
            

        
        

                
        variables.id_in_process += 1
        self.ShouldStop()
        return()

        return ()

    def Rampe2D_init(self):
        self.cons2D = [] #[axis = 'Fast'/'Slow',Measure = True/False,value, Wait threshold = True/false]
        
        self.ReadParam = variables.actionlist[variables.id_in_process][1] # getting the list of parameters to be read
        self.SweepParam = {'Fast':variables.actionlist[variables.id_in_process][2],'Slow':variables.actionlist[variables.id_in_process][3]}
        #the list of parameters to be sweep
        
        
        variables.Lx,variables.Ly = self.SweepParam['Fast'][4],self.SweepParam['Slow'][4] #number of point in x and y direction
        variables.ix,variables.iy = 0,0
        variables.Data_image = np.zeros((variables.Lx,variables.Ly)) #creating the size of the image
        
        self.ReadCustom(self.ReadParam) ##reads devices and adds the measurement to Data
        
        Vfast = variables.Data[self.SweepParam['Fast'][1]][-1] #last read data of fast instrument
        Vslow = variables.Data[self.SweepParam['Slow'][1]][-1] #last read data of slow instrument
        #generate cons
        sign = 2*(self.SweepParam['Fast'][2] > Vfast) - 1
        L = np.arange(Vfast,self.SweepParam['Fast'][2],sign*self.SweepParam['Fast'][6]) #creating array to go from the current value to the first data point of the ramp
        
        for x in L:
            self.cons2D.append(('Fast',False,x,False))
        self.cons2D.append(('Fast',False,self.SweepParam['Fast'][2],False))
        sign = 2*(self.SweepParam['Slow'][2] > Vslow) - 1
        L = np.arange(Vslow,self.SweepParam['Slow'][2],sign*self.SweepParam['Slow'][6])
        for x in L:
            self.cons2D.append(('Slow',False,x,False))
        self.cons2D.append(('Slow',False,self.SweepParam['Slow'][2],False))
        
        sign = 2*(self.SweepParam['Fast'][3] > self.SweepParam['Fast'][2]) - 1
        Lfast = np.linspace(self.SweepParam['Fast'][2],self.SweepParam['Fast'][3],self.SweepParam['Fast'][4])
        Lfastback = np.arange(self.SweepParam['Fast'][3],self.SweepParam['Fast'][2],-sign*self.SweepParam['Fast'][6])
        Lslow = np.linspace(self.SweepParam['Slow'][2],self.SweepParam['Slow'][3],self.SweepParam['Slow'][4])
        for xslow in Lslow:
            self.cons2D.append(('Slow',False,xslow,self.SweepParam['Slow'][7]))
            self.cons2D.append(('Fast',False,Lfast[0],False))
            for k in range(0,len(Lfast)):
                self.cons2D.append(('Fast',True,Lfast[k],self.SweepParam['Fast'][7]))
            #self.cons2D.append(('Fast',False,Lfastback[0]))
            for k in range(0,len(Lfastback)):
                self.cons2D.append(('Fast',False,Lfastback[k],False))
        
        self.id_temp = variables.id_in_process
        
        while True:
            if self.ShouldStop():
                return()
            # print(param)
            if len(self.cons2D) == 0 :
                #QtTest.QTest.qWait(100) #This wait was added to avoid that the save start before acquiring the last data
                variables.id_in_process += 1
                self.ShouldStop()
                return()
            #print([self.SweepParam[self.cons2D[0][0]][0],self.SweepParam[self.cons2D[0][0]][1],self.cons2D[0][2]])
            
            
            self.WriteCustom([self.SweepParam[self.cons2D[0][0]][0],self.SweepParam[self.cons2D[0][0]][1],self.cons2D[0][2]])
            x = self.SweepParam[self.cons2D[0][0]]
            # print(x)
            if self.cons2D[0][3]:
                #print(x)
                # print(x[:2],float(x[9]),float(x[10]),int(x[8]),self.cons2D[0][2])
                # print(self.cons2D[0][2])
                self.CheckThreshold(x[:2],float(x[9]),float(x[10]),int(x[8]),self.cons2D[0][2])
                if self.ShouldStop():
                    return()
            QtTest.QTest.qWait(self.SweepParam[self.cons2D[0][0]][5])
            if self.cons2D[0][1]:
                self.ReadCustom(self.ReadParam)
                try:
                    if variables.ix == variables.Lx:
                        variables.ix = 0
                        variables.iy +=1
                    if variables.ZplotText != 'None':
                        variables.Data_image[variables.ix][variables.iy] = variables.Data[variables.ZplotText][-1]
                    variables.ix+=1
                except:
                    None
                # print(self.i)
            if variables.ZplotText != 'None':
                self.Plot2D()
            
            del self.cons2D[0]
        return()
        




    def SaveDataFunc(self):
        self.id_temp = variables.id_in_process
        param = variables.actionlist[variables.id_in_process][1]
        
        os.chdir(self.VariablesToStr(param[0]))
        
        QtTest.QTest.qWait(100)#waits for the last data points
        
        self.SaveDataLogFile(self.VariablesToStr(param[1]))
        with open(self.VariablesToStr(param[1]),'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t', quotechar='|')
            row = []
            index = 0
            keys = list(variables.Data)
            for k in range(len(keys)-1,-1,-1):#remove empty lists
                if len(variables.Data[keys[k]]) == 0:
                    del keys[k]
            writer.writerow(keys)
            
            ##################
            #I just added this if,  let us see if it works for empty array ###
            #################################
            
            if len(variables.Data[keys[0]]) > 0:
                
                
                for i in range(len(variables.Data[keys[0]])):#The time data is the one with the most elements
                    row = []
                    for key in keys:
                        if i < len(variables.Data[key]):
                            row.append(variables.Data[key][i])
                        else:
                            row.append(None)
                    writer.writerow(row)
                csvfile.close()
                
                
            if param[3]:
                port = 465
                sender = "pangolabtopo2d@gmail.com"
                reciever = param[2]
                password = "PangoTopo2020"
                context = ssl.create_default_context()
                if param [4] : 
                    body = "The file " + self.VariablesToStr(param[1]) +" has been saved, see attached."
                    
                    message = MIMEMultipart()
                    message['From'] = sender
                    message['To'] = reciever
                    message['Subject'] = "File saved"
                    
                    message.attach(MIMEText(body,"plain"))
                    
                    with open(self.VariablesToStr(param[1]),'rb') as attachment:
                        part = MIMEBase("application","octet-stream")
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    
                    part.add_header("Content-Disposition", f"attachment; filename = {param[1]}")
                    
                    message.attach(part)
                    text = message.as_string()
                    
                    with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
                        server.login(sender,password)
                        server.sendmail(sender,reciever,text)
                else:
                    body = "The file "+param[1]+" has been saved."
                    
                    message = MIMEMultipart()
                    message['From'] = sender
                    message['To'] = reciever
                    message['Subject'] = "File saved"
                    
                    message.attach(MIMEText(body,"plain"))
                    text = message.as_string()
                    
                    with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
                        server.login(sender,password)
                        server.sendmail(sender,reciever,text)
                
        #self.MessageDialogue('File saved:' + str(os.getcwd()) +  "\\" + self.SaveInput.text())
        if self.ShouldStop():
            return()
        variables.id_in_process += 1
        self.ShouldStop()
        
        
    def SaveDataLogFile(self,name):
        namesplt = name.split('.')
        if len(namesplt) > 1:
            filename = namesplt[-2] + '_log.' + namesplt[-1]
        else:
            filename = name + '_log'
        with open(filename,'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t', quotechar='|')
            for x in variables.actionlist:
                writer.writerow(x)
        return()

    def ClearDataFunc(self):
        self.id_temp = variables.id_in_process
        all_keys = list(variables.Data)
        for key in all_keys:
            variables.Data[key] = []
        #self.Lcons = [None for k in range(6)]
        if self.ShouldStop():
            return()
        variables.id_in_process += 1
        self.ShouldStop()
    

    def IdleInit(self):
        readparam = variables.actionlist[variables.id_in_process][1]
        idleparam = variables.actionlist[variables.id_in_process][2]
        t0 = time()
        self.id_temp = variables.id_in_process
        while idleparam[1] == -1 or time()-t0 < idleparam[1]*1e-3:
            if idleparam[0] !=0 and len(readparam)>0:
                self.ReadCustom(readparam)
                sleep(idleparam[0]*1e-3)
                if self.ShouldStop():
                    return()
            else:
                sleep(0.1)
            if self.ShouldStop():
                return()
        if self.ShouldStop():
            return()
        variables.id_in_process += 1
        self.ShouldStop()
    
    def MathFunc(self):
        try:
            exec(variables.actionlist[variables.id_in_process][1][0])
        except:
            print('math error')
        if self.ShouldStop():
            return()
        variables.id_in_process += 1
        self.ShouldStop()
        return()
    
    def JumpIfFunc(self):
        # try:
        self.cd = False
        string = 'self.cd = ' + variables.actionlist[variables.id_in_process][1][0]
        exec(string)
        if self.cd:
            if variables.actionlist[variables.id_in_process][1][1] < len(variables.actionlist):
                variables.id_in_process = variables.actionlist[variables.id_in_process][1][1]
            else:
                variables.id_in_process += 1
        else:
            variables.id_in_process += 1
        # except:
        #     variables.id_in_process += 1
        #     print('math error')
        self.ShouldStop()
        return()
    
    def CustomSweepFunc(self):
        readparam = variables.actionlist[variables.id_in_process][1][:]
        writeparam = copy.deepcopy(variables.actionlist[variables.id_in_process][2])
        for k in range(len(writeparam)):
            for i in range(len(writeparam[k])):
                if type(writeparam[k][i]) == str:
                    writeparam[k][i] = self.VariablesToStr(writeparam[k][i])
        for x in writeparam:
            currentValue = float(self.ReadwithoutSaving(x[:2]))
            start,stop = float(x[3]),float(x[4])
            print(x[7])
            # print(float(x[7]))
            largestep = float(x[7])*(start-currentValue >= 0) - float(x[7])*(start-currentValue < 0)
            Gotopoint = np.arange(currentValue,start,largestep)
            for v in Gotopoint:
                self.WriteCustom([x[0],x[1],v])
                # if x[2]:
                #     threshold = float(x[3])
                #     meas = float(self.ReadwithoutSaving(x[:2]))
                #     while meas < (1-threshold)*v or meas > (1+threshold)*v:
                #         sleep(0.02)
                #         meas = float(self.ReadwithoutSaving(x[:2]))
                #         if self.ShouldStop():
                #             return()
                sleep(float(x[6])*1e-3)
                if self.ShouldStop():
                            return()
            step = float(x[5])*(stop-start >= 0) - float(x[5])*(stop-start < 0)
            Sweeppoint = list(np.arange(start,stop,step)) + [stop]
            for v in Sweeppoint:
                self.WriteCustom([x[0],x[1],v])
                if x[8]:
                    self.CheckThreshold(x[:2],float(x[9]),float(x[10]),int(x[11]),v)
                    if self.ShouldStop():
                        return()
                sleep(float(x[6])*1e-3)
                if x[2]:
                    self.ReadCustom(readparam)
                if self.ShouldStop():
                            return()
        variables.id_in_process += 1
        self.ShouldStop()
        return()
            
    def CheckThreshold(self,readparam,threshold,delay,N,v):
        i = 0
        while i < N:
            meas = float(self.ReadwithoutSaving(readparam))
            # print(meas)
            # print(abs(threshold+v))
            # print(abs(-threshold+v))
            if abs(meas-v) > abs(threshold):  #here is the bug
                i = 0
            else:
                i+=1
            sleep(delay*1e-3)
            if self.ShouldStop():
                return()
            # print(i)
        return()
    
     
            
    
    
    
        
    def VariablesToStr(self,string):
        newString = string
        L = [('variables.A',variables.A),('variables.B',variables.B),('variables.C',variables.C),('variables.D',variables.D),('variables.E',variables.E),('variables.F',variables.F)]
        for x in L:
            if x[0] in newString:
                newString = newString.replace(x[0],str(x[1]))
        return(newString)
    
            
    def ShouldStop(self):
        if not variables.IsRunning:
            return(True)
        elif variables.ExitCurrentAction:
            variables.ExitCurrentAction = False
            if variables.id_in_process == len(variables.actionlist):
                variables.IsRunning = False
                variables.id_in_process = -1
                return(True)
            else:
                #self.ActionToFunction()
                return(True)
        elif variables.id_in_process >= len(variables.actionlist):
            variables.IsRunning = False
            variables.id_in_process = -1
            return(True)
        return(False)