# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 16:47:52 2019

@author: FaizQureshi
"""

import math
import statistics
from PIL import Image
import json


#Entry funtction for getConfidence module
def getConfidence(keyVal, tkvcd, imgPath):
    
    #Multipliers are to account for difference in the distance normalization for table key-values
    #In general, increasing a multiplier will boost the confidence scores
    kvMult = 0.8
    tableMult = 1
    
    keyValConf = []
    conf = []
    keyValConfTable = []
    confTable = []
    
    
    try:
        if (keyVal):
            keyValConf, conf = getConfidenceKV(keyVal, imgPath, kvMult)
        if (tkvcd):
            keyValConfTable, confTable = getConfidenceTable(tkvcd, imgPath, tableMult)
      
    except Exception as e:
        #Currently, any exception results in empty lists being returned
        print("Error while computing confidence: ", type(e), "\n", e)
        keyValConf, keyValConfTable = handleException(keyVal, tkvcd)
        #Can add a handler here
    
    finally:
        #Remove all None values 
        confidence = [i for i in conf+confTable if i]
        
        #Check if confidence is empty and calculate median accordingly
        docConf = statistics.median(confidence) if confidence else None
        
    return keyValConf, keyValConfTable, docConf
            



#Sub-function to get confidence values for table key-values
def getConfidenceTable(tkvcd, imgPath, multiplier):
    table_key_val_doc = []
    confidence = []
    
    #Parse tkvcd, compute confidence based on coords, build new table_key_val_doc object & return it
    for table in tkvcd :
        tkvd_list = []
        for kv in table:
            tkvd_dict = {}
            tkvd_dict[kv['key']] = kv['value']
            conf = []
            for val_coord, val in zip(kv['val_coords'], kv['value']):
                if val != '':
                    conf.append(computeConfidence(kv['key_coords'], val_coord, imgPath, multiplier))
#                else:
#                    conf.append(None)
            tkvd_dict['confidence'] = conf
            confidence += conf
            tkvd_list.append(tkvd_dict)
        table_key_val_doc.append(tkvd_list)
    return table_key_val_doc, confidence


#Sub-function to get confidence scores for regular key-values  
def getConfidenceKV(keyVal, imgPath, multiplier):
    i = 0
    confidence = []  
    #Parse keyVal, compute confidence based on coords, append confidence to keyVal & return it
    for kv in keyVal:
        if(kv['val_coords'] and kv['value'] != ''):
            confidence.append(computeConfidence(kv['key_coords'], kv['val_coords'], imgPath, multiplier))
            keyVal[i]['confidence'] = confidence[i]
            i += 1
#        else:
#            keyVal[i]['confidence'] = None
    return keyVal, confidence
  
#If exception occurs, return same object with -1 as confidecne
def handleException(keyVal, tkvcd):
    keyVal, tableKeyValDoc  = [[],[]]
    try:
        i = 0
        for kv in keyVal:
            keyVal[i]['confidence'] = -1
            i += 1 
            
        tableKeyValDoc = []
        for table in tkvcd :
            tkvd_list = []
            for kv in table:
                tkvd_dict = {}
                tkvd_dict[kv['key']] = kv['value']
                tkvd_dict['confidence'] = []
                for value in kv['value']:
                    tkvd_dict['confidence'].append(-1)
                tkvd_list.append(tkvd_dict)
            tableKeyValDoc.append(tkvd_list)
    except Exception as e:
        print("Exception occured (again): ", type(e), "\n", e)
    return keyVal, tableKeyValDoc

#Computes a confidence score based on the proximity of keyCoords and valCoords 
#imgPath is needed to ascertain image diagonal, which is used for distance normalization
def computeConfidence(keyCoords, valCoords, imgPath, multiplier):
    keyXYs = mapXYs (keyCoords)
    valXYs = mapXYs (valCoords)
    distance = findDistance(keyXYs,valXYs)
    return normalize(distance, imgPath, multiplier)


#Uses the top-left and bottom-right box coords to return coords of all 4 vertices
def mapXYs(coords):
    coordXY = []
    coordXY.append((int(coords[0]), int(coords[1])))
    coordXY.append((int(coords[2]), int(coords[1])))
    coordXY.append((int(coords[2]), int(coords[3])))
    coordXY.append((int(coords[0]), int(coords[3])))
    return coordXY
  
    
#Finds the minimum distance between the key and values boxes
def findDistance(keyXY, valXY):
    keyMids = findMids(keyXY)
    valMids = findMids(valXY)
    minDist = 10**7
    for keyMid in keyMids:
        for valMid in valMids:
            dist = math.sqrt((keyMid[0]-valMid[0])**2 + (keyMid[1]-valMid[1])**2)
            minDist = dist if  (dist < minDist) else minDist
    return minDist


#Finds the mid-points of the 4 edges of a box
def findMids(XY):
    mids = []
    i = 0
    j = i + 1
    while (i < 4):
        xm = (XY[i][0] + XY[j][0])/2
        ym = (XY[i][1] + XY[j][1])/2
        mids.append((xm,ym))
        i += 1
        j = (i + 1) if (i < 3) else 0     
    return mids   


#Does 2 things:
#1. Distance is mapped between 0 & 1 using the diagonal size and a multiplier
#2. Returns the confidence score, using the normalized distance as a penalty factor
def normalize(distance, imgPath, multiplier): 
    im = Image.open(imgPath)
    
    #semiDiag = diagonal * multiplier
    semiDiag = math.sqrt(im.size[0]**2 + im.size[1]**2) * multiplier
    
    #To ensure distance is between 0 & 1
    distance = distance/semiDiag if (distance/semiDiag < 1) else 1
    
    #Represents (1-x)^2 for x between 0 & 1 | Can try different polynomials here
    return round(((1-distance)**2),4)


def read(inPath):
    with open (inPath) as jsonFile:
        content = json.load(jsonFile)
    jsonFile.close()
    return content
    

if __name__ == '__main__':
    kvJson = r"C:/Users/FaizQureshi/Desktop/Ricoh/Data/SI/key_val_doc.json"
    tableJson = r"C:/Users/FaizQureshi/Desktop/Ricoh/Data/SI/table_key_val_coords_doc.json"
    kv = read(kvJson)
    tkvd = read(tableJson)
    imgPath = r'C:/Users/FaizQureshi/Desktop/Ricoh/Data/SI/24_00001.tif'
    key_val, table_key_val, docConf, _ = getConfidence(kv,tkvd,imgPath)