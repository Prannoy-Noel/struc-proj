# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 17:24:58 2019

@author: PrachiRani
"""
from .verify_value import verify_value
from .detect_lines import detect_lines
from .table_extraction_tester import get_table_header,get_table_header1
from .table_extraction import table_extraction
from .table_extraction import cell_table_range_extraction
import numpy as np
import pandas as pd
import cv2

single_word_value_keys = ["Invoice_Date","Invoice_Number","Invoice_Net","Invoice_Tax_Amount","Invoice_Total","Currency","PO_Number","Supplier_Tax_Number","Supplier_Bank_Account_Number","Supplier_IBAN","Credit_Note","Supplier_Swift_Code","Delivery_Note_Number"]
multi_word_value_keys = ["Supplier_Name_and_Address","Bill_to_Name_and_Address","Ship_to"]
table_single_word_value_keys = ["Unit_Price","Line_Net_Amount","Line_Tax_Amount","Line_Quantity","Line_Gross_Amount","Shipping/Freight_Amount","UoM"]
table_multi_word_value_keys = ["Line_Item","Material_Number","Line_Description"]
table_keys = table_single_word_value_keys+table_multi_word_value_keys


df = pd.read_csv('./../config/keys.csv')
key_type = {}
for i in range(df.shape[0]):
    key_type[df['Keys'][i]] = df['Type'][i]
def getKey1(item):
    return item[0]

def get_val_from_boxes(key_dict,word_dict,box_dict,disabled_words_idxs,key_val,found_keys):
    for i in range(len(box_dict['coordinates'])):
        keys_in_box = box_dict['key_idxs'][i]
        words_in_box = box_dict['word_idxs'][i]
        if len(keys_in_box)==1 and len(words_in_box)>0:
#            print(keys_in_box,words_in_box)
            if keys_in_box[0] not in found_keys:
                print('key - ',key_dict['value'][keys_in_box[0]])
                key_typ = key_type[key_dict['value'][keys_in_box[0]]]
                key_coord = key_dict['coordinates'][keys_in_box[0]]
                text = ''
                val_idxs = []
                for word in words_in_box:
                    word_coord = word_dict['coordinates'][word]
                    if word_coord[1]>key_coord[1]+10 or (word_coord[1]>key_coord[1]-10 and word_coord[0]>key_coord[2]):
                        text+=' ' +word_dict['value'][word]
                        val_idxs.append(word)
#                        disabled_words_idxs.append(word)
#                    print('text',text)
                if text.strip()!='' and verify_value(key_typ,text.strip()):
#                    print('val - ',text.strip())
                    val = text.strip()
                    disabled_words_idxs.extend(val_idxs)
                    val_x1 = min([word_dict['coordinates'][x1][0] for x1 in val_idxs])
                    val_y1 = min([word_dict['coordinates'][x1][1] for x1 in val_idxs])
                    val_x2 = max([word_dict['coordinates'][x1][2] for x1 in val_idxs])
                    val_y2 = max([word_dict['coordinates'][x1][3] for x1 in val_idxs])
                    val_coords = [val_x1,val_y1,val_x2,val_y2]
                    found_keys.append(keys_in_box[0])
                    key_val_temp ={'key_coords':key_dict['coordinates'][keys_in_box[0]], \
                           'val_coords':val_coords, \
                           'key':key_dict['value'][keys_in_box[0]], \
                           'value':val}
                    key_val.append(key_val_temp)

    return key_val,found_keys


def get_val_single_word(key_dict,word_dict,box_dict,disabled_words_idxs,key_val,found_keys):
    for key_idx in range(len(key_dict['value'])):
        if key_dict['value'][key_idx] in single_word_value_keys and key_idx not in found_keys:

            key_typ = key_type[key_dict['value'][key_idx]]
            if key_dict['side_match'][key_idx]['right']!=[]   \
                        and key_dict['side_match'][key_idx]['right'][0] not in disabled_words_idxs \
                        and verify_value(key_typ,word_dict['value'][key_dict['side_match'][key_idx]['right'][0]]):

                found_keys.append(key_idx)
                key_val_temp ={'key_coords':key_dict['coordinates'][key_idx], \
                               'val_coords':word_dict['coordinates'][key_dict['side_match'][key_idx]['right'][0]], \
                               'key':key_dict['value'][key_idx], \
                               'value':word_dict['value'][key_dict['side_match'][key_idx]['right'][0]]}
                key_val.append(key_val_temp)
                print("key - ",key_dict['value'][key_idx])
                print("val - ",word_dict['value'][key_dict['side_match'][key_idx]['right'][0]])
                print("-"*20)
                disabled_words_idxs.append(key_dict['side_match'][key_idx]['right'][0])
            elif key_dict['bottom_match'][key_idx]!=[] \
                        and key_dict['bottom_match'][key_idx][0] not in disabled_words_idxs \
                        and verify_value(key_typ,word_dict['value'][key_dict['bottom_match'][key_idx][0]]):

                found_keys.append(key_idx)
                key_val_temp ={'key_coords':key_dict['coordinates'][key_idx], \
                               'val_coords':word_dict['coordinates'][key_dict['bottom_match'][key_idx][0]], \
                               'key':key_dict['value'][key_idx], \
                               'value':word_dict['value'][key_dict['bottom_match'][key_idx][0]]}
                key_val.append(key_val_temp)
                print("key - ",key_dict['value'][key_idx])
                print("val - ",word_dict['value'][key_dict['bottom_match'][key_idx][0]])
                print("-"*20)
                disabled_words_idxs.append(key_dict['bottom_match'][key_idx])
            else:
                print("cant find value for ",key_dict['value'][key_idx])
    return key_val,found_keys
def get_val_multi_word(key_dict,paragraph_dict,word_dict,disabled_words_idxs,key_val,found_keys):
    for i in range(len(paragraph_dict['keys'])):
        if paragraph_dict['keys'][i]!=[]:
            keys_in_para = paragraph_dict['keys'][i]
            words_in_keys = [k for j in keys_in_para for k in key_dict['word_idxs'][j]]
#            print("wors in keys ",words_in_keys)
            for key_idx in keys_in_para:
                words_in_current_key = key_dict['word_idxs'][key_idx]
                if key_idx not in found_keys and key_dict['value'][key_idx] in multi_word_value_keys:
                    print('key - ',key_dict['value'][key_idx])
                    key_typ = key_type[key_dict['value'][key_idx]]
#                    for index in paragraph_dict['indices'][i]:
                    val = ''
                    val_idxs = []
#                    print(paragraph_dict['indices'][i],words_in_current_key)
                    try:
                        start = max(paragraph_dict['indices'][i].index(m) for m in words_in_current_key)+1
    #                    print(start)
    #                    print(paragraph_dict['indices'][i])
                        while start< len(paragraph_dict['indices'][i]) and paragraph_dict['indices'][i][start] not in words_in_keys:
                            val += word_dict['value'][paragraph_dict['indices'][i][start]]+' '
                            val_idxs.append(paragraph_dict['indices'][i][start])
                            disabled_words_idxs.append(paragraph_dict['indices'][i][start])
                            start+=1


                        if val.strip()!='' and verify_value(key_typ,val.strip()):
                            val_x1 = min([word_dict['coordinates'][x1][0] for x1 in val_idxs])
                            val_y1 = min([word_dict['coordinates'][x1][1] for x1 in val_idxs])
                            val_x2 = max([word_dict['coordinates'][x1][2] for x1 in val_idxs])
                            val_y2 = max([word_dict['coordinates'][x1][3] for x1 in val_idxs])
                            val_coords = [val_x1,val_y1,val_x2,val_y2]
                            key_val_temp ={'key_coords':key_dict['coordinates'][key_idx], \
                                   'val_coords':val_coords, \
                                   'key':key_dict['value'][key_idx], \
                                   'value':val}
                            key_val.append(key_val_temp)
                            print('val - ',val)
                            found_keys.append(key_idx)
                    except:
                        print("key text was not found inside paragraph while key was present")
#                    print(start)
#    print("xxxxxxxxxxxxxxxxxxxxxxx")
    for i in range(len(key_dict['value'])):
        if i not in found_keys and key_dict['value'][i] in multi_word_value_keys:
            print("key - ",key_dict['value'][i])
#            print("hh")
            key_typ = key_type[key_dict['value'][i]]
            [x1,y1,x2,y2] = key_dict['coordinates'][i]
            dist = []
            for j in range(len(paragraph_dict['keys'])):
                [x_1,y_1,x_2,y_2] = paragraph_dict['coordinates'][j]
                if x_1>=x1-20 and y_1>y1-20:
                    dist.append(np.sqrt(np.square(x_1-x1)+np.square(y_1-y1)))
                else:
                    dist.append(70000)
#            print(dist)
            if min(dist)<500:
#                print("found min dist box")
                nearest_para_idx = dist.index(min(dist))
                val = ''
                val_idxs = []
                key_words_in_nearest_para = [k for j in paragraph_dict['keys'][nearest_para_idx] for k in key_dict['word_idxs'][j]]
                start = 0
                while start< len(paragraph_dict['indices'][nearest_para_idx]) and paragraph_dict['indices'][nearest_para_idx][start] not in key_words_in_nearest_para:
                    val += word_dict['value'][paragraph_dict['indices'][nearest_para_idx][start]]+' '
                    val_idxs.append(paragraph_dict['indices'][nearest_para_idx][start])
                    disabled_words_idxs.append(paragraph_dict['indices'][nearest_para_idx][start])
                    start+=1
                if val.strip()!='' and verify_value(key_typ,val.strip()):
                    val_x1 = min([word_dict['coordinates'][x1][0] for x1 in val_idxs])
                    val_y1 = min([word_dict['coordinates'][x1][1] for x1 in val_idxs])
                    val_x2 = max([word_dict['coordinates'][x1][2] for x1 in val_idxs])
                    val_y2 = max([word_dict['coordinates'][x1][3] for x1 in val_idxs])
                    val_coords = [val_x1,val_y1,val_x2,val_y2]
                    key_val_temp ={'key_coords':key_dict['coordinates'][i], \
                           'val_coords':val_coords, \
                           'key':key_dict['value'][i], \
                           'value':val}
                    key_val.append(key_val_temp)
                    print('val - ',val)
                    found_keys.append(i)
    return key_val,found_keys
def prepare_for_table(box_dict,key_dict,word_dict,image_path,word_blob_list,disabled_words_idxs,w,found_keys):

    table_KV_dict_page=[]
    table_KV_dict_coords_page = []
    adj_box_status = [False]*len(box_dict['coordinates'])
    for i in range(len(box_dict['coordinates'])):
#        print(i,len(box_dict['coordinates']))
#        print('for table ',box_dict['coordinates'][i])
#        print('for table ',box_dict['key_idxs'][i])
#        print('for table ',box_dict['word_idxs'][i])
        if len(box_dict['key_idxs'][i])>1 and box_dict['coordinates'][i][2]-box_dict['coordinates'][i][0]>0.6*w:
#            print('first if')
            table_KV_dict = {}
            relevant_key_dict ={'coordinates':[],'value':[],'bottom_match':[],'index':[],'side_match':[],'word_idxs':[]}
            for idx in box_dict['key_idxs'][i]:
                if key_dict['value'][idx] in table_keys and key_dict['value'][idx] not in relevant_key_dict['value']:
#                    print("box coords ",box_dict['coordinates'][i])
                    relevant_key_dict['coordinates'].append(key_dict['coordinates'][idx])
                    relevant_key_dict['value'].append(key_dict['value'][idx])
                    relevant_key_dict['bottom_match'].append(key_dict['bottom_match'][idx])
                    relevant_key_dict['index'].append(key_dict['index'][idx])
                    relevant_key_dict['side_match'].append(key_dict['side_match'][idx])
                    relevant_key_dict['word_idxs'].append(key_dict['word_idxs'][idx])

            if len(relevant_key_dict['value'])==0:
                pass
            else:

                table_header_dict = get_table_header(relevant_key_dict,box_dict['coordinates'][i])

                if len(table_header_dict['coordinates'])>0:

                    table_KV_dict,table_KV_dict_coords = table_extraction(word_dict,table_header_dict,image_path,box_dict['coordinates'][i],word_blob_list,disabled_words_idxs,[])

                    table_KV_dict_coords_page.append(table_KV_dict_coords)
                    table_KV_dict_page.append(table_KV_dict)
                    for h in range(len(relevant_key_dict['index'])):
                        found_keys.append(relevant_key_dict['index'][h])


        if  not adj_box_status[i] and len(box_dict['key_idxs'][i]) >= len(box_dict['word_idxs'][i]) and key_dict['value'][box_dict['key_idxs'][i][0]] in table_keys:
#            print("second if")
#            print("$"*20)
#            print("box with one key inside ",key_dict['value'][box_dict['key_idxs'][i][0]])
            box = box_dict['coordinates'][i]
            relevant_key_dict ={'coordinates':[],'value':[],'bottom_match':[],'index':[],'side_match':[],'word_idxs':[]}
            adjacent_boxes = [i]
            adj_box_status[i] = True
            for j in range(len(box_dict['coordinates'])):
                box_ = box_dict['coordinates'][j]
                if not adj_box_status[j] and abs(box_[1]-box[1])<10 and abs(box_[3]-box[3])<10 and key_dict['value'][box_dict['key_idxs'][j][0]] in table_keys:
                    adjacent_boxes.append(j)
                    adj_box_status[j] = True
            for item in adjacent_boxes:
                if key_dict['value'][box_dict['key_idxs'][item][0]] not in relevant_key_dict['value']:
                    relevant_key_dict['coordinates'].append(box_dict['coordinates'][item])

                    relevant_key_dict['value'].append(key_dict['value'][box_dict['key_idxs'][item][0]])
                    relevant_key_dict['bottom_match'].append(key_dict['bottom_match'][box_dict['key_idxs'][item][0]])
                    relevant_key_dict['index'].append(key_dict['index'][box_dict['key_idxs'][item][0]])
                    relevant_key_dict['side_match'].append(key_dict['side_match'][box_dict['key_idxs'][item][0]])
                    relevant_key_dict['word_idxs'].append(key_dict['word_idxs'][box_dict['key_idxs'][item][0]])
            if len(relevant_key_dict['value'])==0:
                pass
            else:
                x1 = min([x[0] for x in relevant_key_dict['coordinates'] ])
                y1 = min([x[1] for x in relevant_key_dict['coordinates'] ])
                x2 = max([x[2] for x in relevant_key_dict['coordinates'] ])
                y2 = max([x[3] for x in relevant_key_dict['coordinates'] ])
                header_range = [x1,y1,x2,y2]
#                relevant_key_dict1={}
#                print("yyyy",relevant_key_dict)
                indexes = sorted(range(len(relevant_key_dict['coordinates'])),key=lambda k: relevant_key_dict['coordinates'][k][0])
                relevant_key_dict1={'coordinates':[],'value':[],'bottom_match':[],'index':[],'side_match':[],'word_idxs':[]}
                for i,index in enumerate(indexes):
                    relevant_key_dict1['value'].append(relevant_key_dict['value'][index])
                    relevant_key_dict1['coordinates'].append(relevant_key_dict['coordinates'][index])
                    relevant_key_dict1['bottom_match'].append(relevant_key_dict['bottom_match'][index])
                    relevant_key_dict1['index'].append(relevant_key_dict['index'][index])
                    relevant_key_dict1['side_match'].append(relevant_key_dict['side_match'][index])
                    relevant_key_dict1['word_idxs'].append(relevant_key_dict['word_idxs'][index])
#                relevant_key_dict1['coordinates'] = relevant_key_dict['coordinates']
                table_header_dict = get_table_header1(relevant_key_dict1,header_range)



#                print("table header dict",table_header_dict)
                if len(table_header_dict['coordinates'])>1:
                    table_KV_dict = {}
                    table_KV_dict_coords = {}
#                    try:
                    table_range,table_row  = cell_table_range_extraction(word_dict,table_header_dict,disabled_words_idxs)
                    print("table_range",table_range)
                    table_KV_dict,table_KV_dict_coords = table_extraction(word_dict,table_header_dict,image_path,table_range,word_blob_list,disabled_words_idxs,table_row)
#                    except:
#                        pass
                    table_KV_dict_coords_page.append(table_KV_dict_coords)
                    table_KV_dict_page.append(table_KV_dict)
                    for h in range(len(relevant_key_dict1['index'])):
                        found_keys.append(relevant_key_dict1['index'][h])
#                print("table header ",table_header_dict)

#        print(i,len(box_dict['coordinates']))
#        print('-'*20)
#    print("found keys",found_keys)
    relevant_key_dict ={'coordinates':[],'value':[],'bottom_match':[],'index':[],'side_match':[],'word_idxs':[]}
    for i in range(len(key_dict['value'])):
        if i not in found_keys and key_dict['value'][i] in table_keys and key_dict['value'][i] not in relevant_key_dict['value']:

            relevant_key_dict['coordinates'].append(key_dict['coordinates'][i])
            relevant_key_dict['value'].append(key_dict['value'][i])
            relevant_key_dict['bottom_match'].append(key_dict['bottom_match'][i])
            relevant_key_dict['index'].append(key_dict['index'][i])
            relevant_key_dict['side_match'].append(key_dict['side_match'][i])
            relevant_key_dict['word_idxs'].append(key_dict['word_idxs'][i])
#    print("zzzzzzzz",relevant_key_dict)
    if len(relevant_key_dict['value'])==0:
        pass
    else:
        x1 = min([x[0] for x in relevant_key_dict['coordinates'] ])
        y1 = min([x[1] for x in relevant_key_dict['coordinates'] ])
        x2 = max([x[2] for x in relevant_key_dict['coordinates'] ])
        y2 = max([x[3] for x in relevant_key_dict['coordinates'] ])

        indexes = sorted(range(len(relevant_key_dict['coordinates'])),key=lambda k: relevant_key_dict['coordinates'][k][0])
#        print("indexes",indexes)
        relevant_key_dict1={'coordinates':[],'value':[],'bottom_match':[],'index':[],'side_match':[],'word_idxs':[]}
        for i,index in enumerate(indexes):
            relevant_key_dict1['value'].append(relevant_key_dict['value'][index])
            relevant_key_dict1['coordinates'].append(relevant_key_dict['coordinates'][index])
            relevant_key_dict1['bottom_match'].append(relevant_key_dict['bottom_match'][index])
            relevant_key_dict1['index'].append(relevant_key_dict['index'][index])
            relevant_key_dict1['side_match'].append(relevant_key_dict['side_match'][index])
            relevant_key_dict1['word_idxs'].append(relevant_key_dict['word_idxs'][index])

        header_range = [x1,y1,x2,y2]
#        print("header range",header_range)
        table_header_dict = get_table_header(relevant_key_dict1,header_range)
        x1 = min([x[0] for x in table_header_dict['coordinates'] ])
        y1 = min([x[1] for x in table_header_dict['coordinates'] ])
        x2 = max([x[2] for x in table_header_dict['coordinates'] ])
        y2 = max([x[3] for x in table_header_dict['coordinates'] ])
#        print("table w/o lines detected")
#        print(table_header_dict)
        if len(table_header_dict['coordinates'])>1:
            table_KV_dict = {}
            table_KV_dict_coords = {}

            lines = detect_lines(box_dict['coordinates'],word_dict,image_path)
            table_range_y = []
            for line in lines:
                [(x_1,y_1),(x_2,y_2)] = line
                if (y_1-y_2)<20 and y_1>y2+50:
                    table_range_y.append(y_1)
            if table_range_y != []:
                table_range = [x1,y1,x2,min(table_range_y)]
            else:
                img=cv2.imread(image_path)
                img_height = img.shape[0]
                table_range = [x1,y1,x2,img_height]
            table_KV_dict,table_KV_dict_coords = table_extraction(word_dict,table_header_dict,image_path,table_range,word_blob_list,disabled_words_idxs,[])
            table_KV_dict_coords_page.append(table_KV_dict_coords)
            table_KV_dict_page.append(table_KV_dict)
            for h in range(len(relevant_key_dict1['index'])):
                found_keys.append(relevant_key_dict1['index'][h])

    return table_KV_dict_page,table_KV_dict_coords_page,found_keys




def get_val(key_dict,word_dict,box_dict,disabled_words_idxs,paragraph_dict,image_path,word_blob_list):
    key_val =[]
    found_keys=[]
    img = cv2.imread(image_path)
    w=img.shape[1]
    key_val,found_keys = get_val_from_boxes(key_dict,word_dict,box_dict,disabled_words_idxs,key_val,found_keys)
    key_val,found_keys = get_val_single_word(key_dict,word_dict,box_dict,disabled_words_idxs,key_val,found_keys)
    key_val,found_keys = get_val_multi_word(key_dict,paragraph_dict,word_dict,disabled_words_idxs,key_val,found_keys)
#    try:
    table_KV_dict_page,table_KV_dict_coords_page,found_keys = prepare_for_table(box_dict,key_dict,word_dict,image_path,word_blob_list,disabled_words_idxs,w,found_keys)
#    except:
#        table_KV_dict_page = []
    return key_val,table_KV_dict_page,table_KV_dict_coords_page
