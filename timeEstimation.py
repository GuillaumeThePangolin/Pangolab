# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 17:13:09 2021

@author: Drawings2
"""
import variables


#all the data is in milliseconds

latency_data_read = {'Bilt':50,"Lock-in SR830":72}
latency_data_write = {'Bilt':0,"Lock-in SR830":0}

def calculate():
    runtime = 0
    for i in range(len(variables.actionlist)):
        if type(variables.actionlist[i][1]) != type(None) or variables.actionlist[i][0] == 'ClearData':
            if variables.actionlist[i][0] == 'VRampe':
                runtime += VrampeCalculate(i)
            elif variables.actionlist[i][0] == 'SaveData':
                runtime += SaveDataCalculate(i)
            elif variables.actionlist[i][0] == 'ClearData':
                runtime += ClearDataCalculate(i)
            elif variables.actionlist[i][0] == 'Write':
                runtime += WriteCalculate(i)
            elif variables.actionlist[i][0] == 'Idle':
                runtime += IdleCalculate(i)
            elif variables.actionlist[i][0] == 'Sweep2D':
                runtime += Rampe2DCalculate(i)
            elif variables.actionlist[i][0] == 'Read':
                runtime += ReadCalculate(i)
            elif variables.actionlist[i][0] == 'CustomSweep':
                runtime += CustomSweepCalculate(i)
    return(runtime)

def VrampeCalculate(i):
    if variables.actionlist[i][2][0].split('_')[1] in latency_data_write:
        WriteLatency = latency_data_write[variables.actionlist[i][2][0].split('_')[1]]
    else:
        WriteLatency = 0
    ReadLatency = 0
    DeviceList = []
    LatencyperDevice = []
    for k in range(len(variables.actionlist[i][1])):
        if variables.actionlist[i][1][k][0] != 'Math':
            dev = variables.actionlist[i][1][k][0].split('_')[1]
            if dev in latency_data_read:
                ReadLatency = latency_data_read[dev]
            else:
                ReadLatency = 0
            if variables.actionlist[i][1][k][0] in DeviceList:
                LatencyperDevice[DeviceList.index(variables.actionlist[i][1][k][0])] += ReadLatency
            else:
                LatencyperDevice.append(ReadLatency)
                DeviceList.append(variables.actionlist[i][1][k][0])
    TotalTime = variables.actionlist[i][2][4]*(max(LatencyperDevice) + WriteLatency +variables.actionlist[i][2][5])*(2*float(variables.actionlist[i][2][6])+1)
    return(TotalTime)#in milliseconds

def Rampe2DCalculate(i):
    if variables.actionlist[i][2][0].split('_')[1] in latency_data_write:
        WriteLatency = latency_data_write[variables.actionlist[i][2][0].split('_')[1]]
    else:
        WriteLatency = 0
    ReadLatency = 0
    DeviceList = []
    LatencyperDevice = []
    for k in range(len(variables.actionlist[i][1])):
        if variables.actionlist[i][1][k][0] != 'Math':
            dev = variables.actionlist[i][1][k][0].split('_')[1]
            if dev in latency_data_read:
                ReadLatency = latency_data_read[dev]
            else:
                ReadLatency = 0
            if variables.actionlist[i][1][k][0] in DeviceList:
                LatencyperDevice[DeviceList.index(variables.actionlist[i][1][k][0])] += ReadLatency
            else:
                LatencyperDevice.append(ReadLatency)
                DeviceList.append(variables.actionlist[i][1][k][0])
    fastSweepTime = variables.actionlist[i][2][4]*(max(LatencyperDevice) + WriteLatency +variables.actionlist[i][2][5]) + abs(variables.actionlist[i][2][2] - variables.actionlist[i][2][3])/variables.actionlist[i][2][6]*(WriteLatency +variables.actionlist[i][2][5])
    if variables.actionlist[i][3][0].split('_')[1] in latency_data_write:
        WriteLatency = latency_data_write[variables.actionlist[i][3][0].split('_')[1]]
    else:
        WriteLatency = 0
    TotalTime = (fastSweepTime + WriteLatency + variables.actionlist[i][3][5])*variables.actionlist[i][3][4]
    return(TotalTime)



def CustomSweepCalculate(i):
    ReadLatency = 0
    DeviceList = []
    LatencyperDevice = []
    for k in range(len(variables.actionlist[i][1])):
        if variables.actionlist[i][1][k][0] != 'Math':
            dev = variables.actionlist[i][1][k][0].split('_')[1]
            if dev in latency_data_read:
                ReadLatency = latency_data_read[dev]
            else:
                ReadLatency = 40
            if variables.actionlist[i][1][k][0] in DeviceList:
                LatencyperDevice[DeviceList.index(variables.actionlist[i][1][k][0])] += ReadLatency
            else:
                LatencyperDevice.append(ReadLatency)
                DeviceList.append(variables.actionlist[i][1][k][0])
    maxreadlatency = max(LatencyperDevice)
    TotalTime = 0
    for j in range(len(variables.actionlist[i][2])):
        if variables.actionlist[i][2][j][0].split('_')[1] in latency_data_write:
            WriteLatency = latency_data_write[variables.actionlist[i][2][j][0].split('_')[1]]
        else:
            WriteLatency = 40
        Npoint = abs(((float(variables.actionlist[i][2][j][3])-float(variables.actionlist[i][2][j][4]))/float(variables.actionlist[i][2][j][5])))
        TotalTime += Npoint*(WriteLatency + maxreadlatency + float(variables.actionlist[i][2][j][6]))
    return(TotalTime)#in milliseconds



def SaveDataCalculate(i):
    return(100)

def ClearDataCalculate(i):
    return(10)

def WriteCalculate(i):
    if variables.actionlist[i][1][0].split('_')[1] in latency_data_write:
        WriteLatency = latency_data_write[variables.actionlist[i][2][0].split('_')[1]]
    else:
        WriteLatency = 0
    return(WriteLatency)

def IdleCalculate(i):
    return(variables.actionlist[i][2][1])

def ReadCalculate(i):
    ReadLatency = 0
    DeviceList = []
    LatencyperDevice = []
    for k in range(len(variables.actionlist[i][1])):
        if variables.actionlist[i][1][k][0] != 'Math':
            dev = variables.actionlist[i][1][k][0].split('_')[1]
            if dev in latency_data_read:
                ReadLatency = latency_data_read[dev]
            else:
                ReadLatency = 0
            if variables.actionlist[i][1][k][0] in DeviceList:
                LatencyperDevice[DeviceList.index(variables.actionlist[i][1][k][0])] += ReadLatency
            else:
                LatencyperDevice.append(ReadLatency)
                DeviceList.append(variables.actionlist[i][1][k][0])
    if len(LatencyperDevice) == 0:
        LatencyperDevice = [0]
    return(max(LatencyperDevice))

