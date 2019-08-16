# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 17:01:03 2019

@author: PrachiRani
"""

import json
import os
import xlwt

def JSONtoExcel(op_folder):

    # op_folder = 'C:/Users/PrachiRani/Documents/RICOH/merged first time on 5th/destination/selected'
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sheet1')
    row=0
    ws.write(0,0,'File_Name')
    ws.write(0,1,'Key')
    ws.write(0,2,'Value')
    row +=1
    folders = os.listdir(op_folder)
    for folder in folders:
        if '.xls' in folder:
            continue
        print("doc:JSON ", folder)
        file = op_folder+'/'+folder+'/'+folder+'.json'
        if not os.path.exists(file):
            continue
        with open(file,'r') as f:
            data = json.load(f)
        for item in data:
            if type(item)== list:
                for i in range(len(item)):
                    dictionary = item[i]
                    for key in dictionary.keys():
                        if key!='confidence_score':
                            ws.write(row,0,folder)
                            ws.write(row,1,key)
                            ws.write(row,2,str(dictionary[key]))
                            row+=1
            else:
                if type(item) != type(dict()):
                    continue
                for key in item.keys():
                    if key!='confidence_score':
                        ws.write(row,0,folder)
                        ws.write(row,1,key)
                        ws.write(row,2,str(item[key]))
                        row+=1

    wb.save(op_folder+'/report.xls')
