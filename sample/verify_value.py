# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 17:55:23 2019

@author: PrachiRani
"""
from .date_match_regex import date_match_regex
from .date_match_regex import date_match_regex_sec
from .amount_regex import is_amount
from .swift_regex import is_swift

currency_list = ['usd','aud','euro','eur']

def verify_value(key_type,val):
    if key_type == 'Date':
        res = date_match_regex(val)
        if res!=[]:
            return True
        else:
            res = date_match_regex_sec(val)
            return res
    elif key_type == 'AlphaNumeric':
        print(val)
        cnt_ch=0
        cnt_num=0
        for ch in val:
            if (64< ord(ch)< 92):
                cnt_ch+=1
            elif (47< ord(ch)<58):
                cnt_num+=1
#        print((cnt_ch>=0 and cnt_num>1 and len(val) > 4 and val.count(' ')<2))
        return (cnt_ch>=0 and cnt_num>1 and len(val) > 4 and val.count(' ')<2)
    elif key_type == 'Currency':
        return is_amount(val)

    elif key_type == 'Fix List':
        if val.lower() in currency_list:
            return True
        else:
            return False
    elif key_type == 'Adress':
        return True
    elif key_type == 'Blob':
        return True
    elif key_type == 'Number':

        if val.count(',')<2 :
            val=val.replace(',','')
#        print("number check",val)
        try:
            float(val)
            return True
        except:
            return False

    elif key_type == 'Swift':
        return is_swift(val)
    else:
        return True
#def verify_value(key,val):
#    text = str(val)
#
#    if key == 'Invoice Date':
#        res = date_match_regex(text)
#        if res!=[]:
#            return True
#        else:
#            res = date_match_regex_sec(text)
#            return res
#    elif key == 'Invoice Number':
#        cnt=0
#        for ch in text:
#            if (64< ord(ch)< 92):
#                cnt-=1
#            elif (47< ord(ch)<58):
#                cnt+=1
##        print(cnt)
#        return (cnt>0 and len(set(text)) > 1)
#    elif key == "PO Number"  or key == "Supplier IBAN":
#        cnt=0
#        cnt_num = 0
#        for ch in text:
#            if (64< ord(ch)< 92) or ord(ch) == 32:
#                cnt-=1
#            elif (47< ord(ch)<58):
#                cnt+=1
#            if (47< ord(ch)<58):
#                cnt_num+=1
#            else:
#                cnt_num-=1
#        return (cnt>0 and len(text) > 1 and cnt_num>0)
#    elif key in ["Supplier Tax Number","Invoice Tax Amount","Invoice Total","Invoice Net"]:
#        res = is_amount(text.replace(' ',''))
#        return res
#    elif key == "Supplier Bank Account Number":
#        if len(text.replace(' ',''))>2:
#            res = is_amount(text.replace(' ',''))
#            return res
#        else:
#            return False
#    elif key == "Supplier Swift Code":
#        res = is_swift(text)
#        return res
#    elif key=="Currency":
##        print("qqqqqqqqqqqqq -> ", text)
#        if text.lower()=="usd" or text.lower()=='us. dollar' or text.lower()=='us.' or text.lower()=='us' or text.lower()=='u.s.' or text.lower() == 'myr' or text.lower() == 'eur' or text.lower() =='euro' or text.lower() =='aud' or text.lower() =='australian' or  text.lower() =='dollar' :
#            return True
#        else:
#            return False
#    else:
#        return True
if __name__ == '__main__':
    verify_value('AlphaNumeric','54^5242001')
