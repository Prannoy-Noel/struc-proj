# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 09:10:12 2019

@author: MineshGandhi
"""

from .barcode_detection import get_barcode_coords
import xmltodict
import json
from unidecode import unidecode as u


def is_XinBarcode(x,b_list):
    flag=False
    for b in b_list:
        if b[0]<x[0] and b[1]<x[1] and b[2]>x[2] and b[3]>x[3]:
            flag=True
    return flag
def convert1(xml_path, json_path,image_path):
    barcode_coords = get_barcode_coords(image_path)
    with open(xml_path, "rb") as f:    # notice the "rb" mode
        d = xmltodict.parse(f, xml_attribs=True, attr_prefix='')
    myDict = dict()

    pageNew=dict()
    pageNew['LineList']=[]
    lineList=[]
    l_cnt=0


    tables = []
    try:
        tables=d['Page']['Table']
    except:
        pass
    if type(tables) is not list:
            tables=[tables]
    for table in tables:
        rows=table['Row']
        if type(rows) is not list:
            rows=[rows]
        for row in rows:
            cells=row['Cell']
            if type(cells) is not list:
                cells=[cells]
            for cell in cells:
                if('L' in cell.keys()):
                    line_list=cell['L']
                    if type(line_list) is not list:
                        line_list=[line_list]
                    #print(line_list)
                    for j in range(len(line_list)):
                        line=(line_list[j])
                        lx1, ly1, lx2, ly2=[int(l) for l in (line['pos']).split(',')]
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
                        #rect=[[lx1,ly1],[lx2,ly1],[lx2,ly2],[lx1,ly2]]
                        #cv2.fillPoly(img,np.array([rect]),(255,255,255))
                        lineNew['LineID'] = l_cnt

                        wordlist=line['W']
                        wordNew_list=[]
                        if type(wordlist) is not list:
                            wordlist = [wordlist]
                        for k in range(len(list(wordlist))):
                            word=(wordlist[k])
                            wx1, wy1, wx2, wy2 = [int(w) for w in word['pos'].split(',')]
                            if is_XinBarcode([wx1, wy1, wx2, wy2],barcode_coords):
                                continue
                            wordNew = dict()
                            wordNew['WordStartX'] = wx1
                            wordNew['WordStartY'] = wy1
                            wordNew['WordWidth'] = wx2 - wx1
                            wordNew['WordHeight'] = wy2 - wy1
                            wordNew['WordValue']=u(word['v'])
                            wordNew_list.append(wordNew)
                        lineNew['WordList'] = wordNew_list
                        l_cnt+=1
                        lineList.append(lineNew)
    blocks = []
    try:
        blocks=d['Page']['Block']
    except: pass
    if type(blocks) is not list:
            blocks=[blocks]
    for i in range(len(blocks)):
        block=blocks[i]
        line_list=block['L']
        if type(line_list) is not list:
            line_list=[line_list]
        for j in range(len(line_list)):

                line=(line_list[j])
                lx1, ly1, lx2, ly2=[int(l) for l in (line['pos']).split(',')]
                lineNew = dict()
                lineNew['LineStartX'] = lx1
                lineNew['LineStartY'] = ly1
                lineNew['LineWidth'] = lx2 - lx1
                lineNew['LineHeight'] = ly2 - ly1
                lineNew['Header'] = False
                lineNew['Footer'] = False
                lineNew['Table'] = False
                #rect=[[lx1,ly1],[lx2,ly1],[lx2,ly2],[lx1,ly2]]
                #cv2.fillPoly(img,np.array([rect]),(255,255,255))
                lineNew['LineID'] = l_cnt

                wordlist=line['W']
                wordNew_list=[]
                if type(wordlist) is not list:
                    wordlist = [wordlist]
                for k in range(len(list(wordlist))):
                    word=(wordlist[k])
                    wx1, wy1, wx2, wy2 = [int(w) for w in word['pos'].split(',')]
                    wordNew = dict()
                    wordNew['WordStartX'] = wx1
                    wordNew['WordStartY'] = wy1
                    wordNew['WordWidth'] = wx2 - wx1
                    wordNew['WordHeight'] = wy2 - wy1
                    wordNew['WordValue']=u(word['v'])
                    wordNew_list.append(wordNew)
                lineNew['WordList'] = wordNew_list
                l_cnt+=1
                lineList.append(lineNew)
    lineList = sorted(lineList, key=lambda l: int(l['LineStartY']))

    pageNew['LineList'] = lineList
    pageNew['PageStartX'] = 0
    pageNew['PageStartY'] = 0
    #pageNew['PageWidth'] = img.shape[1]
    #pageNew['PageHeight'] = img.shape[0]
    myDict['page'] = [pageNew]

    f = open(json_path, "w")
    f.write(json.dumps(myDict,indent=2))
    return False



if __name__  == '__main__':
    xml_path = 'C:/Users/PrachiRani/Documents/SametimeFileTransfers/TM000002_layout.xml'
    json_path = 'C:/Users/PrachiRani/Documents/SametimeFileTransfers/3.json'
    page = convert(xml_path, json_path,"")
