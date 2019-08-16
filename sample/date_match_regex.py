# uncompyle6 version 3.3.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.15 |Anaconda, Inc.| (default, Feb 21 2019, 11:55:13) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: C:\Users\DarshilKapadia\Desktop\RICOH\Ricoh_Digitization\codes\date_match_regex.py
# Compiled at: 2019-03-13 14:40:48
# Size of source mod 2**32: 2454 bytes
"""
Created on Thu Mar 15 12:20:28 2018

@author: Manasi
"""
import re

def date_match_regex(text):
    dayRegex = '(' + '|'.join([str(i) for i in range(1, 32)] + ['0' + str(i) for i in range(1, 10)]) + ')'
    monthRegexNumber = '(' + '|'.join([str(i) for i in range(1, 13)] + ['0' + str(i) for i in range(1, 10)]) + ')'
    monthRegexLong = '(january|february|march|april|may|june|july|august|september|october|november|december|Ju/l)'
    monthRegexShort = '(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)'
    monthRegexText = '(' + monthRegexLong + '|' + monthRegexShort + ')'
    yearRegex = '(' + '|'.join([str(i) for i in range(1950, 3001)] + ['0' + str(i) for i in range(0, 10)] + [str(i) for i in range(10, 100)]) + ')'
    format0 = dayRegex + u'[/1\u2014-]' + monthRegexNumber + u'[/1\u2014-]' + yearRegex
    format1 = monthRegexText + dayRegex + ',' + yearRegex
    format2 = dayRegex + monthRegexLong + yearRegex
    format3 = dayRegex + '-' + monthRegexShort + '-' + yearRegex
    format4 = dayRegex + '-' + monthRegexLong + '-' + yearRegex
    format5 = dayRegex + '\\.' + monthRegexNumber + '\\.' + yearRegex
    format6 = monthRegexNumber + u'[/1\u2014-]' + dayRegex + u'[/1\u2014-]' + yearRegex
    format7 = yearRegex + u'[/\u2014-]' + dayRegex + u'[/\u2014-]' + monthRegexNumber
    format8 = dayRegex + monthRegexShort + yearRegex
    format9 = yearRegex + u'[.\u2014-]' + monthRegexNumber + u'[.\u2014-]' + dayRegex
    dateRegex = [
     format0, format1, format2, format3, format4, format5, format6, format8]
    in_date = text.replace(' ', '').replace('?', '7').replace('/l', 'l').lower()
    matches = []
    for f in dateRegex:
        match = re.match(f, in_date)
        if match is not None:
            mg = [item.title() for item in list(match.groups()) if item is not None]
            date = '/'.join(mg)
            if date != '':
                matches.append(date)

    return matches


def date_match_regex_sec(text):
    re_date = u'\\d\\s?\\d\\s?[-]?[\u2014]?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\s?[-]?[\u2014]?\\d{3,}'
    result = bool(re.match(re_date, text))
    return result


if __name__ == '__main__':
    text = '05/09/19'
    matches = date_match_regex(text)
    print(date_match_regex(text))
    if matches == []:
        print('Empty text')
        result = date_match_regex_sec(text)
        print(result)
# okay decompiling date_match_regex.cpython-36.pyc
