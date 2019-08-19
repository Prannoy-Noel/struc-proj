# uncompyle6 version 3.3.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.15 |Anaconda, Inc.| (default, Feb 21 2019, 11:55:13) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: C:\Users\DarshilKapadia\Desktop\RICOH\Ricoh_Digitization\codes\get_word_info.py
# Compiled at: 2019-07-02 12:58:52
# Size of source mod 2**32: 6942 bytes
"""
Created on Fri Feb  9 16:59:08 2018

@author: Darshil
"""
import json
from .date_match_regex import date_match_regex


def is_bottom_match(rect1, rect2):
    w_25 = int((rect1[2] - rect1[0]) / 2)
    h_flag = rect1[3] < rect2[1] and abs(rect2[1] - rect1[3]) < 100
    return h_flag and rect1[0] - w_25 < rect2[0] < rect1[0] + w_25


def is_side_match(rect1, rect2):
    height_min = min(rect1[3]-rect1[1],rect2[3]-rect2[1])
    overlap = min(rect1[3],rect2[3])-max(rect1[1],rect2[1])
    if overlap<0 :
        return False
    elif overlap/height_min>0.7:
        return True
    else:
        return False


def get_word_matches(dict_new, disabled_word_idxs=[]):
    dict_new['bottom_match'] = []
    dict_new['side_match'] = []
    for i in range(0, len(dict_new['coordinates'])):
#        if i in disabled_word_idxs:
#            dict_new['bottom_match'].append(None)
#            continue
        bottom_match_flag = False
        for j in range(0, len(dict_new['coordinates'])):
            if not j in disabled_word_idxs:
                if i == j:
                    pass
                else:
                    if dict_new['coordinates'][j][1] > dict_new['coordinates'][i][3]:
                        if is_bottom_match(dict_new['coordinates'][i], dict_new['coordinates'][j]):
                            bottom_match_flag = True
                            dict_new['bottom_match'].append(j)
                            break

        if not bottom_match_flag:
            dict_new['bottom_match'].append(None)

    for i in range(0, len(dict_new['coordinates'])):
        side_match_list = []
        right_list = []
        left_list = []
        if i in disabled_word_idxs:
            dict_new['side_match'].append({'right':[],  'left':[]})
            continue
        for j in range(0, len(dict_new['coordinates'])):
            if j in disabled_word_idxs:
                continue
            if is_side_match(dict_new['coordinates'][i], dict_new['coordinates'][j]):
                if i != j:
                    if dict_new['coordinates'][j][0] > dict_new['coordinates'][i][0]:
                        right_list.append(j)
                    else:
                        left_list.append(j)

        side_match_list = {'left':left_list,
         'right':right_list}
        side_match_list['left'] = sorted((side_match_list['left']), key=(lambda x: dict_new['coordinates'][x][0]))
        side_match_list['right'] = sorted((side_match_list['right']), key=(lambda x: dict_new['coordinates'][x][0]))
        dict_new['side_match'].append(side_match_list)




def get_word_info(json_out_file):
    all_words = []
    with open(json_out_file) as (data_file):
        data = json.load(data_file)
    wordList = []
    page_list = data['page']
    for page in page_list:
        line_list = page['LineList']
        for line in line_list:
            word_list = line['WordList']
            wordList += word_list

    wordList = [x for x in wordList if 'WordValue' in x.keys()]
    dict_new = {'coordinates':[],  'index':[],  'value':[],  'bottom_match':[],  'side_match':[]}
    if len(wordList) == 0:
        return dict_new,all_words
    else:
        cnt_idx = 0
        for idx, word in enumerate(wordList):
            if word['WordStartX'] == 0:
                if word['WordStartY'] == 0:
                    continue
            all_words.append([word['WordStartX'], word['WordStartY'],
             word['WordStartX'] + word['WordWidth'], word['WordStartY'] + word['WordHeight']])
            if type(word['WordValue']) is dict:
                wordValue = word['WordValue']['em']
            else:
                wordValue = word['WordValue']
            if wordValue is None:
                pass
            else:
                if len(wordValue.strip()) < 3:
                    if wordValue.strip().replace(':', '').replace(',', '').replace(';', '').replace('/', '') == '':
                        continue
                if len(wordValue) < 2:
                    if wordValue != '@':
                        if wordValue != '#':
                            if wordValue != '-':
                                if not (len(wordValue) == 1 and 47 < ord(wordValue) < 58):
                                    if wordValue != 'P':
                                        if wordValue != 'O':
                                            if wordValue != '%':
                                                continue
                dict_new['value'].append(wordValue)
                dict_new['index'].append(cnt_idx)
                cnt_idx += 1
                dict_new['coordinates'].append([word['WordStartX'], word['WordStartY'],
                 word['WordStartX'] + word['WordWidth'], word['WordStartY'] + word['WordHeight']])
#        print(len(dict_new['value']))
        toCombine_idxs_list = []
        toCombine_idxs = []
        i = 0
        cnt = 0
        text = ''
        while 1:
            if i == len(dict_new['coordinates']):
                break
#            print(i)
            if cnt == 3:
                cnt = 0
                toCombine_idxs = []
                text = ''
                i -= 2
            toCombine_idxs.append(i)
            text += dict_new['value'][i]
            match = date_match_regex(text)
            if len(match) == 0:
                cnt += 1
                i += 1
            else:
                print("date",text)
                toCombine_idxs_list.append(toCombine_idxs)
                toCombine_idxs = []
                cnt = 0
                i += 1
                text = ''


        toDeleteList = []
        for sub in toCombine_idxs_list:
            if len(sub) > 1:
                fID = sub[0]
                text = dict_new['value'][fID]
                x0, y0, x1, y1 = dict_new['coordinates'][fID]
                for s in range(1, len(sub)):
                    s = sub[s]
                    text += '' + dict_new['value'][s]
                    if dict_new['coordinates'][s][0] < x0:
                        x0 = dict_new['coordinates'][s][0]
                    if dict_new['coordinates'][s][1] < y0:
                        y0 = dict_new['coordinates'][s][1]
                    if dict_new['coordinates'][s][2] > x1:
                        x1 = dict_new['coordinates'][s][2]
                    if dict_new['coordinates'][s][3] > y1:
                        y1 = dict_new['coordinates'][s][3]
                    toDeleteList.append(s)

                dict_new['coordinates'][fID] = [
                 x0, y0, x1, y1]
                dict_new['value'][fID] = text

        toDeleteList = sorted(toDeleteList, reverse=True)
        for i in toDeleteList:
            del dict_new['value'][i]
            del dict_new['coordinates'][i]
            del dict_new['index'][i]
#        i=0
#        while 1:
#            if i == len(dict_new['coordinates'])-1:
#                break
#            if is_amount(dict_new['value'][i].strip()+' '+dict_new['value'][i+1].strip()):
#                dict_new['value'][i] = dict_new['value'][i].strip()+' '+dict_new['value'][i+1].strip()
#                x1 = min(dict_new['coordinates'][i][0],dict_new['coordinates'][i+1][0])
#                y1 = min(dict_new['coordinates'][i][1],dict_new['coordinates'][i+1][1])
#                x2 = max(dict_new['coordinates'][i][2],dict_new['coordinates'][i+1][2])
#                y2 = max(dict_new['coordinates'][i][3],dict_new['coordinates'][i+1][3])
#                dict_new['coordinates'][i] = [x1,y1,x2,y2]
#                del dict_new['value'][i+1]
#                del dict_new['coordinates'][i+1]
#                del dict_new['index'][i+1]

        get_word_matches(dict_new)
#        print("called get word matches")
    return dict_new, all_words

# okay decompiling get_word_info.cpython-36.pyc
