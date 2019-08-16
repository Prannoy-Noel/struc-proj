# uncompyle6 version 3.3.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.15 |Anaconda, Inc.| (default, Feb 21 2019, 11:55:13) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: C:\Users\DarshilKapadia\Desktop\RICOH\Ricoh_Digitization\codes\word_match.py
# Compiled at: 2019-07-01 11:05:30
# Size of source mod 2**32: 971 bytes
"""
Created on Thu Mar  8 14:32:57 2018

@author: Darshil
"""
import difflib

def wordLen_thresh_map(x):
    mapping = {0:1, 
     1:1,  2:1,  3:1,  4:1,  5:1,  6:1,  7:1}
    if x >= 8:
        y = 0.9
    else:
        y = mapping[x]
    return y


def word_match(matchedKey, text, candidate_list):
    scores = []
    for k_idx, cand in enumerate(candidate_list):
        if matchedKey is not '':
            cand = matchedKey + ' ' + cand
        scores.append(difflib.SequenceMatcher(None, text.lower().replace(' ',''), cand.lower().replace(' ','')).ratio())

    max_score = max(scores)
    if max_score >= wordLen_thresh_map(len(text.strip().replace(' ',''))):
        matchedText = (matchedKey + ' ' + candidate_list[scores.index(max_score)]).strip()
    else:
        matchedText = None
    return matchedText


if __name__ == '__main__':
    matchedKey = ''
    text = 'lmv'
    candidate_list = ['Inv']
    matchedText = word_match(matchedKey, text, candidate_list)
    print(matchedText)
# okay decompiling word_match.cpython-36.pyc
