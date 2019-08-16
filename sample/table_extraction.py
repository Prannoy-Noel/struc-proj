# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 14:25:25 2019

@author: DarshilKapadia
"""

import cv2
import pandas as pd
import re
from verify_value import verify_value

def cell_table_extraction(word_dict,table_header_dict,disabled):
    table_df = pd.DataFrame(columns=table_header_dict['value'])
    temp_ = {}
    key_val_temp =[]
    for i in range(len(table_header_dict['coordinates'])):
        key_val_temp.append({'key':table_header_dict['value'][i],'key_coords':table_header_dict['coordinates'][i],'value':[],'val_coords':[]})
    
    for i in range(len(table_header_dict['value'])):
        
        header = table_header_dict['coordinates'][i]
        print("header ",header)
        temp_[table_header_dict['value'][i]]=[]
        for j in range(len(word_dict['value'])):
            val = word_dict['coordinates'][j]
            
            if j not in disabled and abs(header[0]-val[0])<10 and abs(header[2]-val[2])<10 and abs(val[1]-header[3])<10:
                print("val ",val )
                temp_[table_header_dict['value'][i]].append(word_dict['value'][j])
                key_val_temp[i]['value'].append(word_dict['value'][j])
                key_val_temp[i]['val_coords'].append(word_dict['coordinates'][j])
                header = val
    table_df = table_df.append(temp_,ignore_index=True)
    table_KV_dict = table_df.to_dict(orient='list')
    print(table_KV_dict)
    table_KV_dict_ ={}
    for key,val in table_KV_dict.items():
#        print(item)
#        key = list(item.keys())[0]
#        val = list(item.values())[0]
        table_KV_dict_[key] = val[0]
    return table_KV_dict_,key_val_temp
def table_extraction(word_dict,table_header_dict,image_path,table_range,word_blob_list,disabled_words_idxs,table_row,anchor_key=None):
    print("table_range",table_range)
#    key_val = []
    config_path = './../config/keys.csv'
    df = pd.read_csv(config_path)
    key_val_temp =[]
    print(table_header_dict)
    for i in range(len(table_header_dict['coordinates'])):
        key_val_temp.append({'key':table_header_dict['value'][i],'key_coords':table_header_dict['coordinates'][i],'value':[],'val_coords':[]})
    '''
    Identify the anchor key if not explicitly given 
    '''
    if anchor_key==None:
        for i in range(len(table_header_dict['value'])):    
            if df[df['Keys']==table_header_dict['value'][i]]['Type'].values[0] == 'Number':
                print("yes")
                anchor_key_idx = i
                print(table_header_dict['value'])
                print(anchor_key_idx)
                anchor_key = table_header_dict['value'][anchor_key_idx]
                break
    else:
        anchor_key_idx = [x for x in table_header_dict['value']].index(anchor_key)
    print("anchor key",anchor_key)
#    print(anchor_key_idx)
#    if anchor_key == None:
        
    '''
    End
    '''
    table_KV_dict ={}
    '''
    Find Values of the Anchor key
    '''
        
    anchor_key_entries=[]
    try:
        anchor_coords = table_header_dict['coordinates'][anchor_key_idx]
    #        key_val_temp = {'key':table_header_dict['value'][anchor_key_idx],'key_coords':table_header_dict['coordinates'][anchor_key_idx],'value':[],'val_coords':[]}
        anchor_column_width = table_header_dict['column_range'][anchor_key_idx]
        for i in range(len(word_dict['coordinates'])):
            [x1,y1,x2,y2] = word_dict['coordinates'][i]
            if (x1<anchor_column_width[0] or x2>anchor_column_width[1]) or (y1<anchor_coords[3] or y2>table_range[3]):
            # value should be within column width-X axis and within box-Y axis
                continue
            print(word_dict['value'][i])
            if re.match('^\d*\.?\d*$',word_dict['value'][i]) != None:
                
                anchor_key_entries.append({'value':word_dict['value'][i],'coordinates':word_dict['coordinates'][i]})
    #                key_val_temp_+str(table_header_dict['value'][anchor_key_idx])['val'].append(word_dict['value'][i])
    #                key_val_temp_+str(table_header_dict['value'][anchor_key_idx])['val_coords'].append(word_dict['coordinates'][i])
    #        key_val.append(key_val_temp)
        '''
        End
        '''
        print(anchor_key_entries)
        
    except:
        print("xxxxxxxxxxx")
        pass
    
    '''
    Initiate the table
    '''
    
    table_df = pd.DataFrame(columns=table_header_dict['value'])
    if len(anchor_key_entries)>len(table_row):
        disabled_words_idxs = []
        table_df[table_df.columns[anchor_key_idx]] = [x['value'] for x in anchor_key_entries]
        '''
        End
        '''
        print(table_df)
        
        '''
        Populate the table
        '''
        img_temp = cv2.imread(image_path)
        #img_temp = img_temp[1140:2189,230:2182]
        for entry_idx,anchor_entry in enumerate(anchor_key_entries):
            entry_height_range=[anchor_entry['coordinates'][1],anchor_entry['coordinates'][3]]
            for column_idx in range(len(table_header_dict['value'])):
                
                if column_idx == anchor_key_idx:
                    key_val_temp[column_idx]['value'].append(anchor_key_entries[entry_idx]['value'])
                    key_val_temp[column_idx]['val_coords'].append(anchor_key_entries[entry_idx]['coordinates'])
                    continue
                cell_limits = [table_header_dict['column_range'][column_idx][0],entry_height_range[0],table_header_dict['column_range'][column_idx][1],entry_height_range[1]]
                cv2.rectangle(img_temp,(cell_limits[0],cell_limits[1]),(cell_limits[2],cell_limits[3]),(127,127,0),3)
#                cv2.imshow('',cv2.resize(img_temp,(600,600)))
#                cv2.waitKey()
                type_column = df[df['Keys']==table_header_dict['value'][column_idx]]['Type'].values[0]
        #        print(type_column)
                if type_column in ['Number','AlphaNumeric','Currency']:
                    cell_text_list = []
                    cell_text_coords = []
                    for w_idx in range(len(word_dict['coordinates'])):
                        w_coords = word_dict['coordinates'][w_idx]
                        if w_coords[0] >= table_header_dict['column_range'][column_idx][0] and w_coords[2] <= table_header_dict['column_range'][column_idx][1] and w_idx not in disabled_words_idxs :
    #                            print(min(entry_height_range[1],w_coords[3]) , max(entry_height_range[0],w_coords[1]))
                            if min(entry_height_range[1],w_coords[3]) > max(entry_height_range[0],w_coords[1]):
                                overlap_height = min(entry_height_range[1],w_coords[3]) - max(entry_height_range[0],w_coords[1])
                            else:
                                overlap_height = 0
                            if  overlap_height > 0.6*min(entry_height_range[1]-entry_height_range[0],w_coords[3]-w_coords[1]):
                                # enter
    #                            print(table_df[table_df.columns[column_idx]])
                                if verify_value(df[df['Keys']==table_header_dict['value'][column_idx]]['Type'].values[0],word_dict['value'][w_idx]):
                                    cell_text_list.append(word_dict['value'][w_idx])
                                    cell_text_coords.append(word_dict['coordinates'][w_idx])
                                entry_height_range = [min(entry_height_range[0],word_dict['coordinates'][w_idx][1]),max(entry_height_range[1],word_dict['coordinates'][w_idx][3])]
                    table_df[table_df.columns[column_idx]][entry_idx] = ' '.join(cell_text_list)
                    print(key_val_temp,column_idx)
                    try:
                        x1 = min([x[0] for x in cell_text_coords])
                        y1 = min([x[1] for x in cell_text_coords])
                        x2 = max([x[2] for x in cell_text_coords])
                        y2 = max([x[3] for x in cell_text_coords])
                        val_coords = [x1,y1,x2,y2]
                    except:
                        val_coords = []
                    
                    key_val_temp[column_idx]['value'].append(' '.join(cell_text_list))
                    key_val_temp[column_idx]['val_coords'].append(val_coords)
                elif type_column in ['Blob']:
                    cell_text_coords = []
                    cell_text_list = []
                    for w_blob in word_blob_list:
                        w_coords = w_blob['coordinates']
                        if w_coords[0] >= table_header_dict['column_range'][column_idx][0] and w_coords[2] <= table_header_dict['column_range'][column_idx][1] :
                            print('*'*20)
    #                            print(entry_height_range,w_coords)
                            if min(entry_height_range[1],w_coords[3]) > max(entry_height_range[0],w_coords[1]):
                                overlap_height = min(entry_height_range[1],w_coords[3]) - max(entry_height_range[0],w_coords[1])
                            else:
                                overlap_height = 0
    #                            print(overlap_height)
                            if  overlap_height > 0.6*min(entry_height_range[1]-entry_height_range[0],w_coords[3]-w_coords[1]):
                                # enter
                                print("blob overlap ok")
    #                                print(table_df[table_df.columns[column_idx]])
                                cell_text_list.append(w_blob['value'])
                                cell_text_coords.append(w_blob['coordinates'])
                                entry_height_range = [min(entry_height_range[0],w_blob['coordinates'][1]),max(entry_height_range[1],w_blob['coordinates'][3])]
                    table_df[table_df.columns[column_idx]][entry_idx] = ' '.join(cell_text_list)
                    print(key_val_temp,column_idx)
                    try:
                        x1 = min([x[0] for x in cell_text_coords])
                        y1 = min([x[1] for x in cell_text_coords])
                        x2 = max([x[2] for x in cell_text_coords])
                        y2 = max([x[3] for x in cell_text_coords])
                        val_coords = [x1,y1,x2,y2]
                    except:
                        val_coords = []
                    
                    key_val_temp[column_idx]['value'].append(' '.join(cell_text_list))
                    key_val_temp[column_idx]['val_coords'].append(val_coords)
        table_KV_dict = table_df.to_dict(orient='list')
    else:
        table_KV_dict,key_val_temp = cell_table_extraction(word_dict,table_header_dict,disabled_words_idxs)
    #    except:
    #        pass
        '''
        End
        '''
        '''
        Preparing Output Dictionary
        '''
        
        
        '''
        End
        '''
        
        '''
        img = cv2.imread(image_path)  
        for w_blob in word_blob_list:
            cood = w_blob['coordinates']
            cv2.rectangle(img,(cood[0],cood[1]),(cood[2],cood[3]),(255,0,0),3)
        for i in range(len(table_header_dict['coordinates'])):
            key_coord = table_header_dict['coordinates'][i]
            cv2.rectangle(img,(key_coord[0],key_coord[1]),(key_coord[2],key_coord[3]),(0,0,255),3)
            
        #table_cropped_img = img[1140:2189,230:2182]
        table_cropped_img = img
        cv2.imwrite(image_path[:-4]+'_blobs.jpg',table_cropped_img)
        #cv2.imshow('',cv2.resize(table_cropped_img,(600,600)))
        #cv2.waitKey()
        '''
#    print("key_val_temp",key_val_temp)
    #    for i in range(len(table_header_dict['coordinates'])):
    #        key_val.append(key_val_temp_+str(table_header_dict['value'][i]))
    return table_KV_dict,key_val_temp



def cell_table_range_extraction(word_dict,table_header_dict,disabled):
#    table_df = pd.DataFrame(columns=table_header_dict['value'])
#    temp_ = {}
#    table_val_coords = []
    table_row = []
    x_0 = min([x[0] for x in table_header_dict['coordinates']])
    x_1 = max([x[2] for x in table_header_dict['coordinates']])
    y_0 = min([x[1] for x in table_header_dict['coordinates']])
#    for i in range(len(table_header_dict['value'])):
    
    header = table_header_dict['coordinates'][0]
    print("header ",header)
#        temp_[table_header_dict['value'][i]]=[]
    for j in range(len(word_dict['value'])):
        val = word_dict['coordinates'][j]
#            try:
        if abs(header[0]-val[0])<10 and abs(header[2]-val[2])<10 and abs(val[1]-header[3])<10:
            print("val ",val )
#            temp_[table_header_dict['value'][i]].append(word_dict['value'][j])
            header = val
            y_1 = header[3]
            table_row.append(y_1)
        else:
            y_1 = header[3]
#                print("table range ", [x_0, y_0, x_1, y_1])
#                break
#            except:
#                
#                continue
    
    return [x_0, y_0, x_1, y_1],table_row
    


