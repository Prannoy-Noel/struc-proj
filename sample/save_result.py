# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 15:42:51 2019

@author: DarshilKapadia
"""

from os.path import join
import json


result = []
result_with_table = []


def save_result(key_val,type_key,table_key_val_doc,doc_ID,destination,confidence):

    for item in key_val:
    
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
    #    with open(destination+doc_ID+'_with_coords.json', 'w') as outfile:
    #        json.dumps(key_val, outfile,indent = 2)
    #
    ### add table code here
    
    #    with open(destination+doc_ID+'.json', 'w') as outfile:
    #        json.dumps(result_with_table,indent = 2)
    
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
    
    f= open(join(destination,'result.json'), 'w')
    f.write(json.dumps(result_with_table))
    f.close()