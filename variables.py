# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 11:52:16 2021

@author: Drawings2
"""
from time import time

def init():
    global id_in_process
    id_in_process = -1
    
    #queries: list for each devices of the things they must do (dataquery,setvolt...)
    global QueryList
    QueryList = [[],[],[],[],[],[],[],[],[],[]]#(type,dat) ex:('Write',[key,parameters]) or ('Read',key)
    global close
    close = False
    global actionlist
    actionlist = [] #list of actions displayed in the box (and later executed)
    global Data
    Data = {'Time':[],'Math':[]}
    global t0
    t0 = time()
    global IsRunning
    IsRunning = False
    global ExitCurrentAction
    ExitCurrentAction = False
    global Data_image
    Data_image = None
    global ix
    ix = 0
    global iy
    iy = 0
    global Lx
    Lx = 0
    global Ly
    Ly = 0
    global ZplotText
    ZplotText = ''
    global sharedbuffer#buffer that may be used by the driver of a device, one buffer per device
    sharedbuffer = [None for k in range(10)]
    
    global path
    path = None
    
    
    # Variables for users
    global A,B,C,D,E,F
    A,B,C,D,E,F = 0,0,0,0,0,0
    
    global isPlotting
    isPlotting = False
    global is2DPlotting
    is2DPlotting = False
    
    
    
    return()