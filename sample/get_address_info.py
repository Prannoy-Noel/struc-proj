# uncompyle6 version 3.3.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.15 |Anaconda, Inc.| (default, Feb 21 2019, 11:55:13) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: C:\Users\DarshilKapadia\Desktop\RICOH\Ricoh_Digitization\codes\get_address_info.py
# Compiled at: 2019-07-02 18:12:12
# Size of source mod 2**32: 7120 bytes
"""
Created on Wed June 26 12:11:45 2019

@author: Prannoy Noel Jada
"""
import pandas as pd
#from get_boxes import isXinY

def isXinY(x, y):
    if x[0] > y[0] - 10 and x[1] > y[1] - 10 and x[2] < y[2] + 10 and x[3] < y[3] + 10:
        
        return True
    else:
        return False

def get_address_info(words):
    paragraphs_dict = get_paragraph_info(words)
    addresses_dict = paragraphs_dict
    for i in range(len(addresses_dict['text'])):
        print('\n')
        print(addresses_dict['coordinates'][i])
        print(addresses_dict['text'][i])
        print(addresses_dict['indices'][i])

    return addresses_dict


def get_paragraph_info(words, disabled_words_idxs,keys):
    paragraph_dict = {'coordinates':[],  'text':[],  'indices':[],'keys':[]}
    no_of_words = len(words['bottom_match'])
    words['assigned'] = [False] * no_of_words
    df = pd.DataFrame({'value':words['value'],  'side_match':words['side_match'],  'coordinates':words['coordinates'],  'bottom_match':words['bottom_match'],  'y_coordinate':words['bottom_match']})
    for i in range(len(df)):
        df.loc[i, 'y_coordinate'] = df.loc[i, 'coordinates'][1]

    df = df.sort_values(by=['y_coordinate'])
    df.reset_index(inplace=True)
    for i in range(len(df)):
        index = df.loc[i, 'index']
        if words['assigned'][index] == True:
            continue
        character_length = (words['coordinates'][index][2] - words['coordinates'][index][0]) / len(words['value'][index])
        right_threshold = 2 * character_length
        if words['bottom_match'][index] is None:
            continue
        bottom_word_index = words['bottom_match'][index]
        if abs(words['coordinates'][bottom_word_index][0] - words['coordinates'][index][0]) > 0.2 * character_length or abs(words['coordinates'][index][3] - words['coordinates'][bottom_word_index][1]) > 2 * character_length:
            
            continue
        
        start_index = index
        highest_x2 = words['coordinates'][start_index][2]
        highest_y2 = words['coordinates'][start_index][3]
        word_indices_list_in_paragraph = []
        paragraph_text = ''
        while 1:
            words['assigned'][start_index] = True
            word_indices_list_in_paragraph.append(start_index)
            paragraph_text = paragraph_text + ' ' + words['value'][start_index]
            highest_y2 = words['coordinates'][start_index][3]
            if words['coordinates'][start_index][2] > highest_x2:
                highest_x2 = words['coordinates'][start_index][2]
            temp = start_index
            for k in words['side_match'][start_index]['right']:
                if words['assigned'][k] == True:
                    continue
                if words['coordinates'][k][0] - words['coordinates'][temp][2] < right_threshold:
                    words['assigned'][k] = True
                    if words['coordinates'][k][2] > highest_x2:
                        highest_x2 = words['coordinates'][k][2]
                    highest_y2 = words['coordinates'][k][3]
                    word_indices_list_in_paragraph.append(k)
                    paragraph_text = paragraph_text + ' ' + words['value'][k]
                    temp = k
                else:
                    break

            if words['bottom_match'][start_index] is not None:
                temp_bottom_word = words['bottom_match'][start_index]
                if abs(words['coordinates'][temp_bottom_word][0] - words['coordinates'][start_index][0]) < character_length and abs(words['coordinates'][start_index][3] - words['coordinates'][temp_bottom_word][1]) < right_threshold:
                    
                    start_index = temp_bottom_word
                else:
                    break
            else:
                break

        paragraph_dict['coordinates'].append([words['coordinates'][index][0], words['coordinates'][index][1], highest_x2, highest_y2])
        paragraph_dict['text'].append(paragraph_text.strip())
        paragraph_dict['indices'].append(word_indices_list_in_paragraph)
#        for x in word_indices_list_in_paragraph:
#            disabled_words_idxs.append(int(x))
#    print("key len is ",len(keys['value']))
    for m in range(len(paragraph_dict['indices'])):
        [x1,y1,x2,y2] = paragraph_dict['coordinates'][m]
        keys_in_para =[]
        for j in range(len(keys['value'])):
            [x_1,y_1,x_2,y_2] = keys['coordinates'][j]
            if isXinY([x_1,y_1,x_2,y_2],[x1,y1,x2,y2]):
#                print('yes')
                keys_in_para.append(j)
            
        paragraph_dict['keys'].append(keys_in_para)  
                  
    return (paragraph_dict, disabled_words_idxs)
# okay decompiling get_address_info.cpython-36.pyc
