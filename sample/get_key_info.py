# uncompyle6 version 3.3.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.15 |Anaconda, Inc.| (default, Feb 21 2019, 11:55:13) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: C:\Users\DarshilKapadia\Desktop\RICOH\Ricoh_Digitization\codes\get_key_info.py
# Compiled at: 2019-07-02 18:12:43
# Size of source mod 2**32: 7597 bytes
"""
Created on Wed Feb 21 16:11:45 2018

@author: Darshil
"""
import cv2
import numpy as np
from .get_word_info import get_word_matches
from .get_address_info import get_paragraph_info
single_word_value_keys = ["Invoice_Date","Invoice_Number","Invoice_Net","Invoice_Tax_Amount","Invoice_Total","Currency","PO_Number","Supplier_Tax_Number","Supplier_Bank_Account_Number","Supplier_IBAN","Credit_Note","Supplier_Swift_Code","Delivery_Note_Number"]
multi_word_value_keys = ["Supplier_Name_and_Address","Bill_to_Name_and_Address","Ship_to"]
header_keys = single_word_value_keys+multi_word_value_keys
def get_TEXTinBOX(box_coord, dict_new, word_dict):
    all_keys_words_INBOX = []
    key_idxs_INBOX = []
    word_idxs_INBOX = []
    x1b, y1b, x2b, y2b = box_coord
    for i in range(len(dict_new['coordinates'])):
        x1k, y1k, x2k, y2k = dict_new['coordinates'][i]
        if x1b < x1k:
            if y1b < y1k:
                if x2b > x2k:
                    if y2b > y2k:
                        key_idxs_INBOX.append(i)
                        for y in dict_new['word_idxs'][i]:
                            all_keys_words_INBOX.append(y)

    for j in range(len(word_dict['coordinates'])):
        x1w, y1w, x2w, y2w = word_dict['coordinates'][j]
        if x1b < x1w:
            if y1b < y1w:
                if x2b > x2w:
                    if y2b > y2w:
                        if j not in all_keys_words_INBOX:
                            word_idxs_INBOX.append(j)

    return (key_idxs_INBOX, word_idxs_INBOX)


def get_key_info(identified_keys_list, word_dict, image_path, box_coords):
    identified_key_idx = []
    img = cv2.imread(image_path)
    w=img.shape[1]
    for x in identified_keys_list:
        y = x[:-1] + [x[-1][-1]]
        y = list(set(y))
        identified_key_idx.append(y)

    dict_new = {'coordinates':[],  'index':[],  'word_idxs':[],  'bottom_match':[],  'side_match':[],  'value':[]}
    for cnt, i in enumerate(identified_keys_list):
        dict_new['index'].append(cnt)
        y = i[:-1] + [i[-1][-1]]
        dict_new['word_idxs'].append(list(set(y)))
        dict_new['value'].append(i[-1][0])
        coordinates_list = [word_dict['coordinates'][w] for w in dict_new['word_idxs'][cnt]]
        keyL = min([c[0] for c in coordinates_list])
        keyT = min([c[1] for c in coordinates_list])
        keyR = max([c[2] for c in coordinates_list])
        keyB = max([c[3] for c in coordinates_list])
        dict_new['coordinates'].append([keyL, keyT, keyR, keyB])

#    box_coords = extract_boxes(image_path, all_detected_coordinates)





#    print(box_coords)
    box_dict = {'coordinates':[],  'key_idxs':[],  'word_idxs':[]}
    disabled_words_idxs = []
    for i in range(len(dict_new['coordinates'])):
        disabled_words_idxs += dict_new['word_idxs'][i]
#    print("before calling paragraphs len of keys")
    paragraph_dict, disabled_words_idxs = get_paragraph_info(word_dict, disabled_words_idxs,dict_new)
#    print(paragraph_dict)
    for i in range(len(box_coords)):
        key_idxs_INBOX, word_idxs_INBOX = get_TEXTinBOX(box_coords[i], dict_new, word_dict)
        if len(word_idxs_INBOX) == 0 and len(key_idxs_INBOX) == 1 and dict_new['value'][key_idxs_INBOX[0]] in header_keys:
            dict_new['coordinates'][key_idxs_INBOX[0]] = box_coords[i]
        elif len(word_idxs_INBOX) == 0 and len(key_idxs_INBOX) == 1 and dict_new['value'][key_idxs_INBOX[0]] not in header_keys:
            box_dict['coordinates'].append(box_coords[i])
            box_dict['key_idxs'].append(key_idxs_INBOX)
            box_dict['word_idxs'].append(word_idxs_INBOX)
        elif len(word_idxs_INBOX) < len(key_idxs_INBOX) and len(key_idxs_INBOX) > 1:
            if box_coords[i][2]-box_coords[i][0]>0.6*w:
                for j in range(len(box_coords)):
                    box = box_coords[i]
                    box_ = box_coords[j]
                    if abs(box_[0]-box[0])<10 and abs(box_[2]-box[2])<10 and abs(box_[1]-box[3])<10:
                        box_dict['coordinates'].append([min(box_[0],box[0]),min(box_[1],box[1]),max(box_[2],box[2]),max(box_[3],box[3])])
                        key_idxs_INBOX_j, word_idxs_INBOX_j = get_TEXTinBOX(box_coords[j], dict_new, word_dict)
                        box_dict['key_idxs'].append(key_idxs_INBOX+key_idxs_INBOX_j)
                        box_dict['word_idxs'].append(word_idxs_INBOX+word_idxs_INBOX_j)
            else:
                box_dict['coordinates'].append(box_coords[i])
                box_dict['key_idxs'].append(key_idxs_INBOX)
                box_dict['word_idxs'].append(word_idxs_INBOX)
#                print('--------------------')
#                print('case 2')
#                print(box_coords[i])
#                for i in range(len(key_idxs_INBOX)):
#                    print(dict_new['value'][key_idxs_INBOX[i]])
#                    print(dict_new['coordinates'][key_idxs_INBOX[i]])
#
#                print('--------------------')
        elif len(key_idxs_INBOX) == 0:
            temp_value = ' '.join([x for i, x in enumerate(word_dict['value']) if i in word_idxs_INBOX])
            word_dict['coordinates'].append(box_coords[i])
            word_dict['value'].append(temp_value)
            word_dict['index'].append(len(word_dict['coordinates']) - 1)
            disabled_words_idxs += word_idxs_INBOX
        else:

            if len(key_idxs_INBOX) > 0 and len(word_idxs_INBOX) >= len(key_idxs_INBOX):

                    box_dict['coordinates'].append(box_coords[i])
                    box_dict['key_idxs'].append(key_idxs_INBOX)
                    box_dict['word_idxs'].append(word_idxs_INBOX)

    get_word_matches(word_dict, disabled_words_idxs)
#    print("all boxes traversed")
    def is_side_match(rect1, rect2):
        limit = min(0.4 * (rect1[3] - rect1[1]), 15)
        if abs(rect1[3] - rect2[3]) < limit or abs(rect1[1] - rect2[1]) < limit:
            return True
        else:
            return False

    for i in range(0, len(dict_new['coordinates'])):
        side_match_list = []
        side_match_flag = False
        right_list = []
        left_list = []
        for j in range(0, len(word_dict['coordinates'])):
            if j in dict_new['word_idxs'][i]:# or j in disabled_words_idxs:

                    continue

            if is_side_match(dict_new['coordinates'][i], word_dict['coordinates'][j]):
                side_match_flag = True
                if word_dict['coordinates'][j][0] > dict_new['coordinates'][i][0]:
                    right_list.append(j)
                else:
                    left_list.append(j)

        side_match_list = {'left':left_list,
         'right':right_list}
        side_match_list['left'] = sorted((side_match_list['left']), key=(lambda x: word_dict['coordinates'][x][0]))
        side_match_list['right'] = sorted((side_match_list['right']), key=(lambda x: word_dict['coordinates'][x][0]))
        dict_new['side_match'].append(side_match_list)

    def is_bottom_match(rect1, rect2):
        w_25 = int((rect1[2] - rect1[0]) / 4)
        rect1_mid = int((rect1[0] + rect1[2]) / 2)
        rect2_mid = int((rect2[0] + rect2[2]) / 2)
        h_flag = rect1[3] <= rect2[1] and abs(rect2[1] - rect1[3]) < 100

        if w_25 < 25:
            w_25_flag = 4 * w_25
        else:
            w_25_flag = w_25

        return rect1[0] - w_25_flag < rect2[0] < rect1[0] + 3*w_25 and h_flag

    for i in range(0, len(dict_new['coordinates'])):
        bottom_match_list = []
        for j in range(0, len(word_dict['coordinates'])):
            if j in dict_new['word_idxs'][i] or word_dict['coordinates'][j][1] < dict_new['coordinates'][i][3]:# or j in disabled_words_idxs:

                continue

            if is_bottom_match(dict_new['coordinates'][i], word_dict['coordinates'][j]):
                bottom_match_list.append(j)
#            if (len(dict_new['side_match'][i]['left']) == 0) or (len(dict_new['side_match'][i]['right']) == 0):
#                continue
#            if len(dict_new['side_match'][i]['left']) == 0 and len(dict_new['side_match'][i]['right'])==0:
#                if len(dict_new['side_match'][i]['right']) == 0:
#                        pass
#                continue

        bottom_match_list = sorted(bottom_match_list, key=(lambda x: word_dict['coordinates'][x][1]))
        dict_new['bottom_match'].append(bottom_match_list)

    return (dict_new, word_dict, box_dict, paragraph_dict, disabled_words_idxs)
# okay decompiling get_key_info.cpython-36.pyc
