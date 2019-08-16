# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 14:14:42 2018

@author: Naman
"""

import re

def is_swift(text):
    re_swift = r'^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{2}[A-Z0-9a-z]{1})?[,.;\]]?$'
    re_swift2 = r'^[A-Z]{5}[A-Z0-9]{2}([A-Z0-9]{1};?)$'
#    a = re.search('\]$')
    result = bool(re.match(re_swift, text))
    
    if result == False:
        result = bool(re.match(re_swift2, text))
    return result
    
    
if __name__ == "__main__":
    text = "CITIAUZ2X"
    res = is_swift(text)
    print(res)