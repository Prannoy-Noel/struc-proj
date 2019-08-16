# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 22:31:55 2019

@author: DarshilKapadia
"""

import re

def tax_key_regex(text):
    
    match = re.match('^ *@* *\(*\d{0,2} *[.,]* *\d{0,2} *% *\)*$',text)
    return match





if __name__ == '__main__':
    text = '(12 %)'
    
    xx = tax_key_regex(text)