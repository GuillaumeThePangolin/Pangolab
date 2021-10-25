# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 15:40:29 2021

@author: Drawings2
"""
from time import asctime
import csv
import variables


def SaveTemp():
    with open(variables.path + 'temp//Pangolab_'+ asctime().replace(':','_'),'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quotechar='|')
        row = []
        keys = list(variables.Data)
        writer.writerow(keys)
        for i in range(len(variables.Data[keys[0]])):#The time data is the one with the most elements
            row = []
            for key in keys:
                if i < len(variables.Data[key]):
                    row.append(variables.Data[key][i])
                else:
                    row.append(None)
            writer.writerow(row)