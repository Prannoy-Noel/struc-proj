# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 12:42:25 2019

@author: DarshilKapadia
"""

from xml2json_datacap import convert
from doc_classifier import document_classifier
from get_boxes import extract_boxes
from detect_lines import detect_lines
from get_word_info import get_word_info
from find_keys import find_keys
from get_key_info import get_key_info
from get_value import get_val
from draw_boxes import draw_boxes
from visualization import visualization
from xml2json import convert1
from get_word_blobs import get_word_blobs
from get_confidence import getConfidence
import os
import json
import shutil
import sys
import time


def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])

def Extract_KV(image_path, xml_data_path,Format,folder_path):
#    json_path = folder_path+image_path.split('/')[-1][:-4]+'.json'
    json_path = os.path.join(folder_path,os.path.basename(image_path)[:-4]+'.json')
    print("JSON path", json_path)
    if Format == True:
        convert(xml_data_path,json_path,image_path)    ####new format
    else:
        convert1(xml_data_path,json_path,image_path)     ####old format
    word_dict,all_detected_coordinates = get_word_info(json_path)
    box_coords = extract_boxes(image_path, all_detected_coordinates)
    lines = detect_lines(box_coords,word_dict,image_path)
#    print("lines",lines)
    identified_keys_list1 = find_keys(word_dict)
    identified_keys_list=[]
    for item in identified_keys_list1:
        if item[-1][0] == 'Credit_Note':
            pass
        else:
            identified_keys_list.append(item)
#    print(identified_keys_list1,identified_keys_list)
    word_blob_list = get_word_blobs(word_dict,image_path,lines)
    key_dict, word_dict, box_dict, paragraph_dict, disabled_words_idxs = get_key_info(identified_keys_list, word_dict, image_path, box_coords)
#    draw_boxes(image_path,folder_path,key_dict,word_dict,box_dict,paragraph_dict,disabled_words_idxs)
#    return key_dict, word_dict, box_dict, paragraph_dict, disabled_words_idxs,[],[]
    key_val,table_key_val_page,table_KV_dict_coords_page = get_val(key_dict,word_dict,box_dict,disabled_words_idxs,paragraph_dict,image_path,word_blob_list)
    visualization(key_dict,key_val,image_path,folder_path,box_dict,word_dict)



    return key_dict, word_dict, box_dict, paragraph_dict, disabled_words_idxs,key_val,table_key_val_page,table_KV_dict_coords_page
def main_call(source,folder_path,Format,doc_ID):
    files = os.listdir(source)
    print("File1:",files)
#    xml_data_path =[]
#    image_path=[]
    key_val_doc = []
#    confidence_doc = []
    table_key_val_doc = []
    table_key_val_coords_doc = []
    
    for file in files:
        if file.endswith('.xml'):
            print(file)
            xml_data_path = source + file
            print(xml_data_path)
            image_path = xml_data_path.replace('c.xml','.tif')
            image_path = image_path.replace('_layout.xml','.tif')
            txt_path = image_path.replace('.xml','.txt')
            type_key = document_classifier(txt_path)
#            type_key = ''
            print("|||||||||||||||||||||||",image_path)
            key_dict, word_dict, box_dict, paragraph_dict, disabled_words_idxs,key_val,table_key_val_page,table_KV_dict_coords_page=Extract_KV(image_path,xml_data_path,Format,folder_path)
            key_val_conf, table_key_val_page , doc_conf = getConfidence(key_val,table_KV_dict_coords_page, image_path)
            
#            confidence_doc.extend(confidence)
            key_val_doc.extend(key_val_conf)
            table_key_val_doc.extend(table_key_val_page)
#            table_key_val_coords_doc.extend(table_KV_dict_coords_page)
#        else:
#            print(file)
#            continue
    return key_dict, word_dict, box_dict, paragraph_dict, disabled_words_idxs,key_val_doc,table_key_val_doc,table_key_val_coords_doc,doc_conf,type_key

if __name__ == '__main__':


    #input
#    doc_ID = sys.argv[1]
#    zip_str = sys.argv[2]

    #server changes
#    source = r'/test/MedicalTextExtractionApp/MedicalTextOutput/' + doc_ID + '/'
#    destination = r'/test/EngineOutput/Invoice/' + doc_ID + '/'
    # print(os.getcwd())

    doc_ID = '30108083'
    #local changes
    source = r'source/' + doc_ID + '/'
    destination = r'destination/' + doc_ID + '/'


    #common code
    ##zip
    zipbool = False
#    if zip_str == 'yes':
#        zipbool = True
    start_time = time.time()
    while time.time() - start_time < 10*60:
        if os.path.isdir(source):
            print("Datacap output folder found")
            #checking if files are created
            s_time = time.time()
            while time.time() - s_time < 6 :
                if os.path.exists(source + doc_ID + ".txt"):
                    print("Datacap files found")
                    time.sleep(2)
                    break
                else:
                    print("Datacap files not created yet")
                    time.sleep(2)
            if os.path.isdir(destination):
                shutil.rmtree(destination)
            shutil.copytree(source,destination)
            break
        print("Datacap still processing")
        time.sleep(6)

    key_dict, word_dict, box_dict, paragraph_dict, disabled_words_idxs,key_val,table_key_val_doc,table_key_val_coords_doc,confidence,type_key = main_call(source,destination,zipbool,doc_ID)
    result = []
    result_with_table = []
    
#    confidence_doc = [i for i in confidence if i]
#    doc_confidence = statistics.median(confidence_doc)
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
    line_level_detected = [y for x in result_with_table[1:] for y in x.keys() if y!='confidence_score' and y!='document_confidence_score']
    for xx in line_level_keys:
        if xx not in line_level_detected:
            result_with_table.append({xx:[],'confidence_score':[]})

    f= open(destination+doc_ID+'.json', 'w')
    f.write(json.dumps(result_with_table))
    f.close()
#    image_path = r'C:/Users/VinitaKumari/Desktop/Ricoh_Digitization-master/inputfiles/1_000001.tif'
#    xml_data_path = r'C:/Users/VinitaKumari/Desktop/Ricoh_Digitization-master/inputfiles/1_000001c.xml'
#    key_dict, word_dict, box_dict, paragraph_dict, disabled_words_idxs,key_val=Extract_KV(image_path,xml_data_path)
