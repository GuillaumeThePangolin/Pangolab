# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'swissk.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from pyqtgraph import PlotWidget,ImageView
#import pyqtgraph.opengl as gl
import sys
from pyqtgraph import *
import pyvisa
import minimalmodbus
from time import sleep,time
import numpy as np
import csv
import os
from inspect import getsourcefile
from copy import deepcopy


import variables
variables.init()

import actionThread
import TempFileSaver
import timeEstimation
import plotWindow


#get the path of the python file
variables.path = getsourcefile(lambda:0)
while variables.path[-1] !=  "\\"  and variables.path[-1] !=  "/":
    variables.path = variables.path[:-1]

#path to s
os.chdir(variables.path)

#default path to save
pathsave = "C://Users//Drawings2//Documents//Python Scripts//datapango//"

#global max voltage for Vrampe
global maxvoltage 
maxvoltage = 100#change this value to be allowed to go to higher voltage


#modules must be in the same folder
import yoko7651
import yokogs200
import keithley
import sr830_new
import bilt_new
import cryomag4G
import ips120_new
import HP3245A
import K2000
import Agilent34420A
import Euro2404
import ls350_new
import ls331_new
import cryomag4g_new





#Devices dic // dictionnary for adding devices
DevicesDict = {"Keithley 2400":keithley.Keithley,"Bilt":bilt_new.Bilt,"Lock-in SR830":sr830_new.Sr830,'CryoMag4G':cryomag4g_new.Cryomag4G,"LS350":ls350_new.Ls350,'IPS120-10':ips120_new.Ips120,"Yokogawa GS200":yokogs200.Yokogs200,"Yokogawa 7651":yoko7651.Yoko7561,"LS331":ls331_new.Ls331,'HP3245A':HP3245A.HP3245A,'K2000':K2000.K2000,'Agilent34420':Agilent34420A.A34420A,"Euro2404":Euro2404.Euro2404}




class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowIcon(QtGui.QIcon('icon.jpg'))
        # Dialog.resize(1800, 980)
        self.graphicsView = PlotWidget(Dialog)
        self.graphicsView.setGeometry(QtCore.QRect(430, 20, 631, 471))
        self.graphicsView.setObjectName("graphicsView")
        self.label_d1 = QtWidgets.QLabel(Dialog)
        self.label_d1.setGeometry(QtCore.QRect(20, 30, 47, 13))
        self.label_d1.setObjectName("label_d1")
        self.label_d2 = QtWidgets.QLabel(Dialog)
        self.label_d2.setGeometry(QtCore.QRect(20, 70, 47, 13))
        self.label_d2.setObjectName("label_d2")
        self.label_d3 = QtWidgets.QLabel(Dialog)
        self.label_d3.setGeometry(QtCore.QRect(20, 110, 47, 13))
        self.label_d3.setObjectName("label_d3")
        self.label_d5 = QtWidgets.QLabel(Dialog)
        self.label_d5.setGeometry(QtCore.QRect(20, 190, 47, 13))
        self.label_d5.setObjectName("label_d5")
        self.label_d4 = QtWidgets.QLabel(Dialog)
        self.label_d4.setGeometry(QtCore.QRect(20, 150, 47, 13))
        self.label_d4.setObjectName("label_d4")
        self.label_d6 = QtWidgets.QLabel(Dialog)
        self.label_d6.setGeometry(QtCore.QRect(20, 230, 47, 13))
        self.label_d6.setObjectName("label_d6")
        self.GPIB_1 = QtWidgets.QLineEdit(Dialog)
        self.GPIB_1.setGeometry(QtCore.QRect(80, 30, 113, 20))
        self.GPIB_1.setObjectName("GPIB_1")
        self.GPIB_2 = QtWidgets.QLineEdit(Dialog)
        self.GPIB_2.setGeometry(QtCore.QRect(80, 70, 113, 20))
        self.GPIB_2.setObjectName("GPIB_2")
        self.GPIB_3 = QtWidgets.QLineEdit(Dialog)
        self.GPIB_3.setGeometry(QtCore.QRect(80, 110, 113, 20))
        self.GPIB_3.setObjectName("GPIB_3")
        self.GPIB_4 = QtWidgets.QLineEdit(Dialog)
        self.GPIB_4.setGeometry(QtCore.QRect(80, 150, 113, 20))
        self.GPIB_4.setObjectName("GPIB_4")
        self.GPIB_5 = QtWidgets.QLineEdit(Dialog)
        self.GPIB_5.setGeometry(QtCore.QRect(80, 190, 113, 20))
        self.GPIB_5.setObjectName("GPIB_5")
        self.GPIB_6 = QtWidgets.QLineEdit(Dialog)
        self.GPIB_6.setGeometry(QtCore.QRect(80, 230, 113, 20))
        self.GPIB_6.setObjectName("GPIB_6")
        self.GPIBBox_1 = QtWidgets.QComboBox(Dialog)
        self.GPIBBox_1.setGeometry(QtCore.QRect(220, 30, 121, 22))
        self.GPIBBox_1.setObjectName("GPIBBox_1")

        self.GPIBBox_2 = QtWidgets.QComboBox(Dialog)
        self.GPIBBox_2.setGeometry(QtCore.QRect(220, 70, 121, 22))
        self.GPIBBox_2.setObjectName("GPIBBox_2")

        self.GPIBBox_3 = QtWidgets.QComboBox(Dialog)
        self.GPIBBox_3.setGeometry(QtCore.QRect(220, 110, 121, 22))
        self.GPIBBox_3.setObjectName("GPIBBox_3")

        self.GPIBBox_4 = QtWidgets.QComboBox(Dialog)
        self.GPIBBox_4.setGeometry(QtCore.QRect(220, 150, 121, 22))
        self.GPIBBox_4.setObjectName("GPIBBox_4")

        self.GPIBBox_5 = QtWidgets.QComboBox(Dialog)
        self.GPIBBox_5.setGeometry(QtCore.QRect(220, 190, 121, 22))
        self.GPIBBox_5.setObjectName("GPIBBox_5")

        self.GPIBBox_6 = QtWidgets.QComboBox(Dialog)
        self.GPIBBox_6.setGeometry(QtCore.QRect(220, 230, 121, 22))
        self.GPIBBox_6.setObjectName("GPIBBox_6")

        self.ActionWidget = QtWidgets.QListWidget(Dialog)
        self.ActionWidget.setGeometry(QtCore.QRect(10, 500, 721, 461))
        self.ActionWidget.setObjectName("ActionWidget")
        self.ActionWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection) #enables multiselection in the action list
        self.ListActionBox = QtWidgets.QComboBox(Dialog)
        self.ListActionBox.setGeometry(QtCore.QRect(740, 850, 141, 22))
        self.ListActionBox.setObjectName("ListActionBox")
        self.AddButton = QtWidgets.QPushButton(Dialog)
        self.AddButton.setGeometry(QtCore.QRect(800, 880, 71, 23))
        self.AddButton.setObjectName("AddButton")
        self.AddVRampeButton = QtWidgets.QPushButton(Dialog)
        self.AddVRampeButton.setGeometry(QtCore.QRect(740, 770, 71, 23))
        self.AddVRampeButton.setObjectName("AddVRampeButton")
        self.AddSweep2DButton = QtWidgets.QPushButton(Dialog)
        self.AddSweep2DButton.setGeometry(QtCore.QRect(821, 770, 71, 23))
        self.AddSweep2DButton.setObjectName("AddSweep2DButton")
        self.AddSaveButton = QtWidgets.QPushButton(Dialog)
        self.AddSaveButton.setGeometry(QtCore.QRect(740, 730, 71, 23))
        self.AddSaveButton.setObjectName("AddSaveButton")
        self.AddClearButton = QtWidgets.QPushButton(Dialog)
        self.AddClearButton.setGeometry(QtCore.QRect(821, 730, 71, 23))
        self.AddClearButton.setObjectName("AddClearButton")
        self.AddIdleButton = QtWidgets.QPushButton(Dialog)
        self.AddIdleButton.setGeometry(QtCore.QRect(821, 810, 71, 23))
        self.AddIdleButton.setObjectName("AddIdleButton")
        self.AddReadButton = QtWidgets.QPushButton(Dialog)
        self.AddReadButton.setGeometry(QtCore.QRect(740, 650, 71, 23))
        self.AddReadButton.setObjectName("AddReadButton")
        self.AddWriteButton = QtWidgets.QPushButton(Dialog)
        self.AddWriteButton.setGeometry(QtCore.QRect(821, 650, 71, 23))
        self.AddWriteButton.setObjectName("AddWriteButton")
        self.SaveActionButton = QtWidgets.QPushButton(Dialog)
        self.SaveActionButton.setGeometry(QtCore.QRect(15, 965, 51, 23))
        self.SaveActionButton.setObjectName("SaveActionButton")
        self.LoadActionButton = QtWidgets.QPushButton(Dialog)
        self.LoadActionButton.setGeometry(QtCore.QRect(70, 965, 51, 23))
        self.LoadActionButton.setObjectName("LoadActionButton")
        self.RuntimeButton = QtWidgets.QPushButton(Dialog)
        self.RuntimeButton.setGeometry(QtCore.QRect(215, 965, 51, 23))
        self.RuntimeButton.setObjectName("RuntimeButton")
        self.AddMathButton = QtWidgets.QPushButton(Dialog)
        self.AddMathButton.setGeometry(QtCore.QRect(740, 690, 71, 23))
        self.AddMathButton.setObjectName("AddMathButton")
        self.AddJumpifButton = QtWidgets.QPushButton(Dialog)
        self.AddJumpifButton.setGeometry(QtCore.QRect(821, 690, 71, 23))
        self.AddJumpifButton.setObjectName("AddJumpButton")
        self.AddCustomSweepButton = QtWidgets.QPushButton(Dialog)
        self.AddCustomSweepButton.setGeometry(QtCore.QRect(740, 810, 71, 23))
        self.AddCustomSweepButton.setObjectName("AddCustomSweepButton")
        
        
        
        self.RemoveButton = QtWidgets.QPushButton(Dialog)
        self.RemoveButton.setGeometry(QtCore.QRect(800, 910, 51, 23))
        self.RemoveButton.setObjectName("RemoveButton")
        self.DupeButton = QtWidgets.QPushButton(Dialog)
        self.DupeButton.setGeometry(QtCore.QRect(740, 910, 41, 23))
        self.DupeButton.setObjectName("DupeButton")
        self.GroupMoveButton = QtWidgets.QPushButton(Dialog)
        self.GroupMoveButton.setGeometry(QtCore.QRect(740, 940, 67, 23))
        self.GroupMoveButton.setObjectName("GroupMoveButton")
        self.MoveTo = QtWidgets.QSpinBox(Dialog)
        self.MoveTo.setGeometry(QtCore.QRect(810, 940, 41, 23))
        self.MoveTo.setMinimum(0)
        self.MoveTo.setMaximum(2147483647)
        
        self.StartButton = QtWidgets.QPushButton(Dialog)
        self.StartButton.setGeometry(QtCore.QRect(1480, 840, 121, 71))
        self.StartButton.setObjectName("StartButton")
        self.StopButton = QtWidgets.QPushButton(Dialog)
        self.StopButton.setGeometry(QtCore.QRect(1630, 840, 121, 71))
        self.StopButton.setObjectName("StopButton")
        
        self.newplotButton = QtWidgets.QPushButton(Dialog)
        self.newplotButton.setGeometry(QtCore.QRect(1000, 690, 71, 23))
        self.newplotButton.setObjectName("newplot")
        
        self.XplotLabel = QtWidgets.QLabel(Dialog)
        self.XplotLabel.setGeometry(QtCore.QRect(760, 500, 21, 16))
        self.XplotLabel.setObjectName("XplotLabel")
        
        self.XplotBox = QtWidgets.QComboBox(Dialog)
        self.XplotBox.setGeometry(QtCore.QRect(780, 500, 150, 22))
        self.XplotBox.setObjectName("XplotBox")

        self.YplotBox = QtWidgets.QComboBox(Dialog)
        self.YplotBox.setGeometry(QtCore.QRect(960, 500, 150, 22))
        self.YplotBox.setObjectName("YplotBox")
        
        self.YplotBox_2 = QtWidgets.QComboBox(Dialog)
        self.YplotBox_2.setGeometry(QtCore.QRect(960, 530, 150, 22))
        self.YplotBox_2.setObjectName("YplotBox_2")

        self.YplotBox_3 = QtWidgets.QComboBox(Dialog)
        self.YplotBox_3.setGeometry(QtCore.QRect(960, 560, 150, 22))
        self.YplotBox_3.setObjectName("YplotBox_3")

        self.YplotBox_4 = QtWidgets.QComboBox(Dialog)
        self.YplotBox_4.setGeometry(QtCore.QRect(960, 590, 150, 22))
        self.YplotBox_4.setObjectName("YplotBox_4")

        self.YplotBox_5 = QtWidgets.QComboBox(Dialog)
        self.YplotBox_5.setGeometry(QtCore.QRect(960, 620, 150, 22))
        self.YplotBox_5.setObjectName("YplotBox_5")

        self.YplotBox_6 = QtWidgets.QComboBox(Dialog)
        self.YplotBox_6.setGeometry(QtCore.QRect(960, 650, 150, 22))
        self.YplotBox_6.setObjectName("YplotBox_6")
        

        self.YplotLabel = QtWidgets.QLabel(Dialog)
        self.YplotLabel.setGeometry(QtCore.QRect(940, 500, 16, 16))
        self.YplotLabel.setObjectName("YplotLabel")
        self.ZplotBox = QtWidgets.QComboBox(Dialog)
        self.ZplotBox.setGeometry(QtCore.QRect(1600, 500, 150, 22))
        self.ZplotBox.setObjectName("ZplotBox")

        self.XplotLabel_3 = QtWidgets.QLabel(Dialog)
        self.XplotLabel_3.setGeometry(QtCore.QRect(1580, 500, 47, 13))
        self.XplotLabel_3.setObjectName("XplotLabel_3")
        self.ConnectButton = QtWidgets.QPushButton(Dialog)
        self.ConnectButton.setGeometry(QtCore.QRect(220, 420, 75, 23))
        self.ConnectButton.setObjectName("ConnectButton")
        self.upButton = QtWidgets.QPushButton(Dialog)
        self.upButton.setGeometry(QtCore.QRect(860, 880, 21, 23))
        self.upButton.setObjectName("upButton")
        self.downButton = QtWidgets.QPushButton(Dialog)
        self.downButton.setGeometry(QtCore.QRect(860, 910, 21, 23))
        self.downButton.setObjectName("downButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(1480, 920, 41, 16))
        self.label.setObjectName("label")
        self.Runninglabel = QtWidgets.QLabel(Dialog)
        self.Runninglabel.setGeometry(QtCore.QRect(1520, 920, 81, 16))
        self.Runninglabel.setObjectName("Runninglabel")
        self.paramDialogButton = QtWidgets.QPushButton(Dialog)
        self.paramDialogButton.setGeometry(QtCore.QRect(740, 880, 41, 23))
        self.paramDialogButton.setObjectName("paramDialogButton")
        self.imgView = ImageView(Dialog)
        self.imgView.setGeometry(QtCore.QRect(1120, 20, 631, 471))
        self.imgView.setObjectName("imgView")
        self.GPIBBox_7 = QtWidgets.QComboBox(Dialog)
        self.GPIBBox_7.setGeometry(QtCore.QRect(220, 270, 121, 22))
        self.GPIBBox_7.setObjectName("GPIBBox_7")

        self.label_d9 = QtWidgets.QLabel(Dialog)
        self.label_d9.setGeometry(QtCore.QRect(20, 350, 47, 13))
        self.label_d9.setObjectName("label_d9")
        self.label_d8 = QtWidgets.QLabel(Dialog)
        self.label_d8.setGeometry(QtCore.QRect(20, 310, 47, 13))
        self.label_d8.setObjectName("label_d8")
        self.GPIB_10 = QtWidgets.QLineEdit(Dialog)
        self.GPIB_10.setGeometry(QtCore.QRect(80, 390, 113, 20))
        self.GPIB_10.setObjectName("GPIB_10")
        self.GPIB_7 = QtWidgets.QLineEdit(Dialog)
        self.GPIB_7.setGeometry(QtCore.QRect(80, 270, 113, 20))
        self.GPIB_7.setObjectName("GPIB_7")
        self.GPIB_9 = QtWidgets.QLineEdit(Dialog)
        self.GPIB_9.setGeometry(QtCore.QRect(80, 350, 113, 20))
        self.GPIB_9.setObjectName("GPIB_9")
        self.GPIBBox_10 = QtWidgets.QComboBox(Dialog)
        self.GPIBBox_10.setGeometry(QtCore.QRect(220, 390, 121, 22))
        self.GPIBBox_10.setObjectName("GPIBBox_10")

        self.label_d7 = QtWidgets.QLabel(Dialog)
        self.label_d7.setGeometry(QtCore.QRect(20, 270, 47, 13))
        self.label_d7.setObjectName("label_d7")
        self.label_d10 = QtWidgets.QLabel(Dialog)
        self.label_d10.setGeometry(QtCore.QRect(20, 390, 47, 13))
        self.label_d10.setObjectName("label_d10")
        self.GPIB_8 = QtWidgets.QLineEdit(Dialog)
        self.GPIB_8.setGeometry(QtCore.QRect(80, 310, 113, 20))
        self.GPIB_8.setObjectName("GPIB_8")
        self.GPIBBox_9 = QtWidgets.QComboBox(Dialog)
        self.GPIBBox_9.setGeometry(QtCore.QRect(220, 350, 121, 22))
        self.GPIBBox_9.setObjectName("GPIBBox_9")

        self.GPIBBox_8 = QtWidgets.QComboBox(Dialog)
        self.GPIBBox_8.setGeometry(QtCore.QRect(220, 310, 121, 22))
        self.GPIBBox_8.setObjectName("GPIBBox_8")

        self.labelStartFrom = QtWidgets.QLabel(Dialog)
        self.labelStartFrom.setGeometry(QtCore.QRect(1480, 810, 61, 16))
        self.labelStartFrom.setObjectName("labelStartFrom")
        self.startFromBox = QtWidgets.QSpinBox(Dialog)
        self.startFromBox.setGeometry(QtCore.QRect(1540, 810, 42, 22))
        self.startFromBox.setObjectName("startFromBox")
        self.startFromBox.setMinimum(0)
        self.startFromBox.setMaximum(1000000)
        
        


        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(930, 850, 131, 71))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.measLabel = QtWidgets.QLabel(self.frame)
        self.measLabel.setGeometry(QtCore.QRect(10, 40, 111, 16))
        self.measLabel.setObjectName("measLabel")
        self.measBox = QtWidgets.QComboBox(self.frame)
        self.measBox.setGeometry(QtCore.QRect(10, 10, 69, 22))
        self.measBox.setObjectName("measBox")
        self.measBox.addItem("")
        self.measBox.addItem("")
        self.measBox.addItem("")
        self.measBox.addItem("")
        self.measBox.addItem("")
        self.measBox.addItem("")
        self.measBox.addItem("")
        self.measBox.addItem("")
        self.measBox.addItem("")
        self.measBox.addItem("")

        self.NextButton = QtWidgets.QPushButton(Dialog)
        self.NextButton.setGeometry(QtCore.QRect(1630, 922, 121, 21))
        self.NextButton.setObjectName("NextButton")
        self.NextButton.setText('Next')

        self.init_ui()
        self.init_variables()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PANGOLAB v0.6.4 by Guillaume BERNARD"))
        self.label_d1.setText(_translate("Dialog", "Device 1:"))
        self.label_d2.setText(_translate("Dialog", "Device 2:"))
        self.label_d3.setText(_translate("Dialog", "Device 3:"))
        self.label_d5.setText(_translate("Dialog", "Device 5:"))
        self.label_d4.setText(_translate("Dialog", "Device 4:"))
        self.label_d6.setText(_translate("Dialog", "Device 6:"))
        self.AddButton.setText(_translate("Dialog", "Add"))
        self.AddVRampeButton.setText(_translate("Dialog", "VRampe"))
        self.AddSweep2DButton.setText(_translate("Dialog", "Sweep2D"))
        self.AddSaveButton.setText(_translate("Dialog", "SaveData"))
        self.AddClearButton.setText(_translate("Dialog", "ClearData"))
        self.AddIdleButton.setText(_translate("Dialog", "Idle"))
        self.AddWriteButton.setText(_translate("Dialog", "Write"))
        self.AddReadButton.setText(_translate("Dialog", "Read"))
        self.RemoveButton.setText(_translate("Dialog", "Remove"))
        self.DupeButton.setText(_translate("Dialog", "Dupe"))
        self.SaveActionButton.setText(_translate("Dialog","Save"))
        self.LoadActionButton.setText(_translate("Dialog","Load"))
        self.RuntimeButton.setText(_translate("Dialog","Runtime"))
        self.AddMathButton.setText(_translate("Dialog", "Math"))
        self.AddJumpifButton.setText(_translate("Dialog", "JumpIf"))
        self.AddCustomSweepButton.setText(_translate("Dialog", "CustomSweep"))
        self.GroupMoveButton.setText(_translate("Dialog", "Group Move"))
        self.StartButton.setText(_translate("Dialog", "Start"))
        self.StopButton.setText(_translate("Dialog", "Stop"))
        self.XplotLabel.setText(_translate("Dialog", "X:"))
        self.YplotLabel.setText(_translate("Dialog", "Y:"))
        self.newplotButton.setText(_translate("Dialog", "new plot"))

        self.XplotLabel_3.setText(_translate("Dialog", "Z:"))
        self.ConnectButton.setText(_translate("Dialog", "Connect"))
        self.upButton.setText(_translate("Dialog", "↑"))
        self.downButton.setText(_translate("Dialog", "↓"))
        self.label.setText(_translate("Dialog", "Status:"))
        self.Runninglabel.setText(_translate("Dialog", "Stopped"))
        self.paramDialogButton.setText(_translate("Dialog", "Edit"))
        self.labelStartFrom.setText(_translate("Dialog", "Start from:"))
        self.measLabel.setText(_translate("Dialog", "0"))
        self.measBox.setItemText(0, _translate("Dialog", "1"))
        self.measBox.setItemText(1, _translate("Dialog", "2"))
        self.measBox.setItemText(2, _translate("Dialog", "3"))
        self.measBox.setItemText(3, _translate("Dialog", "4"))
        self.measBox.setItemText(4, _translate("Dialog", "5"))
        self.measBox.setItemText(5, _translate("Dialog", "6"))
        self.measBox.setItemText(6, _translate("Dialog", "7"))
        self.measBox.setItemText(7, _translate("Dialog", "8"))
        self.measBox.setItemText(8, _translate("Dialog", "9"))
        self.measBox.setItemText(9, _translate("Dialog", "10"))

        self.label_d9.setText(_translate("Dialog", "Device 9:"))
        self.label_d8.setText(_translate("Dialog", "Device 8:"))

        self.label_d7.setText(_translate("Dialog", "Device 7:"))
        self.label_d10.setText(_translate("Dialog", "Device 10:"))


    def init_ui(self):
        Dialog.resize(1800, 980)
        # Dialog.showMaximized()
        #def new button


        #disable automatic button selection
        self.AddButton.setAutoDefault(False)
        self.AddVRampeButton.setAutoDefault(False)
        self.AddSaveButton.setAutoDefault(False)
        self.AddClearButton.setAutoDefault(False)
        self.AddIdleButton.setAutoDefault(False)
        self.AddWriteButton.setAutoDefault(False)
        self.AddReadButton.setAutoDefault(False)
        self.RemoveButton.setAutoDefault(False)
        self.DupeButton.setAutoDefault(False)
        self.GroupMoveButton.setAutoDefault(False)
        self.StartButton.setAutoDefault(False)
        self.StopButton.setAutoDefault(False)
        self.paramDialogButton.setAutoDefault(False)
        self.ConnectButton.setAutoDefault(False)
        self.NextButton.setAutoDefault(False)
        self.upButton.setAutoDefault(False)
        self.downButton.setAutoDefault(False)
        self.SaveActionButton.setAutoDefault(False)
        self.LoadActionButton.setAutoDefault(False)
        self.RuntimeButton.setAutoDefault(False)
        self.AddMathButton.setAutoDefault(False)
        self.AddJumpifButton.setAutoDefault(False)
        self.AddSweep2DButton.setAutoDefault(False)
        self.AddCustomSweepButton.setAutoDefault(False)
        self.newplotButton.setAutoDefault(False)
        

        self.imgView.ui.roiBtn.setAutoDefault(False)
        self.imgView.ui.menuBtn.setAutoDefault(False)


        #add actions to listactionbox
        #self.ListActionBox.addItem('SetDirectory')
        self.ListActionBox.addItem('SaveData')
        self.ListActionBox.addItem('ClearData')
        self.ListActionBox.addItem('VRampe')
        self.ListActionBox.addItem('Write')
        self.ListActionBox.addItem('Idle')
        self.ListActionBox.addItem('Sweep2D')
        self.ListActionBox.addItem('Read')
        self.ListActionBox.addItem('Math')
        self.ListActionBox.addItem('JumpIf')
        self.ListActionBox.addItem('CustomSweep')
        self.ListActionBox.addItem('Irampe')
        self.ListActionBox.addItem('SetTemp')

        #connect buttons
        self.paramDialogButton.clicked.connect(self.LaunchCustomDialog)
        self.ConnectButton.clicked.connect(self.ConnectDevices)
        self.AddButton.clicked.connect(self.AddAction)
        self.AddVRampeButton.clicked.connect(self.AddVrampe)
        self.AddSweep2DButton.clicked.connect(self.AddSweep2D)
        self.AddSaveButton.clicked.connect(self.AddSaveData)
        self.AddClearButton.clicked.connect(self.AddClearData)
        self.AddIdleButton.clicked.connect(self.AddIdle)
        self.AddWriteButton.clicked.connect(self.AddWrite)
        self.AddReadButton.clicked.connect(self.AddRead)
        self.RemoveButton.clicked.connect(self.RemoveAction)
        self.DupeButton.clicked.connect(self.DupeAction)
        self.GroupMoveButton.clicked.connect(self.GroupMove)
        self.StartButton.clicked.connect(self.start)
        self.StopButton.clicked.connect(self.stop)
        self.NextButton.clicked.connect(self.next)
        self.upButton.clicked.connect(self.upAction)
        self.downButton.clicked.connect(self.downAction)
        self.ActionWidget.doubleClicked.connect(self.LaunchCustomDialog)
        self.SaveActionButton.clicked.connect(self.SaveAction)
        self.LoadActionButton.clicked.connect(self.LoadAction)
        self.RuntimeButton.clicked.connect(self.Runtime)
        self.AddMathButton.clicked.connect(self.AddMath)
        self.AddJumpifButton.clicked.connect(self.AddJumpif)
        self.AddCustomSweepButton.clicked.connect(self.AddCustomSweep)
        self.newplotButton.clicked.connect(self.newPlotWindow)
        
        self.ZplotBox.currentIndexChanged.connect(self.Zchanged)

        #default gpib id
        self.GPIB_1.setText('ASRL23::INSTR')
        self.GPIB_2.setText('GPIB1::09::INSTR')
        self.GPIB_3.setText('GPIB1::10::INSTR') 
        self.GPIB_4.setText('GPIB1::11::INSTR') 
        self.GPIB_5.setText('GPIB1::28::INSTR') 
        self.GPIB_6.setText('GPIB1::26::INSTR')
        self.GPIB_7.setText('GPIB0::00::INSTR')
        self.GPIB_8.setText('GPIB0::00::INSTR')
        self.GPIB_9.setText('GPIB0::00::INSTR')
        self.GPIB_10.setText('GPIB0::00::INSTR')

        self.frame.setStyleSheet('border:1px solid rgb(0, 0, 0);')

        self.imgView.ui.roiPlot.showAxis('left')

        Dialog.setWindowIcon(QtGui.QIcon('icon.jpg'))




    def init_variables(self):
        Dialog.closeEvent = self.closeEvent

        self.rm = pyvisa.ResourceManager()#resource manag for gpib interface
        
        #self.PlotAxes()
        #
        self.YplotList = [self.YplotBox,self.YplotBox_2,self.YplotBox_3,self.YplotBox_4,self.YplotBox_5,self.YplotBox_6]
        self.colors = ('white','green','red', 'cyan', 'magenta', 'yellow', 'blue')
        self.colors_rgb = ((255,255,255),(0,255,0),(255,0,0),(0,255,255),(255,0,255),(255,255,0))
        self.YplotBox_2.setStyleSheet("background-color: " + self.colors[1])
        self.YplotBox_3.setStyleSheet("background-color: " + self.colors[2])
        self.YplotBox_4.setStyleSheet("background-color: " + self.colors[3])
        self.YplotBox_5.setStyleSheet("background-color: " + self.colors[4])
        self.YplotBox_6.setStyleSheet("background-color: " + self.colors[5])
        
        self.current_param = None #parametres de l'item qui va etre ajoute


        self.connectedDevicesInst = [None for k in range(10)]#inst for each device

        variables.id_in_process = -1 #number of the action running
        self.id_temp = 0
        variables.IsRunning,variables.ExitCurrentAction = False,False
        
        self.plotWindowlist = []
        self.PlotTimer = QtCore.QTimer() # timer for the plot
        self.PlotTimer.timeout.connect(self.PlotData)
        self.PlotTimer.start(100)


        self.StatusTimer = QtCore.QTimer() #timer for the label under the start button
        self.StatusTimer.timeout.connect(self.UpdateStatus)
        self.StatusTimer.start(50)
        
        self.SharedBufferTimer = QtCore.QTimer()
        self.SharedBufferTimer.timeout.connect(self.SharedBufferUpdate)
        self.SharedBufferTimer.start(100)
        
        self.TempFileTimer = QtCore.QTimer()
        self.TempFileTimer.timeout.connect(TempFileSaver.SaveTemp)
        self.TempFileTimer.start(int(3600*1e3))#timer in ms
        

        self.connected_devices_list = [None for k in range(10)]
        self.ReadKeys,self.WriteKeys = [None for k in range(10)],[None for k in range(10)]
        self.WritePatterns = [{} for k in range(10)]
        
        variables.ZplotText = self.ZplotBox.currentText()
        
        self.actionThread = QtCore.QThread()
        self.actionObject = actionThread.Action(self.Plot2D)
        self.actionObject.moveToThread(self.actionThread)
        self.actionThread.started.connect(self.actionObject.run)
        self.actionThread.start()
        self.ThreadList = [QtCore.QThread() for k in range(10)]#list of threads
        self.ThreadObjList = [None for k in range(10)]#list of object (Worker class) for each thread

        


        #Load items gpib boxes
        GPIBBox = [self.GPIBBox_1,self.GPIBBox_2,self.GPIBBox_3,self.GPIBBox_4,self.GPIBBox_5,self.GPIBBox_6,self.GPIBBox_7,self.GPIBBox_8,self.GPIBBox_9,self.GPIBBox_10]
        for box in GPIBBox:
            box.addItems(DevicesDict)


    def closeEvent(self,event):#all threads must be closed when the program is closed
        if self.verify_by_user():
            event.accept()
            self.PlotTimer.stop()
            self.StatusTimer.stop()
            self.TempFileTimer.stop()
            self.closeAllThread()
            for window in self.plotWindowlist:
                window.close()
        else:
            event.ignore()
            
        # self.closeAllThread()

    def closeAllThread(self):#...
        variables.close = True
        self.actionThread.exit()
        self.actionObject = None
        for k in range(len(self.ThreadList)):
                self.ThreadList[k].exit()
                self.ThreadObjList[k] = None




#Connect

    def ConnectDevices(self):#handles the connection to every devices (create/connect the threads), called when the 'connect' button is pressed
        GPIBtext = [self.GPIB_1,self.GPIB_2,self.GPIB_3,self.GPIB_4,self.GPIB_5,self.GPIB_6,self.GPIB_7,self.GPIB_8,self.GPIB_9,self.GPIB_10]
        GPIBBox = [self.GPIBBox_1,self.GPIBBox_2,self.GPIBBox_3,self.GPIBBox_4,self.GPIBBox_5,self.GPIBBox_6,self.GPIBBox_7,self.GPIBBox_8,self.GPIBBox_9,self.GPIBBox_10]
        GPIBlabel = [self.label_d1,self.label_d2,self.label_d3,self.label_d4,self.label_d5,self.label_d6,self.label_d7,self.label_d8,self.label_d9,self.label_d10]
        for k in range(10):
            if GPIBtext[k].text() != '' and GPIBtext[k].text() != 'GPIB0::00::INSTR' and not self.ThreadObjList[k]:
                try:
                    if 'GPIB' in GPIBtext[k].text() or '::' in GPIBtext[k].text():
                        inst = self.rm.open_resource(GPIBtext[k].text())
                    elif 'COM' in GPIBtext[k].text():
                        COM,adr = GPIBtext[k].text().split(':')
                        adress = int(adr)
                        inst = minimalmodbus.Instrument(COM,adress)
                    self.connectedDevicesInst[k] = self.BoxtoModule(inst,GPIBBox[k].currentText())
                    keys = self.connectedDevicesInst[k].data_info(k+1)
                    for key in keys:
                        variables.Data[key] = []
                    self.ReadKeys[k],self.WriteKeys[k] = self.connectedDevicesInst[k].read_info(k+1),self.connectedDevicesInst[k].write_info(k+1)
                    for writeKey in self.WriteKeys[k]:
                        self.WritePatterns[k][writeKey] = self.connectedDevicesInst[k].write_pattern(k+1,writeKey)
    
                    self.ThreadObjList[k] = Worker(k,self.connectedDevicesInst[k])
                    #╧self.ThreadObjList[k].datquery.connect(self.DataThread)
                    self.ThreadObjList[k].moveToThread(self.ThreadList[k])
                    self.ThreadList[k].started.connect(self.ThreadObjList[k].run)
                    self.ThreadList[k].start()
                    GPIBlabel[k].setStyleSheet("background-color: green")
                    
                    self.connected_devices_list[k] = str(k+1) + '_' + GPIBBox[k].currentText()
                except Exception as e:
                    print(e)
                    self.MessageDialogue('Could not connect to ' + str(GPIBtext[k].text()))
                    self.connectedDevicesInst[k] = None
                    self.ThreadObjList[k] = None
                    self.ThreadList[k].exit()
                    GPIBlabel[k].setStyleSheet("background-color: red")
                    
                    self.connected_devices_list[k],self.WritePatterns[k] = None,{}
                    
        
        self.XplotBox.clear()
        self.XplotBox.addItems(list(variables.Data))
        for box in self.YplotList:
            box.clear()
            box.addItems(['None']+list(variables.Data))
        self.ZplotBox.addItems(['None']+list(variables.Data))
        


    def BoxtoModule(self,inst,dev):#links the name to the class of the device
        global DevicesDict
        return(DevicesDict[dev](inst))





#Dialogs
#Each action has its own dialog
#there is a function that will display the dialog and one that will be executed when closed and save the data
#each dialog function has a part where it loads existing data

    def isADeviceConnected(self):
        for x in self.connected_devices_list:
            if x != None:
                return(True)
        return(False)


    def LaunchCustomDialog(self):#connected to the edit button
        if len(variables.actionlist) > 0:
            if not self.isADeviceConnected():
                self.MessageDialogue('No device connected')
                return()
            if variables.actionlist[self.ActionWidget.currentRow()][0] == 'SaveData':
                self.SaveDataDialog()
            elif variables.actionlist[self.ActionWidget.currentRow()][0] == 'ClearData':
                None #rien à afficher
            elif variables.actionlist[self.ActionWidget.currentRow()][0] == 'VRampe':
                self.VrampeDialog()
            elif variables.actionlist[self.ActionWidget.currentRow()][0] == 'Write':
                self.WriteDialog()
            elif variables.actionlist[self.ActionWidget.currentRow()][0] == 'Idle':
                self.IdleDialog()
            elif variables.actionlist[self.ActionWidget.currentRow()][0] == 'Read':
                self.ReadDialog()
            elif variables.actionlist[self.ActionWidget.currentRow()][0] == 'Sweep2D':
                self.Vrampe2DDialog()
            elif variables.actionlist[self.ActionWidget.currentRow()][0] == 'Math':
                self.MathDialog()
            elif variables.actionlist[self.ActionWidget.currentRow()][0] == 'JumpIf':
                self.JumpIfDialog()
            elif variables.actionlist[self.ActionWidget.currentRow()][0] == 'CustomSweep':
                self.CustomSweepDialog()
            elif variables.actionlist[self.ActionWidget.currentRow()][0] == 'Irampe':
                self.IrampeDialog()
            elif variables.actionlist[self.ActionWidget.currentRow()][0] == 'SetTemp':
                self.setTemp()
        return()


    def MessageDialogue(self,m):#a generic dialogue used to display connection errors
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(m)
        msg.setWindowTitle("MessageBox")
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        msg.exec()
        return()

    def SaveDataDialog(self):
        pdialog = QtGui.QDialog()
        pdialog.resize(500,170)
        self.label = QtWidgets.QLabel('File Directory:',pdialog)
        self.SaveD = QtWidgets.QLineEdit(pdialog)
        self.SaveD.setGeometry(QtCore.QRect(1, 15, 411, 23))
        self.label2 = QtWidgets.QLabel('Filename:',pdialog)
        self.label2.setGeometry(QtCore.QRect(1, 35, 411, 23))
        self.SaveN = QtWidgets.QLineEdit(pdialog)
        self.SaveN.setGeometry(QtCore.QRect(1, 55, 411, 23))
        self.label3 = QtWidgets.QLabel('Email adress:',pdialog)
        self.label3.setGeometry(QtCore.QRect(1, 75, 411, 23))
        self.Mail = QtWidgets.QLineEdit(pdialog)
        self.Mail.setGeometry(QtCore.QRect(1, 95, 411, 23))
        self.label4 = QtWidgets.QLabel('Send mail',pdialog)
        self.label4.setGeometry(QtCore.QRect(1, 117, 411, 23))
        self.MailCheck = QtWidgets.QCheckBox(pdialog)
        self.MailCheck.setGeometry(QtCore.QRect(71, 120, 411, 23))
        self.label5 = QtWidgets.QLabel('Attach file',pdialog)
        self.label5.setGeometry(QtCore.QRect(1, 137, 411, 23))
        self.AttachCheck = QtWidgets.QCheckBox(pdialog)
        self.AttachCheck.setGeometry(QtCore.QRect(71, 140, 411, 23))
        self.dirButton = QtWidgets.QPushButton(pdialog)
        self.dirButton.setGeometry(QtCore.QRect(415, 15, 62, 22))
        self.dirButton.setObjectName("dirButton")
        self.dirButton.setText('📁')
        self.dirButton.setAutoDefault(False)
        self.dirButton.clicked.connect(self.SaveDataDir)
        pdialog.closeEvent = self.SaveDataEvent
        #load data into window
        if type(variables.actionlist[self.ActionWidget.currentRow()][1]) != type(None):
            self.SaveD.setText(variables.actionlist[self.ActionWidget.currentRow()][1][0])
            self.SaveN.setText(variables.actionlist[self.ActionWidget.currentRow()][1][1])
        else:
            self.SaveD.setText(pathsave)
            self.SaveN.setText('afile.txt')
        pdialog.exec_()
        
    def SaveDataDir(self):
        f = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', pathsave)[0]
        fname = f.split('/')[-1]
        fdir = f[:-len(fname)]
        self.SaveD.setText(fdir)
        self.SaveN.setText(fname)
        return()

    def SaveDataEvent(self,event):
        self.current_param = [self.SaveD.text(),self.SaveN.text(),self.Mail.text(),self.MailCheck.isChecked(),self.AttachCheck.isChecked()]
        variables.actionlist[self.ActionWidget.currentRow()][1] = self.current_param
        self.UpdateDisplay()
        
    

    def VrampeDialog(self):
        self.sweepForm = QtGui.QDialog()
        self.sweepForm.resize(420, 222)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.sweepForm)
        self.doubleSpinBox.setGeometry(QtCore.QRect(120, 70, 62, 22))
        # self.doubleSpinBox.setMinimum(-float('inf'))
        # self.doubleSpinBox.setMaximum(float('inf'))
        self.doubleSpinBox.setMinimum(-float(maxvoltage))
        self.doubleSpinBox.setMaximum(float(maxvoltage))
        self.doubleSpinBox.setDecimals(6)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.sweepForm)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(220, 70, 62, 22))
        # self.doubleSpinBox_2.setMinimum(-float('inf'))
        # self.doubleSpinBox_2.setMaximum(float('inf'))
        self.doubleSpinBox_2.setMinimum(-float(maxvoltage))
        self.doubleSpinBox_2.setMaximum(float(maxvoltage))
        self.doubleSpinBox_2.setDecimals(6)
        self.spinBox = QtWidgets.QSpinBox(self.sweepForm)
        self.spinBox.setGeometry(QtCore.QRect(120, 130, 42, 22))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1000000)
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self.sweepForm)
        self.doubleSpinBox_3.setGeometry(QtCore.QRect(300, 130, 62, 22))
        self.doubleSpinBox_3.setMinimum(100)
        self.doubleSpinBox_3.setMaximum(1000000)
        
        self.inbetweenSpinBox = QtWidgets.QDoubleSpinBox(self.sweepForm)
        self.inbetweenSpinBox.setGeometry(QtCore.QRect(220, 180, 62, 22))
        self.inbetweenSpinBox.setDecimals(6)
        self.inbetweenSpinBox.setValue(.1)
        
        
        self.deviceBox = QtWidgets.QComboBox(self.sweepForm)
        self.deviceBox.setGeometry(QtCore.QRect(10, 20, 169, 22))
        self.deviceBox.addItems(self.connected_devices_list)
        
        self.writekeysBox = QtWidgets.QComboBox(self.sweepForm)
        self.writekeysBox.setGeometry(QtCore.QRect(180, 20, 169, 22))
        self.writekeysBox.addItems(self.WriteKeys[int(self.deviceBox.currentText().split('_')[0]) - 1])
        self.deviceBox.currentIndexChanged.connect(self.UpdateWriteDialog_key)
                

        self.label = QtWidgets.QLabel(self.sweepForm)
        self.label.setGeometry(QtCore.QRect(120, 50, 47, 13))
        self.label.setText('Vstart (V)')
        self.label_2 = QtWidgets.QLabel(self.sweepForm)
        self.label_2.setGeometry(QtCore.QRect(220, 50, 47, 13))
        self.label_2.setText('Vend (V)')
        self.lineEdit = QtWidgets.QLineEdit(self.sweepForm)
        self.lineEdit.setGeometry(QtCore.QRect(10, 130, 81, 20))
        self.lineEdit.setText('0')
        self.label_3 = QtWidgets.QLabel(self.sweepForm)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 147, 13))
        self.label_3.setText("Sweep ('inf' = infinite)")
        self.label_4 = QtWidgets.QLabel(self.sweepForm)
        self.label_4.setGeometry(QtCore.QRect(300, 110, 57, 13))
        self.label_4.setText('Delay (ms)')
        self.label_5 = QtWidgets.QLabel(self.sweepForm)
        self.label_5.setGeometry(QtCore.QRect(120, 110, 81, 16))
        self.label_5.setText('Number of Points')
        self.label_6 = QtWidgets.QLabel(self.sweepForm)
        self.label_6.setGeometry(QtCore.QRect(220, 110, 57, 13))
        self.label_6.setText('Step (V)')
        self.label_7 = QtWidgets.QLabel(self.sweepForm)
        self.label_7.setGeometry(QtCore.QRect(220, 160, 57, 13))
        self.label_7.setText('large Step')
        self.SwapButton = QtWidgets.QPushButton(self.sweepForm)
        self.SwapButton.setGeometry(QtCore.QRect(300, 70, 62, 22))
        self.SwapButton.setObjectName("SwapButton")
        self.SwapButton.setText('Swap')
        self.SwapButton.setAutoDefault(False)
        self.SwapButton.clicked.connect(self.Swap)
        self.doubleSpinBox_4 = QtWidgets.QDoubleSpinBox(self.sweepForm)
        self.doubleSpinBox_4.setGeometry(QtCore.QRect(220, 130, 62, 22))
        self.doubleSpinBox_4.setMinimum(-float('inf'))
        self.doubleSpinBox_4.setMaximum(float('inf'))
        self.doubleSpinBox_4.setDecimals(6)
        
        self.nextButton = QtWidgets.QPushButton(self.sweepForm)
        self.nextButton.setGeometry(QtCore.QRect(300, 160, 102, 42))
        self.nextButton.setText('Next')
        self.nextButton.setAutoDefault(False)
        self.nextButton.clicked.connect(self.nextReadSweep)
            
        #load data
        if len(variables.actionlist[self.ActionWidget.currentRow()])>2 and type(variables.actionlist[self.ActionWidget.currentRow()][2]) != type(None):
            dat2load = variables.actionlist[self.ActionWidget.currentRow()][2]
            index = self.deviceBox.findText(dat2load[0], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.deviceBox.setCurrentIndex(index)
                index = self.writekeysBox.findText(dat2load[1], QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.writekeysBox.setCurrentIndex(index)
            self.doubleSpinBox.setValue(dat2load[2])
            self.doubleSpinBox_2.setValue(dat2load[3])
            self.spinBox.setValue(dat2load[4])
            self.doubleSpinBox_3.setValue(dat2load[5])
            self.lineEdit.setText(dat2load[6])
            self.inbetweenSpinBox.setValue(dat2load[7])
        self.sweepForm.closeEvent = self.VerifStepVrampe
        self.sweepForm.exec_()
        
    # def nextReadSweep(self):
    #     self.sweepForm.close()
    #     self.ReadDialog()
    #     #self.readForm.closeEvent = self.readSweepEvent
    
        
    def VerifStepVrampe(self,event):
        Form = QtGui.QDialog()
        Form.resize(100, 50)
        if self.doubleSpinBox_4.value()!=0 :
            self.spinBox.setValue(int(abs(self.doubleSpinBox.value()-self.doubleSpinBox_2.value())/self.doubleSpinBox_4.value())+1)
        if self.spinBox.value()-1!=0 :
            self.doubleSpinBox_4.setValue(abs(self.doubleSpinBox.value()-self.doubleSpinBox_2.value())/(self.spinBox.value()-1))
        step = None
        if self.spinBox.value()-1 !=0:
            step = abs(self.doubleSpinBox.value()-self.doubleSpinBox_2.value())/(self.spinBox.value()-1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 0, 60, 13))
        self.label.setText('Step size (V)')
        self.label_1 = QtWidgets.QLabel(Form)
        self.label_1.setGeometry(QtCore.QRect(50, 20, 47, 13))
        self.label_1.setText(str(step))
        Form.closeEvent = self.VrampeEvent
        Form.exec_()
        
        
    def VrampeEvent(self,event):
        self.current_param = [self.deviceBox.currentText(),self.writekeysBox.currentText(),self.doubleSpinBox.value(),self.doubleSpinBox_2.value(),self.spinBox.value(),self.doubleSpinBox_3.value(),self.lineEdit.text(),self.inbetweenSpinBox.value()] #id,key,vstar,Vend,N,delay,sweep,large step at the beginning
        if len(variables.actionlist[self.ActionWidget.currentRow()]) == 3:
            variables.actionlist[self.ActionWidget.currentRow()][2] = self.current_param
        else:
            variables.actionlist[self.ActionWidget.currentRow()].append(self.current_param)
        self.UpdateDisplay()
    
    
    def IrampeDialog(self):
        self.sweepForm = QtGui.QDialog()
        self.sweepForm.resize(420, 222)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.sweepForm)
        self.doubleSpinBox.setGeometry(QtCore.QRect(120, 70, 62, 22))
        self.doubleSpinBox.setMinimum(-float('inf'))
        self.doubleSpinBox.setMaximum(float('inf'))
        self.doubleSpinBox.setMinimum(-float(maxvoltage))
        self.doubleSpinBox.setMaximum(float(maxvoltage))
        self.doubleSpinBox.setDecimals(6)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.sweepForm)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(220, 70, 62, 22))
        self.doubleSpinBox_2.setMinimum(-float('inf'))
        self.doubleSpinBox_2.setMaximum(float('inf'))
        self.doubleSpinBox_2.setMinimum(-float(maxvoltage))
        self.doubleSpinBox_2.setMaximum(float(maxvoltage))
        self.doubleSpinBox_2.setDecimals(6)
        # self.spinBox = QtWidgets.QSpinBox(self.sweepForm)
        # self.spinBox.setGeometry(QtCore.QRect(120, 130, 42, 22))
        # self.spinBox.setMinimum(1)
        # self.spinBox.setMaximum(1000000)
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self.sweepForm)
        self.doubleSpinBox_3.setGeometry(QtCore.QRect(300, 130, 62, 22))
        self.doubleSpinBox_3.setMinimum(100)
        self.doubleSpinBox_3.setMaximum(1000000)
        
        # self.inbetweenSpinBox = QtWidgets.QDoubleSpinBox(self.sweepForm)
        # self.inbetweenSpinBox.setGeometry(QtCore.QRect(220, 180, 62, 22))
        # self.inbetweenSpinBox.setDecimals(6)
        # self.inbetweenSpinBox.setValue(.1)
        
        
        self.deviceBox = QtWidgets.QComboBox(self.sweepForm)
        self.deviceBox.setGeometry(QtCore.QRect(10, 20, 169, 22))
        self.deviceBox.addItems(self.connected_devices_list)
        
        self.writekeysBox = QtWidgets.QComboBox(self.sweepForm)
        self.writekeysBox.setGeometry(QtCore.QRect(180, 20, 169, 22))
        self.writekeysBox.addItems(self.WriteKeys[int(self.deviceBox.currentText().split('_')[0]) - 1])
        self.deviceBox.currentIndexChanged.connect(self.UpdateWriteDialog_key)
                

        self.label = QtWidgets.QLabel(self.sweepForm)
        self.label.setGeometry(QtCore.QRect(120, 50, 47, 13))
        self.label.setText('Vstart (V)')
        self.label_2 = QtWidgets.QLabel(self.sweepForm)
        self.label_2.setGeometry(QtCore.QRect(220, 50, 47, 13))
        self.label_2.setText('Vend (V)')
        self.lineEdit = QtWidgets.QLineEdit(self.sweepForm)
        self.lineEdit.setGeometry(QtCore.QRect(10, 130, 81, 20))
        self.lineEdit.setText('0')
        self.label_3 = QtWidgets.QLabel(self.sweepForm)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 147, 13))
        self.label_3.setText("Sweep ('inf' = infinite)")
        self.label_4 = QtWidgets.QLabel(self.sweepForm)
        self.label_4.setGeometry(QtCore.QRect(300, 110, 57, 13))
        self.label_4.setText('Delay (ms)')
        # self.label_5 = QtWidgets.QLabel(self.sweepForm)
        # self.label_5.setGeometry(QtCore.QRect(120, 110, 81, 16))
        # self.label_5.setText('Number of Points')
        # self.label_6 = QtWidgets.QLabel(self.sweepForm)
        # self.label_6.setGeometry(QtCore.QRect(220, 110, 57, 13))
        # self.label_6.setText('Step (V)')
        # self.label_7 = QtWidgets.QLabel(self.sweepForm)
        # self.label_7.setGeometry(QtCore.QRect(220, 160, 57, 13))
        # self.label_7.setText('large Step')
        self.SwapButton = QtWidgets.QPushButton(self.sweepForm)
        self.SwapButton.setGeometry(QtCore.QRect(300, 70, 62, 22))
        self.SwapButton.setObjectName("SwapButton")
        self.SwapButton.setText('Swap')
        self.SwapButton.setAutoDefault(False)
        self.SwapButton.clicked.connect(self.Swap)
        # self.doubleSpinBox_4 = QtWidgets.QDoubleSpinBox(self.sweepForm)
        # self.doubleSpinBox_4.setGeometry(QtCore.QRect(220, 130, 62, 22))
        # self.doubleSpinBox_4.setMinimum(-float('inf'))
        # self.doubleSpinBox_4.setMaximum(float('inf'))
        # self.doubleSpinBox_4.setDecimals(6)
        
        self.nextButton = QtWidgets.QPushButton(self.sweepForm)
        self.nextButton.setGeometry(QtCore.QRect(300, 160, 102, 42))
        self.nextButton.setText('Next')
        self.nextButton.setAutoDefault(False)
        self.nextButton.clicked.connect(self.nextReadSweep)
            
        #load data
        if len(variables.actionlist[self.ActionWidget.currentRow()])>2 and type(variables.actionlist[self.ActionWidget.currentRow()][2]) != type(None):
            dat2load = variables.actionlist[self.ActionWidget.currentRow()][2]
            index = self.deviceBox.findText(dat2load[0], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.deviceBox.setCurrentIndex(index)
                index = self.writekeysBox.findText(dat2load[1], QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.writekeysBox.setCurrentIndex(index)
            self.doubleSpinBox.setValue(dat2load[2])
            self.doubleSpinBox_2.setValue(dat2load[3])
            # self.spinBox.setValue(dat2load[4])
            self.doubleSpinBox_3.setValue(dat2load[4])
            self.lineEdit.setText(dat2load[5])
            # self.inbetweenSpinBox.setValue(dat2load[7])
        self.sweepForm.closeEvent = self.IrampeEvent
        self.sweepForm.exec_()
        
    # def nextReadSweep(self):
    #     self.sweepForm.close()
    #     self.ReadDialog()
    #     #self.readForm.closeEvent = self.readSweepEvent
    
        
    # def VerifStepIrampe(self,event):
    #     Form = QtGui.QDialog()
    #     Form.resize(100, 50)
    #     if self.doubleSpinBox_4.value()!=0 :
    #         self.spinBox.setValue(int(abs(self.doubleSpinBox.value()-self.doubleSpinBox_2.value())/self.doubleSpinBox_4.value())+1)
    #     if self.spinBox.value()-1!=0 :
    #         self.doubleSpinBox_4.setValue(abs(self.doubleSpinBox.value()-self.doubleSpinBox_2.value())/(self.spinBox.value()-1))
    #     step = None
    #     if self.spinBox.value()-1 !=0:
    #         step = abs(self.doubleSpinBox.value()-self.doubleSpinBox_2.value())/(self.spinBox.value()-1)
    #     self.label = QtWidgets.QLabel(Form)
    #     self.label.setGeometry(QtCore.QRect(30, 0, 60, 13))
    #     self.label.setText('Step size (V)')
    #     self.label_1 = QtWidgets.QLabel(Form)
    #     self.label_1.setGeometry(QtCore.QRect(50, 20, 47, 13))
    #     self.label_1.setText(str(step))
    #     Form.closeEvent = self.IrampeEvent
    #     Form.exec_()    
        
    def IrampeEvent(self,event):
        self.current_param = [self.deviceBox.currentText(),self.writekeysBox.currentText(),self.doubleSpinBox.value(),self.doubleSpinBox_2.value(),self.doubleSpinBox_3.value(),self.lineEdit.text()] #id,key,vstar,Vend,N,delay,sweep,large step at the beginning
        if len(variables.actionlist[self.ActionWidget.currentRow()]) == 3:
            variables.actionlist[self.ActionWidget.currentRow()][2] = self.current_param
        else:
            variables.actionlist[self.ActionWidget.currentRow()].append(self.current_param)
        self.UpdateDisplay()
        
    def Swap(self):
        temp1 = self.doubleSpinBox.value()
        temp2 = self.doubleSpinBox_2.value()
        self.doubleSpinBox.setValue(temp2)
        self.doubleSpinBox_2.setValue(temp1)



    def Vrampe2DDialog(self,axis = 'Fast'):
        self.axis = axis
        self.sweepForm = QtGui.QDialog()
        self.sweepForm.resize(420, 332)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.sweepForm)
        self.doubleSpinBox.setGeometry(QtCore.QRect(120, 70, 62, 22))
        # self.doubleSpinBox.setMinimum(-float('inf'))
        # self.doubleSpinBox.setMaximum(float('inf'))
        self.doubleSpinBox.setMinimum(-float(maxvoltage))
        self.doubleSpinBox.setMaximum(float(maxvoltage))
        self.doubleSpinBox.setDecimals(6)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.sweepForm)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(220, 70, 62, 22))
        # self.doubleSpinBox_2.setMinimum(-float('inf'))
        # self.doubleSpinBox_2.setMaximum(float('inf'))
        self.doubleSpinBox_2.setMinimum(-float(maxvoltage))
        self.doubleSpinBox_2.setMaximum(float(maxvoltage))
        self.doubleSpinBox_2.setDecimals(6)
        self.spinBox = QtWidgets.QSpinBox(self.sweepForm)
        self.spinBox.setGeometry(QtCore.QRect(120, 130, 42, 22))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1000000)
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self.sweepForm)
        self.doubleSpinBox_3.setGeometry(QtCore.QRect(300, 130, 62, 22))
        self.doubleSpinBox_3.setMinimum(100)
        self.doubleSpinBox_3.setMaximum(1000000)
        
        self.inbetweenSpinBox = QtWidgets.QDoubleSpinBox(self.sweepForm)
        self.inbetweenSpinBox.setGeometry(QtCore.QRect(220, 180, 62, 22))
        self.inbetweenSpinBox.setDecimals(6)
        self.inbetweenSpinBox.setValue(1)
        
        
        
        self.deviceBox = QtWidgets.QComboBox(self.sweepForm)
        self.deviceBox.setGeometry(QtCore.QRect(10, 20, 169, 22))
        self.deviceBox.addItems(self.connected_devices_list)
        
        self.writekeysBox = QtWidgets.QComboBox(self.sweepForm)
        self.writekeysBox.setGeometry(QtCore.QRect(180, 20, 169, 22))
        self.writekeysBox.addItems(self.WriteKeys[int(self.deviceBox.currentText().split('_')[0]) - 1])
        self.deviceBox.currentIndexChanged.connect(self.UpdateWriteDialog_key)
                

        self.label = QtWidgets.QLabel(self.sweepForm)
        self.label.setGeometry(QtCore.QRect(120, 50, 47, 13))
        self.label.setText('Vstart (V)')
        self.label_2 = QtWidgets.QLabel(self.sweepForm)
        self.label_2.setGeometry(QtCore.QRect(220, 50, 47, 13))
        self.label_2.setText('Vend (V)')
        self.label_3 = QtWidgets.QLabel(self.sweepForm)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 67, 33))
        self.label_3.setText(self.axis)
        self.label_3.setFont(QtGui.QFont('arial', 20))
        self.label_4 = QtWidgets.QLabel(self.sweepForm)
        self.label_4.setGeometry(QtCore.QRect(300, 110, 57, 13))
        self.label_4.setText('Delay (ms)')
        self.label_5 = QtWidgets.QLabel(self.sweepForm)
        self.label_5.setGeometry(QtCore.QRect(120, 110, 81, 16))
        self.label_5.setText('Number of Points')
        self.label_6 = QtWidgets.QLabel(self.sweepForm)
        self.label_6.setGeometry(QtCore.QRect(220, 110, 57, 13))
        self.label_6.setText('Step')
        self.label_7 = QtWidgets.QLabel(self.sweepForm)
        self.label_7.setGeometry(QtCore.QRect(220, 160, 57, 13))
        self.label_7.setText('large Step')
        self.SwapButton = QtWidgets.QPushButton(self.sweepForm)
        self.SwapButton.setGeometry(QtCore.QRect(300, 70, 62, 22))
        self.SwapButton.setObjectName("SwapButton")
        self.SwapButton.setText('Swap')
        self.SwapButton.setAutoDefault(False)
        self.SwapButton.clicked.connect(self.Swap)
        self.doubleSpinBox_4 = QtWidgets.QDoubleSpinBox(self.sweepForm)
        self.doubleSpinBox_4.setGeometry(QtCore.QRect(220, 130, 62, 22))
        self.doubleSpinBox_4.setMinimum(-float('inf'))
        self.doubleSpinBox_4.setMaximum(float('inf'))
        self.doubleSpinBox_4.setDecimals(6)
        
        self.nextButton = QtWidgets.QPushButton(self.sweepForm)
        self.nextButton.setGeometry(QtCore.QRect(300, 160, 102, 42))
        self.nextButton.setText('Next')
        self.nextButton.setAutoDefault(False)
        self.nextButton.clicked.connect(self.nextReadSweep)
        
        self.checkThreshold = QtWidgets.QCheckBox(self.sweepForm)
        self.NThreshold = QtWidgets.QLineEdit(self.sweepForm)
        self.percentThreshold = QtWidgets.QLineEdit(self.sweepForm)
        self.delayThreshold = QtWidgets.QLineEdit(self.sweepForm)
        self.NThreshold.setGeometry(QtCore.QRect(60,270,50,15))
        self.checkThreshold.setGeometry(QtCore.QRect(10,270,20,20))
        self.percentThreshold.setGeometry(QtCore.QRect(120,270,50,15))
        self.delayThreshold.setGeometry(QtCore.QRect(180,270,50,15))
        
        self.Nlabel = QtWidgets.QLabel(self.sweepForm)
        self.percentlabel = QtWidgets.QLabel(self.sweepForm)
        self.delaylabel = QtWidgets.QLabel(self.sweepForm)
        self.Nlabel.setGeometry(QtCore.QRect(60,260,30,10))
        self.percentlabel.setGeometry(QtCore.QRect(120,260,30,10))
        self.delaylabel.setGeometry(QtCore.QRect(180,260,30,10))
        
        self.Nlabel.setText('N')
        self.percentlabel.setText('Threshold')
        self.delaylabel.setText('Delay (ms)')
        
        
        #load data
        if len(variables.actionlist[self.ActionWidget.currentRow()])>3 and type(variables.actionlist[self.ActionWidget.currentRow()][2]) != type(None):
            if self.axis == 'Fast':
                i = 2
            else:
                i=3
            dat2load = variables.actionlist[self.ActionWidget.currentRow()][i]
            index = self.deviceBox.findText(dat2load[0], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.deviceBox.setCurrentIndex(index)
                index = self.writekeysBox.findText(dat2load[1], QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.writekeysBox.setCurrentIndex(index)
            self.doubleSpinBox.setValue(dat2load[2])
            self.doubleSpinBox_2.setValue(dat2load[3])
            self.spinBox.setValue(dat2load[4])
            self.doubleSpinBox_3.setValue(dat2load[5])
            self.inbetweenSpinBox.setValue(dat2load[6])
            self.checkThreshold.setChecked(dat2load[7])
            self.NThreshold.setText(dat2load[8])
            self.percentThreshold.setText(dat2load[9])
            self.delayThreshold.setText(dat2load[10])
        #self.sweepForm.closeEvent = self.VerifStepVrampe2D
        self.sweepForm.exec_()
        
    def nextReadSweep(self):
        self.sweepForm.close()
        if variables.actionlist[self.ActionWidget.currentRow()][0] == 'Sweep2D':
            ax = self.axis
            self.VerifStepVrampe2D()
            if ax == 'Fast':
                self.Vrampe2DDialog('Slow')
            else:
                self.ReadDialog()
        else:#fails mean its a 1D sweep
            self.ReadDialog()
        #self.readForm.closeEvent = self.readSweepEvent
    
        
    def VerifStepVrampe2D(self):
        Form = QtGui.QDialog()
        Form.resize(100, 50)
        if self.doubleSpinBox_4.value()!=0 :
            self.spinBox.setValue(int(abs(self.doubleSpinBox.value()-self.doubleSpinBox_2.value())/self.doubleSpinBox_4.value())+1)
        if self.spinBox.value()-1!=0 :
            self.doubleSpinBox_4.setValue(abs(self.doubleSpinBox.value()-self.doubleSpinBox_2.value())/(self.spinBox.value()-1))
        step = None
        if self.spinBox.value()-1 !=0:
            step = abs(self.doubleSpinBox.value()-self.doubleSpinBox_2.value())/(self.spinBox.value()-1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 0, 60, 13))
        self.label.setText('Step size (V)')
        self.label_1 = QtWidgets.QLabel(Form)
        self.label_1.setGeometry(QtCore.QRect(50, 20, 47, 13))
        self.label_1.setText(str(step))
        Form.closeEvent = self.Vrampe2DEvent
        Form.exec_()
        
        
    def Vrampe2DEvent(self,event):
        self.current_param = [self.deviceBox.currentText(),self.writekeysBox.currentText(),self.doubleSpinBox.value(),self.doubleSpinBox_2.value(),self.spinBox.value(),self.doubleSpinBox_3.value(),self.inbetweenSpinBox.value(),self.checkThreshold.isChecked(),self.NThreshold.text(),self.percentThreshold.text(),self.delayThreshold.text()] #id,key,vstar,Vend,N,delay,largestep
        if len(variables.actionlist[self.ActionWidget.currentRow()]) == 4:
            if self.axis == 'Fast':
                i = 2
            else:
                i=3
            variables.actionlist[self.ActionWidget.currentRow()][i] = self.current_param
        else:
            variables.actionlist[self.ActionWidget.currentRow()].append(self.current_param)
        self.UpdateDisplay()

    def setTemp(self):
        self.sweepForm = QtGui.QDialog()
        self.sweepForm.resize(420, 222)
        # self.label_9 = QtWidgets.QLabel(self.sweepForm)
        # self.label_9.setGeometry(QtCore.QRect(30, 60, 61, 20))
        # self.label_9.setText("Input:")
        self.label_12 = QtWidgets.QLabel(self.sweepForm)
        self.label_12.setGeometry(QtCore.QRect(30, 90, 51, 20))
        self.label_12.setText("Range:")
        self.outputBox = QtWidgets.QComboBox(self.sweepForm)
        self.outputBox.setGeometry(QtCore.QRect(80, 120, 81, 22))
        self.outputBox.addItem("A")
        self.outputBox.addItem("C")
        self.label_10 = QtWidgets.QLabel(self.sweepForm)
        self.label_10.setGeometry(QtCore.QRect(30, 120, 81, 16))
        self.label_10.setText("Output:")
        self.tuneBox = QtWidgets.QComboBox(self.sweepForm)
        self.tuneBox.setGeometry(QtCore.QRect(80, 90, 81, 22))
        self.tuneBox.addItem("Off")
        self.tuneBox.addItem("1")
        self.tuneBox.addItem("2")
        self.tuneBox.addItem("3")
        self.tuneBox.addItem("4")
        self.tuneBox.addItem("5")
        # self.inputBox = QtWidgets.QComboBox(self.sweepForm)
        # self.inputBox.setGeometry(QtCore.QRect(80, 60, 69, 22))
        # self.inputBox.addItem("A")
        # self.inputBox.addItem("B")
        # self.inputBox.addItem("C")
        # self.inputBox.addItem("D")
        
        
        # self.label = QtWidgets.QLabel(Form)
        # self.label.setGeometry(QtCore.QRect(30, 20, 47, 13))
        # self.label.setText("Device:")
        # self.devBox = QtWidgets.QComboBox(Form)
        # self.devBox.setGeometry(QtCore.QRect(80, 20, 69, 22))
        # self.devBox.addItem("Device 1")
        # self.devBox.addItem("Device 2")
        # self.devBox.addItem("Device 3")
        # self.devBox.addItem("Device 4")
        # self.devBox.addItem("Device 5")
        # self.devBox.addItem("Device 6")
        # self.devBox.addItem("Device 7")
        # self.devBox.addItem("Device 8")
        # self.devBox.addItem("Device 9")
        # self.devBox.addItem("Device 10")
        
        self.deviceBox = QtWidgets.QComboBox(self.sweepForm)
        self.deviceBox.setGeometry(QtCore.QRect(10, 20, 169, 22))
        self.deviceBox.addItems(self.connected_devices_list)
        
        self.writekeysBox = QtWidgets.QComboBox(self.sweepForm)
        self.writekeysBox.setGeometry(QtCore.QRect(180, 20, 169, 22))
        self.writekeysBox.addItems(self.WriteKeys[int(self.deviceBox.currentText().split('_')[0]) - 1])
        self.deviceBox.currentIndexChanged.connect(self.UpdateWriteDialog_key)
        
        
        
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.sweepForm)
        self.doubleSpinBox.setGeometry(QtCore.QRect(80, 150, 62, 22))
        self.doubleSpinBox.setMinimum(0)
        self.doubleSpinBox.setMaximum(1000)
        self.label_42 = QtWidgets.QLabel(self.sweepForm)
        self.label_42.setGeometry(QtCore.QRect(45, 155, 27, 13))
        self.label_42.setText("T (K):")
      
        #load data
        if type(variables.actionlist[self.ActionWidget.currentRow()][1]) != type(None):
            dat2load = variables.actionlist[self.ActionWidget.currentRow()][1]
            print(dat2load)
            index = self.deviceBox.findText(dat2load[0], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.deviceBox.setCurrentIndex(index)
                index = self.writekeysBox.findText(dat2load[1], QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.writekeysBox.setCurrentIndex(index)
            
            
            index = self.tuneBox.findText(dat2load[2], QtCore.Qt.MatchFixedString)

            self.tuneBox.setCurrentIndex(index)
            # self.inputBox.setCurrentIndex(dat2load[1])
            index = self.outputBox.findText(dat2load[3], QtCore.Qt.MatchFixedString)
            self.outputBox.setCurrentIndex(index)
            self.doubleSpinBox.setValue(dat2load[4])
        self.sweepForm.closeEvent = self.setTempEvent
        self.sweepForm.exec_()
        
    

    def setTempEvent(self,event):
        self.current_param = [self.deviceBox.currentText(),self.writekeysBox.currentText(),self.tuneBox.currentText(),self.outputBox.currentText(),self.doubleSpinBox.value()] #id,devicekey, output,range,temperature

        # self.current_param = [self.devBox.currentIndex(),self.inputBox.currentIndex(),self.outputBox.currentIndex(),self.tuneBox.currentIndex(),self.doubleSpinBox.value()] #dev,input,output,range,temp
        # self.actionlist[self.ActionWidget.currentRow()][1] = self.current_param
        # self.UpdateDisplay()
        
        if len(variables.actionlist[self.ActionWidget.currentRow()]) >= 1:
            variables.actionlist[self.ActionWidget.currentRow()][1] = self.current_param
        else:
            variables.actionlist[self.ActionWidget.currentRow()].append(self.current_param)
        self.UpdateDisplay()
        


        
    def WriteDialog(self):#generates the dialog dynamically
        self.writeForm = QtGui.QDialog()
        self.writeForm.resize(191, 352)
        self.deviceBox = QtWidgets.QComboBox(self.writeForm)
        self.deviceBox.setGeometry(QtCore.QRect(10, 20, 169, 22))
        for dev in self.connected_devices_list:
            if type(dev) != type(None):
                self.deviceBox.addItem(dev)
        #self.deviceBox.addItems(self.connected_devices_list)
        self.deviceBox.currentIndexChanged.connect(self.UpdateWriteDialog_key)
        
        self.writekeysBox = QtWidgets.QComboBox(self.writeForm)
        self.writekeysBox.setGeometry(QtCore.QRect(10, 60, 169, 22))
        self.writekeysBox.addItems(self.WriteKeys[int(self.deviceBox.currentText().split('_')[0]) - 1])
        self.writekeysBox.currentIndexChanged.connect(self.UpdateWriteDialog)
        
        
        
        self.writeForm.closeEvent = self.WriteEvent
        self.EditWriteDialog()

        self.writeForm.exec_()
    
    def UpdateWriteDialog_key(self):#updates the combobox depending on the device
        self.writekeysBox.clear()
        self.writekeysBox.addItems(self.WriteKeys[int(self.deviceBox.currentText().split('_')[0]) - 1])
        return()
    
    def UpdateWriteDialog(self):#remove previous display pattern and add the new one
        if self.writekeysBox.currentText() == '':#for the case when the keysbox is cleared and the items are not yet added
            return()
        self.currentPattern = self.WritePatterns[int(self.deviceBox.currentText().split('_')[0]) - 1][self.writekeysBox.currentText()]
        try:
            for dialogObject in self.WriteDialogObjects:
                dialogObject.deleteLater()
                dialogObject = None
            QtTest.QTest.qWait(10)#delay to give it time to delete the objects
        except Exception as e:
            #print(e)
            None
        self.WriteDialogObjects = []
        currentHeight,heightStep,labelHeight = 100,40,20
        for boxPattern in self.currentPattern:
            self.WriteDialogObjects.append(QtWidgets.QLabel(self.writeForm))
            self.WriteDialogObjects[-1].setGeometry(QtCore.QRect(10, currentHeight, 169, 22))
            self.WriteDialogObjects[-1].setText(boxPattern[0])
            if boxPattern[1] == 'choice':
                self.WriteDialogObjects.append(QtWidgets.QComboBox(self.writeForm))
                self.WriteDialogObjects[-1].setGeometry(QtCore.QRect(10, currentHeight + labelHeight, 169, 22))
                self.WriteDialogObjects[-1].addItems(boxPattern[2])
            elif boxPattern[1] == 'text':
                self.WriteDialogObjects.append(QtWidgets.QLineEdit(self.writeForm))
                self.WriteDialogObjects[-1].setGeometry(QtCore.QRect(10, currentHeight + labelHeight, 169, 22))
            currentHeight += heightStep
        self.writeForm.resize(191,currentHeight+heightStep)
        for dialogObject in self.WriteDialogObjects:
            dialogObject.show()
        self.writeForm.update()
    
    def EditWriteDialog(self):
        if type(variables.actionlist[self.ActionWidget.currentRow()][1]) != type(None):
            dat2load = variables.actionlist[self.ActionWidget.currentRow()][1]
            index = self.deviceBox.findText(dat2load[0], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.deviceBox.setCurrentIndex(index)
                index = self.writekeysBox.findText(dat2load[1], QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.writekeysBox.setCurrentIndex(index)
                    self.UpdateWriteDialog()
                    for k in range(len(self.currentPattern)):
                        if self.currentPattern[k][1] == 'choice':
                            index = self.WriteDialogObjects[2*k+1].findText(dat2load[k+2], QtCore.Qt.MatchFixedString)
                            if index >= 0:
                                self.WriteDialogObjects[2*k+1].setCurrentIndex(index)
                        elif self.currentPattern[k][1] == 'text':
                            #print(self.WriteDialogObjects)
                            self.WriteDialogObjects[2*k+1].setText(dat2load[k+2])
        else:#ie nothing to load
            self.UpdateWriteDialog()
    

    def WriteEvent(self,event):
        self.current_param = [self.deviceBox.currentText(),self.writekeysBox.currentText()]
        for i in range(len(self.currentPattern)):
            if self.currentPattern[i][1] == 'choice':
                self.current_param.append(self.WriteDialogObjects[2*i+1].currentText())#2i+1 to avoid label objects
            elif self.currentPattern[i][1] == 'text':
                self.current_param.append(self.WriteDialogObjects[2*i+1].text())
        
        variables.actionlist[self.ActionWidget.currentRow()][1] = self.current_param
        self.UpdateDisplay()


    def ReadDialog(self):
        self.ReadDialogObjects,self.currentHeight,self.stepHeight = [],50,30# ReadDialogObjects: [[devbox1,keybox1,removebutton1,removefunction,keyupdatefunc],[],...]
        self.readForm = QtGui.QDialog()
        self.readForm.resize(400, 352)
        self.addButton = QtWidgets.QPushButton(self.readForm)
        self.addButton.setGeometry(QtCore.QRect(10, 10, 62, 20))
        self.addButton.setText('add')
        self.addButton.setAutoDefault(False)
        self.addButton.clicked.connect(self.addDevReadDialog)
        
        self.readForm.closeEvent = self.readEvent
        self.editReadDialog()
        
        self.readForm.exec_()
    
    def KeyReadDialog(self,N):
        self.ReadDialogObjects[N][1].clear()
        if self.ReadDialogObjects[N][0].currentText() == 'Math':
            self.ReadDialogObjects[N][1].addItems(['variables.A','variables.B','variables.C','variables.D','variables.E','variables.F'])
        else:
            self.ReadDialogObjects[N][1].addItems(self.ReadKeys[int(self.ReadDialogObjects[N][0].currentText().split('_')[0]) - 1])


    def addDevReadDialog(self):
        N = len(self.ReadDialogObjects)
        self.ReadDialogObjects.append([QtWidgets.QComboBox(self.readForm),QtWidgets.QComboBox(self.readForm),QtWidgets.QPushButton(self.readForm),lambda : self.removeDevReadDialog(N),lambda : self.KeyReadDialog(N)])
        self.ReadDialogObjects[N][0].setGeometry(QtCore.QRect(10, self.currentHeight, 169, 20))
        self.ReadDialogObjects[N][1].setGeometry(QtCore.QRect(190, self.currentHeight, 169, 20))
        self.ReadDialogObjects[N][2].setGeometry(QtCore.QRect(360, self.currentHeight, 22, 20))
        self.ReadDialogObjects[N][2].clicked.connect(self.ReadDialogObjects[N][3])
        self.ReadDialogObjects[N][2].setText('X')
        self.ReadDialogObjects[N][2].setAutoDefault(False)
        self.currentHeight += self.stepHeight
        
        self.ReadDialogObjects[N][0].show()
        self.ReadDialogObjects[N][1].show()
        self.ReadDialogObjects[N][2].show()
        for dev in self.connected_devices_list:
            if type(dev) != type(None):
                self.ReadDialogObjects[N][0].addItem(dev)
        self.ReadDialogObjects[N][0].addItem('Math')
        self.ReadDialogObjects[N][0].currentIndexChanged.connect(self.ReadDialogObjects[N][4])
        self.ReadDialogObjects[N][4]()
        
        return()
    
    def WeirdBugIDKremove(self,N):#fix the issue with the  variable scope in functions
        a = N
        g = lambda : self.removeDevReadDialog(a)
        return(g)
    
    def WeirdBugIDKupdate(self,N):
        a = N
        g = lambda : self.KeyReadDialog(a)
        return(g)
    
    def removeDevReadDialog(self,N):#N number of the device to remove
        try:
            for k in range(len(self.ReadDialogObjects[N])-1):
                self.ReadDialogObjects[N][k].deleteLater()
                self.ReadDialogObjects[N][k] = None
        except:
            None
        del self.ReadDialogObjects[N]
        for k in range(N,len(self.ReadDialogObjects)):
            self.ReadDialogObjects[k][3] = self.WeirdBugIDKremove(k)
            self.ReadDialogObjects[k][4] = self.WeirdBugIDKupdate(k)
            self.ReadDialogObjects[k][0].currentIndexChanged.disconnect()
            self.ReadDialogObjects[k][0].currentIndexChanged.connect(self.ReadDialogObjects[k][4])
            self.ReadDialogObjects[k][2].clicked.disconnect()
            self.ReadDialogObjects[k][2].clicked.connect(self.ReadDialogObjects[k][3])
            for i in range(len(self.ReadDialogObjects[k])-2):
                pos = self.ReadDialogObjects[k][i].pos()
                self.ReadDialogObjects[k][i].move(pos.x(),pos.y() - self.stepHeight)
                self.ReadDialogObjects[k][i].show()
                None
        self.currentHeight -= self.stepHeight
        return()
    
    def editReadDialog(self):
        if type(variables.actionlist[self.ActionWidget.currentRow()][1]) != type(None):
            dat2load = variables.actionlist[self.ActionWidget.currentRow()][1]
            for k in range(0,len(dat2load)):
                self.addDevReadDialog()
                index = self.ReadDialogObjects[-1][0].findText(dat2load[k][0], QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.ReadDialogObjects[-1][0].setCurrentIndex(index)
                    index = self.ReadDialogObjects[-1][1].findText(dat2load[k][1], QtCore.Qt.MatchFixedString)
                    if index >= 0:
                        self.ReadDialogObjects[-1][1].setCurrentIndex(index)

    def readEvent(self,event):
        self.current_param = []
        for readObject in self.ReadDialogObjects:
            self.current_param.append([readObject[0].currentText(),readObject[1].currentText()])
        
        variables.actionlist[self.ActionWidget.currentRow()][1] = self.current_param
        self.UpdateDisplay()
        

    def IdleDialog(self):
        self.IdleForm = QtGui.QDialog()
        self.IdleForm.resize(191, 102)
        self.SpinBox = QtWidgets.QSpinBox(self.IdleForm)
        self.SpinBox.setGeometry(QtCore.QRect(120, 20, 62, 22))
        self.SpinBox.setMinimum(-1)
        self.SpinBox.setMaximum(2147483647)
        self.SpinBox_3 = QtWidgets.QSpinBox(self.IdleForm)
        self.SpinBox_3.setGeometry(QtCore.QRect(10,20, 62, 22))
        self.SpinBox_3.setMaximum(10000000)
        self.label = QtWidgets.QLabel(self.IdleForm)
        self.label.setGeometry(QtCore.QRect(120, 0, 97, 13))
        self.label.setText('Idle Time (ms)')
        self.label2 = QtWidgets.QLabel(self.IdleForm)
        self.label2.setGeometry(QtCore.QRect(10, 0, 97, 13))
        self.label2.setText('Sampling Time (ms)')
        
        self.nextButton = QtWidgets.QPushButton(self.IdleForm)
        self.nextButton.setGeometry(QtCore.QRect(100, 50, 72, 42))
        self.nextButton.setText('Next')
        self.nextButton.setAutoDefault(False)
        self.nextButton.clicked.connect(self.nextIdle)
        
        self.IdleForm.closeEvent = self.IdleEvent
        #load data
        try:
            if type(variables.actionlist[self.ActionWidget.currentRow()][2]) != type(None):
                dat2load = variables.actionlist[self.ActionWidget.currentRow()][2]
                self.SpinBox_3.setValue(dat2load[0])
                self.SpinBox.setValue(dat2load[1])
        except:
            None
        self.IdleForm.exec_()
    
    def nextIdle(self):
        self.IdleForm.close()
        self.ReadDialog()
    
    def IdleEvent(self,event):
        self.current_param = [self.SpinBox_3.value(),self.SpinBox.value()] #sampling,idle
        if len(variables.actionlist[self.ActionWidget.currentRow()]) == 3:
            variables.actionlist[self.ActionWidget.currentRow()][2] = self.current_param
        elif len(variables.actionlist[self.ActionWidget.currentRow()]) == 2:
            variables.actionlist[self.ActionWidget.currentRow()].append(self.current_param)
        else:
            print('F')
        self.UpdateDisplay()

    def MathDialog(self):
        pdialog = QtGui.QDialog()
        pdialog.resize(500,70)
        self.label = QtWidgets.QLabel('Math Command:',pdialog)
        self.mathCommand = QtWidgets.QLineEdit(pdialog)
        self.mathCommand.setGeometry(QtCore.QRect(1, 15, 411, 23))
        pdialog.closeEvent = self.MathEvent
        #load data into window
        if type(variables.actionlist[self.ActionWidget.currentRow()][1]) != type(None):
            self.mathCommand.setText(variables.actionlist[self.ActionWidget.currentRow()][1][0])
        else:
            self.mathCommand.setText('variables.B += 1')
        pdialog.exec_()
        

    def MathEvent(self,event):
        self.current_param = [self.mathCommand.text()]
        variables.actionlist[self.ActionWidget.currentRow()][1] = self.current_param
        self.UpdateDisplay()
    
    def JumpIfDialog(self):
        pdialog = QtGui.QDialog()
        pdialog.resize(420,90)
        self.label = QtWidgets.QLabel('Math Condition:',pdialog)
        self.jumpCondition = QtWidgets.QLineEdit(pdialog)
        self.jumpCondition.setGeometry(QtCore.QRect(1, 15, 411, 23))
        self.label2 = QtWidgets.QLabel('Line:',pdialog)
        self.label2.setGeometry(QtCore.QRect(1, 42, 62, 22))
        self.jumpLine = QtWidgets.QSpinBox(pdialog)
        self.jumpLine.setGeometry(QtCore.QRect(1, 60, 62, 22))
        self.jumpLine.setMinimum(0)
        self.jumpLine.setMaximum(9999) #add maximum
        
        pdialog.closeEvent = self.JumpIfEvent
        #load data into window
        if type(variables.actionlist[self.ActionWidget.currentRow()][1]) != type(None):
            self.jumpCondition.setText(variables.actionlist[self.ActionWidget.currentRow()][1][0])
            self.jumpLine.setValue(variables.actionlist[self.ActionWidget.currentRow()][1][1])
        else:
            self.jumpCondition.setText('variables.B < 42')
        pdialog.exec_()
        

    def JumpIfEvent(self,event):
        self.current_param = [self.jumpCondition.text(),self.jumpLine.value()]
        variables.actionlist[self.ActionWidget.currentRow()][1] = self.current_param
        self.UpdateDisplay()








    def CustomSweepDialog(self):
        self.CustomSweepDialogObjects,self.currentHeight,self.stepHeight = [],50,90# ReadDialogObjects: [[devbox1,keybox1,removebutton1,removefunction,keyupdatefunc],[],...]
        self.CustomSweepForm = QtGui.QDialog()
        self.CustomSweepForm.resize(660, 552)
        self.addButton = QtWidgets.QPushButton(self.CustomSweepForm)
        self.addButton.setGeometry(QtCore.QRect(10, 10, 62, 20))
        self.addButton.setText('add')
        self.addButton.setAutoDefault(False)
        self.addButton.clicked.connect(self.addDevCustomSweepDialog)
        
        self.CustomSweepForm.closeEvent = self.CustomSweepEvent
        self.editCustomSweepDialog()
        
        self.CustomSweepForm.exec_()
    
    def KeyCustomSweepDialog(self,N):
        self.CustomSweepDialogObjects[N][1].clear()
        self.CustomSweepDialogObjects[N][1].addItems(self.WriteKeys[int(self.CustomSweepDialogObjects[N][0].currentText().split('_')[0]) - 1])


    def addDevCustomSweepDialog(self):
        N = len(self.CustomSweepDialogObjects)
        self.CustomSweepDialogObjects.append([QtWidgets.QComboBox(self.CustomSweepForm),QtWidgets.QComboBox(self.CustomSweepForm),QtWidgets.QPushButton(self.CustomSweepForm),QtWidgets.QLabel(self.CustomSweepForm),QtWidgets.QCheckBox(self.CustomSweepForm),QtWidgets.QLabel(self.CustomSweepForm),QtWidgets.QLineEdit(self.CustomSweepForm),QtWidgets.QLabel(self.CustomSweepForm),QtWidgets.QLineEdit(self.CustomSweepForm),QtWidgets.QLabel(self.CustomSweepForm),QtWidgets.QLineEdit(self.CustomSweepForm),QtWidgets.QLabel(self.CustomSweepForm),QtWidgets.QLineEdit(self.CustomSweepForm),QtWidgets.QLabel(self.CustomSweepForm),QtWidgets.QLineEdit(self.CustomSweepForm),QtWidgets.QLabel(self.CustomSweepForm),QtWidgets.QCheckBox(self.CustomSweepForm),QtWidgets.QLabel(self.CustomSweepForm),QtWidgets.QLineEdit(self.CustomSweepForm),QtWidgets.QLabel(self.CustomSweepForm),QtWidgets.QLineEdit(self.CustomSweepForm),QtWidgets.QLabel(self.CustomSweepForm),QtWidgets.QLineEdit(self.CustomSweepForm),QtWidgets.QPushButton(self.CustomSweepForm),lambda : self.swapCustomSweepDialog(N),lambda : self.removeDevCustomSweepDialog(N),lambda : self.KeyCustomSweepDialog(N)])
        self.CustomSweepDialogObjects[N][0].setGeometry(QtCore.QRect(10, self.currentHeight, 169, 20))
        self.CustomSweepDialogObjects[N][1].setGeometry(QtCore.QRect(190, self.currentHeight, 169, 20))
        self.CustomSweepDialogObjects[N][2].setGeometry(QtCore.QRect(630, self.currentHeight, 22, 20))
        
        self.CustomSweepDialogObjects[N][3].setGeometry(QtCore.QRect(365, self.currentHeight, 45, 20))
        self.CustomSweepDialogObjects[N][4].setGeometry(QtCore.QRect(410, self.currentHeight, 20, 20))
        
        self.CustomSweepDialogObjects[N][5].setGeometry(QtCore.QRect(10, self.currentHeight +25, 70, 20))
        self.CustomSweepDialogObjects[N][6].setGeometry(QtCore.QRect(10, self.currentHeight + 45, 40, 20))
        self.CustomSweepDialogObjects[N][7].setGeometry(QtCore.QRect(80, self.currentHeight +25, 60, 20))
        self.CustomSweepDialogObjects[N][8].setGeometry(QtCore.QRect(80, self.currentHeight+ 45, 40, 20))
        self.CustomSweepDialogObjects[N][9].setGeometry(QtCore.QRect(150, self.currentHeight +25, 60, 20))
        self.CustomSweepDialogObjects[N][10].setGeometry(QtCore.QRect(150, self.currentHeight+ 45, 40, 20))
        self.CustomSweepDialogObjects[N][11].setGeometry(QtCore.QRect(220, self.currentHeight +25, 60, 20))
        self.CustomSweepDialogObjects[N][12].setGeometry(QtCore.QRect(220, self.currentHeight+ 45, 40, 20))
        self.CustomSweepDialogObjects[N][13].setGeometry(QtCore.QRect(290, self.currentHeight +25, 60, 20))
        self.CustomSweepDialogObjects[N][14].setGeometry(QtCore.QRect(290, self.currentHeight+ 45, 40, 20))
        
        self.CustomSweepDialogObjects[N][15].setGeometry(QtCore.QRect(440, self.currentHeight, 70, 20))
        self.CustomSweepDialogObjects[N][16].setGeometry(QtCore.QRect(515, self.currentHeight, 20, 20))
        self.CustomSweepDialogObjects[N][17].setGeometry(QtCore.QRect(535, self.currentHeight, 60, 20))
        self.CustomSweepDialogObjects[N][18].setGeometry(QtCore.QRect(600, self.currentHeight, 30, 20))
        self.CustomSweepDialogObjects[N][19].setGeometry(QtCore.QRect(535, self.currentHeight+22, 60, 20))
        self.CustomSweepDialogObjects[N][20].setGeometry(QtCore.QRect(600, self.currentHeight+22, 30, 20))
        self.CustomSweepDialogObjects[N][21].setGeometry(QtCore.QRect(535, self.currentHeight-22, 60, 20))
        self.CustomSweepDialogObjects[N][22].setGeometry(QtCore.QRect(600, self.currentHeight-22, 30, 20))
        
        self.CustomSweepDialogObjects[N][23].setGeometry(QtCore.QRect(55, self.currentHeight+45, 20, 20))
        
        
        
        
        
        self.CustomSweepDialogObjects[N][15].setText('Wait Setpoint:')
        self.CustomSweepDialogObjects[N][17].setText('Threshold:')
        self.CustomSweepDialogObjects[N][3].setText('Measure:')
        self.CustomSweepDialogObjects[N][5].setText('Start:')
        self.CustomSweepDialogObjects[N][7].setText('Stop:')
        self.CustomSweepDialogObjects[N][9].setText('Step:')
        self.CustomSweepDialogObjects[N][11].setText('Delay(ms):')
        self.CustomSweepDialogObjects[N][13].setText('Large Step:')
        self.CustomSweepDialogObjects[N][19].setText('Delay stp(ms):')
        self.CustomSweepDialogObjects[N][21].setText('N setp:')
        
        #autofill:
        self.CustomSweepDialogObjects[N][4].setChecked(True)
        if N > 0:
            self.CustomSweepDialogObjects[N][6].setText(self.CustomSweepDialogObjects[N-1][6].text())
            self.CustomSweepDialogObjects[N][8].setText(self.CustomSweepDialogObjects[N-1][8].text())
            self.CustomSweepDialogObjects[N][10].setText(self.CustomSweepDialogObjects[N-1][10].text())
            self.CustomSweepDialogObjects[N][12].setText(self.CustomSweepDialogObjects[N-1][12].text())
            self.CustomSweepDialogObjects[N][14].setText(self.CustomSweepDialogObjects[N-1][14].text())
            self.CustomSweepDialogObjects[N][16].setChecked(self.CustomSweepDialogObjects[N-1][16].isChecked())
            self.CustomSweepDialogObjects[N][18].setText(self.CustomSweepDialogObjects[N-1][18].text())
            self.CustomSweepDialogObjects[N][20].setText(self.CustomSweepDialogObjects[N-1][20].text())
            self.CustomSweepDialogObjects[N][22].setText(self.CustomSweepDialogObjects[N-1][22].text())
            self.CustomSweepDialogObjects[N][0].setCurrentIndex(self.CustomSweepDialogObjects[N-1][0].currentIndex())
            self.CustomSweepDialogObjects[N][1].setCurrentIndex(self.CustomSweepDialogObjects[N-1][1].currentIndex())
            
        
        
        self.CustomSweepDialogObjects[N][2].clicked.connect(self.CustomSweepDialogObjects[N][-2])
        self.CustomSweepDialogObjects[N][2].setText('X')
        self.CustomSweepDialogObjects[N][2].setAutoDefault(False)
        self.CustomSweepDialogObjects[N][23].clicked.connect(self.CustomSweepDialogObjects[N][-3])
        self.CustomSweepDialogObjects[N][23].setText('⇄')
        self.CustomSweepDialogObjects[N][23].setAutoDefault(False)
        self.currentHeight += self.stepHeight
        
        for k in range(len(self.CustomSweepDialogObjects[N]) - 3):
            self.CustomSweepDialogObjects[N][k].show()

        
        self.CustomSweepDialogObjects[N][0].addItems(self.connected_devices_list)
        self.CustomSweepDialogObjects[N][0].currentIndexChanged.connect(self.CustomSweepDialogObjects[N][-1])
        self.CustomSweepDialogObjects[N][-1]()
        
        if N > 0:
            self.CustomSweepDialogObjects[N][6].setText(self.CustomSweepDialogObjects[N-1][6].text())
            self.CustomSweepDialogObjects[N][8].setText(self.CustomSweepDialogObjects[N-1][8].text())
            self.CustomSweepDialogObjects[N][10].setText(self.CustomSweepDialogObjects[N-1][10].text())
            self.CustomSweepDialogObjects[N][12].setText(self.CustomSweepDialogObjects[N-1][12].text())
            self.CustomSweepDialogObjects[N][14].setText(self.CustomSweepDialogObjects[N-1][14].text())
            self.CustomSweepDialogObjects[N][16].setChecked(self.CustomSweepDialogObjects[N-1][16].isChecked())
            self.CustomSweepDialogObjects[N][18].setText(self.CustomSweepDialogObjects[N-1][18].text())
            self.CustomSweepDialogObjects[N][20].setText(self.CustomSweepDialogObjects[N-1][20].text())
            self.CustomSweepDialogObjects[N][22].setText(self.CustomSweepDialogObjects[N-1][22].text())
            self.CustomSweepDialogObjects[N][0].setCurrentIndex(self.CustomSweepDialogObjects[N-1][0].currentIndex())
            self.CustomSweepDialogObjects[N][1].setCurrentIndex(self.CustomSweepDialogObjects[N-1][1].currentIndex())
        
        return()
    
    def LocalVarremove(self,N):#fix the issue with the  variable scope in functions
        a = N
        g = lambda : self.removeDevCustomSweepDialog(a)
        return(g)
    
    def LocalVarupdate(self,N):
        a = N
        g = lambda : self.KeyCustomSweepDialog(a)
        return(g)
    
    def LocalVarswap(self,N):
        a = N
        g = lambda : self.swapCustomSweepDialog(a)
        return(g)
    
    def swapCustomSweepDialog(self,N):
        temp = self.CustomSweepDialogObjects[N][6].text()
        self.CustomSweepDialogObjects[N][6].setText(self.CustomSweepDialogObjects[N][8].text())
        self.CustomSweepDialogObjects[N][8].setText(temp)
    
    def removeDevCustomSweepDialog(self,N):#N number of the device to remove
        try:
            for k in range(len(self.CustomSweepDialogObjects[N])-1):
                self.CustomSweepDialogObjects[N][k].deleteLater()
                self.CustomSweepDialogObjects[N][k] = None
        except:
            None
        del self.CustomSweepDialogObjects[N]
        for k in range(N,len(self.CustomSweepDialogObjects)):
            self.CustomSweepDialogObjects[k][-3] = self.LocalVarswap(k)
            self.CustomSweepDialogObjects[k][-2] = self.LocalVarremove(k)
            self.CustomSweepDialogObjects[k][-1] = self.LocalVarupdate(k)
            self.CustomSweepDialogObjects[k][0].currentIndexChanged.disconnect()
            self.CustomSweepDialogObjects[k][0].currentIndexChanged.connect(self.CustomSweepDialogObjects[k][-1])
            self.CustomSweepDialogObjects[k][2].clicked.disconnect()
            self.CustomSweepDialogObjects[k][2].clicked.connect(self.CustomSweepDialogObjects[k][-2])
            self.CustomSweepDialogObjects[k][23].clicked.disconnect()
            self.CustomSweepDialogObjects[k][23].clicked.connect(self.CustomSweepDialogObjects[k][-3])
            for i in range(len(self.CustomSweepDialogObjects[k])-3):
                pos = self.CustomSweepDialogObjects[k][i].pos()
                self.CustomSweepDialogObjects[k][i].move(pos.x(),pos.y() - self.stepHeight)
                self.CustomSweepDialogObjects[k][i].show()
                None
        self.currentHeight -= self.stepHeight
        return()
    
    def editCustomSweepDialog(self):
        if len(variables.actionlist[self.ActionWidget.currentRow()]) > 2:
            dat2load = variables.actionlist[self.ActionWidget.currentRow()][2]
            for k in range(0,len(dat2load)):
                self.addDevCustomSweepDialog()
                index = self.CustomSweepDialogObjects[-1][0].findText(dat2load[k][0], QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.CustomSweepDialogObjects[-1][0].setCurrentIndex(index)
                    index = self.CustomSweepDialogObjects[-1][1].findText(dat2load[k][1], QtCore.Qt.MatchFixedString)
                    if index >= 0:
                        self.CustomSweepDialogObjects[-1][1].setCurrentIndex(index)
                self.CustomSweepDialogObjects[-1][4].setChecked(dat2load[k][2])
                self.CustomSweepDialogObjects[-1][6].setText(dat2load[k][3])
                self.CustomSweepDialogObjects[-1][8].setText(dat2load[k][4])
                self.CustomSweepDialogObjects[-1][10].setText(dat2load[k][5])
                self.CustomSweepDialogObjects[-1][12].setText(dat2load[k][6])
                self.CustomSweepDialogObjects[-1][14].setText(dat2load[k][7])
                self.CustomSweepDialogObjects[-1][16].setChecked(dat2load[k][8])
                self.CustomSweepDialogObjects[-1][18].setText(dat2load[k][9])
                self.CustomSweepDialogObjects[-1][20].setText(dat2load[k][10])
                self.CustomSweepDialogObjects[-1][22].setText(dat2load[k][11])
                
                
                
                
                

    def CustomSweepEvent(self,event):
        self.current_param = []
        for CustomSweepObject in self.CustomSweepDialogObjects:
            self.current_param.append([CustomSweepObject[0].currentText(),CustomSweepObject[1].currentText(),CustomSweepObject[4].isChecked(),CustomSweepObject[6].text(),CustomSweepObject[8].text(),CustomSweepObject[10].text(),CustomSweepObject[12].text(),CustomSweepObject[14].text(),CustomSweepObject[16].isChecked(),CustomSweepObject[18].text(),CustomSweepObject[20].text(),CustomSweepObject[22].text()])
        
        if len(variables.actionlist[self.ActionWidget.currentRow()]) == 3:
            variables.actionlist[self.ActionWidget.currentRow()][2] = self.current_param
        else:
            variables.actionlist[self.ActionWidget.currentRow()].append(self.current_param)
        self.UpdateDisplay()
        self.ReadDialog()











#Add/Remove

    def AddAction(self):
        variables.actionlist.append([self.ListActionBox.currentText(),None])
        self.UpdateDisplay()
    
    def AddVrampe(self):
        variables.actionlist.append(['VRampe',None])
        self.UpdateDisplay()
        
    def AddSaveData(self):
        variables.actionlist.append(['SaveData',None])
        self.UpdateDisplay()
    
    def AddIdle(self):
        variables.actionlist.append(['Idle',None])
        self.UpdateDisplay()
    
    def AddClearData(self):
        variables.actionlist.append(['ClearData',None])
        self.UpdateDisplay()
    
    def AddWrite(self):
        variables.actionlist.append(['Write',None])
        self.UpdateDisplay()
    
    def AddRead(self):
        variables.actionlist.append(['Read',None])
        self.UpdateDisplay()
    
    def AddMath(self):
        variables.actionlist.append(['Math',None])
        self.UpdateDisplay()
    
    def AddJumpif(self):
        variables.actionlist.append(['JumpIf',None])
        self.UpdateDisplay()
    
    def AddSweep2D(self):
        variables.actionlist.append(['Sweep2D',None])
        self.UpdateDisplay()
    
    def AddCustomSweep(self):
        variables.actionlist.append(['CustomSweep',None])
        self.UpdateDisplay()
        

    def RemoveAction(self):
        if len(variables.actionlist) > 0:
            ilist = [index.row() for index in self.ActionWidget.selectionModel().selectedRows()] #get the row numbers of all the selected items. 
            ilist.sort()
            ilist.reverse()#delete in the right order else errors
            for i in ilist:
                del variables.actionlist[i]
            self.UpdateDisplay()

    def DupeAction(self):
        ilist = [index.row() for index in self.ActionWidget.selectionModel().selectedRows()] #get the row numbers of all the selected items. 
        ilist.sort() #sorts the list from lowest to highest row
        for i in ilist:
            temp = variables.actionlist[i][:]
            variables.actionlist.append(temp)
            self.UpdateDisplay()
        
    def upAction(self):#function to move up an action
        if self.ActionWidget.currentRow() > 0:
            i = self.ActionWidget.currentRow()
            temp = variables.actionlist[i]
            variables.actionlist[i] = variables.actionlist[i - 1]
            variables.actionlist[i - 1] = temp
            self.UpdateDisplay()
            self.ActionWidget.setCurrentRow(i -1)

    def downAction(self):#function to move down an action
        if self.ActionWidget.currentRow() >= 0 and self.ActionWidget.currentRow() <= len(variables.actionlist) - 2:
            i = self.ActionWidget.currentRow()
            temp = variables.actionlist[self.ActionWidget.currentRow()]
            variables.actionlist[self.ActionWidget.currentRow()] = variables.actionlist[self.ActionWidget.currentRow() + 1]
            variables.actionlist[self.ActionWidget.currentRow() + 1] = temp
            self.UpdateDisplay()
            self.ActionWidget.setCurrentRow(i+1)            
            
    def GroupMove(self):
        if self.ActionWidget.currentRow() > 0:
            goal = self.MoveTo.value()
            ilist = [index.row() for index in self.ActionWidget.selectionModel().selectedRows()] #get the row numbers of all the selected items. 
            ilist.sort() #sorts the list from lowest to highest row
            goal = min(goal,len(variables.actionlist) - 1 - len(ilist))
            if goal<=ilist[0]:
                for i in ilist:
                    for k in range(ilist[0]-goal):
                        temp = variables.actionlist[i]
                        variables.actionlist[i] = variables.actionlist[i - 1]
                        variables.actionlist[i - 1] = temp
                        i-=1
            else : 
                ilist.reverse()
                for i in ilist:
                    for k in range(goal-ilist[0]+1):
                        temp = variables.actionlist[i]
                        variables.actionlist[i] = variables.actionlist[i + 1]
                        variables.actionlist[i + 1] = temp
                        i+=1
            self.UpdateDisplay()
            
    def UpdateDisplay(self):#updates the display of the actions
        j = self.ActionWidget.currentRow()
        self.ActionWidget.clear()
        for i in range(len(variables.actionlist)):
            x = variables.actionlist[i]
            actionstr = str(i) 
            for item in x:
                actionstr += ' ' + str(item)
            self.ActionWidget.addItem(actionstr)
        self.ActionWidget.setCurrentRow(j)
        return()
    
    def SaveAction(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', pathsave,"Action file (*.act)")
       
        with open(fname[0],'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t', quotechar='|')
            for action in variables.actionlist:
                writer.writerow(str(action))
        return()
    
    def LoadAction(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', pathsave,"Action file (*.act)")
        if fname != ('',''):
            with open(fname[0],'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
                for row in reader:
                    #exec('L = ' + ''.join(row))
                    code = 'self.a = ' + ''.join(row)
                    exec(code)
                    variables.actionlist.append(self.a)
            self.UpdateDisplay()
        return()
    
    def Runtime(self):
        EstimatedRuntime = timeEstimation.calculate()
        h = EstimatedRuntime//3600000
        m = EstimatedRuntime%3600000//60000
        s= EstimatedRuntime%3600000%60000//1000
        self.MessageDialogue(str(h)+'H'+str(m)+'m'+str(s)+'s')
    
    

#start stop

    def start(self):
        variables.id_in_process = self.startFromBox.value()
        variables.IsRunning = True
        variables.ExitCurrentAction = False

    def stop(self):
        variables.ExitCurrentAction = True
        variables.IsRunning = False
        variables.id_in_process = -1

    def next(self):
        variables.ExitCurrentAction = True
        variables.IsRunning = True
        variables.id_in_process += 1

    def UpdateStatus(self):#updates the label under the start button
        if variables.id_in_process != -1:
            self.Runninglabel.setText('Running ' + str(variables.id_in_process))
            
            #self.ActionWidget.setCurrentRow(variables.id_in_process)
        else:
            self.Runninglabel.setText('Stopped')






        
#Data querys


#plot
    
    def newPlotWindow(self):
        self.plotWindowlist.append(plotWindow.anotherPlot())
        self.plotWindowlist[-1].show()
        
    def updatePlotWindow(self):
        for x in self.plotWindowlist:
            x.plot()

    def PlotData(self):
        if variables.isPlotting:
            return()
        variables.isPlotting = True
        self.updatePlotWindow()
        #L = [self.YplotBox_2.currentIndex(),self.YplotBox_3.currentIndex(),self.YplotBox_4.currentIndex(),self.YplotBox_5.currentIndex(),self.YplotBox_6.currentIndex()]
        #print(len(self.LD[self.XplotBox.currentIndex()]),len(self.LD[self.YplotBox.currentIndex()]))
        isCleared= False
        for k in range(len(self.YplotList)):
            try:
                if self.YplotList[k].currentText() != 'None' and self.YplotList[k].currentText() != '' :
                    X,Y = variables.Data[self.XplotBox.currentText()][:],variables.Data[self.YplotList[k].currentText()][:]
                    if len(X) > 0 and len(Y) > 0 and len(Y) == len(X):
                        if not isCleared:
                            self.graphicsView.clear()
                            isCleared = True
                        pen = mkPen(color = self.colors_rgb[k])
                        self.graphicsView.plot(X,Y,pen = pen,symbol = '+',symbolBrush=self.colors_rgb[k],symbolPen = None)
            except:
                None
        # for k,i in enumerate(L):
        #     if i > 0:
        #         if len(self.LD[self.XplotBox.currentIndex()]) > 0 and len(self.LD[i-1]) > 0 and len(self.LD[i - 1]) == len(self.LD[self.XplotBox.currentIndex()]):
        #             pen = mkPen(color = self.colors_rgb[k])
                    
        #             self.graphicsView.plot(self.LD[self.XplotBox.currentIndex()],self.LD[i-1],pen = pen,symbol = '+',symbolBrush=self.colors_rgb[k],symbolPen = None)
        variables.isPlotting = False
        return()
    
    def Zchanged(self):
        variables.ZplotText = self.ZplotBox.currentText()
        try:
            if variables.ZplotText != 'None' and variables.ZplotText != '' :
                variables.Data_image = np.zeros((variables.Lx,variables.Ly))
                N = variables.ix + variables.Lx*variables.iy
                for k in range(N):
                    variables.Data_image[k%variables.Lx][k//variables.Lx] = variables.Data[self.ZplotBox.currentText()][k-N]
                self.Plot2D()
        except:
            None
    
    
    def Plot2D(self):
        if variables.is2DPlotting:
            return()
        variables.is2DPlotting = True
        self.imgView.setImage(variables.Data_image)
        variables.is2DPlotting = False
        
    
    
    
    def SharedBufferUpdate(self):
        self.measLabel.setText(str(variables.sharedbuffer[self.measBox.currentIndex()]))

        
       
#class called for each connected device and moved to their threads
class Worker(QtCore.QObject):


    def __init__(self,id,devObj):
        super().__init__()
        self.devObj = devObj
        self.id = id


    def run(self):
        while not variables.close:
            if len(variables.QueryList[self.id]) > 0:
                self.Query(variables.QueryList[self.id][0])
                #print(variables.QueryList[self.id])
                del variables.QueryList[self.id][0]
            sleep(0.001)   #decreasing from 0.005 to 0.001
        return()

    def Query(self,q):
        if q[0] == 'Write':
            self.devObj.Write(q[1][0],q[1][1:])#q = [Write,[Key,parameters]]
        if q[0] == 'Read':
            data = self.devObj.Read(q[1])#q = [Read,Key]
            for k in range(len(data)):
                variables.Data[data[k][0]].append(data[k][1])
        if q[0] == 'ReadwithoutSaving':#q = [Read,Key]
            data = self.devObj.Read(q[1])
            dev= int(q[1].split('_')[0])-1
            variables.sharedbuffer[dev] = data[0][1]
        return()
            

class LabelTool(QtWidgets.QDialog, Ui_Dialog): # class created to ask before closing pangolab and to ask confirmation before closing the program
    def __init__(self, parent=None):
        super(LabelTool, self).__init__(parent)
        self.setupUi(self)

    def verify_by_user(self):
        answer = QtWidgets.QMessageBox.question(
            self,
            "Close ?",
            "Are you sure that you want to quit?",
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No,
        )
        return answer == QtWidgets.QMessageBox.Yes

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            # self.close() I commented this, otherwise the escape button will also trigger the close event
            None
        else:
            super(LabelTool, self).keyPressEvent(event)

    # def closeEvent(self, event):



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    #ui.setupUi(Dialog)
    w = LabelTool()
    
    w.show()
    #Dialog.show() 
    sys.exit(app.exec_())

