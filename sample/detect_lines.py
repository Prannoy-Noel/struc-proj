# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 17:53:13 2019

@author: PrachiRani
"""
import cv2
import numpy as np
def detect_lines(box_coords,word_dict,image_path):
    img = cv2.imread(image_path)
    detected_lines=[]
    for box in box_coords:
        x1,y1,x2,y2 = box
        detected_lines += [[(x1,y1),(x2,y1)],[(x1,y1),(x1,y2)],[(x2,y1),(x2,y2)],[(x1,y2),(x2,y2)]]
        cv2.fillConvexPoly(img, np.array([[x1-2,y1-2],[x2+2,y1-2],[x2+2,y2+2],[x1-2,y2+2]]), (255,255,255)) 
    for w_idx in range(len(word_dict['coordinates'])):
        x1,y1,x2,y2 = word_dict['coordinates'][w_idx]
        cv2.fillConvexPoly(img, np.array([[x1,y1],[x2,y1],[x2,y2],[x1,y2]]), (255,255,255)) 
    return detected_lines
#TODO: Include lines which doesn't make boxes