# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:11:44 2019

@author: DarshilKapadia
"""

import cv2

def draw_boxes(image_path,folder_path,key_dict,word_dict,box_dict,paragraph_dict,disabled_words_idxs):
    image = cv2.imread(image_path)
    for i in range(len(key_dict['coordinates'])):
        [x1,y1,x2,y2] = key_dict['coordinates'][i]
        cv2.rectangle(image,(x1,y1),(x2,y2),(0,0,255),3)
    cv2.imwrite(folder_path+image_path.split('/')[-1][:-4]+'_keys.jpg',image)
    image = cv2.imread(image_path)
    for i in range(len(word_dict['coordinates'])):
        if i not in disabled_words_idxs:
            [x1,y1,x2,y2] = word_dict['coordinates'][i]
            cv2.rectangle(image,(x1,y1),(x2,y2),(255,0,0),3)
    cv2.imwrite(folder_path+image_path.split('/')[-1][:-4]+'_words.jpg',image)
    image = cv2.imread(image_path)
    for i in range(len(box_dict['coordinates'])):
        [x1,y1,x2,y2] = box_dict['coordinates'][i]
        cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),3)
    cv2.imwrite(folder_path+image_path.split('/')[-1][:-4]+'_boxes.jpg',image)
    image = cv2.imread(image_path)
    for i in range(len(paragraph_dict['coordinates'])):
        [x1,y1,x2,y2] = paragraph_dict['coordinates'][i]
        cv2.rectangle(image,(x1,y1),(x2,y2),(255,0,255),3)
    cv2.imwrite(folder_path+image_path.split('/')[-1][:-4]+'_paragraphs.jpg',image)