# uncompyle6 version 3.3.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.15 |Anaconda, Inc.| (default, Feb 21 2019, 11:55:13) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: C:\Users\DarshilKapadia\Desktop\RICOH\Ricoh_Digitization\codes\xml2json_datacap.py
# Compiled at: 2019-07-01 14:42:44
# Size of source mod 2**32: 2428 bytes
"""
@author: VikramGaddam
"""
import xmltodict, json
from unidecode import unidecode as u
from .barcode_detection import get_barcode_coords

def is_XinBarcode(x,b_list):
    flag=False
    for b in b_list:
        if b[0]<x[0] and b[1]<x[1] and b[2]>x[2] and b[3]>x[3]:
            flag=True
    return flag
def convert(xml_path, json_path,image_path):
    print("image_path: ", image_path)
    barcode_coords = get_barcode_coords(image_path)
    with open(xml_path, 'rb') as (f):
        d = xmltodict.parse(f, xml_attribs=True, attr_prefix='')
    myDict = dict()
    pageNew = dict()
    pageNew['LineList'] = []
    lineList = []
    l_cnt = 0
    blocks = d['CCO']['L']
    if type(blocks) is not list:
        blocks = [
         blocks]
    for i in range(len(blocks)):
        block = blocks[i]
        line_list = block
        if type(line_list) is not list:
            line_list = [
             line_list]
        for j in range(len(line_list)):
            line = line_list[j]
            lx1, ly1, lx2, ly2 = (int(line['l']), int(line['t']), int(line['r']), int(line['b']))
            if is_XinBarcode([lx1, ly1, lx2, ly2],barcode_coords):
                continue
            lineNew = dict()
            lineNew['LineStartX'] = lx1
            lineNew['LineStartY'] = ly1
            lineNew['LineWidth'] = lx2 - lx1
            lineNew['LineHeight'] = ly2 - ly1
            lineNew['Header'] = False
            lineNew['Footer'] = False
            lineNew['Table'] = False
            lineNew['LineID'] = l_cnt
            wordlist = line['W']
            wordNew_list = []
            if type(wordlist) is not list:
                wordlist = [
                 wordlist]
            for k in range(len(list(wordlist))):
                word = wordlist[k]
                wx1, wy1, wx2, wy2 = (int(word['l']), int(word['t']), int(word['r']), int(word['b']))
                if is_XinBarcode([wx1, wy1, wx2, wy2],barcode_coords):
                    continue
                wordNew = dict()
                wordNew['WordStartX'] = wx1
                wordNew['WordStartY'] = wy1
                wordNew['WordWidth'] = wx2 - wx1
                wordNew['WordHeight'] = wy2 - wy1
                wordNew['WordValue'] = u(word['#text'])
                wordNew_list.append(wordNew)

            lineNew['WordList'] = wordNew_list
            l_cnt += 1
            lineList.append(lineNew)

    lineList = sorted(lineList, key=(lambda l: int(l['LineStartY'])))
    pageNew['LineList'] = lineList
    pageNew['PageStartX'] = 0
    pageNew['PageStartY'] = 0
    myDict['page'] = [
     pageNew]
    f = open(json_path, 'w')
    f.write(json.dumps(myDict, indent=2))
    return False


if __name__ == '__main__':
    xml_path = './new_format.xml'
    json_path = './new_format.json'
    page = convert(xml_path, json_path, '')
# okay decompiling xml2json_datacap.cpython-36.pyc
