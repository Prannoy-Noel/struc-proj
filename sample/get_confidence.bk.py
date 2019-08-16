# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 16:47:52 2019

@author: FaizQureshi
"""

import math
import statistics
from PIL import Image
import json


def getConfidence(keyVal, tkvcd, imgPath):
    
    kvMult = 0.8
    tableMult = 1
    
    if (keyVal):
        keyValConf, conf = getConfidenceKV(keyVal, imgPath, kvMult)
    else:
        keyValConf = []
        conf = []
    if (tkvcd):
        keyValConfTable, confTable = getConfidenceTable(tkvcd, imgPath, tableMult)
    else:
        keyValConfTable = []
        confTable = []
        
    confidence = [i for i in conf+confTable if i]
    docConf = statistics.median(confidence) if confidence else None
    return keyValConf, keyValConfTable, docConf
            
def getConfidenceTable(tkvcd, imgPath, multiplier):
    table_key_val_doc = []
    confidence = []
    for table in tkvcd :
        tkvd_list = []
        for kv in table:
            tkvd_dict = {}
            tkvd_dict[kv['key']] = kv['value']
            conf = []
            for val_coord in kv['val_coords']:
                conf.append(computeConfidence(kv['key_coords'], val_coord, imgPath, multiplier))
            tkvd_dict['confidence'] = conf
            confidence += conf
            tkvd_list.append(tkvd_dict)
        table_key_val_doc.append(tkvd_list)
    return table_key_val_doc, confidence
    
def getConfidenceKV(inJson, imgPath, multiplier):
    i = 0
    confidence = []
    key_val = inJson
    for kv in key_val:
        if(kv['val_coords']):
            confidence.append(computeConfidence(kv['key_coords'], kv['val_coords'], imgPath, multiplier))
            key_val[i]['confidence'] = confidence[i]
            i += 1
        else:
            key_val[i]['confidence'] = None
    return key_val, confidence
    

def computeConfidence(keyCoords, valCoords, imgPath, multiplier):
    keyXYs = mapXYs (keyCoords)
    valXYs = mapXYs (valCoords)
    distance = findDistance(keyXYs,valXYs)
    return normalize(distance, imgPath, multiplier)

def mapXYs(coords):
    coordXY = []
    coordXY.append((int(coords[0]), int(coords[1])))
    coordXY.append((int(coords[2]), int(coords[1])))
    coordXY.append((int(coords[2]), int(coords[3])))
    coordXY.append((int(coords[0]), int(coords[3])))
    return coordXY
  

def findDistance(keyXY, valXY):
    keyMids = findMids(keyXY)
    valMids = findMids(valXY)
    minDist = 10**7
    for keyMid in keyMids:
        for valMid in valMids:
            dist = math.sqrt((keyMid[0]-valMid[0])**2 + (keyMid[1]-valMid[1])**2)
            minDist = dist if  (dist<minDist) else minDist
    return minDist

def findMids(XY):
    mids = []
    i = 0
    j = i + 1
    while (i < 4):
        xm = (XY[i][0] + XY[j][0])/2
        ym = (XY[i][1] + XY[j][1])/2
        mids.append((xm,ym))
        i += 1
        j = (i+1) if (i<3) else 0     
    return mids   

def normalize(distance, imgPath, multiplier): 
    im = Image.open(imgPath)
    semiDiag = math.sqrt(im.size[0]**2 + im.size[1]**2) * multiplier
    distance = distance/semiDiag if (distance/semiDiag < 1) else 1
    return round(((1-distance)**2),4)

def read(inPath):
    with open (inPath) as jsonFile:
        content = json.load(jsonFile)
    jsonFile.close()
    return content
    
