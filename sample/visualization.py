# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 12:40:28 2019

@author: PrachiRani
"""
import cv2
from os.path import join,basename

def draw_keys_test(image_path,folder_path,key_dict):
    image = cv2.imread(image_path)
    f=open(join(folder_path,basename(image_path)[:-4]+'_key_testing.txt'),'w')
    for i in range(len(key_dict['coordinates'])):
        key_x1,key_y1,key_x2,key_y2 = key_dict['coordinates'][i]
        f.write(str(i)+' --> '+key_dict['value'][i])
        f.write('\n')
        cv2.rectangle(image,(key_x1,key_y1),(key_x2,key_y2),(0,0,255),3)
        cv2.putText(image,str(i), (key_x1,key_y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
    f.close()
    cv2.imwrite(join(folder_path,basename(image_path)[:-4]+'_key_testing.jpg'),image)
    
def draw_boxes(image_path,folder_path,box_dict,word_dict,key_dict):
    image = cv2.imread(image_path)
    f=open(join(folder_path,basename(image_path)[:-4]+'_box_testing.txt'),'w')
    for i in range(len(box_dict['coordinates'])):
        [x1,y1,x2,y2] = box_dict['coordinates'][i]
        f.write('-'*30)
        f.write('\n\n')
        f.write('Box '+str(i)+':')
        f.write('\n\n')
        f.write('Keys in the box:')
        f.write('\n')
        for ki in box_dict['key_idxs'][i]:
            f.write(' | ')
            f.write(key_dict['value'][ki])
            f.write(' | ')
        f.write('\n')
        f.write('Words in the box:')
        f.write('\n')
        for wi in box_dict['word_idxs'][i]:
            f.write(' | ')
            f.write(word_dict['value'][wi])
            f.write(' | ')
        f.write('\n\n')
        f.write('-'*30)
        cv2.rectangle(image,(x1,y1),(x2,y2),(255,255,0),3)
        cv2.putText(image,str(i), (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0),2)
    f.close()
    cv2.imwrite(join(folder_path,basename(image_path)[:-4]+'_boxes.jpg'),image)
    
def visualization(key_dict,key_val,image_path,folder_path,box_dict,word_dict):
    image = cv2.imread(image_path)
    for item in key_val:
#        print("box drawn for ",item['key'])
        key_x1,key_y1,key_x2,key_y2 = item['key_coords']
        val_x1,val_y1,val_x2,val_y2 = item['val_coords']
        pair_x1 = min(key_x1,val_x1)
        pair_y1 = min(key_y1,val_y1)
        pair_x2 = max(key_x2,val_x2)
        pair_y2 = max(key_y2,val_y2)
        cv2.rectangle(image,(key_x1,key_y1),(key_x2,key_y2),(0,0,255),3)
        cv2.rectangle(image,(val_x1,val_y1),(val_x2,val_y2),(255,0,0),3)
        cv2.rectangle(image,(pair_x1,pair_y1),(pair_x2,pair_y2),(0,255,0),3)
    
    draw_keys_test(image_path,folder_path,key_dict)
    draw_boxes(image_path,folder_path,box_dict,word_dict,key_dict)
    
#    key_wo_value = list(set([x for x in key_dict['coordinates']]) - set([x['key_coords'] for x in key_val]))
    detected_keys_coords = [x['key_coords'] for x in key_val]
    for rect in key_dict['coordinates']:
        if rect in detected_keys_coords:
            pass
        else:
            x1,y1,x2,y2 = rect
            cv2.rectangle(image,(x1,y1),(x2,y2),(147,20,255),3)
        
    cv2.imwrite(join(folder_path,basename(image_path)[:-4]+'_visualization.jpg'),image)
    
        
        
    