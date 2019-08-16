# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:30:13 2019

@author: DarshilKapadia
"""

from pyzbar.pyzbar import decode
from PIL import Image

def get_barcode_coords(image_path):
    result = decode(Image.open(image_path))
    
    barcode_coords=[]
    for r in result:
        [x,y,w,h] = r.rect
#        [x,y,w,h] = cv2.minAreaRect(np.array(r.polygon))
        barcode_coords.append([x,y,x+w,y+h])
        
    return barcode_coords

if __name__ == '__main__':
    
    import os
    import cv2
    
    
#    image_path = r'C:\Users\DarshilKapadia\Desktop\RICOH\Data\42 Invoice Copies\42 Invoice Copies\Internal\7_000001.tif'
#    barcode_coords = get_barcode_info(image_path)
    
    
    direct = r'C:\Users\DarshilKapadia\Desktop\RICOH\Data\42 Invoice Copies\42 Invoice Copies\Internal'
    for files in os.listdir(direct):
        if files.endswith('.tif'):
            image_path = os.path.join(direct,files)
            img = cv2.imread(image_path)
            barcode_coords = get_barcode_info(image_path)
            for br in barcode_coords:
                cv2.rectangle(img,(br[0],br[1]),(br[2],br[3]+int(1.0*(br[3]-br[1]))),(0,255,0),3)
            cv2.imshow('',cv2.resize(img,(700,700)))
            cv2.waitKey()
            cv2.destroyAllWindows()
            