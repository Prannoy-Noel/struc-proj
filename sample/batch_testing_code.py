# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 12:18:50 2019

@author: DarshilKapadia
"""

import os
import json
from os.path import join
from KV_Extraction_folder_api import Extract_KV
from get_confidence import getConfidence
from doc_classifier import document_classifier

source_direct = r'C:\Users\DarshilKapadia\Desktop\RICOH\R&D\debugging_post_demo\Data\telstra'

dest_direct = r'C:\Users\DarshilKapadia\Desktop\RICOH\R&D\debugging_post_demo\Outputs\telstra'

page_error_counter=0
for doc_ID in os.listdir(source_direct):
    if doc_ID == 'telstra':
        continue
    key_val_doc = []
    table_key_val_doc = []
    table_key_val_coords_doc = []
    for f in os.listdir(join(source_direct,doc_ID)):    
        if f.endswith('.xml'):
            xml_data_path = join(source_direct,doc_ID,f)
            if 'c.xml' in xml_data_path:
                Format = True
            elif '_layout.xml' in xml_data_path:
                Format = False
            else:
                print('OCR output NOT FOUND')
                continue
            
            folder_path = os.path.join(dest_direct,doc_ID)
            try:
                os.makedirs(folder_path)
            except FileExistsError:
                pass
            image_path = xml_data_path.replace('c.xml','.tif').replace('_layout.xml','.tif')
            txt_path = image_path.replace('.tif','.txt')
            type_key = document_classifier(txt_path)
#            try:
            key_dict, word_dict, box_dict, paragraph_dict, disabled_words_idxs,key_val,table_key_val_page,table_KV_dict_coords_page = Extract_KV(image_path, xml_data_path,Format,folder_path)
            key_val_conf, table_key_val_page , confidence = getConfidence(key_val,table_KV_dict_coords_page, image_path)
            key_val_doc.extend(key_val_conf)
            table_key_val_doc.extend(table_key_val_page)
#            except:
#                page_error_counter+=1
                
    result = []
    result_with_table = []
    
    for item in key_val_doc:
    
        all_keys_added = [list(i.keys())[0] for i in result]
        if item['key'] in all_keys_added:
            index = all_keys_added.index(item['key'])
            if item['value'] not in result[index][item['key']]:
                result[index][item['key']].append(item['value'])
                result[index]['confidence_score'].append(item['confidence'])
        else:
            obj = {}
            obj[item['key']] = [item['value']]
            obj['confidence_score']=[item['confidence']]
            if obj not in result:
    
                result.append(obj)
    result.append(type_key)
    
    result_with_table.append(result)
    result_with_table.append({'document_confidence_score':[confidence]})
        
    for table in table_key_val_doc:
        if len(table)<=1:
            pass
        else:
            result_with_table.extend(table)
    
    
    single_word_value_keys = ["Invoice_Date","Invoice_Number","Invoice_Net","Invoice_Tax_Amount","Invoice_Total","Currency","PO_Number","Supplier_Tax_Number","Supplier_Bank_Account_Number","Supplier_IBAN","Credit_Note","Supplier_Swift_Code","Delivery_Note_Number"]
    multi_word_value_keys = ["Supplier_Name_and_Address","Bill_to_Name_and_Address","Ship_to"]
    table_single_word_value_keys = ["Unit_Price","Line_Net_Amount","Line_Tax_Amount","Line_Quantity","Line_Gross_Amount","Shipping/Freight_Amount","UoM"]
    table_multi_word_value_keys = ["Line_Item","Material_Number","Line_Description"]
    line_level_keys = table_single_word_value_keys+table_multi_word_value_keys
    header_level_keys = single_word_value_keys + multi_word_value_keys
    
    header_level_detected = [y for x in result_with_table[0] for y in x.keys() if y!='confidence_score']
    for xx in header_level_keys:
        if xx not in header_level_detected:
            result_with_table[0].append({xx:[],'confidence_score':[]})
    line_level_detected = [y for x in result_with_table[1:] for y in x.keys() if y!='confidence' and y!='document_confidence_score']
    for xx in line_level_keys:
        if xx not in line_level_detected:
            result_with_table.append({xx:[],'confidence_score':[]})
    
    f= open(join(folder_path,'result.json'), 'w')
    f.write(json.dumps(result_with_table))
    f.close()
                    
            
    
