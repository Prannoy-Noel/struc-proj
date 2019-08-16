# uncompyle6 version 3.3.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.15 |Anaconda, Inc.| (default, Feb 21 2019, 11:55:13) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: C:\Users\DarshilKapadia\Desktop\RICOH\Ricoh_Digitization\codes\find_keys.py
# Compiled at: 2019-07-01 14:41:41
# Size of source mod 2**32: 8108 bytes
"""
Created on Fri Feb  9 17:08:07 2018

@author: Darshil
"""
from .key_match_score import key_match_score
from .tax_key_regex import tax_key_regex
import copy, itertools, pandas as pd


# function for identifying the index of extra invoice date keys
def invoicedate_remove_more_occurance(inv_dt, synonyms_list):
    invoice_main = ['invoice', 'date', 'order', 'reference', 'document', 'billing']
    date_list = list()

    for i in synonyms_list:
        if i[0] == 'date':
            date_list = i

    for im in invoice_main:
        for sl in synonyms_list:
            if im == sl[0]:
                if im != 'date':
                    for s in sl:
                        for dt in date_list:
                            complete_key = s + ' ' + dt
                            if complete_key in inv_dt[0]:
                                return inv_dt[0].index(complete_key)
                elif im == 'date':
                    for s in sl:
                        if s in inv_dt[0]:
                            return inv_dt[0].index(s)
    return -1

def find_keys(word_dict):
    identified_keys_list = []
    for idx in range(len(word_dict['coordinates'])):
        matched_text_idx = []
        detected_matched_text_idx = []
        matchedKey = ''
        text = ''
        text += (word_dict['value'][idx] + ' ')
        matchedtext, key_status = key_match_score(text.strip(), matchedKey.strip())
        while True:
            if key_status == 'not_detected':
                if len(detected_matched_text_idx) == 0:
                    break
                else:
                    identified_keys_list.append(detected_matched_text_idx)
                    break
            elif key_status == 'completed':
                matchedKey = (matchedtext + ' ')
                matched_text_idx.append(idx)
                if len(matchedKey.strip().split()) == 1:
                    matched_text_idx = [idx, [matchedKey.strip(), idx]]

                else:
                    matched_text_idx.pop()
                    matched_text_idx.append([matchedKey.strip(), idx])
                identified_keys_list.append(matched_text_idx)
                break
            else:
                matchedKey = (matchedtext + ' ')
                matched_text_idx.append(idx)
                if key_status == 'detected':
                    matched_text_idx_detected = copy.deepcopy(matched_text_idx)
                    if len(matchedKey.strip().split()) == 1:
                        matched_text_idx_detected = [idx, [matchedKey.strip(), idx]]
                    else:
                        matched_text_idx_detected.pop()
                        matched_text_idx_detected.append([matchedKey.strip(), idx])
                    detected_matched_text_idx = matched_text_idx_detected
                try:
                    if abs(word_dict['coordinates'][idx][2] - word_dict['coordinates'][word_dict['side_match'][idx]['right'][0]][0]) < 50:
                        side_idx = word_dict['side_match'][idx]['right'][0]
                        side_text = text + (word_dict['value'][side_idx] + ' ')
                        sideMatchedtext, sideKey_status = key_match_score(side_text.strip(), matchedKey.strip())
                        if sideKey_status == 'not_detected':
                            side_status = False
                        else:
                            side_status = True
                    else:
                        side_status = False
                except IndexError:
                    side_status = False

                bottom_idx = idx = word_dict['bottom_match'][idx]
                if bottom_idx is None:
                    bottom_status = False
                else:
                    bottom_text = text + (word_dict['value'][bottom_idx] + ' ')
                    bottomMatchedtext, bottomKey_status = key_match_score(bottom_text.strip(), matchedKey.strip())
                    if bottomKey_status == 'not_detected':
                        bottom_status = False
                    else:
                        bottom_status = True
                if (side_status is False) and (bottom_status is False):

                    if len(detected_matched_text_idx) == 0:
                        break
                    else:
                        identified_keys_list.append(detected_matched_text_idx)
                        break
                elif (bottom_status is True) and (side_status is False):

                    idx = bottom_idx
                    text = bottom_text
                    matchedtext = bottomMatchedtext
                    key_status = bottomKey_status
                else:
                    idx = side_idx
                    text = side_text
                    matchedtext = sideMatchedtext
                    key_status = sideKey_status

    '''
    Remove the keys which is subset of another key
    '''
#    print("===",identified_keys_list)
    new_key_list = []
    for i in range(0, len(identified_keys_list)):
        subsetFlag = False
        i_list = identified_keys_list[i][:-1]
        i_list.append(identified_keys_list[i][-1][1])
        for j in range(0, len(identified_keys_list)):
            if i is j:
                continue
            j_list = identified_keys_list[j][:-1]
            j_list.append(identified_keys_list[j][-1][1])
            if all(x in j_list for x in i_list):
                subsetFlag = True
                break

        if subsetFlag is False:
            new_key_list.append(identified_keys_list[i])
    '''
    End
    '''

    original_identified_keys = []
    for i in range(0, len(identified_keys_list)):
        original_identified_keys.append(identified_keys_list[i][-1][0])

    '''
    Key Mapping
    '''
    df = pd.read_csv('./../config/keys.csv')
    mapping = {}
    for i in range(df.shape[0]):
        mapping[df['Keys'][i]] = [x.lower() for x in list(df['Mapping'][i].split(','))]

    synonyms_list_path = './../config/synonyms.txt'
    f = open(synonyms_list_path, 'r')
    synonyms_list = f.readlines()
    synonyms_list = [s.strip().split(',') for s in synonyms_list]
    synonyms_list = [[s.strip().lower() for s in synonym] for synonym in synonyms_list]
    f.close()
    for Key in mapping.keys():
        value_list = mapping[Key]
        value_list_expanded = []
        for i in range(len(value_list)):
            value = value_list[i]
            value_words_list = value.split()
            value_word_expanded_list = []
            for v in value_words_list:
                value_word_expanded_list += [s for s in synonyms_list if v in s]

            value_expanded = list(itertools.product(*value_word_expanded_list))
            value_expanded = [' '.join(x) for x in value_expanded]
            value_list_expanded += value_expanded

        mapping[Key] = value_list_expanded

    new_key_list_ = []
    inv_dt = [[], []]
    for cnt, k in enumerate(new_key_list):
        for m in mapping.keys():
            if k[-1][0] in mapping[m]:
                if m.lower() == 'Invoice_Date'.lower():
                    inv_dt[0].append(k[-1][0])
                    inv_dt[1].append(len(new_key_list_))
                    # print('#' * 10, k[-1][0], ' -'*5,len(new_key_list_))
                k[-1][0] = m
                new_key_list_.append(k)
                break

    '''
    End
    '''

    '''
    Handle Tax/GST/VAT regex
    '''
    for k_idx,key in enumerate(new_key_list_):
        if key[-1][0] in ['Invoice_Tax_Amount','Line_Tax_Amount']:
            detected_idx = key[-1][1]
#            print(detected_idx)

            toCombine_idxs = []
            cnt = 0
            text = ''
            curr_idx = copy.deepcopy(detected_idx)
            while True:
                try:
                    curr_idx = word_dict['side_match'][curr_idx]['right'][0]
                except IndexError:
                    break
                if cnt==3:
                    break

                toCombine_idxs.append(curr_idx)
                text += word_dict['value'][curr_idx]
                match = tax_key_regex(text)
                if match is None:
                    cnt += 1
                else:
                    print("Tax regex found. Updating Key!",text)
                    print('old key',key)
                    if key[0] == key[-1][1]:
                        if len(toCombine_idxs)==1:
                            last_ele = [key[-1][0],toCombine_idxs[0]]
                            new_key = key[:-1]+ [last_ele]
                        else:
                            last_ele = [key[-1][0],toCombine_idxs[-1]]
                            new_key = key[:-1]+toCombine_idxs[:-1]
                            new_key.append(last_ele)
                    else:
                        if len(toCombine_idxs)==1:
                            last_ele = [key[-1][0],toCombine_idxs[0]]
                            new_key = key[:-1]+ [key[-1][1]]
                            new_key.append(last_ele)
                        else:
                            last_ele = [key[-1][0],toCombine_idxs[-1]]
                            new_key = key[:-1]+ [key[-1][1]]
                            new_key += toCombine_idxs[:-1]
                            new_key.append(last_ele)
                    print('new key',new_key)
                    new_key_list_[k_idx] = new_key
                    break

    '''
    End
    '''

    org_invoice_date_key_index = invoicedate_remove_more_occurance(inv_dt, synonyms_list)
    # print(new_key_list_)
    if org_invoice_date_key_index != -1:
        new_inv_dt = []
        for i, indval in enumerate(inv_dt[1]):
            if i != org_invoice_date_key_index:
                new_inv_dt.append(indval)

        new_inv_dt.sort(reverse=True)
        for new_index in new_inv_dt:
            new_key_list_.pop(new_index)
    # print('*'*20)
    # print(new_key_list_)
    # print(word_dict)
    # print(mapping)
    # print('*'*20)
    return new_key_list_
# okay decompiling find_keys.cpython-36.pyc
