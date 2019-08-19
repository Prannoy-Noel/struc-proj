# uncompyle6 version 3.3.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.15 |Anaconda, Inc.| (default, Feb 21 2019, 11:55:13) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: C:\Users\DarshilKapadia\Desktop\RICOH\Ricoh_Digitization\codes\key_match_score.py
# Compiled at: 2019-07-01 14:41:09
# Size of source mod 2**32: 9915 bytes
"""
Created on Thu Feb  8 16:46:39 2018

@author: Darshil
"""
import itertools
from .word_match import word_match
import pandas as pd
import os

def read_config():
    file_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(os.path.join(file_path, './../config/keys.csv'))
#    print("read successfully")
    keys_list = list(df['Mapping'])
#    keys_list = [x.strip().lower().split(',') for x in keys_list]
    keys_list = [y.strip().lower() for x in keys_list for y in x.split(',')]

    file_path = os.path.dirname(os.path.realpath(__file__))
    rejectKeys_list_path = os.path.join(file_path, './../config/rejectkeys.txt')

    f = open(rejectKeys_list_path, 'r')
    rejectKeys_list = f.readlines()
    rejectKeys_list = [k.strip().lower() for k in rejectKeys_list]
    f.close()
    keys_list += rejectKeys_list
    f.close()

    file_path = os.path.dirname(os.path.realpath(__file__))
    synonyms_list_path = os.path.join(file_path, './../config/synonyms.txt')
    f = open(synonyms_list_path, 'r')
    synonyms_list = f.readlines()
    synonyms_list = [s.strip().split(',') for s in synonyms_list]
    synonyms_list = [[s.strip().lower() for s in synonym] for synonym in synonyms_list]
    f.close()
    return (keys_list, synonyms_list)


def check_completion(matchedKey, key_list, synonym_list):
    key_len = len(matchedKey.split())
    prob_keys = [k for k in key_list if len(k.split()) >= key_len]
    possible_keys_list = []
    for k in prob_keys:
        completion_for_k = True
        for idx in range(key_len):
            matchedKey_idx = matchedKey.split()[idx]
            key_idx = k.split()[idx]
            try:
                key_idx_synonyms = [s for s in synonym_list if key_idx.lower() in s][0]
            except:
                print("*"*10,' Synonym Not Found ',"*"*10,key_idx)


            if matchedKey_idx not in key_idx_synonyms:
                completion_for_k = False
                break

        if completion_for_k is True:
            possible_keys_list.append(k)

    flag = False
    for k in possible_keys_list:
        if len(k.split()) is len(matchedKey.split()):
            flag = True

    if flag:
        if len(possible_keys_list) == 1:
            key_status = 'completed'

        elif len(possible_keys_list) > 1:
            key_status = 'detected'
    else:
        key_status = 'partially_detected'
    return key_status


def key_match_score(text, matchedKey=''):
    text = text.replace(':', '')
    key_list, synonym_list = read_config()
    key_len = len(matchedKey.split())
    prob_keys = [k for k in key_list if len(k.split()) > key_len]

    if matchedKey == '':
        try:
            candidate_words = [k.split()[0] for k in key_list]
        except IndexError:
            print('index error')
            print()
        candidate_list = []
        for c in candidate_words:
            for s in synonym_list:
                if c in s:
                    candidate_list += s

        candidate_list = list(set(candidate_list))
    else:
        matchedKeyLen = len(matchedKey.split())
        if matchedKeyLen > 1:
            matchedKeyWordSynonyms = []
            for i in range(matchedKeyLen):
                matchedKeyWordSynonyms.append([s for s in synonym_list if matchedKey.split()[i] in s][0])

            matchedKeyWordSynonyms = list((itertools.product)(*matchedKeyWordSynonyms))
            matchedKeySynonyms = [' '.join(x) for x in matchedKeyWordSynonyms]
        else:
            matchedKeySynonyms = [s for s in synonym_list if matchedKey in s][0]
        candidate_keys = [k for k in prob_keys if ' '.join(k.split()[:key_len]) in matchedKeySynonyms]
        candidate_words = [k.split()[key_len:key_len + 1][0] for k in candidate_keys]

        candidate_list = []
        for c in candidate_words:
            for s in synonym_list:
                if c in s:
                    candidate_list += s


    candidate_list = list(set(candidate_list))

    if len(candidate_list) == 0:
        return [None, 'not_detected']

#    print(candidate_list)
    matchedText = word_match(matchedKey, text, candidate_list)
#    print(matchedText)
    if matchedText is not None:
        key_status = check_completion(matchedText, key_list, synonym_list)
        return [matchedText, key_status]
    else:
        return [None, 'not_detected']


if __name__ == '__main__':
    a, b = key_match_score('description',matchedKey='')
    print(a, b)
# okay decompiling key_match_score.cpython-36.pyc
