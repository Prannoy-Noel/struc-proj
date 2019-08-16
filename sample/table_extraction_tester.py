# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 11:54:48 2019

@author: DarshilKapadia
"""

#import json
#from get_word_info import get_word_info
#from xml2json_datacap import convert
#from table_extraction import table_extraction


TABLE_SINGLE_WORD_VALUE_KEYS = ["Unit_Price","Line_Net_Amount","Line_Tax_Amount","Line_Quantity","Line_Gross_Amount","Delivery_Note_Number","Shipping/Freight_Amount","UoM"]
TABLE_MULTI_WORD_VALUE_KEYS = ["Line_Item","Material_Number","Line_Description"]
TABLE_KEYS = TABLE_MULTI_WORD_VALUE_KEYS + TABLE_SINGLE_WORD_VALUE_KEYS

#def table_extraction(key_dict):
#key_dict_path = './key_dict.json'
#anchor_key=None
#
#
#'''
#Initial data processing necessary for table extraction
#'''
#
#image_path = r'.\6_000001.tif'
#xml_path = r'.\6_000001c.xml'
#json_path = image_path[:-4]+'.json'
#convert(xml_path,json_path)
#word_dict,disabled_words_idxs = get_word_info(json_path)
#
#with open(key_dict_path) as (data_file):
#    key_dict = json.load(data_file)
#    
#table_range=[230,1140,2182,2189]
'''
End
'''

'''
Segregate Tabular keys
'''

#key_dict_for_table={'value':[],'coordinates':[],'bottom_match':[],'index':[],'side_match':[],'word_idxs':[]}
## Find tabular keys from detected keys' list
#for i in range(len(key_dict['coordinates'])):
#    if key_dict['value'][i].lower().strip() in [x.lower().strip() for x in TABLE_KEYS]:
#        key_dict_for_table['value'].append(key_dict['value'][i])
#        key_dict_for_table['coordinates'].append(key_dict['coordinates'][i])
#        key_dict_for_table['bottom_match'].append(key_dict['bottom_match'][i])
#        key_dict_for_table['index'].append(key_dict['index'][i])
#        key_dict_for_table['side_match'].append(key_dict['side_match'][i])
#        key_dict_for_table['word_idxs'].append(key_dict['word_idxs'][i])
#
'''
End
'''
        
'''
#Identify keys that make table headers
'''
def get_table_header(key_dict_for_table,table_range):
    key_groups=[]
        
    active_key_flag = [True]*len(key_dict_for_table['coordinates'])
#    print(active_key_flag)
    curr_group=[]
        
    curr_idx=0
    while(True):
        curr_idx+=1
        if curr_idx >= len(curr_group):
            key_groups.append(curr_group)
            curr_idx=0
            curr_group = [active_key_flag.index(True)]
        if active_key_flag[curr_group[curr_idx]]:
            [x1a,y1a,x2a,y2a] = key_dict_for_table['coordinates'][curr_group[curr_idx]]
            for w_jdx in range(len(key_dict_for_table['coordinates'])): 
                if w_jdx in curr_group or not active_key_flag[w_jdx]:
                    continue
                [x1b,y1b,x2b,y2b] = key_dict_for_table['coordinates'][w_jdx]
                
                if min(y2a,y2b) > max(y1a,y1b):
                    overlap_height = min(y2a,y2b) - max(y1a,y1b)
                else:
                    overlap_height = 0
                if  overlap_height > 0.6*min(y2a-y1a,y2b-y1b):
                    curr_group.append(w_jdx)
        
            active_key_flag[curr_group[curr_idx]] = False
        if not any(active_key_flag):
            break
#    print(active_key_flag)    
    key_groups.append(curr_group)
    key_group_len = [len(x) for x in key_groups]
    aligned_keys = key_groups[key_group_len.index(max(key_group_len)) ]
    aligned_keys = sorted(aligned_keys,key=lambda x:key_dict_for_table['coordinates'][x][0])
    table_header_dict={'value':[],'coordinates':[],'bottom_match':[],'index':[],'side_match':[],'word_idxs':[],'column_range':[]}
    for i in range(len(key_dict_for_table)):
        if i in aligned_keys:
            table_header_dict['value'].append(key_dict_for_table['value'][i])
            table_header_dict['coordinates'].append(key_dict_for_table['coordinates'][i])
            table_header_dict['bottom_match'].append(key_dict_for_table['bottom_match'][i])
            table_header_dict['index'].append(key_dict_for_table['index'][i])
            table_header_dict['side_match'].append(key_dict_for_table['side_match'][i])
            table_header_dict['word_idxs'].append(key_dict_for_table['word_idxs'][i])
            
    for i in range(len(table_header_dict['coordinates'])):
        if i == 0:
            left=table_range[0]
        else:
            left=table_header_dict['coordinates'][i-1][2] 
        if i == len(table_header_dict['coordinates'])-1:
            right=table_range[2]
        else:
            right=table_header_dict['coordinates'][i+1][0]
        table_header_dict['column_range'].append([left,right])
    return table_header_dict

def get_table_header1(key_dict_for_table,table_range):
    key_groups=[]
        
    active_key_flag = [True]*len(key_dict_for_table['coordinates'])
#    print(active_key_flag)
    curr_group=[]
        
    curr_idx=0
    while(True):
        curr_idx+=1
        if curr_idx >= len(curr_group):
            key_groups.append(curr_group)
            curr_idx=0
            curr_group = [active_key_flag.index(True)]
        if active_key_flag[curr_group[curr_idx]]:
            [x1a,y1a,x2a,y2a] = key_dict_for_table['coordinates'][curr_group[curr_idx]]
            for w_jdx in range(len(key_dict_for_table['coordinates'])): 
                if w_jdx in curr_group or not active_key_flag[w_jdx]:
                    continue
                [x1b,y1b,x2b,y2b] = key_dict_for_table['coordinates'][w_jdx]
                
                if min(y2a,y2b) > max(y1a,y1b):
                    overlap_height = min(y2a,y2b) - max(y1a,y1b)
                else:
                    overlap_height = 0
                if  overlap_height > 0.6*min(y2a-y1a,y2b-y1b):
                    curr_group.append(w_jdx)
        
            active_key_flag[curr_group[curr_idx]] = False
        if not any(active_key_flag):
            break
#    print(active_key_flag)    
    key_groups.append(curr_group)
    key_group_len = [len(x) for x in key_groups]
    aligned_keys = key_groups[key_group_len.index(max(key_group_len)) ]
    aligned_keys = sorted(aligned_keys,key=lambda x:key_dict_for_table['coordinates'][x][0])
    table_header_dict={'value':[],'coordinates':[],'bottom_match':[],'index':[],'side_match':[],'word_idxs':[],'column_range':[]}
    for i in range(len(key_dict_for_table)):
        if i in aligned_keys:
            table_header_dict['value'].append(key_dict_for_table['value'][i])
            table_header_dict['coordinates'].append(key_dict_for_table['coordinates'][i])
            table_header_dict['bottom_match'].append(key_dict_for_table['bottom_match'][i])
            table_header_dict['index'].append(key_dict_for_table['index'][i])
            table_header_dict['side_match'].append(key_dict_for_table['side_match'][i])
            table_header_dict['word_idxs'].append(key_dict_for_table['word_idxs'][i])
            table_header_dict['column_range'].append([key_dict_for_table['coordinates'][i][0],key_dict_for_table['coordinates'][i][2]])
    return table_header_dict
'''
End
'''
   

#table_KV_dict = table_extraction(word_dict,table_header_dict,image_path,table_range)


